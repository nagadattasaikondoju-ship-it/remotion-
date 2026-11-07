// Render the explainer with Playwright.
//   node render.mjs stills 0.25 0.75 ...   → out/stills/<t>.png  (single frames, same motion blur as the film)
//   node render.mjs beats [from] [to]      → out/beats/tNN.NN.png (one frame per half-beat, 0.12 s after it)
//   node render.mjs audio                  → out/audio_raw.wav    (OfflineAudioContext)
//   node render.mjs full [workers]         → out/sub/s_NNNNN.png  (60 fps × 3 trailing sub-frames = 180 per second)
//   LAND=1 node render.mjs …               → the 1920×1080 landscape version (index.html?l=1), into out/landscape/
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const LAND = process.env.LAND === "1";
const OUT = path.join(HERE, LAND ? "out/landscape" : "out");
const [VW, VH, DUR] = LAND ? [1920, 1080, 76] : [1080, 1920, 76];
const EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const [mode, ...args] = process.argv.slice(2);

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.error("console:", m.text()); });
  await page.goto("file://" + path.join(HERE, "index.html") + (LAND ? "?l=1" : ""));
  await page.evaluate(() => window.ready);
  return page;
}
const shot = async (page, t, file) => {
  await page.evaluate((tt) => window.seek(tt), t);
  await page.screenshot({ path: file, clip: { x: 0, y: 0, width: VW, height: VH }, type: file.endsWith(".jpg") ? "jpeg" : "png", quality: file.endsWith(".jpg") ? 80 : undefined });
};

const browser = await chromium.launch({ executablePath: EXE, args: ["--allow-file-access-from-files", "--disable-gpu-vsync"] });
try {
  if (mode === "stills" || mode === "beats") {
    const dir = path.join(OUT, mode);
    fs.mkdirSync(dir, { recursive: true });
    let times;
    if (mode === "beats") { const a = Number(args[0] || 0), b = Number(args[1] || DUR), st = Number(args[2] || 0.25); times = []; for (let t = a; t < b - 1e-9; t += st) times.push(+(t + 0.12).toFixed(3)); }
    else times = args.map(Number);
    const workers = 3, chunks = Array.from({ length: workers }, (_, w) => times.filter((_, i) => i % workers === w));
    await Promise.all(chunks.map(async (ts) => { const page = await openPage(browser);
      for (const t of ts) await shot(page, t, path.join(dir, `t${t.toFixed(3).padStart(7, "0")}.jpg`)); }));
    console.log(`${times.length} frames → ${dir}`);
  } else if (mode === "audio") {
    const page = await openPage(browser);
    const b64 = await page.evaluate(() => window.renderAudio());
    fs.mkdirSync(OUT, { recursive: true });
    fs.writeFileSync(path.join(OUT, "audio_raw.wav"), Buffer.from(b64, "base64"));
    console.log("audio → out/audio_raw.wav");
  } else if (mode === "full") {
    const dir = path.join(OUT, "sub");
    fs.mkdirSync(dir, { recursive: true });
    const total = DUR * 180, workers = Number(args[0] || 3);
    let next = 0, done = 0;
    const t0 = Date.now();
    await Promise.all(Array.from({ length: workers }, async () => {
      const page = await openPage(browser);
      while (next < total) {
        const n = next++;
        // sub-frame n: output frame f = floor(n/3), trailing shutter (f/60 − (2 − k)/180)
        const f = Math.floor(n / 3), k = n % 3, t = f / 60 - (2 - k) / 180;
        const file = path.join(dir, `s_${String(n).padStart(5, "0")}.png`);
        if (!fs.existsSync(file)) await shot(page, Math.max(0, t), file);
        if (++done % 900 === 0) console.log(`${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
      }
    }));
    console.log("sub-frames done");
  }
} finally {
  await browser.close();
}
