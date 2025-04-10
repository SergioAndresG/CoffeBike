from fastapi import FastAPI, APIRouter, HTTPException, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import decimal
from datetime import datetime
from typing import Dict
from app.models.materia_prima import MateriaPrima
from app.models.factura import Factura
from app.models.productos import Productos
from app.models.detalle_factura import DetalleFactura
from app.models.clientes import Cliente
from sqlalchemy.orm import session
from sqlalchemy.exc import SQLAlchemyError
from app.models.pedidos import Pedido
from app.models.productos_pedido import PedidoProducto
from app.conexion import get_db
from .productos import send_email
import asyncio
from app.schemas.pedidos_schemas import PedidoCreate, PedidoProductoCreate, ClienteCreate
import requests
from uuid import UUID, uuid4




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

router_pedidos = APIRouter(prefix="/pedidos", tags=["Pedidos"])


router = APIRouter()

@router_pedidos.websocket("/ws/cliente/{cliente_id}")
async def websocket_cliente(websocket: WebSocket, cliente_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Hola cliente {cliente_id}, recibí: {data}")
    except WebSocketDisconnect:
        print(f"Cliente {cliente_id} desconectado")


@router_pedidos.get("/{pedido_id}")
def obtener_pedido(pedido_id: str, db: session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    productos = [
        {
            "producto_id": pp.producto_id,
            "producto_nombre": pp.producto.nombre,
            "precio_unitario": pp.precio_unitario,
            "cantidad": pp.cantidad
        }
        for pp in pedido.productos
    ]
    

    return {
        "id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "fecha": pedido.fecha,
        "estado": pedido.estado,
        "total": pedido.total,
        "productos": productos  
    }

@router_pedidos.get("/")
def listar_pedidos(db: session = Depends(get_db)):
    pedidos = db.query(Pedido).all()
    
    return [
        {
            "id": pedido.id,
            "cliente_id": pedido.cliente_id,
            "cliente_nombre": pedido.cliente.nombre if pedido.cliente else None,
            "fecha": pedido.fecha,
            "estado": pedido.estado,
            "total": pedido.total,
            "productos": [
                {
                    "producto_id": pp.producto_id,
                    "producto_nombre": pp.producto.nombre,
                    "precio_unitario": float(pp.precio_unitario),
                    "cantidad": pp.cantidad
                } for pp in pedido.productos
            ]
        }
        for pedido in pedidos
    ]



@router_pedidos.put("/{pedido_id}/estado")
def actualizar_estado_pedido(pedido_id: str, estado: dict, db: session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    pedido.estado = estado["estado"]
    pedido.mensaje = estado["mensaje"]
    db.commit()
    return {"mensaje": "Estado actualizado correctamente"}



@router_pedidos.post("/")
def crear_pedido(pedido: PedidoCreate, db: session = Depends(get_db)):
    
    # Create the order
    nuevo_pedido = Pedido(
        id=str(uuid4()),
        cliente_id=pedido.cliente_id,
        fecha=pedido.fecha,
        total=pedido.total,
        estado=pedido.estado,
        factura_id=pedido.factura_id
    )
    db.add(nuevo_pedido)
    db.flush()  

    for prod in pedido.productos:
        pedido_producto = PedidoProducto(
            pedido_id=nuevo_pedido.id,
            producto_id=prod.producto_id,
            cantidad=prod.cantidad,
            precio_unitario=prod.precio_unitario
        )
        db.add(pedido_producto)

    db.commit()
    db.refresh(nuevo_pedido)
    return {"mensaje": "Pedido creado exitosamente", "pedido_id": nuevo_pedido.id}



@router_pedidos.post("/clientes")
def crear_cliente(cliente: ClienteCreate, db: session = Depends(get_db)):
    existing_cliente = db.query(Cliente).filter(
        Cliente.numero_id == cliente.numero_id
    ).first()
    
    if existing_cliente:
        return {"id": existing_cliente.id, "mensaje": "Cliente ya existe"}
    
    # Create new client
    nuevo_cliente = Cliente(
        nombre=cliente.nombre,
        tipo_id=cliente.tipo_id,
        numero_id=cliente.numero_id
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    
    return {"id": nuevo_cliente.id, "mensaje": "Cliente creado exitosamente"}