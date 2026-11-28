# Lays the voice lines on the reference's phrase starts (vo/lines.tsv: start, slot end, text); a line longer than its slot
# is sped up gently (atempo <= 1.12) -> vo/voice.wav (49.77 s, 48 kHz), and Whisper word timings -> vo/words.json
import subprocess, json, numpy as np, soundfile as sf
SR, DUR = 48000, 49.77
L = [l.rstrip('\n').split('\t') for l in open('vo/lines.tsv')]
out = np.zeros(int(DUR * SR), np.float32)
for i, (a, b, t) in enumerate(L, 1):
    x, sr = sf.read(f'vo/t{i}.wav', dtype='float32'); x = x if x.ndim == 1 else x.mean(1)
    k = len(x) / SR / (float(b) - float(a))
    if k > 1.0:
        tempo = min(1.12, k)
        x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-', '-af', f'atempo={tempo:.4f}', '-f', 'f32le', '-'],
                                         input=x.tobytes(), capture_output=True).stdout, np.float32)
    s = int(float(a) * SR); n = min(len(x), len(out) - s); out[s:s + n] += x[:n]
    print(f'{i:2d} at {float(a):6.2f} len {len(x)/SR:5.2f} ends {float(a)+len(x)/SR:6.2f} (next {L[i][0] if i < len(L) else "-"})  {t[:40]}')
sf.write('vo/voice.wav', out / max(1e-6, np.abs(out).max()) * 0.89, SR)
