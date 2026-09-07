# Current state

Updated: 2026-09-08 03:04 KST  
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
Stage: `PREPRODUCTION_REVIEW`  
Run status: `ACTIVE`

The previous E002 visual packet and A2 board dispatch are superseded. All rejected
master-board/runtime outputs remain quarantine-only and cannot be reused.

E002 has been reopened as a reviewable V2 draft:

- source remains the same traceable TeamBlind post;
- four narrative beats remain;
- decorative backgrounds are reduced to the lowest sufficient level;
- S02 uses a boyfriend thought instead of adding environmental exposition;
- S04 uses a girlfriend thought for the source-derived landing;
- S01 and S04 now declare different face-acting intents so a copied facial template
  is a QC failure;
- a separate cover concept is drafted from S04-style approved art rather than a new
  independent illustration.

No image dispatch is eligible until this review is approved and the source/story/
storyboard hashes are locked.

## Execution surfaces

- Chat durable boundaries:
  `PREPRODUCTION_REVIEW -> BOARD_DISPATCH_READY -> ART_SEQUENCE_QC -> DONE`.
- Work stops at an unapproved preproduction review by default; after approval it
  prefers one-shot execution to DONE or a real retryable block.
- A continuation token is not a substitute for an unpresented editorial review.

## Exact next action

Present the E002 `PREPRODUCTION_REVIEW` to the user in one compact package:
source/topic, premise, four beats, all dialogue/thought copy, background plan, and
cover concept. Accept edits or explicit approval. Do not execute image generation.

After explicit approval, record the exact hashes in
`episodes/E002/editorial_review.json`, advance exactly to `SOURCE_LOCK`, then
continue sequentially through story/storyboard locks, rebuild a `LOCKED` visual
packet, and compile a new V2 board dispatch. The superseded A2 dispatch must never
resume.
