/* Soundtrack for the One Loop explainer, synthesised with an OfflineAudioContext (deterministic: seeded noise, no timers).
   120 BPM: kick on every beat, offbeat hats, a sub-bass line, a hit on every scene change, four risers that END on their
   transition frame (2 sharp-bass, 2 metallic), whooshes that peak on the fastest frame of each move, textures on events.
   Every cue time below is copied from the picture timeline in index.html. Fallback SFX: the Ultimate Editors library is
   not in this repo, so every sound here is generated. */
window.renderAudio = async () => {
  const SR = 48000, LEN = 76, ac = new OfflineAudioContext(2, SR * LEN, SR);
  let seed = 11; const rnd = () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return (((t ^ (t >>> 14)) >>> 0) / 4294967296) * 2 - 1; };
  const noiseBuf = ac.createBuffer(1, SR * 3, SR); { const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = rnd(); }
  const ir = ac.createBuffer(2, SR * 1.6, SR); for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = rnd() * Math.pow(1 - i / d.length, 3.4); }
  const out = ac.createDynamicsCompressor(); out.threshold.value = -12; out.ratio.value = 2.5; out.attack.value = 0.004; out.release.value = 0.14; out.knee.value = 6; out.connect(ac.destination);
  // families on their own buses (music · whooshes · textures · risers · hits) so levels follow the house standard
  const mk = (g) => { const n = ac.createGain(); n.gain.value = g; n.connect(out); return n; };
  const BUS = { music: mk(0.5), whoosh: mk(0.32), tex: mk(0.5), riser: mk(0.62), hit: mk(0.62) };
  const verb = ac.createConvolver(); verb.buffer = ir; const verbIn = ac.createGain(); verbIn.gain.value = 0.22; verbIn.connect(verb); verb.connect(BUS.hit);
  const env = (g, t, a, peak, dec) => { g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + a); g.gain.exponentialRampToValueAtTime(0.0008, t + a + dec); };
  const noise = (bus, t, dur, type, f, q, peak, a, dec, pan = 0, send = 0, f2) => {
    if (t < 0 || t > LEN) return;
    const s = ac.createBufferSource(); s.buffer = noiseBuf; const bq = ac.createBiquadFilter(); bq.type = type; bq.frequency.setValueAtTime(f, t); bq.Q.value = q;
    if (f2) bq.frequency.exponentialRampToValueAtTime(f2, t + dur);
    const g = ac.createGain(); env(g, t, a, peak, dec); const p = ac.createStereoPanner(); p.pan.value = pan;
    s.connect(bq); bq.connect(g); g.connect(p); p.connect(bus); if (send) { const sg = ac.createGain(); sg.gain.value = send; g.connect(sg); sg.connect(verbIn); }
    s.start(t, (t * 0.37) % 2.2); s.stop(t + a + dec + 0.05);
  };
  const tone = (bus, t, type, f0, f1, glide, peak, a, dec, pan = 0, send = 0, lp) => {
    if (t < 0 || t > LEN) return;
    const o = ac.createOscillator(); o.type = type; o.frequency.setValueAtTime(f0, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + glide);
    const g = ac.createGain(); env(g, t, a, peak, dec); let node = o;
    if (lp) { const f = ac.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = lp; o.connect(f); node = f; }
    const p = ac.createStereoPanner(); p.pan.value = pan; node.connect(g); g.connect(p); p.connect(bus);
    if (send) { const sg = ac.createGain(); sg.gain.value = send; g.connect(sg); sg.connect(verbIn); }
    o.start(t); o.stop(t + a + dec + 0.05);
  };
  const BEAT = 0.5;
  // gaps in the groove: the last beats of each riser, and the out-tail
  const rest = (t) => (t >= 11.0 && t < 12.0) || (t >= 17.0 && t < 18.0) || (t >= 49.0 && t < 50.0) || (t >= 64.5 && t < 66.0) || t >= 74.6;

  /* ---------- music: kick on every beat, hats, sub bass ---------- */
  for (let b = 0; b < LEN * 2; b++) { const t = b * BEAT; if (rest(t)) continue; const big = b % 4 === 0;
    tone(BUS.music, t, "sine", 150, 44, 0.11, big ? 0.95 : 0.8, 0.002, 0.36); noise(BUS.music, t, 0.01, "highpass", 2500, 0.7, 0.16, 0.0005, 0.012); }
  for (let b = 4; b < LEN * 2; b++) { const t = b * BEAT + 0.25; if (rest(t)) continue;
    noise(BUS.music, t, 0.04, "highpass", 8000, 0.8, 0.1, 0.001, 0.045, 0.15);
    if ((t > 18 && t < 50) || (t > 66 && t < 70)) noise(BUS.music, b * BEAT + 0.125, 0.03, "highpass", 9500, 0.8, 0.045, 0.001, 0.028, -0.2); }
  const roots = [55, 43.65, 65.41, 49]; // A F C G, one per bar
  for (let b = 2; b < LEN * 2; b++) { const t = b * BEAT; if (rest(t)) continue; const f = roots[Math.floor(b / 4) % 4];
    for (const off of [0.09, 0.3]) { tone(BUS.music, t + off, "sawtooth", f * 2, null, 0, 0.12, 0.01, 0.16, 0, 0, 520); tone(BUS.music, t + off, "sine", f, null, 0, 0.28, 0.01, 0.18); } }
  // a held pad under the end card so the out-tail is not empty
  [[220, -0.3], [277.2, 0.3], [329.6, 0]].forEach(([f, pan]) => tone(BUS.music, 74.0, "triangle", f, null, 0, 0.05, 0.6, 1.4, pan, 0.6, 1800));

  /* ---------- hits: one per scene change, the strongest stacks under the risers ---------- */
  const hit = (t, k = 1) => { tone(BUS.hit, t, "sine", 110, 36, 0.28, 0.55 * k, 0.002, 0.75);
    [527, 811, 1263].forEach((f, i) => tone(BUS.hit, t, "square", f, f * 0.985, 0.3, 0.03 * k, 0.001, 0.32, [-0.35, 0, 0.35][i], 0.6, 5000));
    noise(BUS.hit, t, 0.3, "bandpass", 1800, 0.9, 0.28 * k, 0.001, 0.28, 0, 0.8); };
  [2, 6, 8, 14, 16, 24.12, 26, 30, 34, 36, 40, 42, 46, 48, 52, 56, 58, 62, 64, 72].forEach((t) => hit(t, 0.8));
  [12, 18, 50, 70].forEach((t) => hit(t, 1.3));
  hit(66, 1.7); tone(BUS.hit, 66, "sine", 70, 28, 0.9, 0.7, 0.003, 1.6); // the loudest stack: riser → 66.0

  /* ---------- risers: END on the transition frame ---------- */
  const metallic = (t0, t1, k = 1) => { // inharmonic partials gliding up + a band sweep
    const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true; const bq = ac.createBiquadFilter(); bq.type = "bandpass"; bq.Q.value = 3;
    bq.frequency.setValueAtTime(400, t0); bq.frequency.exponentialRampToValueAtTime(9000, t1);
    const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.36 * k, t1 - 0.01); g.gain.linearRampToValueAtTime(0, t1);
    s.connect(bq); bq.connect(g); g.connect(BUS.riser); s.start(t0); s.stop(t1 + 0.02);
    [1, 2.76, 5.4].forEach((r, i) => { const o = ac.createOscillator(); o.type = "square"; o.frequency.setValueAtTime(180 * r, t0); o.frequency.exponentialRampToValueAtTime(720 * r, t1);
      const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.setValueAtTime(900, t0); lp.frequency.exponentialRampToValueAtTime(7000, t1);
      const og = ac.createGain(); og.gain.setValueAtTime(0.0001, t0); og.gain.exponentialRampToValueAtTime((0.035 / (i + 1)) * k, t1 - 0.01); og.gain.linearRampToValueAtTime(0, t1);
      const p = ac.createStereoPanner(); p.pan.value = [-0.4, 0.4, 0][i]; o.connect(lp); lp.connect(og); og.connect(p); p.connect(BUS.riser); o.start(t0); o.stop(t1 + 0.02); }); };
  const sharpBass = (t0, t1, k = 1) => { // sub sweep with grit + a hiss that opens up
    const o = ac.createOscillator(); o.type = "sawtooth"; o.frequency.setValueAtTime(38, t0); o.frequency.exponentialRampToValueAtTime(190, t1);
    const ws = ac.createWaveShaper(); const cv = new Float32Array(1024); for (let i = 0; i < 1024; i++) { const x = (i / 1023) * 2 - 1; cv[i] = Math.tanh(3 * x); } ws.curve = cv;
    const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.setValueAtTime(180, t0); lp.frequency.exponentialRampToValueAtTime(2400, t1);
    const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.32 * k, t1 - 0.01); g.gain.linearRampToValueAtTime(0, t1);
    o.connect(ws); ws.connect(lp); lp.connect(g); g.connect(BUS.riser); o.start(t0); o.stop(t1 + 0.02);
    const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true; const hp = ac.createBiquadFilter(); hp.type = "highpass"; hp.frequency.setValueAtTime(5000, t0); hp.frequency.exponentialRampToValueAtTime(900, t1);
    const ng = ac.createGain(); ng.gain.setValueAtTime(0.0001, t0); ng.gain.exponentialRampToValueAtTime(0.16 * k, t1 - 0.01); ng.gain.linearRampToValueAtTime(0, t1);
    s.connect(hp); hp.connect(ng); ng.connect(BUS.riser); s.start(t0); s.stop(t1 + 0.02); };
  metallic(10.0, 11.995);       // into the logo
  sharpBass(15.8, 17.995);      // into the growth path
  metallic(47.6, 49.995, 0.9);  // into proof
  sharpBass(63.6, 65.995, 1.15);// into the strongest moment (66.0)

  /* ---------- whooshes: peak on the fastest frame of each move ---------- */
  const whoosh = (tPeak, len, f0, f1, peak = 0.2, pan = 0) => noise(BUS.whoosh, tPeak - len * 0.7, len, "bandpass", f0, 1.4, peak, len * 0.7, len * 0.3, pan, 0.25, f1);
  whoosh(1.85, 0.4, 2400, 500, 0.22);        // the drop falls
  whoosh(6.15, 0.35, 500, 3000, 0.24);       // tiles thrown to the corners
  whoosh(7.8, 0.3, 3000, 600, 0.2);          // tiles pulled back
  whoosh(10.25, 0.45, 400, 2600, 0.24);      // square twists into the infinity
  for (let i = 0; i < 6; i++) whoosh(10.9 + i * 0.18 - i * i * 0.008, 0.16, 1500 + i * 300, 4000, 0.08 + 0.02 * i, (i % 2 ? 1 : -1) * 0.4); // dots racing
  whoosh(12.55, 0.35, 600, 2400, 0.18);      // rise into the lockup
  whoosh(13.95, 0.3, 2400, 700, 0.16);       // lockup flies up
  whoosh(17.85, 0.3, 700, 2800, 0.14);       // dot travels to the lens
  [19.85, 20.35, 20.85, 21.35].forEach((t, i) => whoosh(t - 0.12, 0.22, 900, 3200, 0.09, -0.3 + 0.2 * i)); // lens hunting
  whoosh(22.2, 0.35, 2600, 600, 0.14);       // browser steps back
  whoosh(24.0, 0.32, 500, 4200, 0.26);       // dive into the CTA
  whoosh(25.92, 0.3, 3000, 700, 0.16);       // check becomes the hero block
  [26.35, 26.85, 27.35, 27.62].forEach((t) => whoosh(t, 0.22, 800, 2600, 0.09)); // drags
  for (let k = 0; k < 6; k++) whoosh(29.98 + 0.5 * k + 0.08, 0.26, 3200, 800, 0.15, 0.3); // conveyor
  whoosh(33.15, 0.35, 800, 2400, 0.14);      // cards stack
  whoosh(30.05, 0.3, 2400, 600, 0.12, -0.4); // phone leaves
  whoosh(36.05, 0.3, 600, 2600, 0.14);       // RMC card
  whoosh(47.98, 0.32, 2600, 600, 0.14);      // pipeline leaves
  whoosh(49.98, 0.4, 400, 3600, 0.22);       // cream iris opens
  whoosh(55.98, 0.4, 3600, 400, 0.22);       // iris closes
  [56.35, 56.45, 56.55, 56.65].forEach((t, i) => whoosh(t, 0.3, 1200, 3000, 0.08, i % 2 ? 0.5 : -0.5)); // ticker rows
  whoosh(58.1, 0.4, 400, 1800, 0.16);        // globe grows
  whoosh(61.8, 0.3, 2400, 500, 0.18);        // globe collapses
  whoosh(64.0, 0.3, 2600, 600, 0.16);        // photos thrown out
  whoosh(65.92, 0.25, 3200, 400, 0.2);       // everything into one point
  whoosh(67.75, 0.5, 500, 2400, 0.16); whoosh(68.45, 0.5, 2400, 500, 0.16); // ribbon turns
  whoosh(69.45, 0.35, 600, 3000, 0.18);      // lock face-on
  whoosh(70.2, 0.35, 600, 2200, 0.15);       // rise into the lockup
  whoosh(72.22, 0.35, 2600, 700, 0.15);      // lockup to the top

  /* ---------- textures on events ---------- */
  const T = BUS.tex;
  const pop = (t, peak = 0.16, f = 760) => tone(T, t, "sine", f, f * 0.4, 0.05, peak, 0.001, 0.07);
  const click = (t, f = 2400, peak = 0.14, pan = 0) => { tone(T, t, "sine", f, f * 0.6, 0.03, peak, 0.0008, 0.03, pan); noise(T, t, 0.01, "highpass", 4000, 0.7, peak * 0.5, 0.0005, 0.01, pan); };
  const uiClick = (t) => { click(t, 1800, 0.22); noise(T, t + 0.035, 0.01, "highpass", 3000, 0.7, 0.1, 0.0005, 0.012); };
  const scifi = (t, k = 1) => { tone(T, t, "square", 1320, 660, 0.06, 0.05 * k, 0.001, 0.09, 0, 0.3, 4000); tone(T, t, "sine", 2640, 1980, 0.05, 0.08 * k, 0.001, 0.08); };
  const shutter = (t) => { noise(T, t, 0.02, "bandpass", 3500, 1.5, 0.3, 0.0005, 0.025); noise(T, t + 0.06, 0.02, "bandpass", 2800, 1.5, 0.22, 0.0005, 0.03); }; // camera click
  const success = (t) => [1046.5, 1318.5, 1568].forEach((f, i) => tone(T, t + i * 0.06, "sine", f, null, 0, 0.09, 0.003, 0.35, 0, 0.5));
  const plip = (t, f) => tone(T, t, "sine", f, f * 2.2, 0.04, 0.07, 0.001, 0.06);
  const ping = (t, f) => tone(T, t, "sine", f, null, 0, 0.07, 0.002, 0.3, 0, 0.5);
  const slam = (t) => { pop(t, 0.15, 520); noise(T, t, 0.05, "lowpass", 1200, 0.7, 0.14, 0.001, 0.06); };
  // headline words
  [0, 0.5, 0.75, 1.0, 3.0, 3.12, 3.5, 3.62, 6.0, 6.25, 6.5, 7.0, 8.0, 8.2, 8.4, 8.75, 9.0, 16.0, 16.25, 16.5, 16.75, 17.0, 22.0, 22.2, 22.4, 22.5, 23.0, 24.12, 24.32, 24.5,
    33.0, 33.2, 33.4, 35.0, 35.5, 35.7, 41.0, 41.5, 41.75, 44.0, 44.2, 44.5, 46.5, 47.0, 50.5, 51.0, 58.0, 58.12, 58.5, 58.62, 64.0, 64.15, 64.3, 64.45, 72.25, 72.37, 72.6]
    .forEach((t) => click(t, 2000, 0.07));
  [14.0, 14.5, 15.0, 15.5].forEach(slam);                                  // AUDIT. BUILD. MARKET. AUTOMATE.
  pop(1.25, 0.18); [2.25, 2.5, 2.75, 3.0].forEach((t) => pop(t, 0.14, 640)); // full stop; vendor tiles
  [4.0, 4.5, 5.0, 5.5].forEach((t) => pop(t, 0.16, 880));                 // leak labels
  for (let i = 0; i < 22; i += 2) plip(4.0 + i * 0.1 + 0.55, 900 + (i % 5) * 120); // drops landing
  [8.35, 8.75, 9.25, 9.75].forEach((t) => scifi(t));                       // stitches
  click(12.04, 1400, 0.24); click(69.74, 1400, 0.24);                       // X snaps in
  for (let i = 0; i < 9; i++) click(12.6 + 0.04 * i, 3200, 0.05, -0.4 + 0.1 * i); // wordmark letters
  [18.0, 18.25, 18.5, 18.75, 19.0].forEach((t) => pop(t, 0.12, 700));       // site layers
  [20.0, 20.5, 21.0, 21.5].forEach((t) => { scifi(t, 1.2); pop(t, 0.1, 500); }); // bottleneck pins
  uiClick(24.75); for (let i = 0; i < 4; i++) click(25.05 + i * 0.11, 3000, 0.04); success(25.5); // CTA click → loader → check
  [26.5, 27.0, 27.5, 27.75].forEach((t) => uiClick(t));                     // blocks snap in
  scifi(28.0); noise(T, 28.5, 0.35, "bandpass", 1500, 1.2, 0.08, 0.3, 0.05, 0, 0, 6000); // photo lands; load bar
  [28.5, 29.0, 29.5].forEach((t) => pop(t, 0.12, 820));
  for (let k = 0; k < 6; k++) click(29.95 + 0.5 * k + 0.2, 1600, 0.12);    // product cards land
  [34.0, 34.5, 34.75, 35.0, 35.5].forEach((t, i) => pop(t, 0.14, 600 + i * 60)); // channels
  pop(36.3, 0.12); for (let i = 0; i < 14; i++) click(36.75 + i * 0.045, 2600 + i * 60, 0.05); // leads count up
  pop(38.05, 0.12); for (let i = 0; i < 12; i++) click(38.45 + i * 0.045, 3200 - i * 80, 0.05); // CPL counts down
  scifi(39.25, 1.4);                                                         // −79%
  [40.0, 40.25, 40.5, 40.75].forEach(shutter);                               // photos: camera click, diegetic
  [42.0, 42.5, 43.0, 43.5].forEach((t) => pop(t, 0.13, 560));               // nodes
  [44.0, 44.5, 45.0, 45.5].forEach((t) => { plip(t, 1200); plip(t + 0.9, 1500); }); // leads in / out
  pop(44.9, 0.16, 980); pop(44.96, 0.1, 1300);                              // message sent
  tone(T, 46.5, "sawtooth", 98, null, 0, 0.06, 0.005, 0.35, 0, 0, 600);     // error: very low buzzer
  for (let i = 0; i < 6; i++) click(46.75 + i * 0.09, 2800, 0.04); success(47.25); // self-correction
  [48.1, 48.22, 48.34, 48.46, 48.58].forEach((t) => click(t, 1700, 0.05)); pop(48.9, 0.1);
  [52.0, 54.0, 55.0].forEach((t) => scifi(t, 1.3)); [53.0, 53.1].forEach((t) => pop(t, 0.12, 500));
  pop(56.0, 0.16, 500);
  [58.5, 59.0, 59.5, 60.5, 61.0, 61.5].forEach((t, i) => ping(t, 1568 + i * 196)); // city pins
  [62.0, 62.25, 62.5].forEach(shutter);                                      // team photos
  pop(63.0, 0.15, 520); [0, 1, 2, 3, 4].forEach((i) => pop(64.75 + 0.07 * i, 0.09, 700 + i * 80)); [65.2, 65.32].forEach((t) => pop(t, 0.12, 600));
  for (let i = 0; i < 9; i++) click(70.15 + 0.04 * i, 3200, 0.05, -0.4 + 0.1 * i); noise(T, 70.35, 0.3, "bandpass", 2500, 1, 0.05, 0.2, 0.1);
  pop(73.0, 0.13); uiClick(73.72); success(73.75); [74.0, 74.4, 74.7].forEach((t) => click(t, 2000, 0.07));

  const buf = await ac.startRendering();
  const ch = [buf.getChannelData(0), buf.getChannelData(1)], n = buf.length, bytes = new ArrayBuffer(44 + n * 4), v = new DataView(bytes);
  const w = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  w(0, "RIFF"); v.setUint32(4, 36 + n * 4, true); w(8, "WAVE"); w(12, "fmt "); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true);
  v.setUint32(24, SR, true); v.setUint32(28, SR * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); w(36, "data"); v.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) for (let c = 0; c < 2; c++) v.setInt16(44 + i * 4 + c * 2, Math.max(-1, Math.min(1, ch[c][i])) * 32767, true);
  let bin = ""; const u8 = new Uint8Array(bytes); for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return btoa(bin);
};
