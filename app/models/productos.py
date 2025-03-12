from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from app.conexion import base
from app.schemas import Categoria, Tipo
from app.models import Usuarios, DetalleFactura,Alertas


# Tabla de Productos 
class Productos(base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    cantidad = Column(Integer, nullable=False)
    categoria = Column(Enum(Categoria), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    ruta_imagen = Column(String(100), nullable=True)
    tipo = Column(Enum(Tipo), nullable=False)
    stock_minimo = Column(Integer, nullable=False)

    #Relaciones
    usuario = relationship("Usuarios", back_populates="productos")
    materia_prima_recetas = relationship("MateriaPrimaRecetas", back_populates="producto")
    # Relación con DetalleFactura
    detalles_factura = relationship("DetalleFactura", back_populates="producto")
    # Relacion con Alertas
    alertas = relationship("Alertas", back_populates="producto")
    # Relacion con Materia Prima

    def preparar_producto(self, cantidad):
        """
        Prepara un producto y reduce el inventario de todos los ingredientes 

        Args:
            cantidad:Numero de productos a preparar
        Returns:
            str: Mesaje de confirmacion
        """
        if not self.materia_prima_recetas:
            raise ValueError(f"El producto {self.nombre} no tiene una receta definida")
        
        #Verificar si tenemos suficientes ingredientes
        ingredintes_insuficientes = []

        for ingrediente in self.materia_prima_recetas:
            cantidad_requerida = float(ingrediente.cantidad_ingrediente) * cantidad

            #Determinar la unidad a usar (la de la receta o de la de la materia prima)
            unidad_receta = ingrediente.unidad if ingrediente.unidad else ingrediente.materia_prima.unidad

            #Convertir cantidad requerida a unidad base
            cantidad_requerida_base = unidad_receta.convertir_a_base(cantidad_requerida)

            cantidad_disponible_base = ingrediente.materia_prima.get_cantidad_base()

            if cantidad_disponible_base < cantidad_requerida_base:
                #Calcular cantidades en unidades originales para el mensaje 
                cantidad_disponible = ingrediente.materia_prima.cantidad
                ingredintes_insuficientes.append(
                    f"{ingrediente.materia_prima.nombre}:"
                    f"Nesecita {cantidad_requerida} {unidad_receta.simbolo},"
                    f"Disponible {cantidad_disponible} {ingrediente.materia_prima.unidad.simbolo}"
                )

        if ingredintes_insuficientes:
            raise ValueError(
                f"No hay sufucientes ingredintes para preparar {cantidad} {self.nombre}:\n" + "\n".join(ingredintes_insuficientes)
            )
        #Si tenemos suficiente de todo, reducimos los ingredientes
        for ingrediente in self.materia_prima_recetas:
            ingrediente.usar_ingredientes(cantidad)
            
        #Incrementar la cantidad del proucto preparado
        self.cantidad += cantidad

        return f"Producto preparado"



    def __init__(self, nombre, cantidad, categoria, precio_unitario, id_usuario, tipo,stock_minimo, ruta_imagen=None):
        self.nombre = nombre
        self.cantidad = cantidad
        self.categoria = categoria
        self.precio_unitario = precio_unitario
        self.id_usuario = id_usuario
        self.ruta_imagen = ruta_imagen
        self.tipo = tipo
        self.stock_minimo = stock_minimo