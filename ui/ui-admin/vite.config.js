import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/admin/', // обов'язково для правильного префікса
  build: {
    outDir: 'dist'
  }
})