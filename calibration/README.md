# Board-first calibration

This fixture validates the architectural claim that one 2x2 sampling event can
hold a more coherent visual hand than four unrelated slide generations while
still delivering four separate slide files.

It is not a publishable episode and does not consume `E001`.

Pass requires:

1. one text-free 2x2 board with four clean 4:5 cells;
2. stable Harin identity, outfit, palette, line and location language;
3. story-serving medium-wide, detail, overhead and exterior framings;
4. valid hand/bottle, hand/basket and hand/bag contact;
5. no generic glossy AI/webtoon drift;
6. four separate 1080x1350 art files after split/expansion;
7. one deterministic Korean lettering smoke test.

`PILOT_STATE.json` records the actual live state. A built-in image quota block is
retryable and must never trigger a paid API fallback.

