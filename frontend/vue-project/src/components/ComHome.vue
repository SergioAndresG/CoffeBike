<script setup lang="ts">
import ComNosImg from './icons/IMGENES/ComNosImg.vue';
import ComImagen from './icons/IMGENES/ComImagen.vue';
import ComInicioImg from './icons/IMGENES/ComInicioImg.vue';
</script>

<template>
    <header>
    <nav>
      <ComImagen/>
      <div class="menu-hamburguesa" id="menu-hamburguesa">
        <ul class="menu">
          <li><router-link to="/Menu">Menu</router-link></li>
          <li><router-link to="/Sesion">Iniciar Sesión</router-link></li>
        </ul>
      </div>
    </nav>
  </header>
  <hr>
  <hr id="l2">

  <h1 id="quienes">QUIENES SOMOS</h1>

  <p id="text">
    Somos coffee bike nos apasiona brindar una experiencia única en cada taza. Desde el primer sorbo hasta el último, queremos que disfrutes del auténtico sabor del café recién molido, cuidadosamente seleccionado de los mejores cultivos. Nuestro espacio ha sido diseñado para que te sientas como en casa, ya sea que vengas a trabajar, relajarte o compartir momentos especiales.
  </p>

  <ComInicioImg/>
    <div class="card">
        <p class="small-desc">
          Facil de usar, potente de utilizar
        </p>
        <hr id="car">
    </div>
    <div class="card2">
        <p class="small-desc">
          Facil de usar, potente de utilizar
        </p>
        <hr id="car">
    </div>
    <div class="card3">
        <p class="small-desc">
          Facil de usar, potente de utilizar
        </p>
        <hr id="car">
    </div>

  <div class="nosotros-banner">
      <h2>Nosotros</h2>
  </div>


  <div class="contenedor5">
      <p id="text4">En Coffee Bike nos apasiona brindar una experiencia única en cada taza. Desde el primer sorbo hasta el último, queremos que disfrutes del auténtico sabor del café recién molido, cuidadosamente seleccionado de los mejores cultivos. Nuestro espacio ha sido diseñado para que te sientas como en casa, ya sea que vengas a trabajar, relajarte o compartir momentos especiales.
        Además del café, ofrecemos una amplia variedad de bebidas artesanales, postres irresistibles y opciones ligeras para cualquier momento del día. Todo preparado con ingredientes frescos y mucho cariño.</p>
    </div>


  <div id="container-text-2">
    <h1 id="nuestro">NUESTRA HISTORIA</h1>
    <p id="Coffe-text">Coffee Bike nació del sueño de compartir momentos únicos a través del café. Todo comenzó con una pequeña máquina de espresso y una gran pasión por descubrir los mejores granos del mundo. Inspirados por el aroma y la magia que cada taza puede ofrecer, decidimos crear un espacio donde el café no solo se disfrute, sino que también se sienta.  Gracias a nuestros clientes, cada taza que servimos es un testimonio de amistad, tradición y amor por el café. ¡Esta historia apenas comienza, y queremos que seas parte de ella! </p>
  </div>


  <ComNosImg/>

  <div class="card-flip">
    <div class="card-item">
      <div class="card-front" :style="{ backgroundImage: 'url(https://i.postimg.cc/k5Lnzfkd/Whats-App-Image-2024-11-22-at-5-15-44-PM.jpg)' }">
      </div>
      <div class="card-back">
        <p class="small-desc">
          Tomar riesgos es la piedra angular de los imperios
        </p>
      </div>
    </div>
    
    <div class="card-item">
      <div class="card-front" :style="{ backgroundImage: 'url(https://i.postimg.cc/k5Lnzfkd/Whats-App-Image-2024-11-22-at-5-15-44-PM.jpg)' }">
        <!-- Imagen de fondo -->
      </div>
      <div class="card-back">
        <p class="small-desc">
          ¡Explora nuevas posibilidades con facilidad!
        </p>
      </div>
    </div>
    
    <div class="card-item">
      <div class="card-front" :style="{ backgroundImage: 'url(https://i.postimg.cc/k5Lnzfkd/Whats-App-Image-2024-11-22-at-5-15-44-PM.jpg)' }">
        <!-- Imagen de fondo -->
      </div>
      <div class="card-back">
        <p class="small-desc">
          ¡Innovación al alcance de tu mano!
        </p>
      </div>
    </div>
  </div>

  
    <footer>
      <p>&copy; 2024 </p>
      
       
      <ul class="wrapper">
    <a href="https://www.instagram.com/de_lonuestro?igsh=MXU3NTQ4cGY4cXI2ZA==" target="_blank" rel="noopener noreferrer">

  <li class="icon instagram">
      <span class="tooltip">Instagram</span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        height="1.2em"
        fill="currentColor"
        class="bi bi-instagram"
        viewBox="0 0 16 16"
      >
        <path
          d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"
        ></path>
      </svg>
  </li>
</a>

</ul>  
  
  </footer>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');
body {
    font-family: 'Jura', sans-serif;
    font-weight: normal;
  background-color: black; /* Fondo negro */

}
  
  header {
    padding: 20px;
    background-color: #000000;
  }
  

  
  ul li {
    text-decoration: none;
    border-bottom: 5px solid #A65814;
    transition: border-bottom-color 0.3s ease-in-out;
    border-radius: 5px;
  }
  
  ul li:hover {
    border-bottom-color: rgb(17, 0, 255);
  }

  nav{
    margin-left: 173px;
  }
  
  nav ul {
    list-style: none;
    display: flex;
    justify-content: space-evenly;
    margin-left: 314px;
    margin-top: -73px;
  }
  
  nav li a {
    font-family: 'Jura', sans-serif;

    text-decoration: none;
    color: white;
    padding: 10px;
  }
  
  #res:hover {
    background-color: #ff9178;
    color: aliceblue;
  }
  
  #res{
    transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out;
    background-color: #e03743;
    text-decoration: none;
    border-bottom: 0px;
    width: 150px;
    text-align: center;
    font-size: 18px;
    padding: 4px;
    border-radius: 15px;
  }
  
  hr {
    border-top: 2px solid #D9AB23; /* Ajusta el grosor y color según tus necesidades */
    margin: 20px 0; /* Ajusta el margen superior e inferior */
    margin-top: 64px;
    width: 1300px;
    margin-left: 7%;
  }


  #hr1 {
    border-top: 2px solid #D9AB23; /* Ajusta el grosor y color según tus necesidades */
    margin: 20px 0; /* Ajusta el margen superior e inferior */
    margin-top: 6px;
    width: 1300px;
    margin-left: 7%;
  }
  #l2 {
    margin-top: 10px;
    width: 800px;
    margin-left: 22%;

  }

  #quienes{
    font-family: 'Jura', sans-serif;
    font-size: 44px;
    color: #D9AB23;
    margin-left: 950px;
    margin-top: 80px;
  }

  #text{
    height: 200px;
    width: 600px;
    font-family: 'Jura', sans-serif;
    margin-left: 850px;
    font-size: 23px;
    margin-top: -20px;
  }

  .card-title {
    color: #262626;
    font-size: 1.5em;
    line-height: normal;
    font-weight: 700;
    margin-bottom: 0.5em;
  }
  .small-desc {
    font-size: 1em;
    font-weight: 400;
    line-height: 1.5em;
    color: #452c2c;
  }
  .card {
    font-family: 'Jura', sans-serif;
    width: 180px;
    max-height: 320px;
    border-radius: 10px;
    padding: 2em 1.2em;
    margin: 12px;
    text-decoration: none;
    overflow: hidden;
    background: linear-gradient(to bottom, #D9AB23, #D9AB23);
    margin-top: -213px;
    margin-left: 780px;
  }
  .card2 {
    font-family: 'Jura', sans-serif;
    width: 180px;
    max-height: 320px;
    border-radius: 10px;
    padding: 2em 1.2em;
    margin: 12px;
    text-decoration: none;
    overflow: hidden;
    background: linear-gradient(to bottom, #A65814, #A65814);
    margin-top: -178px;
    margin-left: 1030px;
  }
  .card3 {
    width: 180px;
    font-family: 'Jura', sans-serif;
    max-height: 320px;
    border-radius: 10px;
    padding: 2em 1.2em;
    margin: 12px;
    text-decoration: none;
    overflow: hidden;
    background: linear-gradient(to bottom, #D9AB23, #D9AB23);
    margin-top: -178px;
    margin-left: 1280px;
  }

  #car{
    border-top: 2px solid #ffffff;
    width: 175px;
    margin-top: 16px;
    margin-left: 1px;
  }

  .card:hover .small-desc {
    transition: all 0.5s ease-out;
    color: rgba(255, 255, 255, 0.8);
  }
  .card:hover .card-title {
    transition: all 0.5s ease-out;
    color: #ffffff;
  }

  .card2:hover .small-desc {
    transition: all 0.5s ease-out;
    color: rgba(255, 255, 255, 0.8);
  }
  .card2:hover .card-title {
    transition: all 0.5s ease-out;
    color: #ffffff;
  }

  .card3:hover .small-desc {
    transition: all 0.5s ease-out;
    color: rgba(255, 255, 255, 0.8);
  }
  .card3:hover .card-title {
    transition: all 0.5s ease-out;
    color: #ffffff;
  }

  



  #text4{
    font-family: 'Jura', sans-serif;
    font-size: 23px;
    margin-top: 50px;
    width: 990px;

  }

  .nosotros-banner {
  width: 100%;
  background-color: #d9ab23be;
  text-align: center;
  padding: 10px 0;
  border: 1px solid;
  margin-top: 65px;
}

.nosotros-banner h2 {
  font-family: 'Jura', sans-serif;
  margin: 0;
  font-size: 24px;
  color: #ffffff;
}

.contenedor5 {
  height: 100vh; /* Ocupa toda la ventana */
  background-image: url("https://i.postimg.cc/k5Lnzfkd/Whats-App-Image-2024-11-22-at-5-15-44-PM.jpg");
  background-size: cover; /* La imagen cubre todo el contenedor */
  background-position: center; /* Centra la imagen */
  background-attachment: fixed; /* Imagen fija */
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  text-align: center;
  height: 380px;
}


/* Estilo para el resto del contenido */
#container-text,
#container-text-2 {
  padding: 2rem;
  line-height: 1.6;
}


  #container-text-2{
    width: 700px;
    margin-left: 123px;
    text-align: center;
  }

  #nuestro{
    color: #D9AB23;
    font-family: 'Jura', sans-serif;
    margin-left: 40px;
  }

  #Coffe-text{
    font-family: 'Jura', sans-serif;
    font-size: 20px;
    margin-top: 20px;
    margin-left: 20px;
  }

  .card-flip {
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.card-item {
  margin-left: -30px;
  width: 300px;
  height: 300px;
  perspective: 1000px; /* Esto da el efecto de profundidad al voltear */
}

.card-front, .card-back {
  width: 100%;
  height: 100%;
  backface-visibility: hidden; /* Esto asegura que la parte de atrás no sea visible cuando esté volteada */
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 10px;
  border-radius: 10px;
  transition: transform 0.6s; /* Añade una transición suave al voltear */
}

.card-front {
  background-size: cover;
  background-position: center;
}

.card-back {
  background-color: #fefdae;
  font-family: 'Jura', sans-serif;
  font-size: 30px;
  transform: rotateY(180deg); /* Voltea la parte de atrás */
}

.card-item:hover .card-front {
  transform: rotateY(180deg); /* Voltea la parte delantera cuando el mouse está sobre la carta */
}

.card-item:hover .card-back {
  transform: rotateY(0); /* Muestra la parte trasera cuando el mouse está sobre la carta */
}

  
  footer {
      padding: 20px;
      text-align: center;
      margin-top: 94px;
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
  
  /* From Uiverse.io by david-mohseni */ 
  .wrapper {
    display: inline-flex;
    list-style: none;
    height: 120px;
    width: 100%;
    padding-top: 40px;
    font-family: "Poppins", sans-serif;
    justify-content: center;
    margin-left: -32px;
  }
  
  .wrapper .icon {
    position: relative;
    background: #000000;
    border-radius: 50%;
    margin: 10px;
    width: 50px;
    height: 50px;
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }
  
  .wrapper .tooltip {
    position: absolute;
    top: 0;
    font-size: 14px;
    background: #fff;
    color: #fff;
    padding: 5px 8px;
    border-radius: 5px;
    box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
    opacity: 0;
    pointer-events: none;
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }
  
  .wrapper .tooltip::before {
    position: absolute;
    content: "";
    height: 8px;
    width: 8px;
    background: #fff;
    bottom: -3px;
    left: 50%;
    transform: translate(-50%) rotate(45deg);
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }
  
  .wrapper .icon:hover .tooltip {
    top: -45px;
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
  }
  
  .wrapper .icon:hover span,
  .wrapper .icon:hover .tooltip {
    text-shadow: 0px -1px 0px rgba(0, 0, 0, 0.1);
  }
  
  .wrapper .facebook:hover,
  .wrapper .facebook:hover .tooltip,
  .wrapper .facebook:hover .tooltip::before {
    background: #1877f2;
    color: #fff;
  }
  
  .wrapper .twitter:hover,
  .wrapper .twitter:hover .tooltip,
  .wrapper .twitter:hover .tooltip::before {
    background: #000000;
    color: #fff;
  }
  
  .wrapper .instagram:hover,
  .wrapper .instagram:hover .tooltip,
  .wrapper .instagram:hover .tooltip::before {
    background: #e4405f;
    color: #fff;
  }

</style>