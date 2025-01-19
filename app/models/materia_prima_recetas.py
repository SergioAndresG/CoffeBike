from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base

class MateriaPrimaRecetas(base):
    __tablename__ = 'materia_prima_recetas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    receta_id = Column(Integer, ForeignKey('recetas.id'), nullable=False)
    materia_prima_id = Column(Integer, ForeignKey('materia_prima.id'), nullable=False)
    cantidad_ingrediente = Column(Numeric(10, 2), nullable=False)

    receta = relationship("Receta")
    materia_prima = relationship("MateriaPrima")

    def __init__(self, receta, materia_prima, cantidad_ingrediente):
        self.receta = receta
        self.materia_prima = materia_prima
        self.cantidad_ingrediente = cantidad_ingrediente