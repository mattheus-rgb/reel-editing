# Reel Editing Engine

A Claude Code project for an agency's designer or video editor: a client's phone clip in, a finished
9:16 reel out, in that client's voice and look. One engine, one folder per client brand. Editing is
the only job; posting and client sign-off stay with the agency.

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
3. Fill the house defaults: "build the homebase for _agency".
4. Make a client: **"new brand acme-coffee"**, then **"build the homebase for acme-coffee"** from the
   client's brief. It fills `brands/acme-coffee/brand-kit.md`: who they are, how they sound, how they
   look, words the transcriber gets wrong. Their licensed fonts go in `brands/acme-coffee/fonts/`.
5. Download the Neutral pack's fonts into `assets/fonts/` (see the README there).
6. Drop the client's clip in `inbox/`, say **"switch to acme-coffee"** if it is not active, then
   **"edit this reel"**.

Every setting resolves brand → `brands/_agency` → engine default, so a client with no pack of their
own gets the agency's, and one brand's voice never leaks into another's reel.

Keep this folder out of iCloud Drive; `~/projects/` is right.

## Phrasebook

| Say | Skill |
|---|---|
| set me up | `set-me-up` |
| switch to <brand>, which brand, new brand <name> | `engine/brand.py` |
| build the homebase for <brand> | `homebase` |
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
| `brands/<brand>/` | one per client: `brand-kit.md packs.json learned.json fonts/ projects/` |
| `brands/_agency/` | house defaults every brand inherits; `brands/_template/` starts a new one |
| `.claude/skills/` | one folder per phrase above: trigger words plus a numbered recipe |
| `.claude/hooks/` | session briefing, CapCut draft guard, a chime when Claude waits |
| `engine/` | the Python toolbelt, one package per stage (`cut`, `measure`, `packs`, `type`, `render`, `sound`, `review`, `learn`, `capcut`, `doctor`) |
| `engine/packs/packs.json` | style packs; `user-packs.json` holds yours |
| `brands/<brand>/projects/<job>/` | one folder per reel: `raw/ transcript/ outputs/ plans/ review/ layers/ beat-sheet/` |
| `inbox/` | drop clips here |
| `_local/` | the active brand, render cache, machine notes; never committed |
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

Nothing leaves the editor's computer. Client footage, fonts and learned preferences under `brands/`
are git-ignored; only each brand's kit and packs are committed, so keep this repository private. Transcription and rendering run locally, the renderer's telemetry is
switched off, and no file is uploaded anywhere by the engine.
