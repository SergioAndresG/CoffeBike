from app.conexion import base
from sqlalchemy import Integer, String, Float, Column
from sqlalchemy.orm import relationship

class UnidadMedida(base):
    __tablename__ = 'unidad_medida'

    id=Column(Integer,primary_key=True,autoincrement=True)
    nombre=Column(String(100), nullable=False)
    simbolo=Column(String(20),nullable=False)
    factor_conversion=Column(Float, nullable=False) #El factor para convertir a la unidad base
    tipo_medida = Column(String(20), nullable=False) #peso. volumen, unidad

    materia_prima = relationship("MateriaPrima", back_populates="unidad")

    def convertir_a_base(self, cantidad):
        """
        Se convierte una unidad desde esta unidad a la unidad base
        - Para peso --> convierte a gramos
        - Para volumen --> convierte a miligramos
        - Para las unidades no hay factor de conversion (el factor siempre sera 1)
        """
        return cantidad * self.factor_conversion
    
    def convertir_desde_base(self, cantidad_base):
        """
        Convierte una cantidad desde la unidad base a esta unidad
        - Para peso --> convierte desde gramos
        - Para volumen --> convierte desde mililitros
        - Para unidades --> no hay conversion (factor siempre es 1)
        """
        return cantidad_base / self.factor_conversion
    

    def __init__(self, nombre, simbolo, factor_conversion,tipo_medida):
        self.nombre = nombre
        self.simbolo = simbolo
        self.factor_conversion = factor_conversion
        self.tipo_medida = tipo_medida
