import { resolve } from "node:path";
import { defineConfig } from "vite";

export default defineConfig((opt) => {
  return {
    root: "src",
    build: {
      outDir: "../dist",
      rollupOptions: {
        input: {
          index: resolve(__dirname, "src/index.ts"),
          background: resolve(__dirname, "src/background.ts"),
        },
        output: {
          entryFileNames: "[name].js",
        },
      },
    },
  };
});
