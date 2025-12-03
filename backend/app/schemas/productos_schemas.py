from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from decimal import Decimal
from app.models.materia_prima_recetas import MateriaPrimaRecetas
from .materia_schemas import IngredienteSchema, MateriaPrimaDTO
from .unidad_schema import UnidadesMedidaSchemas


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
    precio_salida: float
    precio_entrada: Optional[float] = None
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
    precio_salida: Optional[float] = None
    precio_entrada: Optional[float] = None
    ruta_imagen: Optional[str] = None
    id_usuario: Optional[int] =None

    class Config:
        from_attributes = True

class ProductoDTO(BaseModel):
    id: int
    nombre: str 
    cantidad: int
    stock_minimo: int
    categoria: Categoria
    precio_salida: float
    precio_entrada: Optional[float] = None
    ruta_imagen: Optional[str]
    id_usuario: int

class ProductoCreate(BaseModel):
    nombre: str
    cantidad: int
    categoria: Categoria
    precio_salida: Decimal
    precio_entrada: Optional[float] = None
    id_usuario: int
    tipo: Tipo
    stock_minimo: int
    ruta_imagen: Optional[str] = None
    ingredientes: Optional[List[IngredienteSchema]] = None

    class Config:
        from_attributes = True

class RecetaIngredienteUpdate(BaseModel):
    materia_prima_id: int
    cantidad_ingrediente: float
    unidad_id: Optional[int] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None #
    categoria: Optional[str] = None #
    tipo: Optional[str] = None   
    precio_unitario: Optional[float] = None #
    cantidad: Optional[float] = None #
    stock_minimo: Optional[float] = None #
    id_usuario: Optional[int] = None
    ingredientes: Optional[List[RecetaIngredienteUpdate]] = None
    
    class Config:
        orm_mode = True

class RecetaIngredienteDTO(BaseModel):
    id: int
    producto_id: int
    materia_prima_id: int
    cantidad_ingrediente: float
    unidad_id: Optional[int] = None
    
    # Relaciones
    materia_prima: Optional[MateriaPrimaDTO] = None
    unidad: Optional[UnidadesMedidaSchemas] = None
    
    class Config:
        orm_mode = True