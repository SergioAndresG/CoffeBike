from pydantic import BaseModel

class Token(BaseModel):
    access_token:str
    token_type:str
    rol:str
    mensaje: str = "Inicio de Sesion exitoso"