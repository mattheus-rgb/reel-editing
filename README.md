# Reel Editing Engine

A Claude Code project that turns a phone clip into a finished 9:16 reel. You film it; Claude edits
it, using the rules, skills and toolbelt in this folder. Editing is the only job: posting stays with you.

## What it does

```
clip in inbox/ → rough cut → you review → creative plan → build → beat sheet → render → export
```

- **Rough cut.** Your clip is transcribed once, cut by the transcript (last take of every repeated
  line, filler dropped), stitched with every boundary on the real voice onset, and levelled to −16 LUFS.
- **Creative plan.** Line by line, what goes on screen: hook, captions, a card or a held word. Asked
  as two single questions: teaching or confessional, MP4 or CapCut draft.
- **Build and render.** Each graphic is its own transparent layer in your style pack's fonts and
  colours, placed around your head from a measurement of your footage, rendered through a check gate
  and cached. Then composited to an MP4, or (v1) handed over as an editable CapCut draft with every
  element on its own track.
- **Learn.** Anything you want kept for next time becomes a bounded preference the builds apply.

## Getting started

1. Install [Claude Code](https://claude.com/claude-code) and open this folder in it.
2. Say **"set me up"**. Claude runs `./check-setup.sh`, installs what is missing (Homebrew is the
   one step you type yourself), builds the toolbelt and the renderer.
3. Say **"build my homebase"** and answer the interview. It fills `brand-kit.md`, the one file
   that is yours: who you are, how you sound, how you look, words the transcriber gets wrong.
4. Download the Neutral pack's fonts into `assets/fonts/` (see the README there).
5. Drop a clip in `inbox/` and say **"edit this reel"**.

Keep this folder out of iCloud Drive; `~/projects/` is right.

## Phrasebook

| Say | Skill |
|---|---|
| set me up | `set-me-up` |
| build my homebase | `homebase` |
| edit this reel, cut this down, rough cut | `rough-cut` |
| plan the graphics, what goes on screen | `creative-plan` |
| beat sheet, storyboard | `beat-sheet` |
| build it, render, looks good | `build` |
| remember that, from now on, /learn list, /learn forget N | `learn` |
| it's stuck, it failed, /report-a-problem | `report-a-problem` |

## Layout

| Where | What |
|---|---|
| `CLAUDE.md` | the persona, the locked road and the twelve rules Claude follows every session |
| `brand-kit.md` | yours: identity, voice, look, transcriber fixes, learned preferences |
| `.claude/skills/` | one folder per phrase above: trigger words plus a numbered recipe |
| `.claude/hooks/` | session briefing, CapCut draft guard, a chime when Claude waits |
| `engine/` | the Python toolbelt, one package per stage (`cut`, `measure`, `packs`, `type`, `render`, `sound`, `review`, `learn`, `capcut`, `doctor`) |
| `engine/packs/packs.json` | style packs; `user-packs.json` holds yours |
| `projects/<job>/` | one folder per reel: `raw/ transcript/ outputs/ plans/ review/ layers/ beat-sheet/` |
| `inbox/` | drop clips here |
| `_local/` | learned preferences, render cache, machine notes; never committed |
| `docs/` | the design blueprint and the build plan |
| `tests/` | `uv sync --extra dev`, then `uv run pytest` |

## Requirements

Mac (Apple Silicon), ffmpeg, uv, Node, CapCut desktop for the CapCut route. Python 3.11 is
managed by uv. Pins: WhisperX 3.8.6 / torch 2.8.0 for speech, HyperFrames 0.8.181 for graphics.

## Status

v0 scaffold. Real today: the rules, skills, brand-kit template, hooks, safe zones, the Neutral pack
loader and learned preferences. Every other script in `engine/` is a stub carrying its contract in its
docstring. Build order: cut → measure → type and render → plan, beat sheet, sound → homebase and packs
→ CapCut. See `docs/GENERIC-ENGINE-PLAN.md`.

## Privacy

Nothing leaves your computer. Transcription and rendering run locally, the renderer's telemetry is
switched off, and no file is uploaded anywhere by the engine.
