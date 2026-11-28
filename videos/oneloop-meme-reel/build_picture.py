"""Picture for the One Loop meme reel.
film.mp4  : the reference's setup 0-37.667 s (internal concept use), fitted to 1080x1920 (same black letterbox)
pitch_bg  : One Loop B-roll cut to the confession lines, inside the reference's picture box (18,544 1043x875)"""
import json, subprocess
P0, FPS, BX, BY, BW, BH = 37.667, 30, 18, 544, 1043, 875
EDL = {   # line -> [(clip, in-point s)], the line's scene time is split evenly between its clips
  'l01': [('0612', 2.0)], 'l02': [('0720', 5.2)], 'l03': [('0705', 1.0), ('0687', 1.0)], 'l04': [('0723', .3)],
  'l05': [('0724', .2)], 'l06': [('0728', 3.6), ('0732', 2.6)], 'l07': [('0680', 4.0)], 'l08': [('0612', 8.0), ('0633', 3.0)],
  'l09': [('0726', .3)], 'l10': [('0741', 3.0)] }
LANDSCAPE = {'0633'}
run = lambda *a: subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
TL = json.load(open('timeline.json'))
segs = []
for l in TL['lines']:
    clips = EDL[l['id']]; d = (l['s1'] - l['s0']) / len(clips)
    for j, (c, a) in enumerate(clips): segs.append((c, a, d))
parts = []
for i, (c, a, d) in enumerate(segs):
    rot = '' if c in LANDSCAPE else 'transpose=2,'
    vf = (f"{rot}scale={BW}:{BH}:force_original_aspect_ratio=increase,crop={BW}:{BH},"
          f"scale=w='{BW}*(1+0.06*t/{d:.3f})':h='{BH}*(1+0.06*t/{d:.3f})':eval=frame,crop={BW}:{BH},"
          f"fps={FPS},setsar=1,tpad=stop_mode=clone:stop_duration=4,trim=duration={d:.4f},setpts=PTS-STARTPTS")
    o = f'out/seg_{i:02d}.mp4'; run('-ss', str(a), '-i', f'broll/MVI_{c}.MP4', '-an', '-vf', vf, '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', o); parts.append(o)
open('out/segs.txt', 'w').write(''.join(f"file '{p[4:]}'\n" for p in parts))
run('-f', 'concat', '-safe', '0', '-i', 'out/segs.txt', '-vf', f'pad=1080:1920:{BX}:{BY}:black,fps={FPS},trim=duration={TL["end"]}', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', 'out/pitch_bg.mp4')
run('-i', 'ref/reference.mp4', '-t', str(P0), '-an', '-vf', f'scale=1043:1920:flags=lanczos,unsharp=5:5:0.6,pad=1080:1920:{BX}:0:black,fps={FPS},setsar=1', '-c:v', 'libx264', '-crf', '14', '-preset', 'fast', '-pix_fmt', 'yuv420p', 'out/film.mp4')
print('segments', len(segs), 'pitch', TL['end'])
