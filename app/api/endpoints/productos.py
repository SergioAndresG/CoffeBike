from fastapi import APIRouter, HTTPException, FastAPI, Depends, Form, UploadFile, File
from typing import Optional
from app.conexion import get_db
from app.models.usuario import Usuarios
from app.models.productos import Productos
from app.models.alertas import Alertas
from app.models.detalle_factura import DetalleFactura
from app.models.materia_prima_recetas import MateriaPrimaRecetas
from app.models.materia_prima import MateriaPrima
from app.schemas.productos_schemas import ProductoBase, ProductoDTO, ProductoCreate, EliminarProductoRequest, Categoria, Tipo
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

router_productos = APIRouter(prefix="/productos", tags=["Productos"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


#ENPOINTS PRODUCTOS 
@router_productos.get("/")
async def consultar(db: session = Depends(get_db)):
    # Aquí se consulta la base de datos usando SQLAlchemy
    productos = db.query(Productos).all()  
    return productos

@router_productos.post("/", response_model=ProductoCreate)
async def agregar_producto(
    nombre: str = Form(...),
    cantidad: int = Form(...),
    categoria: Categoria = Form(...),
    stock_minimo: int = Form(...),
    tipo: Tipo = Form(...),
    precio_unitario: float = Form(...),
    id_usuario: int = Form(...),
    ingredientes: Optional[str] = Form(None),  # JSON con los ingredientes
    file: Optional[UploadFile] = File(None),
    db: session = Depends(get_db)
):
    # Procesar la imagen si se proporciona
    image_path = None
    if file:
        try:
            image_path = f"imagesP/{file.filename}"
            with open(image_path, "wb") as f:
                f.write(await file.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")

    # Validar ingredientes antes de guardar el producto**
    ingredientes_list = []
    if tipo == Tipo.HECHO:
        if not ingredientes:
            raise HTTPException(status_code=400, detail="Los ingredientes son obligatorios para productos tipo HECHO")

        try:
            ingredientes_list = json.loads(ingredientes)
            if not isinstance(ingredientes_list, list):
                raise HTTPException(status_code=400, detail="Formato incorrecto de ingredientes")

            for ingrediente in ingredientes_list:
                materia_prima_id = ingrediente.get("materia_prima_id")
                cantidad_ingrediente = ingrediente.get("cantidad_ingrediente")

                if materia_prima_id is None:
                    raise HTTPException(status_code=400, detail="ID de materia prima no puede ser None")

                materia_prima = db.query(MateriaPrima).filter(MateriaPrima.id == materia_prima_id).first()
                if not materia_prima:
                    raise HTTPException(status_code=404, detail=f"Materia prima con ID {materia_prima_id} no encontrada")

        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Error en el formato del JSON de ingredientes")

    try:
        #Guardar el producto solo si los ingredientes son válidos**
        producto = Productos(
            nombre=nombre,
            cantidad=cantidad,
            categoria=categoria,
            precio_unitario=precio_unitario,
            id_usuario=id_usuario,
            ruta_imagen=image_path,
            tipo=tipo,
            stock_minimo=stock_minimo
        )

        db.add(producto)
        db.commit()
        db.refresh(producto)  # Asegura que producto.id esté disponible

        #  Guardar los ingredientes ahora que el producto está confirmado**
        if tipo == Tipo.HECHO:
            for ingrediente in ingredientes_list:
                receta = MateriaPrimaRecetas(
                    producto_id=producto.id,
                    materia_prima_id=ingrediente["materia_prima_id"],
                    cantidad_ingrediente=ingrediente["cantidad_ingrediente"]
                )
                db.add(receta)

            db.commit()

        # Construir la respuesta**
        respuesta = {
            "id": producto.id,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "precio_unitario": float(producto.precio_unitario),
            "tipo": producto.tipo,
            "stock_minimo": producto.stock_minimo,
            "ruta_imagen": producto.ruta_imagen,
            "id_usuario": producto.id_usuario,
            "cantidad": producto.cantidad
        }

        if producto.tipo == Tipo.HECHO:
            ingredientes_data = []
            recetas = db.query(MateriaPrimaRecetas).filter(MateriaPrimaRecetas.producto_id == producto.id).all()

            for receta in recetas:
                materia_prima = db.query(MateriaPrima).filter(MateriaPrima.id == receta.materia_prima_id).first()
                ingredientes_data.append({
                    "id": receta.id,
                    "materia_prima_id": receta.materia_prima_id,
                    "nombre_materia": materia_prima.nombre if materia_prima else "Desconocido",
                    "cantidad": float(receta.cantidad_ingrediente),
                    "unidad_medida": materia_prima.unidad_id if materia_prima else "Desconocido"
                })
            respuesta["ingredientes"] = ingredientes_data

        return respuesta

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error al guardar producto: {str(e)}")



@router_productos.put("/{id}", response_model=ProductoDTO)
def actualizar_producto(id: int, producto: ProductoDTO, db: session = Depends(get_db)):

    # Buscar el producto por ID
    producto_existente = db.query(Productos).filter(Productos.id == id).first()
    if not producto_existente:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado")

    # Actualizar los campos del producto
    producto_existente.nombre = producto.nombre
    producto_existente.cantidad = producto.cantidad     
    producto_existente.categoria = Categoria(producto.categoria)
    producto_existente.precio_unitario = producto.precio_unitario
    producto_existente.id_usuario = producto.id_usuario
    #producto_existente.tipo = producto.tipo
    producto_existente.stock_minimo = producto.stock_minimo

    db.commit()
    db.refresh(producto_existente)

    return producto_existente


@router_productos.delete("/eliminar")
async def eliminar_producto(data: EliminarProductoRequest, db: session = Depends(get_db)):
    # Buscar al único usuario con el rol "JEFE"
    jefe = db.query(Usuarios).filter(Usuarios.rol == "JEFE").first()
    if not jefe:
        raise HTTPException(status_code=404, detail="No se encontró ningún usuario con el rol Jefe.")

    # Validar que la contraseña proporcionada coincide con la del Jefe
    if jefe.contraseña != data.contraseñaProporcionada:
        raise HTTPException(status_code=403, detail="Acceso denegado: Solo el jefe puede eliminar productos.")

    # Buscar el producto que se quiere eliminar
    producto = db.query(Productos).filter(Productos.id == data.idProductoaEliminar).first()

    #Eliminar las recetas relacionadas con ese producto
    db.query(MateriaPrimaRecetas).filter(MateriaPrimaRecetas.producto_id == data.idProductoaEliminar).delete()

    #Actualizar el id en detalle de factura
    db.query(DetalleFactura).filter(DetalleFactura.producto_id == data.idProductoaEliminar).update({"producto_id": None})

    #Eliminar alertas relacionadas con el producto
    db.query(Alertas).filter(Alertas.producto_id == data.idProductoaEliminar).delete()

    if not producto:
        raise HTTPException(status_code=404, detail="No se encontró un producto con el id especificado.")
    
    # Eliminar el producto
    db.delete(producto)
    db.commit()

    return {"message": f"Producto con ID {data.idProductoaEliminar} eliminado correctamente."}


#Endpoints para obtener por Id, Cantidad y Nombre del producto
@router_productos.get("/{id}", response_model=ProductoDTO)
def obtener_producto_por_id(id: int, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su ID
    producto = db.query(Productos).filter(Productos.id == id).first()
    
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado con el ID: {id}")
    
    return producto

@router_productos.get("/{cantidad}", response_model=ProductoDTO)
def obtener_producto_por_cantidad(cantidad: int, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su cantidad
    producto = db.query(Productos).filter(Productos.cantidad == cantidad).first()
    
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto no encontrado con esa cantidad: {cantidad}")
    
    return producto

@router_productos.get("/consulta-nombre/{nombre}", response_model=ProductoDTO)
def obtener_producto_por_nombre(nombre: str, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su nombre
    producto = db.query(Productos).filter(Productos.nombre == nombre).first()
    
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Producto no encontrado con ese nombre: {nombre}")
    
    return producto