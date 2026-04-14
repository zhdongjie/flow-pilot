import { createApp } from "vue";
import App from "./App.vue";
import "./style.css";
import { initFlowPilot } from "./sdk-bridge";

createApp(App).mount("#app");
initFlowPilot();
