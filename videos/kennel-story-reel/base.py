# Picture: the reference's layout. Black 1080x1920 frame, one picture box (rounded corners), every shot at native resolution:
# the box is 1010x876, cut as a 1080x936 window straight out of the upright 1080x1920 Sony frame and scaled down 0.935x,
# so nothing is ever enlarged (no softness from zooming). The captions are drawn here too, so the footage is compressed once
# (out/picture.mp4 is the master picture; assemble.sh only adds the sound to it).   -> out/picture.mp4 (60 fps, no audio)
#   /usr/bin/python3 -P base.py
import json, os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, "out", "edit.json"))); FPS = E["fps"]; W, H = 1080, 1920
BX, BY, BW, BH = E["box"]
GRADE = {  # a soft, warm, natural look like the reference; "warm_in" lifts the dimmer indoor clips a touch
    "warm": "eq=contrast=1.02:saturation=1.05,colorbalance=rm=0.025:bm=-0.02:rh=0.015",
    "warm_in": "eq=brightness=0.03:contrast=1.02:saturation=1.04:gamma=1.05,colorbalance=rm=0.025:bm=-0.02:rh=0.015",
    "none": "null",
}
# corner radius measured on the reference (its bright flash frame, all four corners, sub-pixel edge): a circular arc of r = 18.3 px
# on its 510 px-wide recording = 39 px here
RADIUS = 39
mask = Image.new("L", (BW * 4, BH * 4), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, BW * 4 - 1, BH * 4 - 1), radius=RADIUS * 4, fill=255)
mask = mask.resize((BW, BH), Image.LANCZOS)

# ---- captions (the reference's style): small white lowercase italic line under the box; an orange ":)" at the end ----
FONT = os.path.join(HERE, "fonts", "NunitoSans-Italic.ttf"); CAP_Y = 1459
def font(size):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([600, 100, 12, 500]); return f
_f40 = font(40); CAP_SIZE = round(40 * 576 / _f40.getlength("your pet is just a small chapter of your life"))   # 576 px wide, as in the reference
_cap = {}
def caption_layer(text, smile=False):
    key = (text, smile)
    if key not in _cap:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        if text:
            f = font(CAP_SIZE); sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(sh).text((W / 2, CAP_Y + 2), text, font=f, fill=(0, 0, 0, 150), anchor="mm")
            layer = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)), layer); d = ImageDraw.Draw(layer)
            d.text((W / 2, CAP_Y), text, font=f, fill=(244, 244, 242, 255), anchor="mm")
        if smile: d.text((W / 2, 985), ":)", font=font(60), fill=(238, 138, 62, 255), anchor="mm")
        _cap[key] = layer
    return _cap[key]
def overlay_at(t):
    c = next((c["text"] for c in E["captions"] if c["start"] <= t < c["end"]), None)
    return caption_layer(c, t >= E["smile"][0]) if (c or t >= E["smile"][0]) else None

def frames(sh, n):
    if sh["kind"] in ("k", "o"):   # Sony originals are stored landscape: rotate upright, cut the box window, scale down
        vf = f"transpose=2,crop=1080:936:0:{sh['y0']},fps={FPS},scale={BW}:{BH}:flags=lanczos,{GRADE[sh['grade']]}"   # no sharpening: the downscale keeps it crisp
    else:                           # reference elements are already box-sized
        vf = f"fps={FPS},scale={BW}:{BH}:flags=lanczos"
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{sh['in']:.3f}", "-i", sh["src"], "-t", f"{n / FPS + 0.2:.3f}",
                          "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        b = p.stdout.read(BW * BH * 3)
        if len(b) == BW * BH * 3: last = Image.frombytes("RGB", (BW, BH), b)
        if last is None: raise SystemExit(f"no frames: {sh['src']}")
        yield last
    p.kill(); p.wait()

def main():
    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "8", "-tune", "film",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", os.path.join(HERE, "out", "picture.mp4")],
                           stdin=subprocess.PIPE)
    black = Image.new("RGB", (W, H)); total = 0
    for sh in E["shots"]:
        n = round((sh["start"] + sh["dur"]) * FPS) - round(sh["start"] * FPS)
        if sh["kind"] == "black":
            for k in range(n):
                fr = black.copy(); ov = overlay_at(sh["start"] + k / FPS)
                if ov: fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")
                enc.stdin.write(fr.tobytes())
        else:
            for k, img in enumerate(frames(sh, n)):
                t = sh["start"] + k / FPS; fr = black.copy()
                a = min(1, max(0, (t - 0.25) / 0.30)) if sh["start"] == 0 else 1.0   # the box fades in from black at the top
                m = mask if a >= 1 else mask.point(lambda v: int(v * a))
                fr.paste(img, (BX, BY), m); ov = overlay_at(t)
                if ov: fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")
                enc.stdin.write(fr.tobytes())
        total += n; print(f"{sh['start']:6.2f} {os.path.basename(sh['src'] or 'black'):14s} {n} frames", flush=True)
    enc.stdin.close(); enc.wait(); print(f"out/picture.mp4: {total} frames ({total / FPS:.2f} s)")

if __name__ == "__main__": main()
