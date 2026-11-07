#!/usr/bin/env bash
# Three Angle Method reel: 4K base (tools/base.py) + 4K caption/graphics overlay (render.mjs frames 2)
# + DeepFilterNet-cleaned voice cut on the same timeline + her clip's own audio under the split
# + real SFX (Openverse → Real SFX → Earshot), two-pass loudnorm −14 LUFS. No music. 2160×3840, 30 fps.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); cd "$HERE"
N=ThreeAngleMethod_2160x3840_30fps
SAMPLE="${SAMPLE:-/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/720a0897-vid_sample__1.mp4}"
END=$(python3 -I -c "import json; print(json.load(open('timeline.json'))['END'])")
export REAL_SFX_CONFIG=$REPO/tools/real-sfx.config.json REAL_SFX_INDEX=$REPO/tools/real-sfx.index.json
for f in out/base4k.mp4 out/overlay4k.mkv out/voice_dn_full.wav; do [ -f "$f" ] || { echo "missing $f (see README)"; exit 1; }; done

# ---- picture: base + overlay, one 4K master encode (skipped when out/video4k.mp4 is newer than both; REDO_VIDEO=1 forces) ----
if [ -n "${REDO_VIDEO:-}" ] || [ ! -f out/video4k.mp4 ] || [ out/video4k.mp4 -ot out/overlay4k.mkv ] || [ out/video4k.mp4 -ot out/base4k.mp4 ]; then
ffmpeg -nostdin -v error -y -i out/base4k.mp4 -i out/overlay4k.mkv -filter_complex "
  [0:v]settb=1/30,setpts=N,format=gbrp[b];[1:v]settb=1/30,setpts=N,format=gbrap[o];
  [b][o]overlay=format=gbrp:shortest=1,format=yuv420p[v]" -map "[v]" \
  -c:v libx264 -preset medium -crf 12 -tune film -profile:v high -level 5.2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -r 30 -movflags +faststart out/video4k.mp4
ffmpeg -nostdin -v error -y -i out/video4k.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -preset veryfast -crf 20 out/proxy1080.mp4
fi

# ---- dialogue: his voice on the timeline (silent under the split), her clip's audio under the split ----
python3 -I - <<'PY'
import json, subprocess
tl = json.load(open("timeline.json")); e = json.load(open("edl.json"))
parts = [(e["intro"][0], e["intro"][1])] + [(s["src0"], s["src0"] + s["t1"] - s["t0"]) for s in tl["segs"] if s["kind"] == "main"]
gap = tl["T_MAIN"] - tl["T_SPLIT"]
fc = []
for i, (a, b) in enumerate(parts):
    fc.append(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={b - a - 0.02:.4f}:d=0.02[a{i}]")
fc.append(f"anullsrc=r=48000:cl=mono,atrim=0:{gap:.4f}[gap]")
order = "[a0][gap]" + "".join(f"[a{i}]" for i in range(1, len(parts)))
fc.append(f"{order}concat=n={len(parts) + 1}:v=0:a=1[a]")
subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", "out/voice_dn_full.wav", "-filter_complex", ";".join(fc),
                "-map", "[a]", "-ar", "48000", "-ac", "1", "out/voice_cut.wav"], check=True)
PY
ffmpeg -nostdin -v error -y -i out/voice_cut.wav -af "highpass=f=85,equalizer=f=300:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1.0:g=2.5,equalizer=f=10000:t=q:w=0.8:g=1.5,deesser=i=0.35,acompressor=threshold=-24dB:ratio=3:attack=6:release=120:makeup=4,alimiter=limit=0.89,apad=whole_dur=$END" -ac 2 -ar 48000 out/voice.wav
# her clip: clean, matched to his loudness (measured over his speech), placed at the split with short fades
VL=$(ffmpeg -nostdin -hide_banner -i out/voice.wav -af "atrim=13:47,ebur128" -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}')
TS=$(python3 -I -c "import json; print(json.load(open('timeline.json'))['T_SPLIT'])")
ffmpeg -nostdin -v error -y -i "$SAMPLE" -vn -af "highpass=f=90,afftdn=nr=10:nf=-45,acompressor=threshold=-26dB:ratio=2.5:attack=8:release=150:makeup=3,loudnorm=I=${VL}:TP=-3:LRA=9,afade=t=in:d=0.04,afade=t=out:st=10.68:d=0.08,adelay=$(python3 -I -c "print(int(round($TS*1000)))")|$(python3 -I -c "print(int(round($TS*1000)))"),apad=whole_dur=$END" -ac 2 -ar 48000 out/sample.wav
ffmpeg -nostdin -v error -y -i out/voice.wav -i out/sample.wav -filter_complex "amix=inputs=2:normalize=0:duration=longest,atrim=0:$END" -c:a pcm_s24le out/dialog.wav
echo "voice loudness (speech) $VL LUFS"

# ---- SFX: Real SFX places the cue sheet's real recordings on the frame; critique checks sync/levels ----
ffmpeg -nostdin -v error -y -i out/proxy1080.mp4 -i out/dialog.wav -map 0:v -map 1:a -c:v copy -c:a pcm_s16le -shortest out/video_v.mov
SFX=$REPO/.claude/skills/real-sfx; W=$HERE/out/sfxwork; mkdir -p "$W/work" "$W/result" out/stems
(cd "$SFX" && python3 -I scripts/from_cues.py "$HERE/sfx_cues.json" --video "$HERE/out/video_v.mov" --out "$W/work/cues.json" \
   --ui library --map "$HERE/sfx_map.json" \
 && python3 -I scripts/mix.py "$W/work/cues.json" --out "$W/result/ta_sfx.mp4" --base-audio "$HERE/out/dialog.wav" --sfx-trim-db -3)
(cd "$SFX" && python3 -I scripts/critique.py "$W/result/ta_sfx_resolved_cues.json" "$W/result/ta_sfx_sfx_track.wav" > "$W/result/critique.txt") || true; head -18 "$W/result/critique.txt"
cp "$W/result/ta_sfx_sfx_track.wav" out/stems/sfx.wav; cp out/voice.wav out/stems/voice.wav; cp out/sample.wav out/stems/her_clip.wav
cp "$W/result/ta_sfx_resolved_cues.json" out/stems/ 2>/dev/null || true
ffmpeg -nostdin -v error -y -i out/dialog.wav -i out/stems/sfx.wav -filter_complex "amix=inputs=2:normalize=0:duration=first,atrim=0:$END" -c:a pcm_f32le out/_pre.wav
J=$(ffmpeg -nostdin -hide_banner -i out/_pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -I -c "import json,sys; print(json.load(sys.stdin)['$1'])" 2>/dev/null; }
ffmpeg -nostdin -v error -y -i out/_pre.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000,apad=whole_dur=$END,atrim=0:$END" -c:a pcm_s24le out/mix_master.wav

# ---- deliverables: 4K master (picture copied from the CRF 12 encode) + 4K share copy ----
ffmpeg -nostdin -v error -y -i out/video4k.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -movflags +faststart -shortest out/${N}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/video4k.mp4 -i out/mix_master.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 17 -maxrate 40M -bufsize 80M -profile:v high -level 5.2 -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 256k -movflags +faststart -shortest out/${N}_share.mp4
for f in out/${N}_*.mp4; do echo "$f"; ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,width,height:format=duration,size,bit_rate -of csv=p=0 "$f"; done
ffmpeg -nostdin -hide_banner -i out/${N}_share.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
rm -f out/_pre.wav out/video_v.mov
