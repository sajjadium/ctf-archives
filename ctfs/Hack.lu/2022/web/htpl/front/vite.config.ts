import { defineConfig } from "vite";
import monacoEditorPlugin from "vite-plugin-monaco-editor";
import { resolve } from "path";
import handlebars from "vite-plugin-handlebars";

export default defineConfig({
  build: {
    chunkSizeWarningLimit: 700,
    rollupOptions: {
      output: {
        compact: false,
        minifyInternalExports: false,
        generatedCode: "es2015",
        sourcemap: true,
      },
      input: {
        index: resolve(__dirname, "index.html"),
        docs: resolve(__dirname, "docs.html"),
        write: resolve(__dirname, "write.html"),
        share: resolve(__dirname, "share.html"),
      },
    },
  },
  plugins: [
    monacoEditorPlugin(),
    handlebars({
      partialDirectory: resolve(__dirname, "./includes"),
    }) as any,
  ],
});
