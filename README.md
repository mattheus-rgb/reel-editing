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

## Install

It is a Claude Code plugin. One line, on Claude Code 2.1.275 or later:

```bash
/plugin install reel-editing --marketplace mattheus-rgb/reel-editing
```

Other ways (a ZIP, pre-enabling it for the whole organisation) are in `INSTALL.md`.

## Getting started

1. Make a folder for your clients, open it in Claude Code.
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
| open my studio, show my clients, studio notes | `studio` |
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
| `templates/workspace/` | what a designer's folder starts with: `CLAUDE.md` (the persona, the road, the rules), `brands/_agency`, `brands/_template` |
| `<workspace>/brands/<brand>/` | one per client: `brand-kit.md packs.json learned.json fonts/ projects/` |
| `<workspace>/brands/_agency/` | house defaults every brand inherits |
| `skills/` | one folder per phrase above: trigger words plus a numbered recipe |
| `hooks/` | session briefing, CapCut draft guard, a chime when Claude waits (`hooks.json`) |
| `engine/` | the Python toolbelt, one package per stage (`cut`, `measure`, `packs`, `type`, `render`, `sound`, `review`, `learn`, `capcut`, `doctor`) |
| `engine/packs/packs.json` | style packs; `user-packs.json` holds yours |
| `<workspace>/brands/<brand>/projects/<job>/` | one folder per reel: `raw/ transcript/ outputs/ plans/ review/ layers/ beat-sheet/` |
| `<workspace>/inbox/` | drop clips here |
| `<workspace>/_local/` | the active brand, studio state; never committed |
| `docs/` | the design blueprint and the build plan |
| `tests/` | `uv sync --extra dev`, then `uv run pytest` |

## Requirements

Mac (Apple Silicon), ffmpeg, uv, Node, CapCut desktop for the CapCut route. Python 3.11 is
managed by uv. Pins: WhisperX 3.8.6 / torch 2.8.0 for speech, HyperFrames 0.8.181 for graphics.

## The Studio

Say "open my studio": a local page (127.0.0.1 only) listing every client, which one is active, each
client's setup state, and every reel with its stage from footage to final. Switch brands, add a
client, open folders, leave a note Claude reads with "studio notes".

## Status

v0.3: installable as a plugin; the engine and each designer's workspace are separate folders. Real today: the rules, skills, brand-kit template, hooks, safe zones, the Neutral pack
loader and learned preferences. Every other script in `engine/` is a stub carrying its contract in its
docstring. Build order: cut → measure → type and render → plan, beat sheet, sound → homebase and packs
→ CapCut. See `docs/GENERIC-ENGINE-PLAN.md`.

## Privacy

Nothing leaves the editor's computer. Client footage, fonts and learned preferences under `brands/`
are git-ignored; only each brand's kit and packs are committed, so keep this repository private. Transcription and rendering run locally, the renderer's telemetry is
switched off, and no file is uploaded anywhere by the engine.
