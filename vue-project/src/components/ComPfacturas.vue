<script>
import axios from 'axios';
import lottie from 'lottie-web';

export default {
  data() {
    return {
      animation: null,
      showMateriaPrimaPanel: false,
      showClientesPanel: false,
      facturasClientes: [],
      fechaBusqueda: null,
      mensajeError: ''  
    };
  },


  mounted() {
    this.loadLottieAnimation();
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
    document.head.appendChild(link);
    
    // Llamar al endpoint de facturas cuando se monta el componente
    this.fetchFacturasClientes();
  },

  methods: {
    loadLottieAnimation() {
      this.animation = lottie.loadAnimation({
        container: this.$refs.lottieContainer,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: 'https://lottie.host/dbd92ec6-d27a-461e-98ee-2fc39e3a5342/zft6pQtYyC.json'
      });
    },

    async exportarExcel() {
      try {
        const response = await axios.get('http://localhost:8000/exportar_excel/', {
          responseType: 'blob'
        });

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'reporte_inventario.xlsx');
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error('Error al exportar el Excel:', error);
      }
    },

    async fetchFacturasClientes() {
      try {
        const response = await axios.get("http://localhost:8000/facturas/");
        
        if (response.data && response.data.data) {
          this.facturasClientes = response.data.data.map(factura => ({
            idFactura: factura.id || 'N/A',
            fecha: factura.fecha_compra ? new Date(factura.fecha_compra).toLocaleDateString() : 'Sin fecha',
            cliente: factura.cliente?.nombre || 'Cliente no especificado',
            idCliente: factura.cliente?.id || 'N/A',
            total: `$${(factura.precio_total || 0).toFixed(2)}`,
            productos: Array.isArray(factura.productos) ? factura.productos.map(p => ({
              nombre: p.nombre || 'Producto sin nombre',
              cantidad: p.cantidad || 0,
              precio: `$${(p.precio_unitario || 0).toFixed(2)}`,
              subtotal: `$${(p.subtotal || 0).toFixed(2)}`
            })) : []
          }));
        } else {
          this.mensajeError = "Formato de respuesta inesperado";
        }
      } catch (error) {
        console.error('Error completo:', error);
        if (error.response) {
          console.error('Datos del error:', error.response.data);
          this.mensajeError = error.response.data?.detail || 
                            error.response.data?.message || 
                            "Error en el servidor";
        } else {
          this.mensajeError = "Error de conexión con el servidor";
        }
        this.facturasClientes = [];
      }
    },

      toggleMateriaPrimaPanel() {
        this.showMateriaPrimaPanel = !this.showMateriaPrimaPanel;
        if (this.showClientesPanel && this.showMateriaPrimaPanel) {
          this.showClientesPanel = false;
        }
      },

      toggleClientesPanel() {
        this.showClientesPanel = !this.showClientesPanel;
        if (this.showMateriaPrimaPanel && this.showClientesPanel) {
          this.showMateriaPrimaPanel = false;
        }
      },
    async buscarFacturasPorFecha() {
      this.mensajeError = ''; // Reiniciar mensaje de error

      if (!this.fechaBusqueda) {
        this.mensajeError = 'Por favor selecciona una fecha.';
        this.facturasClientes = [];
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:8000/facturas/por-fecha`, {
          params: { fecha: this.fechaBusqueda }
        });

        if (response.data && Array.isArray(response.data) && response.data.length > 0) {
          this.facturasClientes = response.data.map(factura => ({
            idCliente: factura.cliente?.id || 'N/A',
            fecha: new Date(factura.fecha_compra).toLocaleDateString(),
            cliente: factura.cliente?.nombre || 'Cliente desconocido',
            total: `$${factura.precio_total?.toFixed(2) || '0.00'}`,
            idFactura: factura.id || 'N/A'
          }));
        } else {
          this.facturasClientes = [];
          this.mensajeError = 'Factura no encontrada.';
        }
      } catch (error) {
        console.error('Error al buscar facturas por fecha:', error.response?.data || error.message);
        this.facturasClientes = [];
        this.mensajeError = 'Factura no encontrada.';
      }
    }
  },

  beforeDestroy() {
    if (this.animation) {
      this.animation.destroy();
    }
  }
};
</script>

<template>
  <header>
    <nav>
      <img src="https://i.postimg.cc/QMwjX2vk/Whats-App-Image-2024-11-23-at-10-53-04-PM.jpg" class="imagen" alt="logo">
    </nav>
    <hr>
    <hr class="linea2">
    <h1 class="titulo">Panel Facturas</h1>
    
    <div class="menu-container">
      <ul class="menu-amarillo">
        <li @click="toggleClientesPanel" :class="{ activo: showClientesPanel }">
          <span class="icon"><i class="fas fa-users"></i></span>
          <span>Facturas clientes</span>
        </li>  
        <div ref="lottieContainer" class="lottie-animation"></div>    
      </ul>
      
      <div class="panel-negro" v-if="showClientesPanel">
        <h3><i class="fas fa-file-invoice" style="margin-right: 10px;"></i>Facturas de Clientes</h3>
        <div class="panel-content">
          <div class="form-group">
            <label>Buscar Factura por Fecha</label>
            <div style="display: flex; align-items: center; gap: 10px;">
              <input type="date" v-model="fechaBusqueda" class="fecha-input">
              <button @click="buscarFacturasPorFecha" class="buscar-btn">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </div>

          
          <div class="facturas-table">
            <div class="table-header">
              <div class="header-item">ID Cliente</div>
              <div class="header-item">Fecha</div>
              <div class="header-item">Cliente</div>
              <div class="header-item">Total</div>
              <div class="header-item">ID Factura</div>
              <p v-if="mensajeError" class="mensaje-error">{{ mensajeError }}</p>

            </div>
            
            <div class="table-row" v-for="(factura, index) in facturasClientes" :key="index">
              <div class="row-item">{{ factura.idCliente }}</div>
              <div class="row-item">{{ factura.fecha }}</div>
              <div class="row-item">{{ factura.cliente }}</div>
              <div class="row-item">{{ factura.total }}</div>
              <div class="row-item">{{ factura.idFactura }}</div>
            </div>
          </div>
          
          <div class="action-buttons">
            <button class="btn btn-gold" @click="exportarExcel">
              <i class="fas fa-file-import"></i> Exportar Excel
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jura:wght@700&display=swap');

body {
    font-family: 'Jura', sans-serif;
    font-weight: normal;
    color: black;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

header {
    padding: 20px;
    background-color: #000000;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}

.imagen {
    height: 100px;
    width: 140px; 
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #D9AB23;
}

hr {
    border-top: 2px solid #D9AB23;
    margin: 20px auto;
    width: 90%;
}
.linea2 {
    border-top: 2px solid #D9AB23;
    margin: 20px auto;
    width: 80%;
    margin-top: -5px;
}

.titulo {
    font-family: 'Jura', sans-serif;
    color: #D9AB23;
    margin-top: 10px;
    font-size: 38px;
}

.menu-container {
    position: absolute;
    left: 172px;
    top: 280px; 
    display: flex;
}

.menu-amarillo {
    background-color: #A65814;
    border: 2px solid #f5f5f5;
    border-right: none;
    padding: 15px;
    list-style: none;
    margin: 0;
    padding-left: 15px;
    min-width: 280px;
    height: 400px;
    border-radius: 35px 0px 0px 35px;
}

.menu-amarillo li {
    padding: 10px 0;
    display: flex;
    align-items: center;
    font-family: 'Jura', sans-serif;
    font-weight: bold;
    font-size: 18px;
    text-align: center;
    margin-top: 20px;
    color: #ffffff;
    cursor: pointer;
    transition: all 0.3s ease;
}

.menu-amarillo li:hover {
    color: #000000;
    transform: translateX(5px);
    border-bottom: 2px solid #ffbf00;
    background-color: #753b0891;
}
.menu-amarillo li:active {
    color: #000000;
    transform: translateX(5px);
    border-bottom: 2px solid #ffbf00;
    background-color: #753b0891;
}

.icon {
    margin-right: 20px;
    font-size: 1.2em;
    width: 20px;
    text-align: center;
    color: #000;
}

.icon:hover {
    color: #ffbf00;
    transform: translateX(5px);
}

.lottie-animation {
  width: 230px;
  height: 230px;
  margin-left: 10px;
  margin-top: 10px;
}

.panel-negro {
  position: absolute;
  left: 100%; 
  top: 0;
  width: 900px;
  background-color: #000000;
  border: 2px solid #ffffff;
  border-left: none;
  border-radius: 0 35px 35px 0;
  padding: 20px;
  color: #D9AB23;
  font-family: 'Jura', sans-serif;
  z-index: 1;
  padding: 15px;
  height: 500px;
  max-height: 400px; 
  max-width: 900px;
  overflow-y: auto;
}

.panel-negro h3 {
  color: #D9AB23;
  border-bottom: 1px solid #D9AB23;
  padding-bottom: 10px;
  margin-bottom: 20px;
  text-align: center;
  font-size: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Jura', sans-serif;
}

.panel-content {
  padding: 15px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.form-group input {
  width: 98%;
  padding: 10px;
  background-color: #333;
  border: 1px solid #D9AB23;
  color: white;
  border-radius: 5px;
  font-family: 'Jura', sans-serif;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
  font-family: 'Jura', sans-serif;
}

.btn {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: -1000px;
  margin-left: 700px;
  height: 30px;

}

.btn-gold {
  background-color: #D9AB23;
  color: black;
  border: none;
  font-family: 'Jura', sans-serif;
}
.fecha-input {
  padding: 6px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.buscar-btn {
  background-color: #ffc107;
  border: none;
  border-radius: 5px;
  padding: 6px 10px;
  cursor: pointer;
  color: #333;
}

.buscar-btn i {
  font-size: 16px;
}

.mensaje-error {
  color: red;
  margin-top: 3px;
  font-weight: bold;
}


.facturas-table {
  margin-top: 20px;
  border: 1px solid #D9AB23;
  border-radius: 5px;
  overflow: hidden;
}

.table-header, .table-row {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr 1fr 0.5fr;
  align-items: center;
}

.table-header {
  background-color: #D9AB23;
  color: #000;
  font-weight: bold;
  padding: 10px 15px;
}

.table-row {
  padding: 10px 15px;
  border-bottom: 1px solid #333;
  color: #fff;
}

.table-row:last-child {
  border-bottom: none;
}

.row-item {
  padding: 5px 0;
}

.action-icon {
  cursor: pointer;
  color: #D9AB23;
  font-size: 1.2em;
  transition: all 0.3s ease;
}

.action-icon:hover {
  color: #fff;
  transform: scale(1.2);
}



</style>