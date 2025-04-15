from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from app.conexion import get_db
from app.models.factura import Factura
from app.models.pedidos import Pedido
from app.models.clientes import Cliente
from app.models.detalle_factura import DetalleFactura
from app.models.productos import Productos  
from datetime import date
from sqlalchemy import func, or_


router_facturas = APIRouter(prefix="/facturas", tags=["Facturas"])

# endpoint de facturas de clientes
@router_facturas.get("/")
def get_todas_facturas(db: Session = Depends(get_db)):
    try:
        facturas = db.query(Factura)\
            .options(
                joinedload(Factura.cliente),
                joinedload(Factura.detalles).joinedload(DetalleFactura.producto),
                joinedload(Factura.pedido)
            )\
            .order_by(Factura.fecha_compra.desc())\
            .all()

        if not facturas:
            return JSONResponse(
                status_code=200,
                content={"data": [], "mensaje": "No hay facturas registradas"}
            )

        result = []
        for factura in facturas:
            total = factura.precio_total or 0.0
            if not total and factura.detalles:
                total = sum(det.subtotal or 0 for det in factura.detalles)

            factura_data = {
                "id": factura.id,
                "fecha_compra": factura.fecha_compra.isoformat() if factura.fecha_compra else None,
                "precio_total": float(total),
                "cliente": {
                    "id": getattr(factura.cliente, "id", None),
                    "nombre": getattr(factura.cliente, "nombre", "Cliente no especificado"),
                    "tipo_id": getattr(factura.cliente, "tipo_id", None),
                    "numero_id": getattr(factura.cliente, "numero_id", None)
                } if factura.cliente else None,
                "pedido": {
                    "id": factura.pedido.id,
                    "estado": factura.pedido.estado,
                    "fecha": factura.pedido.fecha.isoformat() if factura.pedido.fecha else None
                } if factura.pedido else None,
                "productos": [
                    {
                        "id": detalle.producto.id,
                        "nombre": detalle.producto.nombre,
                        "cantidad": detalle.cantidad,
                        "precio_unitario": float(detalle.precio_unitario),
                        "subtotal": float(detalle.subtotal)
                    }
                    for detalle in factura.detalles if detalle.producto
                ] if factura.detalles else []
            }

            result.append(factura_data)

        return {"data": result}

    except Exception as e:
        print(f"Error en endpoint /: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener facturas: {str(e)}"
        )