import { createApp } from "vue";
import "bootstrap/dist/css/bootstrap.min.css";
import "./style.css";
import "@fontsource/archivo/400.css";
import "@fontsource/archivo/500.css";
import "@fontsource/archivo/700.css";
import "@fontsource/archivo-black/index.css";
import "@fontsource/martian-mono/400.css";
import "@fontsource/martian-mono/500.css";
import router from "./router";
import App from "./App.vue";

createApp(App).use(router).mount("#app");
