// BRIDL360 brand layer renderer (Playwright + preinstalled Chromium), 1080x1920, 30 fps, transparent.
//   node render.cjs overlay            -> out/overlay.mov (PNG-in-MOV with alpha; frames outside the brand windows are empty)
//   BASE=<video> node render.cjs stills 14.3 24 27.5 ... -> out/stills/<t>.jpg (overlay composited on BASE, 540x960)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), { spawn, spawnSync } = require('child_process');
const HERE = __dirname, FPS = 30, DUR = 49.7667, OUT = path.join(HERE, 'out');
const [mode, ...args] = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message));
  const times = fs.existsSync(path.join(HERE, 'vo/times.json')) ? fs.readFileSync(path.join(HERE, 'vo/times.json'), 'utf8') : '{}';
  await page.addInitScript(`window.TIMES = ${times};`);
  await page.goto('file://' + path.join(HERE, 'brand.html')); await page.evaluate(() => window.ready);
  const shot = async t => { await page.evaluate(t => seek(t), t); return page.screenshot({ type: 'png', omitBackground: true }); };
  if (mode === 'stills') {
    fs.mkdirSync(path.join(OUT, 'stills'), { recursive: true });
    for (const t of args.map(Number)) {
      const p = path.join(OUT, 'stills', `${t}`); fs.writeFileSync(p + '_ov.png', await shot(t));
      spawnSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(t), '-i', process.env.BASE, '-i', p + '_ov.png', '-filter_complex',
        '[0:v]scale=1080:1920,crop=1050:1867:0:0,scale=1080:1920:flags=lanczos[b];[b][1:v]overlay=0:0,scale=540:960', '-frames:v', '1', p + '.jpg']); fs.unlinkSync(p + '_ov.png');
    }
  } else if (mode === 'overlay') {
    const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'png', '-pix_fmt', 'rgba', path.join(OUT, 'overlay.mov')], { stdio: ['pipe', 'inherit', 'inherit'] });
    const N = Math.round(DUR * FPS); let blank = null;
    for (let f = 0; f < N; f++) {
      const t = f / FPS, active = await page.evaluate(t => ACTIVE(t), t);
      let b; if (active) b = await shot(t); else { if (!blank) blank = await shot(1); b = blank; }
      if (!enc.stdin.write(b)) await new Promise(r => enc.stdin.once('drain', r));
      if (f % 150 === 0) console.log(`frame ${f}/${N}`);
    }
    enc.stdin.end(); await new Promise(r => enc.on('close', r)); console.log(`out/overlay.mov: ${N} frames`);
  }
  await browser.close();
})();
