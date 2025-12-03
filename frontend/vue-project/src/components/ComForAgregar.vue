<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

// Definir interfaz para el formulario
interface FormData {
  nombre: string;
  rol: string;
  subrol: string | null; // Subrol puede ser null si no se define
  correo: string;
  contraseña: string;
  confirmarContraseña: string;
  documento: number | null; // Documento puede ser null inicialmente
  telefono: number;
  file: File | null; // Archivo opcional
}

// Estado inicial del formulario
const formData = ref<FormData>({
  nombre: "",
  rol: "",
  telefono: null,
  subrol: null,
  correo: "",
  contraseña: "",
  confirmarContraseña: "",
  documento: null,
  file: null
});

// Emitir el evento 'close' para cerrar el modal
const emit = defineEmits<{
  (e: "close"): void;
}>();

// Función para manejar el cambio del archivo
const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    formData.value.file = target.files[0]; // Guardar el archivo seleccionado
  }
};

const handleSubmit = async (): Promise<void> => {
    // Validar que las contraseñas coincidan
    if (formData.value.contraseña !== formData.value.confirmarContraseña) {
        alert("Las contraseñas no coinciden");
        return;
    }

    // Validar campos requeridos
    if (!formData.value.nombre || !formData.value.correo || !formData.value.documento) {
        alert("Por favor completa todos los campos requeridos.");
        return;
    }

    try {
        const data = new FormData();

        // Agregar datos del usuario como JSON a FormData
        data.append("nombre", formData.value.nombre);
        data.append("documento", formData.value.documento!.toString());
        data.append("telefono", formData.value.telefono!.toString());
        data.append("rol", formData.value.rol);
        data.append("subrol", formData.value.subrol || "");
        data.append("correo", formData.value.correo);
        data.append("contraseña", formData.value.contraseña);

        // Agregar el archivo de imagen si existe
        if (formData.value.file) {
            data.append("file", formData.value.file);
        }

        // Realizar la solicitud POST al backend
        const response = await axios.post("https://coffebikefastapi-production.up.railway.app/usuarios", data, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        });
        console.log("Usuario agregado con éxito:", response.data);
        closeModal();
    } catch (error) {
        console.error("Error al agregar el usuario:", error);
        if (axios.isAxiosError(error)) {
            alert("Error en la solicitud al servidor. " + (error.response?.data.message || "Inténtalo nuevamente."));
        } else {
            alert("Hubo un error inesperado.");
        }
    }
};

// Función para resetear el formulario
const resetForm = (): void => {
  formData.value = {
    nombre: "",
    rol: "",
    subrol: null,
    telefono: null,
    correo: "",
    contraseña: "",
    confirmarContraseña: "",
    documento: null,
    file: null
  };
};

// Función para cerrar el modal
const closeModal = (): void => {
  emit("close"); // Emitir el evento para cerrar el modal
};
</script>

<template>
<div class="modal-overlay" @click="closeModal">

  <div class="modal-content" @click.stop>
    <button @click="closeModal" class="close-btn">X</button>
    <h1>Agregar Trabajador</h1>
    <div class="form-container">
      <form @submit.prevent="handleSubmit">
        <!-- Campo para Nombre -->
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" v-model="formData.nombre" placeholder="Ingrese su nombre" required />

        <!-- Campo para Documento -->
        <label for="documento">Documento:</label>
        <input type="number" id="documento" v-model.number="formData.documento" placeholder="Ingrese su documento" required />

        <!-- Campo para Telefono -->
        <label for="telefono">Telefono:</label>
        <input type="number" id="telefono" v-model.number="formData.telefono" placeholder="Ingrese su telefono" required />

        <!-- Campo para Correo -->
        <label for="correo">Correo:</label>
        <input type="email" id="correo" v-model="formData.correo" placeholder="Ingrese su correo" required />

        <!-- Campo para Contraseña -->
        <label for="contraseña">Contraseña:</label>
        <input type="password" id="contraseña" v-model="formData.contraseña" placeholder="Ingrese su contraseña" required />

        <!-- Campo para Confirmar Contraseña -->
        <label for="confirmarContraseña">Confirmar Contraseña:</label>
        <input type="password" id="confirmarContraseña" v-model="formData.confirmarContraseña" placeholder="Confirme su contraseña" required />

        <!-- Campo para Rol -->
        <label for="rol">Rol:</label>
        <select id="rol" v-model="formData.rol" required>
          <option disabled value="">Selecciona Rol</option>
          <option value="EMPLEADO">Empleado</option>
        </select>

        <!-- Campo para SubRol -->
        <label for="subrol">Sub-Rol:</label>
        <select id="subrol" v-model="formData.subrol">
          <option disabled value="">Seleccione un sub-rol (opcional)</option>
          <option value="COSINERO">Cocinero</option>
          <option value="MESERO">Mesero</option>
          <option value="">Ninguno</option>
        </select>

        <!-- Campo para Imagen -->
        <label for="ruta_imagen">Imagen:</label>
        <input type="file" id="ruta_imagen" accept="image/*" @change="onFileChange" />

        <button type="submit">Agregar</button>
      </form>
    </div>
  </div>
</div>
  </template>

<style scoped>
h1{
  font-family: 'Jura', sans-serif;
  font-size: 24px;
  text-align: center;
  color: #ffd700;
  margin-top: -13px;

}
/* Estilo del formulario */
.form-container {
  padding: 45px;
  margin: 0 auto;
  border-radius: 8px;
  margin-top: -2px;
  width: 600px;
}
.form-container select{
  font-family: 'Jura', sans-serif;
  margin-bottom: 15px;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #cf9b00; 
  color: #000;
  font-size: 14px;
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
  background-color: #cf9b00; 
  color: #000;
  font-size: 14px;
}

input::placeholder {
  color: #000;
  opacity: 0.8;
}

button {
  background-color: #ffecb3; 
  color: #000;
  padding: 10px 15px;
  font-size: 14px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: 0.3s ease;
  font-family: 'Jura', sans-serif;
  width: 150px;
  margin-left: 220px;
}
.select{
    font-family: 'Jura', sans-serif;
    margin-bottom: 15px;
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #cf9b00; /* Color amarillo similar */
    color: #000;
    font-size: 14px;
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
  overflow-y: auto;
  z-index: 9999;
}
.modal-content {
  background-color: black;
  margin-top: 210px;
  padding: 20px;
  width: 80%;
  height: 800px;
  max-width: 700px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid;
}
.close-btn {
  background-color: red;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 4px;
  width: 50px;
  margin-left: 640px;
}
.close-btn:hover {
  background-color: darkred;
}
</style>