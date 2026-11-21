#!/usr/bin/env python3
"""Download the pinned local models that boring-tools uses.

Normal video work makes no network requests. Run this setup command once before
you disconnect the machine:

    python3 scripts/download-models.py

Each download uses a fixed HTTPS URL and a pinned SHA-256 digest. A partial or
wrong file never replaces a verified cache file.
"""
import argparse
import hashlib
import os
import sys
import urllib.request
from pathlib import Path


CACHE_ROOT = Path(os.environ.get(
    "BORING_TOOLS_MODEL_DIR", Path.home() / ".cache" / "boring-tools"))

MODELS = {
    "whisper": {
        "url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin",
        "path": CACHE_ROOT / "whisper" / "ggml-small.en.bin",
        "sha256": "c6138d6d58ecc8322097e0f987c32f1be8bb0a18532a3f88f734d1bbf9c41e5d",
        "size": 487_614_201,
    },
    "face": {
        "url": ("https://storage.googleapis.com/mediapipe-models/face_detector/"
                "blaze_face_short_range/float16/1/blaze_face_short_range.tflite"),
        "path": CACHE_ROOT / "vision" / "blaze_face_short_range.tflite",
        "sha256": "b4578f35940bf5a1a655214a1cce5cab13eba73c1297cd78e1a04c2380b0152f",
        "size": 229_746,
    },
    "eyeline": {
        "url": ("https://storage.googleapis.com/mediapipe-models/face_landmarker/"
                "face_landmarker/float16/1/face_landmarker.task"),
        "path": CACHE_ROOT / "vision" / "face_landmarker.task",
        "sha256": "64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff",
        "size": 3_758_596,
    },
}


def digest(path):
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def download(name, force=False):
    spec = MODELS[name]
    path = spec["path"]
    if path.exists() and digest(path) == spec["sha256"]:
        print(f"{name}: verified {path}")
        return
    if path.exists() and not force:
        raise RuntimeError(f"{name}: {path} failed its digest; rerun with --force")

    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".part")
    partial.unlink(missing_ok=True)
    print(f"{name}: downloading {spec['size'] / 1_000_000:.1f} MB -> {path}")
    try:
        request = urllib.request.Request(spec["url"], headers={"User-Agent": "boring-tools/1"})
        with urllib.request.urlopen(request) as response, open(partial, "wb") as handle:  # nosec B310
            done = 0
            while chunk := response.read(1024 * 1024):
                handle.write(chunk)
                done += len(chunk)
                if spec["size"] > 20_000_000 and done % (50 * 1024 * 1024) < len(chunk):
                    print(f"  {done / 1_000_000:.0f} MB", file=sys.stderr)
        if partial.stat().st_size != spec["size"]:
            raise RuntimeError(
                f"{name}: expected {spec['size']} bytes, got {partial.stat().st_size}")
        actual = digest(partial)
        if actual != spec["sha256"]:
            raise RuntimeError(f"{name}: SHA-256 mismatch: {actual}")
        os.replace(partial, path)
    except Exception:
        partial.unlink(missing_ok=True)
        raise
    print(f"{name}: verified {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Download pinned models for offline boring-tools use")
    parser.add_argument("models", nargs="*", choices=sorted(MODELS),
                        help="models to download; default: all")
    parser.add_argument("--force", action="store_true",
                        help="replace an existing file that fails verification")
    args = parser.parse_args()
    for name in args.models or MODELS:
        download(name, args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
