// Morrow profile-build reel renderer (Playwright).
//   node render.mjs stills 2.5 3.5 …   → out/stills/<t>.png   (UI frames at given video times)
//   node render.mjs caption            → out/caption.png      (hook caption on transparent background)
//   node render.mjs ui                 → out/ui/f_NNNNN.png   (60 fps, from the beat drop to the end)
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "out");
const EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const [mode, ...args] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: EXE, args: ["--allow-file-access-from-files"] });
try {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  await page.goto("file://" + path.join(HERE, "index.html"));
  await page.evaluate(() => window.ready);
  const T = await page.evaluate(() => window.TIMING);
  if (mode === "stills") {
    fs.mkdirSync(path.join(OUT, "stills"), { recursive: true });
    for (const t of args.map(Number)) { await page.evaluate((tt) => window.seek(tt), t); await page.screenshot({ path: path.join(OUT, "stills", `${t.toFixed(3)}.png`) }); }
  } else if (mode === "caption") {
    await page.evaluate(() => window.caption());
    await page.screenshot({ path: path.join(OUT, "caption.png"), omitBackground: true });
  } else if (mode === "ui") {
    const dir = path.join(OUT, "ui"); fs.mkdirSync(dir, { recursive: true });
    const f0 = Math.round(T.DROP * 60), f1 = Math.round(T.END * 60);
    for (let f = f0; f < f1; f++) { await page.evaluate((tt) => window.seek(tt), f / 60); await page.screenshot({ path: path.join(dir, `f_${String(f - f0).padStart(5, "0")}.png`) }); }
    console.log(`${f1 - f0} frames, ${(f0 / 60).toFixed(3)}–${(f1 / 60).toFixed(3)} s`);
  }
  console.log(JSON.stringify(T));
} finally { await browser.close(); }
