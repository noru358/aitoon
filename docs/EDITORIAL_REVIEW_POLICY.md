# Editorial preproduction review policy

Status: canonical companion to `GPT_APP_BOARD_FIRST_V2`.

## Purpose

Automation must not remove the user's editorial role. For protocol revision 2 and
later, every publishable episode reaches `PREPRODUCTION_REVIEW` before source,
story, or storyboard locks become authoritative.

The review is one compact creative gate, not a return to per-frame approval.

## Review payload

Show the user, in one place:

- source/topic and traceable URL;
- one-line premise and emotional engine;
- narrative slide count;
- beat-by-beat storyboard;
- all proposed dialogue, thought, narration, SFX, and meaning-bearing UI;
- cover title/concept;
- any material uncertainty or adaptation choice that could change the episode.

The user may approve, edit, replace, or reject any of these items.

## Lock semantics

`editorial_review.json` records the approved SHA-256 values of `source.md`,
`story.md`, and `storyboard.json`. After approval, advancing into
`SOURCE_LOCK` fails closed if any reviewed file has changed.

Technical steps after the editorial lock remain autonomous: reference retrieval,
hashing, dispatch compilation, anatomy/contact QC, retry routing, splitting,
lettering execution, export, and validation do not request routine approval.

A plain Chat continuation token is not editorial approval unless the user has
actually approved the presented review content.
