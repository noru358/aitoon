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

`BOARD_FIRST_V1 / B01` attempt 2 received explicit user visual approval and is
the accepted master board.

- both actual 1122x1402 PNGs were inspected and hash-bound;
- the board-first unit produced strong identity, outfit, palette, camera and
  story-state continuity;
- attempt 2 fixed the text-like packaging mark and ambiguous wallet;
- attempt 1 remains rejected and quarantined;
- attempt 2 is accepted because explicit user approval is authoritative for the
  subjective style gate;
- paid API and paid fallback remain disabled.

The accepted board has now been packaged into four separately inspected
1080x1350 PNG slides. All four passed crop, continuity, anatomy/contact,
no-generated-text and story-order checks. A hash-bound Korean lettering smoke
test also passed after correcting a one-line wrapping defect.

See `calibration/FINDINGS.md` and the two structured QC reports. This calibration
does not consume publishable episode `E001`.

## Exact next action

Lock `GPT_APP_BOARD_FIRST_V1` as the production default and initialize a fresh
publishable `E001` from a traceable Korean human story seed. The calibration
story remains fixture-only and must not be promoted as episode content.
