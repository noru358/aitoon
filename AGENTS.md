# AIToon operating contract

Read this file first, then `README.md`, `docs/GPT_APP_PROTOCOL.md`,
`docs/ANATOMY_CONTACT_POLICY.md`, `docs/REFERENCE_POLICY.md`, `config/policy.json`,
`references/registry.json`, and the active episode's `state.json` if one exists.

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
- Approved generated episode art is episode-local by default. Promote only nonredundant, explicitly user-approved, objective-QC-passing continuity anchors; generated anchors never override primary style references.
- One published slide is one 4:5 image. A temporary multi-panel master board is
  allowed only as an internal coherence device and must be expanded into separate
  slide images before export.

## Default production behavior

1. Start with a traceable human-produced story seed.
2. Lock story, dialogue, panel intent, and text-safe regions before image work.
3. Bind the minimum sufficient production-eligible reference set from `references/registry.json` by actual file bytes and SHA-256. One file may cover multiple visual roles when its pixels genuinely contain that evidence.
4. Generate one text-free 2x2 master board for each group of up to four slides.
5. Expand each cell into its own 4:5 image using the master board as the visual
   source of truth; do not reinterpret the shot.
6. Repair the minimum failed unit. Whole-board regeneration is reserved for a
   board-wide style/identity failure.
7. Add editable lettering/UI after art approval and run final sequence QC.
8. Persist state and evidence at every stage so another chat can resume from
   files rather than conversational memory.

## Stop semantics

`DONE` and `ABANDONED_BY_USER` are the only terminal states. Safety, permissions,
missing source bytes, quota exhaustion, and tool faults are nonterminal blocked
states. Record an exact resume action; never manufacture evidence or bypass a
platform restriction.

## Verification

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
python -m pipeline.cli validate
```

