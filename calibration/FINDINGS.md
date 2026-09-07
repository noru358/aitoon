# Board-first calibration findings

Date: 2026-09-07  
Pilot: `BOARD_FIRST_V1`  
Board: `B01`

## Result

Attempt 2 is the accepted master board. The user explicitly approved the actual
rendered pixels and described the artwork as fully passing and highly
satisfactory. That approval supersedes the earlier automated style rejection.

Attempt 1 remains rejected and quarantined. Attempt 2 is stored as
`B01.master.png` and may be used for deterministic slide packaging and future
continuity.

## What the experiment established

Board-first successfully produced a clean 2x2 sequence with stable Harin
identity, outfit and palette, varied story-serving cameras, readable object-state
progression, and plausible contact geometry. The single bounded retry also
removed the text-like packaging artifact and made the wallet unambiguous.

The earlier evaluator over-weighted abstract anti-AI style signals relative to
the user's actual aesthetic target. Subjective style acceptance therefore uses
the following authority order:

1. explicit user approval of inspected pixels;
2. hard output, anatomy, continuity and no-text constraints;
3. automated style heuristics as advisory evidence.

Automated QC must still reject objective defects, but it must not overturn an
explicit user style approval merely because the finish is smoother than its
internal estimate.

## Evidence

- Rejected attempt 1: `B01.qc.a1.json`, SHA-256
  `b436cc81a9f226f0cad87ee96ea9cfec2d0812c543c074f752fa05c578a277a7`
- Accepted attempt 2: `B01.qc.a2.json`, SHA-256
  `c984a5840d73f2448172f25f78b62e6ad4fb0513eeb442a1302c0fe4c6789aeb`

## Packaging result

The accepted board was deterministically split using measured source margins
and gutters. `S01` through `S04` are separate 1080x1350 PNG files and all passed
actual-pixel sequence QC. The Korean lettering renderer also passed a
hash-bound smoke test on `S04`; its first wrap defect was corrected before PASS.

The production architecture is therefore calibrated: board-first is the visual
coherence unit, while delivery remains one independent 4:5 file per slide.
