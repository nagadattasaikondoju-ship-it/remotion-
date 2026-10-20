/* Soundtrack, synthesised with an OfflineAudioContext (deterministic: seeded noise, no timers).
   120 BPM: kick on every beat, offbeat hats, a sub bass line, a hit on every scene change (each bar),
   a riser across bar 6 into the strongest bar, and textures on the on-screen events. */
window.renderAudio = async () => {
  const SR = 48000, LEN = 15, ac = new OfflineAudioContext(2, SR * LEN, SR);
  let seed = 7; const rnd = () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return (((t ^ (t >>> 14)) >>> 0) / 4294967296) * 2 - 1; };
  const noiseBuf = ac.createBuffer(1, SR * 2, SR); { const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = rnd(); }
  // short room so hits have air (decaying seeded noise impulse)
  const ir = ac.createBuffer(2, SR * 1.4, SR); for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = rnd() * Math.pow(1 - i / d.length, 3.2); }
  const out = ac.createDynamicsCompressor(); out.threshold.value = -10; out.ratio.value = 2.5; out.attack.value = 0.004; out.release.value = 0.12; out.knee.value = 6;
  out.connect(ac.destination);
  const bus = ac.createGain(); bus.gain.value = 0.55; bus.connect(out);
  const verb = ac.createConvolver(); verb.buffer = ir; const verbIn = ac.createGain(); verbIn.gain.value = 0.22; verbIn.connect(verb); verb.connect(bus);
  const env = (g, t, a, peak, dec, curve = "exp") => { g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + a);
    if (curve === "exp") g.gain.exponentialRampToValueAtTime(0.0008, t + a + dec); else g.gain.linearRampToValueAtTime(0, t + a + dec); };
  const noise = (t, dur, type, f, q, peak, a, dec, pan = 0, send = 0, f2) => {
    const s = ac.createBufferSource(); s.buffer = noiseBuf; const bq = ac.createBiquadFilter(); bq.type = type; bq.frequency.setValueAtTime(f, t); bq.Q.value = q;
    if (f2) bq.frequency.exponentialRampToValueAtTime(f2, t + dur);
    const g = ac.createGain(); env(g, t, a, peak, dec); const p = ac.createStereoPanner(); p.pan.value = pan;
    s.connect(bq); bq.connect(g); g.connect(p); p.connect(bus); if (send) { const sg = ac.createGain(); sg.gain.value = send; g.connect(sg); sg.connect(verbIn); }
    s.start(t, (t * 0.37) % 1.2); s.stop(t + a + dec + 0.05);
  };
  const tone = (t, type, f0, f1, glide, peak, a, dec, pan = 0, send = 0, lp) => {
    const o = ac.createOscillator(); o.type = type; o.frequency.setValueAtTime(f0, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + glide);
    const g = ac.createGain(); env(g, t, a, peak, dec); let node = o;
    if (lp) { const f = ac.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = lp; o.connect(f); node = f; }
    const p = ac.createStereoPanner(); p.pan.value = pan; node.connect(g); g.connect(p); p.connect(bus);
    if (send) { const sg = ac.createGain(); sg.gain.value = send; g.connect(sg); sg.connect(verbIn); }
    o.start(t); o.stop(t + a + dec + 0.05);
  };
  const BEAT = 0.5;
  // ---- kick on every beat ----
  for (let b = 0; b < 30; b++) { const t = b * BEAT, big = b % 4 === 0;
    tone(t, "sine", 150, 44, 0.11, big ? 0.95 : 0.82, 0.002, 0.38);
    noise(t, 0.01, "highpass", 2500, 0.7, 0.18, 0.0005, 0.012); }
  // ---- offbeat hats (from bar 2) and 16th ghost hats in the data bar ----
  for (let b = 4; b < 29; b++) { noise(b * BEAT + 0.25, 0.04, "highpass", 8000, 0.8, 0.11, 0.001, 0.045, 0.15);
    if (b >= 16 && b < 20) noise(b * BEAT + 0.375, 0.03, "highpass", 9000, 0.8, 0.05, 0.001, 0.03, -0.2); }
  // ---- sub bass: one root per bar, eighth-note pump ducked under the kick ----
  const roots = [55, 43.65, 65.41, 49, 55, 43.65, 41.2, 55]; // A  F  C  G  A  F  E  A
  for (let b = 2; b < 29; b++) { const bar = Math.floor(b / 4); const f = roots[bar];
    for (const off of [0.09, 0.3]) { tone(b * BEAT + off, "sawtooth", f * 2, null, 0, 0.14, 0.01, 0.17, 0, 0, 520);
      tone(b * BEAT + off, "sine", f, null, 0, 0.3, 0.01, 0.19); } }
  // ---- scene-change hits (bars 2..8): low body + bright metallic + noise, with room ----
  const hit = (t, k) => { tone(t, "sine", 110, 38, 0.25, 0.55 * k, 0.002, 0.7);
    [527, 811, 1263].forEach((f, i) => tone(t, "square", f, f * 0.985, 0.3, 0.035 * k, 0.001, 0.32, [-0.35, 0, 0.35][i], 0.6, 5000));
    noise(t, 0.3, "bandpass", 1800, 0.9, 0.32 * k, 0.001, 0.28, 0, 0.8); };
  [2, 4, 6, 8, 10, 14].forEach((t) => hit(t, 1)); hit(12, 1.55);
  // ---- riser across bar 6 into the strongest bar (cuts dead on 12.0) ----
  { const t0 = 10.0, t1 = 11.985; const s = ac.createBufferSource(); s.buffer = noiseBuf; s.loop = true;
    const bq = ac.createBiquadFilter(); bq.type = "bandpass"; bq.Q.value = 2.2; bq.frequency.setValueAtTime(260, t0); bq.frequency.exponentialRampToValueAtTime(7200, t1);
    const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(0.42, t1 - 0.01); g.gain.linearRampToValueAtTime(0, t1);
    s.connect(bq); bq.connect(g); g.connect(bus); s.start(t0); s.stop(t1 + 0.02);
    const o = ac.createOscillator(); o.type = "sawtooth"; o.frequency.setValueAtTime(110, t0); o.frequency.exponentialRampToValueAtTime(880, t1);
    const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.setValueAtTime(400, t0); lp.frequency.exponentialRampToValueAtTime(5000, t1);
    const og = ac.createGain(); og.gain.setValueAtTime(0.0001, t0); og.gain.exponentialRampToValueAtTime(0.09, t1 - 0.01); og.gain.linearRampToValueAtTime(0, t1);
    o.connect(lp); lp.connect(og); og.connect(bus); o.start(t0); o.stop(t1 + 0.02); }
  // ---- movements: whooshes peak on the fastest frame ----
  const whoosh = (tPeak, len, f0, f1, peak, pan = 0) => noise(tPeak - len * 0.7, len, "bandpass", f0, 1.4, peak, len * 0.7, len * 0.3, pan, 0.3, f1);
  whoosh(1.98, 0.42, 400, 3200, 0.22);  // push into the X
  whoosh(3.99, 0.3, 500, 4500, 0.2);    // dive into the full stop
  whoosh(7.9, 0.4, 300, 1800, 0.16);    // ribbon turns edge-on
  whoosh(9.98, 0.4, 3000, 600, 0.14);   // card rounds into the globe
  whoosh(12.05, 0.2, 2500, 400, 0.18);  // tear-off
  whoosh(13.7, 0.3, 600, 2600, 0.16);   // lock face-on
  // ---- textures on events ----
  const click = (t, f = 2400, peak = 0.16, pan = 0) => { tone(t, "sine", f, f * 0.6, 0.03, peak, 0.0008, 0.03, pan); noise(t, 0.01, "highpass", 4000, 0.7, peak * 0.5, 0.0005, 0.01, pan); };
  const pop = (t, peak = 0.2) => tone(t, "sine", 760, 300, 0.05, peak, 0.001, 0.07);
  [2.0, 2.5, 3.0, 3.5].forEach((t) => click(t, 1800, 0.18));                 // word slams
  for (let i = 0; i < 5; i++) click(2.5 + 0.03 * i, 3200, 0.07, -0.3 + 0.15 * i); // BUILD letters land
  for (let i = 0; i < 10; i++) click(3.52 + 0.03 * i, 4200, 0.05, -0.4 + 0.09 * i); // AUTOMATE slot roll
  [4.0, 4.5, 5.0, 5.5].forEach((t) => { pop(t, 0.17); noise(t, 0.12, "bandpass", 900, 1.2, 0.06, 0.005, 0.12, 0, 0.2, 3000); }); // morphs
  for (let k = 0; k < 24; k++) click(8.02 + 0.44 * (1 - Math.pow(1 - (k + 1) / 24, 1 / 0.9)) * 0.9, 3000 + k * 40, 0.045); // counter ticks
  [9.0, 9.125, 9.25, 9.375].forEach((t, i) => pop(t, 0.15 + 0.01 * i));     // country chips
  [10.08, 10.42, 10.86, 11.3, 11.74].forEach((t, i) => tone(t, "sine", 1568 + i * 196, null, 0, 0.06, 0.002, 0.25, 0, 0.5)); // city pings
  click(13.7, 1400, 0.22);                                                    // X snaps in
  click(1.0, 1400, 0.2);
  // ---- the collapse back into the dot: reverse suck that ends in silence (so the loop restarts clean) ----
  noise(14.6, 0.36, "bandpass", 500, 1.3, 0.18, 0.34, 0.02, 0, 0, 5000);
  const buf = await ac.startRendering();
  // 16-bit WAV
  const ch = [buf.getChannelData(0), buf.getChannelData(1)], n = buf.length, bytes = new ArrayBuffer(44 + n * 4), v = new DataView(bytes);
  const w = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  w(0, "RIFF"); v.setUint32(4, 36 + n * 4, true); w(8, "WAVE"); w(12, "fmt "); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true);
  v.setUint32(24, SR, true); v.setUint32(28, SR * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); w(36, "data"); v.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) for (let c = 0; c < 2; c++) v.setInt16(44 + i * 4 + c * 2, Math.max(-1, Math.min(1, ch[c][i])) * 32767, true);
  let bin = ""; const u8 = new Uint8Array(bytes); for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return btoa(bin);
};
