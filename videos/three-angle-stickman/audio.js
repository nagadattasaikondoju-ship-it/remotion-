/* Music bed, written in code (OfflineAudioContext, seeded, deterministic). Upbeat corporate/tech, 112 BPM, C major:
   soft kick, offbeat shaker, clap on 2 and 4, a plucked arpeggio over C–G–Am–F, a quiet pad; it resolves on C at 41.8 s.
   It is mixed low and ducked under the voice in assemble.sh. */
window.renderAudio = async () => {
  const SR = 48000, LEN = 42.5, ac = new OfflineAudioContext(2, Math.round(SR * LEN), SR);
  let seed = 5; const rnd = () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return (((t ^ (t >>> 14)) >>> 0) / 4294967296) * 2 - 1; };
  const nb = ac.createBuffer(1, SR, SR); { const d = nb.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = rnd(); }
  const ir = ac.createBuffer(2, SR * 1.2, SR); for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = rnd() * Math.pow(1 - i / d.length, 3); }
  const bus = ac.createGain(); bus.gain.value = 0.42; const comp = ac.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 3; bus.connect(comp); comp.connect(ac.destination);
  const verb = ac.createConvolver(); verb.buffer = ir; const vin = ac.createGain(); vin.gain.value = 0.2; vin.connect(verb); verb.connect(bus);
  const env = (g, t, a, p, d) => { g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(p, t + a); g.gain.exponentialRampToValueAtTime(0.0006, t + a + d); };
  const tone = (t, type, f, p, a, d, { pan = 0, lp, send = 0, f1, glide } = {}) => { const o = ac.createOscillator(); o.type = type; o.frequency.setValueAtTime(f, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + glide);
    const g = ac.createGain(); env(g, t, a, p, d); let n = o; if (lp) { const fl = ac.createBiquadFilter(); fl.type = "lowpass"; fl.frequency.value = lp; o.connect(fl); n = fl; }
    const pn = ac.createStereoPanner(); pn.pan.value = pan; n.connect(g); g.connect(pn); pn.connect(bus); if (send) { const s = ac.createGain(); s.gain.value = send; g.connect(s); s.connect(vin); } o.start(t); o.stop(t + a + d + 0.05); };
  const noise = (t, type, f, q, p, a, d, pan = 0) => { const s = ac.createBufferSource(); s.buffer = nb; const b = ac.createBiquadFilter(); b.type = type; b.frequency.value = f; b.Q.value = q;
    const g = ac.createGain(); env(g, t, a, p, d); const pn = ac.createStereoPanner(); pn.pan.value = pan; s.connect(b); b.connect(g); g.connect(pn); pn.connect(bus); s.start(t, (t * 0.31) % 0.8); s.stop(t + a + d + 0.05); };
  const BPM = 112, B = 60 / BPM, BAR = 4 * B, END = 41.8;
  const chords = [[261.63, 329.63, 392.0], [196.0, 246.94, 293.66], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63]]; // C G Am F
  const roots = [65.41, 49.0, 55.0, 43.65];
  for (let bar = 0; bar * BAR < END; bar++) {
    const t0 = 0.05 + bar * BAR, ch = chords[bar % 4], r = roots[bar % 4], intro = bar < 1;
    for (let b = 0; b < 4; b++) { const t = t0 + b * B; if (t > END) break;
      if (!intro) tone(t, "sine", 120, 0.5, 0.002, 0.22, { f1: 48, glide: 0.09 });                       // soft kick
      noise(t + B / 2, "highpass", 7000, 0.7, intro ? 0.05 : 0.09, 0.002, 0.05, 0.2);                     // offbeat shaker
      if (!intro && (b === 1 || b === 3)) noise(t, "bandpass", 1500, 0.8, 0.16, 0.002, 0.11, -0.1);       // clap
      // plucked arpeggio, eighth notes
      for (let e = 0; e < 2; e++) { const n = ch[(b * 2 + e) % 3] * (e ? 2 : 1); tone(t + e * B / 2, "triangle", n, 0.11, 0.003, 0.24, { pan: e ? 0.25 : -0.25, send: 0.4 }); tone(t + e * B / 2, "square", n, 0.018, 0.003, 0.12, { lp: 2600, pan: e ? 0.25 : -0.25 }); }
      if (!intro) tone(t + 0.01, "sawtooth", r * 2, 0.06, 0.01, B * 0.8, { lp: 420 });                     // bass
    }
    ch.forEach((f, i) => { const o = ac.createOscillator(); o.type = "sawtooth"; o.frequency.value = f; o.detune.value = (i - 1) * 6; const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 900;
      const g = ac.createGain(); const te = Math.min(t0 + BAR, END + 0.6); g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(0.022, t0 + 0.3); g.gain.setValueAtTime(0.022, te - 0.25); g.gain.linearRampToValueAtTime(0, te);
      o.connect(lp); lp.connect(g); g.connect(bus); o.start(t0); o.stop(te + 0.05); });
  }
  // resolve: a plucked C chord and a soft low C on the last word, ringing out
  [261.63, 329.63, 392.0, 523.25].forEach((f, i) => tone(END + i * 0.03, "triangle", f, 0.1, 0.004, 0.9, { send: 0.6, pan: (i - 1.5) * 0.2 }));
  tone(END, "sine", 65.41, 0.3, 0.01, 0.9);
  const buf = await ac.startRendering();
  const ch = [buf.getChannelData(0), buf.getChannelData(1)], n = buf.length, bytes = new ArrayBuffer(44 + n * 4), v = new DataView(bytes);
  const w = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  w(0, "RIFF"); v.setUint32(4, 36 + n * 4, true); w(8, "WAVE"); w(12, "fmt "); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 2, true);
  v.setUint32(24, SR, true); v.setUint32(28, SR * 4, true); v.setUint16(32, 4, true); v.setUint16(34, 16, true); w(36, "data"); v.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) for (let c = 0; c < 2; c++) v.setInt16(44 + i * 4 + c * 2, Math.max(-1, Math.min(1, ch[c][i])) * 32767, true);
  let bin = ""; const u8 = new Uint8Array(bytes); for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
  return btoa(bin);
};
