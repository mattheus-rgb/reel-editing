---
name: creative-plan
description: Decides line by line what goes on screen, once the cut is approved. Use when they say "plan the graphics", "what goes on screen", "creative plan", "which lines get a card", or right after a rough cut is approved. Asks the register and the finish here, never earlier.
---

# Creative plan

1. Read `outputs/<job>.script.json` and the brand's `brand-kit.md` Parts B and C (brand first, then
   `brands/_agency/brand-kit.md` for anything blank).
2. **Measure.** `uv run "${CLAUDE_PLUGIN_ROOT:-.}"/engine/measure/subject.py <job>` → `plans/subject.json` (head box, open zones).
3. **Register ⏸.** ONE pick-one: "Teaching or confessional?" with the kit's usual register marked.
   Teaching = hook, captions, up to three cards or list lines, a takeover word on the payoff.
   Confessional = hook, captions, maybe one held word. Never a summary card.
4. **Finish ⏸.** ONE pick-one: "MP4, or a CapCut draft?" (CapCut only once `engine/capcut/` exists).
5. Write `plans/graphics.json`: `{job, register, finish, pack, beats:[{id, start, end, line, element,
   zone, text, why}]}`. `zone` comes from `plans/subject.json`, never typed. Every `text` is their
   words in the brand's language and voice; the hook never mirrors the spoken opener.
6. Record: `uv run "${CLAUDE_PLUGIN_ROOT:-.}"/engine/review/gates.py record <job> register=… finish=…`.
7. Show the plan inline as a table (`uv run "${CLAUDE_PLUGIN_ROOT:-.}"/engine/review/plan_table.py <job>`). ⏸ one approval.

**Next:** "beat sheet", or "build it" (the beat sheet is offered on every build).
