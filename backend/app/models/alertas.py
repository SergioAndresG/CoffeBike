from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from app.conexion import base
from sqlalchemy.sql import func


class Alertas(base):
    __tablename__ = 'alertas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    mensaje = Column(String(150),nullable=False)
    fecha_hora = Column(DateTime, nullable=False, default=func.now())
    nivel_critico = Column(String(50), nullable=True) #Baja, Media, Alta

    producto = relationship("Productos", back_populates="alertas")

    def __init__(self, producto_id, mensaje, fecha_hora, nivel_critico=None):
        self.producto_id = producto_id
        self.mensaje = mensaje
        self.fecha_hora = fecha_hora
        self.nivel_critico = nivel_critico