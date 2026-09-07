# Current state

Updated: 2026-09-08 03:20 KST  
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

- Connector-side static V2 consistency check: PASS for the machine policy, schemas,
  E002 review/state/storyboard/visual-packet migration, and superseded A2 dispatch.
- A fresh local checkout was attempted for the canonical regression commands, but
  the execution sandbox could not resolve `github.com`; therefore
  `python -m unittest discover -s tests -p 'test_*.py'` and
  `python -m pipeline.cli validate` were **not executed locally** and are not
  claimed PASS.
- The latest GitHub commit exposed no combined status checks at the time inspected.
  This absence is recorded as unknown validation state, not success.
- Additional static hardening was added so a V2 master-board dispatch cannot compile
  before `VISUAL_PACKET_LOCK` (except bounded retry compilation at
  `MASTER_BOARD_QC`).

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
Stage: `BOARD_DISPATCH_READY`  
Run status: `ACTIVE`

Completed in the current V2 run:

- the presented `PREPRODUCTION_REVIEW` was explicitly user-approved and
  `source.md`, `story.md`, and `storyboard.json` were SHA-256 hash-bound in
  `episodes/E002/editorial_review.json`;
- the state advanced sequentially through `SOURCE_LOCK -> STORY_LOCK -> STORYBOARD_LOCK`
  without changing the approved files;
- both registered PRIMARY_STYLE JPEGs were re-read from latest main and verified
  byte-for-byte against registry SHA-256 and dimensions;
- `visual_packet.json` is now `LOCKED` with V2-narrowed reference influence,
  lowest-sufficient background policy, multidimensional style QC dimensions, and
  distinct episode-local GF/BF appearance text;
- the user's current-session 2x2 preview was visually approved provisionally and
  its observed hash/gen-id/dimensions are recorded only as session feedback. It is
  **not** canonical master-board evidence, not persistent reference authority, and
  does not replace PRIMARY_STYLE;
- a fresh V2 board plan and dispatch were compiled:
  `episodes/E002/boards/B01.plan.v2.json` and
  `episodes/E002/boards/B01.v2.A1.dispatch.json`;
- the active dispatch ID is `E002-B01-V2-MASTER-A1`;
- the fresh dispatch includes target cast definitions, state/continuity contracts,
  lowest-sufficient background levels, S02 phone geometry, conditional anatomy
  contracts, and explicit S01/S04 face-acting separation;
- the legacy V1 A1 and A2 dispatches are marked `SUPERSEDED` and ineligible for
  execution; rejected/quarantined prior outputs remain non-reusable.

The Chat durable boundary `BOARD_DISPATCH_READY` has been reached. No canonical
V2 image call has been executed after this boundary yet.

## Execution surfaces

- Chat durable boundaries:
  `PREPRODUCTION_REVIEW -> BOARD_DISPATCH_READY -> ART_SEQUENCE_QC -> DONE`.
- Work stops at an unapproved preproduction review by default; after approval it
  prefers one-shot execution to DONE or a real retryable block.
- A continuation token is not a substitute for an unpresented editorial review.

## Exact next action

Execute only `episodes/E002/boards/B01.v2.A1.dispatch.json` after current-surface
runtime-attachment preflight. Prefer repository-direct binding of the verified D/E
PRIMARY_STYLE bytes; if that bridge is unavailable, use matching current-session
copies only as `SESSION_ONLY` transport.

Do not execute the superseded V1/A2 dispatches and do not treat the previously
user-approved session preview as canonical board evidence. Import the returned 2x2
V2 board, inspect actual pixels for text contamination, target cast, anatomy/contact,
phone geometry, jeans state continuity, lowest-sufficient background use, style
dimensions, and S01/S04 acting separation, then advance exactly through
`MASTER_BOARD_IMPORTED -> MASTER_BOARD_QC`.
