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
from app.schemas.productos_schemas import ProductoBase, ProductoDTO, ProductoUpdate,ProductoCreate, EliminarProductoRequest, Categoria, Tipo,RecetaIngredienteUpdate, RecetaIngredienteDTO
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
from email.mime.base import MIMEBase
from email import encoders
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from decimal import Decimal
from app.schemas.alerta_schemas import EmailRequest
from typing import List
from app.api.endpoints.materia_prima import verificar_stock_bajo


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
    precio_entrada: Optional[float] =Form(None),
    precio_salida: float = Form(...),
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
            precio_entrada= precio_entrada,
            precio_salida=precio_salida,
            id_usuario=id_usuario,
            ruta_imagen=image_path,
            tipo=tipo,
            stock_minimo=stock_minimo
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)

        materias_prima_afectadas = []  # Para rastrear qué materias primas verificar, y enviar alertas
        
        # Add recipe ingredients if HECHO type
        if tipo == Tipo.HECHO:
            _add_recipe_ingredients(db, producto.id, ingredientes_list)
             
            # Obtener las IDs de las materias primas utilizadas
            materias_prima_afectadas = [ingrediente["materia_prima_id"] for ingrediente in ingredientes_list]
            
            # Prepare initial product if requested
            if preparar_inicial and cantidad > 0:
                try:
                    mensaje = producto.preparar_producto(cantidad)
                    db.commit()

                    for materia_id in materias_prima_afectadas:
                        verificar_stock_bajo(db, materia_id)

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
            "precio_salida": float(producto.precio_salida),
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
    producto_existente = db.query(Productos).filter(Productos.id == id).first()
    if not producto_existente:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Guardar la cantidad anterior para calcular la diferencia
    cantidad_anterior = producto_existente.cantidad
    
    # Actualizar campos básicos
    if producto.nombre is not None:
        producto_existente.nombre = producto.nombre
    if producto.cantidad is not None:
        producto_existente.cantidad = producto.cantidad
    if producto.categoria is not None:
        producto_existente.categoria = producto.categoria
    if producto.precio_unitario is not None:
        producto_existente.precio_unitario = producto.precio_unitario
    if producto.stock_minimo is not None:
        producto_existente.stock_minimo = producto.stock_minimo
    if producto.tipo is not None:
        producto_existente.tipo = producto.tipo
    
    # Si es un producto tipo "HECHO" y hay ingredientes, actualizar la receta
    if producto_existente.tipo == "HECHO" and producto.ingredientes is not None:
        # Eliminar ingredientes existentes
        db.query(MateriaPrimaRecetas).filter(
            MateriaPrimaRecetas.producto_id == id
        ).delete()
        
        # Agregar los nuevos ingredientes
        for ingrediente in producto.ingredientes:
            # Verificar compatibilidad de unidades
            materia_prima = db.query(MateriaPrima).filter(
                MateriaPrima.id == ingrediente.materia_prima_id
            ).first()
            
            if not materia_prima:
                raise HTTPException(status_code=404, detail=f"Materia prima no encontrada")
                
            # Validar compatibilidad de unidades
            if ingrediente.unidad_id:
                unidad = db.query(UnidadMedida).filter(UnidadMedida.id == ingrediente.unidad_id).first()
                if not unidad:
                    raise HTTPException(status_code=404, detail=f"Unidad no encontrada")
                
                if unidad.tipo_medida != materia_prima.unidad.tipo_medida:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Unidades incompatibles: {unidad.tipo_medida} y {materia_prima.unidad.tipo_medida}"
                    )
            
            # Agregar ingrediente a la receta
            nueva_receta = MateriaPrimaRecetas(
                producto_id=id,
                materia_prima_id=ingrediente.materia_prima_id,
                cantidad_ingrediente=ingrediente.cantidad_ingrediente,
                unidad_id=ingrediente.unidad_id
            )
            db.add(nueva_receta)

    # Lista para rastrear las materias primas afectadas
    materias_prima_afectadas = []
    
    # Si cambió la cantidad y es un producto HECHO, ajustar materias primas
    if producto_existente.tipo == "HECHO" and producto.cantidad is not None and producto.cantidad != cantidad_anterior:
        # Calcular cuántas unidades nuevas se producen
        unidades_producidas = producto.cantidad - cantidad_anterior
        
        if unidades_producidas > 0:  # Solo si se aumenta la cantidad, consumir materia prima
            # Obtener ingredientes actualizados
            ingredientes = db.query(MateriaPrimaRecetas).filter(
                MateriaPrimaRecetas.producto_id == id
            ).all()
            
            # Verificar y actualizar stock de materias primas
            for ingrediente in ingredientes:
                materia_prima = db.query(MateriaPrima).filter(
                    MateriaPrima.id == ingrediente.materia_prima_id
                ).first()
                
                # Calcular cantidad necesaria para las nuevas unidades
                cantidad_necesaria = ingrediente.cantidad_ingrediente * Decimal(unidades_producidas)
                
                # Obtener unidad si es diferente
                unidad = None
                if ingrediente.unidad_id and ingrediente.unidad_id != materia_prima.unidad_id:
                    unidad = db.query(UnidadMedida).filter(
                        UnidadMedida.id == ingrediente.unidad_id
                    ).first()
                
                try:
                    # Reducir stock de materia prima
                    materia_prima.reducir_stock(
                        cantidad=cantidad_necesaria,
                        unidad=unidad
                    )

                    # Agregar materia prima a la lista de afectadas
                    materias_prima_afectadas.append(materia_prima.id)
                except ValueError as e:
                    # Si no hay suficiente stock, revertir la operación y enviar alerta
                    raise HTTPException(status_code=400, detail=str(e))

    
    db.commit()
    db.refresh(producto_existente)

    for materia_id in materias_prima_afectadas:
        verificar_stock_bajo(db, materia_id)
    
    return producto_existente

@router_productos.get("/{id}/receta", response_model=List[RecetaIngredienteDTO])
def obtener_receta_producto(id: int, db: session = Depends(get_db)):
    # Verificar si el producto existe
    producto = db.query(Productos).filter(Productos.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar si el producto es de tipo HECHO
    if producto.tipo != "HECHO":
        return []
    
    # Obtener los ingredientes de la receta
    ingredientes = db.query(MateriaPrimaRecetas).filter(
        MateriaPrimaRecetas.producto_id == id
    ).all()
    
    return ingredientes


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

def create_message(sender, to, subject, message_text, attachment_path=None):
    message=MIMEMultipart()
    message['to']=to
    message['from']=sender
    message['subject']=subject

    #Agregar el texto del correo
    msg = MIMEText(message_text, 'html')
    message.attach(msg)

    #si se proporciona un archivo adjuntarlo
    if attachment_path:
        print(f"Intentando adjuntar: {attachment_path}")
        exists = os.path.exists(attachment_path)
        print(f"¿El archivo existe?: {exists}")
        
        if exists:
            with open(attachment_path, "rb") as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
                message.attach(part)  # AÑADIDA ESTA LÍNEA CRUCIAL
                print(f"Archivo adjuntado correctamente: {os.path.basename(attachment_path)}")
        else:
            print(f"¡ADVERTENCIA! El archivo no existe: {attachment_path}")
    #codificar el mensaje en base64
    raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode('utf-8')
    return {'raw': raw_message}


def send_message(service,user_id,message):
    try:
        message=service.users().messages().send(userId=user_id,body=message).execute()
        return message
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error al enviar el correo: {str(e)}")

async def send_email_task(email_request: EmailRequest, attachment_path: str = None):
    try:
        service = get_email_service()
        sender = "sergiogarcia3421@gmail.com"
        message = create_message(
            sender,
            email_request.to_email,
            email_request.subject,
            email_request.message,
            attachment_path=attachment_path
        )
        send_message(service, "me", message)
    except Exception as e:
        print(f"Error en tarea de segundo plano: {e}")
        traceback.print_exc()


@router_productos.post("/send-email")
async def send_email(emailRequest:EmailRequest,background_tasks:BackgroundTasks, attachment_path:str=None):
    try:
        #enviar los correos en segundo plano para no bloquear la respuesta api
        background_tasks.add_task(send_email_task,emailRequest, attachment_path)
        return{"status":"success", "message": "Correo Programado para envio"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error al programar el envio {e}")