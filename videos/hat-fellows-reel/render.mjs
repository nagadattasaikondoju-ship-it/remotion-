// HAT Fellows reel overlay renderer (Playwright): captions + cards as transparent PNG frames, 30 fps.
//   node render.mjs stills 1.0 12.5 …   → out/stills/<t>.png
//   node render.mjs frames              → out/ov/f_NNNNN.png (0 … END)
import { chromium } from "playwright-core";
import fs from "node:fs"; import path from "node:path"; import { fileURLToPath } from "node:url";
const HERE = path.dirname(fileURLToPath(import.meta.url)), OUT = path.join(HERE, "out");
const [mode, ...args] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--allow-file-access-from-files"] });
try {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.goto("file://" + path.join(HERE, "index.html")); await page.evaluate(() => window.ready);
  const T = await page.evaluate(() => window.TIMING);
  if (mode === "stills") {
    fs.mkdirSync(path.join(OUT, "stills"), { recursive: true });
    for (const t of args.map(Number)) { await page.evaluate((tt) => window.seek(tt), t); await page.screenshot({ path: path.join(OUT, "stills", `${t.toFixed(2)}.png`), omitBackground: true }); }
  } else if (mode === "frames") {
    const dir = path.join(OUT, "ov"); fs.mkdirSync(dir, { recursive: true }); const n = Math.round(T.END * 30);
    for (let f = 0; f < n; f++) { await page.evaluate((tt) => window.seek(tt), f / 30); await page.screenshot({ path: path.join(dir, `f_${String(f).padStart(5, "0")}.png`), omitBackground: true }); }
    console.log(n, "frames");
  }
} finally { await browser.close(); }
