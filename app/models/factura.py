from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from app.conexion import base
from datetime import datetime

class Factura(base):
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    fecha_compra = Column(DateTime, nullable=False, default=datetime.utcnow)
    precio_total = Column(Numeric(10, 2), nullable=False)

    usuarios = relationship("Usuarios", back_populates="facturas")
    detalles_factura = relationship("DetalleFactura", back_populates="factura")

    # El constructor no debe tener 'detalles_factura' porque es una relación gestionada por SQLAlchemy
    def __init__(self, fecha_compra, precio_total):
        self.fecha_compra = fecha_compra
        self.precio_total = precio_total