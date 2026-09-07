# Board-first calibration findings

Date: 2026-09-07  
Pilot: `BOARD_FIRST_V1`  
Board: `B01`

## Result

`FAIL` for the complete production-quality gate. Both generated boards were
inspected from their actual 1122x1402 PNG pixels. They remain quarantined and
must not be used as style, continuity, split, repair, lettering, or publishing
inputs.

## What the experiment established

Board-first materially improved within-board continuity. Both attempts produced
a clean 2x2 sequence with stable Harin identity, outfit and palette, varied
story-serving cameras, readable object-state progression, and mostly plausible
contact geometry. Attempt 2 also removed the text-like packaging artifact and
made the wallet unambiguous.

Board-first did not by itself make the image look human-drawn. Attempt 2's
stronger prompt exclusions did not dislodge smooth outlines, modeled clothing
and hair, bottle reflections, polished perspective, or dense retail detail. The
result stayed in a generic polished AI/webtoon basin.

## Architectural decision

Keep `MASTER_BOARD` as the default coherence unit, but treat it only as a
continuity mechanism. Human-drawn quality must be established independently by
the visual packet and confirmed at master-board QC.

Do not run a third prompt variation against `B01`. The current references are
useful for identity and broad drawing language, but their registry explicitly
does not assert human authorship, and two images provide insufficient authority
over the renderer's finish. The next calibration must use a new board ID and a
provenance-verified multi-image human-authored packet that separately anchors:

1. line endings, wobble and weight variation;
2. flat-color boundaries and maximum shading depth;
3. face, hair and clothing simplification;
4. sparse background and blank-package treatment;
5. one full-body interaction example.

The packet should describe measurable visual limits, not merely add more style
adjectives. Rejected generated images remain excluded from every future
reference set.

## Evidence

- Attempt 1: `B01.qc.a1.json`, quarantined PNG SHA-256
  `b436cc81a9f226f0cad87ee96ea9cfec2d0812c543c074f752fa05c578a277a7`
- Attempt 2: `B01.qc.a2.json`, quarantined PNG SHA-256
  `c984a5840d73f2448172f25f78b62e6ad4fb0513eeb442a1302c0fe4c6789aeb`

Separate-slide packaging and lettering were correctly skipped because only a
master-board PASS may enter those stages.
