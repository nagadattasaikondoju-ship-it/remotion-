// ---------- "Chai, Gutkha and the Yellow Wall": characters + scenes (appended to the shared flat-2D engine by make_html.py) ----------
const mixC = (a, b, k) => { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)); const A = p(a), B = p(b); return '#' + A.map((v, i) => Math.round(lerp(v, B[i], clamp(k))).toString(16).padStart(2, '0')).join(''); };
const TEETH = ['#FAF8F0', '#F2E4AE', '#E2C46E', '#C99A4A', '#9E6C3A'];
const teethAt = q => { q = clamp(q) * (TEETH.length - 1); const i = Math.min(TEETH.length - 2, Math.floor(q)); return mixC(TEETH[i], TEETH[i + 1], q - i); };
function ramesh(x, y, s, o = {}) {   // origin = head centre. o: teeth colour, gum colour, recede 0..1, expr ('smile'|'sad'|'touched'), t
  X.save(); X.translate(x, y); X.scale(s, s);
  const sk = '#B9784F', skD = '#A0653F', hair = '#2B2228', grey = '#9B9BA3';
  rr(-34, 92, 68, 70, 20, skD);
  X.beginPath(); X.moveTo(-190, 160); X.quadraticCurveTo(0, 110, 190, 160); X.quadraticCurveTo(225, 420, 205, 620); X.lineTo(-205, 620); X.quadraticCurveTo(-225, 420, -190, 160); X.closePath();
  X.fillStyle = grad(140, 620, [[0, '#8FC6E8'], [1, '#5E9FC9']]); X.fill();
  X.fillStyle = '#E8F4FC'; X.beginPath(); X.moveTo(-60, 132); X.lineTo(-8, 210); X.lineTo(-90, 190); X.closePath(); X.fill(); X.beginPath(); X.moveTo(60, 132); X.lineTo(8, 210); X.lineTo(90, 190); X.closePath(); X.fill();
  circle(-120, 12, 27, skD); circle(120, 12, 27, skD); circle(0, 0, 122, sk);
  X.beginPath(); X.moveTo(-124, -6); X.bezierCurveTo(-130, -110, -60, -150, -20, -132); X.quadraticCurveTo(0, -112, 20, -132); X.bezierCurveTo(60, -150, 130, -110, 124, -6);
  X.bezierCurveTo(112, -60, 96, -84, 70, -96); X.quadraticCurveTo(0, -78, -70, -96); X.bezierCurveTo(-96, -84, -112, -60, -124, -6); X.closePath(); X.fillStyle = hair; X.fill();
  ell(-118, -24, 12, 30, grey); ell(118, -24, 12, 30, grey);
  X.strokeStyle = hair; X.lineWidth = 12; X.lineCap = 'round'; const sad = o.expr === 'sad' || o.expr === 'touched';
  X.beginPath(); X.moveTo(-74, sad ? -40 : -46); X.lineTo(-24, sad ? -50 : -44); X.moveTo(74, sad ? -40 : -46); X.lineTo(24, sad ? -50 : -44); X.stroke();
  if (o.expr === 'smile') { X.strokeStyle = '#1B1638'; X.lineWidth = 8; for (const sx of [-48, 48]) { X.beginPath(); X.arc(sx, 4, 15, Math.PI * 1.1, Math.PI * 1.9); X.stroke(); } }
  else { for (const sx of [-48, 48]) { ell(sx, 2, 12, 15, '#1B1638'); circle(sx + 4, -4, 4.5, '#FFFFFF'); }
    if (o.expr === 'touched') { X.save(); X.globalAlpha = .8; ell(-48, 24, 9, 6, '#9FE3FF'); ell(48, 24, 9, 6, '#9FE3FF'); X.restore(); } }
  X.beginPath(); X.moveTo(-10, 20); X.quadraticCurveTo(0, 46, 14, 34); X.strokeStyle = skD; X.lineWidth = 7; X.stroke();
  circle(-76, 40, 18, 'rgba(255,120,120,.3)'); circle(76, 40, 18, 'rgba(255,120,120,.3)');
  if (o.expr === 'smile') {   // a big open smile: gums on top, teeth below (longer as the gums recede)
    X.save(); X.beginPath(); X.moveTo(-62, 58); X.quadraticCurveTo(0, 150, 62, 58); X.quadraticCurveTo(0, 70, -62, 58); X.closePath(); X.fillStyle = '#5A1E2E'; X.fill(); X.clip();
    const gTop = 58, gH = lerp(16, 6, o.recede || 0), tH = lerp(22, 32, o.recede || 0);
    X.fillStyle = o.gum || '#E77C8F'; X.fillRect(-70, gTop - 6, 140, gH + 10);
    for (let i = -3; i <= 2; i++) { rr(i * 20 + 1, gTop + gH, 18, tH, 5, o.teeth || TEETH[0]); }
    X.restore();
  } else { X.strokeStyle = '#5A1E2E'; X.lineWidth = 7; X.beginPath(); X.moveTo(-30, 82); X.quadraticCurveTo(0, o.expr === 'sad' ? 72 : 90, 30, 82); X.stroke(); }
  X.beginPath(); X.moveTo(-58, 60); X.bezierCurveTo(-40, 36, -10, 44, 0, 52); X.bezierCurveTo(10, 44, 40, 36, 58, 60); X.bezierCurveTo(30, 66, 10, 60, 0, 64); X.bezierCurveTo(-10, 60, -30, 66, -58, 60); X.fillStyle = hair; X.fill();
  X.restore();
}
function girl(x, y, s, o = {}) {   // the daughter; origin = head centre
  X.save(); X.translate(x, y); X.scale(s, s);
  const sk = '#C98A5E', hair = '#2A1A2E', t = o.t || 0;
  for (const sx of [-1, 1]) { X.save(); X.translate(sx * 92, -10); X.rotate(sx * (.35 + Math.sin(t * 3 + sx) * .06)); ell(0, 46, 26, 54, hair); circle(0, 4, 13, '#FF6B9A'); X.restore(); }
  circle(0, -6, 96, hair);
  X.beginPath(); X.moveTo(-110, 110); X.quadraticCurveTo(0, 80, 110, 110); X.lineTo(170, 420); X.lineTo(-170, 420); X.closePath(); X.fillStyle = grad(100, 420, [[0, '#FFD54A'], [1, '#FFB627']]); X.fill();
  circle(0, 0, 86, sk);
  X.beginPath(); X.moveTo(-90, -6); X.bezierCurveTo(-90, -96, 90, -96, 90, -6); X.quadraticCurveTo(40, -46, 0, -40); X.quadraticCurveTo(-40, -46, -90, -6); X.fillStyle = hair; X.fill();
  for (const sx of [-34, 34]) { if (o.happy) { X.strokeStyle = '#1B1638'; X.lineWidth = 7; X.lineCap = 'round'; X.beginPath(); X.arc(sx, 10, 12, Math.PI * 1.1, Math.PI * 1.9); X.stroke(); } else { ell(sx, 8, 10, 13, '#1B1638'); circle(sx + 3, 3, 4, '#FFFFFF'); } }
  circle(-56, 36, 14, 'rgba(255,110,130,.45)'); circle(56, 36, 14, 'rgba(255,110,130,.45)');
  X.strokeStyle = '#5A1E2E'; X.lineWidth = 7; X.lineCap = 'round'; X.beginPath(); X.arc(0, 30, 22, .2 * Math.PI, .8 * Math.PI); X.stroke();
  X.restore();
}
function crayon(pathFn, col, w) { for (let i = 0; i < 3; i++) { X.save(); X.translate((rnd(i * 7) - .5) * 3, (rnd(i * 13) - .5) * 3); X.globalAlpha *= .55; X.strokeStyle = col; X.lineWidth = w; X.lineCap = 'round'; X.lineJoin = 'round'; X.beginPath(); pathFn(); X.stroke(); X.restore(); } }
function drawing(x, y, s, rot, teeth, happy, t, k = 1) {   // the daughter's crayon drawing of Papa
  if (k <= 0) return; X.save(); X.translate(x, y); X.rotate(rot); X.scale(s * back(k, 1.3), s * back(k, 1.3)); X.globalAlpha = clamp(k * 3);
  X.shadowColor = 'rgba(0,0,0,.25)'; X.shadowBlur = 30; X.shadowOffsetY = 10; rr(-300, -360, 600, 720, 14, '#FFFDF6'); X.shadowColor = 'transparent';
  X.strokeStyle = 'rgba(120,170,220,.35)'; X.lineWidth = 3; for (let i = 0; i < 9; i++) { X.beginPath(); X.moveTo(-280, -260 + i * 70); X.lineTo(280, -260 + i * 70); X.stroke(); }
  if (happy) { crayon(() => X.arc(200, -250, 46, 0, 6.29), '#FFB627', 14); for (let i = 0; i < 8; i++) { const a = i * .785; crayon(() => { X.moveTo(200 + Math.cos(a) * 64, -250 + Math.sin(a) * 64); X.lineTo(200 + Math.cos(a) * 92, -250 + Math.sin(a) * 92); }, '#FFB627', 9); }
    heart(-210, -230, 1.6, 'rgba(255,79,122,.85)'); heart(-150, 250, 1.2, 'rgba(255,79,122,.85)'); heart(220, 200, 1.4, 'rgba(255,79,122,.85)'); }
  crayon(() => X.arc(0, -110, 120, 0, 6.29), '#8A5A3B', 10);
  crayon(() => { X.moveTo(-100, -150); X.quadraticCurveTo(0, -270, 100, -150); }, '#2B2228', 16);
  crayon(() => { X.arc(-42, -130, 6, 0, 6.29); X.moveTo(48, -130); X.arc(42, -130, 6, 0, 6.29); }, '#2B2228', 10);
  crayon(() => { X.moveTo(-50, -88); X.quadraticCurveTo(0, -112, 50, -88); }, '#2B2228', 14);
  X.save(); X.beginPath(); X.moveTo(-62, -68); X.quadraticCurveTo(0, -4, 62, -68); X.closePath(); X.fillStyle = teeth; X.globalAlpha *= .9; X.fill(); X.restore();
  crayon(() => { X.moveTo(-62, -68); X.quadraticCurveTo(0, -4, 62, -68); X.closePath(); for (let i = -2; i <= 2; i++) { X.moveTo(i * 22, -66); X.lineTo(i * 22, -44 + Math.abs(i) * -6); } }, '#5A3A2A', 6);
  crayon(() => { X.moveTo(0, 10); X.lineTo(0, 200); X.moveTo(0, 60); X.lineTo(-110, happy ? -10 : 130); X.moveTo(0, 60); X.lineTo(110, happy ? -10 : 130); X.moveTo(0, 200); X.lineTo(-80, 320); X.moveTo(0, 200); X.lineTo(80, 320); }, '#4A90D9', 12);
  X.font = '800 64px P'; X.textAlign = 'center'; X.textBaseline = 'middle'; ['P', 'A', 'P', 'A'].forEach((c, i) => { X.fillStyle = ['#FF5A5F', '#FFB627', '#3DDC84', '#7C5CFF'][i]; X.fillText(c, -150 + i * 32 + (i > 1 ? 210 : 0), 300 + (i % 2) * 8); });
  X.restore();
}
function habitIcon(kind, x, y, k, t) {
  if (k <= 0) return; X.save(); X.translate(x, y); const e = back(k, 1.6); X.scale(e, e); X.globalAlpha = clamp(k * 3);
  X.shadowColor = 'rgba(0,0,0,.2)'; X.shadowBlur = 24; X.shadowOffsetY = 8; circle(0, 0, 118, '#FFFFFF'); X.shadowColor = 'transparent';
  if (kind === 'chai') { X.beginPath(); X.moveTo(-50, -40); X.lineTo(50, -40); X.lineTo(36, 60); X.lineTo(-36, 60); X.closePath(); X.fillStyle = '#C9773E'; X.fill(); ell(0, -40, 50, 12, '#9A5528'); ell(0, -40, 42, 8, '#D7A06A');
    X.strokeStyle = 'rgba(150,150,160,.8)'; X.lineWidth = 7; X.lineCap = 'round'; for (let j = 0; j < 3; j++) { const sx = -24 + j * 24, ph = t * 5 + j; X.beginPath(); X.moveTo(sx, -58); X.bezierCurveTo(sx + 12 * Math.sin(ph), -76, sx - 12 * Math.sin(ph), -92, sx, -108); X.stroke(); } }
  if (kind === 'cig') { X.save(); X.rotate(-.5); rr(-80, -12, 120, 24, 6, '#F5F5F5'); rr(40, -12, 40, 24, 6, '#E9A04B'); circle(-80, 0, 12, '#FF7A3D'); X.restore();
    X.strokeStyle = 'rgba(170,170,180,.7)'; X.lineWidth = 8; X.lineCap = 'round'; X.beginPath(); X.moveTo(-70, 40); X.bezierCurveTo(-90 + 10 * Math.sin(t * 4), 0, -60, -30, -80, -80); X.stroke(); }
  if (kind === 'gutka') { X.save(); X.rotate(.15); rr(-62, -78, 124, 156, 12, '#2E8B57'); rr(-62, -78, 124, 26, 8, '#C9D6DF'); rr(-62, 52, 124, 26, 8, '#C9D6DF');
    for (let j = 0; j < 7; j++) { X.fillStyle = '#B6C4CE'; X.fillRect(-58 + j * 18, -76, 6, 22); X.fillRect(-58 + j * 18, 54, 6, 22); }
    X.fillStyle = '#FFE38A'; X.font = '800 30px P'; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText('gutka', 0, 0); X.restore(); }
  X.restore();
}
function tartar(amount, darkness, t, popT) {   // deposits along the crown near the gum line (both sides) + germs
  if (amount <= 0) return;
  for (const sx of [-1, 1]) for (let i = 0; i < 9; i++) {
    const y = lerp(-170, -30, i / 8), base = sx * (242 - (y + 170) * .45), r = (22 + rnd(i + (sx > 0 ? 20 : 0)) * 18) * clamp(amount * 1.6 - i * .05);
    if (r <= 1) continue; X.save(); X.globalAlpha = clamp(amount * 2);
    ell(base + sx * r * .35, y, r * .9, r * .65, mixC('#E5C76B', '#7A5226', darkness), rnd(i) * 2);
    circle(base + sx * r * .5, y - r * .2, r * .28, 'rgba(255,255,255,.25)'); X.restore();
  }
}
function germs(n, k, t, cx, cy, spread) {
  for (let i = 0; i < n; i++) { const q = clamp(k * 1.5 - i / n * .5); if (q <= 0) continue; const a = rnd(i) * 6.28 + t * (.6 + rnd(i + 3)), r = spread * (.4 + rnd(i + 9) * .6);
    const x = cx + Math.cos(a) * r * (rnd(i + 2) > .5 ? 1 : -1) * 1.4, y = cy + Math.sin(a) * r * .6;
    X.save(); X.translate(x, y); X.scale(q, q); circle(0, 0, 18, '#6BD36B'); for (let j = 0; j < 6; j++) { const b = j * 1.05 + t * 2; circle(Math.cos(b) * 20, Math.sin(b) * 20, 5, '#4FB84F'); }
    circle(-6, -3, 5, '#FFFFFF'); circle(6, -3, 5, '#FFFFFF'); circle(-6, -2, 2.5, '#1B1638'); circle(6, -2, 2.5, '#1B1638'); X.restore(); }
}
// ---------- scenes ----------
function scenePortrait(t) {   // hook: the years go by, the smile changes colour, then the gums
  bg([[0, '#FFE0B0'], [.6, '#F7B48A'], [1, '#D9807A']]);
  X.save(); X.globalAlpha = .16; X.translate(540, 820); X.rotate(t * .04); for (let i = 0; i < 14; i++) { X.rotate(Math.PI / 7); X.beginPath(); X.moveTo(0, 0); X.lineTo(1400, -110); X.lineTo(1400, 110); X.closePath(); X.fillStyle = '#FFFFFF'; X.fill(); } X.restore();
  particles(t, 16, 5, 'rgba(255,255,255,.8)', 9, .7);
  const yk = seg(t, K.smile, K.year + .3), yr = Math.round(lerp(2015, 2025, eio(yk)));
  const habits = [K.chai, K.cig, K.gutka].filter(h => t > h + .05).length;
  const tq = .25 * eio(yk) + habits * .25;
  const recede = eio(seg(t, K.gums, K.gums + .5)), gumC = mixC('#E77C8F', '#B4405A', recede);
  const z = lerp(1.0, 1.18, eio(seg(t, K.gums - .2, K.gums + .6)));
  X.save(); X.translate(540, 820); X.scale(z, z); X.translate(-540, -820);
  ramesh(540, 680 + Math.sin(t * 2.2) * 5, 1.75, { expr: 'smile', teeth: teethAt(tq), gum: gumC, recede, t });
  X.restore();
  // year counter
  if (t < K.chai) { const k = seg(t, .1, .4); X.save(); X.globalAlpha = k; rr(390, 260, 300, 110, 55, 'rgba(27,22,56,.85)'); text(String(yr), 540, 316, 64, '#FFFFFF', 800); X.restore(); }
  // the three habits, each one darkens the smile a little more (no judgement, just the timeline)
  [['chai', K.chai, 180, 470], ['cig', K.cig, 900, 470], ['gutka', K.gutka, 540, 300]].forEach(([kind, t0, x, y]) => habitIcon(kind, x, y, seg(t, t0 - .1, t0 + .25) * (1 - seg(t, K.drew - .9, K.drew - .6)), t));
  if (t > K.gums - .1 && t < K.chai) label('gums pulling back', 540, 1110 - 0, seg(t, K.gums, K.gums + .3), '#FFFFFF', '#B4405A', 46);
}
function sceneDrawing(t, again) {
  bg(again ? [[0, '#FFF1C9'], [1, '#FFC7A8']] : [[0, '#E9E4F7'], [1, '#C9C1E6']]);
  particles(t, 12, again ? 61 : 51, 'rgba(255,255,255,.9)', 8, .6);
  const t0 = again ? K.again0 : K.drew0;
  drawing(540, 660, 1.08, -.04, again ? '#FFFFFF' : '#8E5E2E', again, t, seg(t, t0 - .1, t0 + .4));
  girl(250, 1470, .95, { t, happy: true });
  const rk = eo(seg(t, again ? K.again0 + .5 : K.brown - .2, again ? K.again0 + 1.1 : K.brown + .4));
  if (rk > 0) ramesh(lerp(1180, 820, rk), 1470, .9, { expr: again ? 'smile' : 'touched', teeth: again ? TEETH[0] : TEETH[4], gum: again ? '#E77C8F' : '#B4405A', recede: again ? .55 : 1, t });
  if (again) { for (let i = 0; i < 6; i++) { const k = seg(t, K.again0 + .9 + i * .14, K.again0 + 2.4 + i * .14); if (k > 0 && k < 1) heart(560 + (rnd(i) - .5) * 300, 1420 - k * 220, 1 + rnd(i + 2) * .6, '#FF4F7A', Math.sin(k * Math.PI)); } }
}
function sceneDiveR(t) {
  const k = eio(seg(t, K.but + .1, K.worse + .45));
  bg([[0, '#F7B48A'], [1, '#C86A7A']]);
  X.save(); const z = lerp(1, 10, ei(k)); X.translate(540, 760); X.scale(z, z); X.translate(-540, -(640 + 95 * 1.75));
  ramesh(540, 640, 1.75, { expr: 'smile', teeth: TEETH[4], gum: '#B4405A', recede: 1, t }); X.restore();
  const ir = seg(t, K.worse, K.worse + .45);
  if (ir > 0) { X.save(); X.beginPath(); X.arc(540, 760, 1400 * eo(ir) + 1, 0, 6.29); X.clip(); sceneGum(t); X.restore(); X.save(); X.globalAlpha = Math.sin(ir * Math.PI) * .8; X.fillStyle = '#FFFFFF'; X.fillRect(0, 0, W, H); X.restore(); }
}
function gumState(t) {
  const clean = seg(t, K.deep, K.stains + .4), heal = eio(seg(t, K.gumcare, K.heal + .5));
  return { tartar: seg(t, K.tartar - .1, K.tartar + .9) * (1 - clean), dark: seg(t, K.tobacco - .1, K.tobacco + .6),
    inflame: eio(seg(t, K.attack - .1, K.attack + .6)) * (1 - heal * .85), gumY: lerp(-70, 90, eio(seg(t, K.pull - .2, K.pull + .7))),
    boneY: lerp(60, 230, eio(seg(t, K.bone, K.away + .4))), germ: seg(t, K.germs - .2, K.germs + .4) * (1 - seg(t, K.deep, K.stains)) };
}
function sceneGum(t) {
  bg([[0, '#1A1B4B'], [.6, '#2B2466'], [1, '#3E2B73']]);
  glow(540, 760, 820, 'rgba(110,140,255,.26)'); particles(t, 24, 19, 'rgba(160,200,255,.9)', 9, .5);
  const g = gumState(t), wob = Math.sin(t * 9) * .02 * seg(t, K.away - .3, K.away + .2) * (1 - seg(t, K.away + .8, K.away + 1.3));
  const z = lerp(.92, .8, eio(seg(t, K.bone - .4, K.bone + .2)));
  X.save(); X.translate(540, 780); X.scale(z, z); X.rotate(wob);
  const st = { thin: 0, gumY: g.gumY, boneY: g.boneY, seal: 0, tubes: 0, nerveHot: 0, glowRoot: 0, gumA: mixC('#F3899B', '#D9455E', g.inflame), gumB: mixC('#D9687D', '#A82F48', g.inflame), swell: g.inflame };
  toothXS(st, t);
  tartar(g.tartar, g.dark, t);
  if (g.germ > 0) { germs(10, g.germ, t, 250, g.gumY - 20, 70); germs(8, g.germ, t + 3, -250, g.gumY - 20, 70); }
  // smoke wisps darken the deposits on "tobacco"
  const sk = seg(t, K.tobacco - .2, K.tobacco + 1.0); if (sk > 0 && sk < 1) for (let i = 0; i < 6; i++) { const q = (sk + i * .12) % 1; X.save(); X.globalAlpha = Math.sin(sk * Math.PI) * .5 * (1 - q);
    X.strokeStyle = '#9A9AA8'; X.lineWidth = 22 - q * 10; X.lineCap = 'round'; X.beginPath(); X.moveTo(480 - q * 200, -300 + i * 30); X.bezierCurveTo(400 - q * 220, -260 + i * 20, 360 - q * 260, -200, 300 - q * 120, -140 + i * 10); X.stroke(); X.restore(); }
  // the clean: scaler chips the tartar, a polish cup spins, the enamel shines
  const ck = seg(t, K.deep - .1, K.stains + .5);
  if (ck > 0 && ck < 1) { const y = lerp(-180, -40, (Math.sin(t * 9) + 1) / 2);
    X.save(); X.globalAlpha = Math.sin(ck * Math.PI) * 1.4; X.translate(300, y); X.rotate(-.5); rr(0, -9, 320, 18, 9, '#C9D3DD'); X.strokeStyle = '#C9D3DD'; X.lineWidth = 10; X.lineCap = 'round'; X.beginPath(); X.moveTo(0, 0); X.quadraticCurveTo(-40, 0, -46, 28); X.stroke(); X.restore();
    for (let i = 0; i < 10; i++) { const q = ((t * 2.4 + rnd(i)) % 1); circle(250 + q * 200 * rnd(i + 4), y + (rnd(i + 8) - .5) * 80 - q * 90, 9 * (1 - q), `rgba(229,199,107,${(1 - q)})`); } }
  const pk = seg(t, K.stains - .3, K.stains + .9);
  if (pk > 0) { if (pk < 1) { X.save(); X.globalAlpha = Math.sin(pk * Math.PI) * 1.3; X.translate(0, -560); X.rotate(t * 14); ell(0, 0, 60, 60, '#7AD3F0'); X.strokeStyle = '#4BA9CC'; X.lineWidth = 8; for (let i = 0; i < 4; i++) { X.rotate(1.57); X.beginPath(); X.moveTo(0, 0); X.lineTo(52, 0); X.stroke(); } X.restore(); }
    X.save(); X.globalAlpha = clamp(pk * 2) * (.6 + .4 * Math.sin(t * 5)); for (let i = 0; i < 5; i++) sparkle(-200 + i * 100, -470 + Math.abs(i - 2) * 20, .8 + .4 * Math.sin(t * 6 + i), '#FFFFFF', 1, t * 2 + i); X.restore(); }
  X.restore();
  const ws = (lx, ly) => [540 + lx * z, 780 + ly * z];
  const tT = seg(t, K.tartar, K.tartar + .3) * (1 - seg(t, K.attack - .3, K.attack - .05)); if (tT > 0) { const [px, py] = ws(250, -110); label('TARTAR', 760, 280, tT, P.ink, '#F1D27A', 54, px, py); }
  const tG = seg(t, K.germs, K.germs + .3) * (1 - seg(t, K.attack - .3, K.attack - .05)); if (tG > 0) label('full of germs', 330, 1110, tG, P.ink, '#A8F0A8', 46);
  const tA = seg(t, K.attack, K.attack + .3) * (1 - seg(t, K.pull + .5, K.pull + .8)); if (tA > 0) { const [px, py] = ws(-330, g.gumY + 30); label('gums inflamed', 320, 280, tA, '#FFFFFF', '#C2334F', 48, px, py); }
  const tP = seg(t, K.pull, K.pull + .3) * (1 - seg(t, K.bone - .3, K.bone - .05)); if (tP > 0) { const [px, py] = ws(330, g.gumY + 20); label('pulling back', 760, 1110, tP, P.ink, '#FFC2CD', 46, px, py); }
  const tB = seg(t, K.bone, K.bone + .3) * (1 - seg(t, K.clinic0 - .5, K.clinic0 - .2)); if (tB > 0) { const [px, py] = ws(380, g.boneY + 60); label('bone wears away', 540, 1110, tB, P.ink, '#F6E7CF', 50, px, py); }
  const tC = seg(t, K.deep + .1, K.deep + .4) * (1 - seg(t, K.gumcare - .3, K.gumcare - .05)); if (tC > 0) label('deep cleaning + polish', 540, 280, tC, P.ink, '#9FF3E9', 50);
  const tH = seg(t, K.heal - .1, K.heal + .2) * (1 - seg(t, K.team - .3, K.team - .05)); if (tH > 0) label('gums heal', 540, 280, tH, P.ink, '#FFC2CD', 52);
}
function sceneClinicR(t) {
  bg([[0, '#E6F6FF'], [1, '#BFE3F7']]); rr(0, 1180, W, 740, 0, '#A9D3EA');
  X.save(); X.globalAlpha = .5; for (let i = 0; i < 5; i++) rr(40 + i * 210, 180, 170, 260, 24, '#FFFFFF'); X.restore();
  rr(560, 1020, 380, 70, 34, '#2E9CCB'); rr(560, 820, 80, 260, 36, '#2E9CCB'); rr(720, 1090, 60, 140, 12, '#8FA9BC');
  X.strokeStyle = '#8FA9BC'; X.lineWidth = 14; X.lineCap = 'round'; X.beginPath(); X.moveTo(930, 520); X.quadraticCurveTo(920, 680, 820, 760); X.stroke(); ell(940, 510, 80, 36, '#FFFFFF');
  const ek = eo(seg(t, K.clinic0 - .2, K.clinic0 + .4)); doctor(lerp(-200, 300, ek), 760, 1.0, t);
  ramesh(lerp(1300, 790, eo(seg(t, K.clinic0, K.clinic0 + .5))), 720, .85, { expr: 'smile', teeth: TEETH[4], gum: '#B4405A', recede: 1, t });
  label('dental clinic', 540, 300, seg(t, K.clinic0 + .2, K.clinic0 + .5), '#FFFFFF', '#2E9CCB', 52);
}
function sceneQuit(t) {   // "the team helps him quit, step by step": a streak, the packets fade, the clinician cheers him on
  bg([[0, '#1D4A63'], [1, '#226B73']]); particles(t, 20, 71, 'rgba(170,255,240,.9)', 8, .5);
  const k = eio(seg(t, K.team - .25, K.team + .2));
  X.save(); const e = back(clamp(k), 1.3); X.translate(540, 700); X.scale(e, e);
  X.shadowColor = 'rgba(0,0,0,.35)'; X.shadowBlur = 40; rr(-460, -420, 920, 840, 60, '#FFFFFF'); X.shadowColor = 'transparent';
  text('Quit plan', 0, -320, 70, P.ink, 800);
  const days = [1, 7, 14, 30], dk = seg(t, K.quit - .2, K.step + 1.2);
  days.forEach((d, i) => { const on = dk * 4 > i + .3, x = -330 + i * 220; circle(x, -160, 84, on ? P.green : '#E6EBF0'); text(`Day ${d}`, x, -160, 38, on ? '#FFFFFF' : '#9AA3AF', 800);
    if (i < 3) { X.fillStyle = on ? P.green : '#E6EBF0'; X.fillRect(x + 84, -166, 52, 12); } });
  const fade = seg(t, K.quit, K.step + 1.0);
  X.save(); X.globalAlpha = 1 - fade * .85; X.translate(-170, 90); X.scale(1.3 * (1 - fade * .4), 1.3 * (1 - fade * .4)); habitIcon('cig', 0, 0, 1, t); X.restore();
  X.save(); X.globalAlpha = 1 - fade * .85; X.translate(170, 90); X.scale(1.3 * (1 - fade * .4), 1.3 * (1 - fade * .4)); habitIcon('gutka', 0, 0, 1, t); X.restore();
  text('one step at a time', 0, 320, 58, '#2E9CCB', 800, 'center', seg(t, K.step, K.step + .3));
  X.restore();
}
// ---------- captions ----------
const CHUNKS = [];
LINES.forEach(L => { if (L.i === 12) return; let cur = [];
  L.words.forEach((w, j) => { cur.push(w); const end = /[.,?!]$/.test(w.w) || cur.length >= 4 || j === L.words.length - 1; if (end) { CHUNKS.push(cur); cur = []; } }); });
CHUNKS.forEach((c, i) => { c.t0 = c[0].s - .05; c.t1 = i + 1 < CHUNKS.length ? Math.min(CHUNKS[i + 1][0].s - .05, c[c.length - 1].e + .6) : c[c.length - 1].e + .6; });
const HOT = /^(colour|gums|chai|cigarette|gutka|papa|brown|worse|tartar|germs|tobacco|bone|clinic|cleaning|heal|quit|again)/i;
function captions(t) {
  const c = CHUNKS.find(c => t >= c.t0 && t < c.t1); if (!c) return;
  const k = seg(t, c.t0, c.t0 + .14); X.save(); X.font = '800 70px P'; X.textBaseline = 'middle';
  const parts = c.map(w => w.w.toUpperCase()), widths = parts.map(p => X.measureText(p).width), gap = 22, tw = widths.reduce((a, b) => a + b, 0) + gap * (parts.length - 1);
  let x = 540 - tw / 2; const y = 1240, sc = lerp(.9, 1, eo(k)) * Math.min(1, 980 / tw);
  X.translate(540, y); X.scale(sc, sc); X.translate(-540, -y); X.globalAlpha = clamp(k * 3);
  parts.forEach((p, i) => { const w = c[i], on = t >= w.s - .03, hot = HOT.test(w.w);
    X.lineJoin = 'round'; X.lineWidth = 16; X.strokeStyle = 'rgba(20,14,45,.92)'; X.strokeText(p, x, y);
    X.fillStyle = on ? (hot ? P.yellow : '#FFFFFF') : 'rgba(255,255,255,.55)'; X.fillText(p, x, y); x += widths[i] + gap; });
  X.restore();
}
// ---------- timeline ----------
function seek(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; X.clearRect(0, 0, W, H);
  const xf = (t0, d) => seg(t, t0, t0 + d);
  const over = (fn, a) => { if (a > 0) { X.save(); X.globalAlpha = a; fn(t); X.restore(); } };
  if (t < K.drew0 - .2) scenePortrait(t);
  else if (t < K.but) { sceneDrawing(t, false); over(scenePortrait, 1 - xf(K.drew0 - .2, .3)); }
  else if (t < K.worse + .45) { sceneDiveR(t); over(t => sceneDrawing(t, false), 1 - xf(K.but, .3)); }
  else if (t < K.clinic0 - .2) sceneGum(t);
  else if (t < K.deep - .25) { sceneClinicR(t); over(sceneGum, 1 - xf(K.clinic0 - .2, .3)); }
  else if (t < K.team - .3) { sceneGum(t); over(sceneClinicR, 1 - xf(K.deep - .25, .3)); }
  else if (t < K.again0 - .2) { sceneQuit(t); over(sceneGum, 1 - xf(K.team - .3, .3)); }
  else { sceneDrawing(t, true); over(sceneQuit, 1 - xf(K.again0 - .2, .3));
    const ck = seg(t, K.cta, K.cta + .3); if (ck > 0) { X.save(); X.globalAlpha = .55 * ck; X.fillStyle = '#2A1240'; X.fillRect(0, 1160, W, 170); X.restore();
      text("It's never too late.", 540, 1246, 80, '#FFFFFF', 800, 'center', ck, [P.ink, 10]); } }
  captions(t);
}
window.seek = seek;
window.ready = Promise.all(['500 40px P', '600 40px P', '700 40px P', '800 40px P'].map(f => document.fonts.load(f))).then(() => document.fonts.ready);
</script></body></html>
