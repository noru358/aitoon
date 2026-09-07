# Image runtime control policy

Status: canonical companion to `GPT_APP_BOARD_FIRST_V2`.

This policy exists because repository state is deterministic but the built-in image
renderer is conversation-conditioned and stochastic. More prompt text is not treated
as a hard constraint.

## 1. User-approved pixels are operational

When the user explicitly approves visible pixels, the approval must change later
render behavior.

An approved image can become an `EPISODE_LOCAL` visual anchor when:

- the user explicitly approved it;
- actual pixels were inspected;
- the anchor scope is objectively safe.

The scope can be narrower than the whole image. For example, a board with a bad
phone angle can still anchor face, hair, outfit and approved rendering treatment if
those attributes are clean. Objective anatomy/contact/screen/text failures remain
excluded and are never waived by aesthetic approval.

Once an applicable approved anchor exists, fresh resampling of those anchored
attributes is forbidden. Prefer, in order:

1. derive from approved pixels;
2. edit approved pixels;
3. bind the approved visual anchor as image reference.

If the required anchor cannot be transported into the current image runtime, fail
closed rather than silently redesigning the character.

An approved episode anchor does not automatically become project PRIMARY_STYLE.

## 2. Art-only execution context

A compiled image dispatch is the only story-semantic payload that the image runtime
should see.

At image execution time, do not reopen or restate:

- source prose;
- dialogue/thought/narration copy;
- lettering plans;
- cover copy;
- future beats not present in the current runtime sheet.

Allowed execution context is limited to the active dispatch, approved visual-anchor
manifest, bound registry entries, and the actual reference/anchor media required by
that dispatch.

This rule reduces conversation leakage such as speech bubbles appearing in an art
stage that explicitly forbids text.

## 3. Natural-occupancy runtime sheets

The repository still uses a canonical internal 2x2 board for up to four sequential
slides, but the generator no longer creates empty placeholder cells.

Runtime topology is:

- 1 slide -> 1x1;
- 2 slides -> 1x2;
- 3 slides -> 1x3;
- 4 slides -> 2x2.

After a runtime sheet passes pixel QC, code deterministically packs its cells into
the canonical 2x2 board. Unused canonical cells are created by code as plain empty
cells.

This preserves board-first coherence while removing the unreliable request that a
comic generator intentionally leave some panels blank.

## 4. Semantic noncompliance is not a tool outage

Examples:

- forbidden text appears;
- the renderer ignores the requested runtime topology;
- future beats appear;
- an applicable approved cast anchor is ignored.

These are `RUNTIME_SEMANTIC_NONCOMPLIANCE`, not ordinary
`WAITING_TOOL_RECOVERY`.

After semantic noncompliance, do not keep escalating the prompt in the same long
conversation. Checkpoint `WAITING_CLEAN_IMAGE_SESSION` and resume on a clean image
execution surface with the same locked upstream state and a copy-free dispatch.

Retry budgets count genuine executions of the requested target, not outputs that
clearly ignored the target topology/semantics.

## 5. Risk controls

Approved anchors can freeze defects, so their influence is scoped and objective
defects are excluded.

Clean sessions can lose continuity, so required anchor/reference SHA-256 values are
stored in repository manifests and must be supplied as matching carriers when direct
binding is unavailable.

Variable runtime-sheet topology adds a packing step, so the generated sheet is
never published directly. It must be deterministically packed into the canonical
2x2 board before slide split/export.

The clean-session rule adds a session boundary, but it is triggered only by actual
semantic noncompliance, not normal aesthetic disagreement or routine retries.
