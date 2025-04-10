from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP,Numeric, Enum, DateTime
from sqlalchemy.orm import relationship
from app.conexion import base
from sqlalchemy.sql import func
from app.schemas import TipoIDEnum

#Modelo de clientes
class Cliente(base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    tipo_id = Column(Enum(TipoIDEnum), nullable=False)
    numero_id = Column(String(20), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

 #relacion con pedidos
    pedidos = relationship("Pedido", back_populates="cliente")