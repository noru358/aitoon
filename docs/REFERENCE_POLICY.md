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

## 5. Repository retrieval semantics

If a production-eligible reference already exists in `aitoon`, the operator owns
the retrieval step:

1. resolve it from `references/registry.json`;
2. retrieve the actual bytes;
3. inspect/hash-check them;
4. bind those bytes to the image runtime.

A file not being attached in the current chat does not mean the bytes are missing.
`WAITING_REQUIRED_BYTES` is valid only when repository retrieval or inspection
actually fails.

## 6. Rejection and promotion safety

Rejected/quarantined images can never be promoted or reused.

A promoted continuity anchor can later be retired if it becomes redundant or is
shown to cause drift. Retiring an anchor does not change the primary style authority.

The production registry is curated control data, not an archive of all successful
images.
