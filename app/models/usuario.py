from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Integer, BigInteger
from sqlalchemy.orm import relationship
from app.conexion import base
from app.schemas import Rol, SubRol

class Usuarios(base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(BigInteger, nullable=False)
    documento = Column(BigInteger, nullable=False, unique=True)
    correo = Column(String(100), nullable=False, unique=True)
    contraseña = Column(String(50), nullable=False)
    rol = Column(Enum(Rol), nullable=False)
    subrol = Column(Enum(SubRol), nullable=True)
    ruta_imagen = Column(String(100), nullable=True)

    # Relación con Productos (un usuario puede tener muchos productos)
    productos = relationship("Productos", back_populates="usuario")
    
    # Relación con Facturas (un usuario puede generar muchas facturas)
    facturas = relationship("Factura", back_populates="usuarios")

    def __init__(self, nombre, documento, correo, contraseña, rol, subrol, telefono, ruta_imagen=None):
        self.telefono = telefono
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.contraseña = contraseña
        self.rol = rol
        self.subrol = subrol
        self.ruta_imagen = ruta_imagen

