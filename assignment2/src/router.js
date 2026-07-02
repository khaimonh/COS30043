import { createRouter, createWebHistory } from 'vue-router'
import JobList from './components/JobList.vue'
import JobDetail from './components/JobDetail.vue'
import JobOverview from './components/JobOverview.vue'
import Explorer from './components/Explorer.vue'
import ToDoList from './components/ToDoList.vue'
import ApplicationForm from './components/ApplicationForm.vue'

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
        props: true,
    },
    {
        path: '/overview',
        name: 'JobOverview',
        component: JobOverview,
    },
    {
        path: '/explorer',
        name: 'Explorer',
        component: Explorer,
    },
    {
        path: '/todo',
        name: 'ToDoList',
        component: ToDoList,
    },
    {
        path: '/application-form',
        name: 'ApplicationForm',
        component: ApplicationForm,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
