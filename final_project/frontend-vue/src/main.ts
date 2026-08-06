import { createApp } from "vue";
import "./style.css";
import "@fontsource/space-grotesk/400.css";
import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/600.css";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import router from "./router";
import App from "./App.vue";

createApp(App).use(router).mount("#app");
