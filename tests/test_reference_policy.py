from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from pipeline.validate import ValidationError, validate_reference_registry

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ReferencePolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(PROJECT_ROOT / "references", self.root / "references")
        (self.root / "calibration").mkdir()
        shutil.copytree(
            PROJECT_ROOT / "calibration" / "references",
            self.root / "calibration" / "references",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_user_designated_unverified_reference_is_production_eligible(self) -> None:
        validate_reference_registry(self.root)

    def test_generated_art_cannot_be_primary_style(self) -> None:
        path = self.root / "references" / "registry.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["assets"][0]["source_kind"] = "AI_GENERATED_APPROVED"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate_reference_registry(self.root)


if __name__ == "__main__":
    unittest.main()
