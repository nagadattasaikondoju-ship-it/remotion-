# Sound design playbook (Ultimate Editors house standard)

Source: "UE-Sound-Design-Claude-Training-COMPLETE.md", shared by the user (Drive file 1cZbP3C8ONn_FWaygSY9kgpvKQ7a5CzIm).
Rules below are the user's standard for every edit in this repo. Where a project brief from the user says otherwise
(e.g. One Loop "no music bed"), the project brief wins for that project.

## Philosophy
1. Sound emphasises motion. Nothing on screen → no sound.
2. Three families, one job each:
   - **Whooshes**: movement (slides, pans, zooms, camera moves, scene transitions).
   - **Textures**: events that are not slides (pops, clicks, reveals, write-outs, UI changes, transitions/flashes).
   - **Risers + hits**: anticipation, then release.
3. Never too loud. The voice is king and nothing sits over it louder than it.
4. Under animations and graphics: SFX only, no music. Music goes under the talking head only.
5. One impact per scene. Everything else sits under it.
6. Sound scale matches shot scale: wide shots get roomy sounds, macros get intimate ones.
7. Diegetic first. If the thing on screen makes a real sound, use that sound and name its source.
8. Whoosh peak on the fastest frame of the movement.

## Pipeline (every video, in this order)
1. **Openverse API:** search and fetch real sound effects (`python3 tools/openverse_sfx.py "query" N`, CC0 only).
   They land in `assets/sfx/openverse/<category>/`, with the source and licence of each file in `credits.json`.
2. **Real SFX** (`.claude/skills/real-sfx`): analyse the video and place the sounds on the timeline, on the exact frame.
3. **Earshot** (`.claude/skills/earshot`, `real-sound`): analyse what was placed, generate and refine the missing sounds,
   and check sync, masking and loudness.

The result is a professionally sound-designed video: a new MP4 plus a separate SFX track.

## Library (only source unless told otherwise)
Use the Ultimate Editors SFX library once it's connected. Until then use the CC0 Openverse library from the pipeline above.
Don't generate a sound if a library has one.

Most folders hold 3+ variations. Audition them all, pick one by length, pace and weight, and say which one and why.

**Whooshes:**

| Whoosh | When to use |
|---|---|
| deep voice | most used; the default when unsure |
| hollow, futuristic | go-tos for standard slides and pans |
| organic wind | slow, methodical moves |
| generic long | builds into a fast transition (half riser) |
| synthetic, transition spacey, water dropper | scene-to-scene |
| short | rare; very quick, small moves |
| classy airy | rare; big, heavy moves |

**Textures:**

| On screen | Texture |
|---|---|
| text pops | pop |
| UI pops | UI click |
| change inside an animation | sci-fi click |
| letter-by-letter or typewriter text | gears / tiny gearwheel / complex mechanism gizmo (one per letter/element) |
| on-screen typing | keyboard writing |
| single image/object pop | video scan (gears moving) |
| several assets in sequence | complex mechanism gizmo, one per element |
| new UI/object revealed | sci-fi impact (sci-fi folder is the favourite) |
| into a brand-new animation | activate protection energy |
| clip-to-clip transition or camera flash | **digital camera click, exactly on the transition frame** |
| scene transition | sci-fi hit (also common) |
| huge reveal | cartoon musical heavenly choir |
| conclusion reached | success reward |
| rare low build | alarm buzzer, very low |

**Risers and hits:**
- Favourites: sharp bass riser (typically about 5 s in) and metallic riser.
- Suspenseful build-ups: sparingly.
- Suck-back risers: either very low or very loud, never in the middle.
- Impact hits go under a riser.
- Use at least 2 sharp bass and 2 metallic risers per video.

## Levels (clip gain on library files, which are normalised near 0 dBFS, so roughly peak dBFS)

| Track | Level |
|---|---|
| Whooshes | −12 dB (up to −10 for big moves; never above −10) |
| Textures | −6 to −7 dB (shorter sounds can sit hotter) |
| Risers | −5 dB; hit under it. Riser + hit is the loudest stack of that transition. |
| Music | talking head only, −19 dB under the voice |

If the loudest stack would clip, pull the hit down, never the voice.

## Order (not negotiable)
0. **Confirm assets.** Check the library is connected and note file names. Mute, don't delete, any non-voice original audio.
1. **Analyse frame by frame.** Write a timecoded cue sheet classifying each moment as MOVEMENT → whoosh, EVENT → texture, or BUILD → riser/hit. Report it first.
2. **Ask 2–3 palette questions.** Things to avoid, special moments, the loudest moment. Then wait.
   - Exception: if the user says "start directly", don't block. Still deliver the cue sheet with the result.
3. **Pass 1: whooshes**, top to bottom.
4. **Pass 2: textures.** Place on the exact event frame.
5. **Pass 3: risers and hits.**
   - First riser about 5 s after the hook, with a hit under it.
   - Then segment changes and A-roll → B-roll moments that should feel built.
   - The riser ENDS on the transition frame.
6. **Flag the loudest stack and clipping.**
7. **Hand off for review.** Music only after passes 1–3 are approved. The user supplies their own music.
8. **Learn corrections.** When the user hand-fixes one moment, apply the same logic to every similar moment.

Report after every pass: what was placed, where, which variation, and why.

## Tracks and placement
- One family per track: WHOOSHES · TEXTURES (sub-tracks if they overlap) · RISERS · HITS · MUSIC.
  - In Remotion: one `<Audio>` per clip, grouped per family `<Sequence>`.
  - In HyperFrames: separate `<audio>` elements per family with their own `data-track-index`.
  - Never bake everything into one mixed WAV if the user will refine it.
- Add new tracks. Never touch a layer the user laid down.
- Transitions lead the cut by 2–3 frames. Exceptions:
  - textures land exactly on the event frame;
  - a whoosh's peak sits on the fastest frame.
- Lock the sound's transient/hit point to the visual, not the clip start.
- Place whole clips so each one can be slid or swapped. Overlaps are fine.
- Can't EQ or process library audio. If a muffled version is needed, generate a new one and blend it.
- Generate one sound per request, always an SFX, never music. Never batch.
- Beds and room tone go in first, so the punctuation doesn't feel empty.
- The user always does a manual finish in the mixer; that's by design.

## How the user phrases requests

| Request | What to do |
|---|---|
| "Analyse frame by frame…" | step 1 |
| "Build whooshes / textures / risers first" | that pass |
| "At 00:00:29:58 add X" | single placement locked to the visual peak |
| "Use R01, R04 as risers" | use exactly those IDs |
| "Every X in this sequence → ID" | replace across the whole sequence |
| "Feels empty / cluttered / flat because…" | fix it everywhere |
| "Study 0:00–0:20 and carry it through" | step 8 |
| "3 music options" | audition only; don't place until one is chosen |

## Hand-off checklist
- Every movement has a whoosh, peak on the fastest frame, −12 dB (max −10).
- Every event has a texture on its frame, −6/−7 dB.
- A riser about 5 s after the hook, with a hit under it.
- At least 2 sharp bass and 2 metallic risers at −5 dB.
- Built segment changes have risers.
- No music under graphics.
- Voice untouched and on top.
- One family per track; original audio muted.
- Every placed sound auditioned against its folder variations.
- Loudest stack reported.
- Cue sheet delivered before pass 1; a report after each pass.
