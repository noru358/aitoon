# Current state

Updated: 2026-09-07 23:53 KST  
Repository: `noru358/aitoon`  
Architecture: `GPT_APP_BOARD_FIRST_V1`

## Production default

- canonical GPT-app-only production protocol;
- zero-paid-fallback machine policy;
- fail-closed episode state machine with retryable resource states;
- hash-bound reference/dispatch compiler;
- fixed 2x2 internal coherence board (one to four occupied cells; episode slide count remains variable) to separate 1080x1350 slide extractor;
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

Active episode: `E002 / 그냥 세탁기에 돌려도 되는데`

Stage: `BOARD_DISPATCH_READY`

Run status: `ACTIVE`

Completed for E002:

- `SOURCE_LOCK`: direct Korean TeamBlind human story seed dated 2025-02-24;
- `STORY_LOCK`: four-beat sweet-romance adaptation preserving the stained denim,
  casual laundry request, online research, hand-wash and cute discovery;
- `STORYBOARD_LOCK`: four slide contracts with state deltas, beat-serving cameras,
  anatomy/contact intent, phone front/back geometry, continuity and text-safe regions;
- `VISUAL_PACKET_LOCK`: actual D/E repository JPEG bytes retrieved, registry SHA-256 values
  verified exactly, JPEG structure/dimensions inspected, and the minimum sufficient
  production-eligible PRIMARY_STYLE set bound with explicit allowed/forbidden influence;
- `BOARD_DISPATCH_READY`: a single four-cell B01 plan and hash-bound A1 dispatch are compiled from the locks; D/E are the only bound media, S02 phone geometry and scoped anatomy contracts are carried into the prompt, and the board is required to remain text-free;
- future copy is recorded in storyboard metadata but no lettering is permitted in art.

## Boot/reference guard maintenance

- canonical boot authority is now singular: `AGENTS.md -> CURRENT_STATE.md -> docs/GPT_APP_PROTOCOL.md -> config/policy.json -> active episode state.json`; README is descriptive only;
- after the active episode is known, `state.json.exact_next_action` is the production execution pointer;
- registered production-eligible reference bytes must be retrieved from `aitoon` before any user re-upload request;
- sufficient registry coverage means an episode-local one-off character may receive a distinct new identity inside the PRIMARY_STYLE drawing language without a dedicated new identity image or independent authorship proof;
- E002's stale character notes that incorrectly implied future verified human-drawn identity evidence were removed; its stage and exact next action remain unchanged.

## Reference policy

The production-eligible D/E files already exist in the repository and are
registered as user-designated `PRIMARY_STYLE` references. Independent authorship
verification remains explicitly unasserted; it is not fabricated or treated as a
routine production gate. E002 is therefore active rather than waiting for bytes.

E002 has retrieved and inspected those actual repository bytes and bound D/E as the
minimum sufficient set by path, SHA-256, role, `allowed_influence` and
`forbidden_inference`. The next production step is board-plan/dispatch compilation;
no user re-upload or episode-local identity sheet is required.

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

Dispatch `episodes/E002/boards/B01.dispatch.json` through ChatGPT built-in image
generation with both bound D/E repository references supplied as actual media.
Generate exactly one TEXT-FREE 2x2 master board, persist/import the exact returned
bytes with SHA-256 and dimensions as `episodes/E002/boards/B01.master.png`, then
advance exactly to `MASTER_BOARD_IMPORTED`. If the built-in image runtime cannot
receive the bound repository media, record a retryable `WAITING_TOOL_RECOVERY`
block rather than generating unreferenced art.
