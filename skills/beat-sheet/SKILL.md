---
name: beat-sheet
description: Numbered stills of every planned moment, with a legend, shown before anything renders. Use when they say "beat sheet", "storyboard", "show me the beats", "let me see it before you render", or "beat 4 change this". Offered on every build.
---

# Beat sheet

1. `uv run "${CLAUDE_PLUGIN_ROOT:-.}"/engine/review/beats.py <job>` → `beat-sheet/sheet.jpg` and `beat-sheet/beats.json`.
   One still per beat from `plans/graphics.json`, legend: beat number, time, element, words, motion.
2. Show the sheet. This is the artefact to send a client for sign-off when the agency wants one: it
   is one image, numbered. Notes come back by beat number ("beat 3: smaller", "drop beat 5").
3. Apply notes to `plans/graphics.json`, regenerate, show again. ⏸ until "looks good".

Never render before the sheet is approved.

**Next:** "build it".
