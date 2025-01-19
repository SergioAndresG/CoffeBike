from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base
from app.schemas import Categoria, Tipo
from app.models import Usuarios, DetalleFactura, Receta,Alertas

# Tabla de Productos 
class Productos(base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(200), nullable=False, unique=True)
    cantidad = Column(Integer, nullable=False)
    categoria = Column(Enum(Categoria), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    ruta_imagen = Column(String(100), nullable=True)
    tipo = Column(Enum(Tipo), nullable=False)

    usuario = relationship("Usuarios", back_populates="productos")
    recetas = relationship("Receta", back_populates="producto")

    # Relación con DetalleFactura
    detalles_factura = relationship("DetalleFactura", back_populates="producto")

    # Relacion con Alertas
    alertas = relationship("Alertas", back_populates="producto")

    def __init__(self, nombre, descripcion, cantidad, categoria, precio_unitario, id_usuario, tipo, ruta_imagen=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.categoria = categoria
        self.precio_unitario = precio_unitario
        self.id_usuario = id_usuario
        self.ruta_imagen = ruta_imagen
        self.tipo = tipo