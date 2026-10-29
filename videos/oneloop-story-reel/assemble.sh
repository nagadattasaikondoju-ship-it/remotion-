#!/usr/bin/env bash
# base.mp4 (footage) + out/ov (captions/graphics, transparent PNGs) + sound (VO, SFX, optional music bed)
# → 1080×1920 60 fps master (high bitrate) and a share copy.
#   ./assemble.sh                                   VO + SFX
#   MUSIC=path/to/track.mp3 MUSIC_IN=0 ./assemble.sh  + music bed (MUSIC_IN = seconds into the track to start)
set -euo pipefail
cd "$(dirname "$0")"
VO=${VO:-/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/b6c70251-WhatsApp_Audio_2026-10-28_at_11.49.06_PM.mp4}
NAME=OneLoop_Story_1080x1920_60fps
# VO: one continuous take, raw 1.05 s → video 0.00 (video = raw − 1.05), padded to the 34.5 s cut
ffmpeg -nostdin -v error -y -i "$VO" -af "aresample=48000,pan=mono|c0=c0,highpass=f=80,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,atrim=1.05,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,apad=whole_dur=34.5,atrim=0:34.5" -c:a pcm_s24le out/vo_raw.wav
python3 sfx.py
# two-pass loudnorm to −14 LUFS / −1.5 dBTP (linear, so the voice/SFX balance is kept)
J=$(ffmpeg -nostdin -hide_banner -i out/mix_raw.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
m() { echo "$J" | python3 -c "import json,sys; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -nostdin -v error -y -i out/mix_raw.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=$(m input_i):measured_TP=$(m input_tp):measured_LRA=$(m input_lra):measured_thresh=$(m input_thresh):offset=$(m target_offset):linear=true,aresample=48000" -c:a pcm_s24le out/audio.wav
ffmpeg -nostdin -v error -y -i out/base.mp4 -framerate 60 -i out/ov/f_%05d.png -i out/audio.wav \
  -filter_complex "[0:v][1:v]overlay=format=auto,format=yuv420p[v]" -map "[v]" -map 2:a -frames:v 2070 \
  -c:v libx264 -preset slow -crf 8 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 320k -movflags +faststart out/${NAME}_MASTER.mp4
ffmpeg -nostdin -v error -y -i out/${NAME}_MASTER.mp4 -c:v libx264 -preset slow -crf 19 -maxrate 12M -bufsize 24M -pix_fmt yuv420p \
  -c:a aac -b:a 256k -movflags +faststart out/${NAME}_share.mp4
for f in out/${NAME}_MASTER.mp4 out/${NAME}_share.mp4; do
  ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames,r_frame_rate,width,height:format=duration,bit_rate,size -of csv=p=0 "$f"; done
ffmpeg -nostdin -hide_banner -i out/${NAME}_MASTER.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+I:|Peak:"
