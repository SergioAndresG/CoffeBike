from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Categoria(str, Enum):
    PLATO = "PLATO"
    BEBIDA = "BEBIDA"

class Tipo(str, Enum):
    HECHO = "HECHO",
    COMPRADO = "COMPRADO"


class EliminarProductoRequest(BaseModel):
    idProductoaEliminar: int
    contraseñaProporcionada: str

class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    descripcion: str
    categoria: Categoria
    tipo: Tipo
    precio_unitario: int

class ProductoDTO(BaseModel):
    nombre: str
    cantidad: int
    descripcion: str
    categoria: Categoria
    tipo: Tipo
    precio_unitario: int
    ruta_imagen: Optional[str]
    id_usuario: int

class ProductoResponse(ProductoBase):
    nombre: str
    cantidad: int
    descripcion: str
    categoria: Categoria
    tipo: Tipo
    precio_unitario: int
    ruta_imagen: Optional[str]

    class Config:
        from_attributes = True
