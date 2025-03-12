from pydantic import BaseModel

class UnidadesMedidaSchemas(BaseModel):
    id: int
    nombre: str
    simbolo: str