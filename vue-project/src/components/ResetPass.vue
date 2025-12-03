<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();

const token = ref<string>('');
const password = ref('');
const confirmPassword = ref('');
const isLoading = ref(false);
const message = ref('');
const messageType = ref<'info' | 'success' | 'error'>('info');
const tokenError = ref(false);
const tokenErrorMessage = ref('');
const resetSuccess = ref(false);

const passwordMismatch = computed(() => {
  return password.value && confirmPassword.value && password.value !== confirmPassword.value;
});

const validateToken = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/validate-reset-token', {
      token: token.value,
    });
  } catch (error: any) {
    tokenError.value = true;
    if (
      error.response?.status === 401 &&
      error.response?.data?.detail === 'Token expirado'
    ) {
      tokenErrorMessage.value =
        'El enlace de recuperación ha expirado. Por favor, solicita uno nuevo.';
    } else {
      tokenErrorMessage.value = 'El enlace de recuperación es inválido.';
    }
  }
};

const resetPassword = async () => {
  if (passwordMismatch.value || !password.value) {
    return;
  }

  isLoading.value = true;
  message.value = '';

  try {
    const response = await axios.post('http://127.0.0.1:8000/reset-password', {
      token: token.value,
      new_password: password.value,
    });

    message.value = response.data.message;
    messageType.value = 'success';
    resetSuccess.value = true;
  } catch (error: any) {
    message.value =
      error.response?.data?.detail || 'Ha ocurrido un error. Inténtalo de nuevo.';
    messageType.value = 'error';
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  token.value = route.query.token as string;

  if (!token.value) {
    tokenError.value = true;
    tokenErrorMessage.value = 'No se ha proporcionado un token de recuperación válido.';
  } else {
    validateToken();
  }
});
</script>

<template>
    <div class="reset-password-container">
      <h2>Establecer nueva contraseña</h2>
      
      <div v-if="tokenError">
        <p class="message error">{{ tokenErrorMessage }}</p>
        <div class="links">
          <router-link to="/reset-request">Solicitar un nuevo enlace</router-link>
        </div>
      </div>
      
      <form v-else @submit.prevent="resetPassword">
        <div class="form-group">
          <label for="password">Nueva contraseña</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
            placeholder="Ingresa tu nueva contraseña"
          >
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirmar contraseña</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            required
            placeholder="Confirma tu nueva contraseña"
          >
          <p v-if="passwordMismatch" class="error-text">Las contraseñas no coinciden</p>
        </div>
        
        <button type="submit" :disabled="isLoading || passwordMismatch || !password">
          {{ isLoading ? 'Actualizando...' : 'Establecer nueva contraseña' }}
        </button>
        
        <div v-if="message" class="message" :class="messageType">
          {{ message }}
        </div>
      </form>
      
      <div v-if="resetSuccess" class="links">
        <router-link to="/">Volver al inicio de sesión</router-link>
      </div>
    </div>
  </template>
  

  
  <style scoped>
  
  .reset-password-container {
    font-family: 'Jura', sans-serif;

    max-width: 400px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #000000;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    font-family: 'Jura', sans-serif;

    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
    font-family: 'Jura', sans-serif;

    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    font-family: 'Jura', sans-serif;

    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:disabled {
    background-color: #cccccc;
  }
  
  .message {
    margin-top: 15px;
    padding: 8px;
    border-radius: 4px;
  }
  
  .success {
    font-family: 'Jura', sans-serif;

    background-color: #d4edda;
    color: #155724;
  }
  
  .error {
    font-family: 'Jura', sans-serif;

    background-color: #f8d7da;
    color: #721c24;
  }
  
  .info {
    font-family: 'Jura', sans-serif;

    background-color: #e2f3f8;
    color: #0c5460;
  }
  
  .error-text {
    font-family: 'Jura', sans-serif;

    color: #721c24;
    font-size: 0.9em;
    margin-top: 5px;
  }
  
  .links {
    font-family: 'Jura', sans-serif;

    margin-top: 15px;
    text-align: center;
  }
  
  a {
    font-family: 'Jura', sans-serif;

    color: #007bff;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>