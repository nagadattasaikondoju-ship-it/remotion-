"""Caption map: every spoken sentence, in 2–6 word phrase cards, anchored to word timings.

Each card: (seg, first-word time, last-word end, lines, mode, opts)
  seg/time  — audio time inside that dialogue segment (see edl.SEGS), so cards follow the voice
  lines     — list of (text, cls) ; cls: "" main heavy caps, "sm" smaller support line,
              "kw" Playfair italic emotional keyword ; wrap a word in [..] for copper/terracotta emphasis
  mode      — "behind" (behind the speaker, roto-masked), "env" (pinned to a surface in B-roll),
              "lower" (clean lower phrase), "top" (above a proof screen)
  opts      — placement overrides: x, y, maxw, size, scheme ("light" cream on dark / "dark" charcoal on bright),
              t3d (CSS 3D surface angle), track (piece index for planar tracking), couple (0-1 track strength)
"""

CARDS = [
    # --- Prahalad, day lane (static tripod) ---
    (0, 0.96, 1.98, [("Our first [client]", "")], "behind", {}),
    (0, 1.98, 3.32, [("agreed to pay us", "sm"), ("[₹10,000]", "")], "behind", {"emph": True}),
    (0, 3.32, 3.78, [("for a website,", "")], "lower", {"hold_to": "paper"}),
    # "and we had just started One Loop": the newspaper match cut (3.20-4.30) carries it — every page's
    # highlighted line reads "…we had just started OneLoop…"
    (1, 6.04, 6.74, [("and that money", "")], "behind", {}),
    (1, 6.74, 7.76, [("mattered", "kw"), ("a lot to us.", "")], "behind", {"emph": True}),
    # --- Tarun, dusk (static) ---
    (2, 0.00, 1.10, [("We went to", "sm"), ("every [door]", "")], "behind", {"start_at_picture": True}),
    (2, 1.10, 1.74, [("in [Hyderabad],", "")], "behind", {}),
    (2, 1.98, 2.64, [("from small-scale", "")], "env", {"x": 540, "y": 980, "maxw": 900, "scheme": "dark",
                                                       "t3d": "perspective(1100px) rotateX(48deg)", "couple": 0.12}),
    (2, 2.64, 3.18, [("local [businesses]", "")], "env", {"x": 540, "y": 1420, "maxw": 900, "scheme": "light",
                                                         "couple": 0.15}),
    (2, 3.18, 4.20, [("to large-scale", "sm"), ("[enterprises].", "")], "env", {"x": 540, "y": 640, "maxw": 780,
                                                                          "scheme": "dark",
                                                                          "t3d": "perspective(1400px) rotateY(-14deg)",
                                                                          "couple": 0.1}),
    (3, 4.62, 5.32, [("We pitched", "sm"), ("our [idea]", "")], "env", {"x": 540, "y": 430, "maxw": 860,
                                                                   "scheme": "dark"}),
    (3, 5.32, 6.62, [("on how to develop", "sm"), ("their [business],", "")], "env", {"x": 540, "y": 400,
                                                                                 "maxw": 800, "scheme": "dark"}),
    (3, 6.85, 7.82, [("and one client", "")], "behind", {}),
    (3, 7.82, 8.76, [("said [yes]", "sm"), ("for a website.", "")], "behind", {"emph": True}),
    (4, 9.40, 10.16, [("We built", "sm"), ("the [demo]", "")], "env", {"x": 540, "y": 1290, "maxw": 820,
                                                                  "scheme": "light"}),
    (5, 10.80, 11.34, [("when we were", "sm"), ("ready", "")], "env", {"x": 540, "y": 1230, "maxw": 820,
                                                                    "scheme": "light"}),
    (5, 11.34, 12.12, [("to [publish] it.", "")], "env", {"x": 540, "y": 1230, "maxw": 860, "scheme": "light"}),
    # --- Prahalad, night (static) ---
    (6, 1.52, 2.50, [("And then", "sm"), ("the payments", "")], "behind", {"start_at_picture": True}),
    (6, 2.50, 3.14, [("[slowed down].", "")], "behind", {"emph": True}),
    (6, 3.34, 4.04, [("At the", "sm"), ("beginning,", "")], "behind", {}),
    (6, 4.26, 5.30, [("he paid us", "sm"), ("[₹1,500],", "")], "top", {"y": 330}),
    (7, 6.00, 6.98, [("and then", "sm"), ("nothing", "kw")], "behind", {"emph": True}),
    (7, 6.98, 7.32, [("happened.", "")], "behind", {}),
    # --- B-roll: the calls ---
    (8, 7.68, 9.02, [("So we tried", "sm"), ("calling [him]", "")], "env", {"x": 540, "y": 360, "maxw": 880,
                                                                       "scheme": "dark"}),
    (8, 9.02, 9.68, [("regarding", "sm"), ("[payments],", "")], "env", {"x": 540, "y": 360, "maxw": 880,
                                                                    "scheme": "dark"}),
    (8, 9.96, 10.80, [("and every", "sm"), ("[time]", "")], "env", {"x": 540, "y": 360, "maxw": 860,
                                                                 "scheme": "dark"}),
    (8, 10.80, 11.56, [("he used", "sm"), ("to say", "")], "env", {"x": 540, "y": 360, "maxw": 860,
                                                                "scheme": "dark"}),
    (8, 11.56, 12.38, [("something", "sm"), ("or the [other].", "")], "env", {"x": 300, "y": 520, "maxw": 520,
                                                                          "scheme": "dark"}),
    # --- Prahalad, night ---
    (9, 12.70, 14.16, [("So what did", "sm"), ("we do [next?]", "")], "behind", {"emph": True}),
    # --- Tarun, night (static phone) ---
    (10, 0.86, 1.98, [("You would", "sm"), ("expect us", "")], "behind", {"start_at_picture": True}),
    (10, 1.98, 2.98, [("to publish it", "sm"), ("[anyway],", "")], "behind", {}),
    (11, 3.54, 4.16, [("or to", "sm"), ("walk [away],", "")], "env", {"x": 450, "y": 430, "maxw": 760,
                                                                   "scheme": "light"}),
    (11, 4.26, 5.18, [("but we did", "sm"), ("neither.", "kw")], "behind", {"emph": True}),
    (11, 5.30, 6.30, [("We wanted to", "sm"), ("handle it", "")], "behind", {}),
    (11, 6.30, 6.95, [("professionally.", "kw")], "behind", {"emph": True}),
    (12, 7.14, 8.48, [("but that was not", "sm"), ("the same case", "")], "top", {"y": 470, "scheme": "dark",
                                                                             "start_at": "notpub"}),
    (12, 8.48, 9.28, [("from the", "sm"), ("[client's] side.", "")], "lower", {"scheme": "light"}),
    # --- Prahalad, night selfie (moving: damped head follow) ---
    (13, 10.48, 11.20, [("That was", "sm"), ("about", "")], "behind", {}),
    (13, 11.20, 12.08, [("our first", "sm"), ("[client],", "")], "behind", {}),
    (13, 12.72, 13.50, [("and", "sm"), ("thankfully", "kw")], "behind", {}),
    (13, 13.50, 14.94, [("not every client", "sm"), ("is like [that].", "")], "behind", {}),
    (13, 15.18, 16.04, [("And in", "sm"), ("[part 2],", "")], "behind", {"emph": True}),
    (13, 16.22, 16.90, [("we'll talk", "sm"), ("about", "")], "behind", {}),
    (13, 16.90, 17.72, [("some of the", "sm"), ("[best] clients", "")], "behind", {}),
    (13, 17.72, 18.50, [("we've", "sm"), ("worked with.", "")], "behind", {}),
]
END_CARD = [("Next in", "sm"), ("Part 2", "kw")]
