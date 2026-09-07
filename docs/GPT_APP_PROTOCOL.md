# GPT-app-native Instagram comic protocol

Version: 2.0  
Status: canonical  
Architecture: `GPT_APP_BOARD_FIRST_V2`  
Runtime: ChatGPT Chat or Work with built-in image generation/editing  
Additional paid budget: KRW 0

## 1. Definition of success

An episode succeeds only when all are true:

- it begins from traceable human-produced material;
- the user has had one real preproduction opportunity to inspect and edit the
  topic, premise, beats, dialogue/interiority, slide count, and cover concept;
- the approved creative files are hash-bound before production locks advance;
- art follows the selected reference drawing language without copying incidental
  reference identities, rooms, poses, props, clothes, or story;
- backgrounds and assets use the lowest amount of information needed for the beat;
- recurring identities, episode-local identities, objects, palette and location
  anchors remain coherent;
- camera and acting serve story deltas rather than renderer defaults;
- hands, limbs, device faces, reflections and contacts are physically possible;
- visible facial acting changes when the declared emotional state changes;
- every narrative slide is a separate 1080x1350 4:5 file;
- the cover is a separate packaging artifact;
- semantic lettering is deliberate and matches the drawing language;
- actual pixels and structured evidence exist for every PASS.

The system does not promise deterministic stochastic-image quality. It guarantees
fail-closed evidence, explicit editorial control, bounded repair, and no false DONE.

## 2. Lifecycle

Canonical stages:

`BOOTSTRAP -> PREPRODUCTION_REVIEW -> SOURCE_LOCK -> STORY_LOCK -> STORYBOARD_LOCK -> VISUAL_PACKET_LOCK -> BOARD_DISPATCH_READY -> MASTER_BOARD_IMPORTED -> MASTER_BOARD_QC -> SLIDES_EXPANDED -> ART_SEQUENCE_QC -> LETTERING_COMPLETE -> FINAL_QC -> EXPORT_READY -> DONE`

### BOOTSTRAP

Canonical boot is:

`AGENTS.md -> CURRENT_STATE.md -> docs/GPT_APP_PROTOCOL.md -> config/policy.json -> active state.json`

After the active pointer is known, load only companions required by the exact next
action. Startup attachments never override the repository pointer.

Draft the human source, story, storyboard, text roles, cover concept, and visual
information budget. These are drafts until editorial approval.

### PREPRODUCTION_REVIEW

This is the only default per-episode creative approval gate.

Present, together:

- source URL/topic and provenance uncertainty;
- one-line premise and emotional engine;
- narrative slide count;
- every beat and state delta;
- all proposed dialogue, thought, narration, SFX, and meaning-bearing UI;
- cover title and visual concept;
- any adaptation choice that could materially change the story.

The user may approve or edit. On approval, `editorial_review.json` stores SHA-256
for `source.md`, `story.md`, and `storyboard.json`. Advancement into
`SOURCE_LOCK` fails if any reviewed file changes after approval.

This does not reintroduce routine approval for reference binding, QC, retry, split,
lettering execution, export, or validation.

### SOURCE_LOCK / STORY_LOCK / STORYBOARD_LOCK

Once approved, lock the reviewed contents exactly and move one stage at a time.

Each slide declares:

- beat and state delta;
- visual-information owner;
- shot and action;
- expression;
- `face_acting_intent` and `emotion_delta`;
- continuity in/out;
- text-safe region;
- semantic copy;
- background information budget;
- device geometry when relevant;
- anatomy/contact contract only when manual-action risk is elevated.

Copy roles are `DIALOGUE`, `THOUGHT`, `NARRATION`, `SFX`, and `UI`.
Thought/narration is optional. Silence remains a valid beat.

## 3. Lowest-sufficient visual design

See `docs/VISUAL_MINIMALISM_POLICY.md`.

Every slide chooses one background level:

1. `NONE`: no location drawing is needed;
2. `SYMBOLIC`: one or two cues are enough;
3. `LOCATION_ANCHOR`: a few spatial anchors are required for action/continuity;
4. `FULL_SCENE`: environment geometry itself carries story.

`FULL_SCENE` requires a story reason. Decorative furniture, plants, frames, lamps,
shelves, appliances, packaging, textures and scenery are omitted unless they carry
story, contact, location, continuity, or the punchline.

The rule is not “always blank.” It is “use the lowest sufficient amount.”

## 4. Cover and interiority

A protocol-v2 episode requires a cover separate from narrative `slide_count`.

Default cover strategy is `DERIVED_FROM_APPROVED_ART`: crop/reframe approved
episode art or use a simple spot derived from it, then add title typography
separately. Dedicated cover art is allowed only when approved art cannot
communicate the hook.

Cover title and concept are included in `PREPRODUCTION_REVIEW`.

Inner voice is a semantic text channel, not a mandatory ending trope. A beat may use
`THOUGHT` or `NARRATION` when it contributes information or emotional contrast.
Do not force a thought balloon or caption into every slide.

## 5. Visual references

See `docs/REFERENCE_POLICY.md`.

Coverage, not file count, matters. Retrieve actual repository bytes and verify SHA-256.

Hierarchy:

1. `PRIMARY_STYLE`: drawing-language authority;
2. `CONTINUITY_ANCHOR`: explicit identity/outfit/location/prop continuity;
3. `EPISODE_LOCAL`: current episode only.

A style image may contain known characters, but those identities are not implied
targets. For an episode-local person, use the reference only for declared drawing
grammar. Exact identity influence must be separately explicit.

A new one-off episode character does not require a dedicated identity sheet when
registered person/style coverage is sufficient.

Reference authority is persistent repository path/SHA/role. Chat/Work attachments are
ephemeral carriers only.

## 6. Runtime attachment preflight

Before every reference-consuming generation/edit:

1. resolve bound reference path and locked SHA;
2. retrieve/inspect repository bytes;
3. prefer repository-direct image-runtime binding;
4. prove the current image runtime can consume actual visual media;
5. only after direct bridge failure, map a matching current-session attachment as
   `SESSION_ONLY` transport;
6. never change authority, episode, review, stage, or visual packet because of a
   transport fallback;
7. rerun preflight after session/surface change.

Missing/corrupt repository bytes => `WAITING_REQUIRED_BYTES`.  
Valid bytes but unusable transport => `WAITING_TOOL_RECOVERY`.  
Included image capacity unavailable => `WAITING_INCLUDED_IMAGE_CAPACITY`.

## 7. Board-first, slide-final

Independent full-frame generation re-samples identity/style/anatomy/camera at every
call. Sticker composition often looks assembled. The default remains one internal
text-free master board for up to four sequential slides.

The fixed 2x2 topology is only an internal coherence batch:

- one to four cells may be occupied;
- unused cells remain EMPTY;
- story length is never padded or trimmed to fit;
- more than four slides use another sequential board.

Master-board prompts must:

- describe exactly the occupied beat in each cell;
- specify the lowest-sufficient background and essential assets;
- forbid decorative background invention;
- keep reference cast identity separate from target cast identity;
- forbid titles, dialogue, captions, bubbles, readable UI, letters, numerals,
  logos, watermarks and panel labels;
- maintain one visual hand while varying beat-serving composition and acting.

After an approved board exists, a narrative slide cannot be regenerated from scratch.
It is cropped/expanded from the board or minimally repaired with the board/cell bound.

## 8. Style and facial-acting QC

A style PASS is multidimensional:

- line grammar;
- eye/face grammar;
- head/body proportion;
- hair massing;
- shading density;
- texture;
- detail budget.

Matching palette or general “cute webtoon” appearance is insufficient.

If two slides declare a meaningful emotional delta, a near-identical face render,
eye state, mouth shape and acting template is a sequence FAIL unless the story
specifically requires emotional stasis. Do not solve this with fixed left/right/front
quotas; verify that the beat change is visible.

Generic glossy anime/webtoon beauty treatment, detailed irises, shiny hair,
cinematic blur/light, global beige wash, cloned extras, or unnecessarily complete
backgrounds are rejection traits.

## 9. Anatomy/contact

See `docs/ANATOMY_CONTACT_POLICY.md`.

Use an anatomy contract only when limb/contact ownership is genuinely risky.
Declare semantic limb roles, required contacts, forbidden extra/disconnected limbs,
and the least destructive simplification fallback. Story-bearing contact outranks
decorative gesture.

## 10. Master-board QC and repair routing

Inspect actual pixels in this order:

1. output contract and text contamination;
2. target cast/cardinality and board-wide style;
3. multidimensional style match;
4. anatomy/contact/device/reflection geometry;
5. beat meaning and object-state continuity;
6. facial acting versus emotional delta;
7. camera/acting repetition;
8. unnecessary background/detail burden.

Routing:

- board-wide style/identity/palette/semantic failure -> one whole-board retry;
- isolated hand/limb/contact/expression/beat failure -> repair only that slide;
- upstream story/storyboard error -> return to the owning text stage; do not prompt-loop.

Rejected art is quarantined and cannot become reference evidence.

## 11. Slides and art-sequence QC

Each occupied cell becomes a separate 4:5 slide by deterministic split/resize when
possible, otherwise faithful built-in expansion bound to the approved board.

Sequence QC checks identity, clothing, palette, sparse location anchors, prop states,
anatomy, information geometry, expression fidelity, emotion delta, and viewer-
perceived repetition. Background simplicity is not a defect when the beat remains
clear.

## 12. Lettering

See `docs/LETTERING_STYLE_POLICY.md`.

Art remains text-free until art lock. Final v2 lettering requires
`config/lettering_style.json.status == LOCKED`.

The renderer must respect semantic role, approved font, size range, line spacing,
bubble weight and padding. It must never silently shrink text to hide overflow.

The previously used generic Noto Sans KR treatment is not considered locked merely
because the font file exists.

## 13. FINAL_QC / EXPORT / DONE

Review narrative slides and cover at thumbnail and full size.

Verify:

- exact wording and role;
- speaker/thought ownership;
- typography fit and hierarchy;
- edge safety and reading order;
- visual rhythm and final landing;
- no objective anatomy/contact/screen/text contamination failure;
- one 1080x1350 file/evidence record per narrative slide;
- separate cover evidence;
- state/QC/export consistency.

`DONE` requires structured QC and artifact evidence. A chat statement is not enough.

## 14. Execution surfaces

### Chat

Chat uses bounded autonomous turns with durable boundaries:

`PREPRODUCTION_REVIEW -> BOARD_DISPATCH_READY -> ART_SEQUENCE_QC -> DONE`

At the first boundary, creative approval is real. At later boundaries, `계속` is a
control token, not a new routine approval.

### Work

Work stops at an unapproved preproduction review by default. Once editorial content
is approved, Work prefers one-shot execution through the same lifecycle to `DONE`
or a genuine retryable infrastructure/resource block.

## 15. Fault handling and retry budget

Do not switch to paid fallback.

- one whole-board retry maximum;
- two targeted repairs maximum per isolated slide;
- repeated structural failure triggers decomposition/simplification or upstream
  restaging, not infinite prompt loops;
- quotas/tool faults checkpoint exact resume action;
- independent text/code/QC work continues when possible.

## 16. Evidence

Every PASS records inspected artifact/handle, SHA-256 and dimensions when bytes exist,
producing dispatch, QC version, dependencies, and exact next action.

Editorial approval records the approved source/story/storyboard hashes. Rejected
artifacts remain immutable quarantine evidence and are never reusable.

## 17. Honest boundary

AI-created pixels are not represented as literally human-drawn. The enforceable
target is editorial specificity, visual restraint, coherent drawing language, and
human-like deliberate staging without generic model defaults.
