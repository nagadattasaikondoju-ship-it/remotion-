# One Loop ep. 04: "if i rebuilt your brand's website…" (22 Nov 2026)

13.27 s · 1080×1920 · 60 fps, same series format as ep. 01–03 (`../veridale-ig-reel`). AI-slop site vs the rebuilt site,
same brand on both (**Mindly**, the user's call). Overlays chosen by the user: H1 / S1 / B1 / E1 + E2.

| Song time | On screen |
|---|---|
| 0–2.383 | Hook: MVI_0706 (One Loop B-roll Drive, floral shirt typing → hand to chin) + "if i rebuilt / your brand's / website… / ep. 04" |
| 2.383 drop | the neon `<MINDLY/>` slop site (rebuilt in HTML from the user's reference) |
| 3.442 | "AI slop." |
| 4.504 | 12 agent cursors drag red DEL boxes, the slop is deleted; "now watch it get rebuilt. layer by layer." |
| 5.566 / 6.628 / 7.690 / 8.752 | 24 agents (pill: 31 agents · n / 347 layers) drag blue boxes with size tags; nav → headline → copy, buttons, cards → hero land on the beat. Camera pushes in on each area |
| 9.814 | "your brand deserves the second one." |
| 10.876 | browser shrinks; "comment "SITE" and we'll audit yours free" |
| 11.938 | One Loop logo (traced vector, `logo.js`) + chime |

- The multi-cursor effect is the user's reference video (agents building a page) rebuilt in code: `index.html`, `seek(t)`.
- Mindly layers are crops of the user's reference screenshot (`img/mindly_ref.png`); "347 layers" is the effect's counter, not a claim.
- **Song:** "DANCE…" as used in ep. 03. The clean source recording wasn't on this machine, so it comes from the ep. 03 reel: its pops sit on every
  2-beat step, and the reel's events land on those same beats. Extended from 10.08 to 13.27 s by repeating 6 beats [5.538, 8.724).
- **Sound:** house pipeline, three real recordings (swipe 53 as the swarm flies in, glitch 62 on the delete, whoosh 57 on the shrink), balance 10, −14 LUFS.

```
node render.cjs stills 4.5 7 | node render.cjs caption | node render.cjs ui      (NODE_PATH=$(npm root -g))
B=<MVI_0706.MP4> U=<ep03 reel.mp4> bash assemble.sh
```
