<script setup lang="ts">
import SnowFall from './components/SnowFall.vue';

</script>

<template>
  <div class="animation">
    <SnowFall />
  </div>
  
  <router-view></router-view>

</template>
<style>
body, router-view {
  margin: 0;
  padding: 0;
  background-color: black;
  height: 100%; /* Aseguramos que ocupe toda la pantalla */
  color: white; /* Texto visible */
}

/* Aseguramos que el componente de nieve esté en el fondo */
.container {
  position: fixed; /* Fija la animación en el fondo */
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh; /* Altura completa de la pantalla */
  z-index: -1; /* Envía la animación detrás del contenido principal */
  pointer-events: none; /* Permite la interacción con los elementos de encima */
}

#app {
  position: relative; /* Para que su contenido esté encima de la animación */
  height: 100%;
}

</style>
