<template>
    <div class="contenedor">
      <img src="https://i.postimg.cc/7hdqtfMv/Whats-App-Image-2024-11-22-at-4-54-18-PM.jpg" class="imagen" alt="imagen 1">
    </div>
</template>
  
  <style scoped>
  .imagen {
    display: flex;
    height: 590px;
    width: 620px; 
    margin-top: -283px;
    margin-left: 130px;
    border-radius: 300px 0px 0px 0px;
  }
  .contenedor{
    display: flex;
  }
  @media screen and (min-width: 280px) and (max-width: 490px){
    .imagen {
    display: flex;
    height: 150px;
    width: 280px; 
    border-radius: 300px 0px 0px 0px;
    z-index: -1;
    margin-top: 10px;
    margin-left: -0px;
  }
  .contenedor{
    display: flex;
  }
  }
  </style>