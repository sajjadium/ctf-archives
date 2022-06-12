import { createApp } from 'vue'
import App from './App.vue'
import { createRouter,createWebHistory} from 'vue-router'
import Messages from "@/Messages";
import Register from "@/Register";
import Search from "@/Search";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: "/", name:"index", component: Messages},
        {path: "/register", name: "register", component: Register},
        {path: "/search", name: "search", component: Search},
    ]
})
const app = createApp(App);
app.use(router)
app.mount('#app');

