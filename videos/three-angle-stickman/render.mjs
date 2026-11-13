// node render.mjs stills 1.0 4.5 …   → out/stills/<t>.png
// node render.mjs frames [workers]   → out/frames/f_NNNNN.png at 24 fps (no sub-frames: hand-drawn boil on 12 fps)
import pw from "/opt/node-tools/node_modules/playwright/index.js";
import fs from "node:fs"; import path from "node:path"; import { fileURLToPath } from "node:url";
const { chromium } = pw;
const HERE = path.dirname(fileURLToPath(import.meta.url)), OUT = path.join(HERE, "out"), FPS = 24, END = 42.5;
const [mode, ...args] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--allow-file-access-from-files"] });
async function openPage() { const p = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  p.on("pageerror", (e) => console.error("pageerror:", e.message)); await p.goto("file://" + path.join(HERE, "index.html")); await p.evaluate(() => window.ready); return p; }
const shot = async (p, t, file) => { await p.evaluate((tt) => window.seek(tt), t); await p.screenshot({ path: file, clip: { x: 0, y: 0, width: 1920, height: 1080 } }); };
try {
  if (mode === "stills") { const dir = path.join(OUT, "stills"); fs.mkdirSync(dir, { recursive: true }); const p = await openPage();
    for (const t of args.map(Number)) await shot(p, t, path.join(dir, `${t.toFixed(2).padStart(5, "0")}.png`)); console.log(`${args.length} → ${dir}`); }
  else if (mode === "audio") { const p = await openPage(); await p.addScriptTag({ path: path.join(HERE, "audio.js") });
    const b64 = await p.evaluate(() => window.renderAudio()); fs.mkdirSync(OUT, { recursive: true }); fs.writeFileSync(path.join(OUT, "music_raw.wav"), Buffer.from(b64, "base64")); console.log("music → out/music_raw.wav"); }
  else if (mode === "frames") { const dir = path.join(OUT, "frames"); fs.mkdirSync(dir, { recursive: true }); const total = Math.round(END * FPS), workers = Number(args[0] || 4); let next = 0, done = 0;
    await Promise.all(Array.from({ length: workers }, async () => { const p = await openPage();
      while (next < total) { const n = next++, f = path.join(dir, `f_${String(n).padStart(5, "0")}.png`); if (!fs.existsSync(f)) await shot(p, n / FPS, f); if (++done % 240 === 0) console.log(done + "/" + total); } }));
    console.log("frames done"); }
} finally { await browser.close(); }
