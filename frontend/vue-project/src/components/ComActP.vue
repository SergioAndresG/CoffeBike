<script setup lang="ts">
import { computed, ref, watch } from "vue";
import axios from "axios";
import Swal from "sweetalert2";  
import { defineEmits } from 'vue';
const emit = defineEmits(['close']);

// Variable para guardar los datos de la busqueda
const searchTerm = ref("")
const productos = ref([]);
const ActModal = ref(false);
// Con la palabra any le indicamos que puede guardar un dato de cualquier tipo, en este caso de tipo del objeto producto
const productoSeleccionado = ref<any>(null);
const categorias = ref([]);
const tipos = ref(["HECHO", "COMPRADO"]);
const materiasPrimas = ref([]);
const unidadesMedida = ref([]);

const formData = ref({
  id: null,
  nombre: "",
  categoria: "",
  tipo: "COMPRADO", // Valor por defecto
  precio: null,
  cantidad: 0,
  stock_minimo: 0,
  idUsuarioR: 0,
  ingredientes: [] as Array<{
    materia_prima_id: number,
    cantidad_ingrediente: number,
    unidad_id: number | null,
    nombre_materia_prima?: string
  }>
});

// estado para rastrear que se ha modificado
const camposModificados = ref({
  id: false,
  nombre: false,
  categoria: false,
  tipo: false,
  precio: false,
  cantidad: false,
  stock_minimo: false,
  idUsuarioR: false,
  ingredientes: false
})

// Computed property para mostrar solo si es producto hecho
const mostrarReceta = computed(() => {
  return formData.value.tipo === "HECHO";
});

const cargarCategorias = async () => {
  try {
    const respuesta = await axios.get("http://127.0.0.1:8000/productos/categorias")
    categorias.value = respuesta.data
  } catch (error) {
    console.error("Error al cargar los categorías", error)
  }
}

const cargarMateriasPrimas = async () => {
  try {
    const respuesta = await axios.get("http://127.0.0.1:8000/materia");
    materiasPrimas.value = respuesta.data
  } catch (error) {
    console.error("Error al cargar las materias primas", error)
  }
}

const cargarUnidadesMedida = async () => {
  try {
    const respuesta = await axios.get("http://127.0.0.1:8000/materia/unidades-medida");
    unidadesMedida.value = respuesta.data
  } catch (error) {
    console.error("Error al cargar las unidades de medida", error)
  }
}

cargarCategorias();
cargarMateriasPrimas();
cargarUnidadesMedida();

const cargarProductos = async () => {
  try {
    const respuesta = await axios.get("http://127.0.0.1:8000/productos");
      productos.value = respuesta.data
  } catch (error) {
    console.error("Error al cargar los productos", error)
  }
}

// Función para cargar los ingredientes de un producto
const cargarIngredientes = async (productoId) => {
  try {
    const respuesta = await axios.get(`http://127.0.0.1:8000/productos/${productoId}/receta`);
    return respuesta.data;
  } catch (error) {
    console.error("Error al cargar la receta del producto", error);
    return [];
  }
}

// Función para filtrar los productos por términos de búsqueda
// Definimos la función computed para que se actualice cuando haya un cambio
const filtrarProductos = computed(() => {
  // Si el campo está vacío devuelve los productos sin ningún cambio
  if(!searchTerm.value.trim()) return productos.value
  // Obtenemos el valor lo parseamos a minúsculas y le quitamos los espacios (trim())
  const term = searchTerm.value.toLowerCase().trim()
  // Filtramos los productos que cumplan con el término de búsqueda
  // por cada producto tomamos su nombre, se pasa a minúsculas y si incluye el término de búsqueda lo dejamos si no, lo descartamos
  return productos.value.filter(pro => pro.nombre.toLowerCase().includes(term))
});

cargarProductos();

const handleInputChange = async (campo: string) => {
  camposModificados.value[campo] = true
}

// Agregar un ingrediente a la receta
const agregarIngrediente = () => {
  formData.value.ingredientes.push({
    materia_prima_id: null,
    cantidad_ingrediente: 0,
    unidad_id: null
  });
  camposModificados.value.ingredientes = true;
}

// Eliminar un ingrediente de la receta
const eliminarIngrediente = (index) => {
  formData.value.ingredientes.splice(index, 1);
  camposModificados.value.ingredientes = true;
}

// Manejar cambios en los ingredientes
const handleIngredienteChange = () => {
  camposModificados.value.ingredientes = true;
}

const handleSubmit = async () => {
  try {
    const camposActualizados: any = {};
    for (const campo in camposModificados.value) {
      if (camposModificados.value[campo]) {
        switch(campo) {
          case 'precio':
            camposActualizados['precio_unitario'] = Number(formData.value.precio.toFixed(2));
            break;
          case 'categoria':
            camposActualizados['categoria'] = formData.value.categoria;
            break;
          case 'tipo':
            camposActualizados['tipo'] = formData.value.tipo;
            break;
          case 'idUsuarioR':
            camposActualizados['id_usuario'] = formData.value.idUsuarioR;
            break;
          case 'ingredientes':
            if (formData.value.tipo === "HECHO") {
              camposActualizados['ingredientes'] = formData.value.ingredientes.map(ing => ({
                materia_prima_id: ing.materia_prima_id,
                cantidad_ingrediente: ing.cantidad_ingrediente,
                unidad_id: ing.unidad_id
              }));
            }
            break;
          default:
            camposActualizados[campo] = formData.value[campo];
        }
      }
    }

    console.log('Payload being sent:', camposActualizados);

    if (Object.keys(camposActualizados).length > 0) {
      const response = await axios.patch(
        `http://127.0.0.1:8000/productos/${formData.value.id}`, 
        camposActualizados
      );

      Swal.fire({
          icon: "success",
          title: "Éxito",
          text: "Producto actualizado exitosamente",
        });

      closeModal();
      cargarProductos();
    } else {
      Swal.fire({
        icon:"info",
        title:"Información",
        text:"No se han realizado cambios"
      })
    }
  } catch (error: any) {
    console.error("Full error:", error);
    console.error("Error response:", error.response?.data);
    
    Swal.fire({
      icon: "error",
      title: "Error al actualizar el producto",
      text: error.response?.data?.detail || "Hubo un problema al actualizar el producto.",
    });
  }
};

const openActModal = async (producto: any) => {
  formData.value = {
    id: producto.id,
    nombre: producto.nombre || "",
    categoria: producto.categoria || "",
    tipo: producto.tipo || "COMPRADO",
    precio: producto.precio_unitario || null,
    cantidad: producto.cantidad || null,
    stock_minimo: producto.stock_minimo || null,
    idUsuarioR: producto.id_usuario,
    ingredientes: []
  };

  // Si es un producto HECHO, cargar los ingredientes
  if (producto.tipo === "HECHO") {
    try {
      const ingredientes = await cargarIngredientes(producto.id);
      formData.value.ingredientes = ingredientes.map(ing => ({
        materia_prima_id: ing.materia_prima_id,
        cantidad_ingrediente: ing.cantidad_ingrediente,
        unidad_id: ing.unidad_id,
        nombre_materia_prima: ing.materia_prima?.nombre || "Desconocido"
      }));
    } catch (error) {
      console.error("Error al cargar ingredientes", error);
    }
  }

  for(const campo in camposModificados.value) {
    camposModificados.value[campo] = false;
  }

  productoSeleccionado.value = producto;
  ActModal.value = true;
} 

const closeActModal = () => {
  ActModal.value = false;
} 

const closeModal = () => {
  emit('close');  // Emitir el evento para cerrar el modal
};

// Obtener el nombre de la materia prima por ID
const getNombreMateriaPrima = (id) => {
  const materiaPrima = materiasPrimas.value.find(mp => mp.id === id);
  return materiaPrima ? materiaPrima.nombre : "Desconocido";
}

// Obtener el nombre de la unidad por ID
const getNombreUnidad = (id) => {
  const unidad = unidadesMedida.value.find(u => u.id === id);
  return unidad ? unidad.nombre : "Unidad por defecto";
}

// Observar cambios en el tipo
watch(() => formData.value.tipo, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    handleInputChange('tipo');
    // Si cambiamos de HECHO a otra tipo, podemos limpiar los ingredientes
    if (newValue !== "HECHO") {
      formData.value.ingredientes = [];
    }
  }
});
</script>

<template>
  <div class="modal-overlay">
    <div class="modal-content" @click.stop>
      <!-- Formulario u otro contenido aquí -->
      <button @click="closeModal" class="close-btn3">X</button>
      <h1>Seleccione el producto a Actualizar</h1>
      <div class="search-container">
          <input type="text" v-model="searchTerm" placeholder="Buscar Producto..." class="search-input">
      </div>
      <div class="productos-grid">
        <div v-for="productos in filtrarProductos" :key="productos.id" class="productos-card">
          <div class="productos-imagen">
            <img v-if="productos.ruta_imagen" :src="`http://127.0.0.1:8000/productos/${productos.ruta_imagen}`" />
          </div>
          <div class="productos-info">
            <h4>{{ productos.nombre }}</h4>
            <p v-if="productos.cantidad">Stock: {{ productos.cantidad }}</p>
            <p><strong>Categoría:</strong> {{ productos.categoria }}</p>
            <p><strong>Tipo:</strong> {{ productos.tipo }}</p>
          </div>
        
          <button 
            @click="openActModal(productos)"
            class="btn-agregar-productos">Actualizar
          </button>
        </div>
      </div>

      <div v-if="filtrarProductos.length === 0" class="no-results">
        No se encontraron resultados con la búsqueda
      </div>

      <div class="modal-footer">
        <button @click="closeModal" class="btn-finalizar">Finalizar</button>
      </div>
    </div>

    <div class="modal-overlay" v-if="ActModal">
      <div class="form-container">
        <button @click="closeActModal" class="close-btn4">X</button>
      <h1>Ingrese los datos a Actualizar</h1>

        <form @submit.prevent="handleSubmit">
          <label for="id">ID del Producto:</label>
            <input
              type="number"
              id="id"
              v-model="formData.id"
              disabled
            />
          <label for="nombre">Nombre:</label>
          <input type="text" id="nombre" v-model="formData.nombre" placeholder="Ingrese el nombre del producto" @input="handleInputChange('nombre')"/>

          <label for="categoria">Categoría:</label>
          <select id="categoria" v-model="formData.categoria" @change="handleInputChange('categoria')">
            <option disabled value="">Seleccione una Categoría</option>
            <option v-for="categoria in categorias" :key="categoria" :value="categoria">
              {{ categoria }}
            </option>
          </select>
          
          <label for="tipo">Tipo:</label>
          <select id="tipo" v-model="formData.tipo" @change="handleInputChange('tipo')">
            <option v-for="tipo in tipos" :key="tipo" :value="tipo">
              {{ tipo }}
            </option>
          </select>
          
          <label for="precio">Precio:</label>
          <input type="number" id="precio" v-model="formData.precio" step="0.01" placeholder="Ingrese el precio" 
            @input="handleInputChange('precio')"
          />

          <label for="cantidad">Cantidad:</label>
          <input type="number" id="cantidad" v-model.number="formData.cantidad" placeholder="Ingrese la cantidad" @input="handleInputChange('cantidad')"/>

          <label for="stock_minimo">Cantidad mínimo de stock:</label>
          <input type="text" id="stock_minimo" v-model="formData.stock_minimo" placeholder="Ingrese el stock mínimo" @input="handleInputChange('stock_minimo')"/>

          <label for="id_usuario">ID Usuario:</label>
          <input type="number" id="id_usuario" v-model="formData.idUsuarioR" placeholder="Ingrese el ID del usuario que Actualiza" disabled/>

          <!-- Sección de ingredientes para productos HECHO -->
          <div v-if="mostrarReceta" class="ingredientes-seccion">
            <h3>Ingredientes de la Receta</h3>
            
            <div v-for="(ingrediente, index) in formData.ingredientes" :key="index" class="ingrediente-item">
              <div class="ingrediente-row">
                <label>Materia Prima:</label>
                <select 
                  v-model="ingrediente.materia_prima_id" 
                  @change="handleIngredienteChange"
                  class="ingrediente-select"
                >
                  <option value="">Seleccione una materia prima</option>
                  <option v-for="mp in materiasPrimas" :key="mp.id" :value="mp.id">
                    {{ mp.nombre }}
                  </option>
                </select>
                
                <label>Cantidad:</label>
                <input 
                  type="number" 
                  v-model.number="ingrediente.cantidad_ingrediente" 
                  @input="handleIngredienteChange"
                  step="0.01"
                  min="0"
                  class="ingrediente-input"
                />
                
                <label>Unidad:</label>
                <select 
                  v-model="ingrediente.unidad_id" 
                  @change="handleIngredienteChange"
                  class="ingrediente-select"
                >
                  <option :value="null">Usar unidad de materia prima</option>
                  <option v-for="um in unidadesMedida" :key="um.id" :value="um.id">
                    {{ um.nombre }} ({{ um.simbolo }})
                  </option>
                </select>
                
                <button 
                  type="button" 
                  @click="eliminarIngrediente(index)"
                  class="btn-eliminar-ingrediente"
                >
                  Eliminar
                </button>
              </div>
            </div>
            
            <button 
              type="button" 
              @click="agregarIngrediente"
              class="btn-agregar-ingrediente"
            >
              Agregar Ingrediente
            </button>
          </div>

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
.ingredientes-seccion {
  font-family: 'Jura', sans-serif;
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  background-color: #000000;
}
.ingrediente-item {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #ccc;
}

.ingrediente-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 10px;
  align-items: center;
}
.ingrediente-select, .ingrediente-input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 90%;
}

.btn-eliminar-ingrediente {
  background-color: #ff5252;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 5px;
  transition: all 0.1s ease-in-out;
}
.btn-agregar-ingrediente {
  background-color: #faad14;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
  transition: all 0.1s ease-in-out;
}

.btn-eliminar-ingrediente:hover{
  transform: translateY(-3px) ;
  background-color: #c53436;

}
.btn-agregar-ingrediente:hover{
  transform: translateY(-3px);
  background-color: #A65814;
}

/* Estilo del formulario */
.form-container {
  background-color: #000000; /* Fondo negro */
  padding: 15px;
  width: 700px;
  height: auto;
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
  overflow-y: auto; /* Activa el scroll vertical */
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