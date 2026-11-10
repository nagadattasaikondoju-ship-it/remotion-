// Renders the animated caption overlay as transparent PNG frames: out/ov_<variant>/f_0000.png … (60 fps, 10 s).
// usage: node render_overlay.mjs [channel|comments] [still t]   (with "still t", writes one frame to out/still_<variant>.png)
import { createRequire } from "module";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const dir = path.dirname(fileURLToPath(import.meta.url));
const v = process.argv[2] || "channel", FPS = 60, N = 600;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.join(dir, "overlay.html") + "?v=" + v);
await p.evaluate(() => window.ready);
if (process.argv[3] === "still") {
  await p.evaluate((t) => window.seek(t), Number(process.argv[4] || 0));
  await p.screenshot({ path: path.join(dir, `out/still_${v}.png`), omitBackground: true });
} else {
  const od = path.join(dir, `out/ov_${v}`); fs.mkdirSync(od, { recursive: true });
  for (let f = 0; f < N; f++) {
    await p.evaluate((t) => window.seek(t), f / FPS);
    await p.screenshot({ path: path.join(od, `f_${String(f).padStart(4, "0")}.png`), omitBackground: true });
  }
}
await b.close();
console.log("done", v);
