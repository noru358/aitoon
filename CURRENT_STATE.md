# Current state

Updated: 2026-09-08 00:53 KST  
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

Stage: `MASTER_BOARD_QC`

Run status: `BLOCKED_RETRYABLE`

Block code: `WAITING_TOOL_RECOVERY`

Completed for E002:

- `SOURCE_LOCK`, `STORY_LOCK`, `STORYBOARD_LOCK`, `VISUAL_PACKET_LOCK` and `BOARD_DISPATCH_READY` remain locked and unchanged;
- repository D/E PRIMARY_STYLE JPEG bytes were re-read from latest main and SHA-256 verified exactly: D `dbddf458...` at 1448x1086 and E `b496832...` at 1536x864;
- the two user attachments in this session were verified to be byte-for-byte matches of those same locked D/E files, so they were mapped only as `SESSION_ONLY` carriers after the direct repository-to-image-runtime bridge remained unavailable;
- `E002-B01-MASTER-A1` produced an actual image, which was imported, inspected, hard-failed board-wide, and quarantined because it copied the three reference characters/living-room activity instead of the locked two-character denim/laundry story, omitted the jeans state sequence, repeated the same group staging, and contained baked Latin `Z` marks;
- the rejected A1 canonical board path was removed after preserving the immutable quarantine copy;
- one whole-board retry dispatch `E002-B01-MASTER-A2` was compiled without changing story, storyboard, visual packet or reference authority;
- the current image execution surface did not honor that compiled A2 target either and returned another reference-trio living-room scene. The pixels were inspected and quarantined as a rejected tool-mismatch output. It is not eligible as style, continuity, repair or board evidence;
- `episodes/E002/boards/B01.qc.json` and `episodes/E002/state.json` now record the retryable tool block at `MASTER_BOARD_QC`.

The episode is not `DONE`. No rejected image may be reused.

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

E002 has retrieved and inspected those actual repository bytes and bound D/E as the minimum sufficient set by path, SHA-256, role, `allowed_influence` and `forbidden_inference`. The current session carriers matched the repository bytes exactly, so reference transport itself is no longer the active blocker. The active blocker is the current image execution surface returning a task-mismatched image instead of the compiled B01 target. Both bad outputs are quarantined and cannot be reused.


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

Resume E002 at `MASTER_BOARD_QC` from latest `main`. Re-read `references/registry.json`, the locked D/E bytes, `episodes/E002/boards/B01.qc.json`, and `episodes/E002/boards/B01.dispatch.A2.json`. Retry only after the built-in image execution surface is functioning normally for the compiled target; re-run runtime attachment and dispatch preflight first. Keep the D/E references as the same locked authority and use any matching session copies only as `SESSION_ONLY` carriers. Do not use either quarantined image. When a returned A2 board actually matches the locked two-character denim/laundry specification, import it as the canonical `episodes/E002/boards/B01.master.png`, inspect actual pixels, and advance exactly according to board QC. Do not use paid API/SaaS fallback.
