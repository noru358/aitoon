from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from pipeline.board import BoardError, split_master_board


class BoardTests(unittest.TestCase):
    def test_split_clean_2x2_board(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            # 2 * 400 + 20 gutter wide; 2 * 500 + 20 gutter high.
            board = Image.new("RGB", (820, 1020), "white")
            colors = ["red", "green", "blue", "yellow"]
            boxes = [(0, 0, 400, 500), (420, 0, 820, 500), (0, 520, 400, 1020), (420, 520, 820, 1020)]
            for color, box in zip(colors, boxes):
                board.paste(color, box)
            board_path = root / "board.png"
            board.save(board_path)
            plan = {
                "schema_version": "1.0",
                "episode_id": "E001",
                "board_id": "B01",
                "rows": 2,
                "columns": 2,
                "outer_margin_px": 0,
                "gutter_px": 20,
                "cells": [
                    {"slide_id": "S01", "row": 0, "column": 0, "intent": "one"},
                    {"slide_id": "S02", "row": 0, "column": 1, "intent": "two"},
                    {"slide_id": "S03", "row": 1, "column": 0, "intent": "three"},
                    {"slide_id": "S04", "row": 1, "column": 1, "intent": "four"}
                ]
            }
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            receipt = split_master_board(board_path, plan_path, root / "art", 1080, 1350)
            self.assertEqual(len(receipt["outputs"]), 4)
            for index, output in enumerate(receipt["outputs"]):
                with Image.open(output["path"]) as image:
                    self.assertEqual(image.size, (1080, 1350))
                    pixel = image.getpixel((540, 675))
                    expected = Image.new("RGB", (1, 1), colors[index]).getpixel((0, 0))
                    self.assertEqual(pixel, expected)

    def test_reject_non_4x5_cells(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            Image.new("RGB", (800, 800), "white").save(root / "board.png")
            plan = {
                "schema_version": "1.0",
                "episode_id": "E001",
                "board_id": "B01",
                "rows": 2,
                "columns": 2,
                "outer_margin_px": 0,
                "gutter_px": 0,
                "cells": [{"slide_id": "S01", "row": 0, "column": 0, "intent": "one"}]
            }
            (root / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
            with self.assertRaises(BoardError):
                split_master_board(root / "board.png", root / "plan.json", root / "art")


if __name__ == "__main__":
    unittest.main()

