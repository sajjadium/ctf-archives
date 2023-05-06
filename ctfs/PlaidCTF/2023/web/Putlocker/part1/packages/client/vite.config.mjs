import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
	plugins: [react(), tsconfigPaths()],
	css: {
		modules: {
			localsConvention: "camelCaseOnly"
		}
	},
	resolve: {
		alias: {
			"@": "/src",
			"@assets": "/assets"
		}
	},
	define: {
		__DEV__: false
	},
	server: {
		port: 7008,
		proxy: {
			"/graphql": {
				target: "http://localhost",
			}
		}
	}
});
