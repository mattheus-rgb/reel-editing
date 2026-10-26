---
name: rough-cut
description: The cut every reel starts from. Use when they say "edit this reel", "edit my newest clip", "cut this down", "rough cut", "clean up my footage", "take out the bad takes". Transcribes once, cuts by transcript, stitches by sound, levels the voice, then stops for their review.
---

# Rough cut

Say it will take a few minutes the first time, then run the whole chain.

1. **Intake.** Newest clip in `inbox/` → `projects/<job>/raw/` (copy, never move). Job name: what
   they would call it out loud, kebab-case. Write `projects/<job>/intent.md` after transcribing.
2. **Transcribe once.** `uv run engine/cut/transcribe.py <job>` → `transcript/words.json`.
   Second runs return the cache; `--force` re-hears.
3. **Plan.** `uv run engine/cut/plan.py <job> --print`. Then read it against the rules:
   - keep the last take of a line they said more than once; that is never a question for them
   - drop filler-only fragments and false starts
   - keep every line that names an effect out loud ("imagine a big red arrow here")
   Edit `transcript/cuts.json` if the plan missed something. Never trim a boundary by eye.
4. **Stitch.** `uv run engine/cut/stitch.py <job>` runs restarts → onset snap → close pauses → frame
   grid → one ffmpeg render → master. Writes `outputs/<job>.mp4`.
5. **Script.** `uv run engine/cut/script.py <job>` → `outputs/<job>.script.json`, the cut-aligned words
   with Part D fixes applied. Every later step reads this file.
6. **Level.** `uv run engine/cut/level.py <job>`: voice to −16 LUFS, true peak ≤ −1.5 dBTP.
7. **Review ⏸.** `uv run engine/review/beats.py <job> --cut-only` for stills of the cut; show the kept
   lines as a table with timings and a link to `outputs/<job>.mp4`. Wait for their notes or "looks good".

Re-cuts: edit `cuts.json`, then steps 4–7 again. Never re-transcribe for a re-cut.

**Next:** "plan the graphics" (the `creative-plan` skill).
