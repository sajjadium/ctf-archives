import { build } from "esbuild";
import decoratorsPlugin from "./decoratorsPlugin.mjs";

build({
	entryPoints: [
		"src/index.mts"
	],
	outfile: "dist/index.mjs",
	format: "esm",
	platform: "node",
	target: "esnext",
	external: [
		"pg-native"
	],
	bundle: true,
	minify: false,
	sourcemap: true,
	banner: {
		js: `
			// esm compat
			import { createRequire } from "module";
			const require = createRequire(import.meta.url);
			const __dirname = new URL(".", import.meta.url).pathname;

			// make typeorm work
			import "reflect-metadata";
		`
	},
	plugins: [
		decoratorsPlugin()
	]
}).catch(() => process.exit(1));
