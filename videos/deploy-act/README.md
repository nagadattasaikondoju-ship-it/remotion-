# Deploy act — three phone takes → one reel

1080×1920 · 30 fps · 22.4 s. Build: `python3 scripts/build.py` → `renders/Deploy_Act_master_1080x1920.mp4` + `renders/Deploy_Act_share.mp4`.

## Story (as heard; the source audio is very noisy, so some words are best-effort)

| # | take | on screen | dialogue |
|---|---|---|---|
| 1 | 17:10 | both at the laptop, reviewing | "…the entire site… don't worry about it, it will look fine — you can deploy." |
| 2 | 17:16 | grey shirt explains, then both get to work | "I can see that — I can do it in five or six minutes." |
| 3 | 17:24 | grey shirt on the phone, the developer still at the laptop behind him | "Hey, hi, listen — the [website] is actually good, but I don't know what's the problem, it's failing in deployment. Can you just change the developer, please?" |

Recording order is also the story order: the review and the promise of a quick deploy set up the phone-call punchline.

## Edit
- **Cuts:** hard cuts at 8.23 s and 11.83 s, all in pauses. A 2-frame audio crossfade at each cut stops clicks.
  - Take 1 trims 0.4 s of dead head.
  - Take 2 keeps 1.4 s of them working, as a time-passing beat.
  - Take 3 keeps him dialling before "Hey, hi".
- **Noise removal:** DeepFilterNet3 at full suppression on all three takes.
  - Takes levelled to each other by EBU R128.
  - Chain: high-pass 80 Hz, small presence lift, de-esser, gentle compression.
  - Master at −14 LUFS, ≤ −1 dBTP.
  - A barely-there clean air bed 45 dB under the voice keeps the pauses from dropping into dead digital silence. The pause floor is about 40 dB under the speech.
- **Picture:** auto-rotated to 1080×1920, all takes conformed to 30 fps (take 1 was 29.97). Shared light polish: phone-noise cleanup, +4 % contrast, +6 % saturation, light sharpening.
- **Not added:** no captions, music or SFX yet. The UE SFX library isn't connected, so any SFX now would be synthesised.
