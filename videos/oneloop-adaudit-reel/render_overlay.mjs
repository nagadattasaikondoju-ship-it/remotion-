// node render_overlay.mjs → out/ov/<scene>.png (transparent 1080×1920, one still per scene; the reel hard-cuts between them)
import { createRequire } from "module";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const dir = path.dirname(fileURLToPath(import.meta.url));
fs.mkdirSync(path.join(dir, "out/ov"), { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.join(dir, "overlay.html"));
await p.evaluate(() => window.ready);
await p.waitForLoadState("networkidle");
for (const s of await p.evaluate(() => window.SCENES)) {
  await p.evaluate((s) => window.show(s), s);
  await p.waitForTimeout(120);
  await p.screenshot({ path: path.join(dir, `out/ov/${s}.png`), omitBackground: true });
}
await b.close();
console.log("out/ov/*.png");
