# Prompt Motion — product motion-graphics library

Source: [prompt-motion.com](https://prompt-motion.com), a gallery of motion videos made with Claude Opus 5.5, with the prompts and skills behind them, curated by [@p4nthera_](https://x.com/p4nthera_). Scraped 22 Oct 2026.

Everything here belongs to its creators, who are credited on every entry. The skills are MIT or Apache-2.0 licensed; each folder keeps its licence.

## Site at a glance

- **236 entries in total:** 232 Prompts and 5 Skills (one entry is tagged as both).
- **Categories (entry counts):** Product UI 103 · Kinetic type 98 · Music 51 · Shapes 44 · Particles 43 · Charts 34 · Diagrams 31 · Characters 27 · Photos 23 · Phone 22 · Code 21.
- **This library:** all 103 Product UI entries plus every Skill = 105 entries, with full prompt text, stack, date, creator post and video URL (`product_ui_library.json`).

## The skills (downloaded into `skills/`)

| Skill | What it does | Engine | Install | Local copy | Licence |
|---|---|---|---|---|---|
| **[TasteSkill dashboard showcase](https://prompt-motion.com/lexnlin-f9b3bd8)** by @LexnLin | A design skill that gives coding agents an art direction, real images and in-browser checks so they build distinctive websites, dashboards and app screens. | any web stack (art direction + in-browser checks) | `npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"` | [`skills/taste-skill/skills/taste-skill/SKILL.md`](skills/taste-skill/skills/taste-skill/SKILL.md) | MIT |
| **[Cinetic skill launch film](https://prompt-motion.com/lexnlin-6161a6)** by @LexnLin | An agent skill that has your coding agent concept, brand, score and render a short cinematic launch film or motion piece from code. | Remotion 4 (default) or HyperFrames | `npx skills add Leonxlnx/cinetic` | [`skills/cinetic/skills/cinetic/SKILL.md`](skills/cinetic/skills/cinetic/SKILL.md) | MIT |
| **[Indian civilisation history film](https://prompt-motion.com/buildfastwithai-53234e)** by @BuildFastWithAI | A Claude skill that makes an animated MP4 film on any topic, with every frame drawn in code and a synthesised, beat-synced soundtrack. | Python (pycairo + Pillow) + numpy/scipy audio | `npx skills@latest add https://github.com/buildfastwithai/buildfast-skills` | [`skills/generative-film-skill/SKILL.md`](skills/generative-film-skill/SKILL.md) | MIT |
| **[Reddit marketing tool launch video](https://prompt-motion.com/anthonyriera-9b1b2a)** by @anthonyriera | A Claude Code skill that learns your product's design system, interviews you about the film, then builds and renders a launch or landing-page video in Remotion using your real components, logo and music. | Remotion, inside the product's own codebase | `see repo: https://github.com/Rieranthony/product-film-skill` | [`skills/product-film-skill/plugins/product-film/skills/product-film/SKILL.md`](skills/product-film-skill/plugins/product-film/skills/product-film/SKILL.md) | MIT |
| **[Animated agent session story](https://prompt-motion.com/jake11moran-a269c4)** by @jake11moran | Has your agent read your local Claude Code history and turn a typical session with you into a short scored animated film rendered in HyperFrames. | HyperFrames + p5.brush | `npx skills add heygen-com/hyperframes-community-skills --skill session-story` | [`skills/session-story/SKILL.md`](skills/session-story/SKILL.md) | Apache-2.0 |

Product-motion picks: **cinetic** (cinematic launch/product films), **product-film** (Remotion films built from the product's own design system), **taste-skill** (art direction for the UI shown in the film).
**session-story** and **generative-film** are general motion skills. They're not product-specific, but they're useful patterns: HyperFrames + p5.brush characters, and code-drawn film with a beat-synced synth score.

## What the 103 Product UI prompts have in common

How often each technique appears across the prompts (an entry can count under several):

| Technique | Prompts |
|---|---|
| brand / real site URL | 21 |
| spring / easing | 19 |
| light mode / white canvas | 19 |
| music / BPM / beat | 19 |
| camera moves | 15 |
| UI states / components | 14 |
| dark mode | 14 |
| motion blur | 13 |
| cursor / clicks | 13 |
| sound effects | 12 |
| HTML/Playwright | 11 |
| Geist / Inter font | 11 |
| 3D / depth | 10 |
| kinetic type | 10 |
| morph / one shape | 6 |
| loop | 5 |
| Remotion | 5 |
| HyperFrames | 1 |

**Stack stated:** not stated 74 · Remotion 11 · HyperFrames 5 · HTML + Playwright 3 · HTML 2 · WebGL2 + Playwright 1 · HTML canvas + Playwright + ffmpeg 1 · Remotion, React 1 · JavaScript 1 · HTML, Playwright 1 · HTML/JS, Playwright, ffmpeg 1 · Three.js 1 · Blender 1.

**Also tagged with:** kinetic-type 23 · phone 22 · music 20 · photos 18 · charts 17 · code 12 · diagrams 7 · particles 6 · characters 5.

**Takeaways for our product videos:**
- **Most prompts are short.** Many just point Claude at a product URL and name the beats, for example "user creates a campaign → connects metrics → agent responds → analytics". The best-performing long prompts specify a single continuous element (one shape morphing through UI states), a cursor that does real clicks and drags, one UI font (Geist or Inter), a light neutral canvas with one accent, a song at about 120 BPM, and render-and-review loops.
- **These match the house rules we already use** (one stroke / one shape, beat grid, spring easing, motion blur, review stills). Bring in the cursor-driven UI-state morphs and the real-product-URL capture for One Loop client launch videos.

## Longest, most detailed Product UI prompts (worth studying first)

- [Taxtello bookkeeping app film](https://prompt-motion.com/daniel-haida-8691d4) by @daniel_haida (15306 chars, Remotion)
- [Launch video remake comparison](https://prompt-motion.com/notdwd-c2037d) by @notdwd (10419 chars, stack not stated)
- [Frame by Frame launch video](https://prompt-motion.com/notdwd-7de38a) by @notdwd (10311 chars, stack not stated)
- [Spotify product film](https://prompt-motion.com/brainextends-e19ac3) by @brainextends (8142 chars, stack not stated)
- [Landing page 3D scroll](https://prompt-motion.com/twoclipping-d89be5) by @twoclipping (6638 chars, WebGL2 + Playwright)
- [Ora 2 image model launch film](https://prompt-motion.com/rossaxbt-3085b7) by @rossaxbt (5800 chars, HTML canvas + Playwright + ffmpeg)
- [Photo print app launch film](https://prompt-motion.com/twoclipping-221cab) by @twoclipping (5222 chars, HTML + Playwright)
- [Food craving launch film](https://prompt-motion.com/ultimaxbt-2ddf1e) by @ultimaxbt (4667 chars, HTML)
- [Prompt Motion site promo](https://prompt-motion.com/antonio-kodheli-490109) by @antonio_kodheli (4024 chars, Remotion)
- [White ball UI motion loop](https://prompt-motion.com/rossaxbt-94583b) by @rossaxbt (3684 chars, HTML)
- [Morphing UI states loop](https://prompt-motion.com/demonugc-4c5753) by @demonugc (2711 chars, HTML, Playwright)
- [Shape morphing through UI states](https://prompt-motion.com/twoclipping-5cba86) by @twoclipping (2711 chars, HTML + Playwright)

## All Product UI entries

Newest first. The full prompt text for each is in [`product-ui-prompts.md`](product-ui-prompts.md).

| # | Title | Creator | Date | Type | Stack | Other tags |
|---|---|---|---|---|---|---|
| 1 | [TasteSkill dashboard showcase](https://prompt-motion.com/lexnlin-f9b3bd8) | [@LexnLin](https://x.com/LexnLin) | 2026-10-20 | skill | — | charts |
| 2 | [Landing page 3D scroll](https://prompt-motion.com/twoclipping-d89be5) | [@twoclipping](https://x.com/twoclipping) | 2026-10-14 | prompt | WebGL2 + Playwright | kinetic-type |
| 3 | [White ball UI motion loop](https://prompt-motion.com/rossaxbt-94583b) | [@rossaxbt](https://x.com/rossaxbt) | 2026-10-10 | prompt | HTML | music |
| 4 | [Food craving launch film](https://prompt-motion.com/ultimaxbt-2ddf1e) | [@ultimaxbt](https://x.com/ultimaxbt) | 2026-10-08 | prompt | HTML | kinetic-type, photos, music |
| 5 | [Ora 2 image model launch film](https://prompt-motion.com/rossaxbt-3085b7) | [@rossaxbt](https://x.com/rossaxbt) | 2026-10-07 | prompt | HTML canvas + Playwright + ffmpeg | photos, music |
| 6 | [Prompt Motion site promo](https://prompt-motion.com/antonio-kodheli-490109) | [@antonio_kodheli](https://x.com/antonio_kodheli) | 2026-10-06 | prompt | Remotion | music |
| 7 | [SuperX feature release teaser](https://prompt-motion.com/robj3d3-b18fad) | [@robj3d3](https://x.com/robj3d3) | 2026-10-05 | prompt | — |  |
| 8 | [Cinetic skill launch film](https://prompt-motion.com/lexnlin-6161a6) | [@LexnLin](https://x.com/LexnLin) | 2026-10-04 | skill | — | code |
| 9 | [Lism CSS 1.0 release video](https://prompt-motion.com/ddryo-loos-300829) | [@ddryo_loos](https://x.com/ddryo_loos) | 2026-10-02 | prompt | — | code |
| 10 | [ViralGrow product promo](https://prompt-motion.com/samuel-yostt-891f87) | [@samuel_yostt](https://x.com/samuel_yostt) | 2026-10-01 | prompt | — | phone, photos |
| 11 | [Supasito launch video](https://prompt-motion.com/wozu-co-242285) | [@wozu_co](https://x.com/wozu_co) | 2026-10-01 | prompt | — |  |
| 12 | [Chunku product promo](https://prompt-motion.com/reyzostyle-b55864) | [@reyzostyle](https://x.com/reyzostyle) | 2026-09-30 | prompt | HyperFrames | kinetic-type |
| 13 | [DistilBook motion explainer](https://prompt-motion.com/sudo-kiran-b055de) | [@sudo_kiran](https://x.com/sudo_kiran) | 2026-09-29 | prompt | — | diagrams |
| 14 | [Dubz Up motion showreel](https://prompt-motion.com/devius-maximus-beab45) | [@Devius_Maximus](https://x.com/Devius_Maximus) | 2026-09-29 | prompt | — | phone, kinetic-type, characters |
| 15 | [Launch video remake comparison](https://prompt-motion.com/notdwd-c2037d) | [@notdwd](https://x.com/notdwd) | 2026-09-28 | prompt | — | photos, music |
| 16 | [Mascot referral program promo](https://prompt-motion.com/paulo-kombucha-96431c) | [@paulo_kombucha](https://x.com/paulo_kombucha) | 2026-09-28 | prompt | — | characters |
| 17 | [FundMyCompute platform overview](https://prompt-motion.com/jayscambler-3f8889) | [@JayScambler](https://x.com/JayScambler) | 2026-09-28 | prompt | — | diagrams |
| 18 | [Bold Pilot SEO promo](https://prompt-motion.com/utopyaszx-1b2f94) | [@utopyaszx](https://x.com/utopyaszx) | 2026-09-28 | prompt | — | charts, kinetic-type |
| 19 | [Photo retouch app promo](https://prompt-motion.com/oliahmed205-3e31c4) | [@oliahmed205](https://x.com/oliahmed205) | 2026-09-28 | prompt | — | photos |
| 20 | [GenVizu product launch](https://prompt-motion.com/listudio-820c7b) | [@listudio](https://x.com/listudio) | 2026-09-28 | prompt | — | photos |
| 21 | [sweetRegret app update reel](https://prompt-motion.com/thilina-a-891c09) | [@thilina_a](https://x.com/thilina_a) | 2026-09-28 | prompt | — | phone, characters |
| 22 | [AjustaCV Pro pricing promo](https://prompt-motion.com/thayto-dev-44b911) | [@thayto_dev](https://x.com/thayto_dev) | 2026-09-27 | prompt | HyperFrames |  |
| 23 | [Frame by Frame launch video](https://prompt-motion.com/notdwd-7de38a) | [@notdwd](https://x.com/notdwd) | 2026-09-27 | prompt | — | music |
| 24 | [Pixelup Labs studio showreel](https://prompt-motion.com/arjunsh1607-93005d) | [@arjunsh1607](https://x.com/arjunsh1607) | 2026-09-27 | prompt | — | photos |
| 25 | [Whiteboard skill tutorial](https://prompt-motion.com/lemomo-ai-0d9cff) | [@lemomo_ai](https://x.com/lemomo_ai) | 2026-09-27 | prompt | — | diagrams |
| 26 | [Trezio app motion reel](https://prompt-motion.com/agonaliu-466a8f) | [@agonaliu_](https://x.com/agonaliu_) | 2026-09-27 | prompt | — | kinetic-type |
| 27 | [Taxtello bookkeeping app film](https://prompt-motion.com/daniel-haida-8691d4) | [@daniel_haida](https://x.com/daniel_haida) | 2026-09-27 | prompt | Remotion | charts |
| 28 | [Product intro synced to music](https://prompt-motion.com/bogdandragomir-35e024) | [@BogdanDragomir](https://x.com/BogdanDragomir) | 2026-09-27 | prompt | — | particles, music |
| 29 | [Website analyzer product promo](https://prompt-motion.com/en-ra-81c6dd) | [@en______ra](https://x.com/en______ra) | 2026-09-27 | prompt | — |  |
| 30 | [Ondefica app motion reel](https://prompt-motion.com/jesscaroline7-1ff7cb) | [@jesscaroline7](https://x.com/jesscaroline7) | 2026-09-27 | prompt | HyperFrames | phone, charts, kinetic-type |
| 31 | [Second brain service promo](https://prompt-motion.com/theviableedge-9065be) | [@TheViableEdge](https://x.com/TheViableEdge) | 2026-09-27 | prompt | Remotion | code |
| 32 | [SaaS launch video](https://prompt-motion.com/aschapmann-131210) | [@aschapmann](https://x.com/aschapmann) | 2026-09-27 | prompt | Remotion | music |
| 33 | [Muse connector tracker promo](https://prompt-motion.com/elliot-garreffa-f334bc) | [@elliot_garreffa](https://x.com/elliot_garreffa) | 2026-09-27 | prompt | Remotion |  |
| 34 | [YouTube transcript product ad](https://prompt-motion.com/tstfully-0aa6b4) | [@tstfully](https://x.com/tstfully) | 2026-09-27 | prompt | — | kinetic-type |
| 35 | [Photo print app launch film](https://prompt-motion.com/twoclipping-221cab) | [@twoclipping](https://x.com/twoclipping) | 2026-09-26 | prompt | HTML + Playwright | phone, photos, music |
| 36 | [Travel visa service promo](https://prompt-motion.com/thismacapital-dfba20) | [@thismacapital](https://x.com/thismacapital) | 2026-09-26 | prompt | — | kinetic-type, photos |
| 37 | [Reddit marketing tool launch video](https://prompt-motion.com/anthonyriera-9b1b2a) | [@anthonyriera](https://x.com/anthonyriera) | 2026-09-26 | skill | Remotion | characters |
| 38 | [mdfor.dev product intro video](https://prompt-motion.com/ho-ba-f3f0e9) | [@HO_BA](https://x.com/HO_BA) | 2026-09-26 | prompt | — | code |
| 39 | [MotionSites one million visitors](https://prompt-motion.com/viktoroddy-98c1d8) | [@viktoroddy](https://x.com/viktoroddy) | 2026-09-26 | prompt | — | charts, code |
| 40 | [Email tool promo reel](https://prompt-motion.com/melvynx-6cde6c) | [@melvynx](https://x.com/melvynx) | 2026-09-26 | prompt | — | kinetic-type |
| 41 | [Jev engineering showreel](https://prompt-motion.com/polydao-7a572b) | [@polydao](https://x.com/polydao) | 2026-09-26 | prompt | — | kinetic-type, music |
| 42 | [Spotify product film](https://prompt-motion.com/brainextends-e19ac3) | [@brainextends](https://x.com/brainextends) | 2026-09-26 | prompt | — | music |
| 43 | [Browser automation skill launch](https://prompt-motion.com/hqmank-7c61f1) | [@hqmank](https://x.com/hqmank) | 2026-09-26 | prompt | — | music, code |
| 44 | [founder.page launch video](https://prompt-motion.com/ratheejaisal-1f4538) | [@RatheeJaisal](https://x.com/RatheeJaisal) | 2026-09-26 | prompt | — | charts |
| 45 | [Alan agent platform promo](https://prompt-motion.com/prasad-pilla-2c0cba) | [@prasad_pilla](https://x.com/prasad_pilla) | 2026-09-26 | prompt | — | diagrams |
| 46 | [Tally product demo](https://prompt-motion.com/visheshbaghell-3aba37) | [@VisheshBaghell](https://x.com/VisheshBaghell) | 2026-09-26 | prompt | — | kinetic-type |
| 47 | [DistilBook product explainer](https://prompt-motion.com/sudo-kiran-6609ed) | [@sudo_kiran](https://x.com/sudo_kiran) | 2026-09-26 | prompt | — | diagrams |
| 48 | [Badge unlock screen animation](https://prompt-motion.com/bthreeagency-b9b8d9) | [@BThreeAgency](https://x.com/BThreeAgency) | 2026-09-26 | prompt | — | phone, particles |
| 49 | [AIsa API key promo](https://prompt-motion.com/0xfemyn-e114d3) | [@0xfemyn](https://x.com/0xfemyn) | 2026-09-26 | prompt | — |  |
| 50 | [Developer portfolio site showreel](https://prompt-motion.com/wani-shola-16ca7a) | [@wani_shola](https://x.com/wani_shola) | 2026-09-26 | prompt | Remotion | music |
| 51 | [Step race app promo](https://prompt-motion.com/marklaunches-3b9492) | [@marklaunches](https://x.com/marklaunches) | 2026-09-26 | prompt | — |  |
| 52 | [Bento.surf product video](https://prompt-motion.com/bizibeast-10f264) | [@bizibeast](https://x.com/bizibeast) | 2026-09-26 | prompt | — | phone |
| 53 | [Portfolio motion reel](https://prompt-motion.com/heyiammallik-e72d17) | [@heyiammallik](https://x.com/heyiammallik) | 2026-09-26 | prompt | — | kinetic-type, particles |
| 54 | [Voice agent SaaS launch](https://prompt-motion.com/fractadev-149adc) | [@FractaDev](https://x.com/FractaDev) | 2026-09-26 | prompt | — | charts |
| 55 | [Matra caption app promo](https://prompt-motion.com/gautam-mer1-2ae354) | [@gautam_mer1](https://x.com/gautam_mer1) | 2026-09-26 | prompt | Remotion, React | phone, photos |
| 56 | [Quetzal social app reel](https://prompt-motion.com/miskinho-443898) | [@miskinho_](https://x.com/miskinho_) | 2026-09-26 | prompt | — | photos |
| 57 | [Motion designer showreel](https://prompt-motion.com/danilowm-d3720d) | [@danilowm](https://x.com/danilowm) | 2026-09-26 | prompt | HyperFrames | charts, kinetic-type |
| 58 | [Email verification tool promo](https://prompt-motion.com/kmasiff-cc72cb) | [@KmAsiff](https://x.com/KmAsiff) | 2026-09-26 | prompt | — |  |
| 59 | [AllInvestView product promo](https://prompt-motion.com/rammanq-f5a90f) | [@rammanq](https://x.com/rammanq) | 2026-09-26 | prompt | — | phone, charts |
| 60 | [Amazon wholesale pitch video](https://prompt-motion.com/ceowinkz-7c776b) | [@ceowinkz](https://x.com/ceowinkz) | 2026-09-26 | prompt | — | kinetic-type |
| 61 | [Personal skills showreel](https://prompt-motion.com/ibrahimwasim240-809370) | [@ibrahimwasim240](https://x.com/ibrahimwasim240) | 2026-09-26 | prompt | — | particles, characters |
| 62 | [AgentHud project motion video](https://prompt-motion.com/jazzen-chen-4542ae) | [@Jazzen_Chen](https://x.com/Jazzen_Chen) | 2026-09-26 | prompt | — | code |
| 63 | [CloudJoi search showcase](https://prompt-motion.com/lester-tyy-f897f7) | [@lester_tyy](https://x.com/lester_tyy) | 2026-09-26 | prompt | Remotion | photos |
| 64 | [Brieform product presentation](https://prompt-motion.com/majorbaguette-fb11d7) | [@MajorBaguette](https://x.com/MajorBaguette) | 2026-09-26 | prompt | Remotion |  |
| 65 | [Enxovaly baby app promo](https://prompt-motion.com/gabrielbuzziv-4ff0c6) | [@gabrielbuzziv](https://x.com/gabrielbuzziv) | 2026-09-25 | prompt | HyperFrames | phone |
| 66 | [Distilbook product video](https://prompt-motion.com/ajith-io-c52e09) | [@ajith_io](https://x.com/ajith_io) | 2026-09-25 | prompt | — |  |
| 67 | [Dub promo video](https://prompt-motion.com/steventey-0d20e4) | [@steventey](https://x.com/steventey) | 2026-09-25 | prompt | — | charts |
| 68 | [Distilbook motion showreel](https://prompt-motion.com/itisrazak-3ad902) | [@itisRazak](https://x.com/itisRazak) | 2026-09-25 | prompt | — | kinetic-type, particles, music |
| 69 | [Sahi trading terminal reveal](https://prompt-motion.com/dale-vaz-cc612a) | [@dale_vaz](https://x.com/dale_vaz) | 2026-09-25 | prompt | JavaScript | phone, charts, particles |
| 70 | [AI Arena product promo](https://prompt-motion.com/ezshine-c90d73) | [@ezshine](https://x.com/ezshine) | 2026-09-25 | prompt | — | code |
| 71 | [Stock analysis app promo](https://prompt-motion.com/aistocksavvy-3fb9f5) | [@AIStockSavvy](https://x.com/AIStockSavvy) | 2026-09-25 | prompt | — | charts |
| 72 | [Visual guides library launch](https://prompt-motion.com/techyoutbe-945b56) | [@techyoutbe](https://x.com/techyoutbe) | 2026-09-25 | prompt | — | diagrams, code |
| 73 | [Morphing UI states loop](https://prompt-motion.com/demonugc-4c5753) | [@demonugc](https://x.com/demonugc) | 2026-09-25 | prompt | HTML, Playwright | music |
| 74 | [Supademo launch video](https://prompt-motion.com/jhylee95-e1152f) | [@jhylee95](https://x.com/jhylee95) | 2026-09-25 | prompt | — | kinetic-type, music |
| 75 | [Norilu product launch video](https://prompt-motion.com/sachaarbonel-8f14f4) | [@sachaarbonel](https://x.com/sachaarbonel) | 2026-09-25 | prompt | — |  |
| 76 | [Ren app launch video](https://prompt-motion.com/macrohou-33959d) | [@macrohou](https://x.com/macrohou) | 2026-09-25 | prompt | — | phone, charts |
| 77 | [Fitters Bible app promo](https://prompt-motion.com/adamdesgns-478d6d) | [@Adamdesgns](https://x.com/Adamdesgns) | 2026-09-25 | prompt | — | phone, diagrams |
| 78 | [Studio website showreel](https://prompt-motion.com/andginja-333d32) | [@andginja](https://x.com/andginja) | 2026-09-25 | prompt | — | photos |
| 79 | [PicTwin AI app ad](https://prompt-motion.com/l3d1c-0e35a3) | [@l3d1c](https://x.com/l3d1c) | 2026-09-25 | prompt | — | photos |
| 80 | [QuickDesign brand promo](https://prompt-motion.com/quickdesignio-dd93d0) | [@quickdesignio](https://x.com/quickdesignio) | 2026-09-25 | prompt | — | kinetic-type, music |
| 81 | [Claude self-promo spot](https://prompt-motion.com/slvdev-64c45a) | [@slvDev](https://x.com/slvDev) | 2026-09-25 | prompt | — | phone, kinetic-type |
| 82 | [DistilBook product explainer](https://prompt-motion.com/sudo-kiran-4f8b59) | [@sudo_kiran](https://x.com/sudo_kiran) | 2026-09-25 | prompt | — |  |
| 83 | [SaaS product launch video](https://prompt-motion.com/xelandre-363f00) | [@xelandre__](https://x.com/xelandre__) | 2026-09-25 | prompt | HTML/JS, Playwright, ffmpeg |  |
| 84 | [Parenting app hype video](https://prompt-motion.com/francoxavier33-d2dfd2) | [@francoxavier33](https://x.com/francoxavier33) | 2026-09-25 | prompt | Remotion | phone, kinetic-type |
| 85 | [Motion designer showreel](https://prompt-motion.com/kangaroohere-b10f8d) | [@KangarooHere](https://x.com/KangarooHere) | 2026-09-25 | prompt | — | phone, charts, kinetic-type |
| 86 | [org2html product showreel](https://prompt-motion.com/kyonax-on-tech-aabc1d) | [@kyonax_on_tech](https://x.com/kyonax_on_tech) | 2026-09-25 | prompt | — | code |
| 87 | [Gene Spectra promo](https://prompt-motion.com/madebyjmayala-b9204d) | [@madebyjmayala](https://x.com/madebyjmayala) | 2026-09-25 | prompt | — |  |
| 88 | [Commotion app showreel](https://prompt-motion.com/amol909s-27533e) | [@Amol909S](https://x.com/Amol909S) | 2026-09-25 | prompt | — | phone, code |
| 89 | [Lidlezz app promo](https://prompt-motion.com/cansincengiz-me-cf68dd) | [@cansincengiz_me](https://x.com/cansincengiz_me) | 2026-09-25 | prompt | — |  |
| 90 | [Crux motion design showreel](https://prompt-motion.com/marouanegazouzi-6071d5) | [@marouanegazouzi](https://x.com/marouanegazouzi) | 2026-09-25 | prompt | — | charts, kinetic-type, music |
| 91 | [ocrX app launch video](https://prompt-motion.com/mehul4795-4a7007) | [@mehul4795](https://x.com/mehul4795) | 2026-09-25 | prompt | — |  |
| 92 | [FigPad product promo](https://prompt-motion.com/ai-baymax-0ef9dd) | [@Ai_Baymax](https://x.com/Ai_Baymax) | 2026-09-25 | prompt | — |  |
| 93 | [Database client launch video](https://prompt-motion.com/iammxfschr-d68f90) | [@iamMXFSCHR](https://x.com/iamMXFSCHR) | 2026-09-25 | prompt | — | code |
| 94 | [Design portfolio video reel](https://prompt-motion.com/kikelopezdesign-7cc9e8) | [@kikelopezdesign](https://x.com/kikelopezdesign) | 2026-09-25 | prompt | — | phone |
| 95 | [Shape morphing through UI states](https://prompt-motion.com/twoclipping-5cba86) | [@twoclipping](https://x.com/twoclipping) | 2026-09-24 | prompt | HTML + Playwright | charts, music |
| 96 | [Tennis game launch video](https://prompt-motion.com/deifosv-04e4d3) | [@deifosv](https://x.com/deifosv) | 2026-09-24 | prompt | — | phone |
| 97 | [Five scroll-based sections](https://prompt-motion.com/ercankeskinx-ec2568) | [@ercankeskinx](https://x.com/ercankeskinx) | 2026-09-24 | prompt | — | photos |
| 98 | [Three.js Skyraider aircraft model](https://prompt-motion.com/buildfastwithai-ed9447) | [@BuildFastWithAI](https://x.com/BuildFastWithAI) | 2026-09-24 | prompt | Three.js |  |
| 99 | [Sotto reading app explainer](https://prompt-motion.com/1stnoel-c20a89) | [@1stnoel_](https://x.com/1stnoel_) | 2026-09-24 | prompt | — | phone |
| 100 | [Tented image gen product video](https://prompt-motion.com/justincooperman-e7bbc4) | [@justincooperman](https://x.com/justincooperman) | 2026-09-24 | prompt | Blender | photos |
| 101 | [UGC ad generator promo](https://prompt-motion.com/twoclipping-6dd14e) | [@twoclipping](https://x.com/twoclipping) | 2026-09-23 | prompt | HTML + Playwright | phone, photos, music |
| 102 | [Sherwood agentic hedge fund explainer](https://prompt-motion.com/imthatcarlos-e04bfe) | [@imthatcarlos](https://x.com/imthatcarlos) | 2026-09-23 | prompt | Remotion | kinetic-type, photos |
| 103 | [Datagran ChatGPT ads explainer](https://prompt-motion.com/charlesmendez-73b6e4) | [@charlesmendez](https://x.com/charlesmendez) | 2026-09-23 | prompt | — | phone, charts |
