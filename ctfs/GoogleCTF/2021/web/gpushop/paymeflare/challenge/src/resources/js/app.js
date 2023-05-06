require('./bootstrap');

window.Vue = require('vue').default;

import VueRouter from 'vue-router'
Vue.use(VueRouter)

import { LoaderPlugin } from 'vue-google-login';
Vue.use(LoaderPlugin, {
    client_id: client_id
});

import Home from './components/Home'
import App from './components/App'
import Account from './components/Account'
import Doc from './components/Doc'


 
const router = new VueRouter({
    mode: 'history',
    routes: [
        { path: '/', name: 'home', component: Home },
        { path: '/account', name: 'account', component: Account },
        { path: '/doc', name: 'doc', component: Doc },
    ],
});

const app = new Vue({
    el: '#app',
    components: {App},
    router,
    data: {
        login: false
    }
});
