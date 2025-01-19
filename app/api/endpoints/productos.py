from fastapi import APIRouter, HTTPException, FastAPI, Depends, Form, UploadFile, File
from typing import Optional
from app.conexion import get_db
from app.models.usuario import Usuarios
from app.models.productos import Productos
from app.schemas.productos_schemas import ProductoBase, ProductoDTO, ProductoResponse, EliminarProductoRequest, Categoria, Tipo
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import session
from fastapi.middleware.cors import CORSMiddleware

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




#EndPoint para Aregar Productos
@router_productos.post("/", response_model=ProductoResponse)
async def agregar_producto(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    cantidad: int = Form(...),
    categoria: Categoria = Form(...),
    precio_unitario: int = Form(...),
    id_usuario: str = Form(...),
    file: Optional[UploadFile] = File(None),
    tipo: Tipo = Form(...),
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

    # Crear el producto
    producto = Productos(
        nombre=nombre,
        descripcion=descripcion,
        cantidad=cantidad,
        categoria=categoria,
        precio_unitario=precio_unitario,
        id_usuario=id_usuario,
        ruta_imagen=image_path,  # Guardar la ruta de la imagen si existe
        tipo=tipo,
    )

    # Guardar en la base de datos
    try:
        db.add(producto)
        db.commit()
        db.refresh(producto)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar el usuario en la base de datos: {str(e)}")

    # Preparar la respuesta
    return ProductoResponse(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        cantidad=producto.cantidad,
        categoria=Categoria(producto.categoria),
        precio_unitario=producto.precio_unitario,
        id_usuario=producto.id_usuario,
        ruta_imagen=f"http://127.0.0.1:8000/productos/{image_path}",
        tipo=Tipo(producto.tipo),
    )

@router_productos.put("/{id}", response_model=ProductoDTO)
def actualizar_producto(id: int, producto: ProductoDTO, db: session = Depends(get_db)):

    # Buscar el producto por ID
    producto_existente = db.query(Productos).filter(Productos.id == id).first()
    if not producto_existente:
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado")

    # Actualizar los campos del producto
    producto_existente.nombre = producto.nombre
    producto_existente.descripcion = producto.descripcion
    producto_existente.cantidad = producto.cantidad
    producto_existente.categoria = Categoria(producto.categoria)
    producto_existente.precio_unitario = producto.precio_unitario
    producto_existente.id_usuario = producto.id_usuario

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
    if not producto:
        raise HTTPException(status_code=404, detail="No se encontró un producto con el id especificado.")

    # Eliminar el producto
    db.delete(producto)
    db.commit()

    return {"message": f"Producto con ID {data.idProductoaEliminar} eliminado correctamente."}


@router_productos.get("/{id}", response_model=ProductoDTO)
def obtener_producto_por_id(id: int, db: session = Depends(get_db)):
    # Buscar el usuario en la base de datos por su ID
    producto = db.query(Productos).filter(Productos.id == id).first()
    
    if producto is None:
        raise HTTPException(status_code=404, detail=f"Usuario no encontrado con el ID: {id}")
    
    return producto