# One Loop: "We don't build demos" (skit + Tarun)

61 s · rendered in 4K (2160×3840, 30 fps), with HD (1080×1920) copies downscaled from it.
The skit plays **in story order** (the demo → 3 weeks later the crash → the client calls the manager) and hands over on a record-scratch
freeze to Tarun's explanation: demo vs real world → three proofs → "We don't build demos" → follow → **Comment BUILD**.

Built from Tarun's editing notes (cold open; the sketch "natural, no heavy cuts"; quick zoom on the developer at the crash; freeze + scratch on
the manager call; playful → documentary music; fast keyword cuts; one steady shot; a full-screen flash per proof; a 2 s CTA hold; captions
throughout) and the three style references (see `ANALYSIS.md`).

## v2 changes (user review, Nov 13)
- **Story continuity.** v1 reordered and chopped the skit (26 s → 13.7 s), so the story jumped. v2 keeps every line in its place and only
  removes dead air. Story labels make it readable on mute: THE DEVELOPER / THE CLIENT, DEMO APPROVED + "Deploying to production…",
  a "3 weeks later…" card (from Tarun's script), the red "Deployment failed" toast, and a "Calling Manager…" chip with a call timer.
- **Captions match the audio.** The skit was re-transcribed with Whisper turbo (and checked against medium, cleaned audio and focused
  decodes). "But you can't deploy it" was wrong: the client says **"So you can deploy it."** Two short lines nobody (and no model) can
  make out are cut, not guessed (see `ANALYSIS.md`).
- **Bigger circle.** The picture-in-picture circle is now medium (radius 260 instead of 196) and frames Tarun's whole head, hair to chin.
- **Clearer motion graphics.** Each graphic says what it shows: YOUR APP LIVE → DOWN on the flatline, USERS ONLINE + SERVER LOAD,
  MESSY DATA with a legend (duplicates, empty/NULL, wrong format), BAD NETWORK. The proof cards were re-laid out to sit clear of the circle.
- **Quality.** All footage was AI-upscaled ×4 (Real-ESRGAN general-x4v3, `tools/upscale_realesr.py`) and the whole reel renders in 4K;
  captions and graphics are drawn at 4K, not scaled up.

## Edit (`timeline.py`, one table drives picture, dialogue, captions and sound)

| Time | Shot | What happens |
|---|---|---|
| 0.0 | cold open | flash-forward: "Please do something!", a punch-in on the developer, red "Deployment failed" toast |
| 1.2 | black | "He had no idea / what was coming." |
| 2.5 | the demo (wide) | THE DEVELOPER / THE CLIENT labels, DEMO DAY. Developer: "That's about the entire software." |
| 4.2 | the client (closer) | "The demo looks fine. So you can deploy it." DEMO APPROVED, then "Deploying to production…" fills |
| 7.05 | black card | "3 weeks later…" / "the app goes live" |
| 8.2 | the crash | "Deployment failed" toast, red pulse. Client: "Please do something!" (quick zoom on the developer). Developer: "I'll do something." |
| 11.55 | the call | The client walks off and phones the manager ("Calling Manager…", then a call timer): "Hey, hi. Listen, the demo is actually good. But I don't know what's the problem, but it failed in deployment. Can you… [looks back at the developer] just change the developer, please?" (punch-in on the punchline) |
| 22.1 | freeze | Record scratch + tape-stop, "The demo worked. / Deployment didn't.", Tarun's "You see," over the frozen frame (J-cut) |
| 23.5 | Tarun | "…software that dies": a YOUR APP monitor beeps three times and flatlines (LIVE → DOWN) on "dies" |
| 26.3 | split screen | Top: the DEMO panel (clean data ✓, one user ✓, Wi-Fi perfect ✓). Bottom: Tarun. The panel glitches apart. |
| 29.95 | b-roll | Night traffic (One Loop Drive MVI_0640) + "THE REAL WORLD walks in." |
| 31.75 / 32.8 / 34.0 | full-screen MG | Users 1 → 500 + server load · messy-data table + legend · phone on a bad network → "Request timed out" (Tarun in the circle) |
| 36.5 | one steady shot | "we build for the **wild** from day one", the One Loop badge on "OneLoop" |
| 42.8 / 44.6 / 46.9 | proofs 1–3 | Nirvaha (real Google Play listing and screenshots) · logistics (illustrated map, see open items) · LN Sports Arena (real logo, booking grid). Tarun in the circle. |
| 50.7 | copper slam | "WE DON'T BUILD **DEMOS.**" (struck through) → "WE BUILD SOFTWARE THAT ACTUALLY **WORKS.**" |
| 53.4 | logo | The traced One Loop logo lands with a bass hit; "Follow @oneloop.in" |
| 56.7–60.95 | CTA | "Comment **BUILD**", a comment box types B-U-I-L-D, "so that we build yours.", 2 s hold |

## Look
- **Captions:** white Poppins 800, word by word with a small pop, the punch word in One Loop copper, a heavy shadow and stroke for contrast.
  - Placed below faces and the mic, and beside the circle during full-screen graphics.
  - The two unclear skit lines are left out.
- **Grade:** warm and natural for the skit; cooler, documentary-style for Tarun (per his notes).
- **Upscaling:** the sources are WhatsApp-compressed 480×854. They are upscaled ×4 by Real-ESRGAN general-x4v3 (BSD-3; weights from
  Hugging Face as safetensors, network written out in `tools/upscale_realesr.py`, run on CPU in bfloat16), then placed into a 4K frame
  with a touch of grain so faces don't look plastic. Original camera files would still look better.

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
# once per container: AI-upscale the takes (CPU, ~1 h), see the top of tools/upscale_realesr.py for the weights
/usr/bin/python3 -P ../../tools/upscale_realesr.py $SRC_DIR/skit.mp4 $SRC_DIR/up/skit.mp4 --crf 10   # + clips/t1..t9 with --ss/--to, offsets in up/offsets.json
bash assemble.sh                 # timeline → base_render.py (picture) → render.mjs video (overlay) → sound → deliverables
SKIP_PICTURE=1 bash assemble.sh  # sound + deliverables only
```
- **Sources (`SRC_DIR`):** `skit.mp4`, `clips/t1..t9.mp4` (Tarun's takes, in script order), `broll_0640.mp4`, `clean/*.wav`, `tr/med/*.json` (Whisper medium word timings).
- `img/` holds third-party proof assets and is gitignored. It needs `nirvaha_*.png` (Google Play listing), `lnsports_t.png` (from `oneloop-story-reel/img/clients`) and `logo.js` (from `oneloop-showreel`).

## Open items
1. **Original camera files:** the clips came through WhatsApp at 480p; v2 upscales them with AI, but the phone originals would be sharper still.
2. **Logistics proof:** no product name or screenshots are on file, so it's an illustrated live map with no client name and no numbers. Send real screenshots and the client's OK to name them.
3. **Two unclear skit lines** (the developer at 0:03–0:04 and the client at 0:09–0:11 in the raw skit) are cut. Send the script lines and they go back in, captioned.
