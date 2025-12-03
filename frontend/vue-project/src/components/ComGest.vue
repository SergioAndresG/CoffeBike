<script setup lang="ts">
import ComImagen from './icons/IMGENES/ComImagen.vue';
import ComForAgregar from './ComForAgregar.vue';
import { onMounted, ref, computed } from 'vue';
import ComForDel from './ComForDel.vue';
import ComForAct from './ComForAct.vue';
import axios from "axios";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faArrowLeft, faSearch } from '@fortawesome/free-solid-svg-icons';
import { useRouter } from 'vue-router';

const empleados = ref([]); // Lista reactiva para almacenar los empleados
const searchTerm = ref("");

//funcion para boton para volver entre paginas
const router = useRouter();

const volver = () => {
  router.back();
};

const filtrarProductos = computed (()=> {
  if(!searchTerm.value.trim()) return empleados.value;

  const term =searchTerm.value.toLowerCase().trim()
  return empleados.value.filter(pro => 
    pro.nombre.toLowerCase().includes(term)
  )
});


// Función para cargar empleados desde el backend
const cargarEmpleados = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/usuarios");
    empleados.value = respuesta.data.map(empleado => ({
      ...empleado,
    }));
  } catch (error) {
    console.error("Error al cargar empleados:", error);
  }
};
// Llamar a cargarEmpleados cuando el componente se monte
onMounted(() => {
  cargarEmpleados();
});



const isModalOpen = ref(false);
const isModalOpen2 = ref(false);
const isModalOpen3 = ref(false);

const openModal = () => {
  isModalOpen.value = true;
};
const closeModal = () => {
  isModalOpen.value = false;
};
cargarEmpleados();
const Eliminar = () => {
  isModalOpen2.value = true;
};
cargarEmpleados();
const EliminarClose = () => {
  isModalOpen2.value = false;
};
cargarEmpleados();
const Actualizar = () => {
  isModalOpen3.value = true;
};
cargarEmpleados();
const ActualizarClose = () => {
  isModalOpen3.value = false;
};
cargarEmpleados();

</script>

<template>
  <header>
    <ComImagen style="margin-left: 41.5%;"/>
  </header>
  <div class="container-buttom-come-back"><button @click="volver" class="btn-come-back"><font-awesome-icon :icon="faArrowLeft" class="arrow-back"/>Regresar</button></div>
  <hr>

  <h1>Panel Usuarios</h1>

  <hr id="l2">
     <section class="button-container">
        <button @click="openModal" id="A">Agregar Trabajador</button>
        <button @click="Eliminar" id="A">Eliminar Trabajador</button>
        <button @click="Actualizar" id="A">Actualizar Trabajador</button>
     </section>
     <div class="search-bar">
    <input 
      type="text" 
      v-model="searchTerm" 
      placeholder="Buscar Usuarios..." 
      class="search-input"
      style="font-family: 'Jura', sans-serif;;"
    >
    <font-awesome-icon :icon="faSearch" class="search-icon"/>
  </div>
    <!-- Componente Modal -->
    <ComForAgregar v-if="isModalOpen" @close="closeModal" />
    <ComForDel v-if="isModalOpen2" @close="EliminarClose" />
    <ComForAct v-if="isModalOpen3" @close="ActualizarClose"/>

  <transition-group name="fade" tag="div" class="empleado-container">
  <div class="card2" v-for="empleado in filtrarProductos" :key="empleado.id">
    <div class="empleado-image">
      <img v-if="empleado.ruta_imagen" :src="`https://coffebikefastapi-production.up.railway.app/usuarios/${empleado.ruta_imagen}`" class="empleado-image" />
        <span v-else>{{ empleado.imagen }}</span>
    </div>
    <div class="empleado-info">
        <div class="info-left">
          <p>Nombre: <span class="empleado-name"> {{ empleado.nombre }}</span></p>
          <p>Telefono: <span class="empleado-telefono">{{ empleado.telefono }}</span></p>
          <p>Correo: <span class="empleado-price">{{ empleado.correo }}</span></p>
        </div>
        <div class="info-right">
          <p>Documento: <span class="empleado-price">{{ empleado.documento }}</span></p>
          <p>Rol: <span class="empleado-price">{{ empleado.rol }}</span></p>

          
        </div>  
    </div>
    </div>

    <div v-if="filtrarProductos.length === 0" class="no-results">
          No se encontraron ingredientes que coincidan con la búsqueda.
        </div>
  </transition-group>  

   
    <footer>
      <p>&copy; 2025 </p>
  </footer>
</template>


  
<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');
body{
  font-family: 'Jura', sans-serif;
  font-weight:normal;
}
header {
  padding: 10px;
  background-color: #000000;
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
hr {
  border-top: 2px solid #D9AB23;
  margin-top: 5px;
  width: 1300px;
  margin-left: 7%;
}
#l2 {
  margin-top: 10px;
  width: 800px;
  margin-left: 22%;
}
h1, #txt {
text-align: center;
color: #D9AB23;
font-family: 'Jura', sans-serif;
}
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
.button-container {
    display: flex;
    gap: 10px;
    margin-top: 53px;
    justify-content: center;
}
#A{
  background-color: #A65814; 
    color: #FFFFFF;
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-family: 'Jura', sans-serif;
    font-size: 14px;
    cursor: pointer;
    transition: 0.3s ease-in-out;
}
#A a{
  text-decoration: none;
  color: #ddd
}
#A:hover{
  background-color: #885b34;
  transform: translateY(-2px) scale(1.04);
}
.empleado-container {
  width: 1000px;
  margin-left: 16%;
  margin-top: 70px;
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Tres columnas */
  gap: 20px; /* Espacio entre los productos */
  padding: 20px; /* Margen interno */
  justify-content: center; /* Centrar el contenido horizontalmente */
}
.card2 {
  font-family: 'Jura', sans-serif;
  width: 320px;
  height: 480px;
  background-color: #A65814; 
  color: white;
  border-radius: 12px;
  text-align: left;
  font-size: 14px;
  padding: 19px;
  transition: transform 0.2s ease-in-out;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid rgb(72, 65, 65);
}
.card2:hover {
  border-color: #ff5900;
  box-shadow: 0 4px 18px 0 rgba(0, 0, 0, 0.25);
  transform: scale(1.04);
  border-radius: 20px;
}

.empleado-info {
  display: flex;
  justify-content: space-between;
  margin-left: 25px;
}
.empleado-info p{
  font-size: 20px;
}
.delete-button {
  background-color: #d9ab23;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 15px;
}
.delete-button:hover {
  background-color: #c89a1f;
}
.empleado-image {
  width: 90%;
  height: 200px;
  border-radius: 10%;
  overflow: hidden;
  margin-left: 5.5%;
}
.empleado-name {
  color: rgb(255, 255, 255);
  display: block;

}
.empleado-id {
  margin-top: 300px;
}
.empleado-description {
    color: rgb(255, 255, 255);
    display: block;

}
.empleado-telefono {
    color: rgb(248, 247, 244);
    display: block;

}
.empleado-price {
    color: rgb(255, 255, 255);
    font-size: 1.1em;
}
.empleado-info span{
  font-size: 15px;
}
.info-left, .info-right {
  width: 50%;
}

.info-left p, .info-right p {
  margin: 20px;
  margin-left: -10px;
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
footer p{
  font-family: 'Jura', sans-serif;
}
footer a {
  text-decoration: none;
  color: #333;
  font-family: 'Jura', sans-serif;
}

@media screen and (min-width: 280px) and (max-width: 490px) {
    .menu-hamburguesa {
    position: fixed;
    top: 50px;
    right: 20px;
    z-index: 1000; /* Esto me asegura que el menu este encima del resto del contenido */
    }

    .menu-icon {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      width: 40px;
      height: 30px;
      cursor: pointer;
    }

    .menu-icon span {
      display: block;
      height: 4px;
      background-color: #BF8B8F;
      margin-bottom: 5px;
    }

    #menu-toggle {
      display: none;
    }

    .menu {
      position: fixed;
      top: 5;
      right: -250px; 
      height: 90vh;
      width: 170px;
      background-color: #fff;
      list-style: none;
      padding: 50px 20px;
      box-shadow: -2px 0px 5px rgba(239, 179, 179, 0.716);
      transition: right 0.3s ease-in-out;
    }

    .menu li {
      margin: 20px 0;
    }

    .menu li a, .menu li router-link {
      text-decoration: none;
      color: #333;
    }

    #menu-toggle:checked + .menu-icon + .menu {
      right: 0; /*Este mueve el menu dentro de la pantalla */
    }

    #menu-toggle:checked + .menu-icon span:nth-child(1) {
      transform: rotate(45deg);
      position: relative;
      top: 12px;
    }

    #menu-toggle:checked + .menu-icon span:nth-child(2) {
      opacity: 0;
    }

    #menu-toggle:checked + .menu-icon span:nth-child(3) {
      transform: rotate(-45deg);
      position: relative;
      top: -8px;
    }
    nav ul {
      flex-direction: column;
      margin-left: 0;
      margin-top: 10px;
    }

    nav li {
      margin-bottom: 10px;
    }

    #l2, hr {
      width: 100%;
      margin-left: 0;
      margin-top: 30px;
    }


    .progress-container {
      margin-left: 0;
      width: 100%;
      margin-top: 60px;
    }

    .sidebar {
    width: 200px;
    background-color: #f2d2d0;
    padding: 20px;
    border-radius: 10px;
    margin-left: 10px;
    }
    .employee-actions button {
    align-items: center;
    }
    footer {
      padding: 10px;
      font-size: 12px;
    }

    .wrapper {
      height: auto;
      padding-top: 20px;
    }

    .wrapper .icon {
      width: 40px;
      height: 40px;
      font-size: 16px;
    }

    .wrapper .tooltip {
      font-size: 12px;
      padding: 3px 5px;
    }
 
  }
  </style>