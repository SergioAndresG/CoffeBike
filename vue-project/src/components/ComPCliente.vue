<script setup lang="ts">
import { onMounted, onUnmounted, ref, computed, reactive } from 'vue'
import '@fortawesome/fontawesome-free/css/all.min.css'
import jsPDF from 'jspdf'
import { useRouter } from 'vue-router'
import axios from 'axios'
import lottie from 'lottie-web'
import Swal from 'sweetalert2'

const router = useRouter()
const isHovering = ref(false)

// Definicion del tipo para estados de pedido
type EstadoPedido = 'procesando' | 'en_proceso' | 'completado' | 'nuevo' | 'cancelado'

const estadoVista = reactive({
  textoEstado: 'Esperando confirmación del pedido',
  iconoEstado: 'fa-clock',
  ultimoEstado: 'procesando' as EstadoPedido,
  mensajeEstado: '',
  cargando: false,
  ultimaActualizacion: Date.now()
})

// Interfaces
interface Cliente {
  nombre: string
  tipoId: string
  numeroId: string
  desdeMenu?: boolean
}

interface ProductoPedido {
  id: number
  nombre: string
  precio: number
  cantidad: number
}

const animationContainer = ref(null)

// Estado
const clienteActual = ref<Cliente | null>(null)
const pedidoActual = ref<ProductoPedido[]>([])
const pedidoId = ref<string | null>(null)
const mensajeEstado = ref('')
const iconoEstado = ref('fa-clock')
const cargando = ref(false)
let intervalId: ReturnType<typeof setInterval> | null = null

// Calcular el total del pedido
const totalPedido = computed(() => {
  return pedidoActual.value.reduce((sum, producto) => {
    return sum + (producto.precio * producto.cantidad)
  }, 0)
})

// Configurar animación Lottie
lottie.loadAnimation({
  container: animationContainer.value,
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: 'https://lottie.host/661b9ed1-0384-4333-b8d6-86367aa242e6/yu2qrylFKV.json'
})

// Cargar información del cliente y pedido
const cargarInformacion = async () => {
  // 1. Intentar cargar cliente desde localStorage
  const clienteGuardado = localStorage.getItem('cliente_actual')
  if (clienteGuardado) {
    clienteActual.value = JSON.parse(clienteGuardado)
  } else {
    // Si no hay cliente guardado, redirigir al menú
    router.push('/Menu')
    return false
  }
  
  // 2. Intentar cargar ID del pedido desde localStorage
  const idPedidoGuardado = localStorage.getItem('pedido_id')
  if (idPedidoGuardado) {
    pedidoId.value = idPedidoGuardado
    
    // 3. Cargar detalles del pedido desde la API
    await cargarDetallePedido(pedidoId.value)
  } else {
    // Si no hay pedido, intentar obtener el último pedido del cliente
    await obtenerUltimoPedido()
  }
  
  return true
}

// Obtener el último pedido para el cliente actual
const obtenerUltimoPedido = async () => {
  if (!clienteActual.value) return false
  
  try {
    cargando.value = true
    const response = await axios.get(`http://localhost:8000/pedidos/cliente/${clienteActual.value.numeroId}/ultimo`)
    cargando.value = false
    
    if (response.status === 200 && response.data) {
      // Guardar ID del pedido
      pedidoId.value = response.data.id
      localStorage.setItem('pedido_id', response.data.id.toString())
      
      // Cargar productos
      pedidoActual.value = response.data.productos.map((item: any) => ({
        id: item.producto_id,
        nombre: item.producto_nombre || `Producto ${item.producto_id}`,
        precio: item.precio_unitario || 0,
        cantidad: item.cantidad
      }))
      
      // Actualizar estado
      estadoVista.ultimoEstado = response.data.estado || 'nuevo'
      actualizarEstadoVista(estadoVista.ultimoEstado)

      return true
    }
  } catch (error) {
    console.error('Error al obtener último pedido:', error)
    cargando.value = false
  }
  
  return false
}

// Cargar detalle de un pedido específico
const cargarDetallePedido = async (id: string) => {
  try {
    cargando.value = true
    console.log('Cargando pedido con id:', id)
    const response = await axios.get(`http://localhost:8000/pedidos/${id}`)
    console.log("Respuesta del backend:", response.data)
    cargando.value = false
    
    if (response.status === 200) {
      // Cargar productos
      pedidoActual.value = response.data.productos.map((item: any) => ({
        id: item.producto_id,
        nombre: item.producto_nombre || `Producto ${item.producto_id}`,
        precio: item.precio_salida || 0,
        cantidad: item.cantidad
      }))
      
      // Actualizar estado
      estadoVista.ultimoEstado = response.data.estado || 'nuevo'
      actualizarEstadoVista(estadoVista.ultimoEstado)


      return true
    }
  } catch (error) {
    console.error('Error al cargar pedido:', error)
    cargando.value = false
  }
  
  return false
}

const actualizarEstadoVista = (estado: EstadoPedido) => {
  switch (estado) {
    case 'nuevo':
      estadoVista.textoEstado = 'Tu pedido ha sido recibido';
      estadoVista.iconoEstado = 'fa-clock';
      break;
    case 'en_proceso':
      estadoVista.textoEstado = 'Estamos preparando tu pedido';
      estadoVista.iconoEstado = 'fa-cogs';
      break;
    case 'completado':
      estadoVista.textoEstado = '¡Tu pedido está listo!';
      estadoVista.iconoEstado = 'fa-check-circle';
      break;
    default:
      estadoVista.textoEstado = 'Esperando confirmación del pedido';
      estadoVista.iconoEstado = 'fa-clock';
  }

  estadoVista.ultimaActualizacion = Date.now();
};


// Generar PDF de la factura
const generarPDF = () => {
  if (!clienteActual.value || pedidoActual.value.length === 0) {
    return
  }
  
  const doc = new jsPDF()
  
  // Configuración inicial
  doc.setFontSize(18)
  doc.setFont("helvetica", "bold")
  doc.text("Factura de Compra", 105, 20, { align: 'center' })
  
  // Información del cliente
  doc.setFontSize(12)
  doc.setFont("helvetica", "normal")
  doc.text(`Fecha: ${new Date().toLocaleDateString()}`, 20, 35)
  doc.text(`Cliente: ${clienteActual.value.nombre}`, 20, 45)
  doc.text(`Identificación: ${clienteActual.value.tipoId} ${clienteActual.value.numeroId}`, 20, 55)
  
  // Línea divisoria
  doc.setLineWidth(0.5)
  doc.line(20, 60, 190, 60)

  // Detalle del pedido
  let y = 70
  doc.setFontSize(12)
  doc.text("Detalle del pedido:", 20, y)
  y += 10

  pedidoActual.value.forEach((producto, index) => {
    doc.setFont("helvetica", "bold")
    doc.text(`${index + 1}. ${producto.nombre}`, 20, y)
    doc.setFont("helvetica", "normal")
    doc.text(`Cantidad: ${producto.cantidad}`, 20, y + 7)
    doc.text(`Precio unitario: $${producto.precio.toLocaleString()}`, 20, y + 14)
    doc.text(`Total: $${(producto.precio * producto.cantidad).toLocaleString()}`, 20, y + 21)
    y += 30
  })

  // Total
  doc.setLineWidth(0.5)
  doc.line(20, y, 190, y)
  y += 10

  doc.setFontSize(14)
  doc.setFont("helvetica", "bold")
  doc.text(`Total a pagar: $${totalPedido.value.toLocaleString()}`, 20, y)

  doc.save(`Factura_${clienteActual.value.nombre.replace(/\s+/g, '_')}_${new Date().toISOString().slice(0,10)}.pdf`)
}

// Configurar polling para actualizar estado periódicamente
const iniciarPolling = () => {
  // Limpiar intervalo anterior si existe
  if (intervalId) {
    clearInterval(intervalId)
  }
  
  // Consultar estado cada 10 segundos
  intervalId = setInterval(async () => {
    if (pedidoId.value) {
      await cargarDetallePedido(pedidoId.value)
    }
  }, 10000) // 10 segundos
}

// Actualizar manualmente
const actualizarManual = async () => {
  if (pedidoId.value) {
    await cargarDetallePedido(pedidoId.value)
  }
}

// Volver al menú
const volverAlMenu = () => {
  router.push('/Menu')
}

// Lifecycle hooks
onMounted(async () => {
  // Cargar información y configurar polling
  const cargadoExitoso = await cargarInformacion()
  
  if (cargadoExitoso) {
    iniciarPolling()
  }

  lottie.loadAnimation({
    container: animationContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/661b9ed1-0384-4333-b8d6-86367aa242e6/yu2qrylFKV.json'
  })
})

onUnmounted(() => {
  // Limpiar intervalo al desmontar componente
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
})



// Función para cancelar el pedido
const cancelarPedido = async () => {
  const resultado = await Swal.fire({
    title: '¿Estás segur@?',
    text: '¿Deseas cancelar este pedido? Esto no se puede deshacer',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#335500',
    cancelButtonColor: '#730D06',
    confirmButtonText: 'Si, cancelar',
    cancelButtonText: 'No'
  })

  if (!resultado.isConfirmed) return

  try {
    cargando.value = true

    // Actualizar estado en el backend
    if (pedidoId.value) {
      await axios.put(`http://localhost:8000/pedidos/${pedidoId.value}/estado`, {
        estado: 'cancelado',
        mensaje: 'Pedido cancelado por el cliente'
      });
      
      // Actualizar estado localmente
      estadoVista.ultimoEstado = 'cancelado';
      estadoVista.textoEstado = 'Pedido cancelado';
      estadoVista.iconoEstado = 'fa-times-circle';
    }

    localStorage.removeItem('cliente_actual')
    localStorage.removeItem('pedido_id')
    clienteActual.value = null
    pedidoActual.value = []
    pedidoId.value = null

    await Swal.fire({
      title: 'Cancelado',
      text: 'El pedido ha sido cancelado.',
      icon: 'success',
      confirmButtonText: 'Aceptar'
    })

    router.push('/Menu')
  } catch (error) {
    console.error('Error al cancelar pedido:', error)
    Swal.fire('Error', 'Ocurrió un error al cancelar el pedido', 'error')
  } finally {
    cargando.value = false
  }
}

</script>

<template>
    <header>
        <nav>
            <img src="https://i.postimg.cc/QMwjX2vk/Whats-App-Image-2024-11-23-at-10-53-04-PM.jpg" class="imagen" alt="logo">
        </nav>
        <hr>
    </header>

    <div class="progress-bar">
      <div class="progress-step" :class="{'active-step': estadoVista.ultimoEstado}">
            <div class="progress-circle">
              <i :class="estadoVista.ultimoEstado === 'nuevo' ? 'fas fa-check' : 'fas fa-list'"></i>
            </div>
            <span class="progress-text">Elegir compra</span>
        </div>
        <div class="progress-step" :class="{'active-step': estadoVista.ultimoEstado}">
            <div class="progress-circle">
              <i :class="estadoVista.ultimoEstado === 'nuevo' ? 'fas fa-check' : 'fas fa-edit'"></i>
            </div>
            <span class="progress-text">Insertar datos</span>
        </div>
        <div class="progress-step" :class="{'active-step': estadoVista.ultimoEstado}">
            <div class="progress-circle">
                <i class="fas fa-shopping-cart"></i>
            </div>
            <span class="progress-text">Pedir pedido</span>
        </div>
        <div class="progress-step" 
             :class="{
               'active-step': estadoVista.ultimoEstado,
               'current-step': estadoVista.ultimoEstado === 'procesando'
             }">
            <div class="progress-circle">
                <i :class="estadoVista.ultimoEstado === 'completado' ? 'fas fa-check' : 'fas fa-clock'"></i>
            </div>
            <span class="progress-text">Esperar pedido</span>
        </div>
        <div class="progress-step" :class="{'active-step': estadoVista.ultimoEstado === 'completado'}">
            <div class="progress-circle">
                <i class="fas fa-check"></i>
            </div>
            <span class="progress-text">Listo</span>
        </div>
    </div>
    <div class="contenedor-L">
        <div class="bienvenida-L">
            <h2 class="texto-bienvenido">Bienvenido Cliente</h2>
        </div>
        
        <div class="contenedor-inferior">
        <div class="datos-L">
            <h3 class="titulo-datos">Tus Datos:</h3>
            
            <div v-if="clienteActual">
                <div class="fila-dato">
                    <span class="etiqueta">Nombre:</span>
                    <span class="valor">{{ clienteActual.nombre }}</span>
                </div>
                
                <div class="fila-dato">
                    <span class="etiqueta">Tipo de documento:</span>
                    <span class="valor">{{ clienteActual.tipoId }}</span>
                </div>
                
                <div class="fila-dato">
                    <span class="etiqueta">Identificación:</span>
                    <span class="valor">{{ clienteActual.numeroId }}</span>
                </div>
            </div>

            
            
            <div v-else class="sin-datos">
                <p>No hay datos de cliente disponibles</p>
                <button @click="router.push('/menu')" class="btn-volver">Volver al menú</button>
            </div>
        </div>
        
        <div class="animacion-container" ref="animationContainer"></div>
        </div>
    </div>
    <div class="pedido-container">
        <h2 class="titulo-pedido">Tu Pedido</h2>
        
        <div class="carta-wrapper"
            @mouseenter="isHovering = true"
            @mouseleave="isHovering = false">
            <div class="carta-pedido" 
                :class="{
                'zoom-effect': isHovering,
                'color-effect': isHovering,
                'empty-pedido': !pedidoActual || pedidoActual.length === 0
                }">
                <div class="detalles-pedido">
                    <h2 class="titulo-pediste">Pediste:</h2>
                    <div v-if="!pedidoActual || pedidoActual.length === 0" class="empty-message">
                        <i class="fas fa-shopping-cart"></i>
                        <p>No hay productos en tu pedido</p>
                    </div>
                    <ul v-else class="lista-productos">
                        <li v-for="(producto, index) in pedidoActual" :key="index">
                            • {{ producto.nombre }} ({{ producto.cantidad }})
                        </li>
                    </ul>
                    <div v-if="pedidoActual && pedidoActual.length > 0" class="subtotal">
                        <span>Subtotal:</span>
                        <span class="precio">
                            ${{
                                pedidoActual.reduce((acc, p) => acc + (p.precio * p.cantidad), 0).toLocaleString()
                            }}
                        </span>
                    </div>
                </div>
            </div>
        
            <div class="acciones-pedido">
                <button class="btn-mas-info" 
                        :class="{'show-btn': isHovering}"
                        @click="generarPDF"
                        :disabled="!pedidoActual || pedidoActual.length === 0">
                    Descargar Factura
                </button>
            </div>
        </div>
        
        <div class="estado-pedido">
        <div class="estado-card como-va">
            <h3>¿Cómo va tu pedido?</h3>
            <div class="estado-content">
                <i class="fas" :class="estadoVista.iconoEstado"></i>
                <p>{{ estadoVista.textoEstado }}</p>
                <span class="tiempo-actualizacion">
                    Última actualización: {{ new Date(estadoVista.ultimaActualizacion).toLocaleTimeString() }}
                </span>
            </div>
            <button
                class="btn-cancelar"
                @click="cancelarPedido"
                :disabled="!pedidoId || cargando || estadoVista.ultimoEstado == 'en_proceso' || estadoVista.ultimoEstado == 'completado'">
                <i class="fas fa-times-circle"></i> Cancelar Pedido
            </button>
        </div>
      </div>
    </div>
</template>

<style scoped>
body {
    font-family: 'Jura', sans-serif;
    font-weight: normal;
    color: black;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

header {
    padding: 20px;
    background-color: #000000;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.imagen {
    height: 100px;
    width: 140px; 
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #D9AB23;
}

hr {
    border-top: 2px solid #D9AB23;
    margin: 20px auto;
    width: 90%;
}

.progress-bar {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: #A65814;
    margin: 20px auto;
    width: 90%;
    height: 9px;
    max-height: 10%;
    max-width: 1200px;
    border-radius: 8px;
    margin-top: -10px;
    border-bottom: 2px solid #D9AB23;
}

.progress-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}

.progress-circle {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: #A65814;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 8px;
    margin-top: 30px;
    color: #000000;
    font-size: 20px;
}

.active-step .progress-circle {
    background-color: #D9AB23;
    color: white;
}

.progress-text {
    font-family: 'Jura', sans-serif;
    font-size: 14px;
    color: #ffffff;
    text-align: center;
}

.active-step .progress-text {
    color: #D9AB23;
    font-weight: bold;
}

.contenedor-L {
    width: 90%;
    max-width: 1200px;
    margin: 20px auto;
    background-color: #000000;
    border-radius: 8px;
    overflow: hidden;
    height: 380px;
}

.bienvenida-L {
    width: 100%;
    padding: 20px 0;
    text-align: center;
    border-top: 2px solid #D9AB23;
    margin-top: 40px;
}

.texto-bienvenido {
    color: #ffffff;
    font-size: 28px;
    font-family: 'Jura', sans-serif;
    margin: 0;
}

.contenedor-inferior {
    display: flex;
    min-height: 400px;
}

.datos-L {
    width: 50%;
    padding: 30px;
    box-sizing: border-box;
}

.titulo-datos {
    text-align: center;
    color: #A65814;
    font-family: 'Jura', sans-serif;
    font-size: 1.5rem;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #D9AB23;
}

.fila-dato {
    display: flex;
    margin: 20px 0;
    padding: 0 15px;
}

.etiqueta {
    font-weight: bold;
    color: #A65814;
    width: 150px;
    font-family: 'Jura', sans-serif;
}

.valor {
    color: #ffffff;
    flex-grow: 1;
    font-family: 'Jura', sans-serif;
    border-bottom: 1px dotted #D9AB23;
    padding-bottom: 5px;
}

.animacion-container {
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    margin-top: -110px;
    margin-left: 190px;
}

/* Estilos para la nueva sección de pedido */
.pedido-container {
    width: 90%;
    height: 400px;
    max-width: 1200px;
    margin: 30px auto;
    background-color: #000000;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(239, 237, 237, 0.1);
    border: 1px solid #A65814;
    margin-left: 190px;
}

.titulo-pedido {
    color: white;
    text-align: center;
    font-family: 'Jura', sans-serif;
    margin-bottom: 20px;
    border-bottom: 2px solid #D9AB23;
    padding-bottom: 10px;
}

.carta-wrapper {
    position: relative;
    width: 500px;
    margin: 40px auto;
}

.carta-pedido {
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    width: 100%;
    height: 250px;
    transition: all 0.3s ease;
    transform-origin: center;
    margin-left: -300px;
    border: 2px solid #A65814;
    background-color: rgba(0, 0, 0, 0.7);
}

.detalles-pedido {
    width: 100%;
    padding: 20px;
    font-family: 'Jura', sans-serif;
    text-align: center;
}

.titulo-pediste {
    color: #D9AB23;
    margin-bottom: 20px;
    font-size: 26px;
    margin-top: -30px;
    border-bottom: 2px solid #A65814;
}

.lista-productos {
    list-style-type: none;
    padding: 0;
    margin: 0 auto;
    max-width: 80%;
}

.lista-productos li {
    color: #fdebb5;
    margin: 10px 0;
    text-align: left;
    font-size: 1.1rem;
}

.carta-pedido.zoom-effect {
    transform: scale(1.05) translateY(-7px);
    box-shadow: 0 5px 15px #ab9f03; /* Sombra blanca */
}

.carta-pedido.color-effect {
    background-color: rgba(8, 8, 8, 0.8);
    border: 3px solid rgba(217, 171, 35, 0.8);
}

.carta-pedido.zoom-effect .lista-productos li {
    color: #ffffff;
    transform: translateY(-2px);
}


.detalles-pedido {
    width: 60%;
    padding: 20px;
    font-family: 'Jura', sans-serif;
    margin-top: 30px;
}

.detalles-pedido h3 {
    color: #fdebb5;
    margin-top: 0;
    transition: all 0.3s ease;
}

.carta-pedido.zoom-effect .detalles-pedido h3 {
    color: #ffffff;
}

.subtotal {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    font-size: 1.1rem;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px dashed #ab9f03;
}

.precio {
    color: #A65814;
}

.btn-mas-info {
    position: absolute;
    bottom: -40px;
    left: -45px;
    transform: translateX(-50%);
    width: 40%;
    height: 40px;
    background-color: #A65814;
    color: rgb(255, 255, 255);
    border: none;
    border-radius: 5px;
    font-family: 'Jura', sans-serif;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    opacity: 0;
    visibility: hidden;
}

.btn-mas-info.show-btn {
    opacity: 1;
    visibility: visible;
    bottom: -50px;
}

.btn-mas-info:hover {
    background-color: #ab9f03;
    color: #000000;
    transform: translateX(-50%) scale(1.05);
}

.btn-confirmar {
  background-color: #4CAF50;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-right: 15px;
  transition: all 0.3s ease;
}

.btn-confirmar:hover:not(:disabled) {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.btn-confirmar:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  opacity: 0.7;
}

.btn-cancelar {
    margin-top: 30px;
    margin-left: 45px;
    padding: 10px 20px;
    background-color: #ff4444;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-family: 'Jura', sans-serif;
}

.btn-cancelar:hover {
    background-color: #cc0000;
    transform: scale(1.05);
}

.btn-cancelar:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
    transform: none;
}

.btn-cancelar i {
    font-size: 1.2em;
}

.acciones-pedido {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 30px;
  gap: 15px;
}

.fa-spinner {
  margin-right: 8px;
}

/*cuadros de estado del pedido */
.estado-pedido {
    display: flex;
    flex-direction: column;
    gap: 30px;
    width: 300px;
    margin-left: 750px;
    margin-top: -290px;
}

.estado-card {
    background-color: #1a1a1a;
    border-radius: 8px;
    padding: 15px;
    border: 1px solid #A65814;
    transition: all 0.3s ease;
}

.estado-card h3 {
    color: #D9AB23;
    margin-top: 0;
    margin-bottom: 15px;
    font-family: 'Jura', sans-serif;
    border-bottom: 1px solid #A65814;
    padding-bottom: 8px;
}

.estado-content {
    display: flex;
    align-items: center;
    gap: 15px;
}

.icono-estado {
    font-size: 24px;
    color: #D9AB23;
}

.estado-content p {
    color: #ffffff;
    margin: 0;
    font-family: 'Jura', sans-serif;
    font-size: 14px;
}

.como-va:hover {
    transform: translateY(-7px);
    box-shadow: 0 5px 15px rgba(166, 88, 20, 0.677);
}

.en-preparacion:hover {
    transform: translateY(-7px);
    box-shadow: 0 5px 15px rgba(217, 171, 35, 0.675);
}

.btn-actualizar {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 10px;
    transition: background-color 0.3s;
}

.btn-actualizar:hover {
    background-color: #45a049;
}

.tiempo-actualizacion {
    font-size: 0.8rem;
    color: #666;
    margin-top: 5px;
    display: block;
}

.empty-pedido {
    min-height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.empty-message {
    text-align: center;
    color: #999;
}

.empty-message i {
    font-size: 2rem;
    margin-bottom: 10px;
}

</style>