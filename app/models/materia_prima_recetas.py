from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base

class MateriaPrimaRecetas(base):
    __tablename__ = 'materia_prima_recetas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    materia_prima_id = Column(Integer, ForeignKey('materia_prima.id'), nullable=False)
    cantidad_ingrediente = Column(Numeric(10, 2), nullable=False)
    
    producto = relationship("Productos", back_populates="materia_prima_recetas")
    materia_prima = relationship("MateriaPrima", back_populates="materia_prima_recetas")
    
    def __init__(self, producto_id=None, materia_prima_id=None, cantidad_ingrediente=None, 
                 producto=None, materia_prima=None):
        if producto is not None:
            self.producto = producto
        elif producto_id is not None:
            self.producto_id = producto_id
            
        if materia_prima is not None:
            self.materia_prima = materia_prima
        elif materia_prima_id is not None:
            self.materia_prima_id = materia_prima_id
            
        if cantidad_ingrediente is not None:
            self.cantidad_ingrediente = cantidad_ingrediente