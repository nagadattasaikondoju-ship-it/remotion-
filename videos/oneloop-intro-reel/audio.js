/* Score, written in code with an OfflineAudioContext (deterministic: seeded noise, no timers). 120 BPM, 25 s.
   A kick on every beat, offbeat hats from bar 2, a sub/bass line that changes per bar, a hit on every scene change
   (2, 4, 8, 10, 16 [biggest], 18, 21), a riser 14 → 16 into the payoff, and a rising sweep while the Node draws the
   loops. The interface sounds (clicks, whooshes, pops) are real recordings placed by the SFX pipeline, not here. */
window.renderAudio = async () => {
  const SR = 48000, LEN = 25.6, ac = new OfflineAudioContext(2, Math.round(SR * LEN), SR);
  let seed = 11; const rnd = () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return (((t ^ (t >>> 14)) >>> 0) / 4294967296) * 2 - 1; };
  const noiseBuf = ac.createBuffer(1, SR * 2, SR); { const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = rnd(); }
  const ir = ac.createBuffer(2, SR * 1.6, SR); for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = rnd() * Math.pow(1 - i / d.length, 3.4); }
  const out = ac.createDynamicsCompressor(); out.threshold.value = -12; out.ratio.value = 3; out.attack.value = 0.003; out.release.value = 0.1; out.knee.value = 6; out.connect(ac.destination);
  const bus = ac.createGain(); bus.gain.value = 0.5; bus.connect(out);
  // music bus ducks under each kick (sidechain feel, written as gain automation)
  const mus = ac.createGain(); mus.gain.value = 1; mus.connect(bus);
  const verb = ac.createConvolver(); verb.buffer = ir; const verbIn = ac.createGain(); verbIn.gain.value = 0.25; verbIn.connect(verb); verb.connect(bus);
  const env = (g, t, a, peak, dec) => { g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + a); g.gain.exponentialRampToValueAtTime(0.0008, t + a + dec); };
  const noise = (t, type, f, q, peak, a, dec, { pan = 0, send = 0, f2, dest = bus } = {}) => {
    const s = ac.createBufferSource(); s.buffer = noiseBuf; const bq = ac.createBiquadFilter(); bq.type = type; bq.frequency.setValueAtTime(f, t); bq.Q.value = q;
    if (f2) bq.frequency.exponentialRampToValueAtTime(f2, t + a + dec);
    const g = ac.createGain(); env(g, t, a, peak, dec); const p = ac.createStereoPanner(); p.pan.value = pan;
    s.connect(bq); bq.connect(g); g.connect(p); p.connect(dest); if (send) { const sg = ac.createGain(); sg.gain.value = send; g.connect(sg); sg.connect(verbIn); }
    s.start(t, (t * 0.37) % 1.2); s.stop(t + a + dec + 0.05);
  };
  const tone = (t, type, f0, f1, glide, peak, a, dec, { pan = 0, send = 0, lp, dest = bus } = {}) => {
    const o = ac.createOscillator(); o.type = type; o.frequency.setValueAtTime(f0, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + glide);
    const g = ac.createGain(); env(g, t, a, peak, dec); let node = o;
    if (lp) { const f = ac.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = lp; o.connect(f); node = f; }
    const p = ac.createStereoPanner(); p.pan.value = pan; node.connect(g); g.connect(p); p.connect(dest);
    if (send) { const sg = ac.createGain(); sg.gain.value = send; g.connect(sg); sg.connect(verbIn); }
    o.start(t); o.stop(t + a + dec + 0.05);
  };
  const B = 0.5, NB = 50;
  // ---- kick on every beat (bar downbeats a touch heavier); the music bus ducks under it ----
  for (let b = 0; b < NB; b++) { const t = b * B, big = b % 4 === 0;
    tone(t, "sine", 160, 45, 0.1, big ? 1.0 : 0.85, 0.002, 0.36);
    noise(t, "highpass", 3000, 0.7, 0.16, 0.0005, 0.012);
    mus.gain.setValueAtTime(0.45, t); mus.gain.linearRampToValueAtTime(1, t + 0.22); }
  // ---- hats: offbeats from bar 2, 16ths through the results section (the frantic part) ----
  for (let b = 4; b < 49; b++) { noise(b * B + 0.25, "highpass", 8200, 0.8, 0.1, 0.001, 0.04, { pan: 0.15, dest: mus });
    if (b >= 20 && b < 32) { noise(b * B + 0.125, "highpass", 9500, 0.8, 0.045, 0.001, 0.025, { pan: -0.2, dest: mus }); noise(b * B + 0.375, "highpass", 9500, 0.8, 0.045, 0.001, 0.025, { pan: -0.2, dest: mus }); } }
  // ---- bass: one root per bar, eighth-note pulse; silent in the hook's first bar, drops out for the payoff bar ----
  const roots = [0, 41.2, 41.2, 49, 55, 43.65, 43.65, 49, 49, 0, 41.2, 55, 41.2];
  for (let b = 4; b < NB; b++) { const bar = Math.floor(b / 4), f = roots[bar]; if (!f || (b >= 32 && b < 36)) continue;
    for (const off of [0.0, 0.25]) { tone(b * B + off + 0.02, "sawtooth", f * 2, null, 0, 0.12, 0.008, 0.2, { lp: 480, dest: mus }); tone(b * B + off + 0.02, "sine", f, null, 0, 0.32, 0.008, 0.21, { dest: mus }); } }
  // ---- a three-note motif on the copper beats (the Node's own voice), quiet ----
  const motif = (t, k = 1) => [659.25, 783.99, 987.77].forEach((f, i) => tone(t + i * 0.125, "triangle", f, null, 0, 0.05 * k, 0.004, 0.2, { send: 0.5, pan: [-0.3, 0, 0.3][i], dest: mus }));
  [4, 8, 10, 12, 18, 21].forEach((t) => motif(t));
  // ---- hits on every scene change: low body + metallic partials + noise burst, with room ----
  const hit = (t, k) => { tone(t, "sine", 120, 36, 0.26, 0.6 * k, 0.002, 0.75);
    [523, 817, 1271].forEach((f, i) => tone(t, "square", f, f * 0.985, 0.3, 0.032 * k, 0.001, 0.34, { pan: [-0.35, 0, 0.35][i], send: 0.6, lp: 5200 }));
    noise(t, "bandpass", 1700, 0.9, 0.3 * k, 0.001, 0.3, { send: 0.8 }); };
  [2, 4, 8, 10, 18, 21].forEach((t) => hit(t, 1)); hit(16, 1.6);
  // ---- impact: the Node lands in the gap ----
  tone(1.0, "sine", 90, 40, 0.2, 0.7, 0.002, 0.5); noise(1.0, "lowpass", 900, 0.7, 0.3, 0.001, 0.18);
  // ---- riser 14 → 16, cut dead on the biggest beat ----
  { const t0 = 14.0, t1 = 15.985; const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true;
    const bq = ac.createBiquadFilter(); bq.type = "bandpass"; bq.Q.value = 2.4; bq.frequency.setValueAtTime(240, t0); bq.frequency.exponentialRampToValueAtTime(7600, t1);
    const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.4, t1 - 0.01); g.gain.linearRampToValueAtTime(0, t1);
    s.connect(bq); bq.connect(g); g.connect(bus); s.start(t0); s.stop(t1 + 0.02);
    const o = ac.createOscillator(); o.type = "sawtooth"; o.frequency.setValueAtTime(98, t0); o.frequency.exponentialRampToValueAtTime(784, t1);
    const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.setValueAtTime(380, t0); lp.frequency.exponentialRampToValueAtTime(5200, t1);
    const og = ac.createGain(); og.gain.setValueAtTime(0.0001, t0); og.gain.exponentialRampToValueAtTime(0.085, t1 - 0.01); og.gain.linearRampToValueAtTime(0, t1);
    o.connect(lp); lp.connect(og); og.connect(bus); o.start(t0); o.stop(t1 + 0.02); }
  // ---- the loops being drawn (18 → 19): a sweep that follows the pen ----
  { const o = ac.createOscillator(); o.type = "sine"; o.frequency.setValueAtTime(330, 18.0); o.frequency.exponentialRampToValueAtTime(660, 18.5); o.frequency.exponentialRampToValueAtTime(1318, 19.0);
    const g = ac.createGain(); g.gain.setValueAtTime(0.0001, 18.0); g.gain.exponentialRampToValueAtTime(0.06, 18.5); g.gain.exponentialRampToValueAtTime(0.0001, 19.05);
    o.connect(g); g.connect(verbIn); g.connect(bus); o.start(18.0); o.stop(19.1); }
  // ---- final chord under the end card, gone by 25.4 ----
  [220, 277.18, 329.63, 440].forEach((f, i) => { const o = ac.createOscillator(); o.type = "triangle"; o.frequency.value = f;
    const g = ac.createGain(); g.gain.setValueAtTime(0.0001, 21.0); g.gain.exponentialRampToValueAtTime(0.035, 21.4); g.gain.setValueAtTime(0.035, 24.6); g.gain.exponentialRampToValueAtTime(0.0001, 25.4);
    const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 2400; o.connect(lp); lp.connect(g); g.connect(mus); g.connect(verbIn); o.start(21.0); o.stop(25.5); });
  const buf = await ac.startRendering();
  const ch = [buf.getChannelData(0), buf.getChannelData(1)], n = buf.length, bytes = new ArrayBuffer(44 + n * 4), v = new DataView(bytes);
  const w = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  w(0, "RIFF"); v.setUint32(4, 36 + n * 4, true); w(8, "WAVE"); w(12, "fmt "); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true);
  v.setUint32(24, SR, true); v.setUint32(28, SR * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); w(36, "data"); v.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) for (let c = 0; c < 2; c++) v.setInt16(44 + i * 4 + c * 2, Math.max(-1, Math.min(1, ch[c][i])) * 32767, true);
  let bin = ""; const u8 = new Uint8Array(bytes); for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return btoa(bin);
};
