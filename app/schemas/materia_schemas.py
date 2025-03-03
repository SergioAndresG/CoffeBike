from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MovimientosMateriaPrimaBase(BaseModel):
    id:int
    materia_prima_id: int
    cantidad_de_unidades: float
    fecha_entrada: datetime
    fecha_vencimiento: Optional[datetime]
    usuario_id: Optional[int]

class IngredienteSchema(BaseModel):
    materia_prima_id: int
    unidad_medida: int

class MateriaPrimaBase(BaseModel):
    id:int
    nombre: str
    unidad_medida: str
    cantidad_de_unidades: float
    stock_actual: int
    precio_unitario: int

class MateriaPrimaDTO(BaseModel):
    id:int
    unidad_medida: str
    cantidad_de_unidades: float
    precio_unitario: float
    ruta_imagen: Optional[str]

    class Config:
        from_attributes = True


class MateriaPrimaResponse(MateriaPrimaBase):
    id: int
    cantidad_de_unidades: float
    