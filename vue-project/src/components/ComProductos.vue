<script setup lang="ts">
import Swal from 'sweetalert2';
import { computed, onMounted, ref, watch, watchEffect } from 'vue';
import axios from 'axios';
import ComImagen from './icons/IMGENES/ComImagen.vue';
import ComAgregarP from './ComAgregarP.vue';
import ComActP from './ComActP.vue';
import { useRouter } from 'vue-router';
// Libreria para el icono de busqueda
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faSearch, faExclamationTriangle,faArrowLeft, faMinusCircle, faTimes } from '@fortawesome/free-solid-svg-icons';

//funcion para boton para volver entre paginas
const router = useRouter();

const volver = () => {
  router.go(-1)
}

// Variable para almacenar datos de la busqueda de productos
const searchTerm = ref("")
// Variables para almacenar los datos traidos por el endpoint
const productos = ref([]);
const empleado = ref([]);
// Contraseña obtenida de la informacion proporcionada por el endpoint
const contraseñaProporcionada = ref("");

//Variables reactivas para la carta emergente con informacion del producto
const emergenteMasInformacion = ref(false);
const productoSeleccionado = ref({});

//configuaracion de alertas stock
const umbralAgotado = ref(0);
const umbralProximoAgotar = ref(0);

// Estado para el usuario actual y su rol
const currentUser = ref(null);
const userRole = ref('');

//estado para el panel de alertas
const mostarPanelAlertas = ref(false);
const panelAlertasMinimizado = ref(false);

// Constantes para roles
const ROLES = {
  JEFE: 'JEFE',
  ADMINISTRADOR: 'ADMINISTRADOR',
  EMPLEADO: 'EMPLEADO'
};

// Verificar permisos según el rol
const hasPermission = (allowedRoles) => {
  return allowedRoles.includes(userRole.value);
}

// Cargar datos del usuario al iniciar el componente
const loadUserData = async () => {
  try {
    const token = localStorage.getItem("jwtToken");
    if (!token) return null;

    const response = await axios.get("https://coffebikefastapi-production.up.railway.app/usuarios/me", {
      headers: {
        Authorization: `Bearer ${token}`, 
      },
    });
    currentUser.value = response.data;
    userRole.value = response.data.rol; // Asumiendo que el rol viene en response.data.rol
  } catch (error) {
    console.error("Error obteniendo usuario:", error);
    // Redirigir al login si no hay usuario válido
    // window.location.href = '/login';
  }
};



watchEffect(() => {
  if(productos.value.length > 0){
    umbralProximoAgotar.value = Math.min(...productos.value.map(p => p.stock_minimo))
  }
})





const cargarEmpleados = async () => {
  try {
    const empleados = await axios.get("https://coffebikefastapi-production.up.railway.app/usuarios");
    empleado.value = empleados.data; // Asignamos los datos del empleado

    // Se busca el usuario con el rol de Jefe
    const jefe = empleado.value.find(e=>e.rol==="JEFE")
    if (jefe) {
      contraseñaProporcionada.value = jefe.contraseña // Se guarda solo la contraseña
    } else {
      console.error("No se encontro al jefe")
    }
  } catch (error) {
    console.error("Error al obtner la contraseña del Jefe")
    
  }
}

const cargarProductos = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/productos"); 
    productos.value = respuesta.data; // Asigna los datos de la respuesta
  } catch (error) {
    console.error("Error al cargar productos:", error);
  }
};

const verificarALertasProductos = async () => {
  const productosAgotados = productos.value.filter(p => p.cantidad <= umbralAgotado.value);
  const productosProximosAgotarse = productos.value.filter(
    p=>p.cantidad > umbralAgotado.value && p.cantidad <= umbralProximoAgotar.value
  );

  //si hay productos con alertas mostrar el mensaje
 if(productosAgotados.length> 0 || productosProximosAgotarse.length > 0){
    mostarPanelAlertas.value = true;

    //con los mensajes emergentes se le notifica al usuarios, solo la primera vez

    if(!localStorage.getItem('alertasStockMostradas')){
      let mensaje = '';

      if(productosAgotados.length>0){
        mensaje += `<strong calss="text-danger>¡Atencion!<strong/> Hay ${productosAgotados.length} productos agotados. <br>`
      }
      if(productosProximosAgotarse.length>0){
        mensaje += `<strong class="text-warning">Adevertencia<strong/> Hay ${productosProximosAgotarse.length} proximos a agotarse. `
      }

      Swal.fire({
        title: "Etsado del inventario",
        html:mensaje,
        icon:"warning",
        confirmButtonText: "Revisar",
        showCancelButton: true,
        cancelButtonText: 'Mas Tarde'
      }).then((result)=> {
        if(result.isConfirmed){
          mostarPanelAlertas.value=true;
          panelAlertasMinimizado.value=false;
        } else {
          panelAlertasMinimizado.value=true
        }
      });

      //marcar como mostradas para no molestar constantemente
      localStorage.setItem('alertasStockMostradas', 'true');
      //se reinicia el estado despues de una hora si aun no se ha hecho el re-stock
      setTimeout(()=>{
        localStorage.removeItem('alertasStockMostradas');
      }, 60*60*1000);
    }
  }
};

verificarALertasProductos()

const productosAgotados =computed(()=>{
  return productos.value.filter(p=>p.cantidad<=umbralAgotado.value);
});

const productosProximosAgotarse = computed(() => {
  return productos.value.filter(producto => 
    producto.cantidad > umbralAgotado.value && 
    producto.cantidad <= producto.stock_minimo
  );
});

const tieneLAlertas=computed(()=>{
  return productosAgotados.value.length > 0 || productosProximosAgotarse.value.length
});

cargarEmpleados();

const eliminarProducto = async (idProducto: number) => {
  try {

    if(!contraseñaProporcionada){
      console.error("no se encontro la contraseña del jefe");
      return;
    }

    // Crear el DTO con los datos necesarios
    const eliminarProductoDTO = {
      idProductoaEliminar: idProducto, // Usar el id pasado al método
      contraseñaProporcionada: String(contraseñaProporcionada.value),  // Usar la contraseña del jefe
    };

    console.log(eliminarProductoDTO)
  console.log(typeof idProducto)
  console.log(typeof contraseñaProporcionada)

    // Realizar la solicitud DELETE al backend
    const response = await axios.delete("https://coffebikefastapi-production.up.railway.app/productos/eliminar", {
      data: eliminarProductoDTO,  // Enviar el DTO en el cuerpo de la solicitud
      headers: {
        "Content-Type": "application/json"
      }
    });

    Swal.fire({
      title: "Eliminado con exito",
      icon: "success"
    });
    cargarProductos();
  } catch (error) {
    Swal.fire({
      title: "Error al elminar el Producto",
      icon: "error",
      
    })
  }

};

const filtrarProductos = computed (()=> {
  if(!searchTerm.value.trim()) return productos.value;

  const term =searchTerm.value.toLowerCase().trim()
  return productos.value.filter(pro => 
    pro.nombre.toLowerCase().includes(term)
  )
}) 


const ActualizarProducto = ref(false);
const AgregarProducto = ref(false);
const ConsultarProducto = ref(false);


const openEmergente = (producto) => {
  emergenteMasInformacion.value = true; // Gurada el producto seleccionado
  productoSeleccionado.value = producto; // Para la informacion del producto selecionado

}

const closeEmergente = () => {
  emergenteMasInformacion.value = false;
}

const openAct = () => {
     // Verificar si el usuario tiene permisos para actualizar
     if (!hasPermission([ROLES.JEFE, ROLES.ADMINISTRADOR])) {
    Swal.fire({
      icon: 'error',
      title: 'Acceso denegado',
      text: 'No tienes permisos para agregar materia prima.'
    });
    return;
  }
  ActualizarProducto.value = true;
   // Usamos esto para evitar scroll en el body principal
   document.documentElement.style.overflow = "hidden";
  document.documentElement.style.height = "100hv";
}

const closeAct = () => {
  ActualizarProducto.value = false;
  // Restaurtamos el scroll en el body principal
  document.documentElement.style.overflow = "";
  document.documentElement.style.height = "";
cargarProductos();

}

const openAdd = () => {
     // Verificar si el usuario tiene permisos para agregar
     if (!hasPermission([ROLES.JEFE, ROLES.ADMINISTRADOR])) {
    Swal.fire({
      icon: 'error',
      title: 'Acceso denegado',
      text: 'No tienes permisos para agregar materia prima.'
    });
    return;
  }
  AgregarProducto.value = true;
  // Usamos esto para evitar scroll en el body principal
  document.documentElement.style.overflow = "hidden";
  document.documentElement.style.height = "100hv";
};

const closeAdd = () => {
  AgregarProducto.value = false;
  // Restaurtamos el scroll en el body principal
  document.documentElement.style.overflow = "";
  document.documentElement.style.height = "";
cargarProductos();
};

const closeCons = () => {
  ConsultarProducto.value = false;
  // Restaurtamos el scroll en el body principal
  document.documentElement.style.overflow = "";
  document.documentElement.style.height = "";
}

const openCons = () => {
  ConsultarProducto.value = true;
   // Usamos esto para evitar scroll en el body principal
   document.documentElement.style.overflow = "hidden";
  document.documentElement.style.height = "100hv";
}

const togglePanelAlertas = () => {
  panelAlertasMinimizado.value = !panelAlertasMinimizado.value
}

const cerrarPanelAlertas = () => {
 mostarPanelAlertas.value = false
}



// Cargar datos al montar el componente
onMounted(async () => {
  await loadUserData();
  await cargarProductos();
});

watch(productos, () => {
  verificarALertasProductos();
}, {deep:true})

cargarProductos();


</script>

<template>
  <header>
      <ComImagen style="margin-left: 41.5%;"/>
  </header>
  <div class="container-buttom-come-back"><button @click="volver" class="btn-come-back"><font-awesome-icon :icon="faArrowLeft" class="arrow-back"/>Regresar</button></div>
  <hr/>
  
  <h1 id="panel">Panel Productos</h1>
  <hr id="l3" />
  <div class="button-container">
      <button @click="openAdd"  v-if="hasPermission([ROLES.JEFE, ROLES.ADMINISTRADOR])"  class="custom-button">Agregar Producto</button>
      <button @click="openAct"  v-if="hasPermission([ROLES.JEFE, ROLES.ADMINISTRADOR])"  class="custom-button">Actualizar Producto</button>
      
  </div>

  
  <transition name="fade2"><ComAgregarP v-if="AgregarProducto" @close="closeAdd"/></transition>
  <transition name="fade2"><ComConsulProPre v-if="ConsultarProducto" @close="closeCons"/></transition>
  <transition name="fade2"><ComActP v-if="ActualizarProducto" @close="closeAct"/></transition>


  <div class="search-bar">
    <input 
      type="text" 
      v-model="searchTerm" 
      placeholder="Buscar Productos..." 
      class="search-input"
      style="font-family: 'Jura', sans-serif;;"
    >
    <font-awesome-icon :icon="faSearch" class="search-icon"/>
  </div>
  

  <transition name="slide-fade">
    <div v-if="mostarPanelAlertas && tieneLAlertas && !panelAlertasMinimizado" class="panel-alertas">
      <div class="panel-alertas-header">
        <h4>Alertas de Inventario</h4>
        <div class="panel-alertas-acciones">
          <button class="btn-minimizar" @click="togglePanelAlertas">
            <font-awesome-icon :icon="faMinusCircle" />
          </button>
          
        </div>
      </div>

      <div class="panel-alertas-contenido">
        <div v-if="productosAgotados.length > 0" class="alerta-seccion alerta-agotado">
          <h5>Productos Agotados ({{ productosAgotados.length }})</h5>
          <ul class="alerta-lista">
            <li v-for="prodcuto in productosAgotados" :key="prodcuto.id" class="alerta-item">
              <span class="producto-nombre">{{ prodcuto.nombre }}</span>
              <button class="btn-accion-alerta" @click="openEmergente(prodcuto)">Ver</button>
              <button class="btn-accion-alerta" @click="openAct">Actualizar</button>
            </li>
          </ul>
        </div>

        <div v-if="productosProximosAgotarse.length > 0" class="alerta-seccion alerta-proximo">
        <h5>Productos proximo a Agotarse ({{ productosProximosAgotarse.length }})</h5>
        <ul class="alerta-lista">
          <li v-for="producto in productosProximosAgotarse" :key="producto.id" class="alerta-item">
            <span class="producto-nombre">{{ producto.nombre }}</span>
            <span class="stock-actual">{{ producto.cantidad }}</span>
            <button class="btn-accion-alerta" @click="openEmergente(producto)">Ver</button>
            <button class="btn-accion-alerta" @click="openAct">Actualizar</button>
          </li>
        </ul>
      </div>
      </div>

      
    </div>
  </transition>
  
  <button v-if="mostarPanelAlertas && tieneLAlertas && panelAlertasMinimizado" @click="togglePanelAlertas" class="btn-flotante-alertas"><font-awesome-icon :icon="faExclamationTriangle"/>{{ productosAgotados.length + productosProximosAgotarse.length }} Alertas 
  </button>
  <button  class="btn-cerrar" @click="cerrarPanelAlertas" ></button>
  <transition-group name="fade" tag="div" class="product-container">
  <div class="card2" v-for="producto in filtrarProductos" :key="producto.id">
    <div class="product-image">
      <img v-if="producto.ruta_imagen" :src="`https://coffebikefastapi-production.up.railway.app/productos/${producto.ruta_imagen}`" class="product-image" />
        <span v-else>{{ producto.imagen }}</span>
    </div>
    <div class="product-info">
        <div class="info-left">
          <p>Producto: <span class="product-name"> {{ producto.nombre }}</span></p>
          <p>Cantidad: <span class="product-quantity">{{ producto.cantidad }}</span></p>
        </div>
        <div class="info-right">
          <p>Precio: <span class="product-price">${{ producto.precio_salida }}</span></p>
          <p>Categoría: <span class="product-price">{{ producto.categoria }}</span></p>
        </div>  
    </div>
    <div class="product-buttons">
      <button class="delete-button" @click="eliminarProducto(producto.id)">
        Eliminar
      </button>
    </div>
     <button @click="openEmergente(producto)" class="card-button">Mas Informacion</button>
    </div>

    <div v-if="filtrarProductos.length === 0" class="no-results">
          No se encontraron ingredientes que coincidan con la búsqueda.
        </div>
  </transition-group>

  <div v-if="emergenteMasInformacion" class="moreInfo" @click.self="closeEmergente"> <!-- .self se para que si se da click por accidente no se cierre la ventana -->
    <div class="cardInfo">
        <div class="moreInfoImage">
          <img v-if="productoSeleccionado.ruta_imagen" :src="`https://coffebikefastapi-production.up.railway.app/productos/${productoSeleccionado.ruta_imagen}`" class="product-image" />
        </div>
        <div class="container-info">
          <p>ID: <span class="product-id">{{ productoSeleccionado.id }}</span></p>
            <p>Producto: <span class="product-name"> {{ productoSeleccionado.nombre }}</span></p>
            <p>Tipo: <span class="product-description">{{ productoSeleccionado.tipo }}</span></p>
            <p>Cantidad: <span class="product-quantity">{{ productoSeleccionado.cantidad }}</span></p>
            <p>Precio: <span class="product-price">${{ productoSeleccionado.precio_unitario }}</span></p>
            <p>Categoría: <span class="product-price">{{ productoSeleccionado.categoria }}</span></p>
            <p>Stock Minimo: <span class="product-price">{{ productoSeleccionado.stock_minimo }}</span></p>
    </div>
      <button @click="closeEmergente" class="closeMore">Cerrar</button>
    </div> 
  </div>


</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');

/*Estilos papa la aparicion de ventanas suavemente */

.fade2-enter-active, .fade-leave-active{
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade2-enter-from, .fade-leave-to{
  opacity: 0;
  transform: scale(0.9);
}
header {
  padding: 10px;
  background-color: #000000;
}

hr {
  border-top: 2px solid #D9AB23; 
  margin-top: 5px;
  width: 1300px;
  margin-left: 7%;
}
.btn-come-back{
  width: 120px;
  height: 30px;
  border: none;
  border-radius: 10px;
  background-color: #faad14;
  font-family: 'Jura', sans-serif;
  display: flex;
  gap: 10px;
  justify-content: center;
  padding: 7px;
  transition: all 0.2s ease-in-out;
}
.btn-come-back:hover{
  background-color: #A65814;
  transform: scale(1.05);
  cursor:pointer;
}
.container-buttom-come-back{
  margin-top: -83px;
  margin-left: 10%;
  padding: 23px;
}
.arrow-back{
  margin-top: 1px;
}
#l2 {
  margin-top: 100px;
  width: 800px;
  margin-left: 22%;
}
#panel{
  color: #D9AB23;
  font-family: 'Jura', sans-serif;
  font-weight:normal;
  text-align: center;
}

#l3{
  width: 1100px;
  margin-left: 183px;
  margin-top: 22px;
}
.button-container {
    display: flex;
    gap: 10px;
    margin-top: 53px;
    justify-content: center;
}
.custom-button {
  background-color: #A65814;
  color: #FFFFFF;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-family: 'Jura', sans-serif;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.custom-button:hover {
    background-color: #885b34;
}

/* Estilos de la barra de busqueda */
.search-input{
  margin-left: 32.8%;
  height: 30px;
  width: 520px;
  margin-top: 45px;
}
.search-input:focus {
  outline: none;  
  border: 1px solid #D9AB23; 
  box-shadow: 0 0 5px rgba(78, 141, 166, 0.5);  
  transition: ease-in-out 0.5s;
}
.search-icon{
  margin-left: 15px;
}

.product-container {
  width: 1000px;
  margin-left: 16%;
  margin-top: 70px;
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Tres columnas */
  gap: 40px; /* Espacio entre los productos */
  padding: 28px; /* Margen interno */
  justify-content: center; /* Centrar el contenido horizontalmente */
}
.card2 {
  font-family: 'Jura', sans-serif;
  width: 320px;
  height: 480px;
  background-color: #a65814cc;
  color: white;
  border-radius: 12px;
  text-align: left;
  font-size: 14px;
  padding: 19px;
  transition: transform 0.2s ease-in-out;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid rgb(72, 65, 65);
}

.fade-enter-active, .fade-leave-active{
  transition: opacity 0.8s ease-out, transform 0.5s ease-out;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-15px) scale(0.95);
}

.fade-leave-to{
  opacity: 0;
  transform: translateY(15px) scale(0.95);
}

.card2:hover {
  transform: scale(1.04);
  border-radius: 20px;
}
.card-button {
 transform: translate(-50%, 125%);
 width: 60%;
 border-radius: 1rem;
 border: none;
 background-color: #D9AB23;
 color: #fff;
 font-size: 1rem;
 padding: .5rem 1rem;
 position: absolute;
 left: 50%;
 bottom: 0;
 opacity: 0;
 transition: 0.3s ease-out;
}
.card2:hover {
 border-color: #ff5900;
 box-shadow: 0 4px 18px 0 rgba(0, 0, 0, 0.25);
}
/*boton despues de hacer hover*/
.card2:hover .card-button {
 transform: translate(-50%, 50%);
 opacity: 1;
 cursor: pointer;
}
.product-image {
  width: 90%;
  height: 200px;
  border-radius: 10%;
  overflow: hidden;
  margin-left: 5.5%;
}
.product-info {
  display: flex;
  justify-content: space-between;
  margin-left: 25px;
}
.product-info p{
  font-size: 20px;
}
.product-info span{
  font-size: 15px;
}
.info-left, .info-right {
  width: 50%;
}
.info-left p, .info-right p {
  margin: 20px;
}
.delete-button {
  background-color: #f3ea78;
  color: rgb(9, 8, 8);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 15px;
  margin-left: 100px;
}
.delete-button:hover {
  background-color: #deaf2e;
}
.product-name {
    color: rgb(255, 255, 255);
    display: block;
}
.product-description {
  color: rgb(255, 255, 255);
  display: block;
}
.product-quantity {
  color: rgb(248, 247, 244);
  display: block;
}
.product-price {
    color: rgb(255, 255, 255);
    font-size: 1.1em;
    display: block;
}
.moreInfo{
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
.cardInfo {
  background: rgb(0, 0, 0);
  padding: 20px;
  border-radius: 10px;
  width: 800px;
  height: 500px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  border: solid 1px #fff;
  font-family: 'Jura', sans-serif;
}

.container-info{
  height: 200px;
  width: 200px;
  margin-left: 520px;
  margin-top: -410px;
}

.moreInfoImage img{
  background-color: #A65814;
  width: 400px;
  margin-top: 40px;
  height: 400px;
  margin-left: -350px;
}

.closeMore{
  background-color: #a41010;
  color: rgb(255, 255, 255);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 15px;
  margin-left: 100px;
  margin-top: 220px;
}
.closeMore:hover{
  transform: scale(1.1);
  transition: ease-out 0.3s;
  background-color: #b14a33;
}
.no-results{
  font-size: 24px;
  font-family: 'Jura', sans-serif;
  margin-left: 280px;
  width: 500px;
  height: 200px;

}
.no-results {
  animation: Text 0.2s ease-out forwards;
}

@keyframes Text {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.panel-alertas {
  position: fixed;
  top: 80px;
  right: 20px;
  width: 370px;
  background-color: rgb(0, 0, 0);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgb(255, 255, 4);
  z-index: 1000;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 60vh;
}
.panel-alertas-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #000000;
  border-bottom: 1px solid #D9AB23;
  width: 330px;
}
.panel-alertas-header h4 {
  font-family: 'Jura', sans-serif;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}
.panel-alertas-acciones {
  display: flex;
  gap: 8px;
}
.btn-minimizar {
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  transition: all 0.2s ease-in-out;
}
.btn-minimizar:hover{
  background-color: rgba(0, 0, 0, 0);
  transform: scale(1.2);
}
.btn-cerrar {
  background: none;
  border: none;
  cursor: pointer;
  color: #ffffff;
  font-size: 16px;
  border-radius: 50%;
  transition: all 0.2s ease-in-out;
  margin-top: -15px;
  margin-left: 5px;
}
.btn-cerrar:hover{
  background-color: rgba(0, 0, 0, 0);
  transform: scale(1.2);
}
.panel-alertas-contenido {
  padding: 0;
  overflow-y: auto;
}
.alerta-seccion {
  padding: 12px 16px;
}

.alerta-agotado {
  background-color: #0e0b0b;
  border-bottom: 1px solid #ffccc7;
  width: 330px;
}

.alerta-proximo {
  background-color: #000000;

}
.alerta-seccion h5 {
  font-family: 'Jura', sans-serif;
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
}
.alerta-lista {
  margin: 0;
  padding: 0;
  list-style: none;
}
.alerta-item {
  font-family: 'Jura', sans-serif;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 13px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}
.alerta-item:last-child {
  border-bottom: none;
}

.producto-nombre {
  flex: 1;
  font-weight: 500;
}
.stock-actual {
  margin: 0 12px;
  color: #666;
}
.btn-accion-alerta {
  font-family: 'Jura', sans-serif;
  padding: 4px 8px;
  background-color: #faad14;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  margin-left: 8px;
  transition: all 0.1s ease-in-out;
}
.btn-accion-alerta:hover {
  background-color: #A65814;
  transform: translateY(-3px) ;
}
/* Botón flotante para mostrar alertas */
.btn-flotante-alertas {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 10px 16px;
  background-color: #ff4d4f;
  color: white;
  border: none;
  border-radius: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  height: 43px;
  gap: 8px;
  font-weight: 600;
  z-index: 990;
  transition: all 0.1s ease-in-out;
}
.btn-flotante-alertas:hover {
  background-color: #ff7875;
  transform: scale(1.04);
}
/* Estilos para productos con alertas */
.tarjeta-producto {
  /* Tus estilos de tarjeta existentes */
  position: relative;
}
.producto-agotado {
  opacity: 0.75;
  border: 2px solid #ff4d4f !important;
}
.producto-proximo-agotarse {
  border: 2px solid #faad14 !important;
}
.badge-estado {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  z-index: 1;
}
.badge-agotado {
  background-color: #ff4d4f;
  color: white;
}
.badge-proximo {
  background-color: #faad14;
  color: white;
}
/* Animaciones */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>