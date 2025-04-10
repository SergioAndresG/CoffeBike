from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
from .unidad_schema import UnidadesMedidaSchemas

class IngredienteSchema(BaseModel):
    materia_prima_id: int
    unidad_medida: int
    unidad_id: int


class MateriaPrimaBase(BaseModel):
    nombre: str
    cantidad: float
    ruta_imagen: str | None = None
    stock_minimo: float
    fecha_ingreso: date
    vida_util_dias: int
    unidad_id: int
    precio_unitario: float
  


class MateriaPrimaCreate(MateriaPrimaBase):
    pass

class MateriaPrimaUpdate(BaseModel):
    nombre: Optional[str] = None
    cantidad: Optional[float] = None
    stock_minimo: Optional[float] = None
    fecha_ingreso: Optional[date] = None
    vida_util_dias: Optional[int] = None
    unidad_id: Optional[int] = None
    precio_unitario: Optional[float] = None

    class Config:
        from_attributes = True


class MateriaPrimaDTO(BaseModel):
    id: int  
    nombre: str
    unidad_id: int  
    cantidad: float
    stock_minimo: int
    fecha_ingreso: date
    vida_util_dias: int
    precio_unitario: float
    ruta_imagen: Optional[str]

    class Config:
        from_attributes = True


class MateriaPrimaResponse(MateriaPrimaDTO):
    fecha_vencimiento: date  #para que solo aparezca en la respuesta



class EliminarMateriaRequest(BaseModel):
    idMateriaaEliminar: int
    contraseñaProporcionada: str
    



class LoteCreate(BaseModel):
    cantidad: int
    fecha_ingreso: date
    vida_util_dias: int
    precio_unitario: float