// Render reel.html (three.js + 2D canvas) frame by frame with Playwright + the preinstalled Chromium, served over a tiny local HTTP
// server (ES modules + import map don't load from file://). The page draws at 2x on a 2160x3840 canvas, downscaled to 1080x1920.
//   node render.cjs                 -> out/reel.mp4 (0 .. TEND, FPS env, default 60)
//   node render.cjs --stills 1 5 9  -> out/stills/s_<t>.jpg (540x960 QA)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), http = require('http'), { spawn } = require('child_process');
const HERE = __dirname, FPS = Number(process.env.FPS || 60);
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.png': 'image/png', '.ttf': 'font/ttf', '.json': 'application/json' };
const server = http.createServer((q, r) => { const p = path.join(HERE, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(HERE) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); r.end(); return; }
  r.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r); });
const run = a => new Promise(r => spawn('ffmpeg', a, { stdio: 'inherit' }).on('close', r));
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r)); const url = `http://127.0.0.1:${server.address().port}/reel.html`;
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
  page.on('pageerror', e => console.log('PAGE ERROR', e.message)); page.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await page.goto(url); await page.waitForFunction(() => window.ready); await page.evaluate(() => window.ready);
  const { TEND } = await page.evaluate(() => window.TIMING);
  const grab = async t => { await page.evaluate(t => seek(t), t); return page.locator('#c').screenshot({ type: 'png' }); };
  const si = process.argv.indexOf('--stills');
  if (si > 0) { fs.mkdirSync(path.join(HERE, 'out', 'stills'), { recursive: true });
    for (const t of process.argv.slice(si + 1).map(Number)) { const p = path.join(HERE, 'out', 'stills', `s_${t}`); fs.writeFileSync(p + '.png', await grab(t));
      await run(['-v', 'error', '-y', '-i', p + '.png', '-vf', 'scale=540:960:flags=lanczos', p + '.jpg']); fs.unlinkSync(p + '.png'); }
    await browser.close(); server.close(); return; }
  const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-vf', 'scale=1080:1920:flags=lanczos,format=yuv420p',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '8', '-tune', 'animation', '-r', String(FPS), path.join(HERE, 'out', 'reel.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(TEND * FPS);
  for (let f = 0; f < N; f++) { const b = await grab(f / FPS); if (!enc.stdin.write(b)) await new Promise(r => enc.stdin.once('drain', r)); if (f % 60 === 0) console.log(`frame ${f}/${N}`); }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await browser.close(); server.close(); console.log(`out/reel.mp4: ${N} frames`);
})();
