import ComAdmi from "@/components/ComAdmi.vue";
import ComConsutUsu from "@/components/ComConsutUsu.vue";
import ComEmpleado from "@/components/ComEmpleado.vue";
import ComForAct from "@/components/ComForAct.vue";
import ComForAgregar from "@/components/ComForAgregar.vue";
import ComForDel from "@/components/ComForDel.vue";
import ComGest from "@/components/ComGest.vue";
import ComGestEmpleadoPr from "@/components/ComGestEmpleadoPr.vue";
import ComJefe from "@/components/ComJefe.vue";
import ComMateriaPrima from "@/components/ComMateriaPrima.vue";
import ComMenu from "@/components/ComMenu.vue";
import ComNostros from "@/components/ComNostros.vue";
import ComProductos from "@/components/ComProductos.vue";
import ComSesion from "@/components/ComSesion.vue";
import SnowFall from "@/components/SnowFall.vue";
import { createRouter, createWebHistory } from "vue-router";
import ActulizacionPerfil from "@/components/ActulizacionPerfil.vue";
import ComPCliente from "@/components/ComPCliente.vue";
import ComPedidos from "@/components/ComPedidos.vue";
import ComPfacturas from "@/components/ComPfacturas.vue";
import ComResetPass from "@/components/ComResetPass.vue";
import ResetPass from "@/components/ResetPass.vue";

const routes = [
    {
        path: "/Nosotros",
        name: "Nosotros",
        component: ComNostros
    },
    {
        path: "/",
        name:"Sesion",
        component: ComSesion
    },
    {
        path: "/Jefe",
        name: "Jefe",
        component: ComJefe
    },
    {
        path: "/Admi",
        name: "Admi",
        component: ComAdmi
    },
    {
        path: "/Empleado",
        name: "Empleado",
        component: ComEmpleado
    },
    {
        path: "/Productos",
        name: "Productos",
        component: ComProductos

    },
    {
        path: "/Gest",
        name: "Gest",
        component: ComGest
    },
    {
        path: "/AgregarU",
        name: "AgregarU",
        component: ComForAgregar
    },
    {
        path: "/Menu",
        name: "Menu",
        component: ComMenu
    },
    {
        path: "/EliminarU",
        name: "EliminarU",
        component: ComForDel

    },
    {
        path: "/Actualizar",
        name: "Actualizar",
        component: ComForAct
    },
    {
        path: "/Consultar",
        name: "Consultar",
        component: ComConsutUsu
    },
    {
        path: "/Materia",
        name: "Materia",
        component: ComMateriaPrima
    },
    {
        path: "/GPEmpleados",
        name: "GPEmpleados",
        component: ComGestEmpleadoPr
    },
    {
        path: "/Snowl",
        name: "Snowl",
        component: SnowFall
    },
    {
        path: "/ActualizarPerfil",
        name: "ActualizarPerfil",
        component: ActulizacionPerfil
    },
    {
        path:"/Clientes",
        name:"PedidoCliente",
        component: ComPCliente
    },
    {
        path:"/Pedidos",
        name:"Pedidos",
        component: ComPedidos
    },
    {
        path: "/Facturas",
        name:"Facturas",
        component:ComPfacturas
    },
    {
        path: "/AddNewStock",
        name:"NewStock",
        component:ComPfacturas
    },
    {
        path: "/ResetPass",
        name:"ResetPass",
        component:ComResetPass
    },
     {
        path: "/NewPass",
        name:"NewPass",
        component:ResetPass
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;