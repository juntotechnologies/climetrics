import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.cjs',
  },
  // Base path for GitHub Pages - change this to your repo name if not deploying to a user/org site
  base: '/climetrics/',
})
