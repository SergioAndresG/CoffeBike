<script setup lang="ts">
import { ref } from "vue";
import { defineEmits } from "vue";
import axios from "axios";
import Swal from "sweetalert2";  // Asegúrate de importar SweetAlert2

const emit = defineEmits(["close", "refresh"]); // Emitir los eventos 'close' y 'refresh'

// Datos del formulario
const formData = ref({
  nombreUsuarioAEliminar: "",
  contraseñaJefe: "",
  confirmarContraseña: "",
});

const handleSubmit = async () => {
  // Verificar si las contraseñas coinciden
  if (formData.value.contraseñaJefe !== formData.value.confirmarContraseña) {
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Las contraseñas no coinciden",
    });
    return;
  }
  try {
    // Construir la URL con los parámetros de consulta
    const response = await axios.delete("https://coffebikefastapi-production.up.railway.app/usuarios/eliminar", {
      params: {
        nombre_usuario_a_eliminar: formData.value.nombreUsuarioAEliminar,
        contraseña_proporcionada: formData.value.contraseñaJefe,
      },
    });

    // Si la eliminación fue exitosa, mostramos el mensaje de éxito
    Swal.fire({
      icon: "success",
      title: "Usuario eliminado",
      text: "El usuario ha sido eliminado correctamente.",
    });
    console.log("Usuario eliminado:", response.data);
    // Cerrar el modal y emitir evento para refrescar la lista
    closeModal();
    emit("refresh");
  } catch (error) {
    // Si ocurre un error, mostramos el mensaje de error
    Swal.fire({
      icon: "error",
      title: "Error",
      text: error.response?.data?.detail || "Hubo un error al eliminar el usuario.",
    });
    console.error("Error al eliminar usuario:", error);
  }
};

// Función para cerrar el modal
const closeModal = () => {
  emit("close");  // Emitir el evento para cerrar el modal
};
</script>


<template>
    <div class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h1>Eliminar Usuario</h1>
        <div class="form-container">
          <form @submit.prevent="handleSubmit">
            <label for="nombre">Nombre:</label>
            <input
              type="text"
              id="nombre"
              v-model="formData.nombreUsuarioAEliminar"
              placeholder="Ingrese el nombre del usuario a eliminar"
            />
            <label for="contraseña">Contraseña del Jefe:</label>
            <input
              type="password"
              id="contraseña"
              v-model="formData.contraseñaJefe"
              placeholder="Ingrese la contraseña del jefe"
            />
            <label for="confirmarContraseña">Confirmar Contraseña:</label>
            <input
              type="password"
              id="confirmarContraseña"
              v-model="formData.confirmarContraseña"
              placeholder="Confirme la contraseña"
            />
            <button type="submit">Eliminar</button>
          </form>
        </div>
      </div>
      <button @click="closeModal" class="close-btn">X</button>
    </div>
  </template>
  

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
  font-size: 14px;
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
  transition: 0.3s ease;
  font-family: 'Jura', sans-serif;
  width: 150px;
  margin-left: 180px;

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

  background-color: black;
  margin-top: -33px;
  padding: 20px;
  width: 80%;
  height: 450px;
  max-width: 600px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid;
  margin-left: 230px;
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
  margin-left: 120px;
}

.close-btn:hover {
  background-color: darkred;
}


</style>