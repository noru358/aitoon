# Current state

Updated: 2026-09-07 19:26 KST  
Repository: `noru358/aitoon`  
Architecture: `GPT_APP_BOARD_FIRST_V1`

## Production default

- canonical GPT-app-only production protocol;
- zero-paid-fallback machine policy;
- fail-closed episode state machine with retryable resource states;
- hash-bound reference/dispatch compiler;
- clean 2x2 board to separate 1080x1350 slide extractor;
- hash-bound editable Korean lettering renderer;
- repository/calibration validator and regression tests;
- read-only benchmark and calibration references copied into this repository;
- live calibration dispatch compiled and both bounded attempts executed;
- first publishable episode completed end-to-end with one built-in master-board
  generation, deterministic splitting, lettering, QC and export.

- internal coherence unit: text-free 2x2 master board, up to four occupied 4:5 cells;
- delivery unit: one separate 1080x1350 PNG per slide;
- approved board cells are split/expanded rather than independently reinterpreted;
- isolated failures are repaired at the smallest failed unit;
- lettering and meaning-bearing UI are added only after art lock;
- paid API/SaaS fallback remains disabled.

Calibration attempt 1 remains rejected and quarantined. Calibration attempt 2
remains the accepted calibration board only; its convenience-store story is a
fixture and is not E001 content.

## Active production

Publishable episode: `E001 / 지금! 지금!`

Stage: `DONE`

Run status: `DONE`

Next draft: `E002 / 그냥 세탁기에 돌려도 되는데`

Stage: `STORYBOARD_LOCK`

Run status: `ACTIVE`

Completed for E002:

- `SOURCE_LOCK`: direct Korean TeamBlind human story seed dated 2025-02-24;
- `STORY_LOCK`: four-beat sweet-romance adaptation preserving the stained denim,
  casual laundry request, online research, hand-wash and cute discovery;
- `STORYBOARD_LOCK`: four slide contracts with state deltas, beat-serving cameras,
  anatomy/contact intent, phone front/back geometry, continuity and text-safe regions;
- future copy is recorded in storyboard metadata but no lettering is permitted in art.

## Reference policy

The production-eligible D/E files already exist in the repository and are
registered as user-designated `PRIMARY_STYLE` references. Independent authorship
verification remains explicitly unasserted; it is not fabricated or treated as a
routine production gate. E002 is therefore active rather than waiting for bytes.

Before its image dispatch, E002 must retrieve and inspect those actual bytes and
bind the minimum sufficient reference set by path, SHA-256, role,
`allowed_influence` and `forbidden_inference`.

## Anatomy/contact guard update

A conditional high-risk manual-action guard is now part of the production
architecture via `docs/ANATOMY_CONTACT_POLICY.md`.

- it activates only when limb ownership/contact is genuinely ambiguous;
- it does not require two visible hands in every shot;
- it does not impose a global action-count cap;
- story-bearing prop/device contact outranks decorative gesture;
- risky shots may declare semantic limb roles, required contacts, forbidden
  extra/disconnected limbs, and a simplification fallback;
- the board dispatch compiler carries a declared `anatomy_contract` into the
  generation prompt;
- E002 S02 and S04 carry scoped contracts. S04 is staged immediately after
  the handoff so the girlfriend owns the folded jeans while the boyfriend's
  sheepish gesture no longer competes for the same prop.

## Publishable episode E001

`E001 / 지금! 지금!` is complete and its evidence-bound state is `DONE`.

- source: anonymous Korean community travel anecdote published on Theqoo on
  2024-11-07 (`https://theqoo.net/china/3476715206`);
- adaptation: a traveller's basic Chinese vanishes when a Shanghai cafe clerk
  asks how to serve a grape drink, producing the repeated Korean reply
  `지금! 지금!` and the clerk's correction `시엔짜이!`;
- generation: one text-free 2x2 master board made with ChatGPT built-in image
  generation and three inspected, hash-bound repository references;
- packaging: four separately inspected 1080x1350 art slides, followed by
  deterministic Korean lettering and four ordered 1080x1350 exports;
- result: master-board, art-sequence, lettering and final-pixel QC all pass;
- evidence: `episodes/E001/state.json`, `episodes/E001/boards/B01.qc.json`,
  `episodes/E001/qc/art_sequence.json`, `episodes/E001/qc/final.json` and
  `episodes/E001/export/manifest.json`.

E001 was generated from the user-approved calibration style anchors before the
production registry was formalized. Its inspected pixels and evidence remain
publishable. Its generated assets stay episode-local and do not replace primary
style authority.

No paid API or paid fallback was used. `instatoon`, `AutoPipeline` and `jipbap`
were not edited.

## Exact next action

Publish `episodes/E001/export/S01.png` through `S04.png` in order. To continue
E002, resolve D/E from `references/registry.json`, inspect and hash-check their
actual repository bytes, bind the minimum sufficient set in
`episodes/E002/visual_packet.json`, then advance to `VISUAL_PACKET_LOCK` and
compile B01. Keep `GPT_APP_BOARD_FIRST_V1` as the production default.
