// Three Angle reel overlay renderer (Playwright + the preinstalled Chromium; CDP screenshots with a transparent background).
//   node render.mjs stills 1.2 13.4 …   → out/stills/o_<t>.png   1080×1920 review frames
//   node render.mjs frames [scale]      → out/overlay4k.mkv      every frame at 30 fps, deviceScaleFactor 2 (2160×3840),
//                                          piped straight into a lossless FFV1 BGRA video (no frame folder on disk)
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
const HERE = path.dirname(fileURLToPath(import.meta.url)), OUT = path.join(HERE, "out");
const EXE = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome";
const [mode, ...args] = process.argv.slice(2);
const TL = JSON.parse(fs.readFileSync(path.join(HERE, "timeline.json"), "utf8"));
const DSF = mode === "frames" ? Number(args[0] || 2) : mode === "still4k" ? 2 : 1;
const browser = await chromium.launch({ executablePath: EXE, args: ["--allow-file-access-from-files", "--font-render-hinting=none"] });
try {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: DSF });
  page.on("pageerror", (e) => console.error("pageerror:", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.error("console:", m.text()); });
  await page.goto("file://" + path.join(HERE, "index.html"));
  await page.evaluate(() => window.ready);
  await page.evaluate((tl) => window.init(tl), TL);
  const cdp = await page.context().newCDPSession(page);
  await cdp.send("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });
  const shot = async () => Buffer.from((await cdp.send("Page.captureScreenshot", { format: "png", optimizeForSpeed: true, clip: { x: 0, y: 0, width: 1080, height: 1920, scale: DSF } })).data, "base64");
  if (mode === "stills") {
    fs.mkdirSync(path.join(OUT, "stills"), { recursive: true });
    for (const t of args.map(Number)) { await page.evaluate((tt) => window.seek(tt), t); fs.writeFileSync(path.join(OUT, "stills", `o_${t.toFixed(2)}.png`), await shot()); }
  } else if (mode === "still4k") {
    fs.mkdirSync(path.join(OUT, "stills"), { recursive: true });
    for (const t of args.map(Number)) { await page.evaluate((tt) => window.seek(tt), t);
      fs.writeFileSync(path.join(OUT, "stills", `o4k_${t.toFixed(2)}.png`), Buffer.from((await cdp.send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: 1080, height: 1920, scale: 2 } })).data, "base64")); }
  } else if (mode === "frames") {
    const NF = Math.round(TL.END * 30);
    const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-framerate", "30", "-c:v", "png", "-i", "-",
      "-c:v", "ffv1", "-level", "3", "-slices", "16", "-pix_fmt", "bgra", path.join(OUT, "overlay4k.mkv")], { stdio: ["pipe", "inherit", "inherit"] });
    const t0 = Date.now();
    for (let f = 0; f < NF; f++) {
      await page.evaluate((tt) => window.seek(tt), f / 30);
      const buf = await shot();
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
      if (f % 150 === 0) console.log(`${f}/${NF} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end(); await new Promise((r) => ff.on("close", r)); console.log("frames", NF);
  }
} finally { await browser.close(); }
