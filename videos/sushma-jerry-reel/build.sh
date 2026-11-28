#!/bin/bash
# Dr. Sri Sushma Multispeciality Dental Clinic: the Jerry dental reel with Dr. Sri Sushma's logo as the end card.
# Takes ONE loop from the user's screen recording (it plays twice), cleans the recording artefacts, upscales to
# 1080x1920 and replaces the end card (originally another clinic's logo) with Dr. Sri Sushma's logo, popping in.
#   REF  = the user's screen recording (460x774, 30 fps). One loop = frames 12..236 (0.4–7.9 s):
#          cartoon frames 12..192 (6.03 s), white logo card frames 193..236 (1.47 s, silent).
#   LOGO = the clinic's logo: a PDF (flat black version) or an image (the blue 3D version the user chose, 1056x992,
#          background #FEFFFF). CARD = end-card colour; default = the logo image's own background, so no edge shows.
set -euo pipefail
cd "$(dirname "$0")"
REF=${REF:?path to the reference screen recording}
LOGO=${LOGO:?path to the logo (PDF or image)}
CARD=${CARD:-white}
LOGO_W=${LOGO_W:-870}   # px at full size; the blue logo's badge is ~69 % of its image width, so the badge is ~600 px wide
mkdir -p out
case "$LOGO" in
  *.pdf|*.PDF) pdftocairo -png -r 144 -singlefile "$LOGO" out/logo; CARD=${CARD_PDF:-white}; LOGO_W=${LOGO_W_PDF:-780} ;;  # 2160x2160 on solid white
  *) ffmpeg -v error -y -i "$LOGO" -frames:v 1 -pix_fmt rgb24 out/logo.png ;;
esac
# 1) cartoon: crop off the recording's side bars (content = columns 12..447), undo the player's bottom
#    darkening gradient (multiplicative ramp, 1.0 at row 669 down to 0.733 at row 773, measured on the white card),
#    remove the "0:0x / 0:07" timer with delogo, then upscale to 1080x1920 with a light sharpen.
G="if(gt(Y\,669)\,1-0.267*(Y-669)/104\,1)"
ffmpeg -v error -y -i "$REF" -filter_complex "
  [0:v]trim=start_frame=12:end_frame=193,setpts=PTS-STARTPTS,crop=436:774:12:0,format=gbrp,
       geq=r='min(255\,r(X\,Y)/$G)':g='min(255\,g(X\,Y)/$G)':b='min(255\,b(X\,Y)/$G)',format=yuv420p,
       delogo=x=3:y=733:w=118:h=34,
       scale=1082:1920:flags=lanczos,crop=1080:1920,unsharp=5:5:0.55:5:5:0,setsar=1,fps=30[v]" \
  -map "[v]" -c:v libx264 -preset slow -crf 10 out/a_cartoon.mp4
# 2) end card: white, 44 frames (1.47 s, same as the original). The logo pops in (ease-out-back over 0.3 s,
#    from 30 % with a small overshoot), then keeps growing slowly (+6 %) like the original card's logo.
P="min(1\,n/9)"; E="(1+2.70158*pow($P-1\,3)+1.70158*pow($P-1\,2))"; Wd="trunc($LOGO_W*(0.3+0.7*$E)*(1+0.06*n/44)/2)*2"
ffmpeg -v error -y -f lavfi -i "color=c=$CARD:s=1080x1920:r=30:d=1.4667" -loop 1 -framerate 30 -i out/logo.png -filter_complex "
  [1:v]format=rgba,geq=r='if(gte(r(X\,Y)\,250)\,255\,r(X\,Y))':g='if(gte(g(X\,Y)\,250)\,255\,g(X\,Y))':b='if(gte(b(X\,Y)\,250)\,255\,b(X\,Y))':a='255*clip(min(min(X\,W-1-X)\,min(Y\,H-1-Y))/90\,0\,1)',scale=w='$Wd':h=-2:eval=frame:flags=lanczos[l];
  [0:v]format=rgb24[bg];[bg][l]overlay=x=(W-w)/2:y=(H-h)/2:shortest=1:eval=frame:format=rgb,format=yuv420p[v]" \
  -map "[v]" -frames:v 44 -c:v libx264 -preset slow -crf 10 out/b_card.mp4
# 3) join + the original audio of the same loop (0.4–7.9 s; the card part is silent in the original too)
printf "file 'a_cartoon.mp4'\nfile 'b_card.mp4'\n" > out/list.txt
ffmpeg -v error -y -f concat -safe 0 -i out/list.txt -c copy out/video.mp4
mk() { ffmpeg -v error -y -i out/video.mp4 -ss 0.4 -t 7.5 -i "$REF" -map 0:v -map 1:a -c:v libx264 -preset slow -crf $1 \
  -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -af "afade=t=out:st=7.45:d=0.05" -t 7.5 -movflags +faststart "$2"; }
mk 12 out/DrSriSushma_JerryReel_1080x1920_30fps_MASTER.mp4
mk 17 out/DrSriSushma_JerryReel_1080x1920_30fps_share.mp4
rm -f out/a_cartoon.mp4 out/b_card.mp4 out/video.mp4 out/list.txt
ls -la out/*.mp4
