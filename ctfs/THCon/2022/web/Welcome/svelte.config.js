import adapter from '@sveltejs/adapter-node'
import { config as dotenv } from 'dotenv'
import preprocess from 'svelte-preprocess'

const __dirname = new URL('.', import.meta.url).pathname
dotenv({ path: `${__dirname}/../../.env` })

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: [
    preprocess({
      scss: {
        prependData: `@use "${__dirname}/src/variables.scss" as *;`,
      },
    }),
  ],

  kit: {
    adapter: adapter(),

    vite: {
      css: {
        preprocessorOptions: {
          scss: {
            additionalData: `@use "${__dirname}/src/variables.scss" as *;`,
          },
        },
      },
      server: {
        proxy: {
          '/api': {
            target: `http://localhost:${process.env.VITE_API_PORT}`,
            ws: true,
          },
        },
      },
    },
  },
}

export default config
