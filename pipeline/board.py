from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image

from .state import sha256_file


class BoardError(RuntimeError):
    pass


def _load_plan(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BoardError(f"cannot load board plan: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BoardError("board plan root must be an object")
    if value.get("schema_version") != "1.0":
        raise BoardError("unsupported board plan version")
    if value.get("rows") != 2 or value.get("columns") != 2:
        raise BoardError("v1 board plans must use a 2x2 grid")
    cells = value.get("cells")
    if not isinstance(cells, list) or not 1 <= len(cells) <= 4:
        raise BoardError("board plan requires one to four occupied cells")
    positions: set[tuple[int, int]] = set()
    slide_ids: set[str] = set()
    for cell in cells:
        try:
            position = int(cell["row"]), int(cell["column"])
            slide_id = str(cell["slide_id"])
        except (KeyError, TypeError, ValueError) as exc:
            raise BoardError("invalid board cell") from exc
        if position[0] not in {0, 1} or position[1] not in {0, 1}:
            raise BoardError(f"cell position outside 2x2 grid: {position}")
        if position in positions or slide_id in slide_ids:
            raise BoardError("duplicate board position or slide id")
        positions.add(position)
        slide_ids.add(slide_id)
    return value


def split_master_board(
    input_path: Path,
    plan_path: Path,
    output_dir: Path,
    target_width: int = 1080,
    target_height: int = 1350,
) -> dict[str, Any]:
    plan = _load_plan(plan_path)
    if not input_path.is_file():
        raise BoardError(f"master board missing: {input_path}")
    if target_width <= 0 or target_height <= 0:
        raise BoardError("target dimensions must be positive")

    with Image.open(input_path) as source_image:
        source = source_image.convert("RGB")
    margin = int(plan["outer_margin_px"])
    gutter = int(plan["gutter_px"])
    usable_width = source.width - 2 * margin - gutter
    usable_height = source.height - 2 * margin - gutter
    if usable_width <= 0 or usable_height <= 0:
        raise BoardError("margin/gutter consume the master board")
    if usable_width % 2 or usable_height % 2:
        raise BoardError("board geometry does not divide into equal integer cells")
    cell_width, cell_height = usable_width // 2, usable_height // 2
    expected_ratio = target_width / target_height
    actual_ratio = cell_width / cell_height
    if abs(expected_ratio - actual_ratio) > 0.01:
        raise BoardError(
            f"master cells are not 4:5: {cell_width}x{cell_height}; "
            "use built-in image expansion instead of destructive crop"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[dict[str, Any]] = []
    for cell in plan["cells"]:
        row, column = int(cell["row"]), int(cell["column"])
        left = margin + column * (cell_width + gutter)
        top = margin + row * (cell_height + gutter)
        crop = source.crop((left, top, left + cell_width, top + cell_height))
        if crop.size != (target_width, target_height):
            crop = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
        output = output_dir / f"{cell['slide_id']}.png"
        crop.save(output, "PNG", optimize=False, compress_level=9)
        outputs.append(
            {
                "slide_id": cell["slide_id"],
                "path": output.as_posix(),
                "sha256": sha256_file(output),
                "width": target_width,
                "height": target_height,
                "source_box": [left, top, left + cell_width, top + cell_height],
            }
        )
    return {
        "schema_version": "1.0",
        "board_id": plan["board_id"],
        "master_path": input_path.as_posix(),
        "master_sha256": sha256_file(input_path),
        "plan_sha256": sha256_file(plan_path),
        "outputs": outputs,
    }

