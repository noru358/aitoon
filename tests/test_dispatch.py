from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from pipeline.dispatch import DispatchError, compile_master_board_dispatch
from pipeline.state import advance, approve_editorial_review, init_episode, sha256_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DispatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(PROJECT_ROOT / "config", self.root / "config")
        shutil.copytree(PROJECT_ROOT / "templates", self.root / "templates")
        init_episode("E001", "test", 1, self.root)
        reference = self.root / "assets" / "refs" / "human.png"
        reference.parent.mkdir(parents=True)
        reference.write_bytes(b"reference-bytes")
        visual = {
            "schema_version": "1.0",
            "episode_id": "E001",
            "status": "LOCKED",
            "references": [
                {
                    "path": reference.relative_to(self.root).as_posix(),
                    "sha256": sha256_file(reference),
                    "role": "HUMAN_STYLE",
                    "allowed_influence": "line and flat color language",
                    "forbidden_inference": "identity, pose, story, clothing"
                }
            ],
            "characters": [],
            "palette": ["muted flat color"],
            "line_grammar": ["simple black hand line"],
            "shape_grammar": [],
            "style_match_dimensions": ["LINE_GRAMMAR", "EYE_FACE_GRAMMAR", "DETAIL_BUDGET"],
            "reject_traits": ["glossy generic anime"]
        }
        (self.root / "episodes" / "E001" / "visual_packet.json").write_text(
            json.dumps(visual), encoding="utf-8"
        )
        storyboard = {
            "schema_version": "1.0",
            "episode_id": "E001",
            "cover": {
                "title": "테스트",
                "visual_concept": "simple approved-art crop",
                "strategy": "DERIVED_FROM_APPROVED_ART"
            },
            "slides": [
                {
                    "slide_id": "S01",
                    "beat": "친구가 이상한 봉투를 내민다",
                    "state_delta": "모름에서 의심으로",
                    "visual_owner": "ACTION",
                    "shot": "medium two-shot, eye level",
                    "action": "친구가 봉투를 내민다",
                    "expression": "받는 사람은 살짝 의심",
                    "screen_geometry": None,
                    "background_level": "NONE",
                    "essential_background": [],
                    "background_reason": None,
                    "face_acting_intent": "slight suspicion with closed mouth",
                    "emotion_delta": "baseline -> suspicion",
                    "anatomy_contract": {
                        "risk_reason": "prop plus gesture can duplicate a limb",
                        "limb_roles": [
                            "giver prop hand: holds envelope only",
                            "giver other hand: stays relaxed"
                        ],
                        "required_contacts": ["one giver hand -> envelope"],
                        "forbidden_outcomes": ["extra limb", "disconnected hand"],
                        "simplification_fallback": "preserve the handoff and drop the extra gesture"
                    },
                    "continuity_in": [],
                    "continuity_out": ["봉투가 주인공 손에 있음"],
                    "text_safe_region": "upper left",
                    "copy": []
                }
            ]
        }
        (self.root / "episodes" / "E001" / "storyboard.json").write_text(
            json.dumps(storyboard, ensure_ascii=False), encoding="utf-8"
        )
        episode = self.root / "episodes" / "E001"
        (episode / "source.md").write_text("# Source draft / lock\n- Source URL: https://example.com/post\n", encoding="utf-8")
        (episode / "story.md").write_text("# Story draft / lock\n- Premise: test\n", encoding="utf-8")
        advance("E001", "PREPRODUCTION_REVIEW", "review payload prepared", "present", self.root)
        approve_editorial_review("E001", "user approved", self.root)
        advance("E001", "SOURCE_LOCK", "approved source hash locked", "lock story", self.root)
        advance("E001", "STORY_LOCK", "approved story hash locked", "lock storyboard", self.root)
        advance("E001", "STORYBOARD_LOCK", "approved storyboard hash locked", "lock visual packet", self.root)
        advance("E001", "VISUAL_PACKET_LOCK", "minimum sufficient visual packet locked", "compile B01", self.root)
        self.plan = self.root / "episodes" / "E001" / "boards" / "B01.plan.json"
        self.plan.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "episode_id": "E001",
                    "board_id": "B01",
                    "rows": 2,
                    "columns": 2,
                    "outer_margin_px": 0,
                    "gutter_px": 20,
                    "cells": [{"slide_id": "S01", "row": 0, "column": 0, "intent": "hook"}]
                }
            ),
            encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_compile_hash_bound_prompt(self) -> None:
        output = self.plan.with_name("B01.dispatch.json")
        dispatch = compile_master_board_dispatch("E001", self.plan, output, self.root)
        self.assertEqual(dispatch["operation"], "GENERATE_MASTER_BOARD")
        self.assertEqual(dispatch["dispatch_id"], "E001-B01-V2-MASTER-A1")
        self.assertEqual(len(dispatch["bound_media"]), 1)
        self.assertIn("TOP_LEFT S01", dispatch["prompt"])
        self.assertIn("TEXT-FREE", dispatch["prompt"])
        self.assertIn("anatomy_contract=", dispatch["prompt"])
        self.assertIn("extra limb", dispatch["prompt"])
        self.assertIn("LOWEST-SUFFICIENT", dispatch["prompt"])
        self.assertIn("background_level=NONE", dispatch["prompt"])
        self.assertIn("face_acting_intent=", dispatch["prompt"])
        self.assertIn("state_delta=", dispatch["prompt"])
        self.assertIn("continuity_in=", dispatch["prompt"])
        self.assertIn("Target character definitions:", dispatch["prompt"])
        self.assertIn("Palette match alone is not a style PASS", dispatch["prompt"])
        runtime = dispatch["runtime_attachment"]
        self.assertTrue(runtime["preflight_required_before_execute"])
        self.assertEqual(runtime["source_authority"], "REPOSITORY_REGISTRY_SHA256")
        self.assertEqual(runtime["carrier_scope"], "SESSION_ONLY")
        self.assertEqual(runtime["preferred_carrier"], "REPOSITORY_DIRECT")
        self.assertIn("CURRENT_SESSION_ATTACHMENT", runtime["fallback_carriers"])
        self.assertTrue(runtime["fallback_only_after_direct_runtime_bridge_unavailable"])
        self.assertTrue(runtime["revalidate_after_session_or_surface_change"])
        self.assertTrue(runtime["attachment_does_not_reset_episode_or_stage"])
        self.assertFalse(runtime["opaque_runtime_handle_is_reference_authority"])
        self.assertTrue(output.is_file())

    def test_v2_dispatch_cannot_compile_before_visual_packet_lock(self) -> None:
        state_path = self.root / "episodes" / "E001" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["stage"] = "STORYBOARD_LOCK"
        state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(DispatchError):
            compile_master_board_dispatch("E001", self.plan, self.plan.with_name("early.json"), self.root)

    def test_reference_hash_mismatch_fails_closed(self) -> None:
        visual_path = self.root / "episodes" / "E001" / "visual_packet.json"
        visual = json.loads(visual_path.read_text())
        visual["references"][0]["sha256"] = "0" * 64
        visual_path.write_text(json.dumps(visual), encoding="utf-8")
        with self.assertRaises(DispatchError):
            compile_master_board_dispatch("E001", self.plan, self.plan.with_name("out.json"), self.root)

    def test_malformed_anatomy_contract_fails_closed(self) -> None:
        storyboard_path = self.root / "episodes" / "E001" / "storyboard.json"
        storyboard = json.loads(storyboard_path.read_text())
        storyboard["slides"][0]["anatomy_contract"] = {"risk_reason": "incomplete"}
        storyboard_path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(DispatchError):
            compile_master_board_dispatch("E001", self.plan, self.plan.with_name("bad.json"), self.root)


if __name__ == "__main__":
    unittest.main()

