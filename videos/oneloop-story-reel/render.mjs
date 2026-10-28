// Render overlay.html (captions + graphics) to transparent PNGs with Playwright.
//   node render.mjs stills 1.2 11.9 …  → out/stills/tNN.NNN.png  (single overlay frames, transparent)
//   node render.mjs full [workers]     → out/ov/f_NNNNN.png       (60 fps, 2,280 frames)
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const FPS = 60, DUR = 38;
const [mode, ...args] = process.argv.slice(2);

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.error("console:", m.text()); });
  await page.goto("file://" + path.join(HERE, "overlay.html"));
  await page.evaluate(() => window.ready);
  return page;
}
const shot = async (page, t, file) => {
  await page.evaluate((tt) => window.seek(tt), t);
  await page.screenshot({ path: file, omitBackground: true, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
};

const browser = await chromium.launch({ executablePath: EXE, args: ["--allow-file-access-from-files"] });
try {
  if (mode === "stills") {
    const dir = path.join(HERE, "out/stills"); fs.mkdirSync(dir, { recursive: true });
    const page = await openPage(browser);
    for (const t of args.map(Number)) await shot(page, t, path.join(dir, `t${t.toFixed(3).padStart(6, "0")}.png`));
    console.log(`${args.length} stills → out/stills`);
  } else if (mode === "full") {
    const dir = path.join(HERE, "out/ov"); fs.mkdirSync(dir, { recursive: true });
    const total = DUR * FPS, workers = Number(args[0] || 4); let next = 0, done = 0; const t0 = Date.now();
    await Promise.all(Array.from({ length: workers }, async () => {
      const page = await openPage(browser);
      while (next < total) { const n = next++;
        await shot(page, n / FPS, path.join(dir, `f_${String(n).padStart(5, "0")}.png`));
        if (++done % 120 === 0) console.log(`${done}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)} s`); }
    }));
    console.log(`overlay: ${total} frames → out/ov`);
  }
} finally { await browser.close(); }
