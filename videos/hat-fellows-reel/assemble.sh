#!/usr/bin/env bash
# HAT Fellows reel: graded talking head (tools/grade.py) + caption/card overlay (render.mjs) + voice/music/SFX → 44.6 s, 1080×1920, 30 fps.
# Sound: Openverse → Real SFX (sfx_cues.json + sfx_map.json) → Earshot QA. Original music bed: music/score.py.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
LIB=${LIB:-$REPO/tools/lemo-opuscar}
N=HATFellows_EarlyAccess_1080x1920_30fps; END=44.6
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
[ -f out/graded.mov ] || { echo "run tools/grade.py first (see README)"; exit 1; }
[ -f out/ov/f_01337.png ] || node render.mjs frames
# opaque card frames come out of Chrome as RGB; a mid-stream RGB/RGBA switch resets the overlay's timeline, so make all RGBA
(cd out/ov && identify -format "%f %[channels]\n" f_*.png | awk '$2!="srgba"{print $1}' | xargs -r -P 4 -n 40 mogrify -define png:color-type=6 -define png:compression-level=1)
[ -f out/music.wav ] || (cd "$LIB" && LIB=$LIB .venv/bin/python "$HERE/music/score.py")

# picture: graded face (held under the end card) + overlay
ffmpeg -nostdin -v error -y -i out/graded.mov -framerate 30 -i out/ov/f_%05d.png -filter_complex "
  [0:v]settb=1/30,setpts=N,tpad=stop_mode=clone:stop_duration=3,trim=duration=$END,format=rgba[b];[1:v]settb=1/30,setpts=N[o];
  [b][o]overlay=format=auto:shortest=1,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset slow -crf 8 -tune film -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -movflags +faststart out/video.mp4

# voice: DeepFilterNet3 noise reduction on the whole take (tools/denoise.py → out/voice_dn_full.wav), then cut on the EDL,
# then a clarity chain: rumble cut, de-box at 300 Hz, presence at 3.5 kHz, air, de-ess, gentle levelling
[ -f out/voice_dn_full.wav ] || { echo "run tools/denoise.py first (see README)"; exit 1; }
python3 -I - <<'PY'
import json, subprocess
e = json.load(open("edl.json"))["clips"]
fc = ";".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b-a-0.02:.3f}:d=0.02[a{i}]" for i, (a, b, _) in enumerate(e))
fc += ";" + "".join(f"[a{i}]" for i in range(len(e))) + f"concat=n={len(e)}:v=0:a=1[a]"
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "out/voice_dn_full.wav", "-filter_complex", fc, "-map", "[a]", "-ar", "48000", "out/voice_dn_cut.wav"], check=True)
PY
ffmpeg -nostdin -v error -y -i out/voice_dn_cut.wav -af "highpass=f=85,equalizer=f=300:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=10000:t=q:w=0.8:g=1.5,deesser=i=0.35,acompressor=threshold=-24dB:ratio=3:attack=6:release=120:makeup=4,alimiter=limit=0.89,apad=whole_dur=$END" -ac 2 -ar 48000 out/voice.wav
# music −19 LU under the voice (measured), then the dialogue premix that the SFX are placed against
lufs() { ffmpeg -nostdin -hide_banner -i "$1" -af ebur128 -f null - 2>&1 | awk '/I:/{v=$2} END{print v}'; }
VL=$(lufs out/voice.wav); ML=$(lufs out/music.wav); MG=$(python3 -c "print(round(($VL-19)-($ML),2))")
echo "voice $VL LUFS, music $ML LUFS → music gain $MG dB"
ffmpeg -nostdin -v error -y -i out/voice.wav -i out/music.wav -filter_complex "[1:a]volume=${MG}dB[m];[0:a][m]amix=inputs=2:normalize=0:duration=first" -c:a pcm_f32le out/dialogue_music.wav
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/dialogue_music.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_dm.mov

# Real SFX: the edit's own cue list → Earshot-picked real recordings, placed on the frame
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_dm.mov" --out "$W/work/cues.json" \
   --ui library --map "$HERE/sfx_map.json" --kind pop=slices:10 --one-source pop \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/hat_sfx.mp4" --base-audio "$HERE/out/dialogue_music.wav" --sfx-trim-db -2)
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/hat_sfx_resolved_cues.json" "$W/result/hat_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; head -16 "$W/result/critique.txt"
cp "$W/result/hat_sfx_sfx_track.wav" out/stems/sfx.wav; cp out/voice.wav out/stems/voice.wav
ffmpeg -nostdin -v error -y -i out/music.wav -af "volume=${MG}dB" out/stems/music.wav
cp "$W/result/hat_sfx_resolved_cues.json" "$W/result/hat_sfx_cue_report.md" out/stems/ 2>/dev/null || true

mixdown() {  # $1 = output, rest = stems; two-pass loudnorm −14 LUFS / TP −1.2 (ffmpeg 6.1)
  local o=$1; shift; local ins=() k=0; for s in "$@"; do ins+=(-i "$s"); k=$((k+1)); done
  ffmpeg -nostdin -v error -y "${ins[@]}" -filter_complex "amix=inputs=$k:normalize=0:duration=longest,atrim=0:$END" -c:a pcm_f32le out/_pre.wav
  local J; J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
  m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
  ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad=whole_dur=$END,atrim=0:$END" -c:a pcm_s24le "$o"
}
ffmpeg -nostdin -v error -y -i out/stems/music.wav -af "volume=-4dB" out/stems/music_low.wav
mixdown out/mix_master.wav out/stems/voice.wav out/stems/sfx.wav
mixdown out/mix_withmusic.wav out/stems/voice.wav out/stems/music_low.wav out/stems/sfx.wav
V="-map 0:v -map 1:a -c:v libx264 -preset slow -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -movflags +faststart -shortest"
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav $V -crf 8 -tune film -c:a aac -b:a 320k out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_master.wav $V -crf 15 -maxrate 16M -bufsize 32M -c:a aac -b:a 256k out/${N}_share.mp4
ffmpeg -nostdin -v error -y -i out/video.mp4 -i out/mix_withmusic.wav $V -crf 17 -maxrate 12M -bufsize 24M -c:a aac -b:a 256k out/${N}_share_with-soft-music.mp4
for f in out/${N}_*.mp4; do echo "$f"; ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,width,height:format=duration,size -of csv=p=0 "$f"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
ffmpeg -nostdin -v error -y -ss 12.5 -i out/${N}_share.mp4 -frames:v 1 -q:v 2 out/poster.jpg
