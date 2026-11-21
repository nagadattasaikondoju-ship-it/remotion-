// node render.mjs overlay   -> out/ov/00000.png ... (the captions + emoji as transparent 1080x1920 frames, one per video frame)
// base.py composites them onto the footage in the same pass, so the picture is encoded once.
import { createRequire } from "module";
import { spawn, execFileSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const dir = path.dirname(fileURLToPath(import.meta.url));
const EDIT = JSON.parse(fs.readFileSync(path.join(dir, "out/edit.json"), "utf8"));
const FPS = EDIT.fps, N = Math.round(EDIT.duration * FPS);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
p.on("pageerror", (e) => console.error("PAGE ERROR", e.message));
await p.addInitScript((d) => { window.EDIT = d; }, EDIT);
await p.goto("file://" + path.join(dir, "overlay.html"));
await p.evaluate(() => window.ready);
const frame = (t) => p.evaluate((t) => { window.seek(t); return document.getElementById("c").toDataURL("image/png").split(",")[1]; }, t);
const OV = path.join(dir, "out/ov"); fs.rmSync(OV, { recursive: true, force: true }); fs.mkdirSync(OV, { recursive: true });
for (let f = 0; f < N; f++) fs.writeFileSync(path.join(OV, String(f).padStart(5, "0") + ".png"), Buffer.from(await frame(f / FPS), "base64"));
console.log("out/ov:", N, "frames");
await b.close();
