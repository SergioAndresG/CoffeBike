<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const email = ref('');
const isLoading = ref(false);
const message = ref('');
const messageType = ref<'info' | 'success' | 'error'>('info');

const requestReset = async () => {
  isLoading.value = true;
  message.value = '';

  try {
    const formData = new FormData();
    formData.append('email', email.value);

    const response = await axios.post('http://127.0.0.1:8000/reset-password-request', formData);
    message.value = response.data.message;
    messageType.value = 'success';
  } catch (error: any) {
    message.value =
      error.response?.data?.detail || 'Ha ocurrido un error. Inténtalo de nuevo.';
    messageType.value = 'error';
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
    <div class="reset-password-container">
      <h2>Recuperación de contraseña</h2>
      <p>Ingresa tu correo electrónico para recibir un enlace de recuperación.</p>
      
      <form @submit.prevent="requestReset">
        <div class="form-group">
          <label for="email">Correo electrónico</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required
            placeholder="tucorreo@ejemplo.com"
          >
        </div>
        
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Enviando...' : 'Enviar enlace de recuperación' }}
        </button>
        
        <div v-if="message" class="message" :class="messageType">
          {{ message }}
        </div>
      </form>
      
      <div class="links">
        <router-link to="/">Volver al inicio de sesión</router-link>
      </div>
    </div>
  </template>
  

  
  <style scoped>

    @import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');


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
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  
  input {
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
    background-color: #d4edda;
    color: #155724;
  }
  
  .error {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .info {
    background-color: #e2f3f8;
    color: #0c5460;
  }
  
  .links {
    margin-top: 15px;
    text-align: center;
  }
  
  a {
    
    color: #007bff;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  </style>