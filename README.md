# AIToon

AIToon is a ChatGPT-app-native production protocol for Korean Instagram comics.
The current architecture is **GPT_APP_BOARD_FIRST_V2**.

Constraints:

1. additional paid spend: **KRW 0**;
2. output should read as a deliberately authored Instagram comic rather than a
   generic AI illustration;
3. the user retains one meaningful editorial checkpoint before creative locks.

## Canonical path

`human source -> draft source/story/storyboard/cover -> PREPRODUCTION_REVIEW -> locks -> visual packet -> 2x2 internal board batch -> separate 4:5 slides -> art QC -> semantic lettering + cover -> final QC -> export`

Episode narrative slide count is variable. The fixed 2x2 topology is only an
internal coherence batch with one to four occupied cells.

Key v2 changes:

- one hash-bound preproduction review for topic, dialogue, storyboard and cover;
- lowest-sufficient backgrounds and default omission of decorative assets;
- cover is required but separate from narrative slide count;
- thought/narration are explicit optional text roles;
- project-level typography must be calibrated and locked before v2 final lettering;
- style QC is multidimensional and rejects palette-only matches or repeated facial
  acting across meaningful emotional deltas;
- style references do not imply copying the people or rooms shown in them.

Board-first remains mandatory: once a board exists, narrative slides are derived from
that board rather than independently regenerated.

## Runtime and cost

Allowed: ChatGPT/Work reasoning, web research, image input, built-in image
generation/editing, local code/file tools, and GitHub storage.

Disallowed by default: paid APIs, paid renderer credits, paid SaaS, external paid
image models, and hidden manual production labor.

## Start or resume

```bash
python -m pipeline.cli init E003 --title "working title" --slides 4
python -m pipeline.cli status E003
python -m pipeline.cli validate
```

The canonical boot order is in `AGENTS.md`; this README is descriptive only.
`state.json.exact_next_action` controls resumed execution.

## Repository map

| Path | Role |
|---|---|
| `AGENTS.md` | fail-closed boot and execution contract |
| `CURRENT_STATE.md` | active repository/episode pointer |
| `docs/GPT_APP_PROTOCOL.md` | canonical v2 lifecycle |
| `docs/EDITORIAL_REVIEW_POLICY.md` | one user creative gate and hash lock |
| `docs/VISUAL_MINIMALISM_POLICY.md` | lowest-sufficient background/asset rules |
| `docs/LETTERING_STYLE_POLICY.md` | typography, semantic text, cover rules |
| `docs/REFERENCE_POLICY.md` | reference authority and promotion rules |
| `docs/ANATOMY_CONTACT_POLICY.md` | conditional physical-contact guard |
| `config/policy.json` | machine-readable lifecycle and QC policy |
| `config/lettering_style.json` | project typography calibration/lock |
| `references/registry.json` | production reference authority |
| `schemas/` | structured contracts |
| `pipeline/` | state, validation, dispatch, split and lettering code |
| `templates/` | episode draft/plan templates |
| `tests/` | regression coverage |

Automated checks can verify hashes, transitions, dimensions, packaging, editorial
locks, and policy invariants. Actual visual style, anatomy, acting, and meaning still
require inspection of the real pixels.
