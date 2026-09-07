# AIToon operating contract

## Canonical boot order

Use exactly one boot order for every fresh or resumed production run:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `docs/GPT_APP_PROTOCOL.md`
4. `config/policy.json`
5. the active episode's `state.json`, when an active episode exists
6. only then the companion material required by that active next action, including
   `docs/REFERENCE_POLICY.md`, `docs/ANATOMY_CONTACT_POLICY.md`,
   `references/registry.json`, and the actual reference/calibration bytes to be used

`README.md` is descriptive documentation, not boot authority. `CURRENT_STATE.md`
identifies repository-level production context. Once an active episode is identified,
`state.json.exact_next_action` is the execution pointer. Do not substitute
conversational memory, an older README instruction, or a guessed next step.

## Non-negotiable runtime

- This repository is the only writable authority for AIToon production.
- `instatoon`, `AutoPipeline`, and `jipbap` may be inspected or copied from, but
  must never be edited by this project.
- Use ChatGPT/Work built-in capabilities only. Do not call a paid API, paid SaaS,
  or external image model. Additional paid budget is KRW 0.
- Do not ask the user for routine approval, taste decisions, asset approval, or
  permission to continue. Apply the committed defaults and continue.
- A quota or transient tool failure is retryable state, not a request for user
  input. Checkpoint it, continue every independent text/code/QC task, and resume
  the blocked image step when the built-in capability is available.
- Never claim a visual PASS without inspecting the actual image.
- Never use a rejected image as a style, identity, continuity, or repair input.
- A user-designated project reference is sufficient production provenance unless conflicting evidence exists; record independent authorship verification separately and never invent it.
- If eligible reference bytes already exist in `aitoon`, retrieve and inspect them yourself. Absence from the current chat attachment list is not a user-blocking condition; use `WAITING_REQUIRED_BYTES` only after repository retrieval actually fails.
- Reference authority and runtime transport are separate. Registry path/SHA/authority remain persistent source of truth; a Chat/Work attachment or runtime file is only a session-scoped carrier and never becomes style authority merely because it is attachable.
- Before every built-in image generation/edit that requires visual references, run a runtime-attachment preflight on the current surface. A repository path, base64 payload, connector file URI, or prior-session handle is not sufficient evidence; the current image runtime must actually be able to bind the visual media.
- Prefer direct repository-to-runtime attachment. If that bridge is unavailable, a user-supplied copy of an already locked registered reference may be used as a session-only transport fallback. This is not a request for new reference evidence, does not rewrite `visual_packet.json`, and does not reset the active episode or stage.
- Startup or mid-run image attachments never override `state.json.exact_next_action`. Boot first, keep the active episode pointer, then map eligible attachments only to the already locked reference roles they transport.
- Session/runtime bindings are ephemeral. Re-run attachment preflight after any chat, Work run, or execution-surface change; never persist an opaque runtime handle as reference authority.
- When registered production references already provide sufficient drawing-language coverage, do not ask the user to upload a new reference merely to invent an episode-local one-off character identity. A dedicated identity sheet is required only when exact recurring identity continuity actually needs one.
- Approved generated episode art is episode-local by default. Promote only nonredundant, explicitly user-approved, objective-QC-passing continuity anchors; generated anchors never override primary style references.
- One published slide is one 4:5 image. A temporary multi-panel master board is
  allowed only as an internal coherence device and must be expanded into separate
  slide images before export.

## Default production behavior

1. Start with a traceable human-produced story seed.
2. Lock story, dialogue, panel intent, and text-safe regions before image work.
3. Bind the minimum sufficient production-eligible reference set from `references/registry.json` by actual file bytes and SHA-256. One file may cover multiple visual roles when its pixels genuinely contain that evidence.
4. Compile the board dispatch, then immediately before execution run runtime-attachment preflight on the current Chat/Work surface. Prefer direct repository transport; use an already supplied session attachment only as transport fallback when the direct bridge is unavailable.
5. Generate one text-free fixed 2x2 internal master board for each sequential batch of one to four slides. Episode slide count remains variable; unused board cells stay empty and stories are never padded to fill the grid.
6. Expand each cell into its own 4:5 image using the master board as the visual
   source of truth; do not reinterpret the shot.
7. Repair the minimum failed unit. Whole-board regeneration is reserved for a
   board-wide style/identity failure.
8. Add editable lettering/UI after art approval and run final sequence QC.
9. Persist state and evidence at every stage so another chat can resume from
   files rather than conversational memory.

## Stop semantics

`DONE` and `ABANDONED_BY_USER` are the only terminal states. Safety, permissions,
missing source bytes, quota exhaustion, and tool faults are nonterminal blocked
states. A missing repository-to-image-runtime transport bridge is
`WAITING_TOOL_RECOVERY`, not `WAITING_REQUIRED_BYTES`. If an eligible session
attachment is already available it may satisfy transport without changing the stage.
Record an exact resume action; never manufacture evidence or bypass a platform
restriction.

## Verification

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python -m pipeline.cli validate
```

