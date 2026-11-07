# Final mix: the score (widened mid/side so it isn't near-mono; kick and bass stay centred) + the real-sfx SFX track
# → out/mix.wav. Stems come from real-sfx's mix.py (out/stems/music.wav = base, out/stems/sfx.wav = SFX at mix level).
import os, numpy as np, soundfile as sf
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
m, sr = sf.read(os.path.join(P, "stems", "music.wav"), always_2d=True); s, sr2 = sf.read(os.path.join(P, "stems", "sfx.wav"), always_2d=True)
assert sr == sr2
mid, side = (m[:, 0] + m[:, 1]) / 2, (m[:, 0] - m[:, 1]) / 2 * 2.6
m = np.stack([mid + side, mid - side], 1)
n = max(len(m), len(s)); mix = np.zeros((n, 2)); mix[:len(m)] += m; mix[:len(s)] += s[:, :2]
mix *= min(1, 0.95 / np.abs(mix).max())
sf.write(os.path.join(P, "mix.wav"), mix.astype(np.float32), sr)
print("mix.wav", n / sr, "s")
