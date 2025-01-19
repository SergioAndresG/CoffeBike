from pydantic import BaseModel
from typing import Optional
from enum import Enum



class Rol(str, Enum):
    JEFE = "JEFE"
    ADMINISTRADOR = "ADMINISTRADOR"
    EMPLEADO = "EMPLEADO"

class SubRol(str, Enum):
    COSINERO = "COSINERO"
    MESERO = "MESERO"

class UsuarioBase(BaseModel):
    nombre: str
    documento: int
    correo: str
    rol: Rol # Enum definido para Rol
    subrol: Optional[SubRol]  # Enum definido para SubRol, opcional
    ruta_imagen: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    documento: int
    rol: str
    subrol: Optional[str]
    correo: str
    ruta_imagen: Optional[str]

    class Config:
        from_attributes = True

class UsuarioDTO(BaseModel):
    nombre: str
    documento: int
    rol: str
    subrol: Optional[str] = None
    correo: str
    contraseña: str
    ruta_imagen: Optional[str]

class UsuarioLogin(BaseModel):
    nombre: str
    contraseña: str