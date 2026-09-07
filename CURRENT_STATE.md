# Current state

Updated: 2026-09-08 03:32 KST  
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
Stage: `MASTER_BOARD_QC`  
Run status: `BLOCKED_RETRYABLE`  
Block: `WAITING_TOOL_RECOVERY`

Current V2 evidence:

- editorial approval remains hash-locked and unchanged;
- D/E PRIMARY_STYLE bytes remain verified and `visual_packet.json` remains `LOCKED`;
- canonical parent board `B01` A1 failed actual-pixel QC for baked text, style/cast drift,
  S02 phone geometry and extra-hand contact;
- the single allowed parent-board retry A2 improved S02 phone/back geometry and
  two-hand ownership, but still failed board-wide baked-text, style and GF cast
  appearance gates; there is no A3;
- per the repeated-structural-failure rule, B01 was decomposed into
  `B01D1(S01-S02)` then `B01D2(S03-S04)`, preserving board-first rather than
  switching to independent final-slide generation;
- current runtime execution of `B01D1` was a semantic misdispatch rather than a
  valid decomposed-board attempt: despite a two-cell top-row contract with both
  bottom cells EMPTY and zero text/symbols, the runtime generated all four beats,
  Korean speech/thought bubbles, a heart, the wrong bob-haired/shoulder-bag GF, and
  an extra S02 self-touch hand;
- D1 misdispatch actual pixels are recorded by stable handle
  `image_gen:8df5e643-7a44-4f35-a672-3b6e2e84a50d`, SHA-256
  `ae203c506ea214c836239d7a98519453c1488f336dba9f172b7b180f9109509b`,
  dimensions 1224x1285;
- receipt:
  `episodes/E002/quarantine/B01D1.runtime-misdispatch.receipt.json`;
- QC:
  `episodes/E002/qc/B01D1.runtime-misdispatch.json`.

The D1 target semantics were not executed, so the D1 attempt budget is not consumed.
Rejected A1/A2/D1 pixels are ineligible for style, continuity, or repair reuse.

## Execution surfaces

- Chat durable boundaries:
  `PREPRODUCTION_REVIEW -> BOARD_DISPATCH_READY -> ART_SEQUENCE_QC -> DONE`.
- Work stops at an unapproved preproduction review by default; after approval it
  prefers one-shot execution to DONE or a real retryable block.
- A continuation token is not a substitute for an unpresented editorial review.

## Exact next action

Retry the unchanged decomposed dispatch
`episodes/E002/boards/B01D1.dispatch.json` only after image-runtime tool recovery
or on a clean built-in image surface that demonstrably honors the current target
semantics.

Canonical-boot latest `main`, rerun D/E runtime-attachment preflight, keep the
parent B01 whole-board retry budget exhausted, and do not use any rejected
A1/A2/D1 output.

A valid D1 must:

- illustrate only S01 and S02 in the top row;
- leave both bottom cells EMPTY;
- contain zero text, bubbles, hearts, symbols or UI;
- preserve low-bun GF and BF episode-local appearances;
- preserve the same stained dry jeans;
- obey S02 phone-back geometry and exactly two BF hand roles;
- keep lowest-sufficient backgrounds;
- match PRIMARY_STYLE drawing grammar.

If D1 passes actual-pixel QC, continue to B01D2, derive slides only after both
decomposed boards pass, and then advance to `SLIDES_EXPANDED`. Do not attempt a
parent-board A3.
