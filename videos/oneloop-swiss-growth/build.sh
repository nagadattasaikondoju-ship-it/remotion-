#!/bin/sh
# One Loop: The Growth Path. One-command rebuild (Swiss Motion Graphics, Lemo-Opuscar library in skill mode).
# Needs: the library (bash tools from the repo notes) with its npm/.venv and the vcsl + freepats sample packs,
# the SFX tooling (tools/setup_sfx.sh, real-sfx config/index), ffmpeg. Sound: Openverse → Real SFX → Earshot.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../.." && pwd)
LIB=${LIB:-$REPO/tools/lemo-opuscar}; export LIB
export PLAYWRIGHT_CHROME=${PLAYWRIGHT_CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" "$HERE/out/stems"
cd "$LIB"
node core/render/events.mjs "$HERE" --size 1080x1920
node core/render/readcheck.mjs "$HERE" --size 1080x1920                    # every text holds long enough to read
node core/render/video.mjs "$HERE" --fps 24 --workers 4 --size 1080x1920 --out "$HERE/out/video.mp4"
LIB=$LIB .venv/bin/python "$HERE/music/score.py"                             # → out/music.wav
ffmpeg -nostdin -v error -y -i "$HERE/out/video.mp4" -i "$HERE/out/music.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest "$HERE/out/film_music.mp4"
# Real SFX: the film's own cue list → Earshot-picked real recordings (sfx_map.json), placed on the frame
cd "$SFX"
python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/film_music.mp4" --out "$W/work/cues.json" \
  --ui library --map "$HERE/sfx_map.json" --one-source thump,key,paper,land
python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/swiss_sfx.mp4" --base-audio "$HERE/out/music.wav" --sfx-trim-db -4
python3 -I scripts/critique.py "$W/result/swiss_sfx_resolved_cues.json" "$W/result/swiss_sfx_sfx_track.wav" | head -16
cp "$W/result/swiss_sfx_sfx_track_in_mix_level.wav" "$HERE/out/stems/sfx.wav"; cp "$W/result/swiss_sfx_base.wav" "$HERE/out/stems/music.wav"
cp "$W/result/swiss_sfx_resolved_cues.json" "$W/result/swiss_sfx_cue_report.md" "$HERE/out/stems/"
"$LIB/.venv/bin/python" "$HERE/mix.py"
# Master: two-pass loudnorm −14 LUFS / TP −1.2 (done here because the library's mux.sh needs ffmpeg 7+)
J=$(ffmpeg -nostdin -hide_banner -i "$HERE/out/mix.wav" -af loudnorm=I=-14:TP=-1.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -nostdin -v error -y -i "$HERE/out/mix.wav" -af "loudnorm=I=-14:TP=-1.2:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad=whole_dur=30,atrim=0:30" -c:a pcm_s24le "$HERE/out/mix_master.wav"
V="-map 0:v -map 1:a -r 24 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -shortest"
ffmpeg -nostdin -v error -y -i "$HERE/out/video.mp4" -i "$HERE/out/mix_master.wav" $V -c:v libx264 -preset slow -crf 6 -c:a aac -b:a 320k "$HERE/OneLoop_GrowthPath_1080x1920_24fps_MASTER.mp4"
ffmpeg -nostdin -v error -y -i "$HERE/out/video.mp4" -i "$HERE/out/mix_master.wav" $V -c:v libx264 -preset slow -crf 16 -maxrate 10M -bufsize 20M -c:a aac -b:a 256k "$HERE/oneloop-growth-path.mp4"
ffmpeg -nostdin -v error -y -ss 28.5 -i "$HERE/oneloop-growth-path.mp4" -frames:v 1 -q:v 2 "$HERE/poster.jpg"
ffmpeg -nostdin -hide_banner -i "$HERE/oneloop-growth-path.mp4" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
(cd / && earshot critique "$HERE/oneloop-growth-path.mp4" | head -4) || true                  # Earshot QA
