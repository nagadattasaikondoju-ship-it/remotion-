# Picture: footage + text + logo in one pass -> out/picture.mp4 (1080x1920, 60 fps, no audio). The footage is encoded once (CRF 8);
# the MASTER is this file untouched.
#   /usr/bin/python3 -P picture.py                 full render
#   /usr/bin/python3 -P picture.py --stills 1 5.2  QA stills -> out/stills/t_<t>.png (no encode)
# Every shot is the Sony original's own frame, turned upright: exactly 1080x1920, shown 1:1 (no zoom, crop, upscale or sharpening).
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, "out", "edit.json"))); FPS = E["fps"]; W, H = 1080, 1920
GRADE = {  # warm and a touch brighter, like the rest of the kennel films; "warm_in" lifts the dimmer indoor clips
    "warm": "eq=contrast=1.03:saturation=1.07,colorbalance=rm=0.025:bm=-0.02:rh=0.015",
    "warm_in": "eq=brightness=0.03:contrast=1.02:saturation=1.05:gamma=1.05,colorbalance=rm=0.025:bm=-0.02:rh=0.015",
}
# One Loop brand: cream text, copper accent, Instrument Serif italic + Almarai (the website's fonts)
CREAM, COPPER = (247, 232, 218), (229, 156, 105)
F = lambda n, s: ImageFont.truetype(os.path.join(HERE, "fonts", n), s)
SERIF, SANS = "InstrumentSerif-Italic.ttf", "Almarai-ExtraBold.ttf"
OVERLINE = {"we just signed\na new client": "POV", "meet the team": "OUR NEW CLIENT", "now let's make\nthem famous": "ONE LOOP"}

def tracked(d, xy, text, font, fill, track):  # letter-spaced caps, centred on xy
    w = sum(font.getlength(c) for c in text) + track * (len(text) - 1); x = xy[0] - w / 2
    for c in text: d.text((x, xy[1]), c, font=font, fill=fill, anchor="lm"); x += font.getlength(c) + track

def block(lines, size, over=None, over_size=30):
    """Render a text block (optional copper overline + cream serif lines) to a tight RGBA image with a soft shadow."""
    f = F(SERIF, size); lh = round(size * 1.02); pad = 40
    widths = [f.getlength(l) for l in lines]; bw = int(max(widths + [600])) + 2 * pad
    oh = round(over_size * 2.2) if over else 0; bh = oh + lh * len(lines) + 2 * pad
    im = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if over: tracked(d, (bw / 2, pad + over_size * 0.6), over, F(SANS, over_size), COPPER + (255,), over_size * 0.32)
    for k, l in enumerate(lines): d.text((bw / 2, pad + oh + lh * k + lh / 2), l, font=f, fill=CREAM + (255,), anchor="mm")
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel("A").point(lambda a: int(a * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 4)); out.alpha_composite(im); return out

def gradient(top):  # dark scrim behind the text so it reads over any footage
    g = Image.new("L", (1, H)); px = g.load()
    for y in range(H):
        u = (1 - y / 900) if top else (y - 1080) / (H - 1080)
        px[0, y] = int((200 if top else 150) * max(0, min(1, u)) ** (1.1 if top else 1.4))
    a = g.resize((W, H)); im = Image.new("RGBA", (W, H), (8, 6, 5, 0)); im.putalpha(a); return im
SCRIM = {True: gradient(True), False: gradient(False)}

LOGO = Image.open(os.path.join(HERE, "logo.png")).convert("RGB")
LOGO = LOGO.resize((760, round(LOGO.height * 760 / LOGO.width)), Image.LANCZOS)

# text blocks: one per run of shots with the same text; (layer, centre y, top-scrim?)
_cache = {}
def layer_for(sh):
    key = (sh["kind"], sh["text"])
    if key not in _cache:
        lines = sh["text"].split("\n"); k = sh["kind"]
        if k == "hook": _cache[key] = (block(lines, 112, OVERLINE.get(sh["text"])), 420, True)
        elif k == "big": _cache[key] = (block(lines, 132, OVERLINE.get(sh["text"])), 1430, False)
        elif k == "role": _cache[key] = (block(lines, 124, "MEET THE TEAM"), 1430, False)
        elif k == "burst": _cache[key] = (block(lines, 132), 1450, False)
        else: _cache[key] = (block(lines, 104), 1290, None)
    return _cache[key]

def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3

def text_start(i):  # a text that carries over several shots (the burst) animates in only once
    s = E["shots"]; j = i
    while j > 0 and s[j - 1]["text"] == s[i]["text"]: j -= 1
    return s[j]["start"]

# privacy: the laptop shot shows the browser's tabs and bookmarks (a client's site name among them). A blurred band follows
# that strip as the camera pulls back: (seconds into the shot, band centre y), band 300 px tall.
BLUR = {"MVI_0727.mp4": [(0.0, 300), (0.5, 345), (1.0, 445), (1.6, 520), (2.2, 585)]}
_band_mask = Image.new("L", (W, 300), 0); ImageDraw.Draw(_band_mask).rectangle((0, 40, W, 260), fill=255)
_band_mask = _band_mask.filter(ImageFilter.GaussianBlur(18))
def blur_band(fr, keys, tt):
    for (t0, y0), (t1, y1) in zip(keys, keys[1:]):
        if tt <= t1: cy = y0 + (y1 - y0) * max(0, (tt - t0)) / (t1 - t0); break
    else: cy = keys[-1][1]
    top = int(cy - 150); band = fr.crop((0, top, W, top + 300)).filter(ImageFilter.GaussianBlur(26))
    fr.paste(band, (0, top), _band_mask)

def compose(fr, sh, i, t):
    k = os.path.basename(sh["src"] or "")
    if k in BLUR: blur_band(fr, BLUR[k], t - sh["start"])
    lay, cy, top = layer_for(sh); u = ease((t - text_start(i) - 0.06) / 0.38)
    if top is not None: fr.alpha_composite(SCRIM[top])
    if u > 0:
        im = lay if u >= 1 else lay.copy()
        if u < 1: im.putalpha(im.getchannel("A").point(lambda a: int(a * u)))
        fr.alpha_composite(im, (round((W - lay.width) / 2), round(cy - lay.height / 2 + 26 * (1 - u))))
    return fr

def end_card(t, sh):
    fr = Image.new("RGB", (W, H)); u = ease((t - sh["start"]) / 0.6); s = 0.94 + 0.06 * u
    lg = LOGO.resize((round(LOGO.width * s), round(LOGO.height * s)), Image.LANCZOS) if u < 1 else LOGO
    lg = Image.eval(lg, lambda v: int(v * u)) if u < 1 else lg
    fr.paste(lg, ((W - lg.width) // 2, 760 - lg.height // 2)); fr = fr.convert("RGBA")
    lay, cy, _ = layer_for(sh); v = ease((t - sh["start"] - 0.45) / 0.45)
    if v > 0:
        im = lay.copy(); im.putalpha(im.getchannel("A").point(lambda a: int(a * v)))
        fr.alpha_composite(im, (round((W - lay.width) / 2), round(cy - lay.height / 2 + 20 * (1 - v))))
    return fr.convert("RGB")

def frames(sh, n, start_offset=0.0):
    vf = f"transpose=2,fps={FPS},{GRADE[sh['grade']]}"
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{sh['in'] + start_offset:.3f}", "-i", sh["src"], "-t", f"{n / FPS + 0.2:.3f}",
                          "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    last = None
    for _ in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) == W * H * 3: last = Image.frombytes("RGB", (W, H), b)
        if last is None: raise SystemExit(f"no frames: {sh['src']}")
        yield last
    p.kill(); p.wait()

def frame_at(t):
    i = max(k for k, s in enumerate(E["shots"]) if s["start"] <= t + 1e-6); sh = E["shots"][i]
    if sh["src"] is None: return end_card(t, sh)
    img = next(frames(sh, 1, t - sh["start"]))
    return compose(img.convert("RGBA"), sh, i, t).convert("RGB")

def main():
    if "--stills" in sys.argv:
        os.makedirs(os.path.join(HERE, "out", "stills"), exist_ok=True)
        for t in map(float, sys.argv[sys.argv.index("--stills") + 1:]): frame_at(t).save(os.path.join(HERE, "out", "stills", f"t_{t}.png"))
        return
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "8", "-tune", "film",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", os.path.join(HERE, "out", "picture.mp4")],
                           stdin=subprocess.PIPE)
    total = 0
    for i, sh in enumerate(E["shots"]):
        n = sh["f1"] - sh["f0"]
        if sh["src"] is None:
            for k in range(n): enc.stdin.write(end_card(sh["start"] + k / FPS, sh).tobytes())
        else:
            for k, img in enumerate(frames(sh, n)):
                enc.stdin.write(compose(img.convert("RGBA"), sh, i, sh["start"] + k / FPS).convert("RGB").tobytes())
        total += n; print(f"{sh['start']:6.2f} {os.path.basename(sh['src'] or 'end card'):13s} {n} frames", flush=True)
    enc.stdin.close(); enc.wait(); print(f"out/picture.mp4: {total} frames ({total / FPS:.2f} s)")

if __name__ == "__main__": main()
