from fastapi import APIRouter, FastAPI, HTTPException, Depends, File,UploadFile,Form
from typing import Optional, List
from app.conexion import get_db
from app.schemas.materia_schemas import MateriaPrimaBase, MateriaPrimaDTO, MateriaPrimaResponse
from app.models.materia_prima import MateriaPrima
from app.models.unidad_medida import UnidadMedida
from app.models.usuario import Usuarios
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.compra import enviar
from datetime import datetime


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
            enviar_alerta_materia(materia, db)


def enviar_alerta_materia(item, db):
    usuario = db.query(Usuarios).filter(Usuarios.rol == "JEFE").first()
    # Si el usuario asociado al rol existe
    if usuario and usuario.telefono:
        # El cuerpo del mesaje
        mensaje=f"Alerta --> La materia prima {item.nombre} esta por vencer {item.fecha_vencimiento}"
        try:
            #Eviar el mensaje
            enviar(f"+57{usuario.telefono}", mensaje) #Se le envia al numero registrado al rol
        except Exception as e:
            #Si algo sale mal, imprimir el error
            HTTPException(status_code=400,detail=f"Mensaje no enviado: {e}")
            print(f"Error al enviar el mensaje {e}")


# endpoints materia prima
@router_materia.get("/")
async def consultar(db: session = Depends(get_db)):
    # Aquí se consulta la base de datos usando SQLAlchemy
    materia = db.query(MateriaPrima).all()  
    return materia


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


# Endpoint para agregar una nueva materia prima
@router_materia.post("/", response_model=MateriaPrimaDTO)
async def agregar_materia(
    nombre: str = Form(...),
    unidad_medida: str = Form(...),
    cantidad: float = Form(...),  # Usar `float` para cantidades decimales
    precio_unitario: float = Form(...),  # Usar `float` para el precio
    file: Optional[UploadFile] = File(None),
    db: session = Depends(get_db)
):
    # Verifica si ya existe una Materia Prima con el mismo nombre (por ejemplo, para evitar duplicados)
    existing_materia = db.query(MateriaPrima).filter(MateriaPrima.nombre == nombre).first()
    if existing_materia:
        raise HTTPException(status_code=400, detail="Materia prima ya existe")

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
        unidad_medida=unidad_medida,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        ruta_imagen=image_path
    )

    # Guardar en la base de datos
    try:
        db.add(materia)
        db.commit()
        db.refresh(materia)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el usuario en la base de datos: {str(e)}")

    # Devolver la materia prima agregada como respuesta
    return MateriaPrimaDTO(
        nombre=materia.nombre,
        unidad_medida=materia.unidad_medida,
        cantidad=materia.cantidad,
        precio_unitario=materia.precio_unitario,
        ruta_imagen=f"http://127.0.0.1:8000/{image_path}",
    )