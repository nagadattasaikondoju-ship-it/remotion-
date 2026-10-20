// Render the showreel with Playwright.
//   node render.mjs stills 0.25 0.75 ...   → out/stills/<t>.png  (single frames, same motion blur as the film)
//   node render.mjs beats                  → out/beats/bNN.png   (one frame per beat, 0.12 s after it)
//   node render.mjs audio                  → out/audio_raw.wav   (OfflineAudioContext)
//   node render.mjs full                   → out/sub/s_NNNNN.png (60 fps × 3 trailing sub-frames = 180 per second)
//   VERT=1 node render.mjs …               → the 1080×1920 Reels version, into out/vertical/
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const VERT = process.env.VERT === "1";
const OUT = path.join(HERE, VERT ? "out/vertical" : "out");
const [VW, VH] = VERT ? [1080, 1920] : [1920, 1080];
const EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const [mode, ...args] = process.argv.slice(2);

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.goto("file://" + path.join(HERE, "index.html") + (VERT ? "?v=1" : ""));
  await page.evaluate(() => window.ready);
  return page;
}
const shot = async (page, t, file) => {
  await page.evaluate((tt) => window.seek(tt), t);
  await page.screenshot({ path: file, clip: { x: 0, y: 0, width: VW, height: VH } });
};

const browser = await chromium.launch({ executablePath: EXE, args: ["--allow-file-access-from-files", "--disable-gpu-vsync"] });
try {
  if (mode === "stills" || mode === "beats") {
    const dir = path.join(OUT, mode);
    fs.mkdirSync(dir, { recursive: true });
    const page = await openPage(browser);
    const times = mode === "beats" ? Array.from({ length: 30 }, (_, b) => b * 0.5 + 0.12) : args.map(Number);
    for (const [i, t] of times.entries()) {
      const name = mode === "beats" ? `b${String(i).padStart(2, "0")}.png` : `${t.toFixed(3)}.png`;
      await shot(page, t, path.join(dir, name));
    }
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
    const total = 15 * 180, workers = Number(args[0] || 3);
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
        if (++done % 180 === 0) console.log(`${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
      }
    }));
    console.log("sub-frames done");
  }
} finally {
  await browser.close();
}
