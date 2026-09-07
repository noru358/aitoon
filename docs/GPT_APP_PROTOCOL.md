# GPT-app-native Instagram comic protocol

Version: 1.0  
Status: canonical  
Runtime: ChatGPT Chat or Work with built-in image generation/editing  
Additional paid budget: KRW 0

## 1. Definition of success

An episode succeeds only when all are true:

- the story begins from traceable human-produced material and retains specific
  human behavior or wording rather than generic AI invention;
- the art uses the selected user-designated production reference language to target a human-drawn visual grammar without copying a particular work or character;
- recurring people, episode-only people, palette, line behavior and location are
  coherent across the episode;
- camera, pose, expression and staging serve different beats rather than falling
  into a renderer default;
- hands, limbs, device faces, utensils, contact points and reflections are
  physically possible;
- every slide is its own 4:5 file;
- dialogue and meaning-bearing UI are readable and deliberately placed;
- no frame looks like polished generic AI/webtoon stock art.

There is no unconditional quality guarantee from a stochastic model. The
protocol guarantees something operational instead: nothing becomes final without
visible evidence, failures have an owner and bounded repair path, and the system
never labels an unseen or invalid result as complete.

## 2. Why board-first, slide-final

### Rejected default A: independent full-frame generation

Generating each slide from scratch re-samples identity, style, anatomy, camera,
background and props at every call. A previous PASS gives no control over the
next frame.

### Rejected default B: sticker composition

Composing transparent character poses over background plates preserves bytes but
often produces paper-doll staging, weak contact, repeated bodies and a visibly
assembled result. That conflicts with “a human drew this scene.”

### Canonical default: episode master board

The model draws up to four related text-free shots in one fixed 2x2 internal board.
The single sampling event gives the sequence one visual hand. Each occupied cell is
later expanded or faithfully extracted as an independent 4:5 slide. The master board
is a coherence source, not the delivery format.

The 2x2 topology does **not** fix an episode to four slides. Episode slide count is
story-driven and variable. A board may contain one to four occupied cells; unused
positions remain EMPTY and never justify padding the story. For more than four slides,
use another board for the next sequential batch. Bind the prior board only when its
continuity evidence is materially needed, together with the same primary style
references.

## 3. Persistent episode package

Every episode directory contains:

```text
episodes/E001/
  state.json
  source.md
  story.md
  storyboard.json
  visual_packet.json
  boards/
    B01.plan.json
    B01.dispatch.json
    B01.master.png
    B01.qc.json
  art/
    S01.png
    S02.png
  lettering/
    S01.plan.json
  final/
    S01.png
  qc/
    art_sequence.json
    final.json
  export/
```

Chat memory is never the only copy of a decision. `state.json` identifies the
stage and exact next action. Media records include path, SHA-256 and dimensions.

### Chat vs Work execution scheduling

Chat and Work share one production architecture. Do not fork story, rendering,
reference, retry, QC or export rules by surface.

**Chat default: bounded autonomous multi-turn.** A normal episode is intentionally
split across durable execution turns rather than forcing the entire pipeline through
one assistant response. The preferred boundaries are:

1. `BOARD_DISPATCH_READY`;
2. `ART_SEQUENCE_QC`;
3. `DONE`.

When a Chat turn reaches one of those boundaries after substantive work, write all
stage evidence and the exact next action to the repository, then end the response.
The user's next `계속` message starts a fresh execution turn from canonical boot.
It is a transport/control token only, not a routine approval gate. Do not ask the
user to re-approve unchanged story, storyboard, references, boards, or art merely
because a new turn began.

**Work default: one-shot autonomous completion.** Continue across the same durable
checkpoints toward `DONE` in one Work execution whenever the built-in tools remain
available. A real retryable tool/resource/permission block is still recorded
fail-closed; Work does not bypass limits or quality gates.

A response boundary is never represented as a production stage or retryable block.
The state machine remains the sole production lifecycle. If execution must resume in
another turn, `state.json.exact_next_action` is sufficient handoff authority.
Optimize context by reading only the companion files needed for that action; never
optimize by dropping actual reference-byte verification, pixel inspection, anatomy/
contact checks, quarantine, lettering verification, final QC, export evidence or
repository validation.

## 4. Autonomous stage protocol

### BOOTSTRAP

Use the canonical boot order and no competing variant:

`AGENTS.md -> CURRENT_STATE.md -> docs/GPT_APP_PROTOCOL.md -> config/policy.json -> active episode state.json`

After the active state is known, read only the companion policy, registry and actual
reference/calibration files required by its `exact_next_action`. `README.md` is
informational and is not part of the authority chain. Verify that only `aitoon` is
writable. Do not continue from remembered older repository rules or skip ahead from
the active episode state.

Images attached at Chat/Work startup or later in the same conversation do not start a
new episode, reset a stage, or supersede repository authority. Boot and recover the
active pointer first. Only then may an attachment be mapped as a session-scoped carrier
for an already locked reference role.

### SOURCE_LOCK

Search Korean community/SNS/public posts for traceable human seeds. Prefer direct
posts and comment threads. Record URL, observed facts, exact uncertainty, useful
human phrasing, and whether the final episode is adaptation or inspiration.

Kill a candidate when it is mostly explanation, needs an invented funny part,
has no state change, or would be visualized as people merely explaining.

Autonomous selection rule: choose the highest-scoring candidate on sceneability,
specificity, emotional recognition, visual state change, and landing. Do not ask
the user to choose among near-ties.

### STORY_LOCK

Write beats before polished dialogue. Each body beat must change action,
knowledge, relationship, object state, or emotion. Preserve awkward fragments,
omissions and mundane source details. Remove neat morals, symmetrical AI
wordplay, generic reactions and captions that explain the visible image.

### STORYBOARD_LOCK

For each slide declare:

- story beat and state delta;
- primary visual-information owner;
- shot scale/angle and why it differs from adjacent shots;
- body action, gaze, expression and prop state;
- screen front/back/camera geometry when a device is present;
- continuity facts entering and leaving the shot;
- dialogue/caption-safe region;
- whether silence carries the beat.

Vary the sequence by story function. Never satisfy diversity with a fixed quota
of left-, right- and front-facing heads.

For shots with elevated manual-action ambiguity, apply the conditional
`docs/ANATOMY_CONTACT_POLICY.md` guard. Do not turn that guard into a universal
visible-limb count or fixed action-count quota.

#### Conditional anatomy/contact preflight

Do not globally force every character to show two arms/two hands, and do not cap
every performance to a fixed number of actions. Those rules create false failures
under valid occlusion and flatten natural acting.

Instead, require an `anatomy_contract` only when a shot has elevated manual-action
risk, such as a prop plus a device, a prop handoff plus an expressive self-touch,
multiple people contacting one story-bearing object, crossed/occluded arms, or
another staging choice where limb ownership could become ambiguous.

A triggered contract declares:

- semantic limb roles by character (for example "device hand" or "prop hand");
  do not hard-code left/right handedness unless continuity actually requires it;
- required hand-object/body contacts;
- forbidden duplicate limbs, disconnected hands, or unrequested extra gestures;
- the least destructive simplification fallback if all requested manual actions
  cannot coexist cleanly.

Story-bearing contact outranks decorative acting. If an expressive gesture
competes with a required prop/device contact, preserve the required contact and
simplify the gesture. When a beat reads equally well immediately before or after
a complicated handoff, prefer the lower-contact staging rather than forcing many
hands onto one small object at once.

### VISUAL_PACKET_LOCK

Bind actual files, not textual claims that a reference exists. Reference authority
is defined by `docs/REFERENCE_POLICY.md` and `references/registry.json`.

Production provenance is operational, not forensic: a visual reference explicitly
supplied or designated by the user/project as a target reference is sufficient for
production use unless conflicting evidence exists. Record whether authorship was
independently verified, but do not require independent proof merely to proceed and
do not fabricate such proof.

Required *coverage* is:

1. person/style drawing language;
2. interaction or full-body drawing language when people interact;
3. background/scene drawing language when a location matters;
4. identity sheet for any recurring project character used;
5. a compact episode palette and line/shape grammar.

This is not a minimum file count. One reference may satisfy several roles when its
actual pixels genuinely contain the required evidence.

An episode-local one-off character is not a recurring project character and does not
require a dedicated new identity sheet solely because its identity is new. When the
registered production references already cover the required person/style plus relevant
interaction/background drawing language, author a distinct episode-local identity
inside that visual grammar without copying a reference character. Do not ask the user
for a new upload or independent human-authorship proof merely to create that identity.

Reference hierarchy:

1. `PRIMARY_STYLE`: permanent user-designated style authority;
2. `CONTINUITY_ANCHOR`: selectively promoted approved episode art for identity,
   outfit, location or prop continuity;
3. `EPISODE_LOCAL`: current-episode boards/slides used only for local continuity.

Generated episode art is never automatically promoted and never overrides
`PRIMARY_STYLE`. Promotion requires explicit user visual approval, objective QC
PASS, and nonredundant continuity value.

Each reference record states `path`, `sha256`, `role`, `allowed_influence`,
and `forbidden_inference`. Permanent references also resolve to a production-
eligible registry entry. A style reference does not authorize copying its identity,
pose, clothing, story, camera or location unless that influence is explicitly
allowed.

If eligible bytes already exist in `aitoon`, the operator must retrieve and inspect
those actual bytes and provide them to the image runtime. A repository path alone is
not image conditioning, but absence from the current chat attachment list is not a
user-blocking condition. Use `WAITING_REQUIRED_BYTES` only after retrieval of the
known repository file actually fails.

Fail closed only when required coverage or actual bytes remain unavailable after
that retrieval attempt. Do not replace missing visual evidence with prose.

Reference authority and runtime transport are deliberately separate. The persistent
authority is the registry entry plus repository path/SHA and declared influence bounds.
A Chat attachment, Work runtime file, connector file reference, or image-generation
handle is only a carrier. A carrier never becomes `PRIMARY_STYLE` or
`CONTINUITY_ANCHOR` merely because the current image runtime can consume it.

### BOARD_DISPATCH_READY

Create one target-only dispatch per board. The compiled dispatch being `READY` does
not prove that a session-scoped image carrier is still usable. Immediately before
every generation/edit execution that consumes visual references, run this preflight:

1. re-resolve every bound reference to its locked repository SHA-256;
2. prefer a direct repository-to-current-image-runtime attachment path;
3. prove that the current image runtime can bind the actual visual media -- a path,
   base64 string, connector file URI, or prior-session handle alone is not proof;
4. if the direct bridge is unavailable, use a user-supplied/current-session copy of
   the already locked registered reference as a transport fallback when present;
5. map fallback carriers to the locked registry roles without changing
   `visual_packet.json`, authority, story, episode, or stage;
6. treat all runtime bindings as session-only and repeat this preflight after any
   Chat, Work run, or execution-surface change.

Do not persist an opaque runtime handle as reference authority. A non-secret receipt
may record carrier kind and the source registry SHA it transported, but it must never
claim byte equality when the platform may have re-encoded the attachment.

If repository bytes/hash verification fails, use `WAITING_REQUIRED_BYTES`. If the
bytes are valid but the current surface cannot deliver any valid carrier to the image
runtime, use `WAITING_TOOL_RECOVERY`. If image generation itself is unavailable
after attachment succeeds, use `WAITING_INCLUDED_IMAGE_CAPACITY`. A user attachment
used only as transport is not new reference evidence and does not trigger a new
approval or identity-sheet stage.

Create one target-only dispatch per board. Supply the actual reference media,
the board plan, and no future-board instructions except continuity facts needed
at the boundary. Use the minimum sufficient set: primary style references plus only
those continuity anchors that materially constrain the current board. Do not dump
the accumulated episode archive into every dispatch.

The master board prompt must require:

- a clean 2x2 grid of up to four 4:5 cells;
- exactly the declared shot in each occupied cell;
- no titles, dialogue, captions, speech bubbles, logos, watermarks or fake UI
  text;
- the same visual hand, identity and palette across cells;
- deliberately different beat-serving framing and acting;
- simple hand-drawn black line, flat local color, restrained shading and
  background detail matched to the references;
- no glossy hair, detailed irises, cinematic blur/light, beige global wash,
  generic anime beautification or polished stock-webtoon finish.

Keep prompts concrete and short. The bound images carry visual style; prose
defines roles, actions, geometry and exclusions.

### MASTER_BOARD_IMPORTED and MASTER_BOARD_QC

Import the actual generated board into the episode package when the runtime
provides a file artifact; otherwise keep the generated image as the chat-native
artifact and record its stable app/library handle if one is exposed. Never invent
a path or hash.

Inspect in this order:

1. output contract: correct grid, occupied cells, no text/collage leakage;
2. board-wide style and identity;
3. cell-level anatomy/contact/device/reflection geometry, including whether each
   visible hand/arm has one plausible anatomical origin, declared contacts map to
   unique limbs, and no duplicate/unrooted limb is present; valid occlusion is not
   itself a failure;
4. shot meaning and continuity;
5. sequence-level default-camera bias and repeated acting.

Repair routing:

- board-wide style/identity/palette drift -> one whole-board retry;
- one bad hand, limb, prop contact, expression, or shot meaning -> expand the
  good cells and repair only the failed slide using the board and original cell
  as reference;
- bad story or storyboard -> return to the owning text stage; do not prompt-loop
  an image problem whose cause is upstream.

### SLIDES_EXPANDED

Each occupied board cell becomes one separate 4:5 image. Use one of two paths:

1. deterministic crop/resize when the master board contains full-resolution,
   cleanly divided 4:5 cells;
2. built-in image edit when expansion is required: “faithfully isolate and
   expand cell N; preserve line, colors, identity, pose, expression, camera,
   objects and background; do not redesign or add text.”

The second path is an edit, not a new illustration request. Bind the master board
on every call. Never describe a cell from memory.

### ART_SEQUENCE_QC

Inspect the separate art files together. Check character distinction, clothing,
palette, background continuity, prop state, anatomy, information geometry,
expression fidelity, and viewer-perceived repetition. A frame passes only when
its declared semantic intent survives.

### LETTERING_COMPLETE

Add lettering after art is locked. Keep an editable JSON plan per slide. Prefer a
verified Korean font file, explicit text roles, safe margins, bubble tails aimed
at the speaker, and text ordering that follows the eye path. Messenger/profile
text and read counts are meaning-bearing UI and belong here, not in generated
art.

If direct app-to-local artifact transfer is unavailable, use one built-in edit
per slide to add the already locked lettering while binding that exact slide.
Compare wording character-for-character after the edit. A typo is a hard FAIL.

### FINAL_QC, EXPORT_READY, DONE

Review all final slides in order at thumbnail and full size. Verify wording,
speaker ownership, reading order, edge safety, visual rhythm, final landing and
one-file-per-slide packaging. Export in sequence order with stable names.

`DONE` requires both structured QC reports and exact artifact evidence. A chat
message saying “looks good” is not sufficient.

## 5. Built-in-capacity and fault handling

The system never switches to an API to escape an included-limit failure.

When image generation/editing is temporarily unavailable:

1. write the current retryable state and exact resume action;
2. finish any independent source, script, layout, prompt, or QC work;
3. preserve the dispatch without changing it merely because time passed;
4. retry from the saved stage when the built-in capability returns;
5. when the blocker is specifically a missing repository-to-runtime transport bridge,
   first retry the direct bridge; if it is still unavailable, an already supplied
   current-session copy of the locked reference may be used as the permitted transport
   fallback without changing reference authority or stage;
6. never ask the user to pay, choose a fallback renderer, or re-approve unchanged
   work.

If a scheduled Work task is available and the project files are accessible, it
may resume the saved action. It must not programmatically automate a personal
subscription or bypass service limits.

## 6. Human-drawn quality rubric

### Positive evidence

- line weight and shape simplification match the selected references;
- small irregularities feel intentional and consistent, not simulated noise;
- silhouettes, spacing and expressions are designed for the joke or emotion;
- detail is spent on story-bearing objects and reduced elsewhere;
- backgrounds establish place without competing with the action;
- dialogue feels spoken by a particular person, not by a polished narrator;
- adjacent shots make purposeful visual changes.

### Automatic rejection

- generic glossy anime/webtoon face, hair shine or detailed iris;
- uniform beauty treatment across leads and extras;
- global gradient, cinematic depth of field, lens flare, beige wash or 3D volume;
- the same three-quarter face and medium shot repeated without story reason;
- impossible arm/hand/phone/utensil/reflection geometry;
- an extra who clones a recurring lead;
- generated gibberish, baked speech, logo, watermark or panel numbering;
- visual embellishment that changes the intended emotion;
- collage delivered as the final slide set.

## 7. Retry budget and anti-loop rule

One master board receives at most one whole-board retry. One isolated slide
receives at most two targeted repairs. Exceeding the limit does not become an
infinite prompt loop: decompose the shot, simplify only nonessential geometry, or
return to storyboard staging while preserving the story beat. The system remains
active and chooses the least destructive route itself.

## 8. Evidence model

Every PASS names:

- artifact or app handle actually inspected;
- SHA-256 and dimensions when file bytes exist;
- producing dispatch ID;
- QC report version;
- dependencies and their hashes;
- exact next action.

Rejected artifacts are immutable quarantine records. They cannot be used as
examples of the target style or as repair/continuity seeds.

## 9. Honest boundary

“Actual human drew it” cannot be proven when AI creates the pixels. The enforceable
target is perceptual and editorial: a finished comic with the specificity,
coherence, restraint and deliberate staging expected of human-made Instagram
comics, with no obvious generic model defaults. The protocol must not market AI
output as literally human-authored or fabricate authorship.

