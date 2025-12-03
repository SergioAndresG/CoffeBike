<template>
    <!-- Mostrar modal solo si isModalOpen es verdadero -->
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
      
        <h1>Consultar Empleado</h1>
        <div class="form-container">
          <form @submit.prevent="handleSubmit">
            <label for="idEmpleado">ID del Empleado:</label>
            <input
              type="text"
              id="idEmpleado"
              v-model="idEmpleado"
              placeholder="Ingrese el ID del Empleado"
            />
            <button type="submit">Consultar</button>
          </form>
          <!-- Mostrar información del empleado si existe -->
        <div v-if="empleado" id="container" @click="closeModal">
          <h3>Información del Empleado</h3>
          <p><strong>Nombre:</strong> {{ empleado.nombre }}</p>
          <p><strong>Correo:</strong> {{ empleado.correo }}</p>
          <p><strong>Rol:</strong> {{ empleado.rol }}</p>
        </div>
        </div>
      </div>
       <!-- Botón de cierre -->
       <button @click="closeModal" class="close-btn">X</button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import axios from 'axios';
  
  // Propiedades reactivas
  const idEmpleado = ref(null);
  const empleado = ref(null); // Almacena los datos del empleado
  
  // Función para consultar el empleado por ID
  const handleSubmit = async () => {
    if (!idEmpleado.value) {
      alert("Por favor, ingresa un ID válido.");
      return;
    }
  
    try {
      const respuesta = await axios.get(`http://127.0.0.1:8000/usuarios/${idEmpleado.value}`); // Endpoint ajustado
      empleado.value = respuesta.data; // Asigna los datos del empleado
    } catch (error) {
      console.error("Error al consultar empleado:", error);
      alert("Empleado no encontrado o error en la consulta.");
      empleado.value = null; // Limpia los datos si hay error
    }
  };
  


  
import { defineEmits } from 'vue';

const emit = defineEmits(['close']); // Emitir el evento 'close'

const closeModal = () => {
  emit('close');  // Emitir el evento para cerrar el modal
};
  </script>
  
  <style scoped>
  h1{
    font-family: 'Jura', sans-serif;
    font-size: 24px;
    text-align: center;
    color: #ffd700;

  }
  /* Estilo del formulario */
.form-container {
  background-color: #00000077; /* Fondo negro */
  padding: 15px;
  width: 500px;
  margin: 0 auto;
  border-radius: 8px;
  margin-top: -2px;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  color: #fff; /* Texto blanco */
  font-size: 10px;
  margin-bottom: 5px;
  font-family: 'Jura', sans-serif;
    text-align: center;
}

input {
    font-family: 'Jura', sans-serif;
  margin-bottom: 15px;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #cf9b00; /* Color amarillo similar */
  color: #000;
  font-size: 14px;
}

input::placeholder {
  color: #000;
  opacity: 0.8;
}

button {
  background-color: #ffecb3; /* Botón amarillo claro */
  color: #000;
  padding: 10px 15px;
  font-size: 14px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  width: 150px;
  margin-left: 180px;
  transition: 0.3s ease;
  font-family: 'Jura', sans-serif;

}

button:hover {
  background-color: #ffd700;
}


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  position: relative;
  background-color: rgb(0, 0, 0);
  margin-top: -33px;
  padding: 20px;
  width: 80%;
  height: 410px;
  max-width: flex;
  max-width: 700px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid;
}

.close-icon:hover {
  color: red;
}

.close-btn {
  background-color: transparent;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 4px;
  margin-top: -520px;
  margin-right:-290px ;
  width: 100px;
}

.close-btn:hover {
  background-color: darkred;
}

#container{
    text-align: center;
    font-family: 'Jura', sans-serif;
}
  </style>
  
  
  