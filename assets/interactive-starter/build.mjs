import { build } from "esbuild";
import { mkdir, copyFile } from "node:fs/promises";

await mkdir("dist", { recursive: true });
await copyFile("index.html", "dist/index.html");
await build({
  entryPoints: ["main.js"], outdir: "dist", bundle: true,
  format: "esm", splitting: true, minify: true, target: "es2022",
  supported: { "template-literal": false }, legalComments: "eof",
});
