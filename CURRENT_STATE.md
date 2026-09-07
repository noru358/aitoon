# Current state

Updated: 2026-09-07 19:26 KST  
Repository: `noru358/aitoon`  
Architecture: `GPT_APP_BOARD_FIRST_V1`

## Production default

`GPT_APP_BOARD_FIRST_V1` is locked as the production default after the accepted
board-first calibration.

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

Active episode: `E001`  
Title: `그냥 세탁기에 돌려도 되는데`  
Stage: `STORYBOARD_LOCK`  
Run status: `ACTIVE`

Completed for E001:

- `SOURCE_LOCK`: direct Korean TeamBlind human story seed dated 2025-02-24;
- `STORY_LOCK`: four-beat sweet-romance adaptation preserving the stained denim,
  casual laundry request, online research, hand-wash and cute discovery;
- `STORYBOARD_LOCK`: four slide contracts with state deltas, beat-serving cameras,
  anatomy/contact intent, phone front/back geometry, continuity and text-safe regions;
- future copy is recorded in storyboard metadata but no lettering is permitted in art.

## Reference-policy correction

The earlier E001 `WAITING_REQUIRED_BYTES` block was over-conservative and is
cleared. The actual D/E reference bytes already exist in the repository and are
hash-bound.

Canonical rules now are:

- user/project designation is sufficient production provenance unless conflicting
  evidence exists; independent authorship verification is recorded separately;
- existing repository bytes must be retrieved by the operator before declaring
  `WAITING_REQUIRED_BYTES`;
- required visual roles are coverage requirements, not one-file-per-role quotas;
- generated approved art is `EPISODE_LOCAL` by default and may become only a
  `CONTINUITY_ANCHOR` after explicit user pixel approval, objective QC PASS and
  nonredundant continuity value;
- continuity anchors never override `PRIMARY_STYLE`;
- dispatches use the minimum sufficient reference set rather than accumulating all
  approved episode images.

The curated production authority is `references/registry.json`. The existing D/E
files remain stored under `calibration/references/` and are active
`PRIMARY_STYLE` references; duplicating the binary files is unnecessary.

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
- E001 S02 and S04 now carry scoped contracts. S04 is staged immediately after
  the handoff so the girlfriend owns the folded jeans while the boyfriend's
  sheepish gesture no longer competes for the same prop.

## Exact next action

Resolve the production-eligible D/E entries from `references/registry.json`,
retrieve and inspect their actual repository bytes, bind the minimum sufficient set
in `episodes/E001/visual_packet.json` with path/SHA-256/role/allowed_influence/
forbidden_inference, and advance exactly to `VISUAL_PACKET_LOCK`.

Do not require three separate reference files when the actual D/E pixels cover
multiple roles. Do not generate B01 until those actual bytes are bound. After
`VISUAL_PACKET_LOCK`, compile the text-free 2x2 B01 dispatch and continue the
canonical board-first, slide-final pipeline.

See `episodes/E001/state.json` for the machine resume record.
