from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TipoIDEnum(str, Enum):
    CC = "cedula_de_ciudadania"
    TI = "tarjeta_identidad"
    CE = "cedula_de_extranjeria"

class EstadoPedidoEnum(str, Enum):
    nuevo = "nuevo"
    en_proceso = "en_proceso"
    completado = "completado"
    cancelado = "cancelado"

class PedidoProductoCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class PedidoCreate(BaseModel):
    cliente_id: int
    fecha: datetime
    total: Decimal
    estado: Optional[EstadoPedidoEnum] = EstadoPedidoEnum.nuevo
    factura_id: Optional[int] = None
    productos: List[PedidoProductoCreate]

class ClienteCreate(BaseModel):
    nombre: str
    tipo_id: TipoIDEnum
    numero_id: int
