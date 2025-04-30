import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      // forward /auth/* and /users/* to backend
      "/auth":  "http://localhost:8000",
      "/users": "http://localhost:8000"
    }
  },
});
