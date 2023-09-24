import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    proxy: {
      "/api": "https://picoblog-1ea47ec5f44a1743.brics-ctf.ru",
    },
  },
});
