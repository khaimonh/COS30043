import { createRouter, createWebHistory } from 'vue-router';
import JobOverview from './components/JobOverview.vue';
import JobDetail from './components/JobDetail.vue';

const routes = [
  { 
    path: '/', 
    component: JobOverview 
  },
  { 
    path: '/job/:id', 
    component: JobDetail, 
    props: true   
    }
];

export const router = createRouter({
  history: createWebHistory(), 
  routes
});