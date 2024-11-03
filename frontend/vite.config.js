import { fileURLToPath, URL } from 'node:url'
import path from 'path';

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import createSvgSpritePlugin from 'vite-plugin-svg-spriter'

const SVG_FOLDER_PATH = path.resolve(path.resolve(__dirname, 'src'), 'assets', 'icons')

export default defineConfig({
  plugins: [
    vue(),
    createSvgSpritePlugin({svgFolder: SVG_FOLDER_PATH})
  ],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/scss/global.scss";`
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})