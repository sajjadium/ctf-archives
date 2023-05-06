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
	server: {
		port: 59998,
		proxy: {
			"/api": {
				target: "http://127.0.0.1:59999",
				changeOrigin: true,
				secure: false
			}
		}
	}
});
