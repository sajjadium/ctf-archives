import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { createHtmlPlugin } from 'vite-plugin-html';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		createHtmlPlugin({
			template: 'index.html',
			inject: {
				data: {
					nonce: 'csp-nonce-placeholder-652549-'
				}
			}
		}),
		vue()
	],
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
	},
	build: {
		outDir: "/output",
		rollupOptions: {
			external: [
				/\/api\/v0\/.*/
			]
		}
	}
});
