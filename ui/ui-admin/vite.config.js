import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

// Ми залишаємо index.html у src/pages (як у твоєму дереві),
// тому задаємо root та куди класти білд.
export default defineConfig({
  plugins: [react()],
  root: "src/pages",
  resolve: {
    alias: {
      "@": resolve(__dirname, "src")
    }
  },
  server: {
    port: 5173,
    strictPort: true
  },
  preview: {
    port: 4173
  },
  build: {
    outDir: resolve(__dirname, "dist"),
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, "src/pages/index.html")
    }
  }
});
