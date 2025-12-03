<script setup lang="ts">
import { ref, computed, reactive } from "vue";
import axios from "axios";
import Swal from "sweetalert2";

// Estado del formulario
const formData = ref({
  id: null, 
  nombre: "",
  rol: "",
  telefono: null,
  subrol: null,
  correo: "",
  contraseña: "",
  confirmarContraseña: "",
  documento: null,
});

//estado para rastrear que campos se han modificado
const camposModificados = ref({
  id: false, 
  nombre: false,
  rol: false,
  telefono: false,
  subrol: false,
  correo: false,
  contraseña: "",
  confirmarContraseña: false,
  documento: false,
})

const actModal = ref(false);
const searchTerm = ref("");
const empleados = ref([]);
const empleadoSeleccionado = ref<any>(null);


// Función para cargar empleados desde el backend
const cargarEmpleados = async () => {
  try {
    const respuesta = await axios.get("http://127.0.0.1:8000/usuarios");
    empleados.value = respuesta.data.map(empleado => ({
      ...empleado,
    }));
  } catch (error) {
    console.error("Error al cargar empleados:", error);
  }
};
cargarEmpleados();

const filtrarUsuarios = computed (()=> {
  if(!searchTerm.value.trim()) return empleados.value;

  const term =searchTerm.value.toLowerCase().trim()
  return empleados.value.filter(pro => 
    pro.nombre.toLowerCase().includes(term)
  )
});

//Funcion para manejar el cambio de los campos 
const handleInputChange = async (campo: string) => {
  camposModificados.value[campo] = true;
}
// Función para manejar el envío del formulario
const handleSubmit = async () => {
  // Validar contraseñas si se va a actualizar la contraseña
  if (camposModificados.value.contraseña) {
    if (formData.value.contraseña !== formData.value.confirmarContraseña) {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "Las contraseñas no coinciden",
      });
      return;
    }
  }

  try {
    // Crear un objeto solo con los campos modificados
    const camposActualizados = {};
    
    for (const campo in camposModificados.value) {
      if (camposModificados.value[campo]) {
        if (campo === 'documento') {
          camposActualizados[campo] = parseInt(formData.value[campo]);
        } else {
          camposActualizados[campo] = formData.value[campo];
        }
      }
    }

    // Solo enviar la solicitud si hay campos para actualizar
    if (Object.keys(camposActualizados).length > 0) {
      const response = await axios.patch(`http://127.0.0.1:8000/usuarios/${formData.value.id}`, camposActualizados);

      Swal.fire({
        icon: "success",
        title: "Éxito",
        text: "Usuario actualizado exitosamente",
      });

      console.log("Usuario actualizado con éxito:", response.data);
      closeActModal();
      cargarEmpleados(); // Recargar la lista de empleados
    } else {
      Swal.fire({
        icon: "info",
        title: "Información",
        text: "No se han realizado cambios",
      });
    }
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Error",
      text: "Hubo un error al actualizar el usuario",
    });
    console.error("Error al actualizar el usuario:", error);
  }
};


const openActModal = (empleado) => {
  // Cargar los datos del empleado seleccionado en el formulario
  formData.value = {
    id: empleado.id,
    nombre: empleado.nombre || "",
    rol: empleado.rol || "",
    subrol: empleado.subrol || null,
    correo: empleado.correo || "",
    contraseña: "",
    confirmarContraseña: "",
    documento: empleado.documento || null,
    telefono: empleado.telefono || null
  };
  
  // Resetear los campos modificados
  for (const campo in camposModificados.value) {
    camposModificados.value[campo] = false;
  }
  
  empleadoSeleccionado.value = empleado;
  actModal.value = true;
};

const closeActModal = () => {
  actModal.value = false;
}


// Emitir el evento 'close' para cerrar el modal
import { defineEmits } from "vue";
const emit = defineEmits(["close"]);

const closeModal = () => {
  emit("close");
};
</script>


<template>
  <div class="modal-overlay">
    <div class="modal-content" @click.stop>
      <button @click="closeModal" class="close-btn3">X</button>
      <h1>Seleccione el Trabajador a Actualizar</h1>
      <div class="search-container">
        <input type="text" v-model="searchTerm" placeholder="Buscar Usuarios..." class="search-input">
      </div>
      <div class="usuarios-grid">
        <div v-for="usuario in filtrarUsuarios" :key="usuario.id" class="usuarios-card">
          <div class="usuarios-imagen">
            <img v-if="usuario.ruta_imagen" :src="`http://127.0.0.1:8000/usuarios/${usuario.ruta_imagen}`" />
          </div>
          <div class="usuarios-info">
            <h4>{{ usuario.nombre }}</h4>
            <p v-if="usuario.telefono">Teléfono: {{ usuario.telefono }}</p>
          </div>
          
          <button 
            @click="openActModal(usuario)"
            class="btn-agregar-usuarios">Actualizar
          </button>
        </div>
      </div>
      <div class="modal-footer">
        <button @click="closeModal" class="btn-finalizar">Finalizar</button>
      </div>
      <div v-if="filtrarUsuarios.length === 0" class="no-results">
        No se encontraron resultados con la búsqueda
      </div>
    </div>
  </div>
    
  <div class="modal-overlay-2" v-if="actModal">
    <div class="modal-content-2" @click.stop>
      <h1>Actualizar Usuario</h1>
      <p class="instruccion">Solo modifique los campos que desea actualizar</p>
      <div class="form-container">
        <form @submit.prevent="handleSubmit">
          <!-- Campo para ID (deshabilitado para edición pero visible) -->
          <label for="id">ID del Usuario:</label>
          <input
            type="number"
            id="id"
            v-model="formData.id"
            disabled
          />
  
          <!-- Campo para Nombre -->
            <label for="nombre">Nombre:</label>
            <input
              type="text"
              id="nombre"
              v-model="formData.nombre"
              placeholder="Ingrese su nombre"
              @input="handleInputChange('nombre')"
            />
            <span class="campo-indicador" v-if="camposModificados.nombre">Campo modificado</span>
  
          <!-- Campo para Rol -->
            <label for="rol">Rol:</label>
            <select id="rol" v-model="formData.rol" @change="handleInputChange('rol')">
              <option disabled value="">Seleccione un rol</option>
              <option value="EMPLEADO">Empleado</option>
              <option value="JEFE">Jefe</option>

            </select>
            <span class="campo-indicador" v-if="camposModificados.rol">Campo modificado</span>
  
          <!-- Campo para Sub-Rol -->
            <label for="subrol">Sub-Rol:</label>
            <select id="subrol" v-model="formData.subrol" @change="handleInputChange('subrol')">
              <option disabled value="">Seleccione un sub-rol (opcional)</option>
              <option value="COSINERO">Cocinero</option>
              <option value="MESERO">Mesero</option>
              <option value="">Ninguno</option>
            </select>
            <span class="campo-indicador" v-if="camposModificados.subrol">Campo modificado</span>
  
          <!-- Campo para Correo -->
            <label for="correo">Correo:</label>
            <input
              type="email"
              id="correo"
              v-model="formData.correo"
              placeholder="Ingrese su correo"
              @input="handleInputChange('correo')"
            />
            <span class="campo-indicador" v-if="camposModificados.correo">Campo modificado</span>
  
          <!-- Campo para Teléfono -->
            <label for="telefono">Teléfono:</label>
            <input
              type="text"
              id="telefono"
              v-model="formData.telefono"
              placeholder="Ingrese su teléfono"
              @input="handleInputChange('telefono')"
            />
            <span class="campo-indicador" v-if="camposModificados.telefono">Campo modificado</span>
  
          <!-- Campo para Contraseña -->
            <label for="contraseña">Contraseña:</label>
            <input
              type="password"
              id="contraseña"
              v-model="formData.contraseña"
              placeholder="Ingrese nueva contraseña"
              @input="handleInputChange('contraseña')"
            />
            <span class="campo-indicador" v-if="camposModificados.contraseña">Campo modificado</span>
  
          <!-- Campo para Confirmar Contraseña (solo visible si la contraseña se ha modificado) -->
          <div class="campo-grupo" v-if="camposModificados.contraseña">
            <label for="confirmarContraseña">Confirmar Contraseña:</label>
            <input
              type="password"
              id="confirmarContraseña"
              v-model="formData.confirmarContraseña"
              placeholder="Confirme su contraseña"
            />
          </div>
  
          <!-- Campo para Documento -->
            <label for="documento">Documento:</label>
            <input
              type="number"
              id="documento"
              v-model="formData.documento"
              placeholder="Ingrese su documento"
              @input="handleInputChange('documento')"
            />
            <span class="campo-indicador" v-if="camposModificados.documento">Campo modificado</span>
  
          <!-- Botón para Actualizar -->
          <div class="botones-grupo">
            <button type="submit" class="btn-actualizar" >Actualizar Campos Modificados</button>
            <button type="button" @click="closeActModal" class="btn-cancelar">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
    <!-- Botón para Cerrar -->
    <button @click="closeActModal" class="close-btn">X</button>
  </div>
</template>
  

<style scoped>
.instruccion {
  color: #666;
  font-style: italic;
  margin-bottom: 15px;
  text-align: center;
}

.campo-grupo {
  margin-bottom: 15px;
  position: relative;
}

.campo-indicador {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 0.8em;
  color: #4CAF50;
  background-color: #f0f9f0;
  padding: 2px 8px;
  border-radius: 3px;
}

.botones-grupo {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn-actualizar {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancelar {
  background-color: #f44336;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

h1{
  font-family: 'Jura', sans-serif;
  font-size: 22px;
  text-align: center;
  color: #ffd700;
  margin-top: -10px;
}
  /* Estilo del formulario */
.form-container {
  background-color: #00000077; /* Fondo negro */
  padding: 15px;
  width: 600px;
  margin: 0 auto;
  border-radius: 8px;
  margin-top: -10px;
  overflow-y: auto;
}
.form-container select{
  font-family: 'Jura', sans-serif;
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
  padding: 10px;
}
label {
  color: #fff; /* Texto blanco */
  font-size: 12px;
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
.search-container{
  margin-left: 35%;
  margin-top: 33px;
}

.usuarios-grid{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1.5rem;
  overflow-y: auto;
}
.usuarios-card {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}
.usuarios-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}
.usuarios-imagen {
  height: 120px;
  overflow: hidden;
}
.usuarios-imagen img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.usuarios-card:hover .usuarios-imagen img {
  transform: scale(1.05);
}
.usuarios-info {
  padding: 0.8rem;
}
.usuarios-info h4 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}
.usuarios-info p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
}
.btn-agregar-usuarios {
  width: 100%;
  padding: 0.6rem;
  background-color: #000000;
  color: white;
  border: none;
  cursor: pointer;
  transition: transform ease-in-out 0.3s;
  font-family: 'Jura', sans-serif;
}
.btn-agregar-usuarios:hover {
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
  overflow-y: auto;
}
.modal-overlay-2 {
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
  overflow-y: auto;
}

.modal-content {
  font-family: 'Jura', sans-serif;
  position: fixed;
  left: 26%;
  width: 50%;
  height: 95%;
  background-color: rgb(0, 0, 0);
  margin-top: 10px;
  transition: all 0.3s ease;
  border: solid #cf9b00;
  border-radius: 5%;
  overflow-y: auto;
}

.modal-content-2 {
  background-color: black;
  margin-top: 83px;
  margin-left: -145px;
  padding: 20px;
  width: 80%;
  max-height: 800px;
  max-width: 800px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid;
  overflow-y: auto;
}

.close-btn {
  background-color: transparent;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 4px;
  margin-top: -620px;
  margin-right: -300px;
  width: 90px;
}

.close-btn:hover {
  background-color: darkred;
}


</style>