// Shared Siyari motion library (from videos/siyari-reel/reel.html): renderer + studio envs, faceted gems, ring builder,
// velvet, the swan logo sting (renderSting), the corner lockup, glints and copy helpers. Each reel page imports this.
import * as THREE from 'three';
const W = 1080, H = 1920, S = 2;
const INK = '#FAFCF9', GREEN = '#263A26';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const ss = (a, b, x) => { const k = clamp((x - a) / (b - a)); return k * k * (3 - 2 * k); };
const eio = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const eout = k => 1 - Math.pow(1 - clamp(k), 3);
function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const loadImg = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = src; });

// ---------- velvet texture (shared by the 3D floor and the 2D sting background)
function velvet(size, base, seed, fib) {
  const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d'), R = rng(seed);
  g.fillStyle = base; g.fillRect(0, 0, size, size);
  const im = g.getImageData(0, 0, size, size), d = im.data;
  for (let i = 0; i < d.length; i += 4) { const n = (R() - .5) * 16; d[i] += n; d[i + 1] += n * 1.1; d[i + 2] += n * .9; }
  g.putImageData(im, 0, 0);
  for (let k = 0; k < fib; k++) {                       // short pile fibres, mostly one brush direction
    const x = R() * size, y = R() * size, a = -0.9 + (R() - .5) * .9, l = 3 + R() * 9, lt = R() < .5;
    g.strokeStyle = lt ? `rgba(150,220,170,${.05 + R() * .07})` : `rgba(0,10,4,${.08 + R() * .1})`; g.lineWidth = .7 + R() * .8;
    g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); g.stroke();
  }
  const c2 = document.createElement('canvas'); c2.width = c2.height = size; const g2 = c2.getContext('2d');
  g2.filter = 'blur(0.6px)'; g2.drawImage(c, 0, 0); return c2;
}

// ---------- three.js setup
const glc = document.createElement('canvas'); glc.width = W * S; glc.height = H * S;
const renderer = new THREE.WebGLRenderer({ canvas: glc, antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W * S, H * S, false);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// studio environment for metal + diamond reflections: dark room, a few hard softboxes, green bounce from the velvet below
function envTex() {
  const c = document.createElement('canvas'); c.width = 2048; c.height = 1024; const g = c.getContext('2d'), R = rng(7);
  const gr = g.createLinearGradient(0, 0, 0, 1024);
  gr.addColorStop(0, '#f2f1ee'); gr.addColorStop(.3, '#b9b8b4'); gr.addColorStop(.5, '#6c6c68'); gr.addColorStop(.56, '#2a2c2a'); gr.addColorStop(1, '#1e2620');
  g.fillStyle = gr; g.fillRect(0, 0, 2048, 1024);
  const box = (x, y, w, h, a, col = '255,255,255') => { g.fillStyle = `rgba(${col},${a})`; g.save(); g.filter = 'blur(5px)'; g.fillRect(x - w / 2, y - h / 2, w, h); g.restore(); };
  // black flags give the polished metal and the facets their contrast lines
  box(520, 330, 150, 420, .92, '8,8,8'); box(1290, 300, 110, 380, .9, '10,10,10'); box(1800, 250, 220, 200, .85, '12,12,12'); box(1020, 470, 2048, 26, .8, '15,15,15');
  box(1024, 60, 1400, 140, 1); box(300, 300, 140, 380, 1); box(1520, 270, 170, 330, 1); box(820, 400, 320, 70, .95, '255,238,214');
  box(1900, 420, 110, 260, 1, '238,246,255'); box(80, 430, 300, 80, .9);
  for (let k = 0; k < 90; k++) box(R() * 2048, 90 + R() * 400, 5 + R() * 14, 5 + R() * 14, 1);
  const t = new THREE.CanvasTexture(c); t.mapping = THREE.EquirectangularReflectionMapping; t.colorSpace = THREE.SRGBColorSpace; return t;
}
function gemEnvTex() {
  const c = document.createElement('canvas'); c.width = 2048; c.height = 1024; const g = c.getContext('2d'), R = rng(13);
  const gr = g.createLinearGradient(0, 0, 0, 1024); gr.addColorStop(0, '#ffffff'); gr.addColorStop(.5, '#bdbdbd'); gr.addColorStop(1, '#8a8a8a');
  g.fillStyle = gr; g.fillRect(0, 0, 2048, 1024);
  for (let k = 0; k < 420; k++) { const d = R() < .3, w = 20 + R() * 90, h = 20 + R() * 90;
    g.fillStyle = d ? `rgba(20,22,26,${.55 + R() * .4})` : `rgba(255,255,255,1)`; g.fillRect(R() * 2048, R() * 1024, w, h); }
  for (let k = 0; k < 40; k++) { g.fillStyle = R() < .5 ? 'rgba(200,225,255,.9)' : 'rgba(255,230,200,.9)'; g.fillRect(R() * 2048, R() * 1024, 30 + R() * 60, 30 + R() * 60); }
  const t = new THREE.CanvasTexture(c); t.mapping = THREE.EquirectangularReflectionMapping; t.colorSpace = THREE.SRGBColorSpace; return t;
}
const pmrem = new THREE.PMREMGenerator(renderer);
const ENV = pmrem.fromEquirectangular(envTex()).texture, GENV = pmrem.fromEquirectangular(gemEnvTex()).texture;

// ---------- gem geometry: faceted brilliant / step cut on any outline (flat facets, per-facet tint for fire)
function outline(cut, ph) {
  const c = Math.cos(ph), s = Math.sin(ph);
  switch (cut) {
    case 'oval': return [c, .72 * s];
    case 'marquise': return [c, .5 * s * Math.abs(s)];
    case 'pear': return [c, .66 * s * Math.pow((1 - c) / 2, .38)];
    case 'cushion': return [Math.sign(c) * Math.pow(Math.abs(c), .55), .9 * Math.sign(s) * Math.pow(Math.abs(s), .55)];
    default: return [c, s];
  }
}
const OCT = (a, b, k) => [[a, b - k], [a - k, b], [-a + k, b], [-a, b - k], [-a, -b + k], [-a + k, -b], [a - k, -b], [a, -b + k]];
function gemGeo(cut, seed = 1, tint = null, nn = 16) {
  const step = cut === 'emerald', n = step ? 8 : nn, R = rng(seed);
  const rings = step
    ? [[.62, .17, 0], [.82, .11, 0], [1, .025, 0], [1, -.025, 0], [.72, -.15, 0], [.45, -.28, 0], [.14, -.39, 0]]
    : [[.56, .19, 0], [.82, .115, .5], [1, .025, 0], [1, -.025, 0], [.6, -.2, .5], [.18, -.38, 0]];
  const ring = ([sc, y, ph]) => { const out = [];
    for (let i = 0; i < n; i++) { let x, z;
      if (step) { [x, z] = OCT(1, .7, .2)[i]; } else { [x, z] = outline(cut, (i + ph) / n * Math.PI * 2); }
      out.push(new THREE.Vector3(x * sc, y, z * sc)); } return out; };
  const P = rings.map(ring), pos = [], col = [];
  const tri = (a, b, c) => { pos.push(a.x, a.y, a.z, b.x, b.y, b.z, c.x, c.y, c.z);
    let t; const r = R();
    if (tint) t = tint.map(v => v * (.55 + R() * .5));
    else t = r < .7 ? [1, 1, 1].map(v => v * (.85 + R() * .15)) : r < .82 ? [.82, .9, 1] : r < .92 ? [1, .92, .8] : [.95, .85, 1];
    for (let k = 0; k < 3; k++) col.push(...t); };
  const top = P[0], cTop = new THREE.Vector3(0, top[0].y, 0);
  for (let i = 0; i < n; i++) tri(cTop, top[(i + 1) % n], top[i]);
  for (let r = 0; r < P.length - 1; r++) { const A = P[r], B = P[r + 1];
    for (let i = 0; i < n; i++) { const j = (i + 1) % n; tri(A[i], A[j], B[i]); tri(B[i], A[j], B[j]); } }
  const last = P[P.length - 1], cul = new THREE.Vector3(0, step ? -.41 : -.43, 0);
  for (let i = 0; i < n; i++) tri(last[i], last[(i + 1) % n], cul);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute('color', new THREE.Float32BufferAttribute(col, 3)); g.computeVertexNormals(); return g;
}
const gemMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: .0, vertexColors: true, envMap: GENV, envMapIntensity: 1.35 });
const METAL = {
  yellow: new THREE.MeshPhysicalMaterial({ color: new THREE.Color(1.0, .72, .32), metalness: 1, roughness: .085, envMap: ENV, envMapIntensity: 1.45, clearcoat: .35, clearcoatRoughness: .1 }),
  rose: new THREE.MeshPhysicalMaterial({ color: new THREE.Color(.98, .6, .47), metalness: 1, roughness: .085, envMap: ENV, envMapIntensity: 1.45, clearcoat: .35, clearcoatRoughness: .1 }),
  white: new THREE.MeshPhysicalMaterial({ color: new THREE.Color(.93, .93, .95), metalness: 1, roughness: .075, envMap: ENV, envMapIntensity: 1.55, clearcoat: .35, clearcoatRoughness: .1 }),
};
const GEO = {}; const geoOf = (cut, tint) => { const k = cut + (tint ? 'T' : ''); return GEO[k] || (GEO[k] = gemGeo(cut, 11 + Object.keys(GEO).length, tint)); };
const smallGem = gemGeo('round', 99), AQUA = [.45, .78, .95];

// ---------- ring builder. Local frame: ring axis = Y, band in XZ plane, head points +X.
const Rb = 1.0, TH = .12, BW = .2, RO = Rb + TH / 2;
function bandGeo(bw) { const p = [], r0 = Rb - TH / 2, r1 = Rb + TH / 2, cr = .035, N = 5;
  const arc = (cx, cy, a0, a1) => { for (let i = 0; i <= N; i++) { const a = a0 + (a1 - a0) * i / N; p.push(new THREE.Vector2(cx + Math.cos(a) * cr, cy + Math.sin(a) * cr)); } };
  arc(r1 - cr, -bw / 2 + cr, -Math.PI / 2, 0); arc(r1 - cr, bw / 2 - cr, 0, Math.PI / 2); arc(r0 + cr, bw / 2 - cr, Math.PI / 2, Math.PI); arc(r0 + cr, -bw / 2 + cr, Math.PI, Math.PI * 1.5);
  p.push(p[0].clone()); return new THREE.LatheGeometry(p, 128); }
const BAND = bandGeo(BW), BAND_N = bandGeo(.16);
const prongGeo = new THREE.CylinderGeometry(.021, .026, 1, 10), tipGeo = new THREE.SphereGeometry(.032, 12, 8);
function makeRing(d) {
  const g = new THREE.Group(), m = METAL[d.metal], s = d.size;
  g.add(new THREE.Mesh(d.thin ? BAND_N : BAND, m));
  const xg = RO + .2 + (d.halo ? .03 : 0);                 // girdle height above band
  const stone = new THREE.Mesh(geoOf(d.cut, d.aqua ? AQUA : null), gemMat);
  stone.scale.setScalar(s); stone.rotation.z = -Math.PI / 2; stone.position.x = xg; g.add(stone);
  const toRing = (px, pz, x) => new THREE.Vector3(x, -px, pz);   // stone-local girdle point -> ring coords
  const prongAt = (px, pz) => { const a = toRing(px * s * 1.02, pz * s * 1.02, xg + .07 * s), b = new THREE.Vector3(RO - .03, a.y * .55, a.z * .55);
    const len = a.distanceTo(b), mid = a.clone().add(b).multiplyScalar(.5), pr = new THREE.Mesh(prongGeo, m);
    pr.scale.y = len; pr.position.copy(mid); pr.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), a.clone().sub(b).normalize()); g.add(pr);
    const tp = new THREE.Mesh(tipGeo, m); tp.position.copy(a); g.add(tp); };
  const ang = d.cut === 'marquise' || d.cut === 'pear' ? [0, Math.PI, Math.PI * .5, Math.PI * 1.5] : d.prongs === 6 ? [0, 1, 2, 3, 4, 5].map(i => i * Math.PI / 3) : [1, 3, 5, 7].map(i => i * Math.PI / 4);
  if (d.cut === 'emerald') OCT(1, .7, .2).filter((_, i) => i % 2 === 0).forEach(([x, z]) => prongAt(x, z));
  else ang.forEach(a => { const [x, z] = outline(d.cut, a); prongAt(x, z); });
  if (d.halo) { const k = 20, inst = new THREE.InstancedMesh(smallGem, gemMat, k), M = new THREE.Matrix4(), q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), new THREE.Vector3(1, 0, 0));
    for (let i = 0; i < k; i++) { const [x, z] = outline(d.cut, i / k * Math.PI * 2); M.compose(toRing(x * s * 1.22, z * s * 1.22, xg - .01), q, new THREE.Vector3(.075, .075, .075)); inst.setMatrixAt(i, M); }
    g.add(inst);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(s * 1.22, .03, 8, 64), m); rim.rotation.y = Math.PI / 2; rim.scale.y = d.cut === 'round' ? 1 : .8; rim.position.x = xg - .05; g.add(rim); }
  if (d.pave) { const pts = []; for (let a = .3; a < 1.45; a += .115) { pts.push(a, -a); }
    const inst = new THREE.InstancedMesh(smallGem, gemMat, pts.length), M = new THREE.Matrix4();
    pts.forEach((a, i) => { const nrm = new THREE.Vector3(Math.cos(a), 0, Math.sin(a)); M.compose(nrm.clone().multiplyScalar(RO + .012), new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), nrm), new THREE.Vector3(.058, .058, .058)); inst.setMatrixAt(i, M); });
    g.add(inst); }
  if (d.sides) { const inst = new THREE.InstancedMesh(smallGem, gemMat, 4), M = new THREE.Matrix4(), q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), new THREE.Vector3(1, 0, 0));
    [[.15, .95], [-.25, .9], [.15, -.95], [-.25, -.9]].forEach(([x, z], i) => { M.compose(toRing(x * s, z * s * 1.05, xg - .04), q, new THREE.Vector3(.09, .09, .09)); inst.setMatrixAt(i, M); }); g.add(inst); }
  g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  g.userData.top = new THREE.Vector3(xg + .2 * s, 0, 0);    // table centre, for glints
  return g;
}
// Designs modelled on Siyari's catalogue (product handles on siyari.com in the comments)
const DESIGNS = [
  { cut: 'round', metal: 'white', size: .36, prongs: 4, thin: true },               // icon-round-solitaire
  { cut: 'marquise', metal: 'yellow', size: .5, pave: true },                        // 2ct-marquise-...-solitaire-ring
  { cut: 'emerald', metal: 'rose', size: .4, pave: true },                           // emerald-cut-solitaire-pave
  { cut: 'round', metal: 'yellow', size: .31, halo: true, pave: true },              // dulce-round-halo-pave-solitaire
  { cut: 'pear', metal: 'white', size: .44, pave: true },                            // the pear ring from their Sep 29 reel
  { cut: 'cushion', metal: 'rose', size: .32, halo: true },                          // velina-cushion-everyday
  { cut: 'oval', metal: 'yellow', size: .38, aqua: true, sides: true, thin: true },  // oval-aquamarine-promise-ring
  { cut: 'marquise', metal: 'white', size: .46, pave: true, thin: true },            // amalia-marquise-solitaire-pave
  { cut: 'round', metal: 'rose', size: .38, prongs: 6 },                             // paramount-solitaire
  { cut: 'oval', metal: 'white', size: .4, pave: true },                             // oval solitaire pave
];

const mk = () => { const c = document.createElement('canvas'); c.width = W * S; c.height = H * S; return [c, c.getContext('2d')]; };
const [OFF1, OFF1G] = mk(), [OFF2, OFF2G] = mk();
// ---------- sting: the falling diamond (orthographic, 1 unit = 1 css px, y up = -screen y)
const stingSc = new THREE.Scene(); stingSc.environment = ENV;
stingSc.add(new THREE.HemisphereLight(0xffffff, 0x163a22, .6));
const stingCam = new THREE.OrthographicCamera(0, W, 0, -H, -3000, 3000);
const bigGem = new THREE.Mesh(gemGeo('round', 41), new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 1, roughness: .0, vertexColors: true, envMap: GENV, envMapIntensity: 1.5 }));
stingSc.add(bigGem);

// ---------- logo assets (Siyari's own artwork, see prep_logo.py)
const IMG = {}; const LK = await (await fetch('img/lockup.json')).json();
for (const k of ['swan', 'crown', 'wordmark', 'swan_body', 'swan_wing_upper', 'swan_wing_lower', 'reveal_map']) IMG[k] = await loadImg(`img/${k}.png`);
await document.fonts.load('500 40px Jost'); await document.fonts.load('400 40px Jost'); await document.fonts.load('500 40px Montserrat');
const pix = img => { const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const g = c.getContext('2d'); g.drawImage(img, 0, 0); return g.getImageData(0, 0, c.width, c.height).data; };
const SW = LK.swan_canvas[0], SH = LK.swan_canvas[1];
const PB = pix(IMG.swan_body), PU = pix(IMG.swan_wing_upper), PL = pix(IMG.swan_wing_lower), PM = pix(IMG.reveal_map);
const swanCv = document.createElement('canvas'); swanCv.width = SW; swanCv.height = SH; const swanG = swanCv.getContext('2d'), swanID = swanG.createImageData(SW, SH);
function swanReveal(pb, pu, pl) {             // geodesic draw-on: each part paints itself from its seed along its own curve
  const o = swanID.data, e = .07;
  for (let i = 0; i < o.length; i += 4) {
    const fb = clamp((pb * (1 + e) - PM[i] / 255) / e), fu = clamp((pu * (1 + e) - PM[i + 1] / 255) / e), fl = clamp((pl * (1 + e) - PM[i + 2] / 255) / e);
    o[i] = o[i + 1] = o[i + 2] = 255; o[i + 3] = PB[i + 3] * fb + PU[i + 3] * fu + PL[i + 3] * fl;
  }
  swanG.putImageData(swanID, 0, 0); return swanCv;
}
// lockup geometry from the user's logo file (185x173 px): swan 71..126 x 29..99, wordmark 34..152(+R) x 108..132, tagline 34..155 x 139..145
const REF = { cx: 98, cy: 87 };
function lockupPlan(cx, cy, K) {
  const X = px => cx + (px - REF.cx) * K, Y = py => cy + (py - REF.cy) * K;
  const ks = 56 * K / 580, kw = 119 * K / 559;
  return { K, X, Y, ks, kw, swanX: X(71) - 20 * ks, swanY: Y(29) - 20 * ks, wmX: X(34), wmY: Y(108) - 19 * kw,
    crownX: X(71) + (LK.crown_center[0] - 20) * ks, crownY: Y(29) + (LK.crown_center[1] - 20) * ks, tagX: X(34), tagY: Y(145.5), tagW: 122 * K, tagCap: 7 * K };
}
const LET = LK.wordmark_letters;                    // S I YA R I (R) column groups in wordmark.png
const LET_ORDER = [2, 3, 1, 4, 0, 5];               // reveal from the centre outwards
// st: {swan:[pb,pu,pl], crown:0..1, letters:t-in-seconds since start or null, tag:0..1}
function drawLockup(g, P, st) {
  if (st.full) { g.drawImage(IMG.swan, P.swanX, P.swanY, SW * P.ks, SH * P.ks); }
  else if (st.swan) { const [a, b, c] = st.swan; if (a >= 1 && b >= 1 && c >= 1) g.drawImage(IMG.swan_body, P.swanX, P.swanY, SW * P.ks, SH * P.ks), g.drawImage(IMG.swan_wing_upper, P.swanX, P.swanY, SW * P.ks, SH * P.ks), g.drawImage(IMG.swan_wing_lower, P.swanX, P.swanY, SW * P.ks, SH * P.ks);
    else if (a > 0 || b > 0 || c > 0) g.drawImage(swanReveal(a, b, c), P.swanX, P.swanY, SW * P.ks, SH * P.ks); }
  if (!st.full && st.crown > 0) { g.save(); g.globalAlpha = st.crown; g.drawImage(IMG.crown, P.swanX, P.swanY, SW * P.ks, SH * P.ks); g.restore(); }
  const wm = IMG.wordmark;
  LET.forEach(([x0, x1], gi) => {
    let k = 1, dy = 0, bl = 0;
    if (!st.full) { if (st.letters == null) return; const kk = clamp((st.letters - LET_ORDER.indexOf(gi) * .075) / .32); if (kk <= 0) return; k = eout(kk); dy = (1 - k) * 12; bl = (1 - k) * 7; }
    const sx = Math.max(0, x0 - 2), sw = Math.min(wm.width, x1 + 3) - sx;
    g.save(); g.globalAlpha *= k; if (bl > .3) g.filter = `blur(${bl}px)`;
    g.drawImage(wm, sx, 0, sw, wm.height, P.wmX + sx * P.kw, P.wmY + dy, sw * P.kw, wm.height * P.kw); g.restore();
  });
  const tg = st.full ? 1 : (st.tag || 0);
  if (tg > 0) { g.save(); g.globalAlpha *= eout(tg); g.fillStyle = INK; const size = P.tagCap * .88 / .70; g.font = `450 ${size}px Montserrat`; g.letterSpacing = '0px';
    const txt = 'LAB GROWN DIAMONDS', w0 = g.measureText(txt).width, ls = (P.tagW - w0) / (txt.length - 1) + (1 - eout(tg)) * 3;
    g.letterSpacing = `${ls}px`; g.textBaseline = 'alphabetic'; g.fillText(txt, P.tagX, P.tagY); g.restore(); }
}
// corner lockup (top-left, the reference's wordmark position, kept clear of Instagram's top bar)
const CORNER = lockupPlan(56 + (98 - 34) * 1.12, 128 + (87 - 29) * 1.12, 1.12);

// ---------- 2D helpers
const stingBg = velvet(1024, GREEN, 21, 30000);
function drawStingBg(g) {
  g.fillStyle = GREEN; g.fillRect(0, 0, W, H);
  g.save(); g.globalAlpha = .55; g.drawImage(stingBg, 0, 0, 1024, 1024, -60, -40, 1220, 1220); g.drawImage(stingBg, 0, 0, 1024, 1024, -60, 1180, 1220, 1220); g.restore();
  const rg = g.createRadialGradient(W / 2, H * .44, 60, W / 2, H * .5, H * .72);
  rg.addColorStop(0, 'rgba(120,170,120,.16)'); rg.addColorStop(.5, 'rgba(0,0,0,0)'); rg.addColorStop(1, 'rgba(0,8,2,.55)'); g.fillStyle = rg; g.fillRect(0, 0, W, H);
}
function star(g, x, y, r, a, rot = 0) {             // 4-point jewellery glint
  if (a <= 0 || r <= 0) return;
  g.save(); g.translate(x, y); g.rotate(rot); g.globalCompositeOperation = 'lighter';
  const core = g.createRadialGradient(0, 0, 0, 0, 0, r * .35); core.addColorStop(0, `rgba(255,255,255,${a})`); core.addColorStop(1, 'rgba(255,250,235,0)');
  g.fillStyle = core; g.beginPath(); g.arc(0, 0, r * .35, 0, 7); g.fill();
  const ray = (len, wd, al) => { const gr = g.createLinearGradient(-len, 0, len, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, `rgba(255,253,245,${al})`); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.beginPath(); g.moveTo(-len, 0); g.quadraticCurveTo(0, -wd, len, 0); g.quadraticCurveTo(0, wd, -len, 0); g.fill(); };
  ray(r, r * .07, a); g.rotate(Math.PI / 2); ray(r, r * .07, a); g.rotate(Math.PI / 4); ray(r * .45, r * .04, a * .6); g.rotate(Math.PI / 2); ray(r * .45, r * .04, a * .6);
  g.restore();
}
function copyBlock(g, lines, x, y, align, t0, t) {   // letters fade in one by one, like the reference's EVERY DAY / NEW STYLE
  if (t < t0) return; const size = 66, lh = size * .98; let idx = 0;
  g.save(); g.font = `500 ${size}px Jost`; g.letterSpacing = '1.5px'; g.fillStyle = INK; g.textBaseline = 'alphabetic';
  g.shadowColor = 'rgba(0,20,8,.35)'; g.shadowBlur = 14;
  lines.forEach((ln, li) => {
    const wTot = g.measureText(ln).width; let cx = align === 'right' ? x - wTot : x;
    for (const ch of ln) { const k = clamp((t - t0 - idx * .045) / .22); const wch = g.measureText(ch).width;
      if (k > 0) { g.globalAlpha = k; g.fillText(ch, cx, y + li * lh); } cx += wch; idx++; }
  });
  g.restore();
}
const v3 = new THREE.Vector3();
function project(cam, p) { v3.copy(p).project(cam); return [(v3.x + 1) / 2 * W, (1 - v3.y) / 2 * H, v3.z]; }

// ---------- scenes
function renderChain(S_, tl, t) {
  const [pos, look] = S_.cfg.cam(tl); S_.cam.position.copy(pos); S_.cam.lookAt(look); S_.cam.updateMatrixWorld();
  S_.place(tl); renderer.setClearColor(0x000000, 1); renderer.render(S_.sc, S_.cam);
  ctx.drawImage(glc, 0, 0, W, H);
  // glints on the centre stones (each ring flashes on its own rhythm)
  S_.rings.forEach((r, i) => {
    const p = project(S_.cam, S_.userData_tmp = r.userData.top.clone().applyMatrix4(r.matrix));
    if (p[0] < -50 || p[0] > W + 50 || p[1] < -50 || p[1] > H + 50) return;
    const P = 2.6, ph = (i * .37 + (S_ === C ? .2 : 0)) % 1, f = ((tl / P + ph) % 1) - .5, a = Math.exp(-Math.pow(f * P / .11, 2));
    star(ctx, p[0], p[1], 34 + 40 * a, a * .95, .2 + i);
  });
}
function vignette(g, a) { const rg = g.createRadialGradient(W / 2, H / 2, H * .3, W / 2, H / 2, H * .75); rg.addColorStop(0, 'rgba(0,0,0,0)'); rg.addColorStop(1, `rgba(0,10,4,${a})`); g.fillStyle = rg; g.fillRect(0, 0, W, H); }
const LOCK_B = lockupPlan(W / 2, 905, 4.7), LOCK_D = lockupPlan(W / 2, 770, 4.2);
function renderSting(tl, P, cta, FALL = .62) {
  drawStingBg(ctx);
  // 1) the diamond falls in, spinning, and lands as the crown on the swan's head
  if (tl < FALL + .1) {
    const sub = 7, out = [];
    for (let k = sub - 1; k >= 0; k--) {
      const tt = Math.max(0, tl - k * .014), e = clamp(tt / FALL), ef = e * e * (1.6 - .6 * e);
      const x = lerp(W / 2 + 90, P.crownX, eio(e)), y = lerp(-260, P.crownY, ef), r = lerp(250, 7.5 * P.K / 4.7 * 1.2, Math.pow(e, .85));
      bigGem.position.set(x, -y, 0); bigGem.scale.setScalar(r); bigGem.rotation.set(1.05 - .6 * e, 9 * (1 - Math.pow(1 - e, 2)), .3);
      renderer.setClearColor(0x000000, 0); renderer.render(stingSc, stingCam);
      ctx.save(); ctx.globalAlpha = (k === 0 ? 1 : .22 * (1 - k / sub)) * (1 - ss(FALL, FALL + .1, tl)); ctx.drawImage(glc, 0, 0, W, H); ctx.restore();
    }
  }
  const land = tl - FALL;
  const st = { swan: [eio(clamp((land - .02) / .8)), eio(clamp((land - .42) / .55)), eio(clamp((land - .56) / .55))],
    crown: ss(-.02, .08, land), letters: land > .78 ? land - .78 : null, tag: clamp((land - 1.25) / .5) };
  const L = OFF1, lg = OFF1G; lg.setTransform(1, 0, 0, 1, 0, 0); lg.clearRect(0, 0, W * S, H * S); lg.setTransform(S, 0, 0, S, 0, 0);
  drawLockup(lg, P, st);
  ctx.drawImage(L, 0, 0, W, H);
  // sheen across the finished logo
  const sh = clamp((land - 1.85) / .7);
  if (sh > 0 && sh < 1) { const Sx = OFF2, sg = OFF2G; sg.globalCompositeOperation = 'source-over'; sg.setTransform(1, 0, 0, 1, 0, 0); sg.clearRect(0, 0, W * S, H * S); sg.drawImage(L, 0, 0);
    sg.globalCompositeOperation = 'source-in'; const bx = lerp(-300, W + 300, eio(sh)) * S, gr = sg.createLinearGradient(bx - 240 * S, 0, bx + 240 * S, 160 * S);
    gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, 'rgba(255,248,225,.75)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); sg.fillStyle = gr; sg.fillRect(0, 0, W * S, H * S);
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.drawImage(Sx, 0, 0, W, H); ctx.restore(); }
  // landing flash
  const fl = Math.exp(-Math.pow((land - .03) / .09, 2)) * (land > -.1 ? 1 : 0);
  star(ctx, P.crownX, P.crownY, 150 * P.K / 4.7, fl, .3);
  star(ctx, P.crownX, P.crownY, 60, Math.exp(-Math.pow((land - 2.05) / .12, 2)) * .9, .1);
  if (cta) {
    const c1 = clamp((land - 1.45) / .45), c2 = clamp((land - 1.75) / .45), c3 = clamp((land - 2.05) / .45);
    ctx.save(); ctx.textAlign = 'center'; ctx.fillStyle = INK;
    ctx.globalAlpha = eout(c1) * .9; ctx.font = '400 40px Jost'; ctx.letterSpacing = '0.5px'; ctx.fillText('Custom lab-grown diamond jewellery', W / 2, 1150 + (1 - eout(c1)) * 16);
    ctx.globalAlpha = eout(c2); const y2 = 1262 + (1 - eout(c2)) * 16; ctx.font = '500 34px Jost'; ctx.letterSpacing = '3px';
    const tx = 'DM “CUSTOM” TO DESIGN YOURS', tw = ctx.measureText(tx).width + 70;
    ctx.strokeStyle = 'rgba(250,252,249,.85)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.roundRect(W / 2 - tw / 2, y2 - 52, tw, 80, 40); ctx.stroke();
    ctx.fillText(tx, W / 2 + 1.5, y2);
    ctx.globalAlpha = eout(c3) * .72; ctx.font = '400 30px Jost'; ctx.letterSpacing = '1px'; ctx.fillText('Somajiguda, Hyderabad  ·  siyari.com', W / 2, 1380 + (1 - eout(c3)) * 12);
    ctx.restore();
  }
}
let CORNER_CV = null;
function drawCorner(alpha = .96) { if (!CORNER_CV) { CORNER_CV = document.createElement('canvas'); CORNER_CV.width = W * S; CORNER_CV.height = H * S; const g = CORNER_CV.getContext('2d'); g.scale(S, S);
  g.shadowColor = 'rgba(0,15,6,.45)'; g.shadowBlur = 10; drawLockup(g, CORNER, { full: true }); }
  ctx.save(); ctx.globalAlpha = alpha; ctx.drawImage(CORNER_CV, 0, 0, W, H); ctx.restore(); }

export { THREE, W, H, S, cv, ctx, INK, GREEN, clamp, lerp, ss, eio, eout, rng, loadImg, velvet, renderer, glc, ENV, GENV, gemGeo, gemMat, METAL, outline, OCT, makeRing, DESIGNS, RO, BW,
  renderSting, drawStingBg, drawLockup, lockupPlan, drawCorner, star, copyBlock, project, vignette, LOCK_B, LOCK_D };
