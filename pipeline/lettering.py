from __future__ import annotations

import ctypes
import json
import sys
import types
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from .state import ROOT, sha256_file


class LetteringError(RuntimeError):
    pass


def _resolve_inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise LetteringError(f"path escapes repository: {relative}") from exc
    if not path.is_file():
        raise LetteringError(f"missing file: {relative}")
    return path


def _ctypes_brotli_module() -> types.ModuleType:
    """Minimal decoder shim used only when the Python brotli wheel is absent."""
    library = ctypes.CDLL("libbrotlidec.so.1")
    function = library.BrotliDecoderDecompress
    function.argtypes = [
        ctypes.c_size_t,
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_size_t),
        ctypes.c_void_p,
    ]
    function.restype = ctypes.c_int

    module = types.ModuleType("brotli")

    def decompress(payload: bytes) -> bytes:
        source = ctypes.create_string_buffer(payload)
        capacity = max(len(payload) * 12, 1024 * 1024)
        for _ in range(8):
            target = ctypes.create_string_buffer(capacity)
            target_size = ctypes.c_size_t(capacity)
            result = function(len(payload), source, ctypes.byref(target_size), target)
            if result == 1:
                return target.raw[: target_size.value]
            if result != 3:
                raise LetteringError(f"Brotli WOFF2 decode failed with status {result}")
            capacity *= 2
        raise LetteringError("Brotli WOFF2 output exceeded safe decode budget")

    module.decompress = decompress  # type: ignore[attr-defined]
    module.error = RuntimeError  # type: ignore[attr-defined]
    return module


def _font_for_pillow(path: Path, cache_dir: Path) -> Path:
    if path.suffix.lower() != ".woff2":
        return path
    target = cache_dir / f"{path.stem}-{sha256_file(path)[:12]}.ttf"
    if target.is_file():
        return target
    try:
        import brotli  # noqa: F401
    except ImportError:
        sys.modules["brotli"] = _ctypes_brotli_module()
    try:
        from fontTools.ttLib import TTFont

        font = TTFont(path)
        font.flavor = None
        target.parent.mkdir(parents=True, exist_ok=True)
        font.save(target)
    except Exception as exc:
        raise LetteringError(f"cannot convert WOFF2 font: {exc}") from exc
    return target


def _measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> float:
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=font)
    return float(box[2] - box[0])


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            candidate = current + char
            if current and _measure(draw, candidate, font) > max_width:
                lines.append(current.rstrip())
                current = char.lstrip()
            else:
                current = candidate
        if current or not lines:
            lines.append(current.rstrip())
    return lines


def _draw_bubble(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], bubble: dict[str, Any]) -> None:
    x1, y1, x2, y2 = box
    fill = bubble["fill"]
    outline = bubble["outline"]
    width = int(bubble["outline_width"])
    tail = bubble.get("tail_tip")
    if tail:
        center = (x1 + x2) // 2
        base_y = y2 - max(width, 1)
        half = max(12, min((x2 - x1) // 8, 36))
        draw.polygon(
            [(center - half, base_y), (center + half, base_y), (int(tail["x"]), int(tail["y"]))],
            fill=fill,
            outline=outline if width else None,
        )
    draw.rounded_rectangle(
        box,
        radius=int(bubble["radius"]),
        fill=fill,
        outline=outline if width else None,
        width=width,
    )


def render_lettering(plan_path: Path, output_path: Path, root: Path = ROOT) -> dict[str, Any]:
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LetteringError(f"cannot load lettering plan: {exc}") from exc
    if plan.get("schema_version") != "1.0":
        raise LetteringError("unsupported lettering plan version")

    base = _resolve_inside(root, plan["base_art"]["path"])
    font_source = _resolve_inside(root, plan["font"]["path"])
    if sha256_file(base) != plan["base_art"]["sha256"]:
        raise LetteringError("base art hash mismatch")
    if sha256_file(font_source) != plan["font"]["sha256"]:
        raise LetteringError("font hash mismatch")
    canvas = plan["canvas"]
    if (int(canvas["width"]), int(canvas["height"])) != (1080, 1350):
        raise LetteringError("production canvas must be 1080x1350")

    with Image.open(base) as source:
        image = source.convert("RGBA")
    if image.size != (1080, 1350):
        raise LetteringError(f"base art must be 1080x1350, got {image.size}")
    draw = ImageDraw.Draw(image)
    font_path = _font_for_pillow(font_source, root / ".cache" / "fonts")
    seen: set[str] = set()

    for element in plan.get("elements", []):
        element_id = element["id"]
        if element_id in seen:
            raise LetteringError(f"duplicate lettering element id: {element_id}")
        seen.add(element_id)
        box_data = element["box"]
        x, y = int(box_data["x"]), int(box_data["y"])
        width, height = int(box_data["width"]), int(box_data["height"])
        if x < 0 or y < 0 or x + width > 1080 or y + height > 1350:
            raise LetteringError(f"lettering box outside safe canvas: {element_id}")
        bubble = element.get("bubble")
        padding = int(bubble["padding"]) if bubble else 0
        if bubble:
            _draw_bubble(draw, (x, y, x + width, y + height), bubble)
        text_box = (x + padding, y + padding, x + width - padding, y + height - padding)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]
        font = ImageFont.truetype(str(font_path), int(element["font_size"]))
        lines = _wrap(draw, element["text"], font, text_width)
        line_gap = max(2, round(int(element["font_size"]) * 0.18))
        boxes = [draw.textbbox((0, 0), line or " ", font=font) for line in lines]
        heights = [value[3] - value[1] for value in boxes]
        total_height = sum(heights) + line_gap * max(0, len(lines) - 1)
        if total_height > text_height:
            raise LetteringError(f"text overflow in {element_id}; edit the plan instead of shrinking silently")
        cursor_y = text_box[1] + (text_height - total_height) // 2
        for line, line_box, line_height in zip(lines, boxes, heights):
            line_width = line_box[2] - line_box[0]
            align = element["align"]
            if align == "center":
                cursor_x = text_box[0] + (text_width - line_width) // 2
            elif align == "right":
                cursor_x = text_box[2] - line_width
            else:
                cursor_x = text_box[0]
            draw.text((cursor_x, cursor_y), line, font=font, fill=element["fill"])
            cursor_y += line_height + line_gap

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output_path, "PNG", optimize=False, compress_level=9)
    receipt = {
        "schema_version": "1.0",
        "slide_id": plan["slide_id"],
        "plan_path": plan_path.as_posix(),
        "plan_sha256": sha256_file(plan_path),
        "base_art_sha256": sha256_file(base),
        "font_sha256": sha256_file(font_source),
        "output_path": output_path.as_posix(),
        "output_sha256": sha256_file(output_path),
        "text": [element["text"] for element in plan.get("elements", [])],
    }
    return receipt

