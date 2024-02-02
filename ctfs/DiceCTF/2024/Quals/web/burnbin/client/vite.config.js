import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/css': 'http://localhost:3000',
      '/uploads': 'http://localhost:3000',
      '/api': 'http://localhost:3000'
    }
  },
  build: {
    sourcemap: true
  }
})
