from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertaCreate(BaseModel):
    producto_id: int
    mensaje: str
    nivel_critico: Optional[str]="Media"
    fecha_hora: Optional[datetime]=None

class AlertaResponse(BaseModel):
    id: int
    producto_id: int
    mensaje: str
    fecha_hora: datetime
    nivel_critico: Optional[str]

    class Config:
        from_attributes = True