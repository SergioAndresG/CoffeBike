<script setup lang="ts">
import { onMounted, ref } from 'vue';
import ComImagen from './icons/IMGENES/ComImagen.vue';
import router from '@/routers/misrutas';
import { getCurrentUser } from '@/servicies/auths';
import ActulizacionPerfil from './ActulizacionPerfil.vue';

const usuario = ref(null);
const isModalOpen = ref(false);
const menuActive = ref(false);


const logout = () => {
  localStorage.removeItem("jwtToken");
  localStorage.removeItem("userData");
  router.push({path: "/"});
  if (window.innerWidth<768) {
    menuActive.value = false;
  }
}

const toggleMenu = () =>{
  menuActive.value =! menuActive.value;
}

onMounted(async () => {
  usuario.value = JSON.parse(localStorage.getItem("userData") || null)
  const freshData = await getCurrentUser();
  if(freshData) usuario.value = freshData;
});

const actualizar = () => {
  isModalOpen.value = true;
  if (window.innerWidth<768) {
    menuActive.value = false;
  }
};
const actualizarClose = async () => {
  isModalOpen.value = false;
  const freshData = await getCurrentUser(); // se llama nuevamente la api
  if (freshData) usuario.value = freshData; // actualiza los campos del usuario
};

</script>

<template>
  <header>
    <nav class="navbar">
      <ComImagen class="logo" />
      <!-- Botón del menú hamburguesa (visible solo en móvil) -->
      <div class="hamburger-menu" @click="toggleMenu" :class="{ 'active': menuActive }">
        <span></span>
        <span></span>
        <span></span>
      </div>
      
      <!-- Menú navegación -->
      <div class="menu-container" :class="{ 'active': menuActive }">
        <!-- Área de perfil en el menú -->
        <div class="menu-profile" v-if="usuario">
          <img v-if="usuario.ruta_imagen" :src="`${usuario.ruta_imagen}?t=${new Date().getTime()}`" class="menu-profile-img">
          <p class="menu-profile-name">{{ usuario.nombre }}</p>
        </div>
        
        <ul class="menu">
          <li @click="actualizar" v-if="menuActive" ><i class="fas fa-user"></i> Ver Perfil</li>
          <li @click="logout"><i class="fas fa-sign-out-alt"></i> Cerrar Sesión</li>
        </ul>
      </div>
    </nav>
    <hr>
  </header>
  <h1>¡Bienvenido Empleado!</h1>
  <hr id="l2">
  <div id="main-container" v-if="usuario">
  <img v-if="usuario.ruta_imagen" :src="`${usuario.ruta_imagen}?t=${new Date().getTime()}`" id="cara">
   <p id="jefe-name">{{ usuario.nombre }}</p>
   <ActulizacionPerfil v-if="isModalOpen" @close="actualizarClose"/>
 </div>

  <section id="c">
    <div class="nosotros-banner">
      <h2>Configuraciones</h2>
    </div>

    <div class="alert-config-container">
      <i class="fas fa-box-open panel-icon"></i>
       <h1 class="alert-config-title">Panel de Materia Prima</h1>
       <button class="alert-config-button"><a href="/Materia">Ver mas <i class="fas fa-arrow-right" style="margin-left: 12px;"></i></a></button>
    </div>
    <div class="alert-config-container2">
      <i class="fas fa-tags panel-icon"></i>
       <h1 class="alert-config-title">Panel de Productos</h1>
       <button class="alert-config-button"><a href="/Productos">Ver mas <i class="fas fa-arrow-right" style="margin-left: 12px;"></i></a></button>
    </div>

    <div class="alert-config-container4">
      <i class="fas fa-file-invoice-dollar panel-icon"></i>
        <h1 class="alert-config-title">Panel Facturas</h1>
        <button class="alert-config-button"><a href="/Facturas">Ver mas <i class="fas fa-arrow-right" style="margin-left: 12px;"></i></a></button>
    </div>
    <div class="alert-config-container5">
      <i class="fas fa-clipboard-list panel-icon"></i>
        <h1 class="alert-config-title">Panel Pedidos</h1>
        <button class="alert-config-button"><a href="/Pedidos">Ver mas <i class="fas fa-arrow-right" style="margin-left: 12px;"></i></a></button>
    </div>
    <div class="alert-config-container6">
      <i class="fa-solid fa-paste"></i><br>
        <h1 class="alert-config-title">Menu</h1>
        <button class="alert-config-button"><a href="/Menu">Ver mas <i class="fas fa-arrow-right" style="margin-left: 12px;"></i></a></button>
    </div>
  </section>
  <div class="buttom-container">
    <button @click="actualizar" class="buttom-perfil">Ver Perfil</button>
   </div>

  <footer>
      <p>&copy; 2025</p>  
  </footer>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');
header {
  padding: 20px;
}
ul li {
  text-decoration: none;
  border-bottom: 5px solid #A65814;
  transition: border-bottom-color 0.3s ease-in-out;
  border-radius: 5px;
  cursor: pointer;
}
ul li:hover {
  border-bottom-color: rgb(17, 0, 255);
}
nav{
  margin-left: 173px;
}
nav ul {
  font-family: 'Jura', sans-serif;
  list-style: none;
  display: flex;
  justify-content: space-evenly;
  margin-left: 314px;
  margin-top: -73px;
}
hr {
  border-top: 2px solid #D9AB23;
  margin: 20px 0; 
  margin-top: 54px;
  width: 1300px;
  margin-left: 7%;
}
#l2 {
  margin-top: 10px;
  width: 800px;
  margin-left: 22%;
}
h1{
  font-family: 'Jura', sans-serif;
  text-align: center;
  color: #D9AB23;
  margin-top: -23px;
}
 #txt {
  font-family: 'Jura', sans-serif;
  text-align: center;
  color: #ffffff;
}
#cara {
  margin-top: 98px;
  width: 350px;
  height: 350px;
  object-fit: cover;
  margin-left: 100px;
  border-radius: 170px 170px 170px 170px;
}
#jefe-name{
  text-align: left;
  margin-left: 160px;
  margin-top: -414px;
  color: #D9AB23;
  font-size: 34px;
  font-family: 'Jura', sans-serif;
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  position: relative;
}
.hamburger-menu {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 20px;
  cursor: pointer;
  z-index: 20;
}
.hamburger-menu span {
  display: block;
  height: 3px;
  width: 100%;
  background-color: #D9AB23;
  border-radius: 3px;
  transition: all 0.3s ease;
}
.menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  margin-right: 18vh;
}
.menu li {
  margin-left: 20px;
  cursor: pointer;
  transition: color 0.3s ease;
}
.menu li:hover {
  color: #592E25;
}
.menu-profile {
  display: none; /* Se muestra solo en móvil */
}
.menu-more-profile {
  display: none; /* Se muestra solo en móvil */
}
.buttom-perfil{
  margin-top: 100px;
  background-color: #D9AB23;
  margin-top: -45px;
  width: 105px;
  height: 34px;
  border: solid 1px #e6e6e6;
  border-radius: 5px 5px 5px 5px;
  transition: all 0.3s ease-in-out;
}
.buttom-perfil:hover{
  background-color: #D99923;
  transform: scale(1.05) translateY(-5px);
}
.buttom-container{
  width: 100px;
  height: 100px;
  margin-left: 225px;
  margin-top: -145px;
  text-align: center;
}
#c{
  padding: 22px;
  width: 920px;
  height: 54%;
  margin-left: 32%;
  border-radius: 5px;
  border: 1px solid #D9AB23; 
  margin-top: -80px;
}
.nosotros-banner {
  width: 100%;
  background-color: #d9ab23be;
  text-align: center;
  padding: 10px 0;
  border: 1px solid;
  font-family: 'Jura', sans-serif;
  color: white;
}
.nosotros-banner h2{
  color: white;
  margin-left: -10px;
}
.button-container2 {
    display: flex;
    justify-content: space-between;
    width: 80%;
    max-width: 300px;
    margin-left: 558px;
    margin-top: 51px;
}
.button-container2 button {
  font-family: 'Jura', sans-serif;
  background-color: #D99923;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.button-container2 button a {
  text-align: center;
  text-decoration: none;
  color: white;
}
.button-container2 button:hover {
    background-color: #f2d2d0;
    color: black
}
.alert-config-container {
  background-color: #D9AB23; 
  padding: 20px;
  border-radius: 30px 30px 30px 30px; 
  text-align: center; 
  width: 150px; 
  max-height: 170px;
  margin: 0 auto; 
  margin-left: 50px;
  margin-top: 50px;
}
.alert-config-container2 {
  background-color: #D9AB23; 
  padding: 20px;
  border-radius: 30px;
  text-align: center; 
  width: 150px; 
  max-height: 170px;
  margin: 0 auto; 
  margin-left: 264px;
  margin-top: -208px;
}
.alert-config-container3 {
  background-color: #D9AB23; 
  padding: 30px;
  border-radius: 30px; 
  text-align: center;
  width: 150px; 
  height: 130px;
  margin: 0 auto; 
  margin-left: 480px;
  margin-top: -185px;
}
.alert-config-container4 {
  background-color: #D9AB23; 
  padding: 30px;
  border-radius: 30px; 
  text-align: center;
  width: 150px; 
  height: 130px;
  margin: 0 auto; 
  margin-left: 480px;
  margin-top: -185px;
} 
.alert-config-container5 {
  background-color: #D9AB23; 
  padding: 30px;
  border-radius: 30px; 
  text-align: center;
  width: 150px; 
  height: 130px;
  margin: 0 auto; 
  margin-left: 709px;
  margin-top: -188px;
} 
.alert-config-container6 {
  background-color: #D9AB23; 
  padding: 30px;
  border-radius: 30px; 
  text-align: center;
  width: 150px; 
  height: 130px;
  margin: 0 auto; 
  margin-left: 50px;
  margin-top: 48px;
} 
.alert-config-title {
  font-size: 24px;
  color: #fff;
  position: relative;
  display: inline-block;
  margin-bottom: 20px;
  margin-top: 10px;
}
.alert-config-title::after {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: -10px;
  width: 60%; 
  height: 3px; 
  background-color: black; 
}
/* Estilo del botón */
.alert-config-button {
  background-color: #fff;
  color: black;
  padding: 10px 30px;
  border: none;
  border-radius: 20px; 
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.alert-config-button a{
  color: #000000;
  text-decoration: none;
}
.alert-config-button:hover {
    background-color: #e6e6e6;
}
footer {
  padding: 20px;
  text-align: center;
  margin-top: 34px;
  font-family: 'Jura', sans-serif;
}
/* Media query para modo responsivo */
@media (max-width: 767px) {
  .hamburger-menu {
    display: flex;
  }
  .hamburger-menu {
    display: flex;
  }
  
  .menu-container {
    position: fixed;
    top: 0;
    right: -100%;
    width: 70%;
    height: 100vh;
    background-color: rgba(30, 23, 21, 0.927);
    flex-direction: column;
    justify-content: flex-start;
    padding-top: 20px;
    transition: right 0.3s ease;
    z-index: 10;
    overflow-y: auto;
    padding: 10px;
  }
  .menu-container.active {
    right: 0;
  }
  .menu-profile {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid rgba(217, 171, 35, 0.3);
    margin-bottom: 20px;
    width: 100%;
  }
  .menu-profile-img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #D9AB23;
    padding: 5px;
    margin-top: 9vh;
  }
  .menu-profile-name {
    color: #ffffff;
    font-size: 18px;
    margin-top: 10px;
    font-weight: bold;
    font-family: 'Jura', sans-serif;
  }
  .menu {
    flex-direction: column;
    width: 100%;
    padding: 0;
  }
  .menu li {
    margin: 15px 0;
    padding: 0 30px;
    font-size: 18px;
    color: #ffffff;
    align-items: center;
    font-family: 'Jura', sans-serif;
  }
  .menu li i {
    margin-right: 10px;
    width: 20px;
    text-align: center;
  }
  /* Ajustes adicionales para responsivo */
  #main-container {
    flex-direction: column;
    align-items: center;
  }
  .buttom-container {
    display: none; /* Ocultamos el botón de perfil ya que ahora está en el menú */
  }
  /* Animación para el menú hamburguesa cuando está activo */
  .hamburger-menu.active span:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
  }
  .hamburger-menu.active span:nth-child(2) {
    opacity: 0;
  }
  .hamburger-menu.active span:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
  }
  .buttom-container {
    display: none; /* Ocultamos el botón de perfil ya que ahora está en el menú */
  }
  .logo{
    margin-left: -53%;
    margin-top: 15%;
  }
  hr {
    margin-left: 4%;
    width: 300px;
    margin-top: 1rem;
  }
  #l2 {
    margin-top: 5px;
    margin-left: 23%;
    width: 200px;
  }

  #c{
    margin-left: 10px;
    width: 80%;
    height: 100%;
    margin-top: 2rem;
    padding: auto;
  }

  #main-container{
    display: none;
  }

  /* Ajustes para los contenedores */
  .alert-config-container,
  .alert-config-container2,
  .alert-config-container3,
  .alert-config-container4,
  .alert-config-container5,
  .alert-config-container6 {
    width: 55%;
    margin: 10px auto;
  }
  footer {
  padding: 20px;
  text-align: center;
  margin-top: 4px;
  font-family: 'Jura', sans-serif;
  }
}
</style>