from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from pipeline.state import StateError, advance, block, init_episode, load_state, register_file_artifact, resume
from pipeline.validate import validate_repository

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class StateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(PROJECT_ROOT / "config", self.root / "config")
        shutil.copytree(PROJECT_ROOT / "templates", self.root / "templates")
        shutil.copytree(PROJECT_ROOT / "calibration", self.root / "calibration")
        shutil.copytree(PROJECT_ROOT / "references", self.root / "references")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_init_advance_block_resume_and_validate(self) -> None:
        state = init_episode("E001", "test", 4, self.root)
        self.assertEqual(state["stage"], "BOOTSTRAP")
        state = advance("E001", "SOURCE_LOCK", "source.md contains a URL", "Write story.md", self.root)
        self.assertEqual(state["stage"], "SOURCE_LOCK")
        state = block(
            "E001",
            "WAITING_INCLUDED_IMAGE_CAPACITY",
            "built-in image limit reached",
            "Dispatch unchanged B01 when capacity returns",
            self.root,
        )
        self.assertEqual(state["run_status"], "BLOCKED_RETRYABLE")
        state = resume("E001", "built-in image capability is available", self.root)
        self.assertEqual(state["run_status"], "ACTIVE")
        self.assertIsNone(state["blocked"])
        self.assertEqual(validate_repository(self.root), ["policy", "references", "calibration", "E001"])

    def test_cannot_skip_stage(self) -> None:
        init_episode("E001", "test", 4, self.root)
        with self.assertRaises(StateError):
            advance("E001", "STORY_LOCK", "not enough", "next", self.root)

    def test_artifact_is_hash_bound_and_path_is_immutable(self) -> None:
        init_episode("E001", "test", 4, self.root)
        artifact_path = self.root / "episodes" / "E001" / "source-evidence.txt"
        artifact_path.write_text("one", encoding="utf-8")
        first = register_file_artifact("E001", "SOURCE_EVIDENCE", artifact_path, root=self.root)
        self.assertEqual(len(first["sha256"]), 64)
        artifact_path.write_text("two", encoding="utf-8")
        with self.assertRaises(StateError):
            register_file_artifact("E001", "SOURCE_EVIDENCE", artifact_path, root=self.root)


if __name__ == "__main__":
    unittest.main()
