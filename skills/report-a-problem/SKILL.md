---
name: report-a-problem
description: Any problem, before investigating by hand. Use when they say "/report-a-problem", "it's stuck", "it failed", "something's broken", "it's taking forever", "nothing happened", "I got an error", or paste an error.
user-invocable: true
---

# Report a problem

1. `uv run "${CLAUDE_PLUGIN_ROOT:-.}"/engine/doctor/report.py` collects: tools and versions, the last job's step log
   (`_local/steps.log`), what is still running, disk space, the tail of the last error.
   It writes `_local/problem-report.md`.
2. Read it. If the engine already has a fix (a missing tool, a stale cache, CapCut still open),
   apply it and re-run the step that failed.
3. Otherwise explain in two lines what happened and what to try, and point them at the report file.

Never force past a renderer, never stop a render that is still counting frames.

**Next:** re-run the step, or paste the report.
