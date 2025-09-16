import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: true,
    port: 5173,
    // Add your production domain here to allow it
    // The host "simple-expense-tracker.de" is blocked by default.
    allowedHosts: [
      'simple-expense-tracker.de',
      'www.simple-expense-tracker.de'
    ]
  }
})
