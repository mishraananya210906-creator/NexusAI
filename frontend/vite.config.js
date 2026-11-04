import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '..', '')

  return {
    plugins: [react()],
    envDir: '..',
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
          configure: (proxy) => {
            proxy.on('proxyReq', (proxyReq) => {
              if (env.NEXUSAI_API_KEY) {
                proxyReq.setHeader('X-API-Key', env.NEXUSAI_API_KEY)
              }
            })
          },
        },
      },
    },
  }
})