// إعداد بناء نسخة سطح المكتب (ويندوز) — Electron.
// يبني خادمًا محليًا يعمل داخل التطبيق نفسه (Node) بدل هدف السحابة،
// فيعمل التطبيق بالكامل من ملفاته المحلية دون إنترنت.
import { tanstackStart } from "@tanstack/react-start/plugin/vite";
import tailwindcss from "@tailwindcss/vite";
import viteReact from "@vitejs/plugin-react";
import { nitro } from "nitro/vite";
import { defineConfig } from "vite";
import tsConfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  build: { outDir: "dist-electron" },
  resolve: {
    dedupe: ["react", "react-dom", "@tanstack/react-router", "@tanstack/react-start"],
  },
  plugins: [
    tsConfigPaths({ projects: ["./tsconfig.json"] }),
    tailwindcss(),
    tanstackStart({ server: { entry: "server" } }),
    viteReact(),
    nitro({
      config: {
        preset: "node-server",
        output: { dir: "dist-electron" },
      },
    }),
  ],
});
