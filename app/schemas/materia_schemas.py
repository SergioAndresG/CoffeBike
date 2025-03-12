from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .unidad_schema import UnidadesMedidaSchemas

class IngredienteSchema(BaseModel):
    materia_prima_id: int
    unidad_medida: int
    unidad_id: int


class MateriaPrimaBase(BaseModel):
    id: int
    nombre: str
    cantidad: float
    ruta_imagen: Optional[str]
    stock_minimo: float
    fecha_ingreso: str
    vida_util_dias: int
    fecha_vencimiento: str
    unidad_id: int
    unidad: UnidadesMedidaSchemas

    class Config:
        from_attributes = True  # Para que SQLAlchemy convierta a dict


class MateriaPrimaDTO(BaseModel):
    id:int
    unidad_medida: str
    cantidad_de_unidades: float
    precio_unitario: float
    ruta_imagen: Optional[str]
    unidad_id: int

    unidad: UnidadesMedidaSchemas

    class Config:
        from_attributes = True


class MateriaPrimaResponse(MateriaPrimaBase):
    cantidad_de_unidades: float
    