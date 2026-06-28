import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Tasks from '../views/Tasks.vue'
import Units from '../views/Units.vue'

const routes = [
    {
        path: '/',
        component: Home,
    },
    {
        path: '/tasks',
        component: Tasks,
    },
    {
        path: '/units',
        component: Units,
    },
]

export default createRouter({
    history: createWebHistory(),
    routes,
})
