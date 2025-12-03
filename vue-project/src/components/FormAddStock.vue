<script setup>
import { ref, defineProps, defineEmits  } from "vue";
import axios from "axios";
import Swal from "sweetalert2";

const props = defineProps(["materia"]);

const cantidad = ref(null);
const fecha_ingreso = ref("");
const vida_util_dias = ref(null);
const precio_unitario = ref(null);

const agregarStock = async () => {
  try {
    if (cantidad.value <= 0) {
       Swal.fire({
            icon: "warning",
            title: "Cantidad no válida",
            text: "Debe ingresar una cantidad mayor a 0.",
        });
        return;
    }

    await axios.put(`http://127.0.0.1:8000/materia/agregar-stock/${props.materia.id}`, {
      cantidad: cantidad.value,
      fecha_ingreso: fecha_ingreso.value,
      vida_util_dias: vida_util_dias.value,
      precio_unitario: precio_unitario.value
    });

    Swal.fire({
      icon: "success",
      title: "Exito",
      text: `Stock agregado correctamente a ${props.materia.nombre}.`,
    });

    closeModal();
  } catch (error) {
    console.error("Error al agregar stock:", error);
    Swal.fire({
      icon: "error",
      title: "Error ",
      text: "Hubo un problema al agregar stock. Intenta nuevamente.",
    });
  }
};

const emit = defineEmits(['close']); // Emitir el evento 'close'

const closeModal = () => {
  emit('close');  // Emitir el evento para cerrar el modal
};


</script>

<template>
    <div class="modal-overlay"  @click="closeModal">
      <div class="modal-content" @click.stop >
        <h1 class="titulo">Agregar Stock - {{ materia.nombre }}</h1>
        <div class="form-container">
          <form @submit.prevent="agregarStock">
            <label for="cantidad">Cantidad</label>
            <input type="number" id="cantidad" v-model="cantidad" placeholder="Ingrese la cantidad" required>
  
            <label for="fecha_ingreso">Fecha de Ingreso</label>
            <input type="date" id="fecha_ingreso" v-model="fecha_ingreso"  placeholder="Ingrese la fecha de ingreso" required>
  
            <label for="vida_util">Vida Útil (días)</label>
            <input type="number" id="vida_util" v-model="vida_util_dias" placeholder="Ingrese vida útil en días" required>

            <label for="precio_unitario">Precio Unitario</label>
            <input type="number" id="precio_unitario" v-model="precio_unitario" placeholder="Ingrese precio unitario" required />

            <button type="submit">Agregar </button>
          </form>
        </div>
      </div>
      <button @click="closeModal" class="close-btn">X</button>
    </div>
</template>


<style scoped>
.titulo {
  position: absolute;
  top: 32%;
  left: 51%;
  transform: translate(-50%, -50%);
  font-family: 'Jura', sans-serif;
  font-size: 25px;
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
  color: #ffd700;
  margin-left: -25px;
  margin-top: -50px;
  position: relative;
  z-index: 10;
}

.form-container {
  background-color: #00000077;
  padding: 15px;
  width: 600px;
  height: 332x;
  margin: 0 auto;
  border-radius: 8px;
  border: 2px solid;
  margin-left: -15px;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  color: #fff;
  font-size: 13px;
  margin-bottom: 5px;
  font-family: 'Jura', sans-serif;
  text-align: center;
}

input, select {
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
  font-size: 15px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s ease;
  font-family: 'Jura', sans-serif;
  width: 130px;
  height: 35px;
  margin-left: 235px;
  margin-top: 9px;
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
  z-index: 99;
}

.modal-content {
  background-color: rgb(0, 0, 0);
  margin-top: 50px;
  padding: 17px;
  width: 600px;
  height: 350px;
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
  margin-top: -390px;
  margin-right: 20px;
  margin-left: -60px;
  width: 60px;
}

.close-btn:hover {
  background-color: rgb(255, 255, 255);
}

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