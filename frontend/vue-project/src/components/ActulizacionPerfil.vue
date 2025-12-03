<script setup lang="ts">
import { ref, onMounted} from 'vue';
import axios from 'axios';
import Swal from 'sweetalert2';
import { getCurrentUser } from '@/servicies/auths';
import { defineEmits } from 'vue';


const user = ref({
  id: null,
  nombre: '',
  rol: '',
  subrol: '',
  correo: '',
  telefono: null,
  documento: null,
  ruta_imagen: null,
  contraseña: "",
});

const isEditing = ref(false);
const editedUser = ref({});
const imagePreview = ref(null);
const isHovering = ref(false);

onMounted(async () => {
  const localData = JSON.parse(localStorage.getItem("userData") || '{}');
  
  // Añadir timestamp si existe imagen
  if(localData.ruta_imagen && !localData.ruta_imagen.includes("?t=")) {
    localData.ruta_imagen = `${localData.ruta_imagen}?t=${new Date().getTime()}`;
  }
  
  user.value = localData;
  
  // Actualizar con datos frescos del servidor
  const freshData = await getCurrentUser();
  if(freshData) {
    // Mantener timestamp local si existe
    user.value.ruta_imagen = localData.ruta_imagen || freshData.ruta_imagen
    }
});

const startEditing = () => {
  editedUser.value = { ...user.value };
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
};


const handleImageHover = (hover) => {
  isHovering.value = hover;
};

const triggerFileInput = () => {
  const fileInput = document.getElementById('profile-image-input');
  if (fileInput) {
    fileInput.click();
  }
};


const updateProfile = async () => {
  try {

    const payload = {
      ...editedUser.value,
      id: user.value.id
    }

    const response = await axios.patch(
      `https://coffebikefastapi-production.up.railway.app/usuarios/${user.value.id}`, 
      payload
    );

     // Conservar la ruta de la imagen si no está en la respuesta
     user.value = { 
      ...user.value,  // Mantener los datos actuales
      ...response.data, // Sobrescribir con los nuevos datos
      ruta_imagen: user.value.ruta_imagen
    };

    localStorage.setItem('userData', JSON.stringify(user.value));

    Swal.fire({
      icon: 'success',
      title: 'Perfil Actualizado',
      text: 'Su información se ha actualizado exitosamente'
    });

    isEditing.value = false;
  } catch (error) {
    console.error('Error actualizando perfil:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'No se pudo actualizar el perfil'
    });
  }
};


const handleImageUpload = async (event) => {
  const file = event.target.files[0];
  if (file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(
        `https://coffebikefastapi-production.up.railway.app/usuarios/imagen/${user.value.id}`, 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      // Añadir timestamp una sola vez
      const newImageUrl = `${response.data.ruta_imagen}?t=${new Date().getTime()}`;
      
      // Actualizar reactividad correctamente
      user.value.ruta_imagen = newImageUrl
      
      // Vista previa inmediata
      imagePreview.value = URL.createObjectURL(file);
      
      // Guardar en localStorage CON timestamp
      const userData = JSON.parse(localStorage.getItem('userData') || '{}');
      userData.ruta_imagen = newImageUrl; 
      localStorage.setItem('userData', JSON.stringify(userData));

      Swal.fire('Éxito', 'Imagen actualizada', 'success');
      
    } catch (error) {
      console.error('Error:', error);
      Swal.fire('Error', 'No se pudo actualizar', 'error');
    }
  }
};

const emit = defineEmits(["close"]);
const closeModal = () => {
  emit("close")
};


</script>

<template>
  <div class="modal-overlay">
    <div class="modal-content">
        <div class="perfil-container">
        <div class="perfil-header">
      <button @click="closeModal" class="close-btn">X</button>
          <h1>Mi Perfil</h1>
        </div>
        <div class="perfil-content">
          <div class="profile-image-container">
          <!-- Input oculto para la carga de imagen -->
          <input 
            type="file" 
            id="profile-image-input"
            accept="image/jpeg,image/png,image/gif"
            style="display: none;"
            @change="handleImageUpload"
          />
            <!-- Contenedor de la imagen con efecto hover -->
            <div 
              class="profile-image-wrapper"
              @mouseenter="handleImageHover(true)"
              @mouseleave="handleImageHover(false)"
              @click="triggerFileInput"
            >
              <img 
                :src="user.ruta_imagen"
                alt="Foto de perfil" 
                class="profile-image"
              />
              <!-- Overlay de cambio de imagen -->
              <div 
                class="image-overlay" 
                :class="{ 'visible': isHovering }"
              >
                <div class="overlay-content">
                  <i class="fas fa-camera"></i>
                  <span>Cambiar Imagen</span>
                </div>
              </div>
            </div>
          </div>
          <div class="perfil-informacion">
            <template v-if="!isEditing">
              <div class="info-item">
                <strong>Nombre:</strong> {{ user.nombre }}
              </div>
              <div class="info-item">
                <strong>Rol:</strong> {{ user.rol }}
              </div>
              <div class="info-item" v-if="user.subrol">
                <strong>Sub-Rol:</strong> {{ user.subrol }}
              </div>
              <div class="info-item">
                <strong>Correo:</strong> {{ user.correo }}
              </div>
              <div class="info-item">
                <strong>Teléfono:</strong> {{ user.telefono || 'No registrado' }}
              </div>
              <div class="info-item">
                <strong>Documento:</strong> {{ user.documento || 'No registrado' }}
              </div>
            </template>
            
            <template v-else>
              <div class="form-group">
                <label>Nombre</label>
                <input 
                  id="nombre"
                  v-model="editedUser.nombre" 
                  type="text" 
                  placeholder="Nombre"
                />
              </div>
              <div class="form-group">
                <label>Correo</label>
                <input 
                  v-model="editedUser.correo" 
                  type="email" 
                  placeholder="Correo electrónico"
                />
              </div>
              <div class="form-group">
                <label>Teléfono</label>
                <input 
                  id="telefono"
                  v-model="editedUser.telefono" 
                  type="number" 
                  placeholder="Teléfono"
                />
              </div>
            </template>
            
            <div class="perfil-acciones">
              <template v-if="!isEditing">
                <button 
                  @click="startEditing" 
                  class="btn-editar"
                >
                  Editar Perfil
                </button>
              </template>
              <template v-else>
                <button 
                  @click="updateProfile" 
                  class="btn-guardar"
                >
                  Guardar Cambios
                </button>
                <button 
                  @click="cancelEditing" 
                  class="btn-cancelar"
                >
                  Cancelar
                </button>
              </template>
            </div>
          </div>
        </div>
        
        
      </div>
    </div>
  </div>
  
</template>

<style scoped>
.profile-image-container {
  position: relative;
  width: 250px;
  height: 250px;
  margin: 0 auto;
}

.profile-image-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
  border-radius: 50%;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.profile-image-wrapper:hover {
  transform: scale(1.05);
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: all 0.3s ease;
  border-radius: 50%;
}

.image-overlay.visible {
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 1;
}

.overlay-content {
  text-align: center;
  color: white;
}

.overlay-content i {
  font-size: 2rem;
  margin-bottom: 10px;
}

.overlay-content span {
  display: block;
  font-size: 1rem;
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
  z-index: 999;
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
.perfil-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #000000;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.perfil-header {
  text-align: center;
  margin-bottom: 30px;
}
.perfil-content {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}
.perfil-imagen {
  flex: 0 0 250px;
}
.perfil-imagen img {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border-radius: 50%;
  border: 4px solid #4a4a4a;
}
.perfil-informacion {
  flex: 1;
}
.info-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #000000;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group input {
  width: 90%;
  padding: 10px;
  border: 1px solid #000000;
  background-color: #ffc30e;
  border-radius: 5px;
}
.perfil-acciones {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}
.btn-editar, .btn-guardar, .btn-cancelar {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.btn-editar {
  background-color: #D9AB23;
  color: black;
  transition: all 0.3s ease-in-out;

}
.btn-guardar {
  background-color: #D9AB23;
  color: rgb(255, 255, 255);
  transition: all 0.3s ease-in-out;

}
.btn-cancelar {
  background-color: #ff1100;
  color: black;
  transition: all 0.3s ease-in-out;
}

.btn-editar:hover {
  background-color: #eeb91b;
  color: black;
  transform: scale(1.01) translateY(-5px);

}
.btn-guardar:hover {
  background-color: #a88210;
  color: rgb(255, 255, 255);
  transform: scale(1.01) translateY(-5px);

}
.btn-cancelar:hover {
  background-color: #c5180c;
  color: black;
  transform: scale(1.01) translateY(-5px);
}

.close-btn {
  background-color: transparent;
  color: rgb(255, 0, 0);
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  width: 60px;
  margin-left: 660px;
  margin-top: 23px;
  transition: all 0.3s ease-in-out;
}

.close-btn:hover {
  background-color: darkred;
  transform: scale(1.1);
}

.perfil-adicional {
  background-color: black;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.tarjetas-info {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.tarjeta {
  flex: 1;
  text-align: center;
  padding: 20px;
  background-color: black;
  border-radius: 10px;
}

.tarjeta i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: #4a4a4a;
}
</style>