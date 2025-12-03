<template>
  <div class="contenedor">
    <img src="https://i.postimg.cc/QMwjX2vk/Whats-App-Image-2024-11-23-at-10-53-04-PM.jpg" class="imagen" alt="imagen 1">
  </div>
</template>

<style>
.imagen {
  display: flex;
  height: 210px;
  width: 240px; 
  border-radius: 250px;
}
.contenedor{
  display: flex;
}

@media (max-width: 767px) {
  .imagen {
    width: 150px !important;
    height: 130px !important;
  }
}

</style>