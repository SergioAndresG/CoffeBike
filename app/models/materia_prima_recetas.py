from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base

class MateriaPrimaRecetas(base):
    __tablename__ = 'materia_prima_recetas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    materia_prima_id = Column(Integer, ForeignKey('materia_prima.id'), nullable=False)
    cantidad_ingrediente = Column(Numeric(10, 2), nullable=False)
    #Unidad de medida de la receta
    unidad_id = Column(Integer, ForeignKey("unidad_medida.id"), nullable=True)

    producto = relationship("Productos", back_populates="materia_prima_recetas")
    materia_prima = relationship("MateriaPrima", back_populates="materia_prima_recetas")
    unidad = relationship("UnidadMedida")
    
    @property
    def cantidad_base(self):
        """
        Obtine la cantidad del ingrediente en unidades base 
        si la recetea tiene unidad especifica, usa esa, si no, usa la de la materia prima
        """
        unidad_actual = self.unidad if self.unidad else self.materia_prima.unidad
        return unidad_actual.convertir_a_base(float(self.cantidad_ingrediente))
    
    def usar_ingredientes(self, cantidad_a_preparar=1):
        """
        Reduce el stock de la materia prima al preparar la receta

        Args:
            cantidad_a_preparar: Numero de unidades de receta a preparar (default 1)
        """
        cantidad_requerida = float(self.cantidad_ingrediente) * cantidad_a_preparar

        # Si la receta especifica una unidad diferente a la de la materia prima
        if self.unidad and self.unidad.id != self.materia_prima.unidad_id:
            if self.unidad.tipo_medida != self.materia_prima.unidad.tipo_medida:
                raise ValueError(
                    f"No se puede convertir entre {self.unidad.tipo_medida} y "
                    f"{self.materia_prima.unidad.tipo_medida}. Unidades de diferente tipo"
                )
            # Reducimos el stock con la unidad especifica de la receta
            self.materia_prima.reducir_stock(cantidad_requerida, self.unidad)
        else:
            # Usamos la unidad de la materia prima
            self.materia_prima.reducir_stock(cantidad_requerida)


    def __init__(self, producto_id=None, materia_prima_id=None, cantidad_ingrediente=None, 
                 producto=None, materia_prima=None, unidad=None, unidad_id=None):
        if producto is not None:
            self.producto = producto
        elif producto_id is not None:
            self.producto_id = producto_id
            
        if materia_prima is not None:
            self.materia_prima = materia_prima
        elif materia_prima_id is not None:
            self.materia_prima_id = materia_prima_id
            
        if cantidad_ingrediente is not None:
            self.cantidad_ingrediente = cantidad_ingrediente
        
        if unidad is not None:
            self.unidad = unidad
        elif unidad_id is not None:
            self.unidad_id = unidad_id