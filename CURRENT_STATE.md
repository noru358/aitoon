# Current state

Updated: 2026-09-07 18:36 KST  
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
Run status: `BLOCKED_RETRYABLE`  
Block code: `WAITING_REQUIRED_BYTES`

Completed for E001:

- `SOURCE_LOCK`: direct Korean TeamBlind human story seed dated 2025-02-24;
- `STORY_LOCK`: four-beat sweet-romance adaptation preserving the stained denim,
  casual laundry request, online research, hand-wash and cute discovery;
- `STORYBOARD_LOCK`: four slide contracts with state deltas, beat-serving cameras,
  anatomy/contact intent, phone front/back geometry, continuity and text-safe regions;
- future copy is recorded in storyboard metadata but no lettering is permitted in art.

## Fail-closed reference gate

Image generation is forbidden at the current state.

The repository has actual hash-bound calibration reference files, but
`calibration/references/registry.json` explicitly records that human-authorship
provenance is **not asserted** for them. Therefore they cannot satisfy the
production requirement for an actual provenance-verified human-drawn reference.

No rejected or quarantined generated artifact is eligible to repair this gap.

For this two-person home story, the production visual packet must bind actual
human-drawn evidence covering:

1. person/style drawing language;
2. interaction/full-body drawing language;
3. home/interior scene drawing language.

Each accepted reference must have actual inspectable bytes plus `path`,
`sha256`, `role`, `allowed_influence`, and `forbidden_inference`. The media
must also be available as actual image input to the ChatGPT image runtime; a
repository path or prose description alone is not conditioning.

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

Acquire and inspect provenance-verified actual human-drawn person/style,
interaction/full-body, and home/interior reference media as actual files usable by
the ChatGPT image runtime; copy only permitted bytes into `noru358/aitoon`,
record path/SHA-256/role/allowed_influence/forbidden_inference in
`episodes/E001/visual_packet.json`, exclude all rejected/quarantined/generated
artifacts from reference authority, then resume E001 and advance exactly to
`VISUAL_PACKET_LOCK` before compiling `B01`.

See `episodes/E001/state.json` for the machine resume record.
