# Three Angle Method reel ("Meta reads your creative, not your targeting")

**Format:** 48.9 s, 2160×3840 (4K vertical), 30 fps.
**Structure (the user's brief):**
1. The host full screen: "Guys, watch this first."
2. A split screen: the sample clip on top with its own audio, the host below, paused, silent and listening.
3. The host full screen again for the rest, ending on "DM us META".

The reference analysis and the edit blueprint are in `ANALYSIS.md`. The structure is in `PLAN.md`.

## Sources (not in git)
- **Host:** `VID_20261106_234838148.mp4`, from Drive (file id `16ojs8zXG3ZlTDH-pOoeM3CNO_GCTCzut`).
- **Sample:** `vid_sample (1).mp4`, a user upload.
  - A stranger's username in an Instagram "liked your reel" pop-up (frames 56–95) is blurred.
  - Her burned-in title, captions and screen-recording cursor are cropped or painted out.
- **Reference:** `20261107-0718-48.mp4`, a screen recording of a podcast-host reel.

## Pipeline
1. **Cut list:** `python3 tools/make_edl.py host48.wav whisper.json > edl.json`.
   - Cuts pauses only where the audio really drops, which gives 21 clips.
2. **Timeline:** `python3 tools/timeline.py whisper.json sample_whisper.json` → `timeline.json`.
   - Every word placed at its time in the cut.
   - Fixes Whisper's "Metastell" → "Meta still" and "DMS" → "DM us".
3. **Picture:** `python3 tools/base.py HOST SAMPLE out/base4k.mp4`.
   - Grade at native resolution, then one Lanczos resample per frame straight to 4K. That one resample covers the punch-ins, the split-screen slides and the plate moves in `plate.json`.
   - `--test t1,t2 out.jpg` gives a preview sheet.
4. **Voice:** `PYTHONPATH=<dfnlib> python3 tools/denoise.py out/host48.wav out/voice_dn_full.wav` (DeepFilterNet3, on the whole take).
5. **Graphics:** `index.html` holds the captions and motion graphics, a pure `seek(t)`.
   - `node render.mjs stills t…` gives review frames.
   - `node render.mjs frames 2` streams 2160×3840 straight into `out/overlay4k.mkv` (lossless FFV1 with alpha).
   - Chrome's CDP screenshot needs `clip.scale: 2`; it ignores the page's deviceScaleFactor.
6. **Review:** `python3 tools/preview.py HOST SAMPLE out.jpg t…` composites the stills over the real base frames.
7. **Sound:**
   - `python3 tools/make_cues.py` → `sfx_cues.json`: 38 cues from the word times.
   - `sfx_map.json` picks the real recordings (Openverse CC0 library).
8. **Assembly:** `bash assemble.sh`.
   - The 4K composite (CRF 12) and the voice on the timeline.
   - Her clip's audio, loudness-matched to his.
   - Real SFX placed by Real SFX, then the critique.
   - Two-pass loudnorm to −14 LUFS.
   - Outputs: `ThreeAngleMethod_2160x3840_30fps_{MASTER,share}.mp4`.

## Design
- **Type:**
  - Geist (captions, UI), Geist Mono (labels), Instrument Serif italic (emotion words).
  - Colours: white and near-black, with mint #3DDBB0 as the one accent and red only for negatives (targeting, weakest).
- **Through-line object:** one UI card that morphs through every idea:
  1. audience panel (a cursor drags the age slider and clicks "Women")
  2. struck "your targeting" pill
  3. ad creative being scanned
  4. 01 PROBLEM / 02 PROOF / 03 OFFER angle card
  5. budget chart (cut the weakest, fund the winner)
  6. DM composer (types META, sends)
- **The reference's signature move, used twice:** his frame shrinks into a tilted rounded card on near-black, for "the three angle method" and "same product, three different ads".
- **Grade:**
  - Warm-neutral white balance, soft highlight knee, gentle S-curve, light local contrast, +6 % chroma, 9 % vignette.
  - Following the user's standing note: no background blur and no background dimming. Gradient scrims sit only behind type.

## Proof scene (39.0–45.3 s, added after the first cut)
- **Where:** on "We tested this on different brands… for Meta and Google that bring you leads and sales". The claim gets its proof right there, and each result lands on its word: RMC's leads on "leads", the e-commerce ROAS on "sales".
- **What:** four real Google Ads accounts from the user's screenshots, rebuilt as vector UI (Google's tile colours, real values only). A cursor clicks the first account, the camera dives into each hero number as it counts up, then pulls back to the wall of all four.
- **Verified:** RMC Plumbing and Bamboo Spa match One Loop's *Client Success Stories* PDF exactly.
- **Unnamed:** the Q2 2025 e-commerce account (8.43×; its figures fit Bikers Wear AU's profile) and the March 2026 India account are labelled by what their screenshots show. The user should confirm before either is named.

## Notes
- No numbers or results are claimed on screen beyond what's spoken. The budget chart shows relative bars with no values.
- The "Free delivery" offer card is an illustrative mock ad, not a client's offer.
- No names or logos; the host isn't named on screen.
- The 4K output is upscaled from 1080p phone footage: one Lanczos pass plus thresholded sharpening. The type and graphics are native 4K.
