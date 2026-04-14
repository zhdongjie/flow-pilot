import { createApp } from "vue";
import App from "./App.vue";
import "./style.css";
import { mountGuideLayer } from "./guide/index.js";

createApp(App).mount("#app");
mountGuideLayer();
