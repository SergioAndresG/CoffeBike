<script setup lang="ts">
import Swal from 'sweetalert2';
import { ref, computed, onMounted, watchEffect,watch } from 'vue';
import axios from 'axios';
import ComImagen from './icons/IMGENES/ComImagen.vue';
import FormAddMateria from './FormAddMateria.vue';
import FormActMateria from './FormActMateria.vue';
import FormAddStock from './FormAddStock.vue';
import { faArrowLeft, faExclamationTriangle, faMinusCircle, faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useRouter } from 'vue-router';


// Variable para almacenar datos de la busqueda de materia
const searchTerm = ref("")
// Lista de materias primas
const empleado = ref([]);
const materiasPrimas = ref([]);
// Contraseña obtenida de la informacion proporcionada por el endpoint
const contraseñaProporcionada = ref("");

// Estado para el usuario actual y su rol
const currentUser = ref(null);
const userRole = ref('');

//configuaracion de alertas stock
const umbralAgotado = ref(null);
const umbralProximoAgotar = ref(0);

//estado para el panel de alertas
const mostarPanelAlertas = ref(false);
const panelAlertasMinimizado = ref(false);


watchEffect(() => {
  if (materiasPrimas.value.length > 0) {
    // Establece umbralAgotado a 0 directamente
    umbralAgotado.value = 0;
    
    // Calcula el umbral próximo a agotar basado en los stock_minimo
    const stockMinimos = materiasPrimas.value.map(p => parseFloat(p.stock_minimo) || 0);
    if (stockMinimos.length > 0) {
      umbralProximoAgotar.value = Math.min(...stockMinimos);
    }
  }
});

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

//Variables reactivas para la carta emergente con informacion del producto
const emergenteMasInformacion = ref(false);
const materiaSeleccionada = ref({});

//Variables para la carta emergente para agregar mas stock a una materia prima 
const materiaStockSeleccionada = ref(null);

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
// Cargar materias primas desde la API
const cargarMateriasPrimas = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/materia");
    materiasPrimas.value = respuesta.data;
  } catch (error) {
    console.error("Error al cargar materias primas:", error);
  }
  
};


const verificarALertasMaterias = async () => {
  const materiasAgotados = materiasPrimas.value.filter(p =>
    parseFloat(p.cantidad) <= parseFloat(umbralAgotado.value)
  );

  const materiasProximosAgotarse = materiasPrimas.value.filter(p =>
    parseFloat(p.cantidad) > parseFloat(umbralAgotado.value) &&
    parseFloat(p.cantidad) <= parseFloat(p.stock_minimo)
  );


  //si hay productos con alertas mostrar el mensaje
 if(materiasAgotados.length> 0 || materiasProximosAgotarse.length > 0){
    mostarPanelAlertas.value = true;

    //con los mensajes emergentes se le notifica al usuarios, solo la primera vez
    

    if(!localStorage.getItem('alertasStockMateriasMostradas')){
      let mensaje = '';

      if(materiasAgotados.length>0){
        mensaje += `<strong class="text-danger">¡Atención!</strong> Hay ${materiasAgotados.length} productos agotados. <br>`;
      }
      if(materiasProximosAgotarse.length>0){
        mensaje += `<strong class="text-warning">Advertencia</strong> Hay ${materiasProximosAgotarse.length} próximos a agotarse.`;
      }

      Swal.fire({
          title: "Estado del inventario",
          html: mensaje,
          icon: "warning",
          confirmButtonText: "Revisar",
          showCancelButton: true,
          cancelButtonText: 'Más tarde'
        }).then((result) => {
          if (result.isConfirmed) {
            mostarPanelAlertas.value = true;
            panelAlertasMinimizado.value = false;
          } else {
            panelAlertasMinimizado.value = true;
          }
      });


      //marcar como mostradas para no molestar constantemente
      localStorage.setItem('alertasStockMateriasMostradas', 'true');
      //se reinicia el estado despues de una hora si aun no se ha hecho el re-stock
      setTimeout(()=>{
        localStorage.removeItem('alertasStockMateriasMostradas');
      }, 60*60*1000);
    }
  }
};
materiasPrimas.value.forEach(p => {
  console.log(`${p.nombre}: cantidad=${p.cantidad} (${typeof p.cantidad}), stock_minimo=${p.stock_minimo} (${typeof p.stock_minimo})`);
});

verificarALertasMaterias();

const materiasPrimasAgotados = computed(() => {
  return materiasPrimas.value.filter(p => 
    parseFloat(p.cantidad) <= parseFloat(umbralAgotado.value)
  );
});

const materiasPrimasProximosAgotarse = computed(() => {
  return materiasPrimas.value.filter(materiaPrima => 
    parseFloat(materiaPrima.cantidad) > parseFloat(umbralAgotado.value) && 
    parseFloat(materiaPrima.cantidad) <= parseFloat(materiaPrima.stock_minimo)
  );
});

const tieneLAlertas=computed(()=>{
  return materiasPrimasAgotados.value.length > 0 || materiasPrimasProximosAgotarse.value.length
});



cargarEmpleados();

// Eliminar una materia prima
const eliminarMateria = async (idMateria: number) => {
  // Verificar permisos antes de intentar eliminar
  if (!hasPermission([ROLES.JEFE])) {
    Swal.fire({
      icon: 'error',
      title: 'Acceso denegado',
      text: 'No tienes permisos para eliminar materia prima.'
    });
    return;
  }
  try {

    // Confirmar antes de eliminar
    const confirmResult = await Swal.fire({
      title: '¿Estás seguro?',
      text: "Esta acción no se puede revertir",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    });

    if(!contraseñaProporcionada){
      console.error("no se encontro la contraseña del jefe");
      return;
    }

    // Crear el DTO con los datos necesarios
    const eliminarMateriaDTO = {
      idMateriaaEliminar: idMateria, 
      contraseñaProporcionada: contraseñaProporcionada.value 
    };

    console.log("Datos enviados:", eliminarMateriaDTO);

  // Realizar la solicitud DELETE al backend
  if (confirmResult.isConfirmed) {
      // Realizar la solicitud DELETE al backend enviando solo el ID en el cuerpo de la solicitud
      const response = await axios.delete("http://127.0.0.1:8000/materia/eliminar", {
      data: eliminarMateriaDTO,  // Enviar el DTO en el cuerpo de la solicitud
      headers: {
        "Content-Type": "application/json"
      }
    });
  
      Swal.fire(
        'Eliminado',
        'La materia prima ha sido eliminada correctamente.',
        'success'
      );
  
      // Recargar la lista de materias para reflejar los cambios
      cargarMateriasPrimas();
    }
  } catch (error) {
    console.error("Error al eliminar la materia:", error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'No se pudo eliminar la materia prima.'
    });
  }

};


// Filtrar materias primas en la búsqueda
const filtrarMateriasPrimas = computed(() => {
  if (!searchTerm.value.trim()) return materiasPrimas.value;

  const term =searchTerm.value.toLowerCase().trim()
  return materiasPrimas.value.filter(materia =>
    materia.nombre.toLowerCase().includes(term)
  )
});

const ActualizarMateria = ref(false);
const AgregarMateria = ref(false);
const AgregarStock = ref(false);

const openEmergente = (materia) => {
  emergenteMasInformacion.value = true; // Gurada la materia seleccionado
  materiaSeleccionada.value = materia; // Para la informacion de la materia selecionada

}

const closeEmergente = () => {
  emergenteMasInformacion.value = false;
}

// Funciones para abrir y cerrar modales
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
  ActualizarMateria.value = true;
  // Usamos esto para evitar scroll en el body principal
  document.documentElement.style.overflow = "hidden";
  document.documentElement.style.height = "100hv";

}

const closeAct = () => {
  ActualizarMateria.value = false;
  // Restaurtamos el scroll en el body principal
  document.documentElement.style.overflow = "";
  document.documentElement.style.height = "";
cargarMateriasPrimas ();
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
  AgregarMateria.value = true;
  // Usamos esto para evitar scroll en el body principal
  document.documentElement.style.overflow = "hidden";
  document.documentElement.style.height = "100hv";
};

const closeAdd = () => {
  AgregarMateria.value = false;
   // Restaurtamos el scroll en el body principal
  document.documentElement.style.overflow = "";
  document.documentElement.style.height = "";
cargarMateriasPrimas ();
};

const openStockModal = async (materia) => {
   // Verificar si el usuario tiene permisos para actualizr cantidad
  if (!hasPermission([ROLES.JEFE, ROLES.ADMINISTRADOR])) {
    Swal.fire({
      icon: 'error',
      title: 'Acceso denegado',
      text: 'No tienes permisos para agregar materia prima.'
    });
    return;
  }
  AgregarStock.value = true;
  materiaStockSeleccionada.value = materia;
  document.documentElement.style.overflow = "hidden";
  document.documentElement.style.height = "100hv";
};

const closeStockModal = () => {
  AgregarStock.value = false;
  document.documentElement.style.overflow = "";
  document.documentElement.style.height = "";
cargarMateriasPrimas();
};

const togglePanelAlertas = () => {
  panelAlertasMinimizado.value = !panelAlertasMinimizado.value
}

const cerrarPanelAlertas = () => {
 mostarPanelAlertas.value = false
}


// Cargar datos al montar el componente
onMounted(async () => {
  await loadUserData();
  await cargarMateriasPrimas();
  verificarALertasMaterias();
});

watch(materiasPrimas, () => {
  verificarALertasMaterias();
}, { deep: true });

//funcion para boton para volver entre paginas
const router = useRouter();

const volver = () => {
  router.go(-1)
}

</script>

<template>
  <header>
      <ComImagen style="margin-left: 41.5%;"/>
  </header>
  <div class="container-buttom-come-back"><button @click="volver" class="btn-come-back"><font-awesome-icon :icon="faArrowLeft" class="arrow-back"/>Regresar</button></div>

  <hr />
  <h1 id="panel">Panel Materia Prima</h1>
  <hr id="l3" />
  <!-- Botones condicionados por rol -->
  <div class="button-container">
    <button 
      v-if="hasPermission([ROLES.JEFE, ROLES.ADMINISTRADOR])" 
      @click="openAdd" 
      class="custom-button"
    >
      Agregar Materia Prima
    </button>
    <button 
      v-if="hasPermission([ROLES.JEFE, ROLES.ADMINISTRADOR])" 
      @click="openAct" 
      class="custom-button"
    >
      Actualizar Materia Prima
    </button>
  </div>

  <transition name="fade2"><FormAddMateria v-if="AgregarMateria" @close="closeAdd" /></transition>
  <transition name="fade2"><FormActMateria v-if="ActualizarMateria" :materia="materiaSeleccionada" @close="closeAct" /></transition>

  <div class="search-bar">
    <input 
      type="text" 
      v-model="searchTerm" 
      placeholder="Buscar Materias Primas..." 
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
        <div v-if="materiasPrimasAgotados.length > 0" class="alerta-seccion alerta-agotado">
          <h5>Productos Agotados ({{ materiasPrimasAgotados.length }})</h5>
          <ul class="alerta-lista">
            <li v-for="producto in materiasPrimasAgotados" :key="producto.id" class="alerta-item">
              <span class="producto-nombre">{{ producto.nombre }}</span>
              <button class="btn-accion-alerta" @click="openEmergente(producto)">Ver</button>
              <button class="btn-accion-alerta" @click="openAct">Actualizar</button>
            </li>
          </ul>
        </div>

        <div v-if="materiasPrimasProximosAgotarse.length > 0" class="alerta-seccion alerta-proximo">
        <h5>Productos proximo a Agotarse ({{ materiasPrimasProximosAgotarse.length }})</h5>
        <ul class="alerta-lista">
          <li v-for="producto in materiasPrimasProximosAgotarse" :key="producto.id" class="alerta-item">
            <span class="producto-nombre">{{ producto.nombre }}</span>
            <span class="stock-actual">{{ producto.cantidad }}  {{ producto.unidad_medida.simbolo }}</span>
            <button class="btn-accion-alerta" @click="openEmergente(producto)">Ver</button>
            <button class="btn-accion-alerta" @click="openStockModal(producto)">Actualizar</button>
          </li>
        </ul>
      </div>
      </div>

      
    </div>
  </transition>

  <button v-if="mostarPanelAlertas && tieneLAlertas && panelAlertasMinimizado" @click="togglePanelAlertas" class="btn-flotante-alertas"><font-awesome-icon :icon="faExclamationTriangle"/>{{ materiasPrimasAgotados.length + materiasPrimasProximosAgotarse.length }} Alertas 
  </button>

  <transition-group name="fade" tag="div" class="product-container">
  
    <div class="card2" v-for="materia in filtrarMateriasPrimas" :key="materia.id">
      <div class="product-image">
        <img
          v-if="materia.ruta_imagen"
          :src="`http://127.0.0.1:8000/materia/${materia.ruta_imagen}`"
          class="product-image"
        />
        <span v-else>{{ materia.imagen }}</span>
      </div>
      <div class="product-info">
        <p>Nombre: <span class="product-name">{{ materia.nombre }} </span></p>
        <p>Cantidad: <span class="product-quantity">{{ materia.cantidad }}-{{ materia.unidad.simbolo }}</span></p>
        <p>Stock Minimo: <span class="product-quantity">{{ materia.stock_minimo}}-{{ materia.unidad.simbolo }}</span></p>
        <p>Unidad de Medida: <span class="product-quantity">{{ materia.unidad.simbolo }}</span></p>
      </div>

      <div class="product-buttons">
        <!-- Botón de eliminar solo para JEFE -->
        <button 
          v-if="hasPermission([ROLES.JEFE])"  class="delete-button" @click="eliminarMateria(materia.id)">
          Eliminar
        </button>
      </div>

      <button @click="openEmergente(materia)" class="card-button">Más Información</button>
    </div>

  <div v-if="filtrarMateriasPrimas.length === 0" class="no-results">
    No se encontraron materias primas que coincidan con la búsqueda.
  </div>
  </transition-group>
  <FormAddStock v-if="AgregarStock" :materia="materiaStockSeleccionada" @close="closeStockModal" />

  <div v-if="emergenteMasInformacion" class="moreInfo" @click.self="closeEmergente">
    <div class="cardInfo">
      <div class="moreInfoImage">
        <img
          v-if="materiaSeleccionada.ruta_imagen"
          :src="`http://127.0.0.1:8000/materia/${materiaSeleccionada.ruta_imagen}` 
          "class="product-image"
        />
      </div>
      <div class="container-info">
        <p>ID: <span class="product-id">{{ materiaSeleccionada.id }}</span></p>
        <p>Materia Prima: <span class="product-name">{{ materiaSeleccionada.nombre }}</span></p>
        <p>Cantidad: <span class="product-quantity">{{ materiaSeleccionada.cantidad }}</span></p>
        <p>Stock Mínimo: <span class="product-price">{{ materiaSeleccionada.stock_minimo }}</span></p>
        <p>Fecha Ingreso : <span class="product-price">{{ materiaSeleccionada.fecha_ingreso }}</span></p>
        <p>Vida Util (dias): <span class="product-quantity">{{ materiaSeleccionada.vida_util_dias }}</span></p>
        <p>Fecha vencimiento: <span class="product-price">{{ materiaSeleccionada.fecha_vencimiento }}</span></p>
        <p>Unidad de medida: <span class="product-price">{{ materiaSeleccionada.unidad.simbolo }}</span></p>
      </div>
      <button @click="closeEmergente" class="closeMore">Cerrar</button>
    </div>
  </div>

  <footer>
    <p>&copy; 2024</p>
  </footer>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');
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
    margin-top: 10px;
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
    margin-top: 4px;
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
        font-family: Arial, sans-serif;
        font-size: 14px;
        cursor: pointer;
        transition: background-color 0.3s;
        font-family: 'Jura', sans-serif;
    }

    .custom-button:hover {
        background-color: #D9AB23;
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

.info-button {
  background-color: #A65814;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.info-button:hover {
  background-color: #513d03;
}

.product-container {
  width: 1000px;
  margin-left: 16%;
  margin-top: 70px;
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Tres columnas */
  gap: 40px; /* Espacio entre los productos */
  padding: 20px; /* Margen interno */
  justify-content: center; /* Centrar el contenido horizontalmente */
}

.card2 {
  font-family: 'Jura', sans-serif;
  width: 320px;
  height: 450px;
  background-color: #c89a1f;
  color: rgb(255, 255, 255);
  border-radius: 12px;
  text-align: left;
  font-size: 17px;
  padding: 15px;
  transition: transform 0.2s ease-in-out;
  box-shadow: 0px 4px 6px rgba(139, 108, 21, 0.705);
  border: 1px solid rgb(255, 255, 255);
}

.card2:hover {
  transform: scale(1.03);
  border-radius: 20px;
  box-shadow: 0px 4px 6px rgba(139, 108, 21, 0.705);
  background-color: #D9AB23;

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
  font-size: 19px;
}

.container-info{
  height: 200px;
  width: 200px;
  margin-left: 520px;
  margin-top: -380px;
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
  margin-top: 170px;
}
.closeMore:hover{
  transform: scale(1.1);
  transition: ease-out 0.3s;
  background-color: #b14a33;
}

.card-button {
 transform: translate(-50%, 125%);
 width: 50%;
 border-radius: 1rem;
 border: none;
 background-color: #A65814;
 color: #ffffff;
 font-size: 1rem;
 padding: .5rem 1rem;
 position: absolute;
 left: 50%;
 bottom: 0;
 opacity: 0;
 transition: 0.3s ease-out;
}
.card2:hover .card-button {
 transform: translate(-50%, 50%);
 opacity: 1;
 cursor: pointer;
}


.product-image {
  width: 60%;
  height: 150px;
  border-radius: 10%;
  overflow: hidden;
  margin-left: 10%;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  margin-top: 15px;
  margin-left: 45px;
}


#product-id {
  margin-top: 15px;
  margin-left: 45px;
}

.delete-button {
  background-color: #f5d881;
  color: rgb(0, 0, 0);
  border: none; 
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 34px;
  margin-left: 100px;
}

.delete-button:hover {
  background-color: #c89a1f;
}

.add-button {
  background-color: #f5d881;
  color: rgb(0, 0, 0);
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 5px;
  margin-left: 40px;
}

.add-button:hover {
  background-color: #c89a1f;
}

.product-name {
    color: blue;
    color: rgb(255, 255, 255);
}

.product-id {
  margin-top: 300px;
}

.product-description {
    color: rgb(255, 255, 255);
}

.product-quantity {
    color: rgb(248, 247, 244);
}

.product-price {
    color: rgb(255, 255, 255);
    font-size: 1.1em;
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

        footer {
      padding: 20px;
      text-align: center;
      margin-top: 34px;
  }
  
  footer nav ul {
      list-style: none;
      display: inline-block;
  }
  
  footer nav li {
      display: inline;
      margin: 0 10px;
  }
  
  footer a {
      text-decoration: none;
      color: #333;
  }



  @media (max-width: 767px) {
  .logo{
    margin-left: -28%;
    margin-top: 15%;
  }
  hr {
    margin-left: 9%;
    width: 300px;
    margin-top: -1rem;
  }
  #l2 {
    margin-top: 5px;
    margin-left: 23%;
    width: 200px;
  }
  #l3 {
    margin-top: 5px;
    margin-left: 23%;
    width: 200px;
  }
  .button-container{
    margin: 0;
    padding: 2vh;
  }
  .product-container {
    grid-template-columns: 1fr;
    width: 97%;
    margin: 30px auto 0;
    gap: 12px;
    padding: 10px;
  }
  .card2 {
    min-height: auto;
    padding: 12px;
    flex-direction: row;
    border-radius: 8px;
    height: auto;
  }
  .card2:hover {
    transform: scale(1.02);
    border-radius: 8px;
  }
  .product-image {
    width: 30%;
    height: 90px;
    margin: 0;
    border-radius: 6px;
    flex-shrink: 0;
  }
  .product-info {
    width: 70%;
    padding-left: 12px;
    justify-content: center;
  }
  .product-name-label {
    font-size: 18px;
    margin-bottom: 8px;
    text-align: left;
  }
  .info-details {
    gap: 6px;
  }
  
  .info-details p {
    font-size: 14px;
  }
  
  .info-details span {
    font-size: 13px;
  }
  
  .product-buttons {
    position: absolute;
    right: 10px;
    bottom: 12px;
    margin: 0;
  }
  
  .delete-button {
    font-size: 12px;
    padding: 6px 12px;
    max-width: none;
  }
}

</style>