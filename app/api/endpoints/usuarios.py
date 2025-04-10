from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile, status
from typing import Optional
from app.conexion import get_db
from app.models.usuario import Usuarios
from app.schemas.usuarios_schemas import UsuarioLogin, UsuarioResponse, UsuarioDTO,Rol, SubRol,UsuarioUpdate
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from datetime import timedelta, datetime
from passlib.context import CryptContext
from app.schemas.token_schemas import Token
import os
from app.models.clientes import Cliente


router = APIRouter()
app = FastAPI()

#configuracion para el JWT
SECRET = "sapo_420"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

#configuracion de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict,expires_delta:timedelta=None):
    to_code=data.copy()
    expire=datetime.utcnow()+(expires_delta if expires_delta else
                               timedelta(minutes=ACCESS_TOKEN_EXPIRE_HOURS))
    to_code.update({"exp":expire})
    return jwt.encode(to_code, SECRET,algorithm=ALGORITHM)

#funcion para verificar las contraseñas hasheadas
def verify_passwords(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

#este endpoint es para hashear las contraseñas (ya que se inserto los usuarios desde la base de datos)
@router.post("/hasheo-password")
async def hash(db: session=Depends(get_db)):
    usuario = db.query(Usuarios).all()
    for user in usuario:
        if not pwd_context.identify(user.contraseña): #si no hay hash de la contraseña
            user.contraseña = pwd_context.hash(user.contraseña)
    db.commit()
    return {"menssage": "Contraseñas hasheadas correctamente"}

@router.post("/login", response_model=Token)
async def login(user_login: UsuarioLogin,db: session = Depends(get_db)):
    # Buscar al usuario en la base de datos por su nombre
    usuario = db.query(Usuarios).filter(Usuarios.nombre == user_login.nombre).first()
    if not usuario:
        raise HTTPException(status_code=401,detail="Usuario no econtrado")
    
    #Verificar contraseña
    if not pwd_context.verify(user_login.contraseña, usuario.contraseña):
        raise HTTPException(status_code=404,detail="contraseña incorrecta")
    
    # Verficar si el rol esta en Enum (ya son valores de tipo string)
    if usuario.rol not in Rol.__members__:
        raise HTTPException(status_code=404,detail="Rol no valido")

    #crear tokem JWT con la informacion del usuario
    token_data = {"sub": usuario.nombre, "id": usuario.id, "rol": usuario.rol}
    access_token = create_access_token(token_data)
    #devolver el token y la informacion nesesaria para compatibilidad onc el frontend
    return {
        "access_token":  access_token,
        "token_type": "bearer",
        "rol": usuario.rol,
        "mensaje": f"Bienvenido {usuario.nombre}"
    }

@router.get("/usuarios/me", response_model=UsuarioResponse)
async def obtner_usuario_jwt(token:str=Depends(oauth2_scheme), db: session =Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        nombre_usuario = payload.get("sub")
        usuario = db.query(Usuarios).filter(Usuarios.nombre == nombre_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404,detail="No se encontro un usuario con ese nombre")
        url_imagen = f"http://127.0.0.1:8000/usuarios/{usuario.ruta_imagen}"
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "telefono": usuario.telefono,
            "documento": usuario.documento,
            "rol": usuario.rol,
            "subrol": usuario.subrol,
            "correo": usuario.correo,
            "ruta_imagen": url_imagen,
        }
    except PyJWTError:
        raise HTTPException(status_code=401,detail="Token invalido")



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
    telefono: int = Form(...),
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
        telefono=telefono,
        rol=rol,
        subrol=subrol,
        correo=correo,
        contraseña=contraseña,
        ruta_imagen=image_path,  # Guardar la ruta de la imagen si existe
    )

    if usuario:
        if not pwd_context.identify(usuario.contraseña):
            usuario.contraseña = pwd_context.hash(usuario.contraseña)

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
    if not verify_passwords(contraseña_proporcionada, jefe.contraseña):
        raise HTTPException(status_code=403,detail="Acceso denegado solo el jefe puede eliminar usuarios")

    # Buscar al usuario que se quiere eliminar
    usuario_a_eliminar = db.query(Usuarios).filter(Usuarios.nombre == nombre_usuario_a_eliminar).first()
    if not usuario_a_eliminar:
        raise HTTPException(status_code=404, detail="No se encontró un usuario con el nombre especificado.")

    # Eliminar el usuario
    db.delete(usuario_a_eliminar)
    db.commit()

    return {"message": f"Usuario {nombre_usuario_a_eliminar} eliminado correctamente."}



@router.post("/usuarios/imagen/{id}", response_model=UsuarioResponse)
async def actualizar_imagen_usuario(
    id: int,
    file: Optional[UploadFile] = File(None),
    db: session = Depends(get_db)
):
    # Buscar el usuario por ID
    usuario_existente = db.query(Usuarios).filter(Usuarios.id == id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    try:
        # Eliminar imagen anterior si existe
        if usuario_existente.ruta_imagen and os.path.exists(usuario_existente.ruta_imagen):
            os.remove(usuario_existente.ruta_imagen)
        
        image_path = None
        if file:
            try:
                image_path = f"images/{file.filename}"
                with open(image_path, "wb") as f:
                    f.write(await file.read())
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")
        
        # Actualizar ruta de imagen en base de datos
        usuario_existente.ruta_imagen = image_path
        db.commit()
        db.refresh(usuario_existente)
        
        # Preparar la URL completa de la imagen
        imagen_url = f"http://127.0.0.1:8000/usuarios/{image_path}"
        
        return UsuarioResponse(
            id=usuario_existente.id,
            telefono=usuario_existente.telefono,
            nombre=usuario_existente.nombre,
            documento=usuario_existente.documento,
            rol=usuario_existente.rol,
            subrol=usuario_existente.subrol,
            correo=usuario_existente.correo,
            ruta_imagen=imagen_url,
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")
    

@router.patch("/usuarios/{id}", response_model=UsuarioDTO)
def actualizar_usuario_parcial(
    id: int, 
    usuario: UsuarioUpdate,  # Usamos un modelo específico para actualizaciones
    db: session = Depends(get_db)
):
    # Buscar el usuario por ID
    usuario_existente = db.query(Usuarios).filter(Usuarios.id == id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Convertir los datos de entrada a un diccionario, excluyendo los valores nulos
    usuario_data = usuario.dict(exclude_unset=True)

    # Actualizar solo los campos proporcionados
    for campo, valor in usuario_data.items():
        setattr(usuario_existente, campo, valor)
    if usuario_existente:
        if not pwd_context.identify(usuario_existente.contraseña):
            usuario_existente.contraseña = pwd_context.hash(usuario_existente.contraseña)

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