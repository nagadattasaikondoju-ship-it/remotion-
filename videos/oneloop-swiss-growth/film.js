// One Loop — The Growth Path. Swiss Motion Graphics, 1080×1920, 30 s, 120 BPM (beat 0.5 s = 12 frames at 24 fps).
// The grid means something: four columns = the four parts of a business (website, marketing, operations, brand);
// the gutters between them are the gaps where growth leaks. One copper thread (the only signal colour, the exception:
// linear, never snapped) runs the gaps rule by rule, closes into one loop, leaves the grid and becomes the One Loop mark.
export const W = 1080, H = 1920, DUR = 30;
export const BPM = 120, BEAT = 60 / BPM, E8 = BEAT / 2;
const C = { page: '#111111', paper: '#1C1C1B', ink: '#E1E0CC', line: '#2A2A28', g2: '#3C3C39', g3: '#77766F', cop: '#E59C69' };

/* ---------- time: the only two curves ---------- */
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
function cubicBezier(x1, y1, x2, y2) {
  const bx = u => 3 * (1 - u) * (1 - u) * u * x1 + 3 * (1 - u) * u * u * x2 + u * u * u;
  const by = u => 3 * (1 - u) * (1 - u) * u * y1 + 3 * (1 - u) * u * u * y2 + u * u * u;
  return t => { if (t <= 0) return 0; if (t >= 1) return 1; let lo = 0, hi = 1, u = t;
    for (let i = 0; i < 30; i++) { const x = bx(u); if (Math.abs(x - t) < 1e-6) break; if (x < t) lo = u; else hi = u; u = (lo + hi) / 2; } return by(u); };
}
const E = cubicBezier(.7, 0, .2, 1);
const snap = (t, t1, d = E8) => E(seg(t, t1 - d, t1));          // starts d early, lands on t1
function track(keys) {                                           // [[t_arrive, [values], d?], …]
  return t => { let v = keys[0][1];
    for (let i = 1; i < keys.length; i++) { const [t1, v1, d = BEAT] = keys[i]; if (t < t1 - d) break;
      const p = snap(t, t1, d); v = v.map((x, j) => lerp(x, v1[j], p)); if (p < 1) break; }
    return v; };
}

/* ---------- frame grid: 72 px margins, 4 artifact columns, 36 px gutters ---------- */
const M = 72, G = 36, CWD = (W - 2 * M - 3 * G) / 4;              // column 207 px
const colX = c => M + c * (CWD + G), gutX = k => colX(k) - G / 2;  // gutter k = between column k-1 and k
const AY0 = 1000, AY1 = 1720;                                     // artifact window on screen
const RH = 232, RG = 32, ROWS = 4, ALH = 24 + ROWS * (RH + RG);   // artifact rows (local coords)
const rowY = r => 24 + r * (RH + RG), seamY = r => rowY(r) + RH + RG / 2;
const LABELS = ['website', 'marketing', 'operations', 'brand'];

/* ---------- the rules ---------- */
const STEPS = [  // t = the beat the rule lands on
  { t: 4, n: '01', title: 'audit.', note: 'ad waste · conversion leakage' },
  { t: 8, n: '02', title: 'build.', note: 'sub-second loads · tracking' },
  { t: 12, n: '03', title: 'market.', note: 'search · shopping · meta' },
  { t: 16, n: '04', title: 'automate.', note: 'lead routing · self-correcting ai' },
  { t: 20, n: '05', title: 'scale.', note: 'one system, five markets' },
];
const MARKETS = ['australia', 'dubai', 'india', 'new zealand', 'uk'];   // oneloop.in footer: AU · AE · IN · NZ · UK

/* ---------- the copper thread: a polyline in artifact coords, drawn linearly (the exception never snaps) ---------- */
const XR = colX(3) + CWD + G / 2, XL = M - G / 2;
const PATH = [  // [x, y, t_start, t_end] of each segment's END point
  [gutX(1), 0, 0, 0],
  [gutX(1), seamY(0), 4.00, 4.75], [gutX(2), seamY(0), 4.75, 6.25],
  [gutX(2), seamY(1), 8.00, 8.75], [gutX(3), seamY(1), 8.75, 10.25],
  [gutX(3), seamY(2), 12.00, 12.75], [XR, seamY(2), 12.75, 14.25],
  [XR, seamY(3), 16.00, 16.50], [XL, seamY(3), 16.50, 17.75],
  [XL, 0, 17.75, 19.00], [gutX(1), 0, 19.00, 19.25],
];
function threadPoints(t) {         // the part of the thread drawn by time t (+ its head)
  const pts = [[PATH[0][0], PATH[0][1]]];
  for (let i = 1; i < PATH.length; i++) {
    const [x, y, a, b] = PATH[i], [px, py] = pts[pts.length - 1];
    if (t <= a) break;
    const p = seg(t, a, b); pts.push([lerp(px, x, p), lerp(py, y, p)]); if (p < 1) break;
  }
  return pts;
}
// leak marks (×) in the gutters, one per row; the thread cuts the one it passes, automation cuts the rest by distance
const LEAKS = [];
for (let k = 1; k <= 3; k++) for (let r = 0; r < ROWS; r++) LEAKS.push({ k, r, x: gutX(k), y: rowY(r) + RH / 2 });
const leakCut = l => {
  if (l.k === 1 && l.r === 0) return 4.40; if (l.k === 2 && l.r === 1) return 8.40; if (l.k === 3 && l.r === 2) return 12.40;
  const d = Math.hypot(l.x - XR, l.y - seamY(3)) / 260;            // ripple from the thread's corner, nearest first
  return 16.5 + Math.round(d * 2) * E8;
};

/* ---------- cells: outlined when audited, filled when built; automation fills the rest by distance ---------- */
const CELLS = [];
for (let r = 0; r < ROWS; r++) for (let c = 0; c < 4; c++) CELLS.push({ r, c });
const cellOutline = () => 4.5;                                    // audit outlines every cell (rippled below)
function cellFill(cell) {
  const key = { '1,0': 8.5, '2,1': 12.5, '3,2': 16.5 }[`${cell.r},${cell.c}`]; if (key) return key;
  const d = Math.hypot(colX(cell.c) + CWD / 2 - XR, rowY(cell.r) + RH / 2 - seamY(3)) / 260;
  return 16.75 + Math.round(d * 2) * E8;
}
const CHANNELS = ['search', 'shopping', 'meta', 'pmax'];           // inside the marketing block (oneloop.in)

/* ---------- camera for the artifact: screen = (px, py) + (p − (fx, fy)) · s ---------- */
const MINI = 0.17, MINI_W = (W - 2 * M) * MINI, MINI_GAP = (W - 2 * M - 5 * MINI_W) / 4, MINI_Y = 1130;
const miniX = i => M + i * (MINI_W + MINI_GAP);
const CAM = track([
  [0, [1, 0, 0, 0, AY0]],
  [4.0, [1.32, gutX(1), seamY(0), 330, AY0 + 300]],                 // push into the first gap
  [8.0, [1, 0, 256, 0, AY0]],                                        // hard pan down one row
  [12.0, [1, 0, 512, 0, AY0]],                                       // and one more
  [20.5, [MINI, M, 0, miniX(2), MINI_Y], BEAT],                      // pull out to a wall of five
]);
const CLIP = track([[0, [0, 720]], [8.0, [256, 976]], [12.0, [512, 1232]], [20.5, [0, ALH], BEAT]]);

/* ---------- type ---------- */
function font(g, w, size, ls = -0.02) { g.font = `${w} ${size}px Archivo`; g.letterSpacing = `${(ls * size).toFixed(2)}px`; }
// clip-reveal: rises out of a clip rect from below the baseline (pin 0→1), leaves upward (pout 0→1)
function reveal(g, s, x, base, size, pin, pout = 0, color = C.ink) {
  if (pin <= 0 || pout >= 1) return;
  g.save(); g.beginPath(); g.rect(x - 10, base - size * 1.02, W, size * 1.3); g.clip();
  g.fillStyle = color; g.fillText(s, x, base + (1 - pin) * size * 1.15 - pout * size * 1.15); g.restore();
}
let NUM = { size: 560, left: 0 };
export function measure(g) { font(g, 800, 560, -0.04); const m = g.measureText('0'); NUM = { size: 560, left: m.actualBoundingBoxLeft }; }

/* ---------- drawing ---------- */
const TEXTS_AT = [];
const pushText = (id, text, x0, y0, x1, y1) => TEXTS_AT.push({ id, text, x0, y0, x1, y1 });

function drawGridLines(g, t, a) {               // frame grid hairlines, very quiet
  if (a <= 0) return;
  g.fillStyle = C.line;
  for (let c = 0; c < 4; c++) { const x = colX(c); g.fillRect(x, 120, 1, 860 * a); g.fillRect(x + CWD, 120, 1, 860 * a); }
}

function drawArtifact(g, t, copyIndex, cam, clip, progressT) {  // t: clock for the leaving thread; progressT: the system's state
  const [s, fx, fy, px, py] = cam, S = (x, y) => [px + (x - fx) * s, py + (y - fy) * s];
  g.save(); g.translate(px - fx * s, py - fy * s); g.scale(s, s);
  g.beginPath(); g.rect(XL - 30, clip[0], XR - XL + 60, clip[1] - clip[0]); g.clip();
  const tt = progressT;   // the copies show the finished system
  // columns wipe up, one per beat
  for (let c = 0; c < 4; c++) {
    const p = snap(t, c * BEAT + BEAT, BEAT); if (p <= 0) continue;
    const top = lerp(clip[1], -30, p);
    g.fillStyle = C.paper; g.fillRect(colX(c), top, CWD, ALH + 60 - top);
  }
  // cells: audit outlines (ripple from the first gap), then fills
  CELLS.forEach(cell => {
    const x = colX(cell.c) + 14, y = rowY(cell.r) + 14, w = CWD - 28, h = RH - 28;
    const dO = Math.abs(cell.c - 0.5) + cell.r, po = snap(tt, cellOutline() + Math.round(dO) * E8 / 2, E8);
    const pf = snap(tt, cellFill(cell), E8);
    if (po > 0 && pf < 1) { g.strokeStyle = C.g2; g.lineWidth = 2; g.strokeRect(x, y + h * (1 - po), w, h * po); }
    if (pf > 0) {
      g.fillStyle = C.ink; g.fillRect(x, y + h * (1 - pf), w, h * pf + 1);       // wipe up, overdrawn 1 px
      if (cell.r === 2 && cell.c === 1 && pf >= 1) {                               // the marketing block: channels, overprinted
        font(g, 700, 26, -0.01); g.fillStyle = C.page;
        CHANNELS.forEach((w2, i) => { const pi = snap(tt, 12.75 + i * E8, E8); if (pi > 0) reveal(g, w2, x + 16, y + 44 + i * 40, 26, pi, 0, C.page); });
      }
    }
  });
  // leak marks in the gutters, knife-cut when fixed
  LEAKS.forEach(l => {
    const appear = snap(tt, 2.0 + (l.k - 1) * E8, E8); if (appear <= 0) return;
    const tc = leakCut(l), knife = seg(tt, tc - 0.12, tc), gone = snap(tt, tc + 0.12, 0.12);
    if (gone >= 1) return;
    const r = 9 * (1 - gone);
    g.strokeStyle = C.g3; g.lineWidth = 3; g.beginPath();
    g.moveTo(l.x - r, l.y - r * appear); g.lineTo(l.x + r, l.y + r * appear); g.moveTo(l.x + r, l.y - r * appear); g.lineTo(l.x - r, l.y + r * appear); g.stroke();
    if (knife > 0 && knife < 1 || (knife >= 1 && gone < 1)) { g.fillStyle = C.ink; g.fillRect(l.x - 16, l.y - 1, 32 * Math.min(1, knife), 2); }
  });
  // the thread
  const pts = threadPoints(tt), leave = copyIndex === 2 ? seg(t, 24.5, 26.0) : 0;
  if (tt >= 3.5 && leave === 0) {
    const dot = snap(tt, 3.5, E8);
    g.fillStyle = C.cop; g.beginPath(); g.arc(PATH[0][0], 0, 9 * dot, 0, Math.PI * 2); g.fill();
  }
  if (pts.length > 1) {
    g.strokeStyle = C.cop; g.lineWidth = Math.max(9, 3.2 / s); g.lineJoin = 'miter'; g.lineCap = 'square';
    if (leave > 0) strokePart(g, pts, cum(pts), leave, 1);          // the thread leaves the grid from its start
    else { g.beginPath(); pts.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y))); g.stroke(); }
  }
  g.restore();
  return S;
}

// the One Loop mark (traced artwork, logo.js): the copper line traces the figure-eight, then snaps into the logo
const RL = LOGO.meta.rl, SW = LOGO.meta.sw, TH = Math.asin(2 * RL);
function cum(pts) { const c = [0]; for (let i = 1; i < pts.length; i++) c.push(c[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])); return c; }
function resample(pts, n) { const c = cum(pts), L = c[c.length - 1], out = []; let j = 0;
  for (let i = 0; i < n; i++) { const s = (L * i) / (n - 1); while (j < c.length - 2 && c[j + 1] < s) j++;
    const u = (s - c[j]) / (c[j + 1] - c[j] || 1); out.push([lerp(pts[j][0], pts[j + 1][0], u), lerp(pts[j][1], pts[j + 1][1], u)]); } return out; }
function strokePart(g, pts, c, s0, s1) { const L = c[c.length - 1], a = s0 * L, b = s1 * L; if (b - a < 1e-6) return; g.beginPath(); let st = false;
  for (let i = 0; i < pts.length - 1; i++) { if (c[i + 1] < a || c[i] > b) continue;
    const u0 = clamp((a - c[i]) / (c[i + 1] - c[i] || 1)), u1 = clamp((b - c[i]) / (c[i + 1] - c[i] || 1));
    const p0 = [lerp(pts[i][0], pts[i + 1][0], u0), lerp(pts[i][1], pts[i + 1][1], u0)], p1 = [lerp(pts[i][0], pts[i + 1][0], u1), lerp(pts[i][1], pts[i + 1][1], u1)];
    if (!st) { g.moveTo(p0[0], p0[1]); st = true; } g.lineTo(p1[0], p1[1]); } g.stroke(); }
function fig8Raw() { const p = [], sg = (a, b, m) => { for (let i = 0; i < m; i++) { const u = i / m; p.push([lerp(a[0], b[0], u), lerp(a[1], b[1], u)]); } };
  const arc = (cx, a0, a1, m) => { for (let i = 0; i < m; i++) { const a = lerp(a0, a1, i / m); p.push([cx + RL * Math.cos(a), RL * Math.sin(a)]); } };
  const sn = Math.sin(TH), cs = Math.cos(TH), T = [-0.5 * cs * cs, 0.5 * sn * cs], a0 = Math.PI / 2 - TH, span = Math.PI + 2 * TH;
  sg([0, 0], T, 40); arc(-0.5, a0, a0 + span, 280); sg([T[0], -T[1]], [0, 0], 40); sg([0, 0], [-T[0], T[1]], 40); arc(0.5, Math.PI - a0, Math.PI - a0 - span, 280); sg([-T[0], -T[1]], [0, 0], 41); return p; }
const FIG8 = resample(fig8Raw(), 480), FIG8C = cum(FIG8);
const DL = 0.5 * Math.cos(TH), AL = (Math.PI + 2 * TH) * RL, TL = 4 * DL + 2 * AL;
const FR = [0, DL / TL, (DL + AL) / TL, (2 * DL + AL) / TL, (3 * DL + AL) / TL, (3 * DL + 2 * AL) / TL, 1];
function pathOf(g, polys, S) { g.beginPath(); for (const poly of polys) { poly.forEach(([x, y], i) => (i ? g.lineTo(x * S, y * S) : g.moveTo(x * S, y * S))); g.closePath(); } }
function markDraw(g, S, t, a, snapT) {
  const pts = FIG8.map(([x, y]) => [x * S, y * S]), cc = FIG8C.map(v => v * S);
  if (t < snapT) { g.strokeStyle = C.cop; g.lineWidth = SW * S; g.lineCap = 'butt'; strokePart(g, pts, cc, 0, seg(t, a, snapT)); return; }   // linear: the exception
  g.fillStyle = C.cop; for (const gl of [LOGO.CL, LOGO.CR]) { pathOf(g, gl, S); g.fill('evenodd'); }
  const r = snap(t, snapT + 0.25, 0.25);                     // diagonals retract into the crossing
  if (r < 1) { g.strokeStyle = C.cop; g.lineWidth = SW * S;
    strokePart(g, pts, cc, 0, FR[1] * (1 - r)); strokePart(g, pts, cc, FR[2] + (FR[3] - FR[2]) * r, FR[3]);
    strokePart(g, pts, cc, FR[3], FR[3] + (FR[4] - FR[3]) * (1 - r)); strokePart(g, pts, cc, FR[5] + (FR[6] - FR[5]) * r, 1); }
  const k = snap(t, snapT + 0.25, 0.25); if (k > 0) { g.save(); g.rotate((Math.PI / 2) * (1 - k)); g.scale(k, k); pathOf(g, LOGO.X, S); g.fillStyle = C.cop; g.fill('evenodd'); g.restore(); }
}
function lockup(g, cx, cy, S, t) {
  const Mt = LOGO.meta;
  g.save(); g.translate(cx, cy); markDraw(g, S, t, 24.5, 26.0); g.restore();
  const tw = snap(t, 26.5, BEAT), tt2 = seg(t, 26.75, 27.25);        // wordmark wipes up on the beat; tagline drawn left→right
  if (tw > 0) { const top = cy + Mt.wordTop * S, h = (Mt.wordBot - Mt.wordTop) * S;
    g.save(); g.beginPath(); g.rect(0, top - 3, W, h + 6); g.clip(); g.translate(cx, cy + (1 - tw) * h * 1.15); g.fillStyle = C.ink;
    LOGO.WORD.forEach(L => { pathOf(g, L.paths, S); g.fill('evenodd'); }); g.restore(); }
  if (tt2 > 0) { const x0 = cx + Mt.left * S - 10;
    g.save(); g.beginPath(); g.rect(x0, cy + Mt.tagTop * S - 6, (Mt.right - Mt.left) * S * tt2 + 20, (Mt.tagBot - Mt.tagTop) * S + 12); g.clip();
    g.translate(cx, cy); pathOf(g, LOGO.TAGW, S); g.fillStyle = C.ink; g.fill('evenodd'); pathOf(g, LOGO.TAGC, S); g.fillStyle = C.cop; g.fill(); g.restore(); }
}

function drawProgramme(g, t, cut) {
  // opening headline: One Loop's own thesis ("growth breaks down in the gaps…")
  const out0 = seg(t, 3.25, 3.5);
  font(g, 800, 118);
  reveal(g, 'growth breaks', M, 560, 118, snap(t, 0.5, BEAT), out0);
  reveal(g, 'in the gaps.', M, 690, 118, snap(t, 1.0, BEAT), out0);
  if (t < 3.25) { pushText('h1', 'growth breaks', M, 450, 900, 590); pushText('h2', 'in the gaps.', M, 580, 800, 720); }
  // the rules: giant numeral climbing a module at a time, title, note
  STEPS.forEach((st, i) => {
    const next = STEPS[i + 1], tEnd = next ? next.t : 99;
    if (t < st.t - BEAT || t > tEnd) return;
    const pin = snap(t, st.t, st.t === 4 ? E8 : BEAT), pout = next ? snap(t, next.t, BEAT) : 0;
    font(g, 800, NUM.size, -0.04);
    reveal(g, st.n, M + NUM.left, 640, NUM.size * 0.74, pin, pout);
    font(g, 800, 112);
    const tin = snap(t, st.t + E8, E8), tout = next ? seg(t, next.t - E8, next.t) : 0;
    reveal(g, st.title, M, 800, 112, tin, tout);
    const nin = snap(t, st.t + E8, E8);                       // the note lands with the title
    if (nin > 0 && tout < 1) {
      g.fillStyle = C.g2; g.fillRect(M, 846, (W - 2 * M) * Math.min(1, seg(t, st.t, st.t + E8)), 1);   // rule drawn linearly
      font(g, 500, 32, 0); reveal(g, st.note, M, 900, 32, nin, tout, C.ink);
    }
    if (t >= st.t + E8 && t < tEnd - E8) { pushText('n' + i, st.n + ' ' + st.title, M, 220, 900, 830); pushText('note' + i, st.note, M, 866, 1008, 910); }
  });
  // corner notes: the programme's technical voice
  font(g, 500, 22, 0); g.fillStyle = C.g3;
  g.fillText('one loop — the growth path', M, 96);
  const rule = t < 4 ? 'the problem' : t < 24 ? `rule ${STEPS[Math.min(4, Math.floor((t - 4) / 4))].n} / 05` : '';
  if (rule) g.fillText(rule, colX(2), 96);
}

function drawLabels(g, t, a) {       // caption row under the artifact: what the columns mean
  if (a <= 0) return;
  g.fillStyle = C.g2; g.fillRect(M, 1740, (W - 2 * M) * a, 1);
  font(g, 500, 26, 0);
  LABELS.forEach((s, c) => reveal(g, s, colX(c), 1782, 26, snap(t, (c + 1) * BEAT + E8, E8)));
  font(g, 500, 22, 0); g.fillStyle = C.g3;
  g.fillText('4 col · 36 px gutter', M, 1856);
  const bar = Math.floor(t / 2) + 1, beat = Math.floor((t % 2) / BEAT) + 1;
  g.fillText(`bar ${String(bar).padStart(2, '0')}.${beat} · 120 bpm`, colX(2), 1856);
}

export function renderFilm(g, t) {
  TEXTS_AT.length = 0;
  g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = C.page; g.fillRect(0, 0, W, H);
  const frozen = t >= 24 && t < 24.5 ? 24 : t;                    // the hard stop: one beat where nothing moves
  const T = Math.min(frozen, 24);                                  // the system itself stops at 24
  // knife cut at 25.75 → 26.0 (a line crosses), then everything collapses to its midline by 26.25
  const knife = seg(t, 25.75, 26.0), coll = snap(t, 26.25, 0.25);
  const sysVisible = coll < 1;
  if (sysVisible) {
    g.save();
    const WMID = MINI_Y + ALH * MINI / 2; if (coll > 0) { g.translate(0, WMID); g.scale(1, 1 - coll); g.translate(0, -WMID); }
    drawGridLines(g, T, snap(T, 0.5, BEAT) * (T < 20 ? 1 : 1 - snap(T, 20.5, BEAT)));
    const pk = seg(t, 24.25, 24.5), pc = snap(t, 24.75, 0.25);
    if (pc < 1) { g.save(); if (pc > 0) { g.translate(0, 560); g.scale(1, 1 - pc); g.translate(0, -560); } drawProgramme(g, T, coll); g.restore(); }
    if (pk > 0 && pc < 1) { g.fillStyle = C.ink; g.fillRect(0, 559, W * pk, 2); }
    const cam = CAM(T), clip = CLIP(T);
    const wall = snap(T, 20.5, BEAT);
    if (wall > 0) {             // the other four markets wipe in, nearest first
      [1, 3, 0, 4].forEach((i, k) => { const p = snap(T, 20.75 + Math.floor(k / 2) * E8, E8); if (p <= 0) return;
        g.save(); g.beginPath(); g.rect(miniX(i) - 4, MINI_Y + ALH * MINI * (1 - p), MINI_W + 8, ALH * MINI * p + 4); g.clip();
        drawArtifact(g, 99, i, [MINI, M, 0, miniX(i), MINI_Y], [0, ALH], 99); g.restore(); });
      font(g, 500, 22, 0);
      MARKETS.forEach((m, i) => reveal(g, m, miniX(i), MINI_Y + ALH * MINI + 44, 22, snap(T, 21.25 + i * E8 / 2, E8)));
      if (T >= 21.5) MARKETS.forEach((m, i) => pushText('m' + i, m, miniX(i), MINI_Y + ALH * MINI + 20, miniX(i) + MINI_W, MINI_Y + ALH * MINI + 50));
    }
    // the main artifact (becomes market 3: india, home); its thread is the one that leaves
        drawArtifact(g, t >= 24.5 ? t : T, 2, cam, clip, T);
    drawLabels(g, T, snap(T, 0.5, BEAT) * (1 - snap(T, 20.5, BEAT)));
    if (T < 20.25) LABELS.forEach((s, c) => pushText('l' + c, s, colX(c), 1758, colX(c) + CWD, 1790));
    g.restore();
    if (knife > 0 && coll < 1) { g.fillStyle = C.ink; g.fillRect(0, MINI_Y + ALH * MINI / 2 - 1, W * knife, 2); }
  }
  // the end: the thread leaves the grid and becomes the mark
  if (t >= 24.5) {
    const S = 380, cx = M + 1.0476 * S, cy = 760;
    lockup(g, cx, cy, S, t);
    const r = snap(t, 27.0, BEAT / 2);
    g.fillStyle = C.g2; g.fillRect(M, 1520, (W - 2 * M) * seg(t, 26.75, 27.25), 1);
    font(g, 800, 64); reveal(g, 'audit my business', M, 1610, 64, snap(t, 27.25, E8));
    font(g, 500, 34, 0); reveal(g, 'oneloop.in', M, 1676, 34, snap(t, 27.5, E8), 0, C.g3);
    if (t >= 27.25) pushText('cta', 'audit my business', M, 1550, 700, 1625);
    if (t >= 27.5) pushText('url', 'oneloop.in', M, 1645, 300, 1690);
  }
  return TEXTS_AT.slice();
}

/* ---------- sound events for the mixer (every visible action has a sound) ---------- */
export function buildEvents() {
  const ev = [];
  for (let c = 0; c < 4; c++) ev.push({ t: (c + 1) * BEAT - BEAT, type: 'paper_slap', c });
  ev.push({ t: 0.5, type: 'clack' }, { t: 1.0, type: 'clack' });
  ev.push({ t: 2.0, type: 'tick' }, { t: 2.25, type: 'tick' }, { t: 2.5, type: 'tick' });
  ev.push({ t: 3.5, type: 'dot' });
  STEPS.forEach(s => { ev.push({ t: s.t, type: 'numeral' }, { t: s.t + E8, type: 'clack' }); });
  for (let i = 1; i < PATH.length; i++) ev.push({ t: PATH[i][2], type: 'pen', dur: PATH[i][3] - PATH[i][2] });
  LEAKS.forEach(l => ev.push({ t: leakCut(l), type: 'snick' }));
  CELLS.forEach(c => { const f = cellFill(c); if (f < 20) ev.push({ t: f, type: 'block' }); });
  ev.push({ t: 20.5, type: 'slide' });
  ev.push({ t: 24.0, type: 'stop' }, { t: 24.25, type: 'knife', dur: 0.25 }, { t: 25.75, type: 'knife', dur: 0.25 }, { t: 26.0, type: 'logo' }, { t: 26.5, type: 'clack' }, { t: 27.25, type: 'clack' });
  return ev.sort((a, b) => a.t - b.t);
}
