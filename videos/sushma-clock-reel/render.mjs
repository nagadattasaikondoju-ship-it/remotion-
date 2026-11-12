// node render.mjs stills 0.5 2 13 17.5     → out/stills/t_<t>.png
// node render.mjs video [fps=60]           → out/video.mp4 (frames piped straight into ffmpeg, no temp PNGs)
import { createRequire } from "module";
import { spawn } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const dir = path.dirname(fileURLToPath(import.meta.url));
const mode = process.argv[2] || "stills";
const logo = "data:image/png;base64," + fs.readFileSync(path.join(dir, "assets/logo_blue.png")).toString("base64");
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.addInitScript((d) => { window.LOGO_DATA = d; }, logo);
await p.goto("file://" + path.join(dir, "index.html"));
await p.evaluate(() => window.ready);
if (mode === "stills") {
  fs.mkdirSync(path.join(dir, "out/stills"), { recursive: true });
  for (const t of process.argv.slice(3).map(Number)) {
    await p.evaluate((t) => window.seek(t), t);
    await p.screenshot({ path: path.join(dir, `out/stills/t_${t}.png`) });
  }
} else {
  const fps = Number(process.argv[3] || 60), DUR = 21.0, N = Math.round(DUR * fps);
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "8", "-tune", "animation", "-pix_fmt", "yuv420p",
    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", path.join(dir, "out/video.mp4")], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = 0; f < N; f++) {
    await p.evaluate((t) => window.seek(t), f / fps);
    const buf = await p.screenshot({ type: "png" });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (f % 120 === 0) process.stdout.write(`${f}/${N} `);
  }
  ff.stdin.end(); await new Promise((r) => ff.on("close", r)); console.log("\nout/video.mp4");
}
await b.close();
