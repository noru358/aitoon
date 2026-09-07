from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .state import ROOT, StateError, read_json, sha256_file


class DispatchError(RuntimeError):
    pass


def _bound_references(visual_packet: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    references = visual_packet.get("references")
    if not isinstance(references, list) or not references:
        raise DispatchError("visual packet has no bound reference media")
    bound: list[dict[str, Any]] = []
    for index, item in enumerate(references, start=1):
        try:
            relative = Path(item["path"])
            expected = item["sha256"]
            role = item["role"]
            allowed = item["allowed_influence"]
            forbidden = item["forbidden_inference"]
        except KeyError as exc:
            raise DispatchError(f"reference {index} lacks required role metadata") from exc
        path = (root / relative).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError as exc:
            raise DispatchError(f"reference path escapes AIToon: {relative}") from exc
        if not path.is_file():
            raise DispatchError(f"reference bytes missing: {relative}")
        actual = sha256_file(path)
        if actual != expected:
            raise DispatchError(f"reference hash mismatch: {relative}")
        bound.append(
            {
                "path_or_handle": relative.as_posix(),
                "sha256": actual,
                "role": str(role),
                "allowed_influence": str(allowed),
                "forbidden_inference": str(forbidden),
            }
        )
    return bound


def _slide_map(storyboard: dict[str, Any]) -> dict[str, dict[str, Any]]:
    slides = storyboard.get("slides")
    if not isinstance(slides, list):
        raise DispatchError("storyboard slides must be a list")
    result: dict[str, dict[str, Any]] = {}
    for slide in slides:
        slide_id = slide.get("slide_id")
        if not slide_id or slide_id in result:
            raise DispatchError(f"missing or duplicate slide_id: {slide_id!r}")
        result[slide_id] = slide
    return result


def _cell_label(row: int, column: int) -> str:
    return {
        (0, 0): "TOP_LEFT",
        (0, 1): "TOP_RIGHT",
        (1, 0): "BOTTOM_LEFT",
        (1, 1): "BOTTOM_RIGHT",
    }[(row, column)]


def _anatomy_contract_text(slide: dict[str, Any]) -> str:
    contract = slide.get("anatomy_contract")
    if contract is None:
        return ""
    if not isinstance(contract, dict):
        raise DispatchError("anatomy_contract must be an object when present")
    required = (
        "risk_reason",
        "limb_roles",
        "required_contacts",
        "forbidden_outcomes",
        "simplification_fallback",
    )
    missing = [key for key in required if key not in contract]
    if missing:
        raise DispatchError(f"anatomy_contract missing fields: {', '.join(missing)}")
    for key in ("limb_roles", "required_contacts", "forbidden_outcomes"):
        value = contract[key]
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            raise DispatchError(f"anatomy_contract {key} must contain non-empty strings")
    if not isinstance(contract["risk_reason"], str) or not contract["risk_reason"].strip():
        raise DispatchError("anatomy_contract risk_reason must be non-empty")
    if not isinstance(contract["simplification_fallback"], str) or not contract["simplification_fallback"].strip():
        raise DispatchError("anatomy_contract simplification_fallback must be non-empty")
    return f"; anatomy_contract={json.dumps(contract, ensure_ascii=False, separators=(',', ':'))}"


def compile_master_board_dispatch(
    episode_id: str,
    board_plan_path: Path,
    output_path: Path,
    root: Path = ROOT,
    attempt: int = 1,
) -> dict[str, Any]:
    episode = root / "episodes" / episode_id
    storyboard = read_json(episode / "storyboard.json")
    visual_packet = read_json(episode / "visual_packet.json")
    state = read_json(episode / "state.json")
    board = read_json(board_plan_path)
    if storyboard.get("episode_id") != episode_id or visual_packet.get("episode_id") != episode_id:
        raise DispatchError("episode identity mismatch in storyboard or visual packet")
    if board.get("episode_id") != episode_id:
        raise DispatchError("board plan episode mismatch")
    revision = int(state.get("protocol_revision", 1))
    if revision >= 2:
        if state.get("stage") not in {"VISUAL_PACKET_LOCK", "MASTER_BOARD_QC"}:
            raise DispatchError(
                "v2 master-board dispatch may compile only from VISUAL_PACKET_LOCK "
                "or as a bounded retry from MASTER_BOARD_QC"
            )
        review = read_json(episode / "editorial_review.json")
        if review.get("status") != "APPROVED":
            raise DispatchError("cannot compile v2 image dispatch before editorial approval")
        approved = review.get("approved_hashes")
        if not isinstance(approved, dict):
            raise DispatchError("approved editorial hash lock is missing")
        for name in ("source.md", "story.md", "storyboard.json"):
            if approved.get(name) != sha256_file(episode / name):
                raise DispatchError(f"reviewed file changed after approval: {name}")
        if visual_packet.get("status") != "LOCKED":
            raise DispatchError("v2 visual packet must be LOCKED before image dispatch")
    if board.get("rows") != 2 or board.get("columns") != 2:
        raise DispatchError("master board must be 2x2")
    if not 1 <= attempt <= 2:
        raise DispatchError("whole-board attempts are limited to two total")

    bound = _bound_references(visual_packet, root)
    slides = _slide_map(storyboard)
    cell_lines: list[str] = []
    occupied: set[tuple[int, int]] = set()
    for cell in board.get("cells", []):
        position = int(cell["row"]), int(cell["column"])
        if position in occupied or position[0] not in {0, 1} or position[1] not in {0, 1}:
            raise DispatchError(f"invalid/duplicate board cell: {position}")
        occupied.add(position)
        slide_id = cell["slide_id"]
        if slide_id not in slides:
            raise DispatchError(f"board cell not found in storyboard: {slide_id}")
        slide = slides[slide_id]
        geometry = slide.get("screen_geometry")
        geometry_text = f"; screen_geometry={json.dumps(geometry, ensure_ascii=False)}" if geometry else ""
        anatomy_text = _anatomy_contract_text(slide)
        design_text = ""
        if revision >= 2:
            level = slide.get("background_level")
            essential = slide.get("essential_background")
            if level not in {"NONE", "SYMBOLIC", "LOCATION_ANCHOR", "FULL_SCENE"}:
                raise DispatchError(f"{slide_id}: invalid background_level")
            if not isinstance(essential, list):
                raise DispatchError(f"{slide_id}: essential_background must be a list")
            if level == "FULL_SCENE" and not str(slide.get("background_reason", "")).strip():
                raise DispatchError(f"{slide_id}: FULL_SCENE requires background_reason")
            face = str(slide.get("face_acting_intent", "")).strip()
            emotion = str(slide.get("emotion_delta", "")).strip()
            if not face or not emotion:
                raise DispatchError(f"{slide_id}: v2 face acting fields are required")
            design_text = (
                f"; background_level={level}; essential_background={json.dumps(essential, ensure_ascii=False)}"
                f"; face_acting_intent={face}; emotion_delta={emotion}"
            )
        cell_lines.append(
            f"- {_cell_label(*position)} {slide_id}: shot={slide['shot']}; "
            f"action={slide['action']}; expression={slide['expression']}; "
            f"visual_owner={slide['visual_owner']}; beat={slide['beat']}; "
            f"leave_text_space={slide['text_safe_region']}{design_text}{geometry_text}{anatomy_text}"
        )
    for position in ((0, 0), (0, 1), (1, 0), (1, 1)):
        if position not in occupied:
            cell_lines.append(f"- {_cell_label(*position)}: EMPTY, plain paper cell, no illustration")

    reference_lines = [
        f"- {item['role']}: use only {item['allowed_influence']}; never infer {item['forbidden_inference']}"
        for item in bound
    ]
    palette = ", ".join(str(x) for x in visual_packet.get("palette", [])) or "follow the bound references"
    line_grammar = "; ".join(str(x) for x in visual_packet.get("line_grammar", [])) or "follow the bound references"
    reject = "; ".join(str(x) for x in visual_packet.get("reject_traits", []))
    style_dimensions = "; ".join(str(x) for x in visual_packet.get("style_match_dimensions", []))
    characters = visual_packet.get("characters", [])
    cast_line = ""
    if revision >= 2:
        if not isinstance(characters, list):
            raise DispatchError("visual packet characters must be a list")
        cast_line = (
            f"Target cast has exactly {len(characters)} episode characters defined by the visual packet. "
            "Do not copy people or identities visible in style references unless a character entry explicitly binds that identity."
        )

    prompt = "\n".join(
        [
            "Create one TEXT-FREE 2x2 storyboard master board for a Korean Instagram comic.",
            cast_line,
            "All four cells are portrait 4:5 with clean straight gutters. Draw the occupied cells as one coherent episode in the same visual hand.",
            "Use the LOWEST-SUFFICIENT background in each cell. Omit decorative furniture, plants, wall art, lamps, shelves, appliances, packaging, and texture unless the cell explicitly declares them story-bearing or location-essential. Empty space is valid.",
            "The attached images are binding visual references with separate roles:",
            *reference_lines,
            f"Palette: {palette}.",
            f"Line/shape behavior: {line_grammar}.",
            f"Style-match dimensions that must all agree with the references: {style_dimensions or 'line, face/eye grammar, proportion, hair massing, shading, texture, detail budget'}. Palette match alone is not a style PASS.",
            "Cells:",
            *cell_lines,
            "Preserve only declared recurring identity, clothing, palette, story-bearing location anchors, object states, and drawing language across cells. Do not preserve decorative background clutter. Make each framing, expression, and body action serve its own beat; when emotion_delta changes, visible face acting must change rather than reusing a near-identical face render.",
            "Do not add titles, dialogue, captions, speech bubbles, letters, numerals, logos, watermarks, panel labels, or readable UI text.",
            f"Reject: {reject}.",
            "Return exactly one master-board image and nothing else inside the image.",
        ]
    )
    dispatch_id = (
        f"{episode_id}-{board['board_id']}-V{revision}-MASTER-A{attempt}"
        if revision >= 2
        else f"{episode_id}-{board['board_id']}-MASTER-A{attempt}"
    )
    dispatch = {
        "schema_version": "1.0",
        "dispatch_id": dispatch_id,
        "episode_id": episode_id,
        "target_id": board["board_id"],
        "operation": "GENERATE_MASTER_BOARD",
        "prompt": prompt,
        "bound_media": [
            {
                "path_or_handle": item["path_or_handle"],
                "sha256": item["sha256"],
                "role": item["role"],
            }
            for item in bound
        ],
        "attempt": attempt,
        "status": "READY",
        "runtime_attachment": {
            "preflight_required_before_execute": True,
            "source_authority": "REPOSITORY_REGISTRY_SHA256",
            "carrier_scope": "SESSION_ONLY",
            "preferred_carrier": "REPOSITORY_DIRECT",
            "fallback_carriers": [
                "CURRENT_SESSION_ATTACHMENT",
                "WORK_RUNTIME_FILE",
            ],
            "fallback_only_after_direct_runtime_bridge_unavailable": True,
            "revalidate_after_session_or_surface_change": True,
            "attachment_does_not_reset_episode_or_stage": True,
            "opaque_runtime_handle_is_reference_authority": False,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dispatch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dispatch

