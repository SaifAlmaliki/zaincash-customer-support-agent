import { resolve } from "node:path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

// https://vite.dev/config/
const apiProxy = { "/api": process.env.API_PROXY_TARGET || "http://127.0.0.1:8000" }

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { host: "0.0.0.0", port: 5174, strictPort: true, proxy: apiProxy },
  preview: { host: "0.0.0.0", port: 5174, strictPort: true, proxy: apiProxy },
  resolve: {
    alias: {
      "@": resolve(import.meta.dirname, "./src"),
    },
  },
})
