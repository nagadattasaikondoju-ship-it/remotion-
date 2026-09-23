// Stage 4: render the Short composition with @remotion/renderer.
// Usage: node scripts/render.mjs [out.mp4]
// Set REMOTION_BROWSER_EXECUTABLE to use a local Chrome headless shell.
import { bundle } from "@remotion/bundler";
import { renderMedia, selectComposition } from "@remotion/renderer";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "..");
const output = path.resolve(process.argv[2] ?? "out/short.mp4");
const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE ?? null;

const serveUrl = await bundle({ entryPoint: path.join(root, "src/index.ts"), publicDir: path.join(root, "public") });
const composition = await selectComposition({ serveUrl, id: "Short", browserExecutable });

console.log(`Rendering ${composition.width}x${composition.height} @ ${composition.fps}fps, ${composition.durationInFrames} frames`);
let last = -1;
await renderMedia({
  serveUrl,
  composition,
  codec: "h264",
  crf: 18,
  pixelFormat: "yuv420p",
  audioCodec: "aac",
  audioBitrate: "192k",
  imageFormat: "jpeg",
  jpegQuality: 95,
  outputLocation: output,
  browserExecutable,
  onProgress: ({ progress }) => {
    const pct = Math.floor(progress * 10) * 10;
    if (pct !== last) console.log(`${pct}%`), (last = pct);
  },
});
console.log(`Done -> ${output}`);
