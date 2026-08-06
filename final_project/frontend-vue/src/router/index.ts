import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/about", name: "about", component: () => import("../views/AboutView.vue") },
    { path: "/news", name: "news", component: () => import("../views/NewsView.vue") },
  ],
});

export default router;
