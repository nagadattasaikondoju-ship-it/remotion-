// node render.mjs stills 0.5 2.5 ...  -> out/stills/t_<t>.png (captions over out/base.mp4, for review)
// node render.mjs video               -> out/video.mp4 (out/base.mp4 + overlay.html frames piped into ffmpeg)
import { createRequire } from "module";
import { spawn, execFileSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const dir = path.dirname(fileURLToPath(import.meta.url));
const EDIT = JSON.parse(fs.readFileSync(path.join(dir, "out/edit.json"), "utf8"));
const mode = process.argv[2] || "stills", FPS = EDIT.fps, N = Math.round(EDIT.duration * FPS);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
p.on("pageerror", (e) => console.error("PAGE ERROR", e.message));
await p.addInitScript((d) => { window.EDIT = d; }, EDIT);
await p.goto("file://" + path.join(dir, "overlay.html"));
await p.evaluate(() => window.ready);
const frame = (t) => p.evaluate((t) => { window.seek(t); return document.getElementById("c").toDataURL("image/png").split(",")[1]; }, t);
const BASE = path.join(dir, "out/base.mp4");
if (mode === "stills") {
  fs.mkdirSync(path.join(dir, "out/stills"), { recursive: true });
  for (const t of process.argv.slice(3).map(Number)) {
    const png = path.join(dir, `out/stills/ov_${t}.png`); fs.writeFileSync(png, Buffer.from(await frame(t), "base64"));
    execFileSync("ffmpeg", ["-v", "error", "-y", "-ss", String(t), "-i", BASE, "-i", png, "-frames:v", "1", "-filter_complex", "[0:v][1:v]overlay",
      path.join(dir, `out/stills/t_${t}.png`)]);
  }
} else {
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-i", BASE, "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
    "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-frames:v", String(N),
    "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    path.join(dir, "out/video.mp4")], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = 0; f < N; f++) {
    const buf = Buffer.from(await frame(f / FPS), "base64");
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
  }
  ff.stdin.end(); await new Promise((r) => ff.on("close", r)); console.log("out/video.mp4", N, "frames");
}
await b.close();
