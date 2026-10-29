#!/usr/bin/env bash
# base.mp4 (footage) + out/ov (captions/graphics, transparent PNGs) + sound (VO, SFX, optional music bed)
# → 1080×1920 60 fps master (high bitrate) and a share copy.
#   ./assemble.sh                                   VO + SFX
#   MUSIC=path/to/track.mp3 MUSIC_IN=0 ./assemble.sh  + music bed (MUSIC_IN = seconds into the track to start)
set -euo pipefail
cd "$(dirname "$0")"
VO=${VO:-/root/.claude/uploads/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/80738f9a-WhatsApp_Audio_2026-10-28_at_11.49.06_PM.m4a}
NAME=OneLoop_Story_1080x1920_60fps
# VO: one continuous take, raw 1.05 s → video 0.00 (video = raw − 1.05), padded to the 34.5 s cut.
# Voice-note repair chain: rumble cut · warmth (+3 dB low shelf) · de-box (−3 dB at 380 Hz) · presence (+2.5 dB at 3 kHz)
# · air (+2 dB shelf, and harmonic exciter above 7 kHz to rebuild what WhatsApp cut at ~15 kHz) · de-ess · 3:1 compression
# · a −62 dBFS pink room-tone bed so the voice-note gate doesn't leave dead-silent holes between phrases.
ffmpeg -nostdin -v error -y -i "$VO" -f lavfi -i "anoisesrc=color=pink:amplitude=0.0008:sample_rate=48000:duration=40" -filter_complex "
  [0:a]aresample=48000,pan=mono|c0=c0,atrim=1.05,asetpts=PTS-STARTPTS,highpass=f=75,
       lowshelf=f=150:g=3,equalizer=f=380:t=q:w=1.2:g=-3,equalizer=f=3000:t=q:w=1.0:g=2.5,highshelf=f=9000:g=2,
       aexciter=amount=0.9:drive=4:freq=7000:ceil=16500,deesser=i=0.35:m=0.5:f=0.5,
       acompressor=threshold=-24dB:ratio=3:attack=5:release=90:makeup=4,afade=t=in:d=0.01[v];
  [1:a]lowpass=f=6000,pan=mono|c0=c0[n];
  [v][n]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false,apad=whole_dur=34.5,atrim=0:34.5[o]" -map "[o]" -c:a pcm_s24le out/vo_raw.wav
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
