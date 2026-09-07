# AIToon operating contract

Architecture: `GPT_APP_BOARD_FIRST_V2`

## Canonical boot order

Use exactly one boot order for every fresh or resumed production run:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `docs/GPT_APP_PROTOCOL.md`
4. `config/policy.json`
5. the active episode's `state.json`, when an active episode exists
6. only then the companion material required by that active exact next action,
   including editorial, reference, anatomy/contact, visual-minimalism, lettering,
   registry, and actual reference/calibration files

`README.md` is descriptive only. Once an active episode exists,
`state.json.exact_next_action` is the execution pointer. Do not substitute
conversation memory or a guessed stage.

## Non-negotiable runtime

- `noru358/aitoon` is the only writable repository authority.
- `instatoon`, `AutoPipeline`, and `jipbap` are read/copy only.
- Additional paid budget is KRW 0. Do not use paid APIs, paid SaaS, or external
  paid image models as fallback.
- Routine technical approval is not required. Editorial approval is different:
  protocol revision 2 requires one `PREPRODUCTION_REVIEW` before source/story/
  storyboard locks become authoritative.
- Never fabricate editorial approval. The approved source/story/storyboard hashes
  must be recorded in `editorial_review.json`.
- Never claim visual PASS without actual-pixel inspection.
- Never reuse rejected/quarantined art as style, identity, continuity, or repair
  evidence.
- Registered reference authority and runtime transport are separate. Prefer
  repository-direct image binding; if unavailable, a matching current-session
  copy may carry the already locked reference as `SESSION_ONLY` transport.
- Runtime attachments never reset an episode, stage, review, or reference role.
- A style reference controls only its declared drawing-language influence.
  Reference-character identity, clothes, room, props, pose, or story must not be
  copied unless separately and explicitly bound.
- One published narrative slide is one 1080x1350 4:5 file. The cover is a separate
  packaging artifact and is not included in `slide_count`.

## V2 production behavior

1. Start from a traceable human-produced source.
2. Draft source, premise, slide count, beats, dialogue/thought/narration, cover
   concept, and storyboard before locking them.
3. For every slide choose the **lowest sufficient background**:
   `NONE`, `SYMBOLIC`, `LOCATION_ANCHOR`, or `FULL_SCENE`.
   Omit decorative assets by default.
4. Reach `PREPRODUCTION_REVIEW` and show the user one compact review containing
   source/topic, premise, all beats/copy, slide count, and cover concept.
5. After explicit approval, hash-bind `source.md`, `story.md`, and
   `storyboard.json`; then move exactly through
   `SOURCE_LOCK -> STORY_LOCK -> STORYBOARD_LOCK`.
6. Retrieve and inspect the minimum sufficient production-eligible reference bytes,
   then create a `LOCKED` visual packet. Episode-local one-off identities do not
   require dedicated identity sheets when drawing-language coverage is sufficient.
7. Compile a target-only master-board dispatch and rerun runtime-attachment
   preflight immediately before image execution.
8. Generate one text-free fixed 2x2 internal master board for each sequential
   group of one to four slides. Unused cells stay empty. Never pad a story.
9. Expand approved board cells into separate 4:5 slides; do not independently
   reinterpret a slide after a board exists.
10. Repair the smallest failed unit. Whole-board retry is reserved for board-wide
    style/identity/palette/semantic failure.
11. Run art-sequence QC. Style PASS requires agreement in line grammar, eye/face
    grammar, head/body proportion, hair massing, shading density, texture, and
    detail budget; palette similarity alone is insufficient. If the story declares
    an emotion delta, near-identical facial acting is a FAIL.
12. Add semantic text layers only after art lock:
    `DIALOGUE`, `THOUGHT`, `NARRATION`, `SFX`, `UI`, `TITLE`.
    Silence is valid. Final v2 lettering requires a project typography profile
    whose status is `LOCKED`.
13. Produce a separate cover, defaulting to `DERIVED_FROM_APPROVED_ART`. Generate
    dedicated cover art only when approved episode art cannot carry the hook.
14. Run final QC, one-file-per-slide export, cover evidence, and repository
    validation before `DONE`.

## Chat and Work execution

Both surfaces use the same lifecycle and evidence.

- **Chat** is bounded autonomous execution with durable response boundaries:
  `PREPRODUCTION_REVIEW -> BOARD_DISPATCH_READY -> ART_SEQUENCE_QC -> DONE`.
  At `PREPRODUCTION_REVIEW`, the user may approve or edit the creative package.
  A plain continuation token is not approval unless the review content was actually
  approved.
- **Work** also stops at an unapproved `PREPRODUCTION_REVIEW` by default. After
  editorial approval it prefers one-shot execution to `DONE` or a real retryable
  infrastructure/resource block.
- A response boundary is not a fake production stage or retryable block.
- Do not skip reference checks, pixel QC, anatomy/contact, quarantine, cover,
  lettering, export, or validation to fit a turn.

## Stop semantics

`DONE` and `ABANDONED_BY_USER` are the only terminal states. Quota, permission,
missing bytes, or tool faults are retryable infrastructure states. Editorial review
is an ACTIVE creative gate, not a retryable error.

## Verification

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python -m pipeline.cli validate
```
