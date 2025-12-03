# ☕ Coffee Bike - Proyecto de Grado (SENA)

<p align="center">
  <strong>Plataforma Full-Stack para gestión completa de negocio móvil de café</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Vue.js-3.x-4FC08D?logo=vue.js&logoColor=white" alt="Vue.js" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white" alt="MySQL" />
</p>

---

> 💼 **Proyecto Full-Stack:** Sistema empresarial completo para gestión de coffee bike con control de inventario en tiempo real, sistema de pedidos, alertas inteligentes, facturación y reportería automatizada.

---

## 📋 Tabla de Contenidos

- [🎯 ¿Qué es Coffee Bike?](#-qué-es-coffee-bike)
- [💡 Problema que Resuelve](#-problema-que-resuelve)
- [✨ Características Principales](#-características-principales)
- [🏗️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [👥 Sistema de Roles](#-sistema-de-roles)
- [🔄 Flujo de Pedidos](#-flujo-de-pedidos)
- [📊 Sistema de Alertas](#-sistema-de-alertas)
- [🛠️ Stack Tecnológico](#️-stack-tecnológico)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🐳 Contenerización](#-contenerización)

---

## 🎯 ¿Qué es Coffee Bike?

**Coffee Bike** es un sistema de gestión empresarial completo diseñado para negocios de café móviles. Integra gestión de inventario, sistema de pedidos en tiempo real, facturación, reportería automatizada y alertas inteligentes en una única plataforma.

### 🎬 Flujo Operativo

```
┌─────────────────────────────────────────────────────────────┐
│  1️⃣  Cliente escanea QR y realiza pedido                   │
│  2️⃣  Pedido aparece en tiempo real en panel del empleado   │
│  3️⃣  Empleado cambia estado: Preparando → Completado       │
│  4️⃣  Cliente paga en caja cuando el pedido está listo      │
│  5️⃣  Sistema descuenta stock automáticamente               │
│  6️⃣  Se registra trazabilidad de materias primas usadas    │
│  7️⃣  Reportes se generan automáticamente                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Problema que Resuelve

### Desafíos de los negocios móviles de café:

- 📋 **Control de inventario complejo** - Productos perecederos y materias primas variadas
- ⏱️ **Gestión de pedidos ineficiente** - Pérdida de órdenes o confusión en hora pico
- 📊 **Falta de métricas** - Sin visibilidad de ventas, productos más vendidos o rentabilidad
- ⚠️ **Desperdicio de producto** - Sin alertas de vencimiento o stock bajo
- 👥 **Coordinación de equipo** - Difícil gestión de roles y permisos

### La solución digital:

<table>
<tr>
<td align="center" width="33%">

### 📱 Pedidos en Tiempo Real
Sistema de órdenes con actualización instantánea vía polling constante

</td>
<td align="center" width="33%">

### 🔔 Alertas Inteligentes
Notificaciones automáticas de vencimientos y stock bajo

</td>
<td align="center" width="33%">

### 📈 Reportería Automatizada
Informes semanales y mensuales generados automáticamente

</td>
</tr>
</table>

---

## ✨ Características Principales

### 🔐 Sistema de Autenticación y Roles

- **JWT Authentication** con refresh tokens
- **3 roles diferenciados:** Administrador, Jefe, Empleado
- **Sistema de permisos** granular por funcionalidad
- **Recuperación de contraseña** vía email

### 📦 Gestión de Inventario

#### Productos:
- Catálogo completo con imágenes
- Precios y disponibilidad en tiempo real
- Asociación con materias primas (recetas)
- Control de stock automático

#### Materias Primas:
- Registro de entradas y salidas
- **Fechas de vencimiento** con alertas
- **Niveles de stock mínimo** configurables
- Trazabilidad completa de uso por producto

### 🛒 Sistema de Pedidos

- **Pedidos en tiempo real** con actualización automática (polling)
- Estados del pedido: `Pendiente → Preparando → Completado`
- Panel visual de órdenes activas
- Historial completo de pedidos
- Descuento automático de stock al completar pedido
- Registro de materias primas utilizadas

### 🔔 Sistema de Alertas Inteligentes

**Alertas automáticas para:**
- ⚠️ Productos próximos a vencer (configurable: 3, 5, 7 días)
- ⚠️ Materias primas próximas a vencer
- ⚠️ Stock bajo de productos
- ⚠️ Stock crítico de materias primas
- 📊 Reportes generados automáticamente

### 💰 Facturación
- Generación de facturas
- Registro de ventas por producto
- Exportación de facturas a PDF (jsPDF)

### 📊 Reportería y Analytics
#### Reportes Automatizados (APScheduler):
- **Reportes semanales** - Ventas, productos más vendidos, ingresos
- **Reportes mensuales** - Análisis completo de rentabilidad
- **Exportación a Excel** (openpyxl)

#### Métricas en el archivo Excel:

- Ventas totales (día/semana/mes)
- Productos más vendidos
- Tendencias

### 🔄 Compras y Adquisiciones

- Registro de compras de materias primas
- Actualización automática de inventario
- Historial de proveedores
- Control de costos

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│                  FRONTEND (Vue.js 3 + Vite)                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Cliente    │  │ Empleado    │  │ Admin/Jefe │            │
│  │ (Pedidos)  │  │ (Panel)     │  │ (Gestión)  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                         │                                    │
│                    Axios (HTTP)                              │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                     REST API
                          │
┌─────────────────────────▼────────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────────┤
│  │              JWT Authentication Middleware               │
│  └──────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Endpoints  │  │ Schemas    │  │ Models     │            │
│  │ (Routes)   │  │ (Pydantic) │  │ (ORM)      │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                                                              │
│  ┌──────────────────────────────────────────────────────────┤
│  │           APScheduler (Tareas Programadas)               │
│  │  • Reportes semanales                                    │
│  │  • Reportes mensuales                                    │
│  │  • Verificación de vencimientos                          │
│  │  • Alertas de stock bajo                                 │
│  └──────────────────────────────────────────────────────────┤
└─────────────────────────────┬────────────────────────────────┘
                              │
                         SQLAlchemy ORM
                              │
┌─────────────────────────────▼────────────────────────────────┐
│                     DATABASE (MySQL 8.0)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Usuarios   │  │ Productos  │  │ Materias   │            │
│  │            │  │            │  │ Primas     │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Pedidos    │  │ Facturas   │  │ Compras    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│  ┌────────────┐  ┌────────────┐                             │
│  │ Reportes   │  │ Alertas    │                             │
│  └────────────┘  └────────────┘                             │
└──────────────────────────────────────────────────────────────┘
```

### Características Arquitectónicas

- **Separación de responsabilidades** - Backend/Frontend completamente desacoplados
- **RESTful API** - Endpoints siguiendo estándares REST
- **Arquitectura por capas** - Models, Schemas, Endpoints, Services
- **Sistema de eventos** - Polling constante para actualizaciones en tiempo real
- **Tareas programadas** - Background jobs con APScheduler
- **Contenerización** - Docker para frontend y backend

---

## 👥 Sistema de Roles

### Matriz de Permisos

| Funcionalidad | Administrador | Jefe | Empleado |
|--------------|---------------|------|----------|
| **Gestión de Usuarios** | ✅ | ✅ | ❌ |
| **Gestión de Productos** | ✅ | ✅ | ❌ |
| **Gestión de Materias Primas** | ✅ | ✅ | ❌ |
| **Ver Pedidos** | ✅ | ✅ | ✅ |
| **Cambiar Estado de Pedidos** | ✅ | ✅ | ✅ |
| **Generar Facturas** | ✅ | ✅ | ✅ |
| **Ver Reportes** | ✅ | ✅ | ❌ |
| **Configurar Alertas** | ✅ | ✅ | ❌ |
| **Gestionar Perfil** | ✅ | ✅ | ✅ |

---

## 🔄 Flujo de Pedidos (Tiempo Real)

### 1. Cliente realiza pedido
Cliente escanea QR → Selecciona productos → Confirma orden

### 2. Sistema registra pedido
API valida stock → Crea pedido con estado "Pendiente" → Retorna número de orden

### 3. Panel actualiza en tiempo real
Polling cada 3s actualiza panel de empleado con nuevos pedidos

### 4. Empleado procesa pedido
Empleado marca como "Preparando" → Cliente es notificado

### 5. Pedido completado
Sistema descuenta stock → Registra materias primas usadas → Estado: "Completado"

### 6. Pago y facturación
Cliente paga en caja → Sistema genera factura PDF → Estado: "Pagado"

---

## 📊 Sistema de Alertas

### Tipos de Alertas

#### ⚠️ Alertas de Vencimiento

**Productos:**
**Materias Primas:**
```python
# Similar a productos, verifica materias primas
# Alertas configurables: 3, 5 o 7 días antes
```

#### ⚠️ Alertas de Stock

**Stock Bajo:**

**Stock Crítico:**

#### 📊 Alertas de Reportes

---

## 🛠️ Stack Tecnológico

### Backend

<table>
<tr>
<td valign="top" width="50%">

**Core**
- **Python 3.10+** - Lenguaje base
- **FastAPI** - Framework web de alto rendimiento
- **Uvicorn** - Servidor ASGI
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos

**Autenticación**
- **PyJWT** - JSON Web Tokens
- **Passlib** - Hashing de contraseñas

**Base de Datos**
- **MySQL** - Base de datos relacional
- **PyMySQL** - Conector Python-MySQL
- **mysql-connector-python** - Driver alternativo

</td>
<td valign="top" width="50%">

**Tareas Programadas**
- **APScheduler** - Scheduler de tareas en background

**Procesamiento de Datos**
- **openpyxl** - Generación de reportes Excel

**Integraciones**
- **Google APIs** - Servicios de Google (email, etc.)

**DevOps**
- **Docker** - Contenerización
- **Docker Compose** - Orquestación de contenedores

</td>
</tr>
</table>

### Frontend

<table>
<tr>
<td valign="top" width="50%">

**Core**
- **Vue.js 3** - Framework progresivo
- **Vite** - Build tool ultrarrápido
- **Vue Router** - Enrutamiento SPA
- **Pinia** - State management
- **Axios** - Cliente HTTP

**UI/UX**
- **FontAwesome** - Iconografía
- **SweetAlert2** - Modales y alertas
- **vue-toastification** - Notificaciones toast
- **Lottie** - Animaciones

</td>
<td valign="top" width="50%">

**Utilidades**
- **jsPDF** - Generación de PDFs
- **QR Code** (implícito) - Escaneo de menú

**DevOps**
- **Docker** - Contenerización
- **Nginx** - Servidor web estático

</td>
</tr>
</table>

---

## 📁 Estructura del Proyecto

### Backend

```
backend/
├── app/
│   ├── conexion.py                  # Configuración de BD
│   │
│   ├── models/                      # Modelos ORM (SQLAlchemy)
│   │   ├── usuarios.py
│   │   ├── productos.py
│   │   ├── materia_prima.py
│   │   ├── pedidos.py
│   │   ├── facturas.py
│   │   ├── compras.py
│   │   └── reportes.py
│   │
│   ├── schemas/                     # Esquemas Pydantic
│   │   ├── usuario_schema.py
│   │   ├── producto_schema.py
│   │   ├── pedido_schema.py
│   │   └── ...
│   │
│   ├── endpoints/                   # Rutas de la API
│   │   ├── usuarios.py              # CRUD usuarios
│   │   ├── productos.py             # CRUD productos
│   │   ├── materia_prima.py         # CRUD materias primas
│   │   ├── pedidos.py               # Sistema de pedidos
│   │   ├── facturas.py              # Facturación
│   │   ├── compra.py                # Registro de compras
│   │   └── reportes.py              # Generación de reportes
│   │
│   └── schedulers.py                # Tareas programadas (APScheduler)
│
├── Dockerfile                       # Configuración Docker
├── requirements.txt                 # Dependencias Python
└── main.py                          # Punto de entrada
```

### Frontend

```
frontend/
├── src/
│   ├── main.js                      # Punto de entrada Vue
│   │
│   ├── routers/
│   │   └── misrutas.js              # Definición de rutas
│   │
│   ├── components/                  # Componentes Vue
│   │   ├── ComAdmi.vue              # Panel Administrador
│   │   ├── ComJefe.vue              # Panel Jefe
│   │   ├── ComEmpleado.vue          # Panel Empleado
│   │   ├── ComPCliente.vue          # Vista Cliente (Pedidos)
│   │   │
│   │   ├── ComSesion.vue            # Login
│   │   ├── ResetPass.vue            # Recuperar contraseña
│   │   │
│   │   ├── ComProductos.vue         # Gestión productos
│   │   ├── ComMateriaPrima.vue      # Gestión materias primas
│   │   ├── ComPedidos.vue           # Panel de pedidos
│   │   ├── ComFacturas.vue          # Facturación
│   │   ├── ComReportes.vue          # Vista de reportes
│   │   └── ComPerfil.vue            # Perfil de usuario
│   │
│   ├── servicies/
│   │   └── auths.js                 # Servicio de autenticación
│   │
│   └── assets/                      # Recursos estáticos
│
├── nginx.conf                       # Configuración Nginx
├── Dockerfile                       # Configuración Docker
├── package.json                     # Dependencias Node
└── vite.config.js                   # Configuración Vite
```

---

## 🐳 Contenerización

### Arquitectura Docker

El proyecto está completamente dockerizado para deployment sencillo:

```yaml
# docker-compose.yml (estructura conceptual)
services:
  backend:
    build: ./backend
    ports: 
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://...
      - JWT_SECRET=...
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
```

### Backend Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# Build stage
FROM node:18 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 🔒 Seguridad

### Medidas Implementadas

- ✅ **JWT Authentication** con tokens de acceso y refresh
- ✅ **Bcrypt** para hashing de contraseñas
- ✅ **CORS** configurado apropiadamente
- ✅ **Validación de entrada** con Pydantic
- ✅ **SQL Injection protection** vía ORM
- ✅ **Rate limiting** (recomendado para producción)

---

## 📊 Características Técnicas Destacadas

### 1. Sistema de Polling Inteligente


### 2. Trazabilidad de Materias Primas

```python
# Al completar un pedido, se registra qué materias primas se usaron
```

### 3. Reportes Automatizados


## 💼 Capacidades Demostradas

Este proyecto demuestra competencias en:

### Backend
- 🔹 Diseño de APIs RESTful complejas con FastAPI
- 🔹 Arquitectura de microservicios con Docker
- 🔹 Gestión de tareas programadas (APScheduler)
- 🔹 Autenticación JWT con refresh tokens
- 🔹 ORM avanzado con SQLAlchemy
- 🔹 Generación de reportes (Excel)
- 🔹 Sistema de alertas y notificaciones

### Frontend
- 🔹 SPA compleja con Vue.js 3
- 🔹 State management con Pinia
- 🔹 Polling para actualizaciones en tiempo real
- 🔹 Generación de PDFs en cliente (jsPDF)
- 🔹 UX/UI con múltiples roles
- 🔹 Componentes reutilizables y modulares

### Arquitectura
- 🔹 Separación de responsabilidades (backend/frontend)
- 🔹 Sistema de roles y permisos granular
- 🔹 Trazabilidad completa de operaciones
- 🔹 Escalabilidad mediante contenedores
- 🔹 Diseño orientado a eventos (polling)

### DevOps
- 🔹 Dockerización completa
- 🔹 Configuración de Nginx
- 🔹 Arquitectura lista para producción

---

## 🎯 Casos de Uso

### Para Administradores
- Gestión completa de usuarios, productos y materias primas
- Visualización de todos los reportes
- Configuración de alertas y umbrales
- Análisis de rentabilidad

### Para Jefes
- Supervisión de operaciones diarias
- Gestión de inventario
- Revisión de reportes
- Aprobación de compras

### Para Empleados
- Procesamiento de pedidos en tiempo real
- Cambio de estados de órdenes
- Generación de facturas
- Consulta de productos disponibles

### Para Clientes
- Escaneo de QR para menú digital
- Realización de pedidos
- Seguimiento de estado del pedido
- Recepción de factura digital

---

## 📧 Contacto

- 🐛 **Reportar issues**: [GitHub Issues](https://github.com/SergioAndresG/coffee-bike-fullstack/issues)
- 💡 **Sugerencias**: [GitHub Discussions](https://github.com/SergioAndresG/coffee-bike-fullstack/discussions)
- 📧 **Contacto directo**: sergiogarcia3421@gmail.com

---

## 📊 Especificaciones Técnicas

**Desarrollado como proyecto de portfolio**

- ✅ Sistema completamente funcional
- ✅ Arquitectura escalable y modular
- ✅ Dockerizado para deployment rápido
- ✅ Prácticas de seguridad implementadas

**Capacidades demostradas:**
- ⚡ Sistema de tiempo real con polling
- 🔐 Autenticación segura con JWT
- 📊 Reportería automatizada
- 🔔 Sistema de alertas inteligente
- 📦 Control de inventario avanzado
- 🐳 Contenerización completa
---

<p align="center">
  <sub>Plataforma que integra gestión de inventario, pedidos en tiempo real, facturación y reportería automatizada</sub>
</p>

<p align="center">
  <a href="#-tabla-de-contenidos">⬆️ Volver arriba</a>
</p>
