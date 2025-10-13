import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Configuración de Vite para Codespaces
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,          // permite acceder desde fuera del contenedor
    port: 4237,          // puerto del frontend
    strictPort: true,    // si el 4237 está ocupado, no se cambia automáticamente
    proxy: {
      "/api": {
        target: "http://127.0.0.1:4238", // backend Flask
        changeOrigin: true,
      },
    },
  },
  preview: {
    port: 4237,
    strictPort: true,
  },
});
