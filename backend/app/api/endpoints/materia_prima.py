from fastapi import APIRouter, FastAPI, HTTPException, Depends, File,UploadFile,Form
from typing import Optional, List
from app.conexion import get_db
from app.schemas.materia_schemas import MateriaPrimaCreate, MateriaPrimaDTO, MateriaPrimaResponse, EliminarMateriaRequest, MateriaPrimaUpdate, LoteCreate, MateriaPrimaBase
from app.models.materia_prima import MateriaPrima, LoteMateriaPrima
from app.models.unidad_medida import UnidadMedida
from app.models.usuario import Usuarios
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.responses import JSONResponse
import requests


app = FastAPI()
router_materia = APIRouter(prefix="/materia", tags=["MateriaPrima"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


def verificar_vencimientos(db: session):
    #Verifica las materias primas proximas a vencer y envia alertas
    #Se debe colocar dentro de una funcion text, para que cumpla la sintaxis correcta de la consulta
    mateias = db.execute(text("""
        SELECT
            id,nombre,cantidad,fecha_vencimiento,
            DATEDIFF(fecha_vencimiento, CURDATE()) as dias_restantes
        FROM
            materia_prima
        WHERE
            DATEDIFF(fecha_vencimiento, CURDATE()) <= 7;
    """)).fetchall()

    for materia in mateias:
        if materia.dias_restantes <= 7:
            enviar_alerta_vencimiento(materia, db)

def enviar_alerta_vencimiento(item, db):
    """
    Envía una alerta vía email si el materia prima se va vencer.
    """
    usuario = db.query(Usuarios).filter(Usuarios.rol == "JEFE" and Usuarios.rol == "ADMINISTRADOR").first()
    if usuario and usuario.correo:
        asunto = "¡Alerta de Vencimineto Materia Prima! 🚨"
        mensaje = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                            .container {{ padding: 20px; }}
                            .header {{ font-size: 20px; color: #e53935; font-weight: bold; margin-bottom: 15px; }}
                            .item-name {{ font-size: 18px; font-weight: bold; }}
                            .stock-info {{ margin: 15px 0; padding: 10px; background-color: #f5f5f5; border-left: 4px solid #e53935; }}
                            .icon {{ font-size: 18px; margin-right: 5px; }}
                            .action {{ font-weight: bold; color: #e53935; margin-top: 20px; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">🚨 ¡Alerta de Vencimineto Materia Prima!</div>
                            <p>La fecha de vencimiento de <span class="item-name">{item.nombre}</span> esta llegando al limite.</p>
                            <div class="stock-info">
                                <p><span class="icon">📦</span> <strong>Fecha de Vencimiento:</strong> {item.fecha_vencimiento}</p>
                            </div>
                            <p class="action"><span class="icon">🛒</span> Reabastese lo antes posible.</p>
                        </div>
                    </body>
                    </html>
                    """
        try:
            email_request = {
                "to_email":usuario.correo,
                "subject":asunto,
                "message":mensaje
            }
            
            response = requests.post("http://127.0.0.1:8000/productos/send-email", json=email_request)

            if response.status_code == 200:
                print(f"Alerta enviada a {usuario.nombre}")
            else:
                print(f"Error al enviar la alerta del stock")
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")

def verificar_stock_bajo(db: session, materia_prima_id=None):
    """
    Verifica si hay materias primas con stock bajo y envía alertas.
    Si se proporciona un ID específico, solo verifica esa materia prima.
    """
    if materia_prima_id:
        # Verificar una materia prima específica
        materia = db.query(MateriaPrima).filter(MateriaPrima.id == materia_prima_id).first()
        if materia and float(materia.cantidad) <= float(materia.stock_minimo):
            enviar_alerta_stock_materia(materia, db)
    else:
        # Verificar todas las materias primas
        materias = db.query(MateriaPrima).filter(
            MateriaPrima.cantidad <= MateriaPrima.stock_minimo
        ).all()
        
        for materia in materias:
            enviar_alerta_stock_materia(materia, db)

def enviar_alerta_stock_materia(item, db):
    """
    Envía una alerta vía email si el stock de materia prima es bajo.
    """
    try:
        usuarios = db.query(Usuarios).filter(
            (Usuarios.rol == "JEFE") | (Usuarios.rol == "ADMINISTRADOR")
        ).first()

        if usuarios and usuarios.correo:
            # Obtener el símbolo de la unidad de forma segura
            simbolo_unidad = "unidad"  # Valor predeterminado
            try:
                if hasattr(item, 'unidad') and item.unidad is not None:
                    if hasattr(item.unidad, 'simbolo'):
                        simbolo_unidad = item.unidad.simbolo
            except Exception as e:
                print(f"Error al acceder al símbolo de unidad: {e}")

            asunto = "¡Alerta de Stock Bajo de Materia Prima!"
            mensaje = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                            .container {{ padding: 20px; }}
                            .header {{ font-size: 20px; color: #e53935; font-weight: bold; margin-bottom: 15px; }}
                            .item-name {{ font-size: 18px; font-weight: bold; }}
                            .stock-info {{ margin: 15px 0; padding: 10px; background-color: #f5f5f5; border-left: 4px solid #e53935; }}
                            .icon {{ font-size: 18px; margin-right: 5px; }}
                            .action {{ font-weight: bold; color: #e53935; margin-top: 20px; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">🚨 ¡Alerta de Stock Bajo!</div>
                            <p>El stock de <span class="item-name">{item.nombre}</span> está por debajo del mínimo recomendado.</p>
                            <div class="stock-info">
                                <p><span class="icon">📦</span> <strong>Stock Actual:</strong> {item.cantidad} {simbolo_unidad}</p>
                                <p><span class="icon">⚠️</span> <strong>Stock Mínimo:</strong> {item.stock_minimo} {simbolo_unidad}</p>
                            </div>
                            <p class="action"><span class="icon">🛒</span> Es necesario reabastecer lo antes posible.</p>
                        </div>
                    </body>
                    </html>
                    """
            
            # Usar un timeout para la solicitud HTTP para evitar bloqueos prolongados
            email_request = {
                "to_email": usuarios.correo,
                "subject": asunto,
                "message": mensaje
            }
            
        
            
            import threading
            thread = threading.Thread(
                target=_enviar_correo_background,
                args=(email_request,)
            )
            thread.daemon = True  # El hilo terminará cuando el programa principal termine
            thread.start()

            print(f"Alerta de stock bajo programada para {usuarios.correo}")
            print(f"Alerta de stock bajo programada para {usuarios.correo}")
    except Exception as e:
        print(f"Error al procesar alerta de stock bajo: {e}")


def _enviar_correo_background(email_request):
    """Función para enviar correo en segundo plano"""
    try:
        response = requests.post(
            "http://127.0.0.1:8000/productos/send-email", 
            json=email_request,
            timeout=5  # Timeout de 5 segundos
        )
        
        if response.status_code == 200:
            print(f"Alerta de stock bajo enviada correctamente")
        else:
            print(f"Error al enviar la alerta de stock bajo: {response.text}")
    except Exception as e:
        print(f"Error en envío de correo en segundo plano: {e}")
    

@router_materia.get("/unidades-medida")
async def abtener_medidas(db:session = Depends(get_db)):
    unidades = db.query(UnidadMedida).all()
    return unidades

@router_materia.get("/materia-disponible", response_model=List[dict])
async def obtener_disponibles(db: session = Depends(get_db)):
    materia_prima = db.query(MateriaPrima).all()

    resultado = []
    for mp in materia_prima:
        resultado.append({
            "id": mp.id,
            "nombre": mp.nombre,
            "unidad_medida": mp.unidad_medida.value,
            "cantidad_disponible": float(mp.cantidad),
            "ruta_imagen": mp.ruta_imagen
        })
    return resultado


@router_materia.get("/",response_model=List[MateriaPrimaBase])
async def consultar(db: session = Depends(get_db)):
    # Aquí se consulta la base de datos usando SQLAlchemy
    materia = db.query(MateriaPrima).all()  
    return materia


app = FastAPI()
router_materia = APIRouter(prefix="/materia", tags=["MateriaPrima"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


def verificar_vencimientos(db: session):
    #Verifica las materias primas proximas a vencer y envia alertas
    #Se debe colocar dentro de una funcion text, para que cumpla la sintaxis correcta de la consulta
    mateias = db.execute(text("""
        SELECT
            id,nombre,cantidad,fecha_vencimiento,
            DATEDIFF(fecha_vencimiento, CURDATE()) as dias_restantes
        FROM
            materia_prima
        WHERE
            DATEDIFF(fecha_vencimiento, CURDATE()) <= 7;
    """)).fetchall()

    for materia in mateias:
        if materia.dias_restantes <= 7:
            enviar_alerta_vencimiento(materia, db)



@router_materia.get("/unidades-medida")
async def abtener_medidas(db:session = Depends(get_db)):
    unidades = db.query(UnidadMedida).all()
    return unidades

@router_materia.get("/materia-disponible", response_model=List[MateriaPrimaBase])
async def obtener_disponibles(db: session = Depends(get_db)):
    materia_prima = db.query(MateriaPrima).all()

    resultado = []
    for mp in materia_prima:
        resultado.append({
            "id": mp.id,
            "nombre": mp.nombre,
            "unidad_medida": mp.unidad_medida.value,
            "cantidad_disponible": float(mp.cantidad),
            "ruta_imagen": mp.ruta_imagen
        })
    return resultado


@router_materia.get("/", response_model=List[MateriaPrimaBase])
async def consultar(db: session = Depends(get_db)):
    # Aquí se consulta la base de datos usando SQLAlchemy
    materia = db.query(MateriaPrima).all()  
    return materia

# Endpoint para agregar una nueva materia prima
@router_materia.post("/" )
async def agregar_materia(
    nombre: str = Form(...),
    unidad_id: int = Form(...),
    cantidad: float = Form(...), 
    stock_minimo: int = Form(...),  
    fecha_ingreso: str = Form(...),  
    vida_util_dias: int = Form(...),
    precio_unitario: float = Form(...), 
    file: Optional[UploadFile] = File(None),
    db: session = Depends(get_db)
):
    
    
    unidad = db.query(UnidadMedida).filter(UnidadMedida.id == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=400, detail="Unidad de medida no encontrada")
    
    # Verifica si ya existe una Materia Prima con el mismo nombre
    existe_materia = db.query(MateriaPrima).filter(MateriaPrima.nombre == nombre).first()
    if existe_materia:
        raise HTTPException(status_code=400, detail="Materia prima ya existe")
    
    # Procesar la imagen 
    image_path = None
    if file:
        try:
            image_path = f"imagesM/{file.filename}"
            with open(image_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

    # Crear la instancia de MateriaPrima a partir de los datos del formulario
    materia = MateriaPrima(
        nombre=nombre,
        cantidad=cantidad,
        ruta_imagen=image_path,
        stock_minimo=stock_minimo,
        fecha_ingreso=fecha_ingreso,
        vida_util_dias=vida_util_dias,
        unidad=unidad,
        precio_unitario=precio_unitario
    )

    # Guardar en la base de datos
    try:
        db.add(materia)
        db.commit()
        db.refresh(materia)
        return JSONResponse(content={"nombre": nombre}, status_code=201)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el usuario en la base de datos: {str(e)}")

    
    


@router_materia.patch("/{id}", response_model=MateriaPrimaDTO)
async def actualizar_parcial_materia_prima(id:int, materia: MateriaPrimaUpdate, db: session = Depends(get_db)):
    # Imprimir los datos recibidos para depuración
    print("Datos recibidos:", materia.dict(exclude_unset=True))

    # Buscar la materia prima por ID
    materia_existente = db.query(MateriaPrima).filter(MateriaPrima.id == id).first()
    if not materia_existente:
        raise HTTPException(status_code=404, detail="Materia Prima no encontrada")

    # Diccionario con los valores a actualizar
    materia_data = materia.dict(exclude_unset=True)

    # Actualizar solo los campos proporcionados
    for campo, valor in materia_data.items():
        if valor is not None:
            setattr(materia_existente, campo, valor)
    

    db.commit()
    db.refresh(materia_existente)
    return materia_existente



@router_materia.delete("/eliminar")
async def eliminar_materia(data: EliminarMateriaRequest, db: session = Depends(get_db)):
    print(f"Datos recibidos: {data}") 
    # Buscar al único usuario con el rol "JEFE"
    jefe = db.query(Usuarios).filter(Usuarios.rol == "JEFE").first()
    if not jefe:
        raise HTTPException(status_code=404, detail="No se encontró ningún usuario con el rol Jefe.")

    # Validar que la contraseña proporcionada coincide con la del Jefe
    if jefe.contraseña != data.contraseñaProporcionada:
        raise HTTPException(status_code=403, detail="Acceso denegado: Solo el jefe puede eliminar materia prima.")

    # Buscar la materia que se quiere eliminar
    materia = db.query(MateriaPrima).filter(MateriaPrima.id == data.idMateriaaEliminar).first()


    if not materia:
        raise HTTPException(status_code=404, detail="No se encontró una materia prima con el id especificado.")
    
    # Eliminar el producto
    db.delete(materia)
    db.commit()

    return {"message": f"Materia prima con ID {data.idMateriaaEliminar} eliminado correctamente."}


# Endpoint para consultar  una materia prima por su id
@router_materia.get("/{id}", response_model=MateriaPrimaResponse)
async def obtener_materia_id(id: int, db: session = Depends(get_db)):
    materia = db.query(MateriaPrima).filter(MateriaPrima.id == id).first()

    if materia is None:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    return materia


# Endpoint para consultar una materia prima por su nombre
@router_materia.get("/consulta-nombre/{nombre}", response_model=MateriaPrimaDTO)
def obtener_materia_por_nombre(nombre: str, db: session = Depends(get_db)):
    materia = db.query(MateriaPrima).filter(MateriaPrima.nombre == nombre).first()
    
    if materia is None:
        raise HTTPException(status_code=404, detail=f"Materia Prima no encontrado con ese nombre: {nombre}")
    
    return materia



#endpoint para agregar mas stock a la materia prima
@router_materia.put("/agregar-stock/{materia_id}")
def agregar_stock(materia_id: int, lote: LoteCreate, db: session = Depends(get_db)):

    if lote.cantidad <= 0:
      raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a cero")
    if lote.vida_util_dias <= 0:
      raise HTTPException(status_code=400, detail="La vida útil debe ser mayor a cero")

    materia = db.query(MateriaPrima).filter(MateriaPrima.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia Prima no encontrada")

    nuevo_lote = LoteMateriaPrima(
        materia_prima_id=materia_id,
        cantidad=lote.cantidad,
        fecha_ingreso=lote.fecha_ingreso,
        vida_util_dias=lote.vida_util_dias,
        precio_unitario=lote.precio_unitario
    )

    materia.cantidad += lote.cantidad
    db.add(nuevo_lote)
    db.commit()
    return {"mensaje": "Stock agregado correctamente"}
    

@router_materia.patch("/{id}", response_model=MateriaPrimaDTO)
async def actualizar_parcial_materia_prima(id:int, materia: MateriaPrimaUpdate, db: session = Depends(get_db)):
    # Imprimir los datos recibidos para depuración
    print("Datos recibidos:", materia.dict(exclude_unset=True))

    # Buscar la materia prima por ID
    materia_existente = db.query(MateriaPrima).filter(MateriaPrima.id == id).first()
    if not materia_existente:
        raise HTTPException(status_code=404, detail="Materia Prima no encontrada")

    # Diccionario con los valores a actualizar
    materia_data = materia.dict(exclude_unset=True)

    # Actualizar solo los campos proporcionados
    for campo, valor in materia_data.items():
        if valor is not None:
            setattr(materia_existente, campo, valor)
    

    db.commit()
    db.refresh(materia_existente)
    return materia_existente