---
name: ten-styles-reel
description: One 5-second shot drawn in ten art styles (Madhubani, Ink Wash, Shadow Puppet, Paper Cut-out, Stained Glass, Anime, Warli, Blueprint, Ukiyo-e, Pahari Miniature), each a canvas animation that is a pure function of time, then cut into a ~26 s 9:16 listicle reel (title, numbered list, card wiping every 2 s, comment CTA, voiceover). Use when the user asks for "10 animation styles", "same shot in different art styles", "Jatayu / Pushpak Viman reel", "Indian folk art styles animation", a style-showcase or "comment X for the prompts" reel, or any one of these ten looks on its own.
---

# Ten styles, one shot (the user's Jatayu × Pushpak Viman guide)

Source: the user's PDF "10 Claude Animation Styles: Jatayu × Pushpak Viman" (uploaded 20 Nov 2026). This skill is that guide turned into
working rules. House rules in `CLAUDE.md` still win: sound pipeline for every video, local voice by default, MASTER + share files sent.

## 1. The idea
One dramatic 5 s moment, drawn ten times. **Shapes and timing are shared; only the paint changes.** Because every clip hits its strike at
exactly 2.0 s, the ten clips cut together on a steady beat. The reel is a listicle: title → ten 2 s cards → comment CTA.

## 2. The shared shot (default subject; swap only these lines for another subject)
- 1080×1920, 30 fps, 150 frames. Canvas, rendered frame by frame.
- **Pushpak Viman:** golden flying temple-boat, swan-neck prow, peacock-curl stern, pillared pavilion (mandapa), three-tier shikhara
  topped by a kalash and a saffron flag. Sails right above a sea of clouds.
- **Jatayu:** giant vulture, white ruff, bald pink head.

| Time | Beat |
|---|---|
| 0–1.7 s | Jatayu dives in from the top right |
| 1.7 s | Wings flare, talons thrown forward |
| **2.0 s** | **STRIKE** on the kalash: flash, feather burst, the viman lurches (tilts and drops, recovers by ~3.0 s) |
| 2.0–5.0 s | He beats his wings and climbs away (out of frame before 5.0 s); a flock of small birds scatters |

Swapping the subject (a dragon, a car, a volcano, a One Loop logo, a tooth for Dr. Sushma): change only these scene lines. Keep the
2.0 s strike, the flare at 1.7 s and the exit by 5.0 s, and the ten style specs below work unchanged.

## 3. Engineering rules (non-negotiable)
- **Pure function of time.** `draw(ctx, t)` paints the whole frame from `t` alone: no state between frames, no `Math.random()`.
  Randomness = a seeded hash of (frame or step index, element index), e.g. `h = fract(sin(i*12.9898 + k*78.233)*43758.5453)`.
  Lamp flicker, jitter and wobble are functions of t too.
- **One shared shapes module** (`anims/shapes.js`): `drawViman(ctx, x, y, s, pose)`, `drawJatayu(ctx, x, y, s, pose)`,
  `drawFeathers`, `drawBirds`, `drawClouds`, and one `poseAt(t)` that returns positions, wing angle, tilt and the strike flash.
  Each style file imports them and only supplies the paint (fills, strokes, patterns, textures, the strike effect).
  Shapes take a style object (`{fill, stroke, outline:'double', pattern, …}`) rather than hard-coded colours.
- **Stepped motion** for hand-made looks: sample the pose at `floor(t*fps)/fps` (Paper Cut-out 12 fps, Warli wobble 8 fps) inside the 30 fps clip.
- **Safe zone 9:16:** all text inside x 60–960, y 250–1500. 16:9: text x 192–1728, y 108–972; action x 96–1824, y 54–1026.
- **Devanagari** (the "जटायु" column / cartouche): load Noto Sans Devanagari (OFL, github.com/google/fonts) into the project's `fonts/`;
  the container has no Devanagari font, so it renders as boxes otherwise.
- **Check before rendering:** stills at 0.6, 2.0 and 4.0 s first. Fix shapes and poses on the first style; all ten inherit them.
- **Render:** HyperFrames (`npx hyperframes render -c anims/<style>.html -o assets/clips/<style>.mp4 -w 1`, see `hyperframes-cli`),
  or this repo's Playwright frame-grabber pattern (`render.cjs` with `seek(t)`, e.g. `videos/sushma-jerry-reel`). Never let either download a second Chrome.

## 4. The ten styles
Send/apply one at a time: "Now make the same shot in this style: …". Palettes sampled from the guide's swatches.

| # | Style | Palette | Paint | Strike | Check for |
|---|---|---|---|---|---|
| 01 | **Madhubani** (Mithila folk painting, Bihar) | #D63A1F vermilion · #F0B323 turmeric · #4F8A2E leaf · #2B3A8C indigo · #EFE2C4 paper | Handmade paper; double ink outlines with a paper-coloured gap; flat fills; hatching, fish-scale and dot patterns inside every shape; almond fish eyes; rayed sun; red border of yellow triangles | Red-and-yellow star burst | No shape left flat/empty; the triangle border |
| 02 | **Ink Wash** (Sumi-e) | #F4EFE4 rice paper · #B9B4AB · #6B6760 · #1C1B1A ink · #D33A20 vermilion | Grey washes that darken where they overlap (multiply), dry-brush streaks, soft ink bleed, misty peaks fading into blank paper; vermilion only on sun, flag, seal; vertical "जटायु" column on the left | Ink splatter + one fast brush arc | Lots of empty paper; column inside the safe zone |
| 03 | **Shadow Puppet** (Tholu Bommalata, Andhra Pradesh) | #F3D9A4 lit screen · #C2501F · #8A2B1C · #3D6B3A dyed leather · #2A1B12 | Translucent dyed leather on a cotton screen lit by a flickering lamp; punched holes that let light through; carved outlines; control rods running off the bottom; soft cast shadow | Lamp flare | Light through leather and holes; rods off the bottom edge; flicker is a function of t |
| 04 | **Paper Cut-out** (layered card, stop motion) | #8EC5E8 sky · #FFFFFF cut edge · #F2C14E · #E5603B · #5A4A8A | Layered coloured card, soft drop shadows, thin white cut edges, wavy paper sky strips, stacked cloud strips, paper texture over all; motion stepped at 12 fps with a tiny seeded jitter per step | Paper starburst | 12 fps steps; white edges + shadow on every layer |
| 05 | **Stained Glass** (temple window mosaic) | #1D4FA3 · #B3122E · #1F8A5B · #E9B52A jewel glass · #1A1A1A lead | Pointed-arch temple window; every shape a mosaic of jewel glass in dark lead lines; light glowing through from behind; iron bars across the window | White-gold glass star + flare | Lead between every piece; back-glow; iron bars |
| 06 | **Anime** (TV cel shading) | #3FA6F2 sky · #FFFFFF · #FFCF4A · #E8262F · #111111 ink | Saturated sky, huge cumulus, two-tone hard shadows, bold ink lines; speed lines only during the dive | Exactly 3 black/white impact frames at 2.0 s, then a red frame, then a lens flare | Hard-edged two-tone shading; frame-exact impact |
| 07 | **Warli** (tribal wall art, Maharashtra) | #8A3B22 / #6E2C18 red-brown mud · #F5EFE3 rice-paste white · #D8C9AD | Only circles, triangles and lines: hourglass-triangle bodies, line-fan wings, triangle-chain shikhara, rows of scallops for clouds, triangle-chain border; line wobble updates at 8 fps | Dotted rings | White on mud only; 8 fps wobble |
| 08 | **Blueprint** (engineering drawing on cyanotype) | #1D4E89 · #2F66A8 cyanotype · #FFFFFF lines · #A9C6EA grid | Grid, white line-work only, dimension lines (L = 21.6 m, WINGSPAN 7.4 m), callouts (KALASH, MANDAPA), Jatayu's dashed flight path, title block top-left | "TARGET LOCK" reticle becomes "IMPACT T+2.00s" exactly at 2.0 s | All labels and the title block inside the safe zone |
| 09 | **Ukiyo-e** (Edo woodblock print) | #1F3A6B Prussian blue · #6F93B8 · #C8402F red sun · #E7DCC2 paper · #1B1B1B key block | Prussian-blue gradient sky (bokashi), red sun, horizontal mist bands, flat muted colours, black key-block lines, the cloud sea as clawed foam waves, vertical "जटायु" cartouche with a red seal, woodgrain over the print | Not named in the guide: use a woodblock-style radial spray of key-block lines + paper-white flash | Clawed foam waves; cartouche in the safe zone; woodgrain |
| 10 | **Miniature Painting** (Pahari court, Himalayan foothills) | #1F3F9A lapis · #D4A73A gold · #5B8F3C · #C0392B · #F2EAD6 | Lapis sky band with gold scroll clouds, pale wash below, rolling green hills with round dotted trees and a river, jewel-flat colours, hairline outlines, burnished gold viman with pearl dots, red border with a gold vine | Gold rays | Lapis band on top; hairlines; pearl dots; red/gold border |

## 5. The reel (≈26 s, 9:16)
- Cream background. Title at the top: "10 Claude" with a small spark badge, "Animation styles" below (for a client, their own title).
- Numbered list 1–10 on the left; each style name fades in as its card appears.
- A gold-bordered 9:16 card on the right that wipes to the next style **every 2 s**.
- **Timing trick:** each clip is shown from **1.05 s**, so the 2.0 s strike lands **0.95 s** into its card: every card opens on the dive and
  hits mid-card, a steady punch. Layout: Title (~3 s) · 10 × 2 s cards · Comment CTA (~3 s).
- End: "COMMENT 'Claude' FOR THE PROMPTS" (or the client's keyword) over moving tiles of all ten clips.
- All text inside x 60–960, y 250–1500. Render to MP4.

## 6. Voice and sound
- Script: "Ten Claude animation styles." → each style name as its card wipes in (Madhubani. Ink Wash. Shadow Puppet. Paper Cut-out.
  Stained Glass. Anime. Warli. Blueprint. Ukiyo-e. Miniature Painting.) → "Comment Claude, and I'll send you the prompts."
- Voice: local Kokoro (explainroo / kokoro-js) by default; ElevenLabs only if the user asks (paid). Set pronunciation by hand for
  Madhubani (mudh-oo-BAH-nee), Warli (WAR-lee), Ukiyo-e (oo-KEE-yoh-eh); use phonemes, as done for "Sushma".
- Each name starts on its card wipe; the list item fades in at the same moment. Mix to −14 LUFS.
- Sound goes through the house pipeline (Openverse → real-sfx → earshot): one whoosh per card wipe, one texture on each strike
  (0.95 s into each card), riser into the CTA. Few sounds, real recordings.

## 7. Troubleshooting
| Situation | Fix |
|---|---|
| Strike off-beat in the reel | Check the clip's frame 60 is the strike, and the reel starts each clip at 1.05 s |
| Flicker between renders | Something uses randomness or remembers earlier frames: seed by frame index |
| A style drifts from the scene | Reuse the shared shapes file; only change the paint |
| Devanagari boxes | Load Noto Sans Devanagari |
| Text hidden on Instagram | Draw the safe zone over a frame; move anything outside it |
| Slow render | One clip at a time, `-w 1`; texture-heavy styles take longest |

## 8. Checklist
Stills at 0.6 / 2.0 / 4.0 s approved → ten styles, preview after each → ten clips in `assets/clips/` → reel with title, list, cards, CTA →
text in the safe zone → voice with fixed pronunciations, −14 LUFS → sound pipeline → watch once on a phone → MASTER + share sent.
16:9 version: same timings; viman drifts x 500→1050 with keel near y 640, cloud sea in the lower third with parallax bands, Jatayu's dive on a long diagonal.
