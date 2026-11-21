// Render the One Loop intro reel (1080×1920) with Playwright.
//   node render.mjs stills 0.5 1.25 …   → out/stills/<t>.png
//   node render.mjs beats               → out/beats/bNN.png (one frame per beat, +0.12 s) and out/beats/hNN.png (half beats)
//   node render.mjs audio               → out/audio_raw.wav (OfflineAudioContext)
//   node render.mjs full [workers]      → out/sub/s_NNNNN.png (60 fps × 3 sub-frames)
import pw from "/opt/node-tools/node_modules/playwright/index.js";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const { chromium } = pw;
const HERE = path.dirname(fileURLToPath(import.meta.url)), OUT = path.join(HERE, "out");
const EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", DUR = 25;
const [mode, ...args] = process.argv.slice(2);
async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.error("console:", m.text()); });
  await page.goto("file://" + path.join(HERE, "index.html"));
  await page.evaluate(() => window.ready);
  return page;
}
const shot = async (page, t, file) => { await page.evaluate((tt) => window.seek(tt), t); await page.screenshot({ path: file, clip: { x: 0, y: 0, width: 1080, height: 1920 } }); };
const browser = await chromium.launch({ executablePath: EXE, args: ["--allow-file-access-from-files"] });
try {
  if (mode === "stills" || mode === "beats") {
    const dir = path.join(OUT, mode); fs.mkdirSync(dir, { recursive: true });
    const page = await openPage(browser);
    const times = mode === "beats" ? Array.from({ length: DUR * 4 }, (_, i) => i * 0.25 + 0.12) : args.map(Number);
    for (const [i, t] of times.entries()) await shot(page, t, path.join(dir, mode === "beats" ? `q${String(i).padStart(3, "0")}.png` : `${t.toFixed(3)}.png`));
    console.log(`${times.length} frames → ${dir}`);
  } else if (mode === "audio") {
    await (await import("node:child_process")).execSync("true");
    const page = await openPage(browser);
    await page.addScriptTag({ path: path.join(HERE, "audio.js") });
    const b64 = await page.evaluate(() => window.renderAudio());
    fs.mkdirSync(OUT, { recursive: true }); fs.writeFileSync(path.join(OUT, "audio_raw.wav"), Buffer.from(b64, "base64"));
    console.log("audio → out/audio_raw.wav");
  } else if (mode === "full") {
    const dir = path.join(OUT, "sub"); fs.mkdirSync(dir, { recursive: true });
    const total = DUR * 180, workers = Number(args[0] || 4); let next = 0, done = 0; const t0 = Date.now();
    await Promise.all(Array.from({ length: workers }, async () => {
      const page = await openPage(browser);
      while (next < total) { const n = next++;
        // output frame f = floor(n/3) is the mean of sub-frames at f/60 − (2 − k)/180 (trailing shutter)
        const f = Math.floor(n / 3), k = n % 3, t = f / 60 - (2 - k) / 180;
        const file = path.join(dir, `s_${String(n).padStart(5, "0")}.png`);
        if (!fs.existsSync(file)) await shot(page, Math.max(0, t), file);
        if (++done % 360 === 0) console.log(`${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)} s`); }
    }));
    console.log("sub-frames done");
  }
} finally { await browser.close(); }
