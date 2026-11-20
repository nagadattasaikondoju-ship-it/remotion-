// Render card.html frame by frame (Playwright + the preinstalled Chromium) at 2x, downscaled once to 1080x1920.
//   node render.cjs                 -> out/card.mp4 (150 frames, 30 fps, near-lossless intermediate)
//   node render.cjs --stills 0.3 1  -> out/stills/card_<t>.png (QA, 1080x1920)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const HERE = __dirname, FPS = 30, DUR = Number(process.env.CARD_DUR || 5.0);
const icon = n => fs.readFileSync(path.join(HERE, 'icons', n + '.svg'), 'utf8').match(/ d="([^"]+)"/)[1];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(HERE, 'card.html'));
  await page.evaluate(async ([ig, wa]) => {
    setIcons(ig, wa);
    await Promise.all(['500 40px Poppins', '600 40px Poppins', '700 40px Poppins', '600 40px Oswald'].map(f => document.fonts.load(f)));
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.complete ? 1 : new Promise(r => { i.onload = r; i.onerror = r; })));
  }, [icon('instagram'), icon('whatsapp')]);
  const si = process.argv.indexOf('--stills');
  if (si > 0) {
    fs.mkdirSync(path.join(HERE, 'out', 'stills'), { recursive: true });
    for (const t of process.argv.slice(si + 1).map(Number)) {
      await page.evaluate(t => seek(t), t);
      const png = path.join(HERE, 'out', 'stills', `card_${t}.png`);
      await page.screenshot({ path: png + '.2x.png' });
      await new Promise(r => spawn('ffmpeg', ['-v', 'error', '-y', '-i', png + '.2x.png', '-vf', 'scale=1080:1920:flags=lanczos', png]).on('close', r));
      fs.unlinkSync(png + '.2x.png');
    }
    await browser.close(); return;
  }
  const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-vf', process.env.CARD_4K ? 'format=yuv420p' : 'scale=1080:1920:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '4', '-r', String(FPS),
    path.join(HERE, 'out', 'card.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(DUR * FPS);
  for (let f = 0; f < N; f++) {
    await page.evaluate(t => seek(t), f / FPS);
    const buf = await page.screenshot({ type: 'png' });
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
    if (f % 30 === 0) process.stdout.write(`frame ${f}/${N}\n`);
  }
  enc.stdin.end(); await new Promise(r => enc.on('close', r));
  await browser.close();
  console.log(`out/card.mp4: ${N} frames`);
})();
