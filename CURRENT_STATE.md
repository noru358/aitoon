# Current state

Updated: 2026-09-08 00:12 KST  
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
- paid API/SaaS fallback remains disabled;
- reference authority is repository path/SHA/registry metadata; image-runtime carriers are session-only transport;
- every reference-consuming image call requires runtime-attachment preflight on the current surface;
- direct repository transport is preferred; only after that bridge is unavailable may a matching current-session Chat/Work attachment carry an already locked reference;
- startup or mid-run attachments never reset the active episode, stage, or exact-next-action pointer, and attachment preflight is repeated after session/surface changes.

Calibration attempt 1 remains rejected and quarantined. Calibration attempt 2
remains the accepted calibration board only; its convenience-store story is a
fixture and is not E001 content.

## Active production

Publishable episode: `E001 / 지금! 지금!`

Stage: `DONE`

Run status: `DONE`

Active episode: `E002 / 그냥 세탁기에 돌려도 되는데`

Stage: `BOARD_DISPATCH_READY`

Run status: `BLOCKED_RETRYABLE`

Block code: `WAITING_TOOL_RECOVERY`

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
- repository validation/regression workflow passed for `669d52c2456c68d0c138e8b061741444a16fc081` after the board dispatch commit;
- the current ChatGPT tool surface cannot hand the already retrieved GitHub repository JPEG bytes to built-in image generation as actual attached media, so the episode is retryably blocked rather than generating unreferenced art;
- E002-B01-MASTER-A1 now carries an explicit session-scoped runtime-attachment contract: direct repository transport first, current-session Chat/Work attachment fallback only after direct bridge failure, and mandatory re-preflight after session/surface changes;
- a transport attachment is mapped back to the locked D/E registry roles and never becomes new style authority or a reason to reset the episode/stage;
- future copy is recorded in storyboard metadata but no lettering is permitted in art.

## Boot/reference guard maintenance

- canonical boot authority is now singular: `AGENTS.md -> CURRENT_STATE.md -> docs/GPT_APP_PROTOCOL.md -> config/policy.json -> active episode state.json`; README is descriptive only;
- after the active episode is known, `state.json.exact_next_action` is the production execution pointer;
- registered production-eligible reference bytes must be retrieved from `aitoon` before any request for new reference evidence;
- when valid repository bytes cannot be bridged into the current image runtime, a user-supplied/current-session copy of the already locked reference is allowed only as SESSION_ONLY transport fallback; it does not alter authority, episode, stage, or exact-next-action;
- sufficient registry coverage means an episode-local one-off character may receive a distinct new identity inside the PRIMARY_STYLE drawing language without a dedicated new identity image or independent authorship proof;
- E002's stale character notes that incorrectly implied future verified human-drawn identity evidence were removed; its stage and exact next action remain unchanged.

## Reference policy

The production-eligible D/E files already exist in the repository and are
registered as user-designated `PRIMARY_STYLE` references. Independent authorship
verification remains explicitly unasserted; it is not fabricated or treated as a
routine production gate. E002 is therefore active rather than waiting for bytes.

E002 has retrieved and inspected those actual repository bytes and bound D/E as the
minimum sufficient set by path, SHA-256, role, `allowed_influence` and
`forbidden_inference`. The B01 plan/dispatch is compiled. The remaining blocker is
only the current session's missing GitHub-binary-to-built-in-image media handoff.
Repository D/E remain authority. If direct transport is still unavailable, matching
D/E images supplied in the current Chat/Work session may carry those locked references
to the image runtime without becoming new references or resetting state.

## Runtime attachment guard

- `VISUAL_PACKET_LOCK` proves reference authority/coverage/bytes; it does not prove current-session image-runtime attachability.
- Compiled dispatches carry a `runtime_attachment` contract, but opaque runtime handles are not durable repository state.
- Immediately before every reference-consuming image call, preflight the current surface and revalidate after any session/Work/surface change.
- Preferred lane: `REPOSITORY_DIRECT`.
- Fallback lane after direct bridge failure: matching `CURRENT_SESSION_ATTACHMENT` or `WORK_RUNTIME_FILE`, mapped only to the already locked registry SHA/role.
- A startup attachment is transport, not a new task. Boot and `state.json.exact_next_action` still control production.
- Valid repo bytes plus no usable runtime carrier = `WAITING_TOOL_RECOVERY`; missing/corrupt repo bytes = `WAITING_REQUIRED_BYTES`.

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

Resume E002 at `BOARD_DISPATCH_READY` from latest `main`. Re-read and SHA-verify the locked D/E references, then run runtime-attachment preflight on the current Chat/Work surface immediately before dispatch. Prefer direct repository-to-image-runtime binding. If that bridge is unavailable and matching D/E images are already present in the current session/Work runtime, use them only as SESSION_ONLY carriers mapped to the locked registry roles; do not change `visual_packet.json`, episode, stage, story, or authority. Re-run preflight after every session/surface change. Once both carriers are actually accepted by the image runtime, resume the retryable block and dispatch `E002-B01-MASTER-A1` exactly once, import/register `episodes/E002/boards/B01.master.png`, and advance exactly to `MASTER_BOARD_IMPORTED`.

If no direct bridge and no eligible current-session carrier is available, remain `WAITING_TOOL_RECOVERY`. Do not generate unreferenced art and do not use paid API/SaaS fallback.
