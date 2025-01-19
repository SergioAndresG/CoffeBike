from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RecetaBase(BaseModel):
    producto_id: int
    materia_prima_id: int
    cantidad_necesaria: int

class RecetaCreate(RecetaBase):
    pass


class RecetaResponse(RecetaBase):
    id: int
    # Con esto, Pydantic puede acceder a los atributos del objeto y serializarlos correctamente
    class Config:
        from_attributes = True


        
class TipoMovimiento(str, Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"


class MovimientosMateriaPrimaBase(BaseModel):
    materia_prima_id: int
    tipo_movimiento: TipoMovimiento
    cantidad: int
    fecha_entrada: datetime
    fecha_vencimiento: Optional[datetime]
    usuario_id: Optional[int]


class MovimientosMateriaPrimaCreate(MovimientosMateriaPrimaBase):
    pass


class MovimientosMateriaPrimaResponse(MovimientosMateriaPrimaBase):
    id: int
    # Con esto, Pydantic puede acceder a los atributos del objeto y serializarlos correctamente
    class Config:
        from_attributes = True


class MateriaPrimaBase(BaseModel):
    nombre: str
    unidad_medida: str
    stock_actual: int
    precio_unitario: int


class MateriaPrimaDTO(BaseModel):
    nombre: str
    unidad_medida: str
    cantidad_de_unidades: float
    precio_unitario: float
    ruta_imagen: Optional[str]


    class Config:
        from_attributes = True


class MateriaPrimaResponse(MateriaPrimaBase):
    id: int
    recetas: List[RecetaResponse] = []
    movimientos: List[MovimientosMateriaPrimaResponse] = []
    # Con esto, Pydantic puede acceder a los atributos del objeto y serializarlos correctamente
    class Config:
        from_attributes = True


class MovimientoResponse(BaseModel):
    id: int
    tipo: str
    cantidad: int

    class Config:
        from_attributes = True
