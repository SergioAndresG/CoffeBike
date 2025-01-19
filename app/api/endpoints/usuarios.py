from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from typing import Optional
from app.conexion import get_db
from app.models.usuario import Usuarios
from app.schemas.usuarios_schemas import UsuarioLogin, UsuarioResponse, UsuarioDTO,Rol, SubRol
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


@router.post("/login")
async def login(usuario_login: UsuarioLogin, db: session = Depends(get_db)):
    # Buscar al usuario en la base de datos por su nombre
    usuario = db.query(Usuarios).filter(Usuarios.nombre == usuario_login.nombre).first()
    if not usuario:
        raise HTTPException(status_code=404,detail="Usuario no econtrado")
    
    #Verificar contraseña
    if usuario.contraseña != usuario_login.contraseña:
        raise HTTPException(status_code=404,detail="contraseña incorrecta")
    # Verficar si el rol esta en Enum (ya son valores de tipo string)
    if usuario.rol not in Rol.__members__:
        raise HTTPException(status_code=404,detail="Rol no valido")

    return {"rol": usuario.rol}


# Endpoints usarios
@router.get("/usuarios")
async def consultar(db: session = Depends(get_db)):
        # Aquí se consulta la base de datos usando SQLAlchemy
        empleados = db.query(Usuarios).all()
        return empleados

@router.post("/usuarios", response_model=UsuarioResponse)
async def agregar_usuario(
    nombre: str = Form(...),
    documento: int = Form(...),
    rol: Rol = Form(...),
    subrol: Optional[SubRol] = Form(None),
    correo: str = Form(...),
    contraseña: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: session = Depends(get_db),
):
    # Validar que no exista otro usuario con el mismo rol de ADMINISTRADOR o JEFE
    if rol in [Rol.ADMINISTRADOR, Rol.JEFE]:
        usuario_existente = db.query(Usuarios).filter(Usuarios.rol == rol).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail=f"Ya existe un usuario con el rol: {rol}")

    # Procesar la imagen si se proporciona
    image_path = None
    if file:
        try:
            image_path = f"images/{file.filename}"
            with open(image_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

    # Crear el usuario
    usuario = Usuarios(
        nombre=nombre,
        documento=documento,
        rol=rol,
        subrol=subrol,
        correo=correo,
        contraseña=contraseña,
        ruta_imagen=image_path,  # Guardar la ruta de la imagen si existe
    )

    # Guardar en la base de datos
    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el usuario en la base de datos: {str(e)}")

    # Preparar la respuesta
    return UsuarioResponse(
        id=usuario.id,
        telefono=usuario.telefono,
        nombre=usuario.nombre,
        documento=usuario.documento,
        rol=usuario.rol,
        subrol=usuario.subrol,
        correo=usuario.correo,
        ruta_imagen=f"http://127.0.0.1:8000/{image_path}",
    )

@router.delete("/usuarios/eliminar")
def eliminar_usuario_por_nombre(
    nombre_usuario_a_eliminar: str,
    contraseña_proporcionada: str,
    db: session = Depends(get_db)
):
    # Buscar al único usuario con el rol "Jefe"
    jefe = db.query(Usuarios).filter(Usuarios.rol == "JEFE").first()
    if not jefe:
        raise HTTPException(status_code=404, detail="No se encontró ningún usuario con el rol Jefe.")

    # Validar que la contraseña proporcionada coincide con la del Jefe
    if jefe.contraseña != contraseña_proporcionada:
        raise HTTPException(status_code=403, detail="Acceso denegado: Solo el jefe puede eliminar usuarios.")

    # Buscar al usuario que se quiere eliminar
    usuario_a_eliminar = db.query(Usuarios).filter(Usuarios.nombre == nombre_usuario_a_eliminar).first()
    if not usuario_a_eliminar:
        raise HTTPException(status_code=404, detail="No se encontró un usuario con el nombre especificado.")

    # Eliminar el usuario
    db.delete(usuario_a_eliminar)
    db.commit()

    return {"message": f"Usuario {nombre_usuario_a_eliminar} eliminado correctamente."}


@router.put("/usuarios/{id}", response_model=UsuarioDTO)
def actualizar_usuario(id: int, usuario: UsuarioDTO, db: session = Depends(get_db)):

    # Buscar el usuario por ID
    usuario_existente = db.query(Usuarios).filter(Usuarios.id == id).first()
    if not usuario_existente:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado")

    # Actualizar los campos del usuario
    usuario_existente.nombre = usuario.nombre
    usuario_existente.rol = usuario.rol
    usuario_existente.subrol = usuario.subrol
    usuario_existente.correo = usuario.correo
    usuario_existente.contraseña = usuario.contraseña
    usuario_existente.documento = usuario.documento

    db.commit()
    db.refresh(usuario_existente)

    return usuario_existente


@router.get("/usuarios/{id}", response_model=UsuarioDTO)
def obtener_usuario_por_id(id: int, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su ID
    usuario = db.query(Usuarios).filter(Usuarios.id == id).first()
    
    if usuario is None:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado con el ID: {id}")
    
    return usuario