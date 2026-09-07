from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .state import ROOT, read_json, sha256_file


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


def _approved_visual_anchor(
    episode_dir: Path,
    root: Path,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], list[dict[str, Any]]]:
    manifest_path = episode_dir / "approved_visual_anchor.json"
    if not manifest_path.is_file():
        return None, [], []
    manifest = read_json(manifest_path)
    if manifest.get("status") != "ACTIVE":
        return manifest, [], []
    expected = manifest.get("sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        raise DispatchError("active approved visual anchor must bind SHA-256")
    allowed = str(manifest.get("allowed_influence", "")).strip()
    forbidden = str(manifest.get("forbidden_inference", "")).strip()
    if not allowed or not forbidden:
        raise DispatchError("approved visual anchor influence bounds are required")

    repository_path = manifest.get("repository_path")
    if repository_path:
        relative = Path(repository_path)
        absolute = (root / relative).resolve()
        try:
            absolute.relative_to(root.resolve())
        except ValueError as exc:
            raise DispatchError("approved visual anchor escapes repository") from exc
        if not absolute.is_file():
            raise DispatchError("approved visual anchor repository bytes are missing")
        actual = sha256_file(absolute)
        if actual != expected:
            raise DispatchError("approved visual anchor repository hash mismatch")
        return manifest, [
            {
                "path_or_handle": relative.as_posix(),
                "sha256": actual,
                "role": "USER_APPROVED_EPISODE_VISUAL_ANCHOR",
                "allowed_influence": allowed,
                "forbidden_inference": forbidden,
            }
        ], []

    carrier = {
        "anchor_id": manifest.get("anchor_id", "APPROVED_VISUAL_ANCHOR"),
        "sha256": expected,
        "role": "USER_APPROVED_EPISODE_VISUAL_ANCHOR",
        "allowed_influence": allowed,
        "forbidden_inference": forbidden,
    }
    return manifest, [], [carrier]


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


def _runtime_layout(count: int) -> tuple[int, int]:
    layouts = {
        1: (1, 1),
        2: (1, 2),
        3: (1, 3),
        4: (2, 2),
    }
    try:
        return layouts[count]
    except KeyError as exc:
        raise DispatchError("runtime sheet requires one to four occupied slides") from exc


def _runtime_label(index: int, count: int) -> str:
    if count == 1:
        return "ONLY"
    if count == 2:
        return ("LEFT", "RIGHT")[index]
    if count == 3:
        return ("LEFT", "CENTER", "RIGHT")[index]
    return ("TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT")[index]


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
        raise DispatchError("canonical master board plan must remain 2x2")
    if not 1 <= attempt <= 2:
        raise DispatchError("whole-board attempts are limited to two total")

    cells = board.get("cells")
    if not isinstance(cells, list) or not 1 <= len(cells) <= 4:
        raise DispatchError("board plan requires one to four occupied cells")
    ordered_cells = sorted(cells, key=lambda item: (int(item["row"]), int(item["column"])))
    runtime_rows, runtime_columns = _runtime_layout(len(ordered_cells))

    bound = _bound_references(visual_packet, root)
    anchor_manifest, anchor_bound, required_anchor_carriers = _approved_visual_anchor(episode, root)
    bound.extend(anchor_bound)
    slides = _slide_map(storyboard)

    cell_lines: list[str] = []
    runtime_cells: list[dict[str, Any]] = []
    occupied: set[tuple[int, int]] = set()
    for index, cell in enumerate(ordered_cells):
        canonical_position = int(cell["row"]), int(cell["column"])
        if (
            canonical_position in occupied
            or canonical_position[0] not in {0, 1}
            or canonical_position[1] not in {0, 1}
        ):
            raise DispatchError(f"invalid/duplicate board cell: {canonical_position}")
        occupied.add(canonical_position)
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
        continuity_in = slide.get("continuity_in", [])
        continuity_out = slide.get("continuity_out", [])
        if not isinstance(continuity_in, list) or not isinstance(continuity_out, list):
            raise DispatchError(f"{slide_id}: continuity_in/out must be lists")

        runtime_row = index // runtime_columns
        runtime_column = index % runtime_columns
        runtime_cells.append(
            {
                "slide_id": slide_id,
                "runtime_row": runtime_row,
                "runtime_column": runtime_column,
                "canonical_row": canonical_position[0],
                "canonical_column": canonical_position[1],
            }
        )
        cell_lines.append(
            f"- {_runtime_label(index, len(ordered_cells))} {slide_id}: shot={slide['shot']}; "
            f"action={slide['action']}; expression={slide['expression']}; "
            f"visual_owner={slide['visual_owner']}; beat={slide['beat']}; "
            f"state_delta={slide['state_delta']}; "
            f"continuity_in={json.dumps(continuity_in, ensure_ascii=False)}; "
            f"continuity_out={json.dumps(continuity_out, ensure_ascii=False)}; "
            f"leave_text_space={slide['text_safe_region']}{design_text}{geometry_text}{anatomy_text}"
        )

    reference_lines = [
        f"- {item['role']}: use only {item['allowed_influence']}; never infer {item['forbidden_inference']}"
        for item in bound
    ]
    if required_anchor_carriers:
        reference_lines.extend(
            f"- {item['role']} (SESSION CARRIER REQUIRED, SHA-256 {item['sha256']}): "
            f"use only {item['allowed_influence']}; never infer {item['forbidden_inference']}"
            for item in required_anchor_carriers
        )

    palette = ", ".join(str(x) for x in visual_packet.get("palette", [])) or "follow the bound references"
    line_grammar = "; ".join(str(x) for x in visual_packet.get("line_grammar", [])) or "follow the bound references"
    reject = "; ".join(str(x) for x in visual_packet.get("reject_traits", []))
    style_dimensions = "; ".join(str(x) for x in visual_packet.get("style_match_dimensions", []))
    characters = visual_packet.get("characters", [])
    cast_line = ""
    character_lines: list[str] = []
    if revision >= 2:
        if not isinstance(characters, list):
            raise DispatchError("visual packet characters must be a list")
        cast_line = (
            f"Target cast has exactly {len(characters)} episode characters defined by the visual packet. "
            "Do not copy people or identities visible in PRIMARY_STYLE references unless a character entry explicitly binds that identity."
        )
        for character in characters:
            if not isinstance(character, dict):
                raise DispatchError("visual packet character entry must be an object")
            char_id = str(character.get("id", "")).strip()
            role = str(character.get("role", "")).strip()
            appearance = str(character.get("appearance", character.get("note", ""))).strip()
            if not char_id or not role:
                raise DispatchError("visual packet character requires id and role")
            character_lines.append(
                f"- {char_id} ({role}): {appearance or 'author a distinct episode-local identity inside the PRIMARY_STYLE drawing language'}"
            )

    anchor_lines: list[str] = []
    if anchor_manifest and anchor_manifest.get("status") == "ACTIVE":
        anchor_lines = [
            "The user-approved episode visual anchor is operationally binding inside its declared scope.",
            f"Approved-anchor influence: {anchor_manifest['allowed_influence']}.",
            f"Approved-anchor exclusions: {anchor_manifest['forbidden_inference']}.",
            "Do not freshly redesign an anchored face, hair, outfit, or approved rendering treatment. Objective anatomy/contact/screen/text constraints still override the anchor outside its approved scope.",
        ]

    prompt = "\n".join(
        [
            f"Create one completely TEXT-FREE {runtime_rows}x{runtime_columns} runtime contact sheet for a Korean Instagram comic.",
            f"This runtime sheet contains exactly {len(ordered_cells)} illustrated cell(s). Do not add extra panels, future beats, blank placeholder panels, title areas, or decorative cells.",
            cast_line,
            "Target character definitions:",
            *character_lines,
            *anchor_lines,
            "Draw the listed runtime cells as one coherent batch in the same visual hand.",
            "Use the LOWEST-SUFFICIENT background in each cell. Omit decorative furniture, plants, wall art, lamps, shelves, appliances, packaging, and texture unless the cell explicitly declares them story-bearing or location-essential.",
            "The attached images are binding visual references with separate roles:",
            *reference_lines,
            f"Palette: {palette}.",
            f"Line/shape behavior: {line_grammar}.",
            f"Style-match dimensions that must all agree with the references: {style_dimensions or 'line, face/eye grammar, proportion, hair massing, shading, texture, detail budget'}. Palette match alone is not a style PASS.",
            "Runtime cells:",
            *cell_lines,
            "Treat state_delta plus continuity_in/continuity_out as hard story-state contracts. Preserve only declared recurring identity, clothing, palette, story-bearing location anchors, object states, and drawing language across cells. Do not preserve decorative background clutter. Make each framing, expression, and body action serve its own beat; when emotion_delta changes, visible face acting must change rather than reusing a near-identical face render.",
            "ABSOLUTE ART-ONLY CONTRACT: do not add dialogue, thoughts, captions, speech bubbles, thought bubbles, letters, numerals, logos, watermarks, panel labels, hearts, sparkles, emphasis marks, or readable UI text.",
            f"Reject: {reject}.",
            "Return exactly one runtime contact-sheet image and nothing else inside the image.",
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
        "runtime_sheet": {
            "strategy": "NATURAL_OCCUPANCY",
            "rows": runtime_rows,
            "columns": runtime_columns,
            "cell_count": len(runtime_cells),
            "cells": runtime_cells,
            "generator_empty_cells_forbidden": True,
            "pack_to_canonical_2x2": True,
        },
        "context_isolation": {
            "art_only": True,
            "allowed": [
                "THIS_DISPATCH",
                "APPROVED_VISUAL_ANCHOR_MANIFEST",
                "BOUND_REFERENCE_REGISTRY_ENTRIES",
                "ACTUAL_REFERENCE_OR_ANCHOR_MEDIA",
            ],
            "forbidden": [
                "SOURCE_PROSE",
                "STORY_COPY",
                "STORYBOARD_COPY_TEXT",
                "EDITORIAL_DIALOGUE",
                "LETTERING_PLAN",
                "COVER_COPY",
                "FUTURE_BEATS_OUTSIDE_RUNTIME_SHEET",
            ],
        },
        "approved_visual_anchor": (
            {
                "anchor_id": anchor_manifest.get("anchor_id"),
                "sha256": anchor_manifest.get("sha256"),
                "allowed_influence": anchor_manifest.get("allowed_influence"),
                "forbidden_inference": anchor_manifest.get("forbidden_inference"),
                "transport": "REPOSITORY" if anchor_bound else "SESSION_CARRIER_REQUIRED",
            }
            if anchor_manifest and anchor_manifest.get("status") == "ACTIVE"
            else None
        ),
        "attempt": attempt,
        "status": "READY",
        "runtime_attachment": {
            "preflight_required_before_execute": True,
            "source_authority": "REPOSITORY_MANIFEST_AND_SHA256",
            "carrier_scope": "SESSION_ONLY",
            "preferred_carrier": "REPOSITORY_DIRECT",
            "fallback_carriers": [
                "CURRENT_SESSION_ATTACHMENT",
                "WORK_RUNTIME_FILE",
            ],
            "required_sha_carriers": required_anchor_carriers,
            "fallback_only_after_direct_runtime_bridge_unavailable": True,
            "revalidate_after_session_or_surface_change": True,
            "attachment_does_not_reset_episode_or_stage": True,
            "opaque_runtime_handle_is_reference_authority": False,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dispatch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dispatch
