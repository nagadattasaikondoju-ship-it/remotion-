// node render.mjs video                 -> out/video.mp4 (out/base.mp4 + overlay.html frames piped straight into ffmpeg, no temp PNGs)
//                                          4K by default (SC=2: the overlay draws in 1080x1920 units at 2x); SC=1 for 1080
// SC=1 BASE=base_1080.mp4 node render.mjs stills 1.0 7.3 ...  -> out/stills/t_<t>.png (overlay on a 1080 preview base, for review)
import { createRequire } from "module";
import { spawn, execFileSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const dir = path.dirname(fileURLToPath(import.meta.url));
const TL = JSON.parse(fs.readFileSync(path.join(dir, "out/timeline.json"), "utf8"));
const mode = process.argv[2] || "stills", FPS = 30, N = Math.round(TL.duration * FPS), SC = Number(process.env.SC || 2);
const BASE = path.join(dir, "out", process.env.BASE || "base.mp4");
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
p.on("pageerror", (e) => console.error("PAGE ERROR", e.message));
const IMGDATA = {};
for (const n of ["nirvaha_s1", "nirvaha_s2", "nirvaha_icon", "lnsports_t"]) {
  const buf = fs.readFileSync(path.join(dir, "img", n + ".png")); const mime = buf[0] === 0xff ? "image/jpeg" : "image/png";
  IMGDATA[n] = `data:${mime};base64,` + buf.toString("base64");
}
await p.addInitScript(([d, im, sc]) => { window.TIMELINE = d; window.IMGDATA = im; window.SC = sc; }, [TL, IMGDATA, SC]);
await p.goto("file://" + path.join(dir, "overlay.html"));
await p.evaluate(() => window.ready);
const frame = (t) => p.evaluate((t) => { window.seek(t); return document.getElementById("c").toDataURL("image/png").split(",")[1]; }, t);
if (mode === "stills") {
  fs.mkdirSync(path.join(dir, "out/stills"), { recursive: true });
  for (const t of process.argv.slice(3).map(Number)) {
    const png = path.join(dir, `out/stills/ov_${t}.png`); fs.writeFileSync(png, Buffer.from(await frame(t), "base64"));
    execFileSync("ffmpeg", ["-v", "error", "-y", "-ss", String(t), "-i", BASE, "-i", png, "-frames:v", "1",
      "-filter_complex", "[0:v][1:v]overlay", path.join(dir, `out/stills/t_${t}.png`)]);
  }
} else {
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-i", BASE, "-f", "image2pipe", "-framerate", String(FPS), "-i", "-",
    "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]", "-map", "[v]", "-frames:v", String(N),
    "-c:v", "libx264", "-preset", "medium", "-crf", "11", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    path.join(dir, "out/video.mp4")], { stdio: ["pipe", "inherit", "inherit"] });
  for (let f = 0; f < N; f++) {
    const buf = Buffer.from(await frame(f / FPS), "base64");
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (f % 150 === 0) process.stdout.write(`${f}/${N} `);
  }
  ff.stdin.end(); await new Promise((r) => ff.on("close", r)); console.log("\nout/video.mp4");
}
await b.close();
