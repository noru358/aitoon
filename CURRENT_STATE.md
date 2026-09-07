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
- live calibration dispatch compiled and both bounded attempts executed.

## Calibration result

`BOARD_FIRST_V1 / B01` completed with `FAIL_HUMAN_DRAWN_STYLE` after the initial
generation and the single permitted whole-board retry.

- both actual 1122x1402 PNGs were inspected, hash-bound and quarantined;
- the board-first unit produced strong identity, outfit, palette, camera and
  story-state continuity;
- attempt 2 fixed the text-like packaging mark and ambiguous wallet;
- both attempts retained smooth, modeled, polished AI/webtoon finish beyond the
  references and therefore failed the human-drawn gate;
- neither rejected board was split, repaired, lettered, published, or reused as
  an input;
- paid API and paid fallback remain disabled.

See `calibration/FINDINGS.md` and the two structured QC reports. This calibration
does not consume publishable episode `E001`.

## Exact next action

Retain board-first as the coherence unit, but do not run a third `B01` prompt.
Assemble a provenance-verified multi-image human-authored visual packet with
separate line, flat-color, simplification, sparse-background and full-body
interaction anchors. Bind their hashes, assign a new calibration board ID, and
rerun the pilot using built-in ChatGPT image generation only.
