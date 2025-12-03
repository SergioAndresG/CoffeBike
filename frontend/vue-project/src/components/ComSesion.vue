<script setup lang="ts">
import ComImagen from './icons/IMGENES/ComImagen.vue';
import { ref } from "vue";
import axios from "axios";
import { DotLottieVue } from '@lottiefiles/dotlottie-vue';
import { useRouter } from "vue-router";
import { getCurrentUser } from '@/servicies/auths';

const nombre = ref("");
const contraseña = ref("");
const errorMessage = ref(null);
const successMessage = ref(null);
const router = useRouter();

axios.interceptors.request.use(config => {
  const token = localStorage.getItem("jwtToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config;
})

const validarUsuario = async () => {
  try {
    // Llamada al endpoint de login
    const respuesta = await axios.post("https://coffebikefastapi-production.up.railway.app/login", {
        nombre: nombre.value,
        contraseña: contraseña.value,
        },
        {
        headers: {
          "Content-Type": "application/json",  
        },
    }
    
  );


    // Almacena el token 
    localStorage.setItem("jwtToken", respuesta.data.access_token);

    const userData = await getCurrentUser();
    console.log("Datos enviados", userData);


    localStorage.setItem("userData", JSON.stringify(userData));

    //Redireccion en base al rol
    switch (userData.rol) {
      case "JEFE":
        router.push({
          name: "Jefe",
          state: {userData}
        })
        break;
      case "ADMINISTRADOR":
        router.push({
          name: "Admi",
          state: {userData}
        })
         break;
      case "EMPLEADO":
        router.push({
          name: "Empleado",
          state: {userData}
        })
      break;
      default:
        break;
    }
    
    // Si la respuesta es exitosa, muestra el mensaje de bienvenida
    successMessage.value = respuesta.data.mensaje;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 
                        "Error de conexión";
    localStorage.removeItem("jwtToken");
  }
};
</script>


<template>

    <header>
        <nav>
        <ComImagen class="logo"/>
        <div class="menu-hamburguesa" id="menu-hamburguesa">
            <ul class="menu">
            </ul>
        </div>
        </nav>
    </header>
  <hr>
  <hr id="l2">
  <div class="login-container">
  
  <h2>Iniciar Sesión</h2> 
    <form @submit.prevent="validarUsuario">
      <label for="name">Nombre:</label>
      <input
        type="text"
        v-model.trim="nombre"
        id="nombre"
        name="nombre"
        autocomplete="off"
        placeholder="Ingrese su nombre"
        required
      />
      <label for="password">Contraseña:</label>
      <input
        type="password"
        v-model.trim="contraseña"
        id="contraseña"
        name="contraseña"
        placeholder="Ingrese su contraseña"
        required
      />

      <router-link to="/ResetPass" class="forgot-password">¿Olvidaste la contraseña?</router-link>

      <button type="submit" class="login-btn">Iniciar Sesión</button>
    </form>

    <!-- Mensaje de error si falla el inicio de sesión -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <!-- Mensaje de éxito si el login es correcto -->
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
  </div>
  <DotLottieVue class="animation" style="height: 600px; width: 600px; margin-left: 55%; margin-top: -500px; z-index: -10; " autoplay loop src="https://lottie.host/828cc208-a80f-49c5-b398-365742b9d448/1yNKlcoM18.lottie" />


  <footer>
      <p>&copy; 2025 </p>
  </footer>

</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');

body {
  font-family: 'Jura', sans-serif;
  font-weight: normal;
  color: black; 
}
.logo{
  margin-left: 650px;
}
hr {
  border-top: 2px solid #D9AB23; 
  margin: 20px 0;
  margin-top: -14px;
  width: 1300px;
  margin-left: 7%;
}
#l2 {
  margin-top:5px;
  max-width: 800px;
  margin-left: 22%;
}
.login-container {
  border-radius: 10px;
  padding: 20px 30px;
  text-align: center;
  max-width: 500px;
  min-width: 100px;
  height: 380px;
  background-color: hsla(66, 20%, 68%, 0.4);
  margin-left: 210px;
  margin-top: 80px;
}
h2 {
  color: #D9AB23;
  margin-bottom: 10px;
  font-size: 34px;
  font-family: 'Jura', sans-serif;
}
.register-btn {
  background-color: #8C3420;
  color: #F2F2F2;
  padding: 5px 10px;
  border-radius: 20px;
  text-decoration: none;
  font-size: 18px;
}
form {
  margin-top: 20px;
}
label {
  display: block;
  margin-bottom: 5px;
  color: #ffffff;
  font-family: 'Jura', sans-serif;
  padding: 5px;
  font-weight: bold;
}
input[type="text"],
input[type="password"] {
  width: 70%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #a64e4e;
  border-radius: 12px;
  background-color: #D9AB23;
  font-family: 'Jura', sans-serif;
  transition: all 0.3s ease-in-out;
}
input:focus{
  transform: scale(1.02);
  border-color: #000000;
}
.forgot-password {
  display: block;
  margin-bottom: 20px;
  color: #D9AB23;
  text-decoration: none;
  font-size: 15px;
  font-family: 'Jura', sans-serif;
}
.login-btn {
  transition: background-color, 0.3s ease-in-out;
  background-color: #D9AB23;
  color: #ffffff;
  padding: 10px;
  width: 100%;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 200px;
  height: 50px;
  font-size: 20px;
  font-family: 'Jura', sans-serif;
}
.login-btn:hover {
  background-color: #592E25;
}
.social-login {
  margin-top: 20px;
}
.social-login p {
  margin-bottom: 10px;
  color: #592E25;
}
.social-icons img {
  width: 40px;
  margin: 0 10px;
  cursor: pointer;
}
#hl{
  margin-top: -3px;
}
#imagen{
  margin-left: 954px;
  width: 390px;
  height: 390px;
  margin-top: -435px;
  border-radius: 200px;
}
p{
  font-family: 'Jura', sans-serif;
}
footer {
  padding: 20px;
  text-align: center;
  margin-top: 34px;
}
footer a {
  text-decoration: none;
  color: #333;
}

@media (max-width: 767px) {
  body{
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      width: 100%;
      height: 100%;
  }
  .logo{
    margin-left: 50px;
    margin-top: 42px;
  }
  .login-container {
    margin-left: 15px;
    margin-right: 15px;
    margin-top: 42px;
  }
  hr {
    margin-left: 9%;
    width: 300px;
  }
  #l2 {
    margin-top: 5px;
    margin-left: 23%;
    width: 200px;
  }
  .animation{
    opacity: 0.0;
    height: 300px;
    width: 300px; 
    position: absolute; 
    right: 10%; 
    top: 150px; 
    z-index: -10;
  }
  footer {
    text-align: center;
    margin-top: 30px;
  }
  footer a {
    text-decoration: none;
    color: #333;
  }
}
</style>