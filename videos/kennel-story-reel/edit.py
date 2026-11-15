# "to them, you're their whole book": the kennel dogs story reel. One table drives picture, captions and sound.
#   python3 edit.py -> out/edit.json
# Everything is timed to the reference reel (the user's 43.6 s recording): its shot cuts and caption changes were measured
# frame by frame, and the voiceover is the reference's own audio. Layout = the reference's: a 1.15:1 picture box on black,
# one small lowercase italic caption under it.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SRC_DIR", "/tmp/claude-0/-home-user-remotion-/b8e0fea9-ddb3-5f50-9983-de131f1aa53e/scratchpad/drv2")
FPS, DUR = 60, 43.61
BOX = (35, 546, 1010, 876)        # x, y, w, h in the 1080x1920 frame (reference: x 14-509, y 268-697 of a 510x942 recording)

# (start, source, in-point, crop top y0 in the upright 1080x1920 frame, grade, what it shows)
#  sources: "k:" kennel shoot original (Sony, rotated upright), "o:" One Loop B-roll original, "r:" reference element (box-sized)
SHOTS = [
 (0.00,  "k:MVI_0812", 1.60, 600, "warm", "Mastiff puppy in its crate turns and looks at us through the bars (box fades in at 0.25)"),
 (5.67,  "k:MVI_0794", 7.30, 600, "warm_in", "Maltese trots up and looks up at you"),
 (6.87,  "k:MVI_0799", 18.45, 350, "warm_in", "cheek to cheek: a hug with the Maltese"),
 (8.70,  "k:MVI_0808", 1.35, 500, "warm", "Shih Tzu lying still, looking at you, then away"),
 (10.37, "k:MVI_0816", 1.45, 700, "warm", "the black Cane Corso walks across the yard"),
 (12.23, "k:MVI_0800", 0.55, 200, "warm_in", "sleepy Maltese, face cradled in a hand"),
 (13.93, "k:MVI_0832", 7.35, 420, "warm", "a young man crouches to pet a Mastiff puppy lying in the sun"),
 (17.10, "r:ref_flash", 0.05, 0, "none", "the reference's warm light-leak flash (no dog, no person)"),
 (17.43, "o:MVI_0719", 0.85, 430, "warm", "One Loop B-roll: a hand writing in a diary"),
 (18.60, "o:MVI_0432", 5.60, 500, "warm", "One Loop B-roll: on a call at the laptop"),
 (20.53, "k:MVI_0805", 0.20, 850, "warm", "Shih Tzu waiting at the foot of the stairs, looks up at the camera"),
 (22.47, "k:MVI_0826", 0.00, 300, "warm", "Shih Tzus crowd the railing for treats, tails going"),
 (25.03, "k:MVI_0809", 8.25, 600, "warm", "fawn Cane Corso sitting quietly under the trees"),
 (28.60, "r:ref_floor", 0.00, 0, "none", "the reference's empty floor (AI-upscaled; no dog, no person)"),
 (30.57, "k:MVI_0819", 7.30, 700, "warm", "a man plays with a black dog and a little white dog in a cone"),
 (33.60, "k:MVI_0834", 7.30, 400, "warm", "dinner time: a black Labrador and a cream Cane Corso eat side by side"),
 (35.83, "k:MVI_0779", 18.00, 800, "warm", "a Saint Bernard ambles along its run"),
 (37.13, "k:MVI_0798", 14.90, 400, "warm_in", "the Maltese's nose right up to the lens"),
 (39.93, None, 0, 0, None, "black, :)"),
]
# captions, verbatim from the reference (its quotes and its ".." kept), with the measured change times
CAPS = [
 (0.57, "there's a very famous saying"), (2.53, "\"to you,"), (3.23, "your pet is just a small chapter of your life"),
 (5.67, "but to them,"), (6.87, "you're their whole book\""), (8.70, "that hits really hard"),
 (10.37, "because they don't get decades like we do"), (12.23, "they just get a few short years"),
 (13.93, "and they spend every single one of them,"), (16.23, "loving you.."), (17.10, None),
 (17.43, "we get busy,"), (18.60, "caught up with work and life,"), (20.53, "but there they are,"), (21.50, "waiting by the door,"),
 (22.47, "tail wagging like nothing has changed"), (25.03, "one day you'll look around"),
 (26.17, "and the house will feel a little too quiet"), (28.60, "the floor a little too clean"),
 (30.57, "and you'll wish you had sat down"), (31.77, "more often just to play with them"),
 (33.57, "because to you, they were just a part of your life"), (35.83, "but to them,"),
 (37.13, "you were their whole damn universe."), (39.93, None),
]

def path(src):
    kind, name = src.split(":")
    return {"k": f"{SRC}/orig/{name}.mp4", "o": f"{SRC}/ol/{name}.mp4", "r": f"{SRC}/up/{name}.mp4"}[kind]

def main():
    shots = []
    for (a, src, i, y0, grade, note), b in zip(SHOTS, [s[0] for s in SHOTS[1:]] + [DUR]):
        shots.append({"start": a, "dur": round(b - a, 4), "src": path(src) if src else None, "kind": src.split(":")[0] if src else "black",
                      "in": i, "y0": y0, "grade": grade, "note": note})
    caps = [{"start": a, "end": b, "text": t} for (a, t), (b, _) in zip(CAPS, CAPS[1:] + [(DUR, None)]) if t]
    out = {"fps": FPS, "duration": DUR, "box": BOX, "shots": shots, "captions": caps, "smile": [39.93, DUR]}
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "out", "edit.json"), "w"), indent=1, ensure_ascii=False)
    for s in shots: print(f"{s['start']:6.2f} {s['dur']:5.2f} {os.path.basename(s['src'] or '-'):14s} {s['note']}")

if __name__ == "__main__": main()
