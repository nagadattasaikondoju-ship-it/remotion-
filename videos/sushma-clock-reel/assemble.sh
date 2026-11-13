#!/bin/bash
# Picture (render.mjs video) + the reference reel's own background song (one loop, 18.73 s, cut from the user's
# recording into assets/song_ref.wav) + real CC0 SFX placed by the Real SFX skill from sfx_cues.json.
# Two-pass loudnorm to −14 LUFS → MASTER + share. SONG=0 makes the SFX-only version (for adding a song in Instagram).
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
END=18.73; SONG=${SONG:-1}
N=DrSriSushma_ToothClock_1080x1920_60fps$([ "$SONG" = 1 ] || echo "_SFX-only")
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
[ -f out/video.mp4 ] || node render.mjs video 60
# ---- bed: the song at −16 LUFS (or silence) ----
if [ "$SONG" = 1 ]; then
  ffmpeg -nostdin -v error -y -i assets/song_ref.wav -af "loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,apad=whole_dur=$END,atrim=0:$END" -c:a pcm_s24le out/bed.wav
else
  ffmpeg -nostdin -v error -y -f lavfi -i anullsrc=r=48000:cl=stereo -t $END -c:a pcm_s24le out/bed.wav
fi
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/bed.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_v.mov
# ---- real SFX on their frames, over the bed ----
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/clk_sfx.mp4" --base-audio "$HERE/out/bed.wav" --sfx-trim-db ${SFX_TRIM:-4})
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/clk_sfx_resolved_cues.json" "$W/result/clk_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; sed -n 1,16p "$W/result/critique.txt"
cp "$W/result/clk_sfx_sfx_track.wav" out/stems/sfx.wav; cp out/bed.wav out/stems/song.wav
ffmpeg -nostdin -v error -y -i out/bed.wav -i out/stems/sfx.wav -filter_complex "[1:a]apad=whole_dur=$END[s];[0:a][s]amix=inputs=2:normalize=0:duration=first,atrim=0:$END" -c:a pcm_f32le out/_pre.wav
TARGET=$([ "$SONG" = 1 ] && echo -14 || echo -20)
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=$TARGET:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=$TARGET:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,atrim=0:$END" -c:a pcm_s24le out/mix_master.wav
# ---- deliverables ----
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 10 -tune animation -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a 320k -af apad -t $END -movflags +faststart out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 15 -tune animation -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -profile:v high -c:a aac -b:a 256k -af apad -t $END -movflags +faststart out/${N}_share.mp4
rm -f out/video_v.mov out/_pre.wav
for f in out/${N}_*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration,size:stream=nb_frames -of csv=p=0 "$f" | tr '\n' ' ')"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
