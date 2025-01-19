from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.conexion import base


class Receta(base):
    __tablename__ = 'recetas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # Clave foránea para usuarios
    proceso_receta = Column(String(250), nullable=False)

    # Relación con Productos (un producto puede tener muchas recetas)
    producto = relationship("Productos", back_populates="recetas")

    # Relación con MateriaPrimaRecetas (una receta puede tener varios ingredientes)
    ingredientes = relationship("MateriaPrimaRecetas", back_populates="receta")

    # Relación inversa con Usuarios
    usuarios = relationship("Usuarios", back_populates="recetas")  # Esto hace la relación bidireccional

    def __init__(self, producto, proceso_receta, usuario):
        self.producto = producto
        self.proceso_receta = proceso_receta
        self.usuario = usuario

