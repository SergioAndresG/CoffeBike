from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from app.conexion import base
from datetime import datetime


class Factura(base):
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)  # Cambiado de id_usuario a cliente_id
    fecha_compra = Column(DateTime, nullable=False, default=datetime.utcnow)
    precio_total = Column(Numeric(10, 2), nullable=False)

    cliente = relationship("Cliente", back_populates="facturas")
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")
    pedido = relationship("Pedido", back_populates="factura", uselist=False)


def __init__(self, fecha_compra, precio_total, cliente_id):
    self.fecha_compra = fecha_compra
    self.precio_total = precio_total
    self.cliente_id = cliente_id