import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/admin/', // важливо, бо ти проксиш через /admin/
  build: {
    outDir: 'dist',
  },
})
