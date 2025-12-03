<script setup lang="ts">
import { ref, computed } from "vue";
import axios from "axios";
import Swal from "sweetalert2";
import { defineEmits } from 'vue';

const emit = defineEmits(["close"]);

const searchTerm = ref("")
const isModalOpen = ref(false);
const unidades = ref([]);
const ActModal = ref(false);
const materiaSeleccionada = ref<any>(null);
const materiasPrimas = ref([]);


// 1️.Definición de datos reactivos
const formData = ref({ 
  id: null,        
  nombre: "",         
  cantidad: null,    
  ruta_imagen: null as File | null,     
  stock_minimo: null,  
  fecha_ingreso: "",   
  vida_util_dias: null,
  unidad_id: "",  
});

const camposModificados = ref({
  id: false,        
  nombre: false,         
  cantidad: false,    
  ruta_imagen: false,     
  stock_minimo: false,  
  fecha_ingreso: false,   
  vida_util_dias: false,
  unidad_id: false,  
})



// Cargar unidades de medida
const cargarUnidades = async () => {
  try {
    const response = await axios.get("http://localhost:8000/materia/unidades-medida");
    unidades.value = response.data;
  } catch (error) {
    console.error("Error al obtener unidades de medida", error);
  }
};
cargarUnidades();

// Cargar materias primas desde la API
const cargarMateriasPrimas = async () => {
  try {
    const respuesta = await axios.get("http://127.0.0.1:8000/materia");
    materiasPrimas.value = respuesta.data;
  } catch (error) {
    console.error("Error al cargar materias primas:", error);
  }
};

cargarMateriasPrimas();


//Funcion para filtrar los productos por terminos de busqueda
// Definimos la funcion computed para que se actualice cuando halla un cambio
const filtrarmateria = computed(() => {
  // Si el campo esta vacio devuelve los productos sin ningun cambgio
  if(!searchTerm.value.trim()) return materiasPrimas.value
  // Obtenemos el valor lo pareseamos a minisculas y le quitamos los espacio (trim())
  const term = searchTerm.value.toLowerCase().trim()
  // Filtramos lo prodcutos que cumplan con el termino de busqueda
  // por cada producto tomamos su nombre, se pasa a minusculas y si incluye el termino de busqueda lo dejamos si no, lo descartamos
  return materiasPrimas.value.filter(materia => materia.nombre.toLowerCase().includes(term))
});



const handleInputChange = async (campo: string) => {
  camposModificados.value[campo] = true
}

const handleImageUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    formData.value.ruta_imagen = file;
    camposModificados.value.ruta_imagen = true;
  }
};

// 4.Función para enviar los datos actualizados al backend
const handleSubmit = async () => {
  try {
    const camposActualizados: any = {};
    for (const campo in camposModificados.value) {
      if (camposModificados.value[campo]) {
        switch(campo){
          case "nombre":
            camposActualizados["nombre"] = formData.value.nombre;
            break;
          case "cantidad":
            camposActualizados["cantidad"] = Number((formData.value.cantidad ?? 0).toFixed(2));
            break;
          case "stock_minimo":
            camposActualizados["stock_minimo"] = Number(formData.value.stock_minimo.toFixed(2));
            break;
          case "fecha_ingreso":
            camposActualizados["fecha_ingreso"] = formData.value.fecha_ingreso;
            break;
          case "vida_util_dias":
            camposActualizados["vida_util_dias"] = Number((formData.value.vida_util_dias ?? 0).toFixed(2));
            break;
          case "unidad_id":
            camposActualizados["unidad_id"] = unidades.value.find(u => u.nombre ===  formData.value.unidad_id)?.id || null;
            break;
          case "ruta_imagen":
            camposActualizados["ruta_imagen"] = formData.value.ruta_imagen;
            break;
          default:
            camposActualizados[campo] = formData.value[campo];
        }
      }
    }

    console.log('Payload being sent:', camposActualizados);

    
    if (Object.keys(camposActualizados).length > 0) {
    const response = await axios.patch(
      `http://127.0.0.1:8000/materia/${formData.value.id}`, 
      camposActualizados
    );
    Swal.fire({
        icon: "success",
        title: "Materia Prima Actualizada",
        text: "La materia prima ha sido actualizada correctamente."
    });
    closeModal();
    cargarMateriasPrimas();
    } else {
      Swal.fire({
        icon: "info",
        title: "Informacion",
        text: "No se han realizado modificaciones."
      });
    }
  } catch (error) {
    console.error("Error al actualizar la materia prima:", error);
    Swal.fire({
      icon: "error",
      title: "Error al actualizar",
      text: error.response?.data?.detail || "Hubo un problema al actualizar la materia prima."
    });
  }
};

const openActModal = (materia: any) => {
  formData.value = {
    id: materia.id,
    nombre: materia.nombre || "",
    cantidad: materia.cantidad || null,
    stock_minimo: materia.stock_minimo || null,
    fecha_ingreso: materia.fecha_ingreso || "",
    vida_util_dias: materia.vida_util_dias || null,
    unidad_id: materia.unidad_id || "",
    ruta_imagen: materia.ruta_imagen ? materia.ruta_imagen : null, 
  };
  
  for (const campo in camposModificados.value) {
      camposModificados.value[campo] = false;
  }
    
  materiaSeleccionada.value = materia;
  ActModal.value = true;
};


const closeActModal = () => {
  ActModal.value = false;
};


const closeModal = () => {
  emit('close');  
};
</script>

<template>
  <!--  Modal para actualizar la materia prima -->
  <div class="modal-overlay" >
    <div class="modal-content" @click.stop>
      <button @click="closeModal" class="close-btn3">X</button>
      <h1>Seleccione la materia prima a actualizar</h1>
      <input type="text" v-model="searchTerm" placeholder="Buscar Materia Prima..." class="search-input" />

      <div class="productos-grid">
        <div v-for="materia in filtrarmateria" :key="materia.id" class="productos-card">
          <div class="productos-imagen">
            <img v-if="materia.ruta_imagen" :src="`http://127.0.0.1:8000/materia/${materia.ruta_imagen}`" />
          </div>
          <div class="productos-info">
          <h4>{{ materia.nombre }}</h4>
          <p v-if="materia.cantidad">Stock: {{ materia.cantidad }} {{ materia.unidad.simbolo }}</p>
          </div>

          <button @click="openActModal(materia)" class="btn-agregar-productos">Actualizar</button>
        </div>
      </div>

      <div v-if="filtrarmateria.length === 0" class="no-results">
        No se encontraron resultados con la búsqueda
      </div>

      <div class="modal-footer">
        <button @click="closeModal" class="btn-finalizar">Finalizar</button>
      </div>
    </div>


      <div class="modal-overlay" v-if="ActModal">
        <div class="form-container">
          <button @click="closeActModal" class="close-btn4">X</button>
          <form @submit.prevent="handleSubmit">
          <label for="id">ID de la materia prima:</label>
            <input
              type="number"
              id="id"
              v-model="formData.id"
              disabled
            />

            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" v-model="formData.nombre"  placeholder="Ingrese el nombre" @input="handleInputChange('nombre')" />

            <label for="cantidad">Cantidad:</label>
            <input type="number" id="cantidad" v-model="formData.cantidad"  placeholder="Cantidad en stock" @input="handleInputChange('cantidad')" />

            <label for="stock_minimo">Stock Mínimo:</label>
            <input type="number" id="stock_minimo" v-model="formData.stock_minimo"   placeholder="Stock mínimo permitido" @input="handleInputChange('stock_minimo')"  />

            <label for="fecha_ingreso">Fecha de Ingreso:</label>
            <input type="date" id="fecha_ingreso" v-model="formData.fecha_ingreso" placeholder="Ingrese la fecha de ingreso" @input="handleInputChange('fecha_ingreso')" />

            <label for="vida_util_dias">Vida Útil (días):</label>
            <input type="number" id="vida_util_dias" v-model="formData.vida_util_dias" placeholder="Días de vida útil" @input="handleInputChange('vida_util_dias')"   />

            <label for="unidad_id">Unidad ID:</label>
            <select id="unidad_id" v-model="formData.unidad_id" placeholder="ID de la unidad" @input="handleInputChange('unidad_id')" >
              <option v-for="unidad in unidades" :key="unidad.nombre" :value="unidad.nombre">
                {{ unidad.nombre }} ({{ unidad.simbolo }})
              </option>
            </select>

            <label for="imagen">Imagen:</label>
            <input type="file" id="imagen" @change="handleImageUpload">

            <button type="submit" class="act-bottom">Actualizar</button>

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
  margin-left: 20px;
}
/* Estilo del formulario */
.form-container {
  background-color: #000000; /* Fondo negro */
  padding: 15px;
  width: 700px;
  height: 585px;
  margin-top: 40px;
  border-radius: 8px;
  margin-left: 435.5px;
  border: 2px solid;
}
.close-btn4 {
  background-color: transparent;
  color: rgb(255, 0, 0);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  width: 60px;
  margin-left: 640px;
  transition: all 0.3s ease-in-out;
}
.close-btn4:hover {
  background-color: darkred;
  transform: scale(1.1);
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
  padding: 7px;
  border: none;
  border-radius: 4px;
  background-color: #cf9b00; /* Color amarillo similar */
  color: #000;
  font-size: 12px;
}
input::placeholder {
  color: #000;
  opacity: 0.8;
}
.act-bottom {
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
  margin-left: 280px;
  transition: all 3.0s ease-in-ou;
  margin-top: 18px;
}
.act-bottom:hover {
  background-color: #ffd700;
  transform: scale(1.05);
}
.modal-overlay {
  text-align: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
}
.modal-content {
  font-family: 'Jura', sans-serif;
  position: fixed;
  left: 27%;
  width: 50%;
  height: 95%;
  background-color: rgb(0, 0, 0);
    margin-top: 20px;
  transition: all 0.3s ease;
  border: solid #cf9b00;
  border-radius: 5%;
  overflow-y: auto; /* Activa el scroll vertical */
}
.productos-grid{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
  overflow-y: auto;
}
.productos-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}
.productos-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}
.productos-imagen {
  height: 120px;
  overflow: hidden;
}
.productos-imagen img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.productos-card:hover .productos-imagen img {
  transform: scale(1.05);
}
.productos-info {
  padding: 0.8rem;
}
.productos-info h4 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}
.productos-info p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
}
.btn-agregar-productos {
  width: 100%;
  padding: 0.6rem;
  background-color: #000000;
  color: white;
  border: none;
  cursor: pointer;
  transition: transform ease-in-out 0.3s;
  font-family: 'Jura', sans-serif;
}
.btn-agregar-productos:hover {
  background-color: #cf9b00;
  transform: scale(1.1);
}
.no-results {
  padding: 2rem;
  text-align: center;
  color: #666;
  font-style: italic;
}
.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
}
.btn-finalizar {
  background-color: #de0a0a;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.3s ease-in-out;
}
.btn-finalizar:hover{
  transform: scale(1.1);
}
.close-btn3 {
  background-color: transparent;
  color: rgb(255, 0, 0);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  width: 60px;
  margin-left: 670px;
  margin-top: 23px;
  transition: all 0.3s ease-in-out;
}
.close-btn3:hover {
  background-color: darkred;
  transform: scale(1.1);
}

</style>