import { defineConfig } from 'vite'
import path from 'node:path'

export default defineConfig(() => {
  return {
    root: __dirname,
    server: { port: 5174 },
    build: { outDir: path.join(__dirname, 'dist'), emptyOutDir: true },
    envPrefix: 'RELACE_',
    envDir: path.join(__dirname, '..', '..', '..'),
    define: {
      // Inject envs into window for the UI script to read
      'window.RELACE_API_KEY': JSON.stringify(process.env.RELACE_API_KEY || ''),
      'window.RELACE_BASE_URL': JSON.stringify(
        process.env.RELACE_BASE_URL || 'https://api.relace.run/v1/',
      ),
    },
  }
})
