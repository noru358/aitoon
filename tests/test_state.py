from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from pipeline.state import StateError, advance, approve_editorial_review, block, init_episode, load_state, register_file_artifact, resume
from pipeline.validate import ValidationError, validate_repository

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
        state = init_episode("E001", "test", 1, self.root)
        self.assertEqual(state["stage"], "BOOTSTRAP")
        episode = self.root / "episodes" / "E001"
        (episode / "source.md").write_text("# Source draft / lock\n- Source URL: https://example.com/post\n", encoding="utf-8")
        (episode / "story.md").write_text("# Story draft / lock\n- Premise: test\n", encoding="utf-8")
        storyboard = {
            "schema_version": "1.0",
            "episode_id": "E001",
            "cover": {
                "title": "테스트",
                "visual_concept": "approved art crop",
                "strategy": "DERIVED_FROM_APPROVED_ART"
            },
            "slides": [{
                "slide_id": "S01",
                "beat": "beat",
                "state_delta": "before -> after",
                "visual_owner": "ACTION",
                "shot": "medium",
                "action": "acts",
                "expression": "neutral",
                "screen_geometry": None,
                "background_level": "NONE",
                "essential_background": [],
                "background_reason": None,
                "face_acting_intent": "neutral attention",
                "emotion_delta": "baseline",
                "continuity_in": [],
                "continuity_out": [],
                "text_safe_region": "top",
                "copy": []
            }]
        }
        (episode / "storyboard.json").write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
        state = advance("E001", "PREPRODUCTION_REVIEW", "draft review payload prepared", "Present review", self.root)
        self.assertEqual(state["stage"], "PREPRODUCTION_REVIEW")
        with self.assertRaises(StateError):
            advance("E001", "SOURCE_LOCK", "source ready", "next", self.root)
        approve_editorial_review("E001", "user approved source, dialogue, storyboard and cover", self.root)
        state = advance("E001", "SOURCE_LOCK", "approved source hash locked", "Write story lock evidence", self.root)
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
        self.assertEqual(validate_repository(self.root), ["policy", "lettering_style", "references", "calibration", "E001"])

    def test_chat_and_work_execution_modes_are_locked(self) -> None:
        policy_path = self.root / "config" / "policy.json"
        data = json.loads(policy_path.read_text(encoding="utf-8"))
        self.assertEqual(data["execution_modes"]["chat"]["strategy"], "BOUNDED_AUTONOMOUS_MULTI_TURN")
        self.assertEqual(
            data["execution_modes"]["chat"]["durable_turn_boundaries"],
            ["PREPRODUCTION_REVIEW", "BOARD_DISPATCH_READY", "ART_SEQUENCE_QC", "DONE"],
        )
        self.assertFalse(data["execution_modes"]["chat"]["continuation_token_is_approval"])
        self.assertEqual(data["execution_modes"]["work"]["strategy"], "ONE_SHOT_AFTER_EDITORIAL_APPROVAL_TO_DONE_OR_RETRYABLE_BLOCK")
        self.assertTrue(data["execution_modes"]["common"]["same_production_state_machine"])

        data["execution_modes"]["chat"]["continuation_token_is_approval"] = True
        policy_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with self.assertRaises(ValidationError):
            validate_repository(self.root)

    def test_cannot_skip_stage(self) -> None:
        init_episode("E001", "test", 4, self.root)
        with self.assertRaises(StateError):
            advance("E001", "SOURCE_LOCK", "not enough", "next", self.root)

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
