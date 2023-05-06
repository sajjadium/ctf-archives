import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Logout from '../views/Logout.vue'
import Chat from '../views/Chat.vue'
import Users from '../views/Users.vue'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
  {
    path: '/users',
    name: 'Users',
    component: Users
  },
  {
    path: '/chat/:username',
    name: 'Chat',
    component: Chat
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (!['Home', 'Login'].includes(to.name) && !store.state.username) next({ name: 'Login' })
  else if (['Home', 'Login'].includes(to.name) && store.state.username) next({ name: 'Users' })
  else next()
})

export default router
