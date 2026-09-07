# Lettering and cover style policy

Status: canonical companion to `GPT_APP_BOARD_FIRST_V2`.

## Typography lock

Final lettering for protocol revision 2+ must use a project-level style profile in
`config/lettering_style.json` with status `LOCKED`. The current profile is
`CALIBRATION_PENDING` because the previous font/scale treatment was rejected.

Do not silently shrink text to make it fit. Edit wording, box geometry, or the
approved style plan instead.

Text is semantic, not one generic caption channel. Supported roles are
`DIALOGUE`, `THOUGHT`, `NARRATION`, `SFX`, `UI`, and `TITLE`.
Thought/narration is optional and selected by beat; silence remains valid.

## Cover

A cover is required for protocol revision 2+ but is not counted as a narrative
slide. Default strategy is `DERIVED_FROM_APPROVED_ART`: reuse/crop approved
episode art or a simple spot from it, then add title typography separately.
Generate dedicated cover art only when approved art cannot communicate the hook.

The cover and narrative lettering are checked together for font fit, hierarchy,
reading order, margins, bubble weight, and compatibility with the drawing language.
