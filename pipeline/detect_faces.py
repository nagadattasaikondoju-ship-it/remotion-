"""Stage 2: per-frame face bounding boxes (run once, offline).

Output (alongside the video):
  {"width", "height", "fps", "frameCount",
   "frames": [{"f", "x", "y", "w", "h", "score", "detected"}]}
x/y/w/h are normalized 0..1 of the source frame (top-left origin).
Frames with no detection are linearly interpolated between neighbours
(detected:false) so Remotion always has a box to follow.
"""
import argparse
import json
import os
import sys

import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL = os.path.join(HERE, "models", "blaze_face_short_range.tflite")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--min-score", type=float, default=0.5)
    a = ap.parse_args()

    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
        base_options=mp_python.BaseOptions(model_asset_path=a.model),
        running_mode=vision.RunningMode.VIDEO,
        min_detection_confidence=a.min_score,
    ))

    frames, prev = [], None
    i = 0
    while True:
        ok, bgr = cap.read()
        if not ok:
            break
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        res = det.detect_for_video(img, int(round(i * 1000 / fps)))
        box = None
        if res.detections:
            # Several faces: follow the one closest to the previous box, else the largest.
            def key(d):
                b = d.bounding_box
                if prev:
                    cx, cy = (b.origin_x + b.width / 2) / W, (b.origin_y + b.height / 2) / H
                    return -((cx - prev[0]) ** 2 + (cy - prev[1]) ** 2)
                return b.width * b.height
            d = max(res.detections, key=key)
            b = d.bounding_box
            box = {"x": b.origin_x / W, "y": b.origin_y / H, "w": b.width / W, "h": b.height / H,
                   "score": d.categories[0].score}
            prev = (box["x"] + box["w"] / 2, box["y"] + box["h"] / 2)
        frames.append({"f": i, **(box or {}), "detected": box is not None})
        i += 1
    cap.release()

    # Fill gaps by interpolating between the nearest detected frames.
    known = [k for k, fr in enumerate(frames) if fr["detected"]]
    if not known:
        sys.exit("no faces detected")
    for k, fr in enumerate(frames):
        if fr["detected"]:
            continue
        lo = max((j for j in known if j < k), default=None)
        hi = min((j for j in known if j > k), default=None)
        a_, b_ = frames[lo if lo is not None else hi], frames[hi if hi is not None else lo]
        t = 0 if lo is None or hi is None else (k - lo) / (hi - lo)
        for key in ("x", "y", "w", "h"):
            fr[key] = a_[key] + (b_[key] - a_[key]) * t
        fr["score"] = 0
    for fr in frames:
        for key in ("x", "y", "w", "h", "score"):
            fr[key] = round(fr[key], 4)

    json.dump({"source": os.path.basename(a.video), "width": W, "height": H, "fps": fps,
               "frameCount": len(frames), "frames": frames}, open(a.out, "w"), separators=(",", ":"))
    print(f"{len(known)}/{len(frames)} frames with a face -> {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
