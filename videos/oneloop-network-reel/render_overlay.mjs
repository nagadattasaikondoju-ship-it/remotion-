// Renders overlay.html to a transparent 1080x1920 PNG (out/overlay.png), plus a preview over a still (out/preview.png).
import { createRequire } from "module";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH || "/opt/node-tools/node_modules/playwright");
const dir = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await p.goto("file://" + path.join(dir, "overlay.html"));
await p.evaluate(() => window.ready);
await p.screenshot({ path: path.join(dir, "out/overlay.png"), omitBackground: true });
await b.close();
console.log("out/overlay.png");
