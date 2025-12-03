<script setup lang="ts">
import { ref, computed, watch } from "vue";
import axios from "axios";
import Swal from "sweetalert2";

const categorias = ref([]);
const ingredientes = ref([]);
const unidades = ref([]);
const productos = ref([]);
const usuario = ref([]);

const showIngredientesModal = ref(false);
const showCantidadModal = ref(false);
const selectedUnidad_id = ref(null);
const cantidadIngrediente = ref(null);
const selectedUnidad = ref(null);
const searchTerm = ref("");
const currentIngrediente = ref(null);

// Form data
const formData = ref({
  nombre: "",
  precio: null,
  precio_entrada: null,
  cantidad: null,
  id_empleado: 0,
  categoria: "",
  imagen: null as File | null,
  stockMinimo: null,    
  tipo: "COMPRADO",
  ingredientes: [] as {id: number; nombre: string; cantidad: number; unidad: string; imagen?: string; unidad_id: number}[],
});

// Filtrar ingredientes según término de búsqueda
const filteredIngredientes = computed(() => {
  if (!searchTerm.value.trim()) return ingredientes.value;
  
  const term = searchTerm.value.toLowerCase().trim();
  return ingredientes.value.filter(ing => 
    ing.nombre.toLowerCase().includes(term)
  );
});

// Watch para resetear ingredientes si cambia el tipo
watch(() => formData.value.tipo, (newValue) => {
  if (newValue !== "HECHO") {
    formData.value.ingredientes = [];
  }
});


const cargarProductos = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/productos")
    productos.value = respuesta.data
  } catch (error) {
    console.error("Error al cargar los produtos", error)
  }
}

cargarProductos();

const cargarCategorias = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/productos/categorias")
    categorias.value = respuesta.data
  } catch (error) {
    console.error("Error al cargar los produtos", error)
  }
}

cargarCategorias();

cargarProductos();

const cargarMateria = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/materia");
    ingredientes.value = respuesta.data;  
  } catch (error) {
    console.error("Error al cargar la materia prima");
  }
}

cargarMateria();

const cargarUnidadMedida = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/materia/unidades-medida");
    unidades.value = respuesta.data;
  } catch (error) {
    console.error("Error al cargar las unidades de medida");
  }
}

cargarUnidadMedida();

const cargarEmpleados = async () => {
  try {
    const respuesta = await axios.get("https://coffebikefastapi-production.up.railway.app/usuarios");
    usuario.value = respuesta.data;  
  } catch (error) {
    console.error("Error al cargar los usuarios");
  }
}

cargarEmpleados()

const handleImageUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    formData.value.imagen = file;
  }
};

const openIngredientesModal = () => {
  showIngredientesModal.value = true;
  searchTerm.value = "";
};

const closeIngredientesModal = () => {
  showIngredientesModal.value = false;
};

const openCantidadModal = (ingrediente) => {
  currentIngrediente.value = ingrediente;
  cantidadIngrediente.value = null;
  selectedUnidad.value = null;
  showCantidadModal.value = true;
  // Usamos esto para evitar scroll en el body principal
  document.documentElement.style.overflow = "hidden";
  document.documentElement.style.height = "100hv";
};

const closeCantidadModal = () => {
  showCantidadModal.value = false;
  document.body.classList.remove("no-scroll");
  currentIngrediente.value = null;
  // Restaurtamos el scroll en el body principal
  document.documentElement.style.overflow = "";
  document.documentElement.style.height = "";
};

const actualizarUnidad = () => {
  const unidadSeleccionada = unidades.value.find(u => u.nombre === selectedUnidad.value);
  if (unidadSeleccionada) {
    selectedUnidad_id.value = unidadSeleccionada.id;
  }
};

const agregarIngrediente = () => {
  if (!currentIngrediente.value || cantidadIngrediente.value === null || !selectedUnidad.value || !selectedUnidad_id.value) {
    Swal.fire({
      icon: "error",
      title: "Campos incompletos",
      text: "Por favor, ingrese la cantidad y seleccione una unidad.",
    });
    return;
  }

  // Verificar si el ingrediente ya existe en la lista
  const ingredienteExistente = formData.value.ingredientes.findIndex(
    item => item.nombre === currentIngrediente.value.nombre
  );

  if (ingredienteExistente >= 0) {
    // Actualizar cantidad si ya existe
    formData.value.ingredientes[ingredienteExistente].cantidad = cantidadIngrediente.value;
    formData.value.ingredientes[ingredienteExistente].unidad = selectedUnidad.value;
    
    Swal.fire({
      icon: "success",
      title: "Ingrediente actualizado",
      text: `Se actualizó la cantidad de ${currentIngrediente.value.nombre}`,
      timer: 1500,
      showConfirmButton: false
    });
  } else {
    // Agregar nuevo ingrediente a la lista
    formData.value.ingredientes.push({
      id: currentIngrediente.value.id,
      nombre: currentIngrediente.value.nombre,
      cantidad: cantidadIngrediente.value,
      unidad: selectedUnidad.value,
      unidad_id: selectedUnidad_id.value,
      imagen: currentIngrediente.value.imagen || null
  });
    
    Swal.fire({
      icon: "success",
      title: "Ingrediente agregado",
      text: `${currentIngrediente.value.nombre} agregado a la receta`,
      timer: 1500,
      showConfirmButton: false
    });
  }

  // Cerrar modal
  closeCantidadModal();
};

const eliminarIngrediente = (index: number) => {
  Swal.fire({
    title: "¿Eliminar ingrediente?",
    text: `¿Desea eliminar ${formData.value.ingredientes[index].nombre} de la receta?`,
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#ffd700",
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar"
  }).then((result) => {
    if (result.isConfirmed) {
      formData.value.ingredientes.splice(index, 1);
      Swal.fire({
        icon: "success",
        title: "Ingrediente eliminado",
        timer: 1500,
        showConfirmButton: false
      });
    }
  });
};
const handleSubmit = async () => {
  try {
    // Validar datos antes de enviarlos
    if (
      !formData.value.nombre ||
      formData.value.cantidad === null ||
      formData.value.stockMinimo === null || 
      !formData.value.tipo 
    ) {
      Swal.fire({
        icon: "error",
        title: "Campos incompletos",
        text: "Por favor, complete todos los campos obligatorios.",
      });
      return;
    }

    // Validar que si es un producto hecho, tenga ingredientes
    if (formData.value.tipo === "HECHO" && formData.value.ingredientes.length === 0) {
      Swal.fire({
        icon: "error",
        title: "Receta vacía",
        text: "Los productos de tipo 'Hecho' deben tener al menos un ingrediente.",
      });
      return;
    }

    // Crear un objeto FormData para enviar tanto los datos como la imagen
    const form = new FormData();
    form.append("nombre", formData.value.nombre);
    form.append("cantidad", formData.value.cantidad?.toString() ?? "0");
    form.append("id_usuario", formData.value.id_empleado.toString());
    form.append("categoria", formData.value.categoria);
    form.append("stock_minimo", formData.value.stockMinimo?.toString() ?? "0");
    form.append("tipo", formData.value.tipo);



    if (formData.value.tipo === "COMPRADO") {
      form.append("precio_entrada", formData.value.precio_entrada?.toString() ?? "0");
      form.append("precio_salida", formData.value.precio?.toString() ?? "0");
    } else if (formData.value.tipo === "HECHO") {
      form.append("precio_salida", formData.value.precio?.toString() ?? "0");
      form.append("preparar_inicial", "true");
          // Preparar lista de ingredientes en el formato que espera el backend
      const ingredientesParaEnviar = formData.value.ingredientes.map(ing => ({
        materia_prima_id: ing.id,
        cantidad_ingrediente: ing.cantidad,
        unidad_id: ing.unidad_id,
      }));
        
        // Convertir a string JSON
      const ingredientesJsonString = JSON.stringify(ingredientesParaEnviar);
      form.append("ingredientes", ingredientesJsonString);
    }

    // Si hay una imagen, añadirla a la solicitud
    if (formData.value.imagen instanceof File) {
      form.append("file", formData.value.imagen);
    }

    console.log("Enviando form data:");
    for (let pair of form.entries()) {
      console.log(pair[0]+ ': ' + pair[1]); 
    }

    // Realizar la solicitud POST al backend
    const response = await axios.post("https://coffebikefastapi-production.up.railway.app/productos", form, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });


    Swal.fire({
      icon: "success",
      title: "Producto agregado con éxito",
      text: `El producto ${response.data.nombre} fue agregado correctamente.`,
    });

    // Limpiar el formulario después de enviar
    formData.value = {
      nombre: "",
      precio: null,
      precio_entrada: null,
      cantidad: null,
      id_empleado: 0,
      categoria: "PLATO",
      imagen: null,
      stockMinimo: null,
      tipo: "COMPRADO",
      ingredientes: []
    };
    
    // Cerrar el modal después de enviar
    closeModal();
  } catch (error) {
    console.error("Error al agregar el producto:", error.response?.data || error.message);
    Swal.fire({
      icon: "error",
      title: "Error al agregar el producto",
      text: error.response?.data?.detail || "Hubo un problema al agregar el producto. Verifique los datos e intente nuevamente.",
    });
  }
};

// Emitir evento para cerrar el modal
const emit = defineEmits(["close"]);
const closeModal = () => {
  emit("close")
};
</script>



<template>
<transition name="fade2">
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <button @click="closeModal" class="close-btn">X</button>
      <h1>Agregar Producto</h1>
      <div class="form-container">
        <form @submit.prevent="handleSubmit">

          <div class="column">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" v-model="formData.nombre" placeholder="Ingrese el nombre del producto" required />

            <label for="cantidad">Cantidad:</label>
            <input type="number" id="cantidad" v-model="formData.cantidad" placeholder="Ingrese la cantidad" required />

            <label for="precio">Precio de venta:</label>
            <input type="number" id="precio" v-model="formData.precio" placeholder="Ingrese el precio para vender el producto"  required />
          </div>

          <div class="column">
            <label for="nombre">Nombre de quien agrega el producto:</label>

            <select
              id="idEmpleado"
                v-model="formData.id_empleado"
                required
              >
                <option value="">Seleccione una categoría</option>
                <option
                   v-for="usuarioItem in usuario"
                  :key="usuarioItem.id"
                  :value="usuarioItem.id"
                >
                  {{ usuarioItem.nombre }}
                </option>
            </select>

            <label for="categoria">Categoría:</label>
            <select id="categoria" v-model="formData.categoria" required>
              <option value="" >Seleccione una categoria</option>
                  <option v-for="categoria in categorias" :key="categoria" :value="categoria" placeholder="">
                    {{ categoria }}
                </option>
            </select>

            <label for="tipo">Tipo:</label>
            <select id="tipo" v-model="formData.tipo" required>
              <option value="HECHO">Hecho</option>
              <option value="COMPRADO">Comprado</option>
            </select>

            <!-- Mostrar input de precio de entrada si es COMPRADO -->
            <label v-if="formData.tipo === 'COMPRADO'" for="precioEntrada">Precio de Entrada:</label>
            <input 
              v-if="formData.tipo === 'COMPRADO'" 
              type="number" 
              id="precioEntrada" 
              v-model="formData.precio_entrada" 
              placeholder="Ingrese el precio de entrada" 
              required 
            />
           <transition class="fade-expand">
                <div v-if="formData.tipo === 'HECHO'" class="ingredientes-button-container">
                   <button type="button" @click="openIngredientesModal" class="btn-agregar-receta">
                       Agregar/Editar Receta
                   </button>
                  <span v-if="formData.ingredientes.length > 0" class="ingredientes-count">
                        {{ formData.ingredientes.length }} ingredientes agregados
                  </span>
                </div>
            </transition>

            
            <label for="stockMinimo">Stock Mínimo:</label>
            <input type="number" id="stockMinimo" v-model="formData.stockMinimo" placeholder="Ingrese el stock mínimo" required />

            <label for="imagen">Agregar imagen:</label>
            <input type="file" id="imagen" @change="handleImageUpload">
          </div>

          <button type="submit" class="agregar">Agregar</button>
        </form>
        
          <!-- Modal de ingredientes -->
        <transition name="fade2">
          <div v-if="showIngredientesModal" class="ingredientes-modal-overlay">
            <div class="ingredientes-modal">
              <div class="modal-header">
                <button @click="closeIngredientesModal" class="close-btn3">X</button>
                <h2>Seleccione ingredientes para la receta</h2>
              </div>
              <div class="search-container">
                <input 
                  type="text" 
                  v-model="searchTerm" 
                  placeholder="Buscar ingredientes..." 
                  class="search-input"
                >
              </div>

              <!-- Lista de ingredientes ya agregados -->
              <div v-if="formData.ingredientes.length > 0" class="added-ingredients">
                <h3>Ingredientes en la receta</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Ingrediente</th>
                      <th>Cantidad</th>
                      <th>Unidad</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(ing, idx) in formData.ingredientes" :key="idx">
                      <td class="ingredient-name">
                        <img 
                          v-if="ing.imagen" 
                          :src="ing.imagen" 
                          alt="Imagen de ingrediente" 
                          class="ingredient-image"
                        >
                        {{ ing.nombre }}
                      </td>
                      <td>{{ ing.cantidad }}</td>
                      <td>{{ ing.unidad }}</td>

                      <td>
                        <button @click="openCantidadModal(ing)" class="btn-edit">Editar</button>
                        <button @click="eliminarIngrediente(idx)" class="btn-delete">Eliminar</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="ingredientes-grid">
                <div v-for="ingrediente in filteredIngredientes" :key="ingrediente.id" class="ingrediente-card">
                  <div class="ingrediente-imagen">
                    <img v-if="ingrediente.ruta_imagen" :src="`https://coffebikefastapi-production.up.railway.app/materia/${ingrediente.ruta_imagen}`" />
                  </div>
                  <div class="ingrediente-info">
                    <h4>{{ ingrediente.nombre }}</h4>
                    <p v-if="ingrediente.cantidad">Stock: {{ ingrediente.cantidad }} {{ ingrediente.unidad.simbolo }}</p>
                  </div>
                  <button 
                    @click="openCantidadModal(ingrediente)" 
                    class="btn-agregar-ingrediente">Agregar</button>
                </div>
              </div>

              <div v-if="filteredIngredientes.length === 0" class="no-results">
                No se encontraron ingredientes que coincidan con la búsqueda.
              </div>

              <div class="modal-footer">
                <button @click="closeIngredientesModal" class="btn-finalizar">Finalizar</button>
              </div>
            </div>
          </div>
        </transition>

          
        <!-- Modal para cantidad y unidad -->
        <div v-if="showCantidadModal" class="cantidad-modal-overlay" @click="closeCantidadModal">
          <div class="cantidad-modal" @click.stop>
            <div class="modal-header">
              <button @click="closeCantidadModal" class="close-btn2">X</button>

              <h3>Agregar {{ currentIngrediente?.nombre }}</h3>
            </div>

            <div class="cantidad-form">
              <div class="form-group">
                <label for="cantidad">Cantidad:</label>
                <input 
                  type="number" 
                  id="cantidad" 
                  v-model="cantidadIngrediente" 
                  placeholder="Ej: 250" 
                  min="0.01" 
                  step="0.01"
                  class="cantidad-input"
                  autofocus
                >
              </div>

              <div class="form-group">
                <label for="unidad">Unidad de medida:</label>
                <select id="unidad" v-model="selectedUnidad" @change="actualizarUnidad" class="unidad-select">
                  <option value="" disabled selected>Seleccione una unidad</option>
                  <option v-for="unidad in unidades" :key="unidad.id" :value="unidad.nombre">
                    {{ unidad.nombre }} ({{ unidad.simbolo }})  
                  </option>
                </select>
              </div>
            </div>

            <div class="modal-footer">
              <button @click="closeCantidadModal" class="btn-cancelar">Cancelar</button>
              <button @click="agregarIngrediente" class="btn-confirmar">Confirmar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</transition>

</template>


<style scoped>
h1 {
  font-family: 'Jura', sans-serif;
  font-size: 24px;
  text-align: center;
  color: #ffd700;
  margin-top: -13px;
}

.form-container {
  border: 2px solid white;
  background-color: #000;
  padding: 20px;
  width: 1000px;
  height: 520px;
  max-width: 1200px;
  border-radius: 8px;
  display: flex;
  gap: 15px;
  margin-left: -20px;
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
  color: #fff;
  font-size: 12px;
  margin-bottom: 5px;
  font-family: 'Jura', sans-serif;
}

input,
select {
  font-family: 'Jura', sans-serif;
  margin-bottom: 15px;
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #cf9b00;
  color: #000;
  font-size: 14px;
  width: 450px;
  margin-left: 10px;
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
  z-index: 9999;
  backdrop-filter: blur(5px); /* Desenfoque del contenido detrás del overlay */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: rgba(0, 0, 0, 0.261);
  padding: 30px;
  width: 1000px;
  height: 600px;
  max-width: 1000px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.close-btn {
  color: rgb(247, 247, 247);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  margin-left: 980px;
  width: 50px;
  background-color: red;
  transition: 0.3s ease;

}

.close-btn:hover {
  background-color: #cf0000;
  transform: scale(1.1);
}

.ingredientes-modal-overlay{
  text-align: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
}
.close-btn2 {
  color: rgb(247, 247, 247);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  margin-left: 380px;
  margin-top: 22px;
  width: 50px;
  background-color: red;
  transition: 0.3s ease;
}
.close-btn3 {
  color: rgb(247, 247, 247);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  margin-left: 730px;
  margin-top: 22px;
  width: 50px;
  background-color: red;
  transition: 0.3s ease;
}
.close-btn2:hover, .close-btn3:hover {
  background-color: #cf0000;
  transform: scale(1.1);
}
.ingredientes-modal{
  font-family: 'Jura', sans-serif;
  position: fixed;
  left: 10%;
  width: 80%;
  height: 100%;
  background-color: rgb(0, 0, 0);
  z-index: 1100;
  transition: all 0.3s ease;
  border: solid #cf9b00;
  border-radius: 5%;
  overflow-y: auto; /* Activa el scroll vertical */
}

.cerrar-ingredientes {
  color: rgb(247, 247, 247);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  width: 50px;
  background-color: red;
  transition: 0.3s ease;
  margin-top: -51%;
  margin-left: 84%;

}

.cerrar-ingredientes:hover {
  background-color: #cf0000;
  transform: scale(1.1);
}


@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-content, .ingredientes-section {
  animation: modalAppear 0.2s ease-out forwards;
}

.btn-agregar-receta{
  background-color: #ffecb3;
  color: #000;
  width: 170px;
  height: 30px;
  font-size: 13px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: 0.3s ease;
  font-family: 'Jura', sans-serif;
  margin-left: 149px;
}

.btn-agregar-receta:hover{
  background-color: #af9608;
  transform: scale(1.1);

}

.added-ingredients {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #eee;
}

.added-ingredients table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}

.added-ingredients th, .added-ingredients td {
  padding: 0.6rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.ingredient-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 12px;
}

.ingredient-image {
  width: 30px;
  height: 30px;
  object-fit: cover;
  border-radius: 4px;
}

.btn-edit, .btn-delete {
  padding: 0.3rem 0.6rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-right: 0.3rem;
  transition: transform 0.2s ease-in-out;
}

.btn-edit {
  background-color: #FFC107;
  color: #333;
}

.btn-delete {
  background-color: #c3382f;
  color: white;   
}

.btn-edit:hover{
  transform: translateY(-3px);
  background-color: #ffe100;
}

.btn-delete:hover{
  transform: translateY(-3px);
  background-color: #cf0000;
}

/*Estilos del contenedor de ingredientes */
.ingredientes-grid{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
  overflow-y: auto;
}

.ingrediente-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.ingrediente-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.ingrediente-imagen {
  height: 120px;
  overflow: hidden;
}

.ingrediente-imagen img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.ingrediente-card:hover .ingrediente-imagen img {
  transform: scale(1.05);
}

.ingrediente-info {
  padding: 0.8rem;
}

.ingrediente-info h4 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}

.ingrediente-info p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
}

.btn-agregar-ingrediente {
  width: 100%;
  padding: 0.6rem;
  background-color: #ffd700;
  color: white;
  border: none;
  cursor: pointer;
  transition: transform ease-in-out 0.3s;
}

.btn-agregar-ingrediente:hover {
  background-color: #cf9b00;
  transform: scale(1.1);
}

.no-results {
  padding: 2rem;
  text-align: center;
  color: #666;
  font-style: italic;
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

/* Modal de cantidad */
.modal-header h3{
  font-family: 'Jura', sans-serif;
  text-align: center;
}

.cantidad-modal-overlay {
  position: fixed;
  width: 110%;
  height: 110%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(3px);
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: -130px;
  margin-left: -40px;
  z-index: 1200;
}

.cantidad-modal {
  background-color: rgb(0, 0, 0);
  border-radius: 8px;
  width: 450px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  border: solid 1px #fff;
  margin-left: -63px;
}

.cantidad-modal input{
  width: 374px;
}

.cantidad-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.cantidad-input, .unidad-select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
}
.btn-cancelar {
  padding: 0.6rem 1.2rem;
  background-color: #ff0000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Jura', sans-serif;
  transition: transform 0.2s ease-in-out;
}
.btn-confirmar {
  font-family: 'Jura', sans-serif;
  padding: 0.6rem 1.2rem;
  background-color: #FFC107;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: transform 0.2s ease-in-out;
}

.btn-cancelar:hover,.btn-confirmar:hover{
  transform: scale(1.1);
}

/*Animacion para expandir el contenedor */
.fade-expand-enter-active, .fade-expand-leave-active {
  transition: max-height 2s ease-out, opacity 1s ease-in-out;
  overflow: hidden;
}

.fade-expand-enter-from, .fade-expand-leave-to {
  max-height: 0;
  opacity: o;
}

.fade-expand-enter-to, .fade-expand-leave-from {
  max-height: 250px;
  opacity: 1;
}


.fade2-enter-active, .fade2-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade2-enter-from, .fade2-leave-to {
  opacity: 0;
  transform: scale(0.9); /* Efecto de zoom al aparecer */
  
}

.fade2-leave-to{
  transform: translateY(-50px);
}

.ingrediente{
  margin-left: 38px;
}
.cantidad{
  margin-left: 53px;
  width: 100px;
}
.unidad{
  margin-left: 65px;
}
</style>