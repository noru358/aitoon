from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from pipeline.lettering import LetteringError, render_lettering
from pipeline.state import sha256_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class LetteringTests(unittest.TestCase):
    def test_render_korean_hash_bound_lettering(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            art = root / "episodes" / "E001" / "art" / "S01.png"
            font = root / "assets" / "fonts" / "NotoSansKR-Regular.woff2"
            art.parent.mkdir(parents=True)
            font.parent.mkdir(parents=True)
            Image.new("RGB", (1080, 1350), "#eadfcf").save(art)
            shutil.copy2(PROJECT_ROOT / "assets" / "fonts" / font.name, font)
            plan = {
                "schema_version": "1.0",
                "slide_id": "S01",
                "base_art": {"path": art.relative_to(root).as_posix(), "sha256": sha256_file(art)},
                "canvas": {"width": 1080, "height": 1350},
                "font": {"path": font.relative_to(root).as_posix(), "sha256": sha256_file(font)},
                "elements": [
                    {
                        "id": "speech_1",
                        "role": "SPEECH",
                        "text": "아니, 진짜 이걸 먹는다고?",
                        "box": {"x": 100, "y": 80, "width": 700, "height": 210},
                        "align": "center",
                        "font_size": 52,
                        "fill": "#111111",
                        "bubble": {
                            "fill": "#ffffff",
                            "outline": "#111111",
                            "outline_width": 5,
                            "radius": 45,
                            "padding": 35,
                            "tail_tip": {"x": 730, "y": 360}
                        }
                    }
                ]
            }
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            output = root / "final.png"
            receipt = render_lettering(plan_path, output, root)
            self.assertTrue(output.is_file())
            self.assertEqual(len(receipt["output_sha256"]), 64)
            self.assertEqual(receipt["plan_path"], "plan.json")
            self.assertEqual(receipt["output_path"], "final.png")
            with Image.open(output) as image:
                self.assertEqual(image.size, (1080, 1350))

    def test_reject_changed_base_art(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            art = root / "art.png"
            font = root / "font.ttf"
            Image.new("RGB", (1080, 1350), "white").save(art)
            shutil.copy2("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font)
            plan = {
                "schema_version": "1.0",
                "slide_id": "S01",
                "base_art": {"path": "art.png", "sha256": "0" * 64},
                "canvas": {"width": 1080, "height": 1350},
                "font": {"path": "font.ttf", "sha256": sha256_file(font)},
                "elements": []
            }
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            with self.assertRaises(LetteringError):
                render_lettering(plan_path, root / "out.png", root)


if __name__ == "__main__":
    unittest.main()
