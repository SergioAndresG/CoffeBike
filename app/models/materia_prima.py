from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base

class MateriaPrima(base):
    __tablename__ = 'materia_prima'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    unidad_medida = Column(String(50), nullable=False)
    cantidad_de_unidades = Column(Numeric(10, 2), nullable=False)
    precio_unitario = Column(Integer, nullable=False)
    ruta_imagen = Column(String(100), nullable=True)

    def __init__(self, nombre, unidad_medida, cantidad_de_unidades, precio_unitario, ruta_imagen):
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.cantidad_de_unidades = cantidad_de_unidades
        self.precio_unitario = precio_unitario
        self.ruta_imagen = ruta_imagen


