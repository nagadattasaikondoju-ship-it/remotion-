# One Loop: "We don't build demos" (skit + Tarun)

55 s · 1080×1920 · 30 fps. The skit ("the demo works, deployment fails, change the developer") hands over on a record-scratch freeze to Tarun's explanation: demo vs real world → three proofs → "We don't build demos" → follow → **Comment BUILD**.

Built from Tarun's editing notes (cold open, freeze + scratch handoff, playful → documentary music, fast keyword cuts, one steady shot, a full-screen flash per proof, word-by-word slam, a 2 s CTA hold, captions throughout) and the three style references (see `ANALYSIS.md`).

## Edit (`timeline.py`, one table drives picture, dialogue, captions and sound)

| Time | Shot | What happens |
|---|---|---|
| 0.0 | cold open | "Please do something!", a quick punch-in on the dev, red "Deployment failed" toast, glitch |
| 1.2 | black | "He had no idea / what was coming." (serif italic), low hit |
| 2.5–16.2 | the skit | Tightened from 26 s to 13.7 s: pauses removed, jump cuts hidden by small zoom changes, crash punch-in on the dev's face, playful pizzicato bed |
| 16.2 | freeze | Record scratch + tape-stop, drained colour, "PAUSED", "The demo worked. / Deployment didn't.", Tarun's "You see," starts over the frozen frame (J-cut) |
| 17.6 | Tarun | "…software that dies": an ECG trace beeps three times and flatlines on "dies" |
| 20.4 | split screen | Top: the DEMO panel (clean data ✓, one user ✓, Wi-Fi perfect ✓, ticking on each word). Bottom: Tarun. The panel glitches apart. |
| 24.1 | b-roll | Night traffic (One Loop Drive MVI_0640) + "THE REAL WORLD walks in." |
| 25.9 / 26.9 / 28.1 | full-screen MG | Users 1 → 500 · messy-data table · phone losing signal → "Request timed out", "middle of nowhere" (Tarun in a circle) |
| 30.6 | one steady shot | "we build for the **wild** from day one", a One Loop badge on "OneLoop" |
| 36.9 / 38.7 / 41.0 | proofs 1–3 | Nirvaha (real Google Play listing, real store screenshots) · logistics (illustrated map, see open items) · LN Sports Arena (real logo, booking grid). Impact on each, Tarun in a circle. |
| 44.8 | copper slam | "WE DON'T BUILD **DEMOS.**" (struck through) → black "WE BUILD SOFTWARE THAT ACTUALLY **WORKS.**", music drops out |
| 47.5 | logo | The traced One Loop logo lands on "OneLoop" with a bass hit; "Follow @oneloop.in" |
| 50.8–55.1 | CTA | "Comment **BUILD**", a comment box types B-U-I-L-D and posts, "so that we build yours.", 2 s hold |

## Look
- **Captions:** white Poppins 800, word by word with a small pop, the punch word in One Loop copper, a heavy shadow and stroke for contrast.
  - Placed below faces and the mic, and beside the circle during full-screen graphics.
  - The two unclear skit lines are left out.
- **Grade:** warm and natural for the skit; cooler, documentary-style for Tarun (per his notes).
- **Upscaling:** the sources are WhatsApp-compressed 480×854, so they're denoised and upscaled with sharpening.

## Sound
- **Dialogue** (`clean/*.wav`, made with ffmpeg):
  - high-pass at 85 Hz, FFT denoise, EQ (−2 dB at 250 Hz, +2.5 dB at 3.2 kHz), de-ess, compression;
  - each take level-matched.
  - Measured: no song was detectable in the skit or Tarun's takes (no beat grid, AudioSet music 0.12). The phone had already gated the background, so the gaps are near-silent.
- **Music** (`audio_build.py`, composed in code because Freesound and Wikimedia downloads are refused from this session):
  - playful plucked strings, 116 BPM in C, under the skit, tape-stopped at the freeze;
  - documentary piano and pad, 72 BPM, Am–F–C–G, under Tarun, with a soft kick pulse under the proofs;
  - silence for the slam, then a resolving C chord for the logo and the CTA.
  - It's ducked by the voice, about 20 dB under him.
- **SFX** (`sfx_cues.py` → Real SFX, 40 cues, all on their frames):
  - real CC0 library sounds (whooshes, impacts, ticks, typewriter keys, chime, pops);
  - plus three sounds made with `earshot forge`, because no recording was reachable: the record scratch (ranked "strong"), the glitch burst and the monitor beep.
  - The master is −14 LUFS.

## Build
```bash
bash assemble.sh                 # timeline → base_render.py (picture) → render.mjs video (overlay) → sound → deliverables
SKIP_PICTURE=1 bash assemble.sh  # sound + deliverables only
```
- **Sources (`SRC_DIR`):** `skit.mp4`, `clips/t1..t9.mp4` (Tarun's takes, in script order), `broll_0640.mp4`, `clean/*.wav`, `tr/med/*.json` (Whisper medium word timings).
- `img/` holds third-party proof assets and is gitignored. It needs `nirvaha_*.png` (Google Play listing), `lnsports_t.png` (from `oneloop-story-reel/img/clients`) and `logo.js` (from `oneloop-showreel`).

## Open items
1. **Original camera files:** the clips came through WhatsApp at 480p. Send the phone originals and the same build re-renders sharp.
2. **Logistics proof:** no product name or screenshots are on file, so it's an illustrated live map with no client name and no numbers. Send real screenshots and the client's OK to name them.
3. **Two unclear skit lines** (0:03.5 and 0:09–0:11 in the raw skit) aren't captioned or used. Send the script lines if you want them in.
