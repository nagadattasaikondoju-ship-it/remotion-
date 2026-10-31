# Remove burned-in captions from one shot (band crop) with a motion-aligned clean plate.
#   1. align every frame to the middle frame (ECC, affine, caption pixels excluded)
#   2. clean plate = per-pixel median of every frame's uncovered pixels, warped into the reference frame
#   3. pixels never uncovered in the shot: OpenCV xphoto FSR inpainting on the plate (done once → no flicker)
#   4. each frame: masked pixels ← plate warped back into that frame, feathered edge
# usage: clean.py <shot dir> [plate|frame]
import os, sys, glob, numpy as np, cv2
D = sys.argv[1]; MODE = sys.argv[2] if len(sys.argv) > 2 else "plate"
fr = [cv2.imread(f) for f in sorted(glob.glob(os.path.join(D, "band_frames", "*.png")))]
mk = [cv2.imread(f, 0) > 127 for f in sorted(glob.glob(os.path.join(D, "band_masks", "*.png")))]
n = len(fr); H, W = fr[0].shape[:2]; ref = n // 2; s = 0.5
small = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), None, fx=s, fy=s).astype(np.float32) for f in fr]
smask = [(cv2.resize((~m).astype(np.uint8) * 255, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)) for m in mk]

def ecc(j):  # affine mapping frame-j coordinates → reference-frame coordinates (full resolution)
    if j == ref: return np.eye(2, 3, dtype=np.float32)
    A = np.eye(2, 3, dtype=np.float32)
    try:
        _, A = cv2.findTransformECC(small[ref], small[j], A, cv2.MOTION_AFFINE,
                                    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5), smask[ref], 5)
    except cv2.error:
        A = np.eye(2, 3, dtype=np.float32)
    A = A.copy(); A[:, 2] /= s
    return cv2.invertAffineTransform(A)  # ECC gives ref→j sampling map; invert to warp j into ref
A = [ecc(j) for j in range(n)]
flags = cv2.INTER_LINEAR

# clean plate in reference coordinates
stack, valid = [], []
for j in range(n):
    w = cv2.warpAffine(fr[j], A[j], (W, H), flags=flags, borderMode=cv2.BORDER_CONSTANT)
    ok = cv2.warpAffine((~mk[j]).astype(np.uint8), A[j], (W, H), flags=cv2.INTER_NEAREST, borderValue=0) > 0
    ok &= cv2.warpAffine(np.ones((H, W), np.uint8), A[j], (W, H), flags=cv2.INTER_NEAREST, borderValue=0) > 0
    stack.append(w); valid.append(ok)
stack = np.stack(stack).astype(np.float32); valid = np.stack(valid)
need = np.zeros((H, W), bool)
for j in range(n): need |= cv2.warpAffine(mk[j].astype(np.uint8), A[j], (W, H), flags=cv2.INTER_NEAREST) > 0
plate = fr[ref].astype(np.float32).copy()
st = np.where(valid[..., None], stack, np.nan)
med = np.nanmedian(st[:, need], axis=0) if need.any() else None
seen = valid[:, need].any(0)
vals = plate[need]; vals[seen] = med[seen]; plate[need] = vals
hole = np.zeros((H, W), bool); idx = np.argwhere(need); hole[idx[~seen, 0], idx[~seen, 1]] = True
plate = np.clip(plate, 0, 255).astype(np.uint8)
if hole.any():
    hole_d = cv2.dilate(hole.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    out = np.zeros_like(plate)
    cv2.xphoto.inpaint(plate, (~hole_d).astype(np.uint8) * 255, out, cv2.xphoto.INPAINT_FSR_FAST)
    plate[hole_d] = out[hole_d]
cv2.imwrite(os.path.join(D, "plate.png"), plate)
print(os.path.basename(D.rstrip('/')), f"frames {n}  caption px {int(need.sum())}  never-uncovered {int(hole.sum())} ({100*hole.sum()/max(1,need.sum()):.0f}%)")

# put the plate back under each frame's caption
od = os.path.join(D, "band_clean"); os.makedirs(od, exist_ok=True)
for j in range(n):
    inv = cv2.invertAffineTransform(A[j])
    back = cv2.warpAffine(plate, inv, (W, H), flags=flags, borderMode=cv2.BORDER_REFLECT)
    a = cv2.GaussianBlur(cv2.dilate(mk[j].astype(np.uint8) * 255, np.ones((5, 5), np.uint8)), (0, 0), 3).astype(np.float32)[..., None] / 255
    o = fr[j].astype(np.float32) * (1 - a) + back.astype(np.float32) * a
    cv2.imwrite(os.path.join(od, f"{j:05d}.png"), np.clip(o, 0, 255).astype(np.uint8))
