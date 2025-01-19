from pydantic import BaseModel


class EstadisticasDTO(BaseModel):
    empleados_count: int
    productos_count: int
    max_empleados: int
    max_productos: int