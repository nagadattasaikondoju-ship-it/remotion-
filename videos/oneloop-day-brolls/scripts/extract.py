# Extract each B-roll shot's clean (sharp) frame range from the master video and build caption masks.
import subprocess, os, sys, numpy as np, cv2
V = sys.argv[1]; OUT = sys.argv[2]
SHOTS = [  # name, first frame, last frame (60 fps), has caption
    ("01_walk_in_title", 15, 118), ("02_gate_open", 134, 173), ("03_door_open", 194, 239),
    ("04_checking_in", 264, 359), ("05_checking_emails", 374, 475), ("06_scrum_meet", 483, 561),
    ("07_heads_down_coding", 575, 675), ("08_bro_check_this_bug", 689, 815), ("09_testing_what_we_built", 816, 955),
    ("10_wrapping_up", 956, 1169)]
W, H = 1080, 1920
def read(a, b):  # frames a..b only (one shot at a time keeps memory low)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", V, "-vf", f"select=between(n\,{a}\,{b})", "-vsync", "vfr",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
for name, a, b in SHOTS:
    d = os.path.join(OUT, name); os.makedirs(os.path.join(d, "frames"), exist_ok=True); os.makedirs(os.path.join(d, "masks"), exist_ok=True)
    fr = read(a, b); assert len(fr) == b - a + 1, (name, len(fr))
    for i, f in enumerate(fr): cv2.imwrite(os.path.join(d, "frames", f"{i:05d}.png"), f)
    hsv = [cv2.cvtColor(f, cv2.COLOR_BGR2HSV) for f in fr]
    if name.startswith("01"):
        # animated title: per-frame mask — white "A Day at" + copper "Oneloop", only inside the title zone
        masks = []
        for f, h in zip(fr, hsv):
            zone = np.zeros((H, W), bool); zone[660:1220, 20:1060] = True
            white = (h[..., 2] > 205) & (h[..., 1] < 60)
            copper = (h[..., 0] >= 5) & (h[..., 0] <= 22) & (h[..., 1] > 90) & (h[..., 2] > 70) & (h[..., 2] < 235)
            m = ((white | copper) & zone).astype(np.uint8) * 255
            m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
            masks.append(m)
        # union over a short window so faint (fading-in) strokes are covered too
        masks = np.stack(masks); out = []
        for i in range(len(masks)):
            u = masks[max(0, i - 6): i + 7].max(0)
            sh = np.roll(np.roll(u, 7, 0), 7, 1)                      # drop shadow sits down-right
            m = cv2.dilate(np.maximum(u, sh), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
            out.append(m)
    else:
        # static caption: white in every frame of the shot, inside the caption band
        band = np.zeros((H, W), bool); band[400:660, :] = True
        white_always = np.mean([(h[..., 2] > 200) & (h[..., 1] < 70) for h in hsv], axis=0) > 0.92
        core = (white_always & band).astype(np.uint8) * 255
        core = cv2.morphologyEx(core, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        sh = np.roll(np.roll(core, 8, 0), 8, 1)
        m = cv2.dilate(np.maximum(core, sh), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
        out = [m] * len(fr)
    for i, m in enumerate(out): cv2.imwrite(os.path.join(d, "masks", f"{i:05d}.png"), m)
    # preview: mask overlaid on the middle frame
    k = len(fr) // 2; pv = fr[k].copy(); pv[out[k] > 0] = (0.5 * pv[out[k] > 0] + [0, 0, 127]).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, f"maskprev_{name}.jpg"), cv2.resize(pv, (270, 480)))
    print(name, len(fr), "frames", f"{len(fr)/60:.2f}s", "mask px:", int((out[k] > 0).sum()))
