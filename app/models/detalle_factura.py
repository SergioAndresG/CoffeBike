from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base

class DetalleFactura(base):
    __tablename__ = 'detalle_factura'

    id = Column(Integer, primary_key=True, autoincrement=True)
    factura_id = Column(Integer, ForeignKey('facturas.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id',ondelete="SET NULL"), nullable=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    factura = relationship("Factura", back_populates="detalles")

    producto = relationship("Productos", back_populates="detalles")


    def __init__(self, factura, producto, cantidad, precio_unitario, subtotal, factura_id, producto_id):
        self.factura = factura
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.factura_id = factura_id
        self.producto_id = producto_id


        