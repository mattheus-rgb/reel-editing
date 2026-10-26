---
name: build
description: The one build pass, then the render. Use when they say "build it", "render", "export", "looks good, go", "make the reel". Builds every layer from the approved plan, renders through the check gate, composites to MP4 or hands to CapCut.
---

# Build

Say it will take a few minutes, send them off, do it all.

1. Read `plans/graphics.json`. Refuse to start if the beat sheet was not approved (`review/choices.json`).
2. `uv run engine/type/build.py <job>`: one composition per layer in `layers/<name>/`, skinned from the
   pack by role. Hook size through `engine/measure/fit.py`.
3. `uv run engine/render/render.py <job>`: each layer through the check gate, then rendered to a
   transparent `.mov`, cached by content. A failed check is ONE warning line; render as placed.
4. `uv run engine/sound/sfx.py plan <job>`: one cue per graphic arrival, never on cuts; density from
   the kit; levels from `engine/sound/levels.py`.
5. **MP4:** `uv run engine/render/composite.py <job>` → `outputs/<job>.final.mp4`.
   **CapCut:** `uv run engine/capcut/draft.py <job>` with CapCut quit; every element its own track.
6. Say once what got applied and how to change it. If any check flagged text near their face, say
   so once, plainly, and deliver anyway.
7. End of reel: `uv run engine/learn/teach.py offer <job>`; if it prints notes, run the `learn` flow.

**Next:** check it on your phone; "remember that" for anything to keep for next time.
