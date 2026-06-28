import { createRouter, createWebHistory } from 'vue-router'
import JobList from './components/JobList.vue'
import JobDetail from './components/JobDetail.vue'
import JobOverview from './components/JobOverview.vue'

const routes = [
    {
        path: '/',
        name: 'JobList',
        component: JobList,
    },
    {
        path: '/job/:id',
        name: 'JobDetail',
        component: JobDetail,
        props: true, // Allow passing params as props
    },
    {
        path: '/overview',
        name: 'JobOverview',
        component: JobOverview,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
