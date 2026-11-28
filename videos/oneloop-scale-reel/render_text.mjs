// Render the text layers as transparent 1080×1920 PNGs: out/text_hook.png, out/text_c0..5.png, out/text_tiles.png
import { chromium } from "playwright-core";
import path from "node:path";
import { fileURLToPath } from "node:url";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--allow-file-access-from-files"] });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto("file://" + path.join(HERE, "text.html")); await page.evaluate(() => window.ready);
for (const s of ["hook", "c0", "c1", "c2", "c3", "c4", "c5", "tiles"]) {
  await page.evaluate((st) => window.render(st), s);
  await page.screenshot({ path: path.join(HERE, "out", `text_${s}.png`), omitBackground: true });
}
await browser.close(); console.log("text layers done");
