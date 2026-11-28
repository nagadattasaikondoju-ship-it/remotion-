"""Audio for the One Loop meme reel.
0-37.667 s : the reference scene's own audio.   37.667 s on: Naga's cloned voice (VO track) over the reference's beat
(separated from its dub voice with Demucs, looped on 8-bar boundaries, ducked under the voice), plus four real SFX from the
CC0 library on the moments that matter: the cut, the first lead ping, the 66 reveal and the end card."""
import json, subprocess
P0 = 37.667; TL = json.load(open('timeline.json')); END = TL['end']; L = {l['id']: l for l in TL['lines']}
at = lambda k, w: L[k]['t0'] + (L[k]['t1'] - L[k]['t0']) * max(0, L[k]['text'].find(w)) / len(L[k]['text'])
SFX = '../../assets/sfx/openverse/'
cues = [  # (file, time in pitch, gain dB)  -- textures -6/-7, whoosh -12, impact under the cut
  (SFX + 'impact/cinematic-impact_2e291c.mp3', 0.0, -9),
  (SFX + 'chime/chime-notification_adb6e2.mp3', at('l06', 'leads') + .05, -14),
  (SFX + 'soft-pop/single-pop_fa52a6.wav', at('l07', 'sixty'), -10),
  (SFX + 'whoosh/deep-whoosh-3_dabfec.mp3', L['l10']['t0'] - .25, -14),
]
run = lambda *a: subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
BED = 'out/sep/htdemucs/pitch_ref/no_vocals.wav'; B0, BAR8 = .464, 32 * .4645
fc = (f"[0]atrim={.067}:{B0 + BAR8},asetpts=PTS-STARTPTS[a];[1]atrim={B0}:{B0 + BAR8},asetpts=PTS-STARTPTS[b];[2]atrim={B0}:{B0 + BAR8},asetpts=PTS-STARTPTS[c];"
      f"[a][b]acrossfade=d=0.02[ab];[ab][c]acrossfade=d=0.02,atrim=0:{END},afade=t=out:st={END - 1.3}:d=1.3[o]")
run('-i', BED, '-i', BED, '-i', BED, '-filter_complex', fc, '-map', '[o]', '-ar', '48000', '-ac', '2', 'out/bed.wav')
ins = ['-i', 'vo/vo_track.wav', '-i', 'out/bed.wav'] + sum([['-i', f] for f, _, _ in cues], [])
fc = "[0]aformat=channel_layouts=stereo,volume=1.0,asplit=2[vo][sc];[1]volume=-3dB[bed0];[bed0][sc]sidechaincompress=threshold=0.05:ratio=4:attack=15:release=250[bed];"
for i, (_, t, g) in enumerate(cues): fc += f"[{i + 2}]aformat=channel_layouts=stereo,volume={g}dB,adelay={int(t * 1000)}|{int(t * 1000)}[s{i}];"
fc += '[vo][bed]' + ''.join(f'[s{i}]' for i in range(len(cues))) + f'amix=inputs={2 + len(cues)}:normalize=0,atrim=0:{END}[p]'
run(*ins, '-filter_complex', fc, '-map', '[p]', '-ar', '48000', 'out/pitch_audio.wav')
run('-i', 'ref/reference.mp4', '-t', str(P0), '-vn', '-af', f'afade=t=out:st={P0 - .06}:d=0.06', '-ar', '48000', '-ac', '2', 'out/film_audio.wav')
# match the pitch loudness to the film's so the switch is a voice change, not a volume jump
run('-i', 'out/film_audio.wav', '-i', 'out/pitch_audio.wav', '-filter_complex', '[0][1]concat=n=2:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', 'out/full_audio.wav')
print('cues', [(round(t, 2), f.split('/')[-1]) for f, t, _ in cues])
