/// <reference types="vitest" />

import { defineConfig, loadEnv } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.ts',
      formats: ['es'],
    },
  },
  test: {
    env: loadEnv('test', '..', 'RELACE_'),
  },
})
