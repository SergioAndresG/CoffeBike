from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from app.conexion import base
from app.schemas import EstadoPedidoEnum
from app.models import Usuarios, DetalleFactura,Alertas

class Pedido(base):
    __tablename__ = "pedidos"

    id = Column(String(36), primary_key=True)  # UUID
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    estado = Column(Enum(EstadoPedidoEnum), default=EstadoPedidoEnum.nuevo)
    fecha = Column(DateTime, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=True)

    cliente = relationship("Cliente", back_populates="pedidos")
    productos = relationship("PedidoProducto", back_populates="pedido")
    estados = relationship("EstadoPedido", back_populates="pedido")
    factura = relationship("Factura", back_populates="pedido")