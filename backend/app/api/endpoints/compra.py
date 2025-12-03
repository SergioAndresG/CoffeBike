from fastapi import FastAPI, APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import decimal
from datetime import datetime
from typing import Dict
from app.models.materia_prima import MateriaPrima
from app.models.factura import Factura
from app.models.productos import Productos
from app.models.detalle_factura import DetalleFactura
from app.models.usuario import Usuarios
from sqlalchemy.orm import session
from sqlalchemy.exc import SQLAlchemyError
from app.models.materia_prima_recetas import MateriaPrimaRecetas
from app.conexion import get_db
from .productos import send_email
import asyncio
from app.schemas.alerta_schemas import EmailRequest
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

router_compra = APIRouter()

def enviar_alerta_stock(item, db):
    """
    Envía una alerta vía email si el stock del producto o materia prima es insuficiente.
    """
    usuario = db.query(Usuarios).filter(Usuarios.rol == "JEFE").first()
    if usuario and usuario.correo:
        asunto = "¡Alerta de Stock Bajo! 🚨"
        mensaje = f"""
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                            .container {{ padding: 20px; }}
                            .header {{ font-size: 20px; color: #e53935; font-weight: bold; margin-bottom: 15px; }}
                            .item-name {{ font-size: 18px; font-weight: bold; }}
                            .stock-info {{ margin: 15px 0; padding: 10px; background-color: #f5f5f5; border-left: 4px solid #e53935; }}
                            .icon {{ font-size: 18px; margin-right: 5px; }}
                            .action {{ font-weight: bold; color: #e53935; margin-top: 20px; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">🚨 ¡Alerta de Stock Bajo!</div>
                            <p>El stock de <span class="item-name">{item.nombre}</span> es crítico.</p>
                            <div class="stock-info">
                                <p><span class="icon">📦</span> <strong>Cantidad actual:</strong> {item.cantidad}</p>
                            </div>
                            <p class="action"><span class="icon">🛒</span> Reabastese lo antes posible.</p>
                        </div>
                    </body>
                    </html>
                    """
        try:
            email_request = {
                "to_email":usuario.correo,
                "subject":asunto,
                "message":mensaje
            }
            
            response = requests.post("http://127.0.0.1:8000/productos/send-email", json=email_request)

            if response.status_code == 200:
                print(f"Alerta enviada a {usuario.nombre}")
            else:
                print(f"Error al enviar la alerta del stock")
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")


@router_compra.post("/comprar")
def realizar_compra(request: dict, db: session = Depends(get_db)):
    # Convertir claves a enteros porque vienen como strings del frontend
    productos_cantidad = {int(k): v for k, v in request.get("productos", {}).items()}
    try:

        detalles_procesados = []

        # Procesar cada producto
        for producto_id, cantidad_comprada in productos_cantidad.items():
            # Validar existencia del producto
            producto = db.query(Productos).filter(Productos.id == producto_id).first()
            if not producto:
                raise HTTPException(status_code=404, detail=f"Producto no encontrado con ID: {producto_id}")
            
            # Validar stock del producto (igual para todos los tipos)
            if producto.cantidad < cantidad_comprada:
                # Enviar alerta si el stock es bajo
                enviar_alerta_stock(producto, db)
                raise HTTPException(status_code=400, detail=f"Inventario insuficiente para el producto: {producto.nombre}")
            
            # Actualizar inventario del producto (igual para todos los tipos)
            producto.cantidad -= cantidad_comprada
            db.add(producto)
            
            # Guardar detalle para la respuesta
            detalles_procesados.append({
                "producto_id": producto_id,
                "nombre": producto.nombre,
                "cantidad": cantidad_comprada,
                "precio_salida": float(producto.precio_salida)
            })
            
            # Verificar si después de la venta el stock ha llegado al mínimo
            if producto.cantidad <= producto.stock_minimo:
                enviar_alerta_stock(producto, db)
        
        # Guardar cambios en inventario
        db.commit()

        return {
            "mensaje": "Inventario actualizado correctamente", 
            "detalles": detalles_procesados
        }
    
    except SQLAlchemyError as e:
        db.rollback()
        error_msh=str(e)
        print(f"Error SQL: {error_msh}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        db.rollback()
        print(f"Error general {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))






