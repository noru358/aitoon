from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .board import BoardError, split_master_board
from .dispatch import DispatchError, compile_master_board_dispatch
from .lettering import LetteringError, render_lettering
from .state import ROOT, StateError, advance, block, init_episode, load_state, register_file_artifact, resume
from .validate import ValidationError, validate_repository


def _print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AIToon GPT-app-native production state manager")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize an episode package")
    init.add_argument("episode_id")
    init.add_argument("--title", required=True)
    init.add_argument("--slides", required=True, type=int)

    status = sub.add_parser("status", help="show current episode state")
    status.add_argument("episode_id")

    move = sub.add_parser("advance", help="move exactly one canonical stage")
    move.add_argument("episode_id")
    move.add_argument("--to", required=True)
    move.add_argument("--evidence", required=True)
    move.add_argument("--next-action", required=True)

    blocked = sub.add_parser("block", help="record a retryable resource/tool block")
    blocked.add_argument("episode_id")
    blocked.add_argument("--code", required=True)
    blocked.add_argument("--detail", required=True)
    blocked.add_argument("--resume-action", required=True)

    resumed = sub.add_parser("resume", help="resume after a retryable block")
    resumed.add_argument("episode_id")
    resumed.add_argument("--evidence", required=True)

    artifact = sub.add_parser("register-artifact", help="hash-bind a repository file to episode state")
    artifact.add_argument("episode_id")
    artifact.add_argument("--role", required=True)
    artifact.add_argument("--path", required=True)
    artifact.add_argument("--dispatch")

    split = sub.add_parser("split-board", help="split a clean 2x2 master board into 4:5 slides")
    split.add_argument("--input", required=True)
    split.add_argument("--plan", required=True)
    split.add_argument("--output-dir", required=True)
    split.add_argument("--width", type=int, default=1080)
    split.add_argument("--height", type=int, default=1350)
    split.add_argument("--manifest")

    compile_dispatch = sub.add_parser("compile-board-dispatch", help="compile a hash-bound built-in image prompt")
    compile_dispatch.add_argument("episode_id")
    compile_dispatch.add_argument("--plan", required=True)
    compile_dispatch.add_argument("--output", required=True)
    compile_dispatch.add_argument("--attempt", type=int, default=1)

    lettering = sub.add_parser("render-lettering", help="render a hash-bound editable lettering plan")
    lettering.add_argument("--plan", required=True)
    lettering.add_argument("--output", required=True)
    lettering.add_argument("--receipt")

    sub.add_parser("validate", help="fail-closed repository validation")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            _print_json(init_episode(args.episode_id, args.title, args.slides))
        elif args.command == "status":
            _print_json(load_state(args.episode_id))
        elif args.command == "advance":
            _print_json(advance(args.episode_id, args.to, args.evidence, args.next_action))
        elif args.command == "block":
            _print_json(block(args.episode_id, args.code, args.detail, args.resume_action))
        elif args.command == "resume":
            _print_json(resume(args.episode_id, args.evidence))
        elif args.command == "register-artifact":
            path = Path(args.path)
            if not path.is_absolute():
                path = ROOT / path
            _print_json(register_file_artifact(args.episode_id, args.role, path, args.dispatch))
        elif args.command == "split-board":
            receipt = split_master_board(
                Path(args.input),
                Path(args.plan),
                Path(args.output_dir),
                args.width,
                args.height,
            )
            if args.manifest:
                manifest = Path(args.manifest)
                manifest.parent.mkdir(parents=True, exist_ok=True)
                manifest.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_json(receipt)
        elif args.command == "compile-board-dispatch":
            plan = Path(args.plan)
            output = Path(args.output)
            if not plan.is_absolute():
                plan = ROOT / plan
            if not output.is_absolute():
                output = ROOT / output
            _print_json(compile_master_board_dispatch(args.episode_id, plan, output, ROOT, args.attempt))
        elif args.command == "render-lettering":
            plan = Path(args.plan)
            output = Path(args.output)
            if not plan.is_absolute():
                plan = ROOT / plan
            if not output.is_absolute():
                output = ROOT / output
            receipt = render_lettering(plan, output, ROOT)
            if args.receipt:
                receipt_path = Path(args.receipt)
                if not receipt_path.is_absolute():
                    receipt_path = ROOT / receipt_path
                receipt_path.parent.mkdir(parents=True, exist_ok=True)
                receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            _print_json(receipt)
        elif args.command == "validate":
            checked = validate_repository()
            print("AITOON_VALID " + " ".join(checked))
        else:  # pragma: no cover
            raise StateError(f"unsupported command: {args.command}")
    except (StateError, BoardError, DispatchError, LetteringError, ValidationError, OSError, ValueError) as exc:
        print(f"AITOON_FAIL: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
