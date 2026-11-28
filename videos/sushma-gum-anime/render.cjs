// Render anime.html frame by frame (Playwright + preinstalled Chromium) at 2x = 2160x3840 (4K master intermediate).
//   node render.cjs                    -> out/anime_4k.mp4 (0 .. TEND)
//   node render.cjs --stills 1.2 5 ... -> out/stills/s_<t>.jpg (540x960 QA)
//   FROM=600 TO=760 OUT=part.mp4 node render.cjs -> re-render frames 600..759 only (splice into anime_4k.mp4)
//   node render.cjs --last             -> out/last_frame.png (1080x1920, the card's backdrop)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const HERE = __dirname, FPS = 30, TEND = 33.9;
const run = (args) => new Promise(r => spawn('ffmpeg', args, { stdio: 'inherit' }).on('close', r));
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(HERE, 'anime.html'));
  await page.evaluate(() => window.ready());
  const grab = async t => { await page.evaluate(t => seek(t), t); return page.screenshot({ type: 'png' }); };
  const si = process.argv.indexOf('--stills');
  if (si > 0) {
    fs.mkdirSync(path.join(HERE, 'out', 'stills'), { recursive: true });
    for (const t of process.argv.slice(si + 1).map(Number)) {
      const p = path.join(HERE, 'out', 'stills', `s_${t}`); fs.writeFileSync(p + '.png', await grab(t));
      await run(['-v', 'error', '-y', '-i', p + '.png', '-vf', 'scale=540:960:flags=lanczos', p + '.jpg']); fs.unlinkSync(p + '.png');
    }
    await browser.close(); return;
  }
  if (process.argv.includes('--last')) {
    const p = path.join(HERE, 'out', 'last_frame'); fs.writeFileSync(p + '.2x.png', await grab(TEND - 1 / FPS));
    await run(['-v', 'error', '-y', '-i', p + '.2x.png', '-vf', 'scale=1080:1920:flags=lanczos', p + '.png']); fs.unlinkSync(p + '.2x.png');
    await browser.close(); return;
  }
  const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-vf', 'format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '10', '-tune', 'animation', '-r', String(FPS),
    path.join(HERE, 'out', process.env.OUT || 'anime_4k.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(TEND * FPS), t0 = Date.now(), F0 = Number(process.env.FROM || 0), F1 = Number(process.env.TO || N);
  for (let f = F0; f < F1; f++) {
    const buf = await grab(f / FPS);
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
    if (f % 60 === 0) console.log(`frame ${f}/${N}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await browser.close();
  console.log(`out/anime_4k.mp4: ${N} frames`);
})();
