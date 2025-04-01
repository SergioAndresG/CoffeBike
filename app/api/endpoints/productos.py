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
    preparar_inicial: bool = Form(None),
    file: Optional[UploadFile] = File(None),
    db: session = Depends(get_db)
):
    # Procesar la imagen si se proporciona
    image_path = None
    if file:
        try:
            image_path = f"imagesP/{file.filename}"
            with open(image_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

    # Validar ingredientes antes de guardar el producto**
    ingredientes_list = []
    if tipo == Tipo.HECHO:
        if not ingredientes:
            raise HTTPException(status_code=400, detail="Los ingredientes son obligatorios para productos tipo HECHO")

        try:
            ingredientes_list = json.loads(ingredientes)
            if not isinstance(ingredientes_list, list):
                raise HTTPException(status_code=400, detail="Formato incorrecto de ingredientes")

            for ingrediente in ingredientes_list:
                materia_prima_id = ingrediente.get("materia_prima_id")
                cantidad_ingrediente = ingrediente.get("cantidad_ingrediente")
                unidad_id = ingrediente.get("unidad_id") #para porder usare la conversion

                if materia_prima_id is None:
                    raise HTTPException(status_code=400, detail="ID de materia prima no puede ser None")
                #Verificar que la materia prima exista
                materia_prima = db.query(MateriaPrima).filter(MateriaPrima.id == materia_prima_id).first()
                if not materia_prima:
                    raise HTTPException(status_code=404, detail=f"Materia prima con ID {materia_prima_id} no encontrada")
                
                # Si se proporcina una unidad, verificar que existe y si es compatible
                if unidad_id:
                    unidad_medida = db.query(UnidadMedida).filter(UnidadMedida.id == unidad_id).first()
                    if not unidad_medida:
                        raise HTTPException(status_code=400, detail="Unidad de medida no encontrada")
                    
                    #Verificar compatibilidad entre unidades
                    if unidad_medida.tipo_medida != materia_prima.unidad.tipo_medida:
                        raise HTTPException(status_code=400,detail=f"No se puede convertir entre {unidad_medida.tipo_medida} y {materia_prima.unidad.tipo_medida}, Medidas de diferente tipo")

        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Error en el formato del JSON de ingredientes")

    try:
        #Guardar el producto inicialmente con cantidad 0 si se va a preparar despues
        cantidad_inicial = 0 if (tipo == "HECHO" and preparar_inicial) else cantidad
        #Guardar el producto solo si los ingredientes son válidos
        producto = Productos(
            nombre=nombre,
            cantidad=cantidad,
            categoria=categoria,
            precio_unitario=precio_unitario,
            id_usuario=id_usuario,
            ruta_imagen=image_path,
            tipo=tipo,
            stock_minimo=stock_minimo
        )
        db.add(producto)
        db.commit()
        db.refresh(producto) # Asegura que producto.id esté disponible
        #  Guardar los ingredientes ahora que el producto está confirmado**
        if tipo == Tipo.HECHO:
            for ingrediente in ingredientes_list:
                receta = MateriaPrimaRecetas(
                    producto_id=producto.id,
                    materia_prima_id=ingrediente["materia_prima_id"],
                    cantidad_ingrediente=ingrediente["cantidad_ingrediente"],
                    unidad_id=ingrediente.get("unidad_id") # Puede ser none, en ese caso se usara el tipo de medida de materia prima (base)
                )
                db.add(receta)
            db.commit()
            db.refresh(producto)
            #Si se debe preparar un producto, hacerlos despues de guardar la receta
            if preparar_inicial and cantidad > 0:
                try:
                    mensaje = producto.preparar_producto(cantidad)
                    db.commit()
                except Exception as e:
                    #Si no hay sufucientes ingredientes hacemos rollback y notificamos
                    db.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
        # Construir la respuesta**
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
            #Lista vacia para almacenar los ingredientes
            ingredientes_data = []
            recetas = db.query(MateriaPrimaRecetas).filter(MateriaPrimaRecetas.producto_id == producto.id).all()
            #Bucle para procesar  cada ingrediente
            for receta in recetas:
                #en esta variable almacenamos la unidad de medida del ingrediente
                unidad_receta = None
                if receta.unidad_id:
                    unidad_receta = db.query(UnidadMedida).filter(UnidadMedida.id == receta.unidad_id).first()
                materia_prima = db.query(MateriaPrima).filter(MateriaPrima.id == receta.materia_prima_id).first()
                #se crea un diccionario con la informacion del ingrediente para añadirlo a la lista
                ingredientes_data.append({
                    #Se añade el id de la relacion receta
                    "id": receta.id,
                    #Añade el is de la materia prima (imgrediente)
                    "materia_prima_id": receta.materia_prima_id,
                    #Añade el nombre de la materia 
                    #Si el materia_prima es None (no se encontro), usamos "Desconocido como fallback"
                    "nombre_materia": materia_prima.nombre if materia_prima else "Desconocido",
                    #Se añade la cantidad del ingrediente convertida a float 
                    "cantidad": float(receta.cantidad_ingrediente),
                    #Aca se define la unidad de medida para este ingredinete
                    #si la receta tiene una undiad especifica, usa esa
                    #si no, intenta usar la unuidad asociada a la materia prima.
                    #si tampoco hay materia prima, usa 0 como valor predeterminado
                    "unidad_medida": receta.unidad_id if receta.unidad_id else (materia_prima.unidad_id if materia_prima else 0),
                    #Similar a lo anterior pero devuelve None en lugar de 0 si no hay unidad
                    "unidad_id": receta.unidad_id if receta.unidad_id else (materia_prima.unidad_id if materia_prima else None),
                    #Obtiene el simbolo de la unidad de medida
                    #Si falla intentar obtenerlo desde la unidad aosicada a la materia prima 
                    #si todo falla devuelve un fallvack mencionado anteriormente
                    "unidad_simbolo": unidad_receta.simbolo if unidad_receta else (materia_prima.unidad.simbolo if materia_prima else "Desconocido")

                })
            respuesta["ingredientes"] = ingredientes_data

        return respuesta

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al guardar producto: {str(e)}")


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