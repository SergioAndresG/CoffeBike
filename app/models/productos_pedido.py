from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base
from app.schemas import Categoria, Tipo
from app.models import Usuarios, DetalleFactura,Alertas

class PedidoProducto(base):
    __tablename__ = "pedidos_productos"

    pedido_id = Column(String(36), ForeignKey("pedidos.id"), primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido", back_populates="productos")
    producto = relationship("Productos")  