#!/usr/bin/env bash
# Background plates for brand.html, cut from the upscaled reference (REF_UP).
#   plate_satin.png (14.0 s) and plate_scene40.png (40.6 s, clean before the presenter enters): reference framing, for segments A and G
#   plate_satin_fix.png and plate_family.png (32.5 s): framing-fixed (crop 1050x1867, scaled to 1080x1920), for the full-frame segments D and E
set -euo pipefail; cd "$(dirname "$0")"; REF_UP=${REF_UP:?upscaled reference}
FIXV="crop=1050:1867:0:0,scale=1080:1920:flags=lanczos"
ffmpeg -nostdin -v error -y -ss 14.0 -i "$REF_UP" -frames:v 1 img/plate_satin.png
ffmpeg -nostdin -v error -y -ss 40.6 -i "$REF_UP" -frames:v 1 img/plate_scene40.png
ffmpeg -nostdin -v error -y -ss 14.0 -i "$REF_UP" -frames:v 1 -vf "$FIXV" img/plate_satin_fix.png
ffmpeg -nostdin -v error -y -ss 32.5 -i "$REF_UP" -frames:v 1 -vf "$FIXV" img/plate_family.png
