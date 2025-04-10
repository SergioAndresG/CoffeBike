from fastapi import APIRouter, HTTPException, FastAPI, Depends, Form, UploadFile, File, BackgroundTasks
from typing import Optional
from app.conexion import get_db
from app.models.usuario import Usuarios
from app.models.productos import Productos
from app.models.alertas import Alertas
from app.models.detalle_factura import DetalleFactura
from app.models.materia_prima_recetas import MateriaPrimaRecetas
from app.models.materia_prima import MateriaPrima
from app.models.unidad_medida import UnidadMedida
from app.schemas.productos_schemas import ProductoBase, ProductoDTO, ProductoUpdate,ProductoCreate, EliminarProductoRequest, Categoria, Tipo
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import pickle
import base64
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from decimal import Decimal
from app.schemas.alerta_schemas import EmailRequest

app = FastAPI()

router_productos = APIRouter(prefix="/productos", tags=["Productos"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


#ENPOINTS PRODUCTOS 
@router_productos.get("/categorias")
async def obtener_categorias(db: session = Depends(get_db)):
    return [categoria.value for categoria in Categoria]

@router_productos.get("/")
async def consultar(db: session = Depends(get_db)):
    # Aquí se consulta la base de datos usando SQLAlchemy
    productos = db.query(Productos).all()  
    return productos
@router_productos.post("/", response_model=ProductoCreate)
async def agregar_producto(
    nombre: str = Form(...),
    cantidad: int = Form(...),
    categoria: Categoria = Form(...),
    stock_minimo: int = Form(...),
    tipo: Tipo = Form(...),
    precio_unitario: float = Form(...),
    id_usuario: int = Form(...),
    ingredientes: Optional[str] = Form(None),  # JSON con los ingredientes
    preparar_inicial: bool = Form(False),  # Default value to avoid None
    file: Optional[UploadFile] = File(None),
    db: session = Depends(get_db)
):
    """
    Endpoint para agregar un nuevo producto con validación de ingredientes y
    posibilidad de procesamiento inicial.
    """
    # Pse procesa la imagen si se envia desde el frontend
    image_path = None
    if file:
        try:
            image_path = f"imagesP/{file.filename}"
            with open(image_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

    # Process and validate ingredients for HECHO type products
    # prceso y validacion de ingredientes para los products de tipo hecho
    ingredientes_list = []
    if tipo == Tipo.HECHO:
        if not ingredientes:
            raise HTTPException(status_code=400, detail="Los ingredientes son obligatorios para productos tipo HECHO")
        
        # Parse and validate ingredients
        ingredientes_list = _parse_and_validate_ingredients(ingredientes, db)

    try:
        # Initialize with proper quantity
        cantidad_inicial = cantidad if not (tipo == Tipo.HECHO and preparar_inicial) else 0
        
        # Create product
        producto = Productos(
            nombre=nombre,
            cantidad=cantidad_inicial,
            categoria=categoria,
            precio_unitario=precio_unitario,
            id_usuario=id_usuario,
            ruta_imagen=image_path,
            tipo=tipo,
            stock_minimo=stock_minimo
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)
        
        # Add recipe ingredients if HECHO type
        if tipo == Tipo.HECHO:
            _add_recipe_ingredients(db, producto.id, ingredientes_list)
            
            # Prepare initial product if requested
            if preparar_inicial and cantidad > 0:
                try:
                    mensaje = producto.preparar_producto(cantidad)
                    db.commit()
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
        
        # Build and return response
        return _build_product_response(db, producto)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al guardar producto: {str(e)}")


def _parse_and_validate_ingredients(ingredientes_json, db):
    """Helper function to parse and validate ingredients JSON"""
    try:
        ingredientes_list = json.loads(ingredientes_json)
        if not isinstance(ingredientes_list, list):
            raise HTTPException(status_code=400, detail="Formato incorrecto de ingredientes")
        
        # Collect all materia_prima_ids and unidad_ids for batch fetching
        materia_prima_ids = [ing.get("materia_prima_id") for ing in ingredientes_list]
        unidad_ids = [ing.get("unidad_id") for ing in ingredientes_list if ing.get("unidad_id")]
        
        # Batch fetch all materias primas and unidades to avoid N+1 queries
        materias_primas = {mp.id: mp for mp in db.query(MateriaPrima).filter(MateriaPrima.id.in_(materia_prima_ids)).all()}
        unidades = {u.id: u for u in db.query(UnidadMedida).filter(UnidadMedida.id.in_(unidad_ids)).all()} if unidad_ids else {}
        
        # Validate each ingredient
        for ingrediente in ingredientes_list:
            materia_prima_id = ingrediente.get("materia_prima_id")
            unidad_id = ingrediente.get("unidad_id")
            
            if materia_prima_id is None:
                raise HTTPException(status_code=400, detail="ID de materia prima no puede ser None")
            
            # Check if materia prima exists
            materia_prima = materias_primas.get(materia_prima_id)
            if not materia_prima:
                raise HTTPException(status_code=404, detail=f"Materia prima con ID {materia_prima_id} no encontrada")
            
            # Check unit compatibility if provided
            if unidad_id:
                unidad_medida = unidades.get(unidad_id)
                if not unidad_medida:
                    raise HTTPException(status_code=400, detail=f"Unidad de medida con ID {unidad_id} no encontrada")
                
                if unidad_medida.tipo_medida != materia_prima.unidad.tipo_medida:
                    raise HTTPException(
                        status_code=400,
                        detail=f"No se puede convertir entre {unidad_medida.tipo_medida} y {materia_prima.unidad.tipo_medida}, Medidas de diferente tipo"
                    )
        
        return ingredientes_list
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error en el formato del JSON de ingredientes")


def _add_recipe_ingredients(db, producto_id, ingredientes_list):
    """Helper function to add recipe ingredients to database"""
    for ingrediente in ingredientes_list:
        receta = MateriaPrimaRecetas(
            producto_id=producto_id,
            materia_prima_id=ingrediente["materia_prima_id"],
            cantidad_ingrediente=ingrediente["cantidad_ingrediente"],
            unidad_id=ingrediente.get("unidad_id")
        )
        db.add(receta)
    db.commit()


def _build_product_response(db, producto):
    """Helper function to build product response with ingredients if needed"""
    respuesta = {
        "id": producto.id,
        "nombre": producto.nombre,
        "categoria": producto.categoria,
        "precio_unitario": float(producto.precio_unitario),
        "tipo": producto.tipo,
        "stock_minimo": producto.stock_minimo,
        "ruta_imagen": producto.ruta_imagen,
        "id_usuario": producto.id_usuario,
        "cantidad": producto.cantidad
    }

    if producto.tipo == Tipo.HECHO:
        # Fetch all recipe ingredients in one query
        recetas = db.query(MateriaPrimaRecetas).filter(MateriaPrimaRecetas.producto_id == producto.id).all()
        
        # Get all related materias primas and unidades in batch
        materia_prima_ids = [receta.materia_prima_id for receta in recetas]
        unidad_ids = [receta.unidad_id for receta in recetas if receta.unidad_id]
        
        materias_primas = {mp.id: mp for mp in db.query(MateriaPrima).filter(MateriaPrima.id.in_(materia_prima_ids)).all()}
        unidades = {u.id: u for u in db.query(UnidadMedida).filter(UnidadMedida.id.in_(unidad_ids)).all()} if unidad_ids else {}
        
        # Build ingredients data
        ingredientes_data = []
        for receta in recetas:
            materia_prima = materias_primas.get(receta.materia_prima_id)
            unidad_receta = unidades.get(receta.unidad_id) if receta.unidad_id else None
            
            ingredientes_data.append({
                "id": receta.id,
                "materia_prima_id": receta.materia_prima_id,
                "nombre_materia": materia_prima.nombre if materia_prima else "Desconocido",
                "cantidad": float(receta.cantidad_ingrediente),
                "unidad_medida": receta.unidad_id if receta.unidad_id else (materia_prima.unidad_id if materia_prima else None),
                "unidad_id": receta.unidad_id if receta.unidad_id else (materia_prima.unidad_id if materia_prima else None),
                "unidad_simbolo": unidad_receta.simbolo if unidad_receta else (materia_prima.unidad.simbolo if materia_prima else "Desconocido")
            })
        
        respuesta["ingredientes"] = ingredientes_data
    
    return respuesta


@router_productos.patch("/{id}", response_model=ProductoDTO)
def actualizar_producto(id: int, producto: ProductoUpdate, db: session = Depends(get_db)):
        # Imprimir los datos recibidos para depuración
        print("Datos recibidos:", producto.dict(exclude_unset=True))
        
        # Buscar el producto por ID
        producto_existente = db.query(Productos).filter(Productos.id == id).first()
        if not producto_existente:
            raise HTTPException(
                status_code=404, detail="Producto no encontrado")
    
        # Convertir los datos a un diccionario, excluyendo valores no establecidos
        producto_data = producto.dict(exclude_unset=True)

        for campo, valor in producto_data.items():
            if valor is not None:
                setattr(producto_existente, campo, valor)
    
        db.commit()
        db.refresh(producto_existente)

        return producto_existente



@router_productos.delete("/eliminar")
async def eliminar_producto(data: EliminarProductoRequest, db: session = Depends(get_db)):
    # Buscar al único usuario con el rol "JEFE"
    jefe = db.query(Usuarios).filter(Usuarios.rol == "JEFE").first()
    if not jefe:
        raise HTTPException(status_code=404, detail="No se encontró ningún usuario con el rol Jefe.")

    # Validar que la contraseña proporcionada coincide con la del Jefe
    if jefe.contraseña != data.contraseñaProporcionada:
        raise HTTPException(status_code=403, detail="Acceso denegado: Solo el jefe puede eliminar productos.")

    # Buscar el producto que se quiere eliminar
    producto = db.query(Productos).filter(Productos.id == data.idProductoaEliminar).first()

    #Eliminar las recetas relacionadas con ese producto
    db.query(MateriaPrimaRecetas).filter(MateriaPrimaRecetas.producto_id == data.idProductoaEliminar).delete()

    #Actualizar el id en detalle de factura
    db.query(DetalleFactura).filter(DetalleFactura.producto_id == data.idProductoaEliminar).update({"producto_id": None})

    #Eliminar alertas relacionadas con el producto
    db.query(Alertas).filter(Alertas.producto_id == data.idProductoaEliminar).delete()

    if not producto:
        raise HTTPException(status_code=404, detail="No se encontró un producto con el id especificado.")
    
    # Eliminar el producto
    db.delete(producto)
    db.commit()

    return {"message": f"Producto con ID {data.idProductoaEliminar} eliminado correctamente."}


#Endpoints para obtener por Id, Cantidad y Nombre del producto
@router_productos.get("/{id}", response_model=ProductoDTO)
def obtener_producto_por_id(id: int, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su ID
    producto = db.query(Productos).filter(Productos.id == id).first()
    
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado con el ID: {id}")
    
    return producto

@router_productos.get("/{cantidad}", response_model=ProductoDTO)
def obtener_producto_por_cantidad(cantidad: int, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su cantidad
    producto = db.query(Productos).filter(Productos.cantidad == cantidad).first()
    
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto no encontrado con esa cantidad: {cantidad}")
    
    return producto

@router_productos.get("/consulta-nombre/{nombre}", response_model=ProductoDTO)
def obtener_producto_por_nombre(nombre: str, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su nombre
    producto = db.query(Productos).filter(Productos.nombre == nombre).first()
    
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto no encontrado con ese nombre: {nombre}")
    
    return producto

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PATH = 'token.pickle'
CREDENTIALS_PATH = 'credentials.json'

def get_email_service():
    creds = None
    #Intenta guardar las credenciales guardadas
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    #si no hay credenciales validas disponibles, deja que el usuario inicie sesion
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH,SCOPES)
            creds = flow.run_local_server(port=0)

        #Guarda las credenciales para la proxima vez 
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    message=MIMEMultipart()
    message['to']=to
    message['from']=sender
    message['subject']=subject

    #Agregar el texto del correo
    msg = MIMEText(message_text, 'html')
    message.attach(msg)

    #codificar el mensaje en base64
    raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')
    return {'raw':str(raw_message)}


def send_message(service,user_id,message):
    try:
        message=service.users().messages().send(userId=user_id,body=message).execute()
        return message
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {str(e)}")

async def send_email_task(email_request:EmailRequest):
    try:
        service=get_email_service()
        sender="sergiogarcia3421@gmail.com"
        message=create_message(sender,email_request.to_email, email_request.subject, email_request.message)
        send_message(service,"me",message)
    except Exception as e:
        print(f"Error en tarea de segundo plano: {e}")
        traceback.print_exc()

@router_productos.post("/send-email")
async def send_email(emailRequest:EmailRequest,background_tasks:BackgroundTasks):
    try:
        #enviar los correos en segundo plano para no bloquear la respuesta api
        background_tasks.add_task(send_email_task,emailRequest)
        return{"status":"success", "message": "Correo Programado para envio"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al programar el envio {e}")