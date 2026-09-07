# Current state

Updated: 2026-09-07  
Repository: `noru358/aitoon`  
Architecture: `GPT_APP_BOARD_FIRST_V1`

## Completed

- canonical GPT-app-only production protocol;
- zero-paid-fallback machine policy;
- fail-closed episode state machine with retryable resource states;
- hash-bound reference/dispatch compiler;
- clean 2x2 board to separate 1080x1350 slide extractor;
- hash-bound editable Korean lettering renderer;
- repository/calibration validator and regression tests;
- read-only benchmark and calibration references copied into this repository;
- live calibration dispatch compiled.

## Live calibration

The first built-in image generation call returned `usage_limit_reached`.

- state: `BLOCKED_RETRYABLE`
- code: `WAITING_INCLUDED_IMAGE_CAPACITY`
- paid fallback: disabled
- provider reset time returned by the app: `2026-09-07T08:23:37Z`
- exact resume action: run `calibration/B01.dispatch.json` with its two bound
  images through built-in image generation, then inspect the actual board.
- autonomous continuation: one-time ChatGPT Work task scheduled for
  `2026-09-07T09:12:05Z`, after the returned capacity reset time.

This is not a user approval gate and does not consume publishable episode `E001`.

## Decision after calibration

- PASS: lock board-first as production default and initialize fresh `E001`.
- board-wide identity/style FAIL after one retry: revise visual packet/reference
  roles, not the story prompt.
- isolated cell geometry FAIL: expand good cells and repair only the failed slide.
- repeated structural FAIL: retain GPT-app-only/cost policy, revise the render unit
  based on observed evidence; do not resurrect paid APIs or paper-doll composition
  by default.
