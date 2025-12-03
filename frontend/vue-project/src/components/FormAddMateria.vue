<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import Swal from "sweetalert2"; 

const unidades = ref([]);


const formData = ref({
  nombre: "",
  cantidad: null,
  stock_minimo: null,
  fecha_ingreso: "",
  vida_util_dias: null,
  unidad_id: "",
  precio_unitario: null,
  file: null as File | null,
  
});

// Método para cargar las unidades de medida
const cargarUnidadMedida = async () => {
  try {
    const respuesta = await axios.get("http://127.0.0.1:8000/materia/unidades-medida");
    unidades.value = respuesta.data;
  } catch (error) {
    console.error("Error al cargar las unidades de medida", error);
  }
};

// Cargar unidades cuando el componente se monta
onMounted(() => {
  cargarUnidadMedida();
});

console.log("Unidades cargadas:", unidades.value);

const handleImageUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    formData.value.file = file;
  }
};



// Método para manejar el envío del formulario
const handleSubmit = async () => {
  try {
    console.log("nombre:", formData.value.nombre);
    console.log("cantidad:", formData.value.cantidad);
    console.log("stock_minimo:", formData.value.stock_minimo);
    console.log("fecha_ingreso:", formData.value.fecha_ingreso);
    console.log("vida_util_dias:", formData.value.vida_util_dias);
    console.log("unidad_id:", formData.value.unidad_id);
    console.log("precio_unitario:", formData.value.precio_unitario);
    if (
      !formData.value.nombre ||
      formData.value.cantidad === null ||
      formData.value.stock_minimo === null ||
      !formData.value.fecha_ingreso ||
      formData.value.vida_util_dias === null ||
      !formData.value.unidad_id === null ||
      formData.value.precio_unitario == null
    ) { 
      Swal.fire({
        icon: "error",
        title: "Campos incompletos",
        text: "Por favor, complete todos los campos obligatorios.",
      });
      return;
    }

    // Crear un FormData para manejar los archivos
    const form = new FormData();
    form.append("nombre", formData.value.nombre);
    form.append("cantidad", formData.value.cantidad.toString());
    form.append("stock_minimo", formData.value.stock_minimo.toString());
    form.append("fecha_ingreso", formData.value.fecha_ingreso);
    form.append("vida_util_dias", formData.value.vida_util_dias.toString());
    form.append("unidad_id", parseInt(formData.value.unidad_id).toString());
    form.append("precio_unitario", parseInt(formData.value.precio_unitario).toString());
    
    if (formData.value.file instanceof File) {
      form.append("file", formData.value.file);
    }

    


    const response = await axios.post("http://127.0.0.1:8000/materia", form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
    });

  
    Swal.fire({
      icon: "success",
      title: "Materia Prima agregada con éxito",
      text: `La Materia Prima ${response.data.nombre} fue agregada correctamente.`,
    });

    // Resetear formulario
    formData.value = {
      nombre: "",
      cantidad: null,
      stock_minimo: null,
      fecha_ingreso: "",
      vida_util_dias: null,
      unidad_id: "",
      precio_unitario: null,
      file: null,
    };

    // Cerrar el modal después de enviar
    closeModal();
  } catch (error) {
    console.error("Error al agregar la Materia Prima:", error.response?.data || error.message);
    if (error.response) {
    console.error("Detalles del error:", error.response.data);
    }
    Swal.fire({
      icon: "error",
      title: "Error al agregar la materia prima",
      text: error.response?.data?.detail || "Hubo un problema al agregar la materia prima. Verifique los datos e intente nuevamente.",
    });
  }
};

// Emitir evento para cerrar el modal
const emit = defineEmits(["close"]);
const closeModal = () => {
  emit("close");
};
</script>

<template>
  <transition name="fade">
    <div class="modal-overlay" @click="closeModal"> 
      <h1 class="titulo">Agregar Materia Prima</h1>
      <div class="modal-content" @click.stop>
        <div class="form-container">
          <form @submit.prevent="handleSubmit">

            <div class="column">
              <label for="nombre">Nombre:</label>
              <input type="text" id="nombre" v-model="formData.nombre" placeholder="Ingrese el nombre" required />

              <label for="cantidad">Cantidad:</label>
              <input type="number" id="cantidad" v-model="formData.cantidad" placeholder="Cantidad en stock" required />

              <label for="stock_minimo">Stock Mínimo:</label>
              <input type="number" id="stock_minimo" v-model="formData.stock_minimo" placeholder="Stock mínimo permitido" required />

              <label for="fecha_ingreso">Fecha de Ingreso:</label>
              <input type="date" id="fecha_ingreso" v-model="formData.fecha_ingreso" required />
            </div>

            <div class="column">
              <label for="vida_util_dias">Vida Útil (días):</label>
              <input type="number" id="vida_util_dias" v-model="formData.vida_util_dias" placeholder="Días de vida útil" required />

              <label for="unidad_id">Unidad ID:</label>
              <select id="unidad_id" v-model="formData.unidad_id" required>
                <option disabled value="">Seleccione una unidad</option>
                <option
                  v-for="unidad in unidades"
                  :key="unidad.id"
                  :value="unidad.id"
                >
                  {{ unidad.nombre }} ({{ unidad.simbolo }})
                </option>
              </select>
              
              <label for="precio_unitario">Precio Unitario:</label>
              <input type="number" id="precio_unitario" v-model="formData.precio_unitario" placeholder="Ingrese precio unitario" required />

              <label for="imagen">Imagen:</label>
              <input type="file" id="imagen" @change="handleImageUpload">
            </div>

            <button type="submit" class="agregar">Agregar</button>
          </form>
        </div>
      </div>
      <button @click="closeModal" class="close-btn">X</button>
    </div>
  </transition>
</template>


  

<style scoped>






.titulo{
  position: absolute;
  top: 9%;
  left: 51%;
  transform: translate(-50%, -50%);
  font-family: 'Jura', sans-serif;
  font-size: 28px;
  text-align: center;
  color: #ffd700;
  background-color: transparent;
  padding: 10px 20px;
  border-radius: 8px;
  width: auto;
}


h1 {
  font-family: 'Jura', sans-serif;
  font-size: 24px;
  text-align: center;
  color: #ffd700; /* Amarillo */
  margin-left: -20px;
  margin-top: -30px;
  position: relative;
  z-index: 10;
}

  /* Estilo del formulario */
.form-container {
  background-color: #00000077; /* Fondo negro */
  padding: 15px;
  width: 910px;
  height: 598px;
  margin: 0 auto;
  border-radius: 8px;
  margin-top: -20px;
  border: 2px solid;
  margin-left: -15px;
}

form {
 display: flex;
  gap: 20px;
  width: 100%;
}

.column {
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  color: #fff; /* Texto blanco */
  font-size: 13px;
  margin-bottom: 5px;
  font-family: 'Jura', sans-serif;
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

.form-container select{
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

.agregar {
  background-color: #ffecb3;
  color: #000;
  padding: 10px 15px;
  width: 250px;
  height: 60px;
  font-size: 14px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: 0.3s ease;
  font-family: 'Jura', sans-serif;
  margin-top: 430px;
  margin-left: -89px;
}

.agregar:hover {
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
  z-index: 99;
}

.modal-content {
  background-color: rgb(0, 0, 0);
  margin-top: 50px;
  padding: 17px;
  width: 910px;
  height: 590px;
  max-width: 1000px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.close-btn {
  background-color: red;
  color: rgb(255, 255, 255);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  margin-top: -630px;
  margin-right: 20px;
  margin-left: -60px;
  width: 60px;

}

.close-btn:hover {
  background-color: rgb(255, 255, 255);
}


/* transiciones para el */ 

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.fade-enter-to, .fade-leave-from {
  opacity: 1;
}


</style>