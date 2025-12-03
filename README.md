# ☕ Coffee Bike - Proyecto de Grado (SENA)

<p align="center">
  <strong>Plataforma Full-Stack para gestión completa de negocio móvil de café</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Proyecto-SENA-orange" alt="SENA" />
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
- [🛠️ Stack Tecnológico](#️-stack-tecnológico)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🐳 Contenerización](#-contenerización)
- [💼 Capacidades Demostradas](#-capacidades-demostradas)
- [🎯 Casos de Uso](#-casos-de-uso)
- [👥 Equipo de Desarrollo](#-equipo-de-desarrollo)

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

**Productos:**
- Catálogo completo con imágenes y precios
- Disponibilidad en tiempo real
- Asociación con materias primas (recetas)
- Control de stock automático

**Materias Primas:**
- Registro de entradas y salidas
- Fechas de vencimiento con alertas
- Niveles de stock mínimo configurables
- Trazabilidad completa de uso

### 🛒 Sistema de Pedidos

- **Pedidos en tiempo real** con actualización automática (polling cada 3s)
- Estados: `Pendiente → Preparando → Completado`
- Panel visual de órdenes activas
- Descuento automático de stock
- Registro de materias primas utilizadas por pedido

### 🔔 Sistema de Alertas Inteligentes

**Alertas automáticas para:**
- ⚠️ Productos próximos a vencer (configurable: 3, 5, 7 días)
- ⚠️ Materias primas próximas a vencer
- ⚠️ Stock bajo de productos
- ⚠️ Stock crítico de materias primas
- 📊 Reportes generados automáticamente

### 💰 Facturación
- Generación automática de facturas
- Registro de ventas por producto
- Exportación a PDF (jsPDF)
- Trazabilidad de transacciones

### 📊 Reportería y Analytics

**Reportes Automatizados (APScheduler):**
- **Semanales** - Ventas, productos más vendidos, ingresos (Lunes 9:00 AM)
- **Mensuales** - Análisis completo de rentabilidad (Día 1, 9:00 AM)
- **Exportación a Excel** (openpyxl)

**Métricas en Dashboard:**
- Ventas totales (día/semana/mes)
- Productos más vendidos
- Inventario bajo
- Alertas activas
- Tendencias de consumo

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
│  │  • Reportes semanales • Reportes mensuales              │
│  │  • Verificación de vencimientos • Alertas de stock      │
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
└──────────────────────────────────────────────────────────────┘
```

### Características Arquitectónicas

- **Separación de responsabilidades** - Backend/Frontend completamente desacoplados
- **RESTful API** - Endpoints siguiendo estándares REST
- **Arquitectura por capas** - Models, Schemas, Endpoints, Services
- **Sistema de eventos** - Polling constante para actualizaciones en tiempo real
- **Tareas programadas** - Background jobs con APScheduler
- **Contenerización completa** - Docker + Docker Compose

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

**Proceso completo:**

1. **Cliente** escanea QR → Accede a menú digital → Selecciona productos → Confirma pedido

2. **Sistema** valida stock disponible → Registra pedido con estado "Pendiente"

3. **Panel de empleado** se actualiza automáticamente (polling cada 3s) → Muestra nuevo pedido

4. **Empleado** prepara orden → Cambia estado a "Preparando" → Finaliza y marca "Completado"

5. **Sistema** descuenta stock automáticamente → Registra materias primas utilizadas

6. **Cliente** llega a caja → Empleado confirma pago → Sistema genera factura PDF

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

**DevOps**
- **Docker** - Contenerización
- **Nginx** - Servidor web estático

</td>
</tr>
</table>

---

## 📁 Estructura del Proyecto

### Arquitectura Modular

**Backend (FastAPI):**
```
backend/
├── app/
│   ├── models/          # ORM (SQLAlchemy) - Usuarios, Productos, Pedidos, etc.
│   ├── schemas/         # Validación (Pydantic)
│   ├── endpoints/       # API Routes (CRUD completo)
│   ├── schedulers.py    # Tareas programadas (APScheduler)
│   └── conexion.py      # Configuración BD
├── Dockerfile
├── requirements.txt
└── main.py
```

**Frontend (Vue.js 3):**
```
frontend/
├── src/
│   ├── components/      # Componentes por rol (Admin/Jefe/Empleado/Cliente)
│   ├── routers/         # Vue Router
│   ├── servicies/       # Clientes API (Auth, etc.)
│   └── main.js
├── Dockerfile
├── nginx.conf
└── package.json
```

**Organización:** Models → Schemas → Endpoints → Frontend Components

---

## 🐳 Contenerización

### Arquitectura Docker

El proyecto está completamente dockerizado con Docker Compose para orquestación de servicios:

**Servicios:**
- **Backend:** Contenedor Python con FastAPI y Uvicorn
- **Frontend:** Build multi-stage con Nginx para servir SPA
- **Database:** MySQL 8.0 con volúmenes persistentes

**Características:**
- Variables de entorno para configuración
- Volúmenes para persistencia de datos
- Network interno para comunicación entre servicios
- Health checks para monitoreo
- Restart policies para alta disponibilidad

**Deployment:** Arquitectura lista para deployment en cualquier entorno con `docker-compose up`

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

## 🎓 Contexto del Proyecto

**Coffee Bike** fue desarrollado como proyecto de grado para el **SENA (Servicio Nacional de Aprendizaje)**, demostrando la aplicación práctica de tecnologías modernas en la solución de problemas reales.

**Propósito:** Digitalizar completamente la operación de un negocio de café, desde la toma de pedidos hasta la generación de reportes financieros, mejorando eficiencia operativa y trazabilidad.

---

## 📧 Contacto

- 🐛 **Reportar issues**: [GitHub Issues](https://github.com/SergioAndresG/CoffeBike/issues)
- 💡 **Sugerencias**: [GitHub Discussions](https://github.com/SergioAndresG/CoffeBike/discussions)
- 📧 **Contacto directo**: sergiogarcia3421@gmail.com

---

## 📊 Especificaciones Técnicas

**Desarrollado como proyecto de portfolio**

- ✅ Sistema completamente funcional
- ✅ Arquitectura escalable y modular
- ✅ Dockerizado para deployment rápido
- ✅ Código documentado
- ✅ Prácticas de seguridad implementadas

**Capacidades demostradas:**
- ⚡ Sistema de tiempo real con polling
- 🔐 Autenticación segura con JWT
- 📊 Reportería automatizada
- 🔔 Sistema de alertas inteligente
- 📦 Control de inventario avanzado
- 🐳 Contenerización completa

---

## 👥 Equipo de Desarrollo

Este proyecto fue desarrollado colaborativamente por:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/SergioAndresG">
        <img src="https://github.com/SergioAndresG.png" width="100px;" alt="Sergio García"/>
        <br />
        <sub><b>Sergio Andrés García</b></sub>
      </a>
      <br />
      <sub>Full-Stack Developer</sub>
      <br />
      💻 📊 🎨 📖
    </td>
    <td align="center">
      <a href="https://github.com/camilaaven">
        <img src="https://github.com/camilaaven.png" width="100px;" alt="Camila"/>
        <br />
        <sub><b>Camila Bernal Avendaño</b></sub>
      </a>
      <br />
      <sub>Full-Stack Developer</sub>
      <br />
      💻 🎨 🐛 📖
    </sub>
    </td>
  </tr>
</table>

<p align="center">
  <a href="#-tabla-de-contenidos">⬆️ Volver arriba</a>
</p>
