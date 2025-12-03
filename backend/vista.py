from fastapi import FastAPI, HTTPException, UploadFile, Form, Depends, File
from app.conexion import crear, get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.conexion import base, crear
from typing import Dict
from app.api.endpoints.usuarios import router
from app.api.endpoints.productos import router_productos
from app.api.endpoints.compra import router_compra
from app.api.endpoints.materia_prima import router_materia
from app.api.endpoints.pedidos import router_pedidos
from app.api.endpoints.factutras import router_facturas
from app.api.endpoints.reportes import router_reporte
from app.schedulers import scheduler

app = FastAPI()
app.include_router(router)
app.include_router(router_compra)
app.include_router(router_productos)
app.include_router(router_compra)
app.include_router(router_materia)
app.include_router(router_pedidos)
app.include_router(router_facturas)
app.include_router(router_reporte)

# Para acceder a las imagenes mediante archivos estaticos hay que colocarlo en el archivo principal
app.mount("/productos/imagesP", StaticFiles(directory="imagesP"), name="imagesP")

app.mount("/materia/imagesM", StaticFiles(directory="imagesM"), name="imagesM")

app.mount("/usuarios/images", StaticFiles(directory="images"), name="images")

@app.on_event("startup")
async def starup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shotdown_event():
    scheduler.shutdown()
    
base.metadata.create_all(bind=crear)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)