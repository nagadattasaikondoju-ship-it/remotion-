# "10 things Claude should add to your website" — fix pass

Source: `WhatsApp_Video_2026-10-14_at_1.58.07_PM.mp4` (1080×1920, 30 fps, 28.3 s). Output: `renders/Claude_Website_Reel_HD_1080x1920.mp4` (27.2 s).

1. **Arrow removed (24.0 s → end).** `scripts/remove_arrow.py` is the tool.
   - It finds the yellow ↓ graphic frame by frame, only from 23.7 s on and only an arrow-sized shape at x 840–960.
   - It paints the wall back in with OpenCV inpainting; 96 frames were touched, nothing else.
   - The yellow words in the earlier UI captions are left untouched.
2. **Audio cleaned.**
   - DeepFilterNet3 at full suppression removes the horns and background noise.
   - Clarity chain: high-pass 80 Hz, small cut at 200 Hz, presence lift at 3.5 kHz and air at 9 kHz, de-esser, gentle compression.
   - Mastered to −14.5 LUFS with peaks under −1 dBTP.
3. **Ending trimmed.** The video now ends at 27.2 s, just after "…delete from your website first." The stop-recording ("End Video") part is cut, with a 0.15 s audio fade.
4. **HD finish.**
   - Light temporal denoise (cleans the compression blotches on skin and wall).
   - Contrast-adaptive sharpening and +3 % contrast / +5 % saturation.
   - H.264 High at CRF 14 (≈18 Mbps vs the original 7.6 Mbps), 1080×1920 at 30 fps.
