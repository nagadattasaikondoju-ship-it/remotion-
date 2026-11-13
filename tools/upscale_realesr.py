# AI upscale (x4) for low-resolution footage, e.g. 480p WhatsApp clips, on CPU.
# Model: Real-ESRGAN "realesr-general-x4v3" (xinntao/Real-ESRGAN, BSD-3-Clause), the SRVGGNetCompact network
# written out below; weights are a plain safetensors file (no pickled code):
#   curl -L -o tools/models/realesr-general-x4v3.safetensors \
#     https://huggingface.co/OzzyGT/RealESRGAN_general_x4v3/resolve/main/model.safetensors
# Usage:
#   /usr/bin/python3 -P tools/upscale_realesr.py IN.mp4 OUT.mp4 [--ss 1.0 --to 9.5] [--scale 4] [--crf 12]
#   --scale 2 renders at 4x then downsizes (sharper than a plain 2x resize).
# Audio is dropped. The output is constant-frame-rate at the source's nominal rate: frame k sits at source time ss + k/fps.
import argparse, os, subprocess, sys, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from safetensors.torch import load_file

HERE = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = os.path.join(HERE, "models", "realesr-general-x4v3.safetensors")


class SRVGGNetCompact(nn.Module):
    def __init__(self, num_feat=64, num_conv=32, upscale=4):
        super().__init__()
        self.upscale = upscale
        body = [nn.Conv2d(3, num_feat, 3, 1, 1), nn.PReLU(num_feat)]
        for _ in range(num_conv):
            body += [nn.Conv2d(num_feat, num_feat, 3, 1, 1), nn.PReLU(num_feat)]
        body += [nn.Conv2d(num_feat, 3 * upscale * upscale, 3, 1, 1)]
        self.body = nn.Sequential(*body)
        self.up = nn.PixelShuffle(upscale)

    def forward(self, x):
        return self.up(self.body(x)) + F.interpolate(x, scale_factor=self.upscale, mode="nearest")


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate", "-of", "csv=p=0", path], text=True).strip().split(",")
    n, d = out[2].split("/")
    return int(out[0]), int(out[1]), out[2], float(n) / float(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--ss", type=float); ap.add_argument("--to", type=float)
    ap.add_argument("--scale", type=int, default=4); ap.add_argument("--crf", type=int, default=12)
    ap.add_argument("--threads", type=int, default=os.cpu_count())
    ap.add_argument("--fp32", action="store_true", help="skip bfloat16 (bf16 is ~3x faster on CPUs with AMX/AVX512-BF16)")
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    net = SRVGGNetCompact(); net.load_state_dict(load_file(WEIGHTS)); net.eval()
    net = net.to(memory_format=torch.channels_last)
    amp = torch.autocast("cpu", dtype=torch.bfloat16, enabled=not a.fp32)
    w, h, rate, fps = probe(a.src)
    cut = (["-ss", str(a.ss)] if a.ss is not None else []) + (["-to", str(a.to)] if a.to is not None else [])
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-nostdin", *cut, "-i", a.src, "-vf", f"fps={rate}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    ow, oh = (w * 4, h * 4) if a.scale == 4 else (w * a.scale // 2 * 2, h * a.scale // 2 * 2)
    vf = [] if a.scale == 4 else ["-vf", f"scale={ow}:{oh}:flags=lanczos"]
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w*4}x{h*4}", "-r", rate,
                            "-i", "-", *vf, "-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
                            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", a.dst], stdin=subprocess.PIPE)
    fsz, k, t0 = w * h * 3, 0, time.time()
    with torch.inference_mode():
        while True:
            buf = dec.stdout.read(fsz)
            if len(buf) < fsz: break
            x = torch.from_numpy(np.frombuffer(buf, np.uint8).reshape(h, w, 3).copy()).permute(2, 0, 1)[None].float() / 255
            with amp: y = net(x.contiguous(memory_format=torch.channels_last)).float()
            y = y.clamp_(0, 1)[0].permute(1, 2, 0).mul_(255).round_().byte().numpy()
            enc.stdin.write(y.tobytes()); k += 1
            if k % 24 == 0: print(f"{os.path.basename(a.dst)} {k} frames, {(time.time()-t0)/k:.2f} s/frame", file=sys.stderr, flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"{a.dst}: {k} frames at {fps:.3f} fps, {ow}x{oh}, {time.time()-t0:.0f} s")


if __name__ == "__main__":
    main()
