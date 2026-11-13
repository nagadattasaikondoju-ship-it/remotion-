#!/usr/bin/env bash
# Three Angle Method stickman explainer: 24 fps frames → H.264; Kokoro voice (one continuous master) + code music bed
# ducked under it + real CC0 SFX placed by Real SFX from sfx_cues.json; two-pass loudnorm to −14 LUFS.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=ThreeAngleMethod_Stickman_1920x1080_24fps; END=42.5
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
[ -f out/music_raw.wav ] || { echo "run: node render.mjs audio"; exit 1; }
# ---- picture ----
if [ -n "${REDO_VIDEO:-}" ] || [ ! -f out/video.mp4 ]; then
ffmpeg -nostdin -v error -y -framerate 24 -i out/frames/f_%05d.png -vf "format=yuv420p" -c:v libx264 -preset slow -crf 12 -tune animation \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 24 -movflags +faststart out/video.mp4
fi
# ---- voice: one continuous take, cleaned and levelled ----
ffmpeg -nostdin -v error -y -i voice/voice_master.wav -af "highpass=f=80,equalizer=f=250:t=q:w=1:g=-1.5,equalizer=f=3200:t=q:w=1:g=2,deesser=i=0.3,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=3,alimiter=limit=0.9,apad=whole_dur=$END,atrim=0:$END" -ac 2 -ar 48000 out/voice.wav
# ---- music: low, and ducked by the voice (sidechain) ----
ffmpeg -nostdin -v error -y -i out/music_raw.wav -i out/voice.wav -filter_complex \
  "[0:a]volume=-15dB,atrim=0:$END[m];[1:a]asplit=2[k][v];[m][k]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=380:makeup=1[md];[md][v]amix=inputs=2:normalize=0:duration=longest,atrim=0:$END" \
  -c:a pcm_s24le out/bed.wav
ffmpeg -nostdin -v error -y -i out/music_raw.wav -i out/voice.wav -filter_complex "[0:a]volume=-15dB,atrim=0:$END[m];[m][1:a]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=380:makeup=1" -c:a pcm_s24le out/music_ducked.wav
# ---- real SFX on their frames ----
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/bed.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_v.mov
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/st_sfx.mp4" --base-audio "$HERE/out/bed.wav" --sfx-trim-db 9)
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/st_sfx_resolved_cues.json" "$W/result/st_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; sed -n 1,16p "$W/result/critique.txt"
cp "$W/result/st_sfx_sfx_track.wav" out/stems/sfx.wav; cp out/voice.wav out/stems/voice.wav; cp out/music_ducked.wav out/stems/music.wav
ffmpeg -nostdin -v error -y -i out/bed.wav -i out/stems/sfx.wav -filter_complex "amix=inputs=2:normalize=0:duration=first,atrim=0:$END" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,atrim=0:$END" -c:a pcm_s24le out/mix_master.wav
# ---- deliverables ----
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 14 -tune animation -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 320k -movflags +faststart -shortest out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 19 -tune animation -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 192k -movflags +faststart -shortest out/${N}_share.mp4
for f in out/${N}_*.mp4; do echo "$f"; ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,width,height,r_frame_rate:format=duration,size -of csv=p=0 "$f"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
rm -f out/_pre.wav out/video_v.mov
