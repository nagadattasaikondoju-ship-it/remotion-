import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clip_rank = load_script("clip_rank", "scripts/clip_rank.py")
        cls.wall_graphics = load_script("wall_graphics", "scripts/wall-graphics.py")

    def test_clip_cut_uses_an_argument_list(self):
        video = "/videos/a file'; touch never"
        out = "/videos/out file.mp4"
        candidate = {"start": 1.2, "end": 4.8}
        args = self.clip_rank.ffmpeg_args(video, candidate, out)
        self.assertIsInstance(args, list)
        self.assertIn(video, args)
        self.assertEqual(args[-1], out)
        self.assertNotIn("shell", self.clip_rank.ffmpeg_cmd(video, candidate, out))

    def test_subject_edge_falls_back_on_invalid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            edge = Path(tmp) / "edge.tsv"
            edge.write_text("#max\tnot-a-number\n", encoding="utf-8")
            self.assertEqual(self.wall_graphics.read_edge_max(edge, 1200), 1200)
            edge.write_text("#max\t1337\n", encoding="utf-8")
            self.assertEqual(self.wall_graphics.read_edge_max(edge, 1200), 1337)

    def test_every_python_cli_has_help(self):
        scripts = [ROOT / "verify.py", *sorted((ROOT / "scripts").glob("*.py"))]
        for script in scripts:
            with self.subTest(script=script.name):
                result = subprocess.run(
                    [sys.executable, str(script), "--help"],
                    capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout.lower())

    def test_empty_word_transcript_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            transcript = Path(tmp) / "empty.json"
            transcript.write_text(json.dumps({"transcription": []}), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/word-spans.py"),
                 str(transcript), str(Path(tmp) / "missing.wav")],
                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no transcript words found", result.stderr)

    def test_broll_output_can_be_rebuilt_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.tsv"
            plan.write_text("# empty plan\n", encoding="utf-8")
            out = Path(tmp) / "frames"
            command = [sys.executable, str(ROOT / "scripts/broll-screens.py"),
                       str(plan), "8", "8", "30", "2", str(out)]
            subprocess.run(command, check=True, capture_output=True)
            subprocess.run(command, check=True, capture_output=True)
            self.assertTrue((out / "br000000.png").exists())
            self.assertTrue((out / "br000001.png").exists())

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                         "ffmpeg and ffprobe are required")
    def test_verify_accepts_a_synthetic_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            render = Path(tmp) / "render.mp4"
            subprocess.run([
                "ffmpeg", "-nostdin", "-v", "error", "-y",
                "-f", "lavfi", "-i", "color=c=black:s=320x240:r=30:d=1",
                "-f", "lavfi", "-i", "sine=frequency=1000:sample_rate=48000:duration=1",
                "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-movflags", "+faststart", str(render),
            ], check=True)
            result = subprocess.run(
                [sys.executable, str(ROOT / "verify.py"), str(render)],
                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("all PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
