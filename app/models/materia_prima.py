from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, Date, Computed
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from app.conexion import base
import decimal


class MateriaPrima(base):
    __tablename__ = 'materia_prima'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    cantidad = Column(Numeric(10, 2), nullable=False)
    ruta_imagen = Column(String(100), nullable=True)
    stock_minimo = Column(Numeric(10,2), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    vida_util_dias = Column(Integer, nullable=False) 
    fecha_vencimiento = Column(Date, Computed("DATE_ADD(fecha_ingreso, INTERVAL vida_util_dias DAY)", persisted=True))
    unidad_id=Column(Integer, ForeignKey("unidad_medida.id"))
    precio_unitario = Column(Numeric(10,2), nullable=False)

    # Relacion con la unidad de medida
    unidad=relationship("UnidadMedida",back_populates="materia_prima" )
    # Relacion con la tabla materia_prima_recetas
    materia_prima_recetas = relationship("MateriaPrimaRecetas", back_populates="materia_prima")
    # Relacion con la tabla de lotes
    lotes = relationship("LoteMateriaPrima", back_populates="materia_prima")

    def get_cantidad_base(self):
        """
        Obtine la cantidad en unidades base
        (gramos para peso, mililitros para volumen, unidades para conteo)
        """
        return self.unidad.convertir_a_base(float(self.cantidad))
    
    def agregar_stock(self, cantidad, unidad=None):
        """
        Añade stock al inventario con converison opcional de unidades

        Args:
            cantidad --> cantidad a agregar
            unidad --> Objeto UnidadMedida (si es diferente a la de material)
        """
        unidad_actual = unidad if unidad else self.unidad

        #Verificar que los tipos de medida coincidan
        if unidad and unidad.tipo_medida != self.unidad.tipo_medida:
            raise ValueError(
                f"No se puede convertir entre {unidad.tipo_medida} y {self.unidad.tipo_medida}. Unidades de diferente tipo"
            )
        # Convertir a unidades base primero
        cantidad_base = unidad_actual.convertir_a_base(float(cantidad))

        cantidad_en_unidad_material = self.unidad.convertir_desde_base(cantidad_base)

        self.cantidad = decimal.Decimal(float(self.cantidad) + cantidad_en_unidad_material)
    
    def reducir_stock(self, cantidad, unidad=None):
        """
        Reduce el stock con la conversion opcional de unidades

        Args:
            cantidad --> Cantidad a reducir
            unidad --> Objeto UnidadMedida (Si es diferente a la de material)
        Errores:
            ValueError: Si no hay sufuciente stock
        """
        unidad_actual = unidad if unidad else self.unidad

        #Veirificar que los tipos de medida coincidan 
        if unidad and unidad.tipo_medida != self.unidad.tipo_medida:
            raise ValueError(
                f"No se puede convertir entre {unidad.tipo_medida} y {self.unidad.tipo_medida}. Unidades de diferente tipo"
        )

        #Convertir a unidades base primero
        cantidad_base = unidad_actual.convertir_a_base(float(cantidad))

        #Convertir desde unidades base a la unidad del material
        cantidad_en_unidad_material = self.unidad.convertir_desde_base(cantidad_base)

        #Verificar si hay suficiente stock
        if float(self.cantidad) < cantidad_en_unidad_material:
            raise ValueError(f"Stock insuficiente. Solicitado: {cantidad} {unidad_actual.simbolo},"
                             f"Disponible: {self.cantidad} {self.unidad.simbolo}")
        
        self.cantidad = decimal.Decimal(float(self.cantidad)-cantidad_en_unidad_material)
    
    def __init__(self, nombre, unidad, cantidad, ruta_imagen, stock_minimo, fecha_ingreso, vida_util_dias, precio_unitario):
        self.nombre = nombre
        self.unidad = unidad
        self.cantidad = cantidad
        self.ruta_imagen = ruta_imagen
        self.stock_minimo = stock_minimo
        self.precio_unitario = precio_unitario
        self.fecha_ingreso = fecha_ingreso
        self.vida_util_dias = vida_util_dias


class LoteMateriaPrima(base):
    __tablename__ = "lotes_materia_prima"

    id = Column(Integer, primary_key=True, index=True)
    materia_prima_id = Column(Integer, ForeignKey("materia_prima.id"), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    vida_util_dias = Column(Integer, nullable=False)
    fecha_vencimiento = Column(Date, Computed("DATE_ADD(fecha_ingreso, INTERVAL vida_util_dias DAY)", persisted=True))
    precio_unitario = Column(Numeric(10,2), nullable=False)

    materia_prima = relationship("MateriaPrima", back_populates="lotes")