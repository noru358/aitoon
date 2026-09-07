# GPT-app-native Instagram comic protocol

Version: 1.0  
Status: canonical  
Runtime: ChatGPT Chat or Work with built-in image generation/editing  
Additional paid budget: KRW 0

## 1. Definition of success

An episode succeeds only when all are true:

- the story begins from traceable human-produced material and retains specific
  human behavior or wording rather than generic AI invention;
- the art uses the selected human-drawn reference language without copying a
  particular work or character;
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

The model draws up to four related text-free shots in one 2x2 board. The single
sampling event gives the sequence one visual hand. Each cell is later expanded
or faithfully extracted as an independent 4:5 slide. The master board is a
coherence source, not the delivery format.

For more than four slides, use another board. Bind the prior board plus the same
style/identity/location references. Do not reserve a fake overlap slide or pad a
story merely to fill four cells; unused cells are explicitly marked EMPTY in the
plan and ignored on export.

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

## 4. Autonomous stage protocol

### BOOTSTRAP

Read repository authority, validate policy, inspect the active state, and verify
that only `aitoon` is writable. Do not continue from remembered older repository
rules.

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

Bind actual files, not textual claims that a reference exists. Minimum packet:

1. one human-drawn person/style reference;
2. one interaction or full-body reference when people interact;
3. one background/scene reference when a location matters;
4. identity sheet for any recurring project character used;
5. a compact episode palette and line/shape grammar.

Each reference record states `path`, `sha256`, `role`, `allowed_influence`, and
`forbidden_inference`. A style reference does not authorize copying its identity,
pose, clothing, story, camera or location.

Fail closed if required bytes cannot be inspected. This is a retryable resource
state, not permission to replace the reference with prose.

### BOARD_DISPATCH_READY

Create one target-only dispatch per board. Supply the actual reference media,
the board plan, and no future-board instructions except continuity facts needed
at the boundary.

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
5. never ask the user to pay, choose a fallback renderer, or re-approve unchanged
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

