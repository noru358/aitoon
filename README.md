# AIToon

AIToon is a ChatGPT-app-native production protocol for Korean Instagram comics.
It is designed around two constraints:

1. additional paid spend: **KRW 0**;
2. the result must read as a deliberately drawn human Instagram comic, not a
   generic AI illustration.

The system does not pretend that a prompt can guarantee those constraints. It
uses curated user-designated visual references, one-generation episode boards,
minimum-scope editing, deterministic state, and evidence-bound QC to make failures
visible and repairable.

## Canonical path

`human source -> story -> storyboard -> visual packet -> 2x2 master board ->`
`separate 4:5 slides -> lettering/UI -> sequence QC -> export`

The key rendering decision is **board-first, slide-final**:

- up to four related shots are drawn together once, preserving one sampled line,
  palette, character, and location language;
- the board is an internal artifact, never a publishable collage;
- each cell is then expanded to a separate 4:5 image without redesign;
- a local defect repairs one slide; a board-wide drift repairs one board.

This avoids both known failure modes: unrelated per-slide resampling and rigid
paper-doll asset composition.

## What “GPT app only” means

Allowed:

- ChatGPT/Work reasoning, web search, image input, built-in image generation and
  editing, file tools, and local Python execution supplied by the app;
- the user's existing GitHub repositories as read-only references;
- GitHub storage for this repository.

Disallowed by default:

- OpenAI API calls, third-party image APIs, paid renderer credits, paid SaaS,
  unattended account automation, and hidden manual drawing labor.

The app's included image limits are finite. The protocol therefore uses one
master-board generation per four slides, bounds repairs, and persists a retryable
state instead of silently switching to paid infrastructure.

## Start or resume

```bash
python -m pipeline.cli init E001 --title "working title" --slides 4
python -m pipeline.cli status E001
python -m pipeline.cli validate
```

The ChatGPT operator follows `docs/GPT_APP_PROTOCOL.md`. Machine policy is in
`config/policy.json`; episode files live under `episodes/<episode_id>/`.

## Repository map

| Path | Role |
|---|---|
| `AGENTS.md` | fail-closed boot and autonomy contract |
| `docs/GPT_APP_PROTOCOL.md` | canonical creative/execution protocol |
| `docs/PLATFORM_ASSUMPTIONS.md` | official capability evidence and uncertainty boundary |
| `config/policy.json` | machine-readable stages, retries, cost, reference and QC policy |
| `references/registry.json` | curated production reference authority and provenance basis |
| `docs/REFERENCE_POLICY.md` | primary/continuity/episode-local reference hierarchy and promotion rules |
| `schemas/` | episode, board, dispatch and QC contracts |
| `pipeline/` | state, validation, board extraction and command-line tools |
| `templates/` | prompts and editable episode artifacts |
| `tests/` | regression coverage for state and image packaging |
| `CURRENT_STATE.md` | current calibration state and exact resume action |

## Verification boundary

Code can verify state transitions, hashes, dimensions, separate-file delivery,
and unchanged dependencies. Visual style, identity, anatomy, acting, and meaning
still require the ChatGPT vision model to inspect the actual pixels and write a
structured QC report. Passing only the automated checks is never a visual PASS.
