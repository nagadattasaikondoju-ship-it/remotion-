"""Trim each chosen VO take, lay the lines end to end (rapid-fire, like the reference), write timeline.json + vo_track.wav.
usage: python3 build_timeline.py [l03=1 ...]   (pick take 1 instead of take 0 for a line)"""
import json, subprocess, sys, re, wave, contextlib
lines = json.load(open('script.json')); pick = dict(a.split('=') for a in sys.argv[1:])
GAP, LEAD, TAIL = .12, .06, 1.6
def dur(p):
    with contextlib.closing(wave.open(p)) as w: return w.getnframes() / w.getframerate()
out, t, parts = [], LEAD, []
for k, text in lines:
    src, dst = f'vo/{k}_t{pick.get(k, "0")}.wav', f'vo/{k}_trim.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse', '-ar', '48000', '-ac', '1', dst], check=True)
    d = dur(dst); t0, t1 = t, t + d
    # caption chunks: split on sentence/comma breaks, timed by characters
    chunks = [c.strip() for c in re.split(r'(?<=[!?.,])\s+', text) if c.strip()]
    merged = []
    for c in chunks:
        if merged and len(merged[-1]) + len(c) < 26: merged[-1] += ' ' + c
        else: merged.append(c)
    tot = sum(len(c) for c in merged); a = t0; caps = []
    for c in merged: b = a + d * len(c) / tot; caps.append([c, round(a, 3), round(b + (GAP if c == merged[-1] else 0), 3)]); a = b
    out.append({'id': k, 'text': text, 't0': round(t0, 3), 't1': round(t1, 3), 'caps': caps}); parts.append((dst, t0)); t = t1 + GAP
for i, l in enumerate(out): l['s0'] = 0 if i == 0 else out[i]['t0'] - .04; l['s1'] = out[i + 1]['t0'] - .04 if i + 1 < len(out) else t + TAIL
end = round(t + TAIL, 3); out[-1]['s1'] = end
json.dump({'lines': out, 'end': end}, open('timeline.json', 'w'), indent=1)
inputs = sum([['-i', p] for p, _ in parts], []); fc = ''.join(f'[{i}]adelay={int(t0*1000)}|{int(t0*1000)}[a{i}];' for i, (_, t0) in enumerate(parts))
fc += ''.join(f'[a{i}]' for i in range(len(parts))) + f'amix=inputs={len(parts)}:normalize=0,apad=whole_dur={end}[o]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', fc, '-map', '[o]', '-ar', '48000', 'vo/vo_track.wav'], check=True)
for l in out: print(f"{l['id']} {l['t0']:6.2f}-{l['t1']:6.2f}  {l['text']}")
print('pitch length', end)
