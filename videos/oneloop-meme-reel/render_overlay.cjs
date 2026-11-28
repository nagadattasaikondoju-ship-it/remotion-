// Render overlay.html (transparent) to a ProRes 4444 .mov with alpha.  env: OUT, FPS (30), TAG_ONLY=1, T0/T1 (seconds)
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path'), http = require('http'), { spawn } = require('child_process');
const HERE = __dirname, FPS = Number(process.env.FPS || 30);
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.ttf': 'font/ttf' };
const server = http.createServer((q, r) => { const p = path.join(HERE, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(p, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' }); r.end(d); }); });
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto(`http://127.0.0.1:${server.address().port}/overlay.html`); await page.waitForFunction(() => window.ready === true, null, { timeout: 120000 });
  if (process.env.TAG_ONLY) await page.evaluate(() => { window.TAG_ONLY = true; });
  if (process.argv[2] === '--stills') { for (const t of process.argv.slice(3).map(Number)) { await page.evaluate(t => window.seek(t), t);
      fs.writeFileSync(path.join(HERE, 'out', `ov_${t}.png`), await page.locator('#c').screenshot({ omitBackground: true })); } await browser.close(); server.close(); return; }
  const tend = await page.evaluate(() => window.TIMING.TEND), T0 = Number(process.env.T0 || 0), T1 = Number(process.env.T1 || tend);
  const enc = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', process.env.OUT || 'out/overlay.mov'], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round((T1 - T0) * FPS);
  for (let f = 0; f < n; f++) { await page.evaluate(t => window.seek(t), T0 + f / FPS); const b = await page.locator('#c').screenshot({ omitBackground: true });
    if (!enc.stdin.write(b)) await new Promise(r => enc.stdin.once('drain', r)); if (f % 90 === 0) console.log(`frame ${f}/${n}`); }
  enc.stdin.end(); await new Promise(r => enc.on('close', r)); await browser.close(); server.close(); console.log(`done ${n} frames`);
})();
