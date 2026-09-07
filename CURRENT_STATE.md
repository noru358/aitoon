# Current state

Updated: 2026-09-08 04:04 KST  
Repository: `noru358/aitoon`  
Architecture: `GPT_APP_BOARD_FIRST_V2`

## Production default

The project has migrated from V1 to V2 after structural review of the first
publishable runs.

V2 keeps:

- GPT-app/Work built-in execution only;
- additional paid budget KRW 0;
- fail-closed repository state;
- hash-bound reference authority and SESSION_ONLY runtime transport;
- board-first, slide-final production;
- conditional anatomy/contact guard;
- actual-pixel visual QC;
- rejected/quarantined artifact non-reuse;
- one narrative file per 1080x1350 slide.

V2 adds:

- one real `PREPRODUCTION_REVIEW` before source/story/storyboard locks;
- explicit user review of topic, premise, slide count, beats, dialogue/interiority,
  and cover concept;
- hash-binding of the approved source/story/storyboard files;
- lowest-sufficient background levels and default omission of decorative assets;
- cover as a required packaging artifact separate from narrative `slide_count`;
- semantic text roles: dialogue, thought, narration, SFX, UI, title;
- project-level typography calibration/lock;
- multidimensional style QC rather than palette-only similarity;
- visible facial-acting change when a beat declares an emotional delta;
- style-reference identity/room copying forbidden unless separately explicit.

## Risk review and mitigation

The migration deliberately avoids several failure modes:

- **Over-minimal backgrounds:** V2 does not force blank backgrounds. It uses
  `NONE / SYMBOLIC / LOCATION_ANCHOR / FULL_SCENE`, and FULL_SCENE remains
  available when environment geometry carries story.
- **Approval fatigue:** only one per-episode creative gate is required. Reference
  hashing, image QC, repair, split, export, and validation remain autonomous.
- **Work-mode regression:** Work stops only for an unapproved editorial review;
  after approval it returns to one-shot execution toward DONE or a real retryable
  infrastructure block.
- **Breaking old completed work:** E001 is grandfathered as protocol revision 1.
  V2-only cover/editorial/typography requirements are enforced only for revision
  2+ episodes.
- **Cover increasing stochastic drift:** the default cover strategy is
  `DERIVED_FROM_APPROVED_ART`; dedicated cover generation is fallback only.
- **Typography lock blocking production:** art can proceed independently, but v2
  final lettering cannot PASS until the one-time project typography profile is
  actually user-approved and `LOCKED`.
- **Diversity hard-coding:** V2 does not require fixed camera or face-direction
  quotas. It rejects near-duplicate facial acting only when the story declares a
  meaningful emotional delta.
- **Style reference causing cast cloning:** production reference roles now narrow
  PRIMARY_STYLE influence to drawing grammar; exact reference identity and room
  content are forbidden unless explicitly bound.

## Validation status

- Connector-side static consistency check: **PASS** for the focused runtime-control
  revision across policy, E002 state, scoped approved-anchor manifest, clean D1
  dispatch, superseded legacy D1 dispatch, canonical plan, dispatch/packing code,
  validator hooks, runtime policy, reference policy, and regression-test sources.
- Regression coverage was updated for:
  - operational approved-anchor SHA carriers;
  - natural-occupancy runtime sheets;
  - absence of generator-owned EMPTY cells;
  - deterministic 1x2 -> canonical 2x2 packing;
  - clean-session policy invariants;
  - approved visual-anchor manifest validation.
  - native-pixel packing and explicit non-4:5 routing to board-bound expansion.
- A fresh local checkout was attempted again after these changes, but the execution
  sandbox still could not resolve `github.com`. Therefore the canonical commands
  `python -m unittest discover -s tests -p 'test_*.py'` and
  `python -m pipeline.cli validate` were **not executed locally** and are not
  claimed PASS.
- GitHub exposed no combined status checks or PR-triggered workflow runs for the
  queried latest indexed commit. Their absence is recorded as unknown validation
  state, not success.

## Typography state

`config/lettering_style.json` exists with status `CALIBRATION_PENDING`.

The previous generic Noto Sans KR treatment is therefore not treated as a final
approved design system. A future one-time typography calibration will lock the
font/profile before any V2 `LETTERING_COMPLETE` PASS.

## Publishable episode E001

`E001 / 지금! 지금!`

- protocol revision: legacy V1;
- state: `DONE`;
- existing final QC/export evidence remains valid;
- V2 migration does not retroactively invalidate it.

## Active episode E002

`E002 / 그냥 세탁기에 돌려도 되는데`

Protocol revision: 2  
Stage: `MASTER_BOARD_QC`  
Run status: `BLOCKED_RETRYABLE`  
Block: `WAITING_CLEAN_IMAGE_SESSION`

The latest structural review identified that the dominant current failure is not an
ordinary renderer outage. The current long conversation repeatedly produced
`RUNTIME_SEMANTIC_NONCOMPLIANCE`: forbidden Korean copy, wrong panel topology,
future beats outside the target batch, and cast-anchor drift.

The following changes are now authoritative:

- explicit user approval of visible pixels is operational rather than comment-only;
- the previously approved E002 preview is persisted in
  `episodes/E002/approved_visual_anchor.json` as an `EPISODE_LOCAL` anchor
  manifest with SHA-256
  `536d8a75f7d549faab5d0627d94a7862f3fa17c3a4784c94f5666e38b95cebbb`;
- its safe influence is scoped to GF/BF identity, hair, outfit, local palette and
  approved rendering treatment; known S02 phone geometry and all action/contact/
  layout/text details are explicitly excluded;
- an applicable approved anchor may no longer be silently replaced by fresh
  resampling;
- image execution is now art-only: once a dispatch is compiled, source prose,
  dialogue/thought/narration copy, lettering, cover copy and future beats are not
  loaded/restated into the image execution context;
- the image generator no longer owns empty canonical cells. Runtime batches use
  natural occupancy (1x1, 1x2, 1x3, or 2x2), then code deterministically packs a
  passing sheet into the canonical internal 2x2 board;
- deterministic packing preserves the runtime cells' native pixels/aspect ratio;
  it never stretches non-4:5 art to fit. Non-4:5 cells route to the existing
  board-bound expansion step for final 4:5 conversion;
- the old `B01D1.dispatch.json` is `SUPERSEDED`;
- the next executable target is
  `episodes/E002/boards/B01D1.clean.dispatch.json`, a two-cell 1x2 art-only sheet
  containing only S01 and S02;
- same-session prompt escalation after semantic noncompliance is forbidden.

Rejected A1/A2/D1 pixels remain ineligible for style, continuity or repair reuse.
The approved preview anchor is not a canonical master board and is not promoted to
project PRIMARY_STYLE; it is only a scoped episode continuity/rendering anchor.

## Execution surfaces

- Chat durable boundaries:
  `PREPRODUCTION_REVIEW -> BOARD_DISPATCH_READY -> ART_SEQUENCE_QC -> DONE`.
- Work stops at an unapproved preproduction review by default; after approval it
  prefers one-shot execution to DONE or a real retryable block.
- A continuation token is not a substitute for an unpresented editorial review.

## Exact next action

Start a **clean Chat/Work image execution session**. Canonical-boot latest
`main`, then load only:

- `docs/IMAGE_RUNTIME_POLICY.md`;
- `episodes/E002/boards/B01D1.clean.dispatch.json`;
- `episodes/E002/approved_visual_anchor.json`;
- the exact D/E registry entries;
- the actual D/E media and a current-session carrier whose SHA-256 matches the
  approved-anchor manifest.

Do **not** open or restate `source.md`, `story.md`, storyboard copy text,
dialogue/thought text, lettering plans, cover copy, S03/S04, or rejected images in
that image-execution session.

Revalidate all carrier hashes and execute exactly the 1x2 S01-S02 runtime sheet.
If it passes actual-pixel QC, deterministically pack it into the canonical 2x2 board,
then continue to D2. If a clean session still ignores topology/copy/anchor semantics,
do not retry again in that same session; checkpoint for renderer-strategy review.
