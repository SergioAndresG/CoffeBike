from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.conexion import base
from app.schemas import EstadoPedidoEnum
from app.models import Usuarios, DetalleFactura,Alertas

class EstadoPedido(base):
    __tablename__ = "estados_pedido"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(String(36), ForeignKey("pedidos.id"), nullable=False)
    estado = Column(Enum(EstadoPedidoEnum), nullable=False)
    mensaje = Column(String(255))
    timestamp = Column(TIMESTAMP, server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    pedido = relationship("Pedido", back_populates="estados")
    usuario = relationship("Usuarios")