import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import { ensureUser, token, user, isAdmin } from "../lib/session";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/about", name: "about", component: () => import("../views/AboutView.vue") },
    { path: "/news", name: "news", component: () => import("../views/NewsView.vue") },
    { path: "/login", name: "login", component: () => import("../views/AuthView.vue") },
    { path: "/market", name: "market", component: () => import("../views/MarketView.vue") },
    { path: "/stocks/:ticker", name: "stock", component: () => import("../views/StockView.vue") },
    { path: "/portfolio", name: "portfolio", component: () => import("../views/PortfolioView.vue"), meta: { requiresAuth: true } },
    { path: "/watchlist", name: "watchlist", component: () => import("../views/WatchlistView.vue"), meta: { requiresAuth: true } },
    { path: "/orders", name: "orders", component: () => import("../views/OrdersView.vue"), meta: { requiresAuth: true } },
    { path: "/bank-accounts", name: "bank", component: () => import("../views/BankAccountsView.vue"), meta: { requiresAuth: true } },
    { path: "/admin", name: "admin", component: () => import("../views/AdminView.vue"), meta: { requiresAuth: true, requiresAdmin: true } },
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

router.beforeEach(async (to) => {
  await ensureUser();
  if (to.meta.requiresAuth && !token.value) {
    return { name: "login", query: { redirect: to.fullPath } };
  }
  if (to.meta.requiresAdmin && !isAdmin()) {
    return { name: "market" };
  }
  if (to.name === "login" && token.value && user.value) {
    return { name: "market" };
  }
});

export default router;
