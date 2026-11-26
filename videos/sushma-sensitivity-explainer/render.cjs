// Render explainer.html frame by frame (Playwright, preinstalled Chromium) at 2x, downscaled once to 1080x1920.
//   node render.cjs                    -> out/explainer.mp4 (0 .. TEND, 30 fps)
//   node render.cjs --stills 1 5 9 ... -> out/stills/s_<t>.jpg (540x960 QA)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const HERE = __dirname, FPS = Number(process.env.FPS || 60);
const run = a => new Promise(r => spawn('ffmpeg', a, { stdio: 'inherit' }).on('close', r));
(async () => {
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(HERE, 'explainer.html')); await page.evaluate(() => window.ready);
  const { TEND } = await page.evaluate(() => window.TIMING);
  const grab = async t => { await page.evaluate(t => seek(t), t); return page.screenshot({ type: 'png' }); };
  const si = process.argv.indexOf('--stills');
  if (si > 0) { fs.mkdirSync(path.join(HERE, 'out', 'stills'), { recursive: true });
    for (const t of process.argv.slice(si + 1).map(Number)) { const p = path.join(HERE, 'out', 'stills', `s_${t}`); fs.writeFileSync(p + '.png', await grab(t));
      await run(['-v', 'error', '-y', '-i', p + '.png', '-vf', 'scale=540:960:flags=lanczos', p + '.jpg']); fs.unlinkSync(p + '.png'); }
    await browser.close(); return; }
  const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-vf', 'scale=1080:1920:flags=lanczos,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '8', '-tune', 'animation', '-r', String(FPS), path.join(HERE, 'out', 'explainer.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(TEND * FPS);
  for (let f = 0; f < N; f++) { const b = await grab(f / FPS); if (!enc.stdin.write(b)) await new Promise(r => enc.stdin.once('drain', r)); if (f % 90 === 0) console.log(`frame ${f}/${N}`); }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await browser.close(); console.log(`out/explainer.mp4: ${N} frames`);
})();
