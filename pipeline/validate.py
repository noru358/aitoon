from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .state import EPISODE_RE, ROOT, StateError, policy, read_json, sha256_file


class ValidationError(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate_policy(root: Path = ROOT) -> None:
    data = policy(root)
    _require(data.get("schema_version") == "1.0", "unsupported policy schema")
    execution = data.get("execution", {})
    _require(execution.get("additional_paid_budget_krw") == 0, "paid budget must be zero")
    _require(execution.get("paid_api_allowed") is False, "paid API must be disabled")
    _require(execution.get("paid_saas_allowed") is False, "paid SaaS must be disabled")
    _require(execution.get("ask_user_for_routine_approval") is False, "routine user gates must be disabled")
    _require(execution.get("terminal_states") == ["DONE", "ABANDONED_BY_USER"], "terminal state drift")
    stages = data.get("stages")
    _require(isinstance(stages, list) and len(stages) == len(set(stages)), "stages must be unique")
    _require(stages[0] == "BOOTSTRAP" and stages[-1] == "DONE", "stage boundary drift")
    render = data.get("render", {})
    _require(render.get("default_lane") == "MASTER_BOARD", "master-board lane must remain default")
    _require(render.get("maximum_slides_per_board") == 4, "v1 board capacity drift")
    _require(data.get("product", {}).get("delivery") == "ONE_FILE_PER_SLIDE", "delivery contract drift")



def validate_reference_registry(root: Path = ROOT) -> None:
    registry = read_json(root / "references" / "registry.json")
    _require(registry.get("schema_version") == "1.0", "production reference registry version drift")
    assets = registry.get("assets")
    _require(isinstance(assets, list) and assets, "production reference registry is empty")
    allowed_authorities = {"PRIMARY_STYLE", "CONTINUITY_ANCHOR"}
    seen_ids: set[str] = set()
    primary_count = 0
    for item in assets:
        required = {
            "id", "path", "sha256", "authority", "provenance_basis",
            "independent_authorship_verification", "production_eligible",
            "source_kind", "role", "allowed_influence", "forbidden_inference", "status"
        }
        _require(required.issubset(item), "malformed production reference registry entry")
        _require(item["id"] not in seen_ids, f"duplicate production reference id: {item['id']}")
        seen_ids.add(item["id"])
        _require(item["authority"] in allowed_authorities, f"bad reference authority: {item['authority']}")
        _require(isinstance(item["production_eligible"], bool), "production_eligible must be boolean")
        _require(
            isinstance(item["independent_authorship_verification"], bool),
            "independent_authorship_verification must be boolean",
        )
        _require(bool(item["provenance_basis"]), "reference provenance basis missing")
        _require(
            bool(item["allowed_influence"]) and bool(item["forbidden_inference"]),
            "reference influence bounds missing",
        )
        path = (root / item["path"]).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError as exc:
            raise ValidationError("production reference escapes repository") from exc
        _require(path.is_file(), f"production reference missing: {item['path']}")
        _require(sha256_file(path) == item["sha256"], f"production reference hash mismatch: {item['path']}")
        if item["authority"] == "PRIMARY_STYLE":
            primary_count += 1
            _require(
                item["source_kind"] != "AI_GENERATED_APPROVED",
                "generated episode art cannot be PRIMARY_STYLE",
            )
    _require(primary_count >= 1, "at least one PRIMARY_STYLE reference is required")


def validate_calibration(root: Path = ROOT) -> None:
    directory = root / "calibration"
    registry = read_json(directory / "references" / "registry.json")
    _require(registry.get("schema_version") == "1.0", "calibration reference registry version drift")
    registered: dict[str, dict[str, Any]] = {}
    for item in registry.get("assets", []):
        path = (root / item["path"]).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError as exc:
            raise ValidationError("calibration reference escapes repository") from exc
        _require(path.is_file(), f"calibration reference missing: {item['path']}")
        _require(sha256_file(path) == item["sha256"], f"calibration reference hash mismatch: {item['path']}")
        registered[item["path"]] = item
    _require(len(registered) >= 2, "calibration requires identity/person and scene references")

    dispatch = read_json(directory / "B01.dispatch.json")
    _require(dispatch.get("operation") == "GENERATE_MASTER_BOARD", "calibration dispatch operation drift")
    _require(dispatch.get("attempt") == 1, "calibration first dispatch attempt drift")
    for binding in dispatch.get("bound_media", []):
        registry_item = registered.get(binding.get("path_or_handle"))
        _require(registry_item is not None, "dispatch uses an unregistered calibration reference")
        _require(binding.get("sha256") == registry_item["sha256"], "dispatch/reference hash disagreement")

    pilot = read_json(directory / "PILOT_STATE.json")
    _require(pilot.get("paid_fallback_allowed") is False, "calibration paid fallback must be disabled")
    _require(pilot.get("user_input_required") is False, "calibration must not create a routine user gate")
    _require(bool(pilot.get("exact_next_action")), "calibration exact next action missing")


def _validate_artifact(root: Path, item: dict[str, Any], episode_id: str) -> None:
    required = {"artifact_id", "role", "path", "sha256", "size_bytes", "registered_at"}
    _require(required.issubset(item), f"{episode_id}: malformed artifact record")
    path = (root / item["path"]).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise ValidationError(f"{episode_id}: artifact escapes repository") from exc
    _require(path.is_file(), f"{episode_id}: missing artifact {item['path']}")
    _require(sha256_file(path) == item["sha256"], f"{episode_id}: artifact hash mismatch {item['path']}")
    _require(path.stat().st_size == item["size_bytes"], f"{episode_id}: artifact size mismatch")


def _validate_qc_reports(root: Path, episode_dir: Path, episode_id: str) -> None:
    for report_path in sorted((episode_dir / "qc").glob("*.json")):
        report = read_json(report_path)
        _require(report.get("episode_id") == episode_id, f"{report_path}: episode mismatch")
        _require(report.get("status") in {"PASS", "FAIL", "BLOCKED_UNSEEN"}, f"{report_path}: bad status")
        inspected = report.get("inspected")
        _require(isinstance(inspected, list) and inspected, f"{report_path}: no inspected evidence")
        if report.get("status") == "PASS":
            for item in inspected:
                _require(
                    bool(item.get("sha256") or item.get("stable_app_handle")),
                    f"{report_path}: PASS inspection lacks artifact evidence",
                )


def validate_episode(episode_dir: Path, root: Path = ROOT) -> None:
    episode_id = episode_dir.name
    _require(bool(EPISODE_RE.fullmatch(episode_id)), f"invalid episode directory: {episode_id}")
    state = read_json(episode_dir / "state.json")
    _require(state.get("schema_version") == "1.0", f"{episode_id}: unsupported state schema")
    _require(state.get("episode_id") == episode_id, f"{episode_id}: state id mismatch")
    stages = policy(root)["stages"]
    _require(state.get("stage") in stages, f"{episode_id}: unknown stage")
    _require(state.get("run_status") in {"ACTIVE", "BLOCKED_RETRYABLE", "DONE", "ABANDONED_BY_USER"}, f"{episode_id}: bad run status")
    _require(bool(state.get("exact_next_action")), f"{episode_id}: next action missing")
    if state["run_status"] == "BLOCKED_RETRYABLE":
        _require(isinstance(state.get("blocked"), dict), f"{episode_id}: blocked detail missing")
        allowed = set(policy(root)["execution"]["retryable_states"])
        _require(state["blocked"].get("code") in allowed, f"{episode_id}: unrecognized retry block")
    else:
        _require(state.get("blocked") is None, f"{episode_id}: stale blocked record")
    for name in ("source.md", "story.md", "storyboard.json", "visual_packet.json"):
        _require((episode_dir / name).is_file(), f"{episode_id}: missing {name}")
    for artifact in state.get("artifacts", []):
        _validate_artifact(root, artifact, episode_id)
    _validate_qc_reports(root, episode_dir, episode_id)
    if state["run_status"] == "DONE":
        _require(state["stage"] == "DONE", f"{episode_id}: DONE status/stage mismatch")
        final_report = episode_dir / "qc" / "final.json"
        _require(final_report.is_file(), f"{episode_id}: DONE without final QC")
        _require(read_json(final_report).get("status") == "PASS", f"{episode_id}: final QC is not PASS")
        exports = list((episode_dir / "export").glob("S*.png"))
        if len(exports) != state["slide_count"]:
            manifest_path = episode_dir / "export" / "manifest.json"
            _require(manifest_path.is_file(), f"{episode_id}: export count mismatch and no stable-handle manifest")
            manifest = read_json(manifest_path)
            _require(manifest.get("episode_id") == episode_id, f"{episode_id}: export manifest episode mismatch")
            slides = manifest.get("slides")
            _require(isinstance(slides, list) and len(slides) == state["slide_count"], f"{episode_id}: export manifest count mismatch")
            expected_size = (
                policy(root).get("product", {}).get("width"),
                policy(root).get("product", {}).get("height"),
            )
            seen: set[str] = set()
            for item in slides:
                slide_id = item.get("slide_id")
                _require(isinstance(slide_id, str) and slide_id not in seen, f"{episode_id}: duplicate/bad export slide id")
                seen.add(slide_id)
                _require(bool(item.get("stable_app_handle")), f"{episode_id}: export manifest lacks stable app handle")
                sha = item.get("sha256")
                _require(isinstance(sha, str) and len(sha) == 64, f"{episode_id}: export manifest lacks SHA-256")
                _require((item.get("width"), item.get("height")) == expected_size, f"{episode_id}: export manifest dimensions drift")


def validate_repository(root: Path = ROOT) -> list[str]:
    validate_policy(root)
    validate_reference_registry(root)
    validate_calibration(root)
    checked = ["policy", "references", "calibration"]
    episodes = root / "episodes"
    if episodes.is_dir():
        for directory in sorted(path for path in episodes.iterdir() if path.is_dir()):
            validate_episode(directory, root)
            checked.append(directory.name)
    return checked
