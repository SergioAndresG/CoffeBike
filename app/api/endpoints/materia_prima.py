from fastapi import APIRouter, FastAPI, HTTPException, Depends, File,UploadFile,Form
from typing import Optional
from app.conexion import get_db
from app.schemas.materia_schemas import MateriaPrimaBase, MateriaPrimaDTO, MateriaPrimaResponse
from app.models.materia_prima import MateriaPrima
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router_materia = APIRouter(prefix="/materia", tags=["MateriaPrima"])

    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# endpoints materia prima
@router_materia.get("/")
async def consultar(db: session = Depends(get_db)):
    # Aquí se consulta la base de datos usando SQLAlchemy
    materia = db.query(MateriaPrima).all()  
    return materia



app.mount("/imagesM", StaticFiles(directory="imagesM"), name="imagesM")

# Endpoint para agregar una nueva materia prima
@router_materia.post("/", response_model=MateriaPrimaDTO)
async def agregar_materia(
    nombre: str = Form(...),
    unidad_medida: str = Form(...),
    cantidad_de_unidades: float = Form(...),  # Usar `float` para cantidades decimales
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
        cantidad_de_unidades=cantidad_de_unidades,
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
        cantidad_de_unidades=materia.cantidad_de_unidades,
        precio_unitario=materia.precio_unitario,
        ruta_imagen=f"http://127.0.0.1:8000/{image_path}",
    )
