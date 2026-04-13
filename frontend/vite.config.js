import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      "/chat": "http://localhost:8000",
      "/auth": "http://localhost:8000",
      "/account": "http://localhost:8000",
    },
  },
});
