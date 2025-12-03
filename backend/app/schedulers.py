# Este es el cronometro, que maneja todo en segundo plano, sin afectar el programa principal
from apscheduler.schedulers.background import BackgroundScheduler   
# Importamos la funcion para verificar las materias primas
from app.api.endpoints.materia_prima import verificar_vencimientos
from app.api.endpoints.reportes import exportar_excel
from fastapi import Depends

#Configuracion de la base de datos
from app.conexion import SessionLocal
from sqlalchemy.orm import session

def verificaion_vencer():
    db = SessionLocal()
    # Se ejecuta la tarea periodicamente
    try:
        verificar_vencimientos(db) #Aqui se llama a la logica para los vencimientos
    finally:
        db.close()   #cerramos la conexion de la base de datos

def enviar_reporte():
    db = SessionLocal()
    # Se ejecuta la tarea periodicamente
    try:
        exportar_excel(db) #Aqui se llama a la logica para el excel
    finally:
        db.close()   #cerramos la conexion de la base de datos


scheduler = BackgroundScheduler() # Creamos un nuevo scheduler (Tarea)
scheduler.add_job(verificaion_vencer, 'interval', hours=5) #Agregarmos la tarea para que se ejecute cada 24 horas

scheduler.add_job(enviar_reporte, 'interval', hours=10)