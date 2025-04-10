from fastapi import APIRouter, FastAPI, HTTPException, Depends, File,UploadFile,Form
from typing import Optional, List
from app.conexion import get_db
from app.schemas.materia_schemas import MateriaPrimaCreate, MateriaPrimaDTO, MateriaPrimaResponse, EliminarMateriaRequest, MateriaPrimaUpdate, LoteCreate
from app.models.materia_prima import MateriaPrima, LoteMateriaPrima
from app.models.unidad_medida import UnidadMedida
from app.models.usuario import Usuarios
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi.responses import JSONResponse

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


@router_materia.get("/")
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
        unidad_id= unidad.id,
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