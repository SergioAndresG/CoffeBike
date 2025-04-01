from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from decimal import Decimal
from app.models.materia_prima_recetas import MateriaPrimaRecetas
from .materia_schemas import IngredienteSchema

class Categoria(str, Enum):
    AMASIJOS = "AMASIJOS"
    BEBIDAS_FRIAS = "BEBIDAS_FRIAS"
    BEBIDAS_CALIENTES = "BEBIDAS_CALIENTES"
    DESAYUNOS = "DESAYUNOS"
    HOJALDRES = "HOJALDRES"
    MALTEADAS = "MALTEADAS"


class Tipo(str, Enum):
    HECHO = "HECHO",
    COMPRADO = "COMPRADO"

class MateriaPrimaRecetaInsert(BaseModel):
    materia_prima_id: int
    cantidad_ingridiente: float

class ProductoBase(BaseModel):
    nombre: str
    cantidad: int
    categoria: Categoria
    stock_minimo: int
    tipo: Tipo
    precio_unitario: int
    id_usuario: int
    materias_primas: Optional[List[MateriaPrimaRecetas]] = None
    ruta_imagen: Optional[str]
    class Config:
        arbitrary_types_allowed = True

class EliminarProductoRequest(BaseModel):
    idProductoaEliminar: int
    contraseñaProporcionada: str

class ProductoUpdate(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    cantidad: Optional[int] = None
    stock_minimo: Optional[int] = None
    categoria: Optional[Categoria] = None
    # tipo: Tipo
    precio_unitario: Optional[Decimal] = None
    ruta_imagen: Optional[str] = None
    id_usuario: Optional[int] =None

    class Config:
        orm_mode = True
        from_attributes = True

class ProductoDTO(BaseModel):
    id: int
    nombre: str 
    cantidad: int
    stock_minimo: int
    categoria: Categoria
    # tipo: Tipo
    precio_unitario: float
    ruta_imagen: Optional[str]
    id_usuario: int

class ProductoCreate(BaseModel):
    nombre: str
    cantidad: int
    categoria: Categoria
    precio_unitario: float
    id_usuario: int
    tipo: Tipo
    stock_minimo: int
    ruta_imagen: Optional[str] = None
    ingredientes: Optional[List[IngredienteSchema]] = None
    

    class Config:
        from_attributes = True