from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "policy.json"
EPISODE_RE = re.compile(r"^E[0-9]{3,}$")


class StateError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StateError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StateError(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise StateError(f"JSON root must be an object: {path}")
    return data


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    descriptor, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def policy(root: Path = ROOT) -> dict[str, Any]:
    return read_json(root / "config" / "policy.json")


def stages(root: Path = ROOT) -> list[str]:
    value = policy(root).get("stages")
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise StateError("policy stages must be an array of strings")
    return value


def episode_dir(episode_id: str, root: Path = ROOT) -> Path:
    if not EPISODE_RE.fullmatch(episode_id):
        raise StateError(f"invalid episode id: {episode_id!r}")
    return root / "episodes" / episode_id


def state_path(episode_id: str, root: Path = ROOT) -> Path:
    return episode_dir(episode_id, root) / "state.json"


def load_state(episode_id: str, root: Path = ROOT) -> dict[str, Any]:
    return read_json(state_path(episode_id, root))


def _copy_template(root: Path, name: str, target: Path, replacements: dict[str, str] | None = None) -> None:
    source = root / "templates" / name
    content = source.read_text(encoding="utf-8")
    for before, after in (replacements or {}).items():
        content = content.replace(before, after)
    target.write_text(content, encoding="utf-8")


def init_episode(episode_id: str, title: str, slide_count: int, root: Path = ROOT) -> dict[str, Any]:
    directory = episode_dir(episode_id, root)
    if directory.exists():
        raise StateError(f"episode already exists: {episode_id}")
    if not 1 <= slide_count <= 20:
        raise StateError("slide_count must be between 1 and 20")

    for child in ("boards", "art", "lettering", "cover", "final", "qc", "export", "quarantine"):
        (directory / child).mkdir(parents=True, exist_ok=True)
    _copy_template(root, "source.md", directory / "source.md")
    _copy_template(root, "story.md", directory / "story.md")
    _copy_template(
        root,
        "visual_packet.json",
        directory / "visual_packet.json",
        {"REPLACE_ME": episode_id},
    )
    storyboard = {
        "schema_version": "1.0",
        "episode_id": episode_id,
        "slides": [],
    }
    atomic_write_json(directory / "storyboard.json", storyboard)
    review = {
        "schema_version": "1.0",
        "episode_id": episode_id,
        "status": "PENDING",
        "review_scope": [
            "SOURCE", "TOPIC", "PREMISE", "SLIDE_COUNT", "BEATS",
            "DIALOGUE", "THOUGHT_NARRATION", "COVER_CONCEPT"
        ],
        "approved_hashes": None,
        "approval_evidence": None,
        "approved_at": None,
    }
    atomic_write_json(directory / "editorial_review.json", review)
    created = utc_now()
    state = {
        "schema_version": "1.0",
        "protocol_revision": int(policy(root).get("protocol_revision", 1)),
        "episode_id": episode_id,
        "title": title,
        "slide_count": slide_count,
        "stage": "BOOTSTRAP",
        "run_status": "ACTIVE",
        "blocked": None,
        "exact_next_action": "Draft source.md, story.md, storyboard.json and advance exactly to PREPRODUCTION_REVIEW for the user editorial review.",
        "stage_history": [
            {
                "at": created,
                "from": None,
                "to": "BOOTSTRAP",
                "evidence": "episode package initialized",
            }
        ],
        "artifacts": [],
    }
    atomic_write_json(directory / "state.json", state)
    return state


def approve_editorial_review(
    episode_id: str,
    approval_evidence: str,
    root: Path = ROOT,
) -> dict[str, Any]:
    if not approval_evidence.strip():
        raise StateError("editorial approval requires explicit evidence")
    current = load_state(episode_id, root)
    if current.get("stage") != "PREPRODUCTION_REVIEW":
        raise StateError("editorial approval is only valid at PREPRODUCTION_REVIEW")
    if current.get("run_status") != "ACTIVE":
        raise StateError("editorial review cannot be approved from a blocked or terminal state")
    review_path = episode_dir(episode_id, root) / "editorial_review.json"
    review = read_json(review_path)
    if review.get("episode_id") != episode_id:
        raise StateError("editorial review episode mismatch")
    approved_hashes = {
        "source.md": sha256_file(episode_dir(episode_id, root) / "source.md"),
        "story.md": sha256_file(episode_dir(episode_id, root) / "story.md"),
        "storyboard.json": sha256_file(episode_dir(episode_id, root) / "storyboard.json"),
    }
    review["status"] = "APPROVED"
    review["approved_hashes"] = approved_hashes
    review["approval_evidence"] = approval_evidence.strip()
    review["approved_at"] = utc_now()
    atomic_write_json(review_path, review)
    current["exact_next_action"] = "Advance exactly to SOURCE_LOCK using the approved review hashes; then continue STORY_LOCK and STORYBOARD_LOCK without another routine approval."
    atomic_write_json(state_path(episode_id, root), current)
    return review


def _require_editorial_hash_lock(episode_id: str, root: Path) -> None:
    review = read_json(episode_dir(episode_id, root) / "editorial_review.json")
    if review.get("status") != "APPROVED":
        raise StateError("PREPRODUCTION_REVIEW has not been explicitly approved")
    approved = review.get("approved_hashes")
    if not isinstance(approved, dict):
        raise StateError("editorial review approved hashes are missing")
    for name in ("source.md", "story.md", "storyboard.json"):
        path = episode_dir(episode_id, root) / name
        if approved.get(name) != sha256_file(path):
            raise StateError(f"reviewed file changed after approval: {name}")


def advance(
    episode_id: str,
    target_stage: str,
    evidence: str,
    next_action: str,
    root: Path = ROOT,
) -> dict[str, Any]:
    if not evidence.strip():
        raise StateError("stage transition requires evidence")
    if not next_action.strip():
        raise StateError("stage transition requires an exact next action")
    current = load_state(episode_id, root)
    if current["run_status"] == "ABANDONED_BY_USER":
        raise StateError("episode was abandoned by user")
    if current["run_status"] == "DONE":
        raise StateError("episode is already DONE")
    if current["run_status"] == "BLOCKED_RETRYABLE":
        raise StateError("resume the retryable block before advancing")

    ordered = stages(root)
    try:
        current_index = ordered.index(current["stage"])
        target_index = ordered.index(target_stage)
    except ValueError as exc:
        raise StateError("current or target stage is not in policy") from exc
    if target_index != current_index + 1:
        raise StateError(
            f"invalid transition {current['stage']} -> {target_stage}; "
            f"expected {ordered[current_index + 1] if current_index + 1 < len(ordered) else 'none'}"
        )

    if (
        int(current.get("protocol_revision", 1)) >= 2
        and current["stage"] == "PREPRODUCTION_REVIEW"
        and target_stage == "SOURCE_LOCK"
    ):
        _require_editorial_hash_lock(episode_id, root)

    current["stage_history"].append(
        {
            "at": utc_now(),
            "from": current["stage"],
            "to": target_stage,
            "evidence": evidence.strip(),
        }
    )
    current["stage"] = target_stage
    current["exact_next_action"] = next_action.strip()
    if target_stage == "DONE":
        current["run_status"] = "DONE"
    atomic_write_json(state_path(episode_id, root), current)
    return current


def block(
    episode_id: str,
    code: str,
    detail: str,
    resume_action: str,
    root: Path = ROOT,
) -> dict[str, Any]:
    allowed = set(policy(root)["execution"]["retryable_states"])
    if code not in allowed:
        raise StateError(f"not a configured retryable block code: {code}")
    if not detail.strip() or not resume_action.strip():
        raise StateError("block detail and resume action are required")
    current = load_state(episode_id, root)
    if current["run_status"] in {"DONE", "ABANDONED_BY_USER"}:
        raise StateError("terminal episode cannot be blocked")
    current["run_status"] = "BLOCKED_RETRYABLE"
    current["blocked"] = {
        "code": code,
        "detail": detail.strip(),
        "resume_action": resume_action.strip(),
        "recorded_at": utc_now(),
    }
    current["exact_next_action"] = resume_action.strip()
    atomic_write_json(state_path(episode_id, root), current)
    return current


def resume(episode_id: str, evidence: str, root: Path = ROOT) -> dict[str, Any]:
    current = load_state(episode_id, root)
    if current["run_status"] != "BLOCKED_RETRYABLE" or not current.get("blocked"):
        raise StateError("episode is not retryably blocked")
    if not evidence.strip():
        raise StateError("resume requires recovery evidence")
    previous = current["blocked"]
    current["run_status"] = "ACTIVE"
    current["blocked"] = None
    current["stage_history"].append(
        {
            "at": utc_now(),
            "from": current["stage"],
            "to": current["stage"],
            "evidence": f"resumed {previous['code']}: {evidence.strip()}",
        }
    )
    atomic_write_json(state_path(episode_id, root), current)
    return current


def register_file_artifact(
    episode_id: str,
    role: str,
    file_path: Path,
    producing_dispatch: str | None = None,
    root: Path = ROOT,
) -> dict[str, Any]:
    resolved_root = root.resolve()
    resolved = file_path.resolve()
    try:
        relative = resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise StateError("artifact must be inside the AIToon repository") from exc
    if not resolved.is_file():
        raise StateError(f"artifact file missing: {resolved}")

    width = height = None
    if resolved.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        try:
            from PIL import Image

            with Image.open(resolved) as image:
                width, height = image.size
        except Exception as exc:  # Pillow reports useful format errors inconsistently.
            raise StateError(f"cannot inspect image artifact: {resolved}: {exc}") from exc

    artifact = {
        "artifact_id": f"A{len(load_state(episode_id, root)['artifacts']) + 1:04d}",
        "role": role,
        "path": relative.as_posix(),
        "sha256": sha256_file(resolved),
        "size_bytes": resolved.stat().st_size,
        "width": width,
        "height": height,
        "producing_dispatch": producing_dispatch,
        "registered_at": utc_now(),
    }
    current = load_state(episode_id, root)
    duplicate = next((x for x in current["artifacts"] if x["path"] == artifact["path"]), None)
    if duplicate and duplicate["sha256"] != artifact["sha256"]:
        raise StateError("artifact path changed bytes; create a new versioned path")
    if not duplicate:
        current["artifacts"].append(artifact)
        atomic_write_json(state_path(episode_id, root), current)
    return duplicate or artifact

