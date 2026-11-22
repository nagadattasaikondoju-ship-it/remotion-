// ep. 04 renderer (Playwright + the preinstalled Chromium), 1080x1920 at 60 fps like ep. 01-03.
//   node render.cjs stills 3.5 4.3 ...  -> out/stills/<t>.jpg (540x960 QA)
//   node render.cjs caption             -> out/caption.png (hook text on transparent ground)
//   node render.cjs ui                  -> out/ui.mp4 (from the beat drop to the end, near-lossless)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const HERE = __dirname, OUT = path.join(HERE, 'out'), FPS = 60;
const [mode, ...args] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('pageerror:', e.message));
  await page.goto('file://' + path.join(HERE, 'index.html')); await page.evaluate(() => window.ready);
  const T = await page.evaluate(() => window.TIMING);
  if (mode === 'stills') {
    fs.mkdirSync(path.join(OUT, 'stills'), { recursive: true });
    for (const t of args.map(Number)) { await page.evaluate(tt => seek(tt), t); const p = path.join(OUT, 'stills', `${t}`);
      await page.screenshot({ path: p + '.png' });
      await new Promise(r => spawn('ffmpeg', ['-v', 'error', '-y', '-i', p + '.png', '-vf', 'scale=540:960', p + '.jpg']).on('close', r)); fs.unlinkSync(p + '.png'); }
  } else if (mode === 'caption') {
    await page.evaluate(() => caption()); await page.screenshot({ path: path.join(OUT, 'caption.png'), omitBackground: true });
  } else if (mode === 'ui') {
    const f0 = Math.round(T.DROP * FPS), f1 = Math.round(T.END * FPS);
    const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-vf', 'format=yuv420p',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '6', '-r', String(FPS), path.join(OUT, 'ui.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = f0; f < f1; f++) { await page.evaluate(tt => seek(tt), f / FPS); const b = await page.screenshot({ type: 'png' });
      if (!enc.stdin.write(b)) await new Promise(r => enc.stdin.once('drain', r)); if ((f - f0) % 120 === 0) console.log(`frame ${f - f0}/${f1 - f0}`); }
    enc.stdin.end(); await new Promise(r => enc.on('close', r)); console.log(`${f1 - f0} frames ${(f0 / FPS).toFixed(3)}-${(f1 / FPS).toFixed(3)} s`);
  }
  await browser.close();
})();
