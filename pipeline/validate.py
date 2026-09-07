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
    _require(data.get("architecture") == "GPT_APP_BOARD_FIRST_V2", "architecture revision drift")
    _require(data.get("protocol_revision") == 2, "protocol revision drift")
    execution = data.get("execution", {})
    _require(execution.get("additional_paid_budget_krw") == 0, "paid budget must be zero")
    _require(execution.get("paid_api_allowed") is False, "paid API must be disabled")
    _require(execution.get("paid_saas_allowed") is False, "paid SaaS must be disabled")
    _require(execution.get("ask_user_for_routine_approval") is False, "routine user gates must be disabled")
    _require(execution.get("terminal_states") == ["DONE", "ABANDONED_BY_USER"], "terminal state drift")
    modes = data.get("execution_modes", {})
    chat = modes.get("chat", {})
    work = modes.get("work", {})
    common = modes.get("common", {})
    _require(chat.get("strategy") == "BOUNDED_AUTONOMOUS_MULTI_TURN", "Chat execution strategy drift")
    _require(chat.get("routine_approval_required") is False, "Chat must not create routine approval gates")
    _require(chat.get("editorial_review_mode") == "USER_REQUIRED", "Chat must preserve the editorial user gate")
    _require(chat.get("continuation_token_is_approval") is False, "Chat continuation token cannot be an approval")
    _require(
        chat.get("durable_turn_boundaries") == ["PREPRODUCTION_REVIEW", "BOARD_DISPATCH_READY", "ART_SEQUENCE_QC", "DONE"],
        "Chat durable turn boundary drift",
    )
    _require(chat.get("boundary_checkpoint_required") is True, "Chat turn boundary must checkpoint repository state")
    _require(chat.get("response_boundary_is_state_machine_stage") is False, "response boundary cannot become a production stage")
    _require(chat.get("quality_gates_may_be_skipped_for_turn_budget") is False, "Chat turn budget cannot weaken quality gates")
    _require(work.get("strategy") == "ONE_SHOT_AFTER_EDITORIAL_APPROVAL_TO_DONE_OR_RETRYABLE_BLOCK", "Work execution strategy drift")
    _require(work.get("routine_approval_required") is False, "Work must not create routine approval gates")
    _require(work.get("editorial_review_mode") == "USER_REQUIRED_BY_DEFAULT", "Work editorial review policy drift")
    _require(work.get("stops_for_unapproved_editorial_review") is True, "Work must not bypass an unapproved editorial review")
    _require(work.get("stage_checkpoint_required") is True, "Work must preserve stage checkpoints")
    _require(work.get("quality_gates_may_be_skipped_for_execution_budget") is False, "Work execution budget cannot weaken quality gates")
    _require(common.get("same_production_state_machine") is True, "Chat and Work must share one state machine")
    _require(common.get("repository_state_is_cross_turn_authority") is True, "repository state must remain cross-turn authority")
    _require(common.get("canonical_boot_from_latest_main_each_turn") is True, "each execution turn must canonical-boot latest main")
    _require(common.get("conversational_summary_is_handoff_authority") is False, "conversation summary cannot become handoff authority")
    _require(common.get("load_only_exact_next_action_companions_after_boot") is True, "post-boot context must stay exact-next-action scoped")
    stages = data.get("stages")
    _require(isinstance(stages, list) and len(stages) == len(set(stages)), "stages must be unique")
    _require(stages[0] == "BOOTSTRAP" and stages[-1] == "DONE", "stage boundary drift")
    _require(stages[1] == "PREPRODUCTION_REVIEW", "editorial review stage drift")
    render = data.get("render", {})
    _require(render.get("default_lane") == "MASTER_BOARD", "master-board lane must remain default")
    _require(render.get("maximum_slides_per_board") == 4, "board capacity drift")
    _require(render.get("canonical_board_rows") == 2 and render.get("canonical_board_columns") == 2, "canonical board geometry drift")
    _require(render.get("runtime_sheet_strategy") == "NATURAL_OCCUPANCY", "runtime sheet strategy drift")
    _require(render.get("generator_empty_cells_forbidden") is True, "generator must not own empty canonical cells")
    _require(render.get("deterministic_pack_to_canonical_2x2") is True, "runtime sheet must pack deterministically")
    _require(
        render.get("runtime_sheet_layouts") == {
            "1": {"rows": 1, "columns": 1},
            "2": {"rows": 1, "columns": 2},
            "3": {"rows": 1, "columns": 3},
            "4": {"rows": 2, "columns": 2},
        },
        "runtime sheet layout drift",
    )
    product = data.get("product", {})
    _require(product.get("delivery") == "ONE_FILE_PER_SLIDE", "delivery contract drift")
    _require(product.get("narrative_slide_count_excludes_cover") is True, "cover must not change narrative slide_count")
    cover = product.get("cover", {})
    _require(cover.get("required_from_protocol_revision") == 2, "cover requirement drift")
    _require(cover.get("default_strategy") == "DERIVED_FROM_APPROVED_ART", "cover should default to approved-art derivation")
    design = data.get("visual_design", {})
    _require(design.get("background_default") == "LOWEST_SUFFICIENT", "background minimalism drift")
    _require(design.get("background_levels") == ["NONE", "SYMBOLIC", "LOCATION_ANCHOR", "FULL_SCENE"], "background level drift")
    _require(design.get("decorative_assets_default") == "OMIT", "decorative asset default drift")
    editorial = data.get("editorial", {})
    _require(editorial.get("stage") == "PREPRODUCTION_REVIEW", "editorial stage policy drift")
    _require(editorial.get("explicit_user_approval_required") is True, "editorial approval must be explicit")
    _require(editorial.get("approval_hash_binds") == ["source.md", "story.md", "storyboard.json"], "editorial hash binding drift")
    visual_approval = data.get("visual_approval", {})
    _require(visual_approval.get("explicit_visual_approval_is_operational") is True, "visual approval must affect production")
    _require(visual_approval.get("fresh_resampling_when_applicable_anchor_exists_forbidden") is True, "approved anchor cannot be discarded by fresh resampling")
    _require(visual_approval.get("objective_anatomy_contact_screen_text_failures_never_overridden") is True, "user aesthetic approval cannot waive objective defects")
    _require(visual_approval.get("missing_required_anchor_transport_fails_closed") is True, "missing approved anchor transport must fail closed")
    image_runtime = data.get("image_runtime", {})
    _require(image_runtime.get("art_only_context_required") is True, "image runtime must use art-only context")
    _require(image_runtime.get("compiled_dispatch_must_be_copy_free") is True, "image dispatch must be copy-free")
    _require(image_runtime.get("same_session_retry_after_semantic_noncompliance_forbidden") is True, "semantic misdispatch must not same-session retry")
    _require(image_runtime.get("recovery_after_semantic_noncompliance") == "WAITING_CLEAN_IMAGE_SESSION", "semantic misdispatch recovery drift")
    _require(image_runtime.get("stronger_same_session_prompt_escalation_forbidden") is True, "same-session prompt escalation must be disabled")
    runtime = data.get("runtime_attachment", {})
    _require(runtime.get("preflight_required_before_image_dispatch") is True, "runtime attachment preflight must be required")
    _require(runtime.get("revalidate_after_session_or_surface_change") is True, "runtime attachment must be session-revalidated")
    _require(runtime.get("persistent_authority") == "REPOSITORY_REGISTRY_SHA256", "runtime carrier cannot replace repository authority")
    _require(runtime.get("carrier_scope") == "SESSION_ONLY", "runtime carrier must remain session-only")
    _require(runtime.get("preferred_carrier") == "REPOSITORY_DIRECT", "repository-direct transport must remain preferred")
    _require(runtime.get("user_attachment_transport_fallback_allowed") is True, "session attachment transport fallback must remain allowed")
    _require(runtime.get("fallback_only_after_direct_runtime_bridge_unavailable") is True, "attachment fallback must not bypass an available direct bridge")
    _require(runtime.get("attachment_does_not_reset_episode_or_stage") is True, "attachment must not reset episode state")
    _require(runtime.get("opaque_runtime_handle_is_reference_authority") is False, "runtime handles must not become reference authority")
    _require(runtime.get("file_uri_alone_proves_image_binding") is False, "file URI alone cannot prove image-runtime binding")
    _require(runtime.get("approved_visual_anchor_carrier_allowed") is True, "approved visual anchor carrier must be supported")
    _require(runtime.get("approved_visual_anchor_manifest_is_authority") is True, "approved anchor manifest must remain repository authority")
    _require(runtime.get("anchor_carrier_must_match_manifest_sha256") is True, "approved anchor carrier must hash-match manifest")



def validate_lettering_style(root: Path = ROOT) -> None:
    data = read_json(root / "config" / "lettering_style.json")
    _require(data.get("schema_version") == "1.0", "lettering style schema drift")
    _require(data.get("style_id") == "AIT_V2_EDITORIAL_COMIC", "lettering style id drift")
    _require(data.get("status") in {"CALIBRATION_PENDING", "LOCKED"}, "bad lettering style status")
    roles = data.get("roles")
    _require(isinstance(roles, dict), "lettering role config missing")
    for role in ("DIALOGUE", "THOUGHT", "NARRATION", "SFX", "UI", "TITLE"):
        item = roles.get(role)
        _require(isinstance(item, dict), f"lettering role missing: {role}")
        bounds = item.get("font_size_range")
        _require(isinstance(bounds, list) and len(bounds) == 2 and 8 <= bounds[0] <= bounds[1] <= 220, f"bad lettering size range: {role}")


def _validate_editorial_review(root: Path, episode_dir: Path, episode_id: str, state: dict[str, Any]) -> None:
    revision = int(state.get("protocol_revision", 1))
    if revision < 2:
        return
    review_path = episode_dir / "editorial_review.json"
    _require(review_path.is_file(), f"{episode_id}: missing editorial_review.json")
    review = read_json(review_path)
    _require(review.get("episode_id") == episode_id, f"{episode_id}: editorial review id mismatch")
    _require(review.get("status") in {"PENDING", "APPROVED"}, f"{episode_id}: bad editorial review status")
    stages = policy(root)["stages"]
    if stages.index(state["stage"]) > stages.index("PREPRODUCTION_REVIEW"):
        _require(review.get("status") == "APPROVED", f"{episode_id}: advanced without editorial approval")
        approved = review.get("approved_hashes")
        _require(isinstance(approved, dict), f"{episode_id}: approved review lacks hashes")
        for name in ("source.md", "story.md", "storyboard.json"):
            _require(approved.get(name) == sha256_file(episode_dir / name), f"{episode_id}: reviewed file drift after approval: {name}")


def _validate_v2_storyboard(root: Path, episode_dir: Path, episode_id: str, state: dict[str, Any]) -> None:
    if int(state.get("protocol_revision", 1)) < 2:
        return
    stages = policy(root)["stages"]
    if stages.index(state["stage"]) < stages.index("PREPRODUCTION_REVIEW"):
        return
    storyboard = read_json(episode_dir / "storyboard.json")
    cover = storyboard.get("cover")
    _require(isinstance(cover, dict), f"{episode_id}: v2 storyboard cover is missing")
    for key in ("title", "visual_concept", "strategy"):
        _require(isinstance(cover.get(key), str) and cover[key].strip(), f"{episode_id}: cover {key} missing")
    _require(cover.get("strategy") in {"DERIVED_FROM_APPROVED_ART", "DEDICATED_COVER_ART_IF_NEEDED"}, f"{episode_id}: bad cover strategy")
    slides = storyboard.get("slides")
    _require(isinstance(slides, list) and len(slides) == state.get("slide_count"), f"{episode_id}: storyboard slide count mismatch")
    allowed_backgrounds = {"NONE", "SYMBOLIC", "LOCATION_ANCHOR", "FULL_SCENE"}
    allowed_copy_roles = {"DIALOGUE", "THOUGHT", "NARRATION", "SFX", "UI"}
    for slide in slides:
        sid = slide.get("slide_id", "?")
        level = slide.get("background_level")
        _require(level in allowed_backgrounds, f"{episode_id}/{sid}: bad or missing background_level")
        essential = slide.get("essential_background")
        _require(isinstance(essential, list) and all(isinstance(x, str) and x.strip() for x in essential), f"{episode_id}/{sid}: essential_background malformed")
        if level == "NONE":
            _require(not essential, f"{episode_id}/{sid}: NONE background cannot declare essential background assets")
        if level == "FULL_SCENE":
            _require(isinstance(slide.get("background_reason"), str) and slide["background_reason"].strip(), f"{episode_id}/{sid}: FULL_SCENE requires story reason")
        _require(isinstance(slide.get("face_acting_intent"), str) and slide["face_acting_intent"].strip(), f"{episode_id}/{sid}: face_acting_intent missing")
        _require(isinstance(slide.get("emotion_delta"), str) and slide["emotion_delta"].strip(), f"{episode_id}/{sid}: emotion_delta missing")
        copy = slide.get("copy")
        _require(isinstance(copy, list), f"{episode_id}/{sid}: copy must be a list")
        for item in copy:
            _require(item.get("role") in allowed_copy_roles, f"{episode_id}/{sid}: unsupported copy role")


def _validate_v2_cover_done(root: Path, episode_dir: Path, episode_id: str, state: dict[str, Any]) -> None:
    if int(state.get("protocol_revision", 1)) < 2 or state.get("run_status") != "DONE":
        return
    style = read_json(root / "config" / "lettering_style.json")
    _require(style.get("status") == "LOCKED", f"{episode_id}: DONE with unlocked lettering style")
    cover_file = episode_dir / "cover" / "final.png"
    manifest_path = episode_dir / "cover" / "manifest.json"
    _require(cover_file.is_file() or manifest_path.is_file(), f"{episode_id}: DONE without cover artifact")
    if manifest_path.is_file():
        manifest = read_json(manifest_path)
        _require(manifest.get("episode_id") == episode_id, f"{episode_id}: cover manifest episode mismatch")
        _require(bool(manifest.get("sha256") or manifest.get("stable_app_handle")), f"{episode_id}: cover manifest lacks evidence")



def _validate_approved_visual_anchor(root: Path, episode_dir: Path, episode_id: str) -> None:
    path = episode_dir / "approved_visual_anchor.json"
    if not path.is_file():
        return
    anchor = read_json(path)
    _require(anchor.get("schema_version") == "1.0", f"{episode_id}: approved visual anchor schema drift")
    _require(anchor.get("episode_id") == episode_id, f"{episode_id}: approved visual anchor episode mismatch")
    _require(anchor.get("status") in {"ACTIVE", "RETIRED"}, f"{episode_id}: bad approved visual anchor status")
    sha = anchor.get("sha256")
    _require(isinstance(sha, str) and len(sha) == 64, f"{episode_id}: approved visual anchor lacks SHA-256")
    _require(isinstance(anchor.get("allowed_influence"), str) and anchor["allowed_influence"].strip(), f"{episode_id}: approved anchor influence scope missing")
    _require(isinstance(anchor.get("forbidden_inference"), str) and anchor["forbidden_inference"].strip(), f"{episode_id}: approved anchor exclusions missing")
    _require(anchor.get("primary_style_promotion") is False, f"{episode_id}: episode anchor cannot silently promote to PRIMARY_STYLE")
    if anchor.get("status") == "ACTIVE":
        qc = anchor.get("objective_scope_qc")
        _require(isinstance(qc, dict), f"{episode_id}: active approved anchor lacks objective scope QC")
        _require(qc.get("actual_pixels_inspected") is True, f"{episode_id}: approved anchor pixels were not inspected")
        _require(qc.get("anchor_scope_status") == "PASS", f"{episode_id}: approved anchor scope is not PASS")
        repository_path = anchor.get("repository_path")
        if repository_path:
            resolved = (root / repository_path).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError as exc:
                raise ValidationError(f"{episode_id}: approved anchor escapes repository") from exc
            _require(resolved.is_file(), f"{episode_id}: approved anchor repository bytes missing")
            _require(sha256_file(resolved) == sha, f"{episode_id}: approved anchor repository hash mismatch")
        else:
            _require(
                anchor.get("transport_status") == "SESSION_CARRIER_REQUIRED_ON_CLEAN_SESSION",
                f"{episode_id}: active non-repository anchor lacks clean-session carrier requirement",
            )


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
    _validate_editorial_review(root, episode_dir, episode_id, state)
    _validate_v2_storyboard(root, episode_dir, episode_id, state)
    _validate_approved_visual_anchor(root, episode_dir, episode_id)
    for artifact in state.get("artifacts", []):
        _validate_artifact(root, artifact, episode_id)

    if state.get("run_status") != "DONE":
        for dispatch_path in sorted((episode_dir / "boards").glob("*.dispatch.json")):
            dispatch = read_json(dispatch_path)
            contract = dispatch.get("runtime_attachment")
            _require(isinstance(contract, dict), f"{episode_id}: active dispatch lacks runtime attachment contract")
            _require(contract.get("preflight_required_before_execute") is True, f"{dispatch_path}: runtime preflight not required")
            _require(
                contract.get("source_authority") in {"REPOSITORY_REGISTRY_SHA256", "REPOSITORY_MANIFEST_AND_SHA256"},
                f"{dispatch_path}: runtime authority drift",
            )
            _require(contract.get("carrier_scope") == "SESSION_ONLY", f"{dispatch_path}: runtime carrier scope drift")
            _require(contract.get("revalidate_after_session_or_surface_change") is True, f"{dispatch_path}: stale runtime binding may be reused")
            _require(contract.get("attachment_does_not_reset_episode_or_stage") is True, f"{dispatch_path}: attachment may not reset state")
            _require(contract.get("opaque_runtime_handle_is_reference_authority") is False, f"{dispatch_path}: runtime handle cannot become authority")
            if dispatch.get("status") == "READY" and dispatch.get("eligible_for_execution", True) is not False:
                runtime_sheet = dispatch.get("runtime_sheet")
                _require(isinstance(runtime_sheet, dict), f"{dispatch_path}: executable dispatch lacks runtime_sheet")
                _require(runtime_sheet.get("strategy") == "NATURAL_OCCUPANCY", f"{dispatch_path}: bad runtime sheet strategy")
                _require(runtime_sheet.get("generator_empty_cells_forbidden") is True, f"{dispatch_path}: generator owns empty cells")
                _require(runtime_sheet.get("pack_to_canonical_2x2") is True, f"{dispatch_path}: runtime sheet is not canonical-packable")
                context = dispatch.get("context_isolation")
                _require(isinstance(context, dict) and context.get("art_only") is True, f"{dispatch_path}: executable dispatch lacks art-only context isolation")
                _require(isinstance(contract.get("required_sha_carriers"), list), f"{dispatch_path}: required SHA carriers missing")
    _validate_qc_reports(root, episode_dir, episode_id)
    if state["run_status"] == "DONE":
        _require(state["stage"] == "DONE", f"{episode_id}: DONE status/stage mismatch")
        _validate_v2_cover_done(root, episode_dir, episode_id, state)
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
    validate_lettering_style(root)
    validate_reference_registry(root)
    validate_calibration(root)
    checked = ["policy", "lettering_style", "references", "calibration"]
    episodes = root / "episodes"
    if episodes.is_dir():
        for directory in sorted(path for path in episodes.iterdir() if path.is_dir()):
            validate_episode(directory, root)
            checked.append(directory.name)
    return checked
