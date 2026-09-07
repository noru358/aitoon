# AIToon production reference policy

Version: 1.0  
Status: canonical companion to `GPT_APP_PROTOCOL.md`

## 1. Provenance boundary

AIToon records what is actually known.

A visual reference explicitly supplied or designated by the user/project as a
target reference is sufficient production provenance unless conflicting evidence
exists. Independent authorship verification is recorded separately and is not a
routine production gate.

Never claim that an artist, process, or human authorship was independently verified
when it was not.

## 2. Authority hierarchy

### PRIMARY_STYLE

Permanent authority for line, shape simplification, eye/face grammar, palette,
shading restraint and background abstraction.

Primary style references are curated and stable. Generated episode art must not
replace or outrank them.

### CONTINUITY_ANCHOR

Approved generated art may be promoted only when all are true:

- the user explicitly approved the actual inspected pixels;
- objective QC passed: anatomy/contact, continuity, no baked text and semantic intent;
- the image contributes nonredundant continuity information such as a useful
  recurring-character view, interaction, outfit, location or prop state;
- it does not conflict with primary style authority.

Promotion does not mean style authority. Use the anchor only for its declared
`allowed_influence`.

### EPISODE_LOCAL

Master boards, extracted slides and repair inputs are local continuity evidence by
default. They are not carried into later episodes unless promoted.

A user-approved generated image may also become a **scoped operational episode
visual anchor** without being promoted to CONTINUITY_ANCHOR or PRIMARY_STYLE when:

- the user explicitly approved the visible pixels;
- the actual pixels were inspected;
- the approved influence scope is objectively safe;
- any known objective failure is explicitly excluded from that scope.

For example, an image with a wrong phone-facing direction may still anchor a clean
face identity, hair silhouette, outfit palette, and user-approved rendering
treatment, while the phone geometry remains forbidden inference. Aesthetic approval
does not waive anatomy/contact/screen/text defects.

Once such an episode anchor applies, its declared identity/rendering attributes must
not be silently replaced by fresh resampling. Prefer derivation/editing from the
approved pixels, then explicit anchor binding. If the anchor cannot be transported
to the image runtime, fail closed rather than redesigning the character.

This scoped episode anchor is not automatically reusable in later episodes and
never becomes PRIMARY_STYLE without a separate explicit promotion action.

## 3. Curation rule

Do not automatically accumulate every approved image.

For each image dispatch, prefer the smallest set that fully constrains the task:

- the necessary primary style reference(s);
- zero or a few relevant continuity anchors;
- current-episode local evidence when required.

More references are not automatically better. Redundant or conflicting references
can average identities, repeat camera/pose biases, freeze episode-specific clothing,
increase processing cost and cause copy-of-copy style drift.

## 4. Multi-role references

Coverage, not file count, is mandatory. A single actual image may satisfy person,
interaction/full-body and scene drawing-language roles if its pixels genuinely show
all of them. Do not create artificial user blocks merely to obtain one file per role.

## 5. Episode-local identity and re-upload rule

A new one-off episode character does not require a dedicated identity reference merely
because that exact person has not appeared before. `PRIMARY_STYLE` references control
the drawing language; the operator may author a distinct episode-local identity within
that language unless the task requires exact recurring-character identity continuity.

When registered production-eligible references already provide the required coverage,
requesting the user to re-upload those references as *new reference evidence* or supply
a new identity image is a protocol error. Retrieve the registered bytes from `aitoon`
first. Ask for new visual evidence only when the required visual role is genuinely
uncovered after repository retrieval, or when the user explicitly requires an exact
identity not represented by existing authority.

A narrow transport exception exists when the repository bytes are valid but the
current Chat/Work surface has no repository-binary-to-image-runtime bridge. In that
case a user-supplied/current-session copy of the already locked reference may be used
only as a session carrier. It does not become a new reference, does not change
authority, does not require a new approval, and does not reset the episode or stage.

## 6. Repository retrieval semantics

If a production-eligible reference already exists in `aitoon`, the operator owns
the retrieval step:

1. resolve it from `references/registry.json`;
2. retrieve the actual bytes;
3. inspect/hash-check them;
4. attempt direct binding of those bytes to the current image runtime;
5. if the direct bridge is unavailable, map an eligible current-session attachment
   to the already locked registry role as a transport-only fallback;
6. immediately before generation/editing, verify that the current image runtime can
   actually consume the carrier.

A file not being attached in the current chat does not mean the bytes are missing.
`WAITING_REQUIRED_BYTES` is valid only when repository retrieval or inspection
actually fails. Valid repository bytes plus an unavailable runtime transport bridge
is `WAITING_TOOL_RECOVERY`.

## 6.1 Runtime carrier semantics

The repository reference is durable authority; the runtime carrier is ephemeral
transport.

- preferred carrier: direct repository materialization accepted by the current image runtime;
- permitted fallback: current-session Chat/Work attachment corresponding to an already
  locked registered reference, only after the direct bridge is unavailable;
- carrier scope: current session/run only;
- session or surface change: rerun preflight before the next image call;
- opaque runtime handles and connector file URIs are never persisted as style authority;
- platform re-encoding is allowed for transport lineage, so carrier bytes need not share
  the repository SHA; the carrier must instead be mapped back to the source registry SHA;
- an attachment alone never changes `state.json.exact_next_action`.

## 7. Rejection and promotion safety

Rejected/quarantined images can never be promoted or reused.

A promoted continuity anchor can later be retired if it becomes redundant or is
shown to cause drift. Retiring an anchor does not change the primary style authority.

The production registry is curated control data, not an archive of all successful
images.
