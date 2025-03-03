from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, Date
from sqlalchemy.orm import relationship
from app.conexion import base


class MateriaPrima(base):
    __tablename__ = 'materia_prima'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    cantidad = Column(Numeric(10, 2), nullable=False)
    ruta_imagen = Column(String(100), nullable=True)
    stock_minimo = Column(Numeric(10,2), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    vida_util_dias = Column(Integer, nullable=False) 
    fecha_vencimiento = Column(Date, nullable=True)
    unidad_id=Column(Integer, ForeignKey("unidad_medida.id"))


    # Relacion con la unidad de medida
    unidad=relationship("UnidadMedida",back_populates="materia_prima" )
    # Relacion con la tabla materia_prima_recetas
    materia_prima_recetas = relationship("MateriaPrimaRecetas", back_populates="materia_prima")
    


    def __init__(self, nombre, unidad, cantidad, ruta_imagen, stock_minimo, fecha_ingreso, fecha_vencimiento, vida_util_dias):
        self.nombre = nombre
        self.unidad = unidad
        self.cantidad = cantidad
        self.ruta_imagen = ruta_imagen
        self.stock_minimo = stock_minimo
        self.fecha_ingreso = fecha_ingreso
        self.vida_util_dias = vida_util_dias
        self.fecha_vencimiento = fecha_vencimiento


