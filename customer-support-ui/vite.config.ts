import { resolve } from "node:path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { host: "0.0.0.0", proxy: { "/api": "http://127.0.0.1:8000" } },
  preview: { host: "0.0.0.0", proxy: { "/api": "http://127.0.0.1:8000" } },
  resolve: {
    alias: {
      "@": resolve(import.meta.dirname, "./src"),
    },
  },
})
