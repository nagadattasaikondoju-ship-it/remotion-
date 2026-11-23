// Shared anime primitives, cut from ../sushma-gum-anime/anime.html (Pink in the Sink). Needs globals X (2D context) and INK.
// ---------- math ----------
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const lerp = (a, b, k) => a + (b - a) * k;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eio = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const eo = k => 1 - Math.pow(1 - k, 3);
const back = k => { const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const hash = (i, k = 0) => { const s = Math.sin(i * 12.9898 + k * 78.233) * 43758.5453; return s - Math.floor(s); };
const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
const mix = (a, b, k) => { const A = hex(a), B = hex(b); return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], k))).join(',')})`; };
const shake = (t, t0, dur, amp) => { const k = seg(t, t0, t0 + dur); if (k <= 0 || k >= 1) return [0, 0]; const a = amp * (1 - k);
  const f = Math.floor(t * 30); return [(hash(f, 1) - .5) * 2 * a, (hash(f, 2) - .5) * 2 * a]; };

// ---------- primitives ----------
function star4(x, y, r, col, rot = 0) {
  X.save(); X.translate(x, y); X.rotate(rot); X.beginPath();
  for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, rr = i % 2 ? r * .22 : r; X.lineTo(Math.cos(a) * rr, Math.sin(a) * rr); }
  X.closePath(); X.fillStyle = col; X.fill(); X.restore();
}
function sparkles(t, cx, cy, rx, ry, n, seed, col = '#FFFFFF', size = 26) {
  for (let i = 0; i < n; i++) {
    const ph = hash(i, seed) * 6.28, sp = 2 + hash(i, seed + 1) * 2, k = .5 + .5 * Math.sin(t * sp + ph);
    if (k < .15) continue;
    star4(cx + (hash(i, seed + 2) - .5) * 2 * rx, cy + (hash(i, seed + 3) - .5) * 2 * ry, size * k * (.6 + .6 * hash(i, seed + 4)), col, t * .5 + ph);
  }
}
function drop(x, y, r, col, hi = '#FFFFFF') {   // teardrop, point up
  X.beginPath(); X.moveTo(x, y - r * 1.9); X.bezierCurveTo(x + r * .3, y - r * 1.2, x + r, y - r * .5, x + r, y);
  X.arc(x, y, r, 0, Math.PI); X.bezierCurveTo(x - r, y - r * .5, x - r * .3, y - r * 1.2, x, y - r * 1.9); X.closePath();
  X.fillStyle = col; X.fill(); X.lineWidth = Math.max(3, r * .22); X.strokeStyle = INK; X.stroke();
  X.beginPath(); X.ellipse(x - r * .38, y - r * .15, r * .18, r * .32, -.4, 0, 6.28); X.fillStyle = hi; X.fill();
}
function txt(s, x, y, size, fill, stroke, sw, font = 'Bangers', rot = 0, align = 'center', shadow = true) {
  X.save(); X.translate(x, y); X.rotate(rot); X.font = `${font === 'MB' ? '900 ' : ''}${size}px ${font}`; X.textAlign = align; X.textBaseline = 'middle';
  X.lineJoin = 'round'; X.miterLimit = 2;
  if (shadow) { X.fillStyle = 'rgba(10,12,40,.45)'; X.fillText(s, 6, 9); }
  if (sw) { X.lineWidth = sw * 1.8; X.strokeStyle = INK; X.strokeText(s, 0, 0); X.lineWidth = sw; X.strokeStyle = stroke; X.strokeText(s, 0, 0); }
  X.fillStyle = fill; X.fillText(s, 0, 0); X.restore();
}
function speedLines(t, cx, cy, r0, n, col, alpha, seed = 0) {
  const f = Math.floor(t * 15); X.save(); X.globalAlpha = alpha; X.fillStyle = col;
  for (let i = 0; i < n; i++) {
    const a = hash(i, f + seed) * 6.2832, w = .004 + hash(i, f + 7) * .012, r1 = r0 + hash(i, f + 3) * 260;
    X.beginPath(); X.moveTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1);
    X.lineTo(cx + Math.cos(a - w) * 2400, cy + Math.sin(a - w) * 2400); X.lineTo(cx + Math.cos(a + w) * 2400, cy + Math.sin(a + w) * 2400); X.fill();
  }
  X.restore();
}

// ---------- sky + clouds (cel shaded) ----------
const CLOUDS = [[120, 760, 1.25, .010], [620, 640, 1.6, .006], [980, 820, 1.1, .013], [320, 420, .8, .018], [860, 330, .75, .015]];
function cloud(x, y, s, base, shade) {
  const P = [[0, 0, 95], [-110, 25, 70], [110, 30, 75], [-55, -55, 70], [60, -50, 80], [-190, 55, 45], [195, 60, 50], [5, -105, 55]];
  X.fillStyle = shade; for (const [dx, dy, r] of P) { X.beginPath(); X.arc(x + dx * s, y + dy * s, r * s, 0, 6.28); X.fill(); }
  X.fillStyle = base; for (const [dx, dy, r] of P) { X.beginPath(); X.arc(x + (dx - 10) * s, y + (dy - 16) * s, r * s * .93, 0, 6.28); X.fill(); }
}
function sky(t, mood, hero) {
  // mood 0 = bright day, 1 = danger dusk. hero = golden light from above
  const g = X.createLinearGradient(0, -400, 0, 1500);
  g.addColorStop(0, mix('#1C6FE0', '#2A1650', mood)); g.addColorStop(.55, mix('#53AEF6', '#8C2F6B', mood)); g.addColorStop(1, mix('#B7E4FF', '#F07A6A', mood));
  X.fillStyle = g; X.fillRect(-600, -800, 2400, 2600);
  if (hero > 0) {
    X.save(); X.globalAlpha = hero; const rg = X.createRadialGradient(540, 420, 40, 540, 420, 1300);
    rg.addColorStop(0, '#FFF6C8'); rg.addColorStop(.35, 'rgba(255,214,110,.75)'); rg.addColorStop(1, 'rgba(80,150,255,0)');
    X.fillStyle = rg; X.fillRect(-600, -800, 2400, 2600);
    X.globalAlpha = hero * .35; X.fillStyle = '#FFFFFF';
    for (let i = 0; i < 18; i++) { const a = i / 18 * 6.283 + t * .25; X.beginPath(); X.moveTo(540, 420);
      X.lineTo(540 + Math.cos(a - .05) * 2600, 420 + Math.sin(a - .05) * 2600); X.lineTo(540 + Math.cos(a + .05) * 2600, 420 + Math.sin(a + .05) * 2600); X.fill(); }
    X.restore();
  }
  for (const [x, y, s, v] of CLOUDS) {
    const xx = ((x + t * v * 900) % 1500 + 1500) % 1500 - 210;
    cloud(xx, y, s, mix('#FFFFFF', '#F7C6D9', mood), mix('#C8DDF4', '#9B5A8F', mood));
  }
}
function sun(t, a) {
  if (a <= 0) return; X.save(); X.globalAlpha = a; const x = 860, y = 300;
  const rg = X.createRadialGradient(x, y, 10, x, y, 420); rg.addColorStop(0, 'rgba(255,255,240,1)'); rg.addColorStop(.2, 'rgba(255,240,180,.7)'); rg.addColorStop(1, 'rgba(255,240,180,0)');
  X.fillStyle = rg; X.beginPath(); X.arc(x, y, 420, 0, 6.28); X.fill();
  // lens flare dots towards centre
  [[.35, 40, 'rgba(255,200,120,.35)'], [.6, 22, 'rgba(140,220,255,.4)'], [.85, 60, 'rgba(255,255,255,.18)']].forEach(([k, r, c]) => {
    X.fillStyle = c; X.beginPath(); X.arc(lerp(x, 300, k), lerp(y, 1100, k), r, 0, 6.28); X.fill(); });
  X.restore();
}

// ---------- the tooth ----------
function toothPath(s) {
  X.beginPath(); X.moveTo(-140 * s, 0);
  X.bezierCurveTo(-175 * s, -80 * s, -185 * s, -230 * s, -150 * s, -290 * s);
  X.bezierCurveTo(-125 * s, -338 * s, -70 * s, -348 * s, -40 * s, -318 * s);
  X.bezierCurveTo(-15 * s, -298 * s, 15 * s, -298 * s, 40 * s, -318 * s);
  X.bezierCurveTo(70 * s, -348 * s, 125 * s, -338 * s, 150 * s, -290 * s);
  X.bezierCurveTo(185 * s, -230 * s, 175 * s, -80 * s, 140 * s, 0);
  X.bezierCurveTo(130 * s, 80 * s, 120 * s, 170 * s, 95 * s, 215 * s);
  X.bezierCurveTo(80 * s, 242 * s, 50 * s, 237 * s, 45 * s, 205 * s);
  X.bezierCurveTo(35 * s, 140 * s, 25 * s, 80 * s, 0, 72 * s);
  X.bezierCurveTo(-25 * s, 80 * s, -35 * s, 140 * s, -45 * s, 205 * s);
  X.bezierCurveTo(-50 * s, 237 * s, -80 * s, 242 * s, -95 * s, 215 * s);
  X.bezierCurveTo(-120 * s, 170 * s, -130 * s, 80 * s, -140 * s, 0); X.closePath();
}
function arm(sx, sy, a1, a2, s, side, flex) {
  const l1 = 70 * s, l2 = 62 * s;
  const ex = sx + Math.cos(a1) * l1, ey = sy + Math.sin(a1) * l1, hx = ex + Math.cos(a2) * l2, hy = ey + Math.sin(a2) * l2;
  for (const [w, c] of [[34 * s, INK], [22 * s, '#FFFFFF']]) {
    X.lineCap = 'round'; X.lineJoin = 'round'; X.lineWidth = w; X.strokeStyle = c;
    X.beginPath(); X.moveTo(sx, sy); X.lineTo(ex, ey); X.lineTo(hx, hy); X.stroke();
  }
  if (flex) { X.beginPath(); X.arc(lerp(sx, ex, .55) - side * 2 * s, lerp(sy, ey, .55) - 14 * s, 16 * s, 0, 6.28); X.fillStyle = '#FFFFFF'; X.fill();
    X.lineWidth = 5 * s; X.strokeStyle = INK; X.stroke(); }
  X.beginPath(); X.arc(hx, hy, 19 * s, 0, 6.28); X.fillStyle = '#FFFFFF'; X.fill(); X.lineWidth = 6 * s; X.strokeStyle = INK; X.stroke();
}
function eye(x, y, s, type, blink, lx, ly, side) {
  X.save(); X.translate(x, y);
  X.lineCap = 'round'; X.lineJoin = 'round';
  if (type === 'happy' || blink > .92) {          // ^ ^  (closed happy arcs)
    X.lineWidth = 9 * s; X.strokeStyle = INK; X.beginPath(); X.arc(0, 8 * s, 22 * s, Math.PI * 1.1, Math.PI * 1.9); X.stroke(); X.restore(); return;
  }
  if (type === 'closed') { X.lineWidth = 8 * s; X.strokeStyle = INK; X.beginPath(); X.moveTo(-22 * s, 0); X.quadraticCurveTo(0, 10 * s, 22 * s, 0); X.stroke(); X.restore(); return; }
  if (type === 'wink' && side > 0) { X.lineWidth = 9 * s; X.strokeStyle = INK; X.beginPath(); X.moveTo(-22 * s, 4 * s); X.lineTo(16 * s, -6 * s); X.moveTo(-22 * s, 4 * s); X.lineTo(16 * s, 14 * s); X.stroke(); X.restore(); return; }
  if (type === 'panic') {                          // spiral eyes
    X.lineWidth = 6 * s; X.strokeStyle = INK; X.beginPath();
    for (let a = 0; a < 15; a += .2) { const r = a * 2.1 * s; X.lineTo(Math.cos(a + side) * r, Math.sin(a + side) * r); } X.stroke(); X.restore(); return;
  }
  const ry = 38 * s * (1 - blink), rx = 28 * s;
  X.beginPath(); X.ellipse(0, 0, rx + 6 * s, ry + 6 * s, 0, 0, 6.28); X.fillStyle = '#FFFFFF'; X.fill();
  if (type === 'shock') {                          // tiny pupils in white eyes
    X.lineWidth = 6 * s; X.strokeStyle = INK; X.stroke(); X.beginPath(); X.arc(lx * 4 * s, ly * 4 * s, 8 * s, 0, 6.28); X.fillStyle = INK; X.fill(); X.restore(); return;
  }
  X.beginPath(); X.ellipse(lx * 5 * s, ly * 5 * s, rx, ry, 0, 0, 6.28); X.save(); X.clip();
  const g = X.createLinearGradient(0, -ry, 0, ry); g.addColorStop(0, '#0E1230'); g.addColorStop(.45, '#1E2C78'); g.addColorStop(1, '#4C8DF0');
  X.fillStyle = g; X.fillRect(-rx * 2, -ry * 2, rx * 4, ry * 4); X.restore();
  if (ry > 6 * s) {
    if (type === 'sparkle') { star4(lx * 5 * s - 8 * s, ly * 5 * s - 12 * s, 22 * s, '#FFFFFF', .2); star4(lx * 5 * s + 10 * s, ly * 5 * s + 14 * s, 10 * s, '#FFFFFF'); }
    else { X.fillStyle = '#FFFFFF'; X.beginPath(); X.arc(lx * 5 * s - 9 * s, ly * 5 * s - 13 * s * (1 - blink), 10 * s, 0, 6.28); X.fill();
      X.beginPath(); X.arc(lx * 5 * s + 10 * s, ly * 5 * s + 14 * s * (1 - blink), 5 * s, 0, 6.28); X.fill(); }
  }
  X.restore();
}
function face(s, ex, t, big) {
  const blink = (() => { const p = (t + (big ? 0 : 1.3)) % 3.1; return p < .12 ? Math.sin(p / .12 * Math.PI) : 0; })();
  const look = ex.look || [0, 0];
  for (const side of [-1, 1]) eye(side * 58 * s, -175 * s, s, ex.eyes, blink, look[0], look[1], side);
  // brows for worried/angry/determined
  if (ex.brows) { X.lineWidth = 7 * s; X.strokeStyle = INK; X.lineCap = 'round';
    for (const side of [-1, 1]) { X.beginPath(); const tilt = ex.brows === 'worried' ? -1 : 1;
      X.moveTo(side * 30 * s, -232 * s + tilt * 8 * s); X.lineTo(side * 82 * s, -232 * s - tilt * 8 * s); X.stroke(); } }
  // blush
  X.fillStyle = 'rgba(255,120,150,.55)';
  for (const side of [-1, 1]) { X.beginPath(); X.ellipse(side * 98 * s, -128 * s, 30 * s, 16 * s, 0, 0, 6.28); X.fill();
    X.strokeStyle = 'rgba(230,70,110,.7)'; X.lineWidth = 3.5 * s; for (let k = -1; k <= 1; k++) { X.beginPath(); X.moveTo(side * 98 * s + k * 14 * s - 6 * s, -120 * s); X.lineTo(side * 98 * s + k * 14 * s + 4 * s, -136 * s); X.stroke(); } }
  // mouth
  X.lineWidth = 7 * s; X.strokeStyle = INK; X.lineCap = 'round'; X.lineJoin = 'round';
  const m = ex.mouth;
  if (m === 'smile' || m === 'grin') {
    X.beginPath(); X.moveTo(-26 * s, -122 * s); X.quadraticCurveTo(0, (m === 'grin' ? -78 : -96) * s, 26 * s, -122 * s); X.closePath();
    X.fillStyle = '#C72F4E'; X.fill(); X.stroke(); X.save(); X.clip(); X.fillStyle = '#FF8FA8'; X.beginPath(); X.ellipse(0, -92 * s, 16 * s, 12 * s, 0, 0, 6.28); X.fill(); X.restore();
  } else if (m === 'o') { X.beginPath(); X.ellipse(0, -112 * s, 11 * s, 14 * s, 0, 0, 6.28); X.fillStyle = '#C72F4E'; X.fill(); X.stroke(); }
  else if (m === 'shock') { X.beginPath(); X.ellipse(0, -108 * s, 18 * s, 26 * s, 0, 0, 6.28); X.fillStyle = '#C72F4E'; X.fill(); X.stroke(); }
  else if (m === 'wavy') { X.beginPath(); for (let i = 0; i <= 12; i++) X.lineTo((-30 + i * 5) * s, -112 * s + Math.sin(i * 1.6 + t * 20) * 6 * s); X.stroke(); }
  else if (m === 'flat') { X.beginPath(); X.moveTo(-18 * s, -114 * s); X.lineTo(18 * s, -114 * s); X.stroke(); }
}
function tooth(x, y, s, ex, t, opt = {}) {
  X.save(); X.translate(x, y);
  if (opt.rot) { X.translate(0, 220 * s); X.rotate(opt.rot); X.translate(0, -220 * s); }
  if (opt.sq) X.scale(1 / opt.sq, opt.sq);
  // arms behind? no: arms in front, drawn after body
  toothPath(s); X.fillStyle = '#BFD5F0'; X.fill();               // shadow tone
  X.save(); toothPath(s); X.clip();
  X.translate(-30 * s, -20 * s); toothPath(s); X.fillStyle = '#F7FBFF'; X.fill(); X.translate(30 * s, 20 * s);
  X.fillStyle = '#E9D29A'; X.fillRect(-250 * s, 0, 500 * s, 300 * s);   // root (only seen when the gum pulls back)
  X.fillStyle = '#D4B676'; X.fillRect(40 * s, 0, 200 * s, 300 * s);
  X.fillStyle = '#FFFFFF'; X.beginPath(); X.ellipse(-95 * s, -235 * s, 18 * s, 48 * s, .45, 0, 6.28); X.fill();   // gloss
  X.beginPath(); X.arc(-62 * s, -292 * s, 9 * s, 0, 6.28); X.fill();
  X.restore();
  toothPath(s); X.lineWidth = 10 * s; X.strokeStyle = INK; X.lineJoin = 'round'; X.stroke();
  face(s, ex, t, opt.big);
  if (opt.arms) { const [l1, l2, r1, r2, flex] = opt.arms; arm(-160 * s, -150 * s, l1, l2, s, -1, false); arm(160 * s, -150 * s, r1, r2, s, 1, flex); }
  X.restore();
}

function bubble(x, y, w, h, tx, ty, label, k) {
  if (k <= 0) return; X.save(); X.translate(x, y); X.scale(back(k), back(k));
  X.fillStyle = '#FFFFFF'; X.strokeStyle = INK; X.lineWidth = 7;
  X.beginPath(); X.ellipse(0, 0, w / 2, h / 2, 0, 0, 6.28); X.fill(); X.stroke();
  X.beginPath(); X.moveTo(-18, h / 2 - 10); X.lineTo(tx - x, ty - y); X.lineTo(18, h / 2 - 6); X.fill(); X.stroke();
  X.fillStyle = '#FFFFFF'; X.fillRect(-16, h / 2 - 16, 32, 12);
  X.fillStyle = INK; X.font = '58px Bangers'; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText(label, 0, 4);
  X.restore();
}
function note(x, y, s, col) {
  X.save(); X.translate(x, y); X.scale(s, s); X.fillStyle = col; X.strokeStyle = col; X.lineWidth = 7;
  X.beginPath(); X.ellipse(0, 0, 16, 12, -.4, 0, 6.28); X.fill(); X.beginPath(); X.moveTo(13, -4); X.lineTo(13, -62); X.quadraticCurveTo(30, -50, 34, -30); X.stroke(); X.restore();
}

// ---------- hook scene: the sink ----------
function stamp(t, t0, s, x, y, size, fill, rot, dur = 99) {
  const k = seg(t, t0, t0 + .16); if (k <= 0 || t > t0 + dur) return;
  const sh = shake(t, t0, .3, 10);
  X.save(); X.translate(x + sh[0], y + sh[1]); X.rotate(rot); X.scale(back(k) * (1 + (1 - k) * .6), back(k) * (1 + (1 - k) * .6));
  txt(s, 0, 0, size, fill, fill === '#FFFFFF' ? '#FF4F86' : '#FFFFFF', 16, 'Bangers', 0);
  X.restore();
}
