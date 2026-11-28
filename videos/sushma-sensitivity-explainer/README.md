# "The Ice Cream Betrayal": tooth-sensitivity explainer (Dr. Sri Sushma Multispeciality Dental Clinic)

| | |
|---|---|
| Brief | User, 26 Nov 2026: a flat 2D explainer (Kurzgesagt-style look: bold flat shapes, soft gradients and glows, smooth zooms inside the tooth) of the story concept "The Ice Cream Betrayal" |
| Length | 30–40 s, vertical |
| Voice | Built-in female voice (Kokoro, local), because the team's own voice isn't available yet |
| End card | The clinic's card, with the same data as the earlier reels |
| Output | 39.8 s, 1080x1920, 60 fps: `out/DrSriSushma_IceCreamBetrayal_Sensitivity_Explainer_1080x1920_60fps_{MASTER,share}.mp4` |

## Story and science (what each beat shows)
| Time | Voice | Picture |
|---|---|---|
| 0–4 s | Riya loved ice cream. Until ice cream started hating her back. | Riya + kulfi, hearts; the kulfi turns angry |
| 4–7 s | One cold bite, and a sharp zap shot through her tooth. | the bite, lightning, screen shake, "ZAP!" |
| 7–11 s | Warm water only. Chewing on one side. Fake smiles at every party. | three habit cards |
| 11–13.5 s | But what was really happening inside her tooth? | push into her mouth, iris into the tooth |
| 13.5–16.8 s | Enamel is your tooth's hard shield. But Riya brushed too hard. | cross-section: enamel labelled, a hard brush scrubbing, enamel flecks |
| 16.8–19.3 s | Her enamel wore thin, and her gums pulled back. | enamel thins (wear marks), the gum line and bone recede |
| 19.3–22.9 s | That exposed the root, full of tiny tubes that lead straight to the nerve. | the exposed root glows; zoom to the tubules (dentinal tubules) and the nerve |
| 22.9–26 s | So cold rushes in, like opening a door in winter. | snowflakes ride the tubules to the nerve, which flares; a door opens on snow |
| 26–28.5 s | At the clinic, the doctor found the real cause. | clinician with a magnifier: hard brushing + gums pulled back |
| 28.5–33 s | They sealed the exposed spots, and switched her to a soft brush, with gentle circles. | a seal coat painted over the root; cold now bounces off; hard brush ✕ → soft brush ✓ in circles |
| 33–36.5 s | Now? The kulfi is back. Sensitive teeth are not something to live with… | sparkles instead of lightning; "Sensitive teeth? Don't live with it." |
| 36.5–39.8 s | …Book your appointment today. | the clinic card ("Cold Hurts? Get It Checked!" + the clinic's details) |

Medical framing is the standard picture of dentine hypersensitivity: exposed dentine tubules let cold move fluid toward the nerve.
- **Causes shown:** enamel wear and gum recession.
- **Fixes shown, kept general:** sealing/protecting exposed areas and a soft brush with a gentle technique.
- **No cure claims.** The CTA is a check-up.

## Build
```
SPEED=1.08 node tts.mjs vo/lines.tsv vo hf_beta      # Kokoro hf_beta, local; then trim + 48 kHz (see below)
for i in $(seq 1 13); do ffmpeg -i vo/l$i.wav -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse" -ar 48000 vo/t$i.wav; done
python3 build_vo.py && echo "window.TL = $(cat timeline.json);" > timeline.js     # STARTS place the lines; Whisper gives word times
NODE_PATH=$(npm root -g) node render.cjs             # explainer.html at 2x -> out/explainer.mp4 (60 fps, 0-36.5 s); --stills t... for QA
bash build.sh                                         # end card, sound pipeline, -14 LUFS, MASTER + share
```

- **Timing:** every animation beat reads its time from the narration's word timings (`KEYS` in explainer.html). Re-voicing the lines re-times the picture automatically.
- **Captions:** word by word, keywords in yellow. Lines 4 and 13 aren't captioned, because the habit cards and the CTA carry that text on screen.
- **Sound:** real recordings only, about 20 cues, all through the house pipeline. There is no music under the animation, per the sound playbook.
