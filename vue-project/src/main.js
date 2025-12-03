
import { createApp } from 'vue'
import App from './App.vue'
import router from './routers/misrutas';
import './assets/main.css'; 
import 'sweetalert2/dist/sweetalert2.min.css'; 
import '@fortawesome/fontawesome-free/css/all.css';



const app = createApp(App);

app.use(router)
.mount('#app')

