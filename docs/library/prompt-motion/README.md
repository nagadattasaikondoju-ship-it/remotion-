# Prompt Motion — motion-graphics prompt & skill library

Source: [prompt-motion.com](https://prompt-motion.com), a gallery of motion videos made with Claude Opus 5.5, with the prompts and skills behind them, curated by [@p4nthera_](https://x.com/p4nthera_). Scraped 22 Oct 2026.
Everything belongs to its creators, credited per entry. The skills keep their MIT / Apache-2.0 licences.

**236 entries:** 232 Prompts and 5 Skills (one entry is both). Full data, including prompt text, stack, date, links and video URL, is in [`all_entries.json`](all_entries.json).

## Categories (one file each, with the full prompt text)

Entries can belong to several categories.

| Category | Entries | File |
|---|---|---|
| Product UI | 103 | [`categories/product-ui.md`](categories/product-ui.md) |
| Phone | 22 | [`categories/phone.md`](categories/phone.md) |
| Charts | 34 | [`categories/charts.md`](categories/charts.md) |
| Diagrams | 31 | [`categories/diagrams.md`](categories/diagrams.md) |
| Kinetic type | 98 | [`categories/kinetic-type.md`](categories/kinetic-type.md) |
| Shapes | 44 | [`categories/shapes.md`](categories/shapes.md) |
| Particles | 43 | [`categories/particles.md`](categories/particles.md) |
| Characters | 27 | [`categories/characters.md`](categories/characters.md) |
| Photos | 23 | [`categories/photos.md`](categories/photos.md) |
| Music | 51 | [`categories/music.md`](categories/music.md) |
| Code | 21 | [`categories/code.md`](categories/code.md) |
| Uncategorized | 4 | [`categories/uncategorized.md`](categories/uncategorized.md) |

## Templates (both on the site)

These are the curator's own customizable prompts, separate from the gallery:
- **[The showreel prompt](templates/showreel.md):** the improved version of the most-used prompt on the site, the 15-second motion-designer showreel. It's the brief behind our One Loop "One stroke" showreel.
- **[The 3D template](templates/realtime.md):** for real-time three.js pieces, with the gallery set as a 3D space of video cards; swap in your subject.

## Skills (all 5 on the site)

| Skill | What it does | Engine | Here | Licence |
|---|---|---|---|---|
| **[TasteSkill dashboard showcase](https://prompt-motion.com/lexnlin-f9b3bd8)** by @LexnLin | A design skill that gives coding agents an art direction, real images and in-browser checks so they build distinctive websites, dashboards and app screens. | any web stack | reference copy; source [`skills/taste-skill/skills/taste-skill/SKILL.md`](skills/taste-skill/skills/taste-skill/SKILL.md) | MIT |
| **[Cinetic skill launch film](https://prompt-motion.com/lexnlin-6161a6)** by @LexnLin | An agent skill that has your coding agent concept, brand, score and render a short cinematic launch film or motion piece from code. | Remotion 4 or HyperFrames | **installed** → `.claude/skills/cinetic`; source [`skills/cinetic/skills/cinetic/SKILL.md`](skills/cinetic/skills/cinetic/SKILL.md) | MIT |
| **[Indian civilisation history film](https://prompt-motion.com/buildfastwithai-53234e)** by @BuildFastWithAI | A Claude skill that makes an animated MP4 film on any topic, with every frame drawn in code and a synthesised, beat-synced soundtrack. | Python (pycairo/Pillow + numpy audio) | reference copy; source [`skills/generative-film-skill/SKILL.md`](skills/generative-film-skill/SKILL.md) | MIT |
| **[Reddit marketing tool launch video](https://prompt-motion.com/anthonyriera-9b1b2a)** by @anthonyriera | A Claude Code skill that learns your product's design system, interviews you about the film, then builds and renders a launch or landing-page video in Remotion using your real components, logo and music. | Remotion, in the product's codebase | **installed** → `.claude/skills/product-film`; source [`skills/product-film-skill/plugins/product-film/skills/product-film/SKILL.md`](skills/product-film-skill/plugins/product-film/skills/product-film/SKILL.md) | MIT |
| **[Animated agent session story](https://prompt-motion.com/jake11moran-a269c4)** by @jake11moran | Has your agent read your local Claude Code history and turn a typical session with you into a short scored animated film rendered in HyperFrames. | HyperFrames + p5.brush | reference copy; source [`skills/session-story/SKILL.md`](skills/session-story/SKILL.md) | Apache-2.0 |

**cinetic** and **product-film** are installed as project skills; the other three are kept as reference.

## Techniques across all prompts

| Technique | Prompts |
|---|---|
| music / BPM / beat sync | 31 |
| light canvas | 28 |
| real product / URL | 24 |
| spring / easing | 23 |
| camera moves | 19 |
| UI components / dashboard | 16 |
| dark canvas | 16 |
| 3D / depth | 15 |
| sound effects | 14 |
| cursor / real clicks | 14 |
| particles | 11 |
| kinetic type | 9 |
| one shape / morph | 7 |
| loop | 7 |
| motion blur | 6 |

**Takeaways for our videos:**
- **Most prompts are short:** a product URL plus the story beats.
- **The detailed ones lock in a few things:** one continuous element, a cursor doing real clicks, one UI font, a light canvas with one accent, a song at about 120 BPM, spring easing, motion blur, and a render-and-review loop.
- **We already use most of this:** it matches the One Loop house style (one stroke, beat grid, review stills).
- **Worth adding:** cursor-driven UI-state morphs and real-product-URL capture.
