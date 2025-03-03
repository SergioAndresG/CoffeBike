from app.conexion import base
from sqlalchemy import Integer, String, Float, Column
from sqlalchemy.orm import relationship

class UnidadMedida(base):
    __tablename__ = 'unidad_medida'

    id=Column(Integer,primary_key=True,autoincrement=True)
    nombre=Column(String(100), nullable=False)
    simbolo=Column(String(20),nullable=False)
    factor_conversion=Column(Float, nullable=False) #El factor para convertir a la unidad base

    materia_prima = relationship("MateriaPrima", back_populates="unidad")

