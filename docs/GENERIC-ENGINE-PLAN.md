# Generic Reels Engine for a new creator: build plan

Companion to `REBUILD-BLUEPRINT.md`. That document says what the current engine is; this one
says what to build for a team member who is their own creator, in what order, and what "done"
looks like at each step. Everything here is written fresh; nothing from the licensed engine is
copied.

Working name below: **the Engine**. Rename at will.

---

## 1. Scope decisions

| Decision | Choice | Why |
|---|---|---|
| Platform | Mac only, Apple Silicon | one person, one machine; drops ~3,000 lines of shims |
| Formats | Yap (talking head) only at v0 | the other formats are forks of the same pipeline; add later |
| Review | chat + beat-sheet stills at v0; visual editor deferred | the editor is ~15,000 lines; stills review works |
| Output | MP4 first, CapCut draft second | MP4 needs no VectCut; CapCut is a v1 add |
| Updates | git, no signed updater | it's your own code; `git pull` is the update |
| Personal layer | `brand-kit.md` + `_local/` + `packs/` ignored by git | same separation, simpler mechanism |
| Persona | written for the actual person, by name, their pronouns | the original's "she / mom" voice is not theirs |

---

## 2. Folder skeleton

```
the-engine/
├── CLAUDE.md                 # ~12 KB: persona, rules, phase table, where things live
├── SETUP.md                  # what "set me up" installs, for humans
├── brand-kit.md              # THE one file the creator fills (template in section 3)
├── check-setup.sh            # reports missing tools, prints the install line for each
├── pyproject.toml            # uv-managed; pins everything in section 7
├── .gitignore                # _local/, projects/, inbox/, packs/user-*.json, *.mp4
├── .claude/
│   ├── settings.json         # hooks, allow ffmpeg/ffprobe/uv run, deny secrets folders
│   ├── hooks/
│   │   ├── session-nudge.sh  # tools missing? brand-kit unfilled? say so once
│   │   ├── protect-drafts.sh # PreToolUse: block destructive touches to CapCut's draft folder
│   │   └── chime.sh          # Notification: sound when Claude waits
│   └── skills/               # section 5
├── engine/                   # the Python toolbelt (section 6), importable as a package
│   ├── cut/      transcribe.py  plan.py  stitch.py  snap.py  restarts.py  pauses.py  script.py  level.py
│   ├── measure/  subject.py  safe_zones.py  fit.py
│   ├── packs/    load.py  write.py  packs.json  neutral-pack/
│   ├── type/     build.py  template/ (HyperFrames comp)  effects.py
│   ├── render/   render.py  gate.py  cache.py  composite.py
│   ├── sound/    levels.py  sfx.py  sfx/ (CC0 index + files)
│   ├── capcut/   draft.py  safety.py  tracks.py   (v1)
│   ├── review/   beats.py  plan_table.py  gates.py
│   ├── learn/    prefs.py  teach.py
│   └── doctor/   report.py
├── assets/fonts/             # OFL fonts only
├── inbox/
├── projects/<job>/           # raw/ transcript/ outputs/ plans/ review/ layers/ beat-sheet/
└── _local/                   # learned.json, machine.txt, server state
```

---

## 3. Fresh `brand-kit.md` template

The homebase skill fills this by interview. Every `{{field}}` blank blocks nothing; an edit
goes ahead with defaults, but the engine suggests the interview once per session until the
count of blanks is 0. Write it to `brand-kit.md` exactly like this:

```markdown
# Brand kit

## Part A: who you are
- Name: {{name}}
- Pronouns: {{pronouns}}
- Handles: {{handles}}
- One line on what you do: {{what_you_do}}
- Who you make reels for: {{audience}}
- What they are stuck on: {{audience_pain}}

## Part B: how you sound
- Three words for your tone: {{tone_words}}
- A line you would say / a line you would never say: {{say}} / {{never_say}}
- Spelling: {{spelling}}            (UK / US)
- Contractions: {{contractions}}    (yes / mostly no)
- Banned words and phrases: {{banned}}
- Punctuation rules: {{punctuation}}
- Usual register: {{register}}      (teaching / confessional / ask each time)
- How a reel should end: {{endings}} (question / micro-action / nothing)

## Part C: how you look
- Style pack: {{pack}}              (Neutral to start; "build my pack" makes yours)
- Accent colour: {{accent}}
- Where captions sit: {{caption_zone}} (under chin / above head)
- Camera: {{camera}}                (still / slow push-ins / none)
- Sound density: {{sfx}}            (none / light / full)
- Music under voice: {{music}}      (none / yes, quiet)

## Part D: words the transcriber gets wrong
- {{word}} → {{fix}}

## Part E: learned preferences
(the engine appends one bullet per thing you teach it; `learn forget N` removes one)
```

The engine reads Parts A–D by a small parser (`engine/learn/prefs.py` reads the kit into a dict
once per run) rather than relying on Claude to re-read prose. Part E mirrors `_local/learned.json`.

---

## 4. CLAUDE.md outline (target 10–14 KB)

1. **Who you are talking to.** Their name, their pronouns, their engine. Tone: plain, warm,
   short. Long steps get one "go grab a coffee" line, then no check-ins.
2. **What this does.** Footage in, a reel out. Editing only; posting is theirs.
3. **The road, locked.** clip → rough cut → review ⏸ → creative plan ⏸ (register + finish asked
   here, never before) → build → beat sheet ⏸ → render → export. Nothing about the reel is
   asked before the cut.
4. **Rules.** Twelve lines, one each:
   plan→approve→build once · every cut goes through the stitch tool, never hand-trimmed ·
   transcribe once, the cut script is truth · measure placement, never type a number ·
   a check warns, never blocks · one layer per change · pack is config, never code ·
   register ≠ doneness · never replace a CapCut draft, CapCut quit for every write ·
   learned prefs are allowlisted · every on-screen word is in their language and their voice ·
   fix the system when a correction will recur.
5. **Brand kit.** Where it is, the blank count check, "build my homebase" once per session.
6. **Where things live.** The folder table.
7. **Phrasebook.** One line per skill with its trigger words.
8. **How the engine carries itself.** Never ask what the files answer; every handoff ends with
   "Next:"; nothing leaves the computer.

No personal style rules live here. They live in `brand-kit.md` and `_local/learned.json`.

---

## 5. Skills (v0: eight)

Each `SKILL.md`: frontmatter `name`, `description` opening with the trigger phrases, then a
numbered recipe. Keep each under 6 KB.

| Skill | Triggers | Recipe (scripts in order) |
|---|---|---|
| `set-me-up` | set me up, first run, setup | `check-setup.sh` → install what it flags (brew, one warm line + OK first) → `uv sync` → `npx hyperframes@<pin> browser ensure` → offer homebase |
| `homebase` | build my homebase, redo my brand kit | interview Parts A–D one part at a time → write `brand-kit.md` → offer one real clip |
| `rough-cut` | edit this reel, cut this, rough cut, edit my newest clip | intake copy → `transcribe` → `plan --print` → Claude edits the plan → `stitch` → `script` → `level` → beat stills of the cut → review ⏸ |
| `creative-plan` | plan the graphics, what goes on screen | read script + `subject` zones → ask register (pick-one) → ask finish MP4/CapCut (pick-one) → write `plans/graphics.json` → show as a table ⏸ |
| `beat-sheet` | beat sheet, storyboard, show me the beats | `beats.py` → numbered stills with legend → notes by number ⏸ |
| `build` | build it, render, looks good | `type/build.py` per layer → `render.py` with gate + cache → `composite` → MP4, or `capcut/draft.py` |
| `learn` | remember that, from now on, learn my pattern, /learn list, /learn forget | `prefs.py add <field> <value>` + bullet in Part E; end-of-reel `teach.py` checklist |
| `report-a-problem` | it's stuck, it failed, something's broken | `doctor/report.py` → one pasteable file |
| `style-pack` (v1) | build my pack, switch to <pack> | `packs/write.py --from Neutral --set …` |

---

## 6. The toolbelt: each script, its contract, its "done" test

Every script is `uv run engine/<area>/<name>.py <job> [flags]`, reads and writes only inside
`projects/<job>/`, prints one line per thing it did, and never asks a question (Claude asks).

### cut/
| Script | In → Out | Done when |
|---|---|---|
| `transcribe.py` | `raw/*.mov` → `transcript/words.json` `{clips:[{clip,path,duration,words:[{word,start,end,score}]}]}` | a 60 s clip transcribes with per-word times; second run returns the cache; `--force` re-hears |
| `plan.py` | words.json → `transcript/cuts.json` `{segments:[{clip,start,end,text}]}` | keeps the last take of a repeated sentence; drops filler-only fragments; `--print` shows kept/dropped lines |
| `restarts.py` | cuts + audio → cuts (tightened) | a deliberate "so what I… so what I did" keeps only the second |
| `snap.py` | cuts + audio → cuts (onset-snapped) | every in-point is ~40 ms before voice, out ~60 ms after |
| `pauses.py` | cuts → cuts | silences > 0.7 s inside a kept segment are closed |
| `stitch.py` | cuts → `outputs/<job>.mp4` | boundaries frame-snapped; equal-power crossfade at joins; one ffmpeg graph; static +gain and limiter; no clicks at joins (listen) |
| `script.py` | words + final cuts → `outputs/<job>.script.json` | every kept word re-timed onto the cut's clock; Part D fixes applied |
| `level.py` | mp4 → mp4 | −16 LUFS integrated, true peak ≤ −1.5 dBTP, one static gain |

### measure/
| Script | In → Out | Done when |
|---|---|---|
| `subject.py` | mp4 → `plans/subject.json` `{head:{top,bottom,left,right}, zones:{above,below,left,right}}` | OpenCV YuNet on sampled frames; median head box; zones in px and as 0–1 y |
| `safe_zones.py` | – | one module: top 270 / bottom 300 px bands on 1080×1920, scaled for other canvases |
| `fit.py` | text + font + max width → px size | hook never overflows the safe width at peak animation scale |

### packs/
| File | Contract |
|---|---|
| `packs.json` | `{packs:{Neutral:{fonts:{headline,caption,aside}, roles:{hook,caption,takeover,aside:{font,size,case,tracking}}, colors:{light,dark,accent}, shadow}}}` |
| `load.py` | `role(pack,"hook")` returns a resolved dict with a real font file or a warned fallback; a build with no pack fails loud |
| `write.py` | `--name X --from Neutral --set colors.accent=#…`; refuses to touch an existing pack without `--force`; user packs saved to `packs/user-packs.json` (gitignored) |
| `neutral-pack/` | Inter + Instrument Serif, white, soft shadow; the starting look for any creator |

### type/ and render/
| Script | Contract |
|---|---|
| `type/build.py` | `plans/graphics.json` + pack → one HyperFrames composition per layer in `layers/<name>/` (index.html, hyperframes.json, fonts/); kinds at v0: hook, captions (word-by-word), takeover word, simple card |
| `type/effects.py` | the named animation vocabulary (rise, pop, typewriter, fade) emitted as GSAP; packs pick by name |
| `render/gate.py` | runs `npx hyperframes@<pin> check`; a failure is one warning line, never a stop (`--strict` to refuse) |
| `render/render.py` | comp → `.mov` (ProRes 4444 alpha); cache by content hash in `_local/render-cache/`; one render at a time |
| `render/composite.py` | base + layers@start + sfx → `outputs/<job>.final.mp4` in one ffmpeg pass |

### sound/
| Script | Contract |
|---|---|
| `levels.py` | the one table: voice −16 LUFS; SFX −8 dB under voice peak; music −12 dB under voice (defaults; Part C overrides) |
| `sfx.py` | `--list` from `sfx/index.json` (file, material, mood); `place <cue> at <t>` writes `plans/sound.json`; one cue per graphic arrival, never on cuts |

### review/ and learn/
| Script | Contract |
|---|---|
| `review/beats.py` | plan + mp4 → `beat-sheet/sheet.jpg` numbered stills with legend (beat, time, element, words, motion) |
| `review/plan_table.py` | graphics.json → markdown table for chat |
| `review/gates.py` | prints the pick-one JSON for register / finish; records `review/choices.json` |
| `learn/prefs.py` | allowlist with clamps: `caption.zone`, `caption.size_scale`, `hook.size`, `sfx.density`, `music.duck_db`, `camera.push`; `add / forget / list / get`; mirrors to brand-kit Part E |
| `learn/teach.py` | end of reel: turns review notes into candidate rules, one pick-many box, saves the ticked ones |

### capcut/ (v1)
| Script | Contract |
|---|---|
| `draft.py` | main track = one clip per kept line; each layer `.mov` its own named track; each SFX its own clip; LUT not baked |
| `safety.py` | refuse while CapCut runs; never reuse a draft name (`1.1 → 1.2`); hook blocks rm in the drafts folder |
| `tracks.py` | thin client for a VectCut-style server you run yourself (fork sun-guannan/VectCutAPI, Apache 2.0) |

---

## 7. Pins (pyproject.toml / package.json)

```
python = 3.11
whisperx = 3.8.6, torch = 2.8.0, torchaudio = 2.8.0, ctranslate2 = 4.8.1
faster-whisper (verify pass, model small)
opencv-python-headless, numpy, pillow, pyloudnorm (or ffmpeg ebur128)
node: hyperframes@0.8.181 (or the newest you test against; pin it, never @latest)
```
Fonts: OFL only in the repo (Inter, Instrument Serif, Playfair Display, DM Sans). SFX: CC0 only,
with the source URL in `index.json`.

---

## 8. Build order and milestones

| Week | Milestone | Done when |
|---|---|---|
| 1 | **Skeleton + cut** | `set-me-up` passes on a clean Mac; "edit this reel" produces a clean `outputs/<job>.mp4` and script JSON from one phone clip; joins have no clicks; voice at −16 LUFS |
| 2 | **Measure + review** | subject zones JSON; beat stills of the cut; review ⏸ works as a chat table; `learn` writes and reads prefs |
| 3 | **Type + render** | hook + word captions in the Neutral pack over the cut, placed above the head from the measured zones, through the HyperFrames gate, cached; MP4 out |
| 4 | **Creative plan + beat sheet + sound** | register pick-one shapes the plan; beat sheet before any render; 3–4 SFX at the right duck; the whole road runs end to end on three different clips |
| 5 | **Homebase + their pack** | the interview fills the kit; `style-pack` builds their pack from two colours and three fonts; every on-screen font resolves from the pack by role |
| 6 (v1) | **CapCut handoff** | VectCut fork running; draft lands in CapCut with every element its own track; safety rules enforced; "never replace" tested |
| later | visual editor, voiceover format, b-roll reels, carousel | only if chat + stills review proves too slow |

Three test clips to keep in `tests/fixtures/`: a clean single take, a take with two restarts
and a long pause, a clip with the head high in frame (so "above head" has no room).

---

## 9. Deliberately not ported

Windows / Store / Intel shims · signed update feed and keep-changes merge · the original
in-chat widget road (one review road only) · Canva / DESIGN.md pack importers · trial reels ·
face cover · DaVinci bridge · favorites-from-CapCut import · the hashtag reminder · any
creator-specific house style (lost-my-hours look, BP evidence, warm-film-light grade). The new
creator's style arrives through their own kit, their own pack and what they teach.
