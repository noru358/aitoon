from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image

from .state import sha256_file


class BoardError(RuntimeError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BoardError(f"cannot load JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BoardError("JSON root must be an object")
    return value


def _load_plan(path: Path) -> dict[str, Any]:
    value = _load_json(path)
    if value.get("schema_version") != "1.0":
        raise BoardError("unsupported board plan version")
    if value.get("rows") != 2 or value.get("columns") != 2:
        raise BoardError("canonical board plans must use a 2x2 grid")
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


def _sheet_geometry(
    width: int,
    height: int,
    rows: int,
    columns: int,
    margin: int,
    gutter: int,
    target_width: int,
    target_height: int,
) -> tuple[int, int]:
    usable_width = width - 2 * margin - max(0, columns - 1) * gutter
    usable_height = height - 2 * margin - max(0, rows - 1) * gutter
    if usable_width <= 0 or usable_height <= 0:
        raise BoardError("margin/gutter consume the runtime sheet")
    if usable_width % columns or usable_height % rows:
        raise BoardError("runtime sheet geometry does not divide into equal integer cells")
    cell_width = usable_width // columns
    cell_height = usable_height // rows
    expected_ratio = target_width / target_height
    actual_ratio = cell_width / cell_height
    if abs(expected_ratio - actual_ratio) > 0.01:
        raise BoardError(
            f"runtime cells are not 4:5: {cell_width}x{cell_height}; "
            "use built-in image expansion/repair rather than destructive crop"
        )
    return cell_width, cell_height


def pack_runtime_sheet(
    input_path: Path,
    plan_path: Path,
    dispatch_path: Path,
    output_path: Path,
    target_width: int = 1080,
    target_height: int = 1350,
) -> dict[str, Any]:
    plan = _load_plan(plan_path)
    dispatch = _load_json(dispatch_path)
    runtime = dispatch.get("runtime_sheet")
    if not isinstance(runtime, dict):
        raise BoardError("dispatch has no runtime_sheet contract")
    if runtime.get("strategy") != "NATURAL_OCCUPANCY":
        raise BoardError("unsupported runtime sheet strategy")
    rows = int(runtime.get("rows", 0))
    columns = int(runtime.get("columns", 0))
    cells = runtime.get("cells")
    if rows <= 0 or columns <= 0 or not isinstance(cells, list) or not cells:
        raise BoardError("invalid runtime sheet geometry")
    if len(cells) != int(runtime.get("cell_count", -1)):
        raise BoardError("runtime sheet cell count mismatch")
    if runtime.get("generator_empty_cells_forbidden") is not True:
        raise BoardError("runtime sheet must not delegate empty canonical cells to generator")
    if runtime.get("pack_to_canonical_2x2") is not True:
        raise BoardError("runtime sheet must deterministically pack to canonical 2x2")
    if not input_path.is_file():
        raise BoardError(f"runtime sheet missing: {input_path}")
    if target_width <= 0 or target_height <= 0:
        raise BoardError("target dimensions must be positive")

    canonical = {
        str(cell["slide_id"]): (int(cell["row"]), int(cell["column"]))
        for cell in plan["cells"]
    }
    if set(canonical) != {str(cell.get("slide_id")) for cell in cells}:
        raise BoardError("runtime sheet slides do not match canonical plan")

    with Image.open(input_path) as source_image:
        source = source_image.convert("RGB")

    margin = int(plan["outer_margin_px"])
    gutter = int(plan["gutter_px"])
    cell_width, cell_height = _sheet_geometry(
        source.width,
        source.height,
        rows,
        columns,
        margin,
        gutter,
        target_width,
        target_height,
    )

    canonical_width = 2 * target_width + gutter
    canonical_height = 2 * target_height + gutter
    board = Image.new("RGB", (canonical_width, canonical_height), "white")
    packed: list[dict[str, Any]] = []

    for item in cells:
        slide_id = str(item["slide_id"])
        rr = int(item["runtime_row"])
        rc = int(item["runtime_column"])
        if rr < 0 or rr >= rows or rc < 0 or rc >= columns:
            raise BoardError(f"runtime cell outside sheet: {slide_id}")
        left = margin + rc * (cell_width + gutter)
        top = margin + rr * (cell_height + gutter)
        crop = source.crop((left, top, left + cell_width, top + cell_height))
        if crop.size != (target_width, target_height):
            crop = crop.resize((target_width, target_height), Image.Resampling.LANCZOS)
        cr, cc = canonical[slide_id]
        out_left = cc * (target_width + gutter)
        out_top = cr * (target_height + gutter)
        board.paste(crop, (out_left, out_top))
        packed.append(
            {
                "slide_id": slide_id,
                "runtime_box": [left, top, left + cell_width, top + cell_height],
                "canonical_position": [cr, cc],
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    board.save(output_path, "PNG", optimize=False, compress_level=9)
    return {
        "schema_version": "1.0",
        "operation": "PACK_RUNTIME_SHEET_TO_CANONICAL_2X2",
        "runtime_sheet_path": input_path.as_posix(),
        "runtime_sheet_sha256": sha256_file(input_path),
        "plan_sha256": sha256_file(plan_path),
        "dispatch_sha256": sha256_file(dispatch_path),
        "canonical_board_path": output_path.as_posix(),
        "canonical_board_sha256": sha256_file(output_path),
        "width": canonical_width,
        "height": canonical_height,
        "packed": packed,
    }


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
    cell_width, cell_height = _sheet_geometry(
        source.width,
        source.height,
        2,
        2,
        margin,
        gutter,
        target_width,
        target_height,
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
