# Reels Editing Engine v2.3.15: analysis and rebuild blueprint

Written 2026-10-25 from a read of the installed engine. Describes the architecture and the
transferable design ideas in its own words so a similar system can be built independently.

---

## 0. Read this first: the licence

`LICENSE.md` (Homewell LLC) is explicit:

- One licence is one person. A team member, assistant or contractor "needs their own license".
- You may not copy, share or redistribute the Software or its files, "whether modified or not".
- Building your own separate system is allowed. Reselling or sharing this one is not.
- The vendored third-party parts have their own licences: HyperFrames skills and VectCutAPI
  are Apache 2.0, bundled SFX are CC0, fonts are OFL (see `THIRD-PARTY-NOTICES.md`).

So the two legitimate routes are:

1. **Buy a second licence** for the team member. Cheapest by far; they get updates and the
   visual editor for free. Then copy only the personal layer (section 5) across.
2. **Rebuild your own engine** on the same ideas, with your own code and skill text. This
   document is the blueprint for that. Do not copy `product/*.py`, the skill files or
   `CLAUDE.engine.md` verbatim.

The rest of this document assumes route 2 but is useful for route 1 too (it tells you what to
carry over).

---

## 1. What the engine is, in one paragraph

A Claude Code project folder that turns a phone clip into a finished 9:16 reel. Claude is the
editor; the folder gives it a persona, a phrasebook of skills, a Python toolbelt and a set of
hard rules. Footage goes in `inbox/`, gets transcribed once with WhisperX, cut by transcript,
stitched by ffmpeg with acoustic clean-up, reviewed by the creator on a local web page, dressed
with typographic "looks" rendered by HyperFrames (headless Chromium + GSAP), and handed over as
an editable CapCut draft (written through a vendored VectCut/pyJianYingDraft server) or a baked
MP4. Every creative choice is collected before one build pass; CapCut is polish only.

Size of the real thing:

| Layer | Approx. size |
|---|---|
| `product/*.py` | 140 files, ~54,000 lines |
| Rough-cut scripts (in the skill folder) | ~6,400 lines of bash + Python |
| Visual editor | `visual_editor.py` 6,458 lines + `editor.html` 6,964 lines + server 1,270 |
| Vendored VectCutAPI | ~9,700 lines Python + CapCut draft templates |
| Skills | 61 folders (36 engine-owned, 20 vendored HyperFrames toolkit, 5 doctrine) |
| CLAUDE.md | 56 KB, ~29% of it personal |
| Tests | 237 standalone test scripts |

A rebuild does not need most of that. Section 6 says what the minimal core is.

---

## 2. The five layers

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Claude Code scaffolding                                   │
│    CLAUDE.md (persona + operating rules)                     │
│    .claude/skills/<name>/SKILL.md (phrase-triggered recipes) │
│    .claude/settings.json (hooks, permissions, env)           │
│    .claude/hooks/*.sh (session nudges, draft protection)     │
├─────────────────────────────────────────────────────────────┤
│ 2. Personalisation (never overwritten by updates)            │
│    brand-kit.md · _local/learned.json · style packs ·         │
│    presets/caption-corrections.json · favorites/             │
├─────────────────────────────────────────────────────────────┤
│ 3. Orchestration docs (what Claude reads to decide)          │
│    product/FLOW.md · CLEANYAP.md · STYLE-PACKS-SPEC.md ·      │
│    WHY-IT-WORKS.md · WRITING-THE-HOOK.md                      │
├─────────────────────────────────────────────────────────────┤
│ 4. Python toolbelt (product/, scripts/, workflows/)          │
│    cut · audio · captions/type · layout · packs · CapCut ·    │
│    editor server · learned prefs · diagnostics                │
├─────────────────────────────────────────────────────────────┤
│ 5. External engines                                          │
│    ffmpeg · WhisperX (uv venv) · HyperFrames (npx, pinned) ·  │
│    VectCut Flask server :9001 → CapCut desktop · OpenCV       │
└─────────────────────────────────────────────────────────────┘
```

The important split is layers 1–2 (prose, read by Claude every session) vs layer 4 (code, run
by Claude). Skills are thin: most SKILL.md files are a trigger phrase list plus a numbered
recipe of which scripts to run in which order. The intelligence is in the rules, the code
makes the rules enforceable.

---

## 3. The pipeline, stage by stage

Each stage names its entry point, what it reads, what it writes. Artifact names are the
engine's; keep the same shape in a rebuild, the names are yours.

| # | Stage | Entry | Reads | Writes | Engine |
|---|---|---|---|---|---|
| 0 | Intake | `rough-cut` skill | newest clip in `inbox/` | `projects/<job>/raw/` (copy, never move), `intent.md` | ffmpeg (HDR→SDR, AV-sync pad) |
| 1 | Transcribe once | `word-timings.sh` | raw clips | `transcript/words.json` (per-word start/end/score) | WhisperX large-v3 + wav2vec2 align, in a uv venv |
| 2 | Cut plan | `transcript-cut.py` or Claude by hand | words.json | `transcript/cuts.json` (segments: clip, start, end, text) | stdlib |
| 3 | Stitch | `stitch-cut.sh` | cuts.json | `outputs/<job>.mp4`, `outputs/<job>.transcript.json` (the cut-aligned script every later stage treats as truth) | trim-restarts (MFCC/DTW) → snap-to-sound (onset ±ms) → close-pauses → frame-snap → one ffmpeg filtergraph → fixed gain + limiter → −16 LUFS |
| 4 | Review gate ⏸ | `review_gate.py` | – | `review/route.json` | AskUserQuestion pick-one |
| 5 | Review | `visual_editor.py open` | base cut + script | `transcript/script-review.json`, `review/phase.json` | local stdlib HTTP server on 127.0.0.1:47815, single-file HTML page |
| 6 | Creative plan ⏸ | `graphics-plan` skill | transcript, register, `subject-zones.json` | `graphics-plan.json` (beats: id, start, end, line, element, zone, idea), `caption-plan.json` | OpenCV YuNet face box → open zones |
| 7 | Build | `build-reel-type.py` / lookbook | caption-plan + pack | `hf-reel-type-<pack>/` or `hf-graphics/_looks/…` (HyperFrames compositions) | templates copied from `templates/hf-reel/` |
| 8 | Beat sheet ⏸ | `beat-sheet` skill | plan + looks | `beat-sheet/beat-sheet.jpg` (numbered stills with legend) | ffmpeg + Pillow |
| 9 | Render + finish | `finish.py run <job> capcut\|mp4` | looks, sound plan | per-layer `.mov` (content-hash cached), then CapCut draft or `outputs/<job>.final.mp4` | `hyperframes check` gate → `hyperframes render`; VectCut `/create_draft`…`/save_draft` |
| 10 | Export naming | `name-final.sh` | outputs | `<job>.final.mp4` + copy to Downloads | – |
| 11 | Teach | `teach_style.py offer` | review notes | `_local/learned.json` + brand-kit Part C | pick-many checklist |

Pauses (⏸) are the only places Claude stops: before the cut (phase-by-phase vs autopilot),
after the cut (review), at the creative plan (register, route), at the beat sheet, at finish.

### How the CapCut draft is written

- VectCutAPI is a Flask server wrapping pyJianYingDraft, which knows CapCut's draft JSON
  (`draft_info.json` on Mac). Calls: `create_draft` → `add_video`/`add_audio`/`add_text`
  (each with a `track_name`) → `save_draft` into `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/`.
- "Every element its own layer" is simply: every call gets a distinct track name, so each
  caption, look, SFX cue lands as its own clip on its own track. Never compound, never group.
- Safety rules are enforced in code, not prose: CapCut must be quit before a write
  (`pgrep -x CapCut`), a draft the creator opened is never replaced (versions `1.1 → 1.2`),
  and a PreToolUse hook blocks any Bash/Edit that touches the drafts folder destructively.
- Graphics that CapCut cannot build natively go in as transparent ProRes 4444 `.mov` per
  element; camera moves go in as CapCut keyframes, never baked.

---

## 4. The design principles worth stealing

These are the ideas that make it work, independent of any code.

1. **Plan → approve → build once.** All creative choices are collected at fixed gates, then one
   build pass. No creative choice after the build, none before the rough cut. Gate questions
   are a single pick-one with the default marked.
2. **One hearing, one script.** Transcribe once per job; after each stitch, re-time the kept
   words onto the cut's clock and write one transcript file. Captions, graphics, placement
   all read that file, so a word fix propagates everywhere.
3. **Cut by transcript, clean by sound.** The transcript decides what stays; the acoustic
   tools decide where exactly the boundary sits (word onset, restart detection, pause closing,
   frame snap). Never trim by eye, never hand-roll ffmpeg.
4. **Measure, never eyeball.** Head box and open zones are measured per reel from the footage.
   Safe bands come from one module. Hook size comes from a fit function, not a magic pixel.
5. **A check is a warning, never a wall.** Face overlap, off-frame text, failed render checks:
   fix automatically where possible, otherwise render as placed and say so once. The creator
   always gets her reel.
6. **A change costs one layer.** Each graphic is its own transparent layer, rendered through one
   function that caches by content hash. Changing one look never re-renders the reel.
7. **Style pack = config injection, never logic.** Fonts, colours, shadow and sizes live in JSON
   keyed by pack. One shared type builder does all animation. A pack that needs new code is a
   pack built wrong. Roles are resolved by job: captions, hook, takeover, thoughts.
8. **Two independent axes.** Register (teaching vs confessional) sets how loaded the graphics
   are; doneness (raw / medium / well-done) sets how baked the output is. Never let one imply
   the other.
9. **Personal layer is physically separate and protected.** `brand-kit.md`, `_local/`, user
   packs, corrections and `projects/` are on a protected list the updater never writes.
   CLAUDE.md is regenerated from a template plus the user's own "Applied" block.
10. **Learned preferences are an allowlist with clamps.** Only named fields (caption zone, SFX
    density, music duck dB, hook size…) can be taught, each bounded. Register, hook copy and
    pixel placements are deliberately not learnable.
11. **Never replace a draft.** CapCut has no version history, so every write is additive or a
    new version. Enforced by a hook and by every writer refusing while CapCut is open.
12. **Skills are phrase-triggered recipes.** Each SKILL.md opens with the exact things the
    creator might say, then a numbered recipe calling scripts. Thin skills, thick toolbelt.
13. **Hooks do the nagging, not the prose.** SessionStart hooks check tools, unfilled brand-kit
    fields, pending updates; a PreToolUse hook protects drafts; a Notification hook chimes
    when Claude is waiting. Nothing sends data anywhere.
14. **Fix the system, not the reel.** Any correction that will recur becomes a learned
    preference, a pack edit or an engine default.

---

## 5. What is generic vs what is Mattheus

If the team member edits **your** content, carry the personal layer over. If they are their
own creator, build only the generic layer and give them a fresh brand kit.

**Generic engine (reusable ideas, rewrite in your own words/code):**
CLAUDE.md sections on formats, operating rules, the phase table, house rules; all skills; the
Python toolbelt; FLOW/CLEANYAP/STYLE-PACKS specs; shipped packs Editorial/Playful/Butter.

**Personal (yours, portable as data):**

| Where | What |
|---|---|
| `brand-kit.md` Part A | identity, @ohheymattheus, voice, hard rules (no em dashes, no hype words), corrections |
| CLAUDE.md "Applied" block (~16 KB) | house style = lost-my-hours-30s, premium bar, locked text/hook/sound style (Instrument Serif lockups above head, payoff behind head, 4.5 s cover hook, marigold hero word, 3–4 SFX at −8 dB), no look-away frames, warm-film-light grade, voice at −15 LUFS with bed −12.5 dB, BP-01…26 evidence |
| `product/creative-vault/user-packs.json`, `user-style.json` | Mattheus Butter / Butter Bold / Editorial packs; default pack |
| `_local/learned.json` | 6 taught prefs: per-word crossfade captions, lighter SFX, captions above, music −12.5 dB, visual editor default |
| `_local/lookbooks/` | saved looks and custom designs |
| `presets/caption-corrections.json` | mattheus/matthias/matthews → Mattheus |
| `projects/style-references/` | the four-creator study and BP evidence |
| `RESOLVE-EDITING.md`, `workflows/davinci-resolve/` | the DaVinci route (hardcoded `/Users/mattheussozo` paths) |
| `assets/brand/luts/warm-film-light.cube` | the grade as a LUT |

Things to strip from any copy regardless: `_local/machine.txt`, `render-log/`, `pivots.json`,
`sound-levels.json` (absolute paths), `_update-backups/`, `.claude/launch.json` (absolute
path), the stray `"product/` folder at the root, the `#startupmomedit` hashtag, the
`product.json` update and course URLs (they are tied to your purchase and would keep polling).

---

## 6. Rebuild plan: what to build, in what order

### v0: the core (about 15–20% of the original)

Goal: clip in, captioned MP4 or CapCut draft out, in the creator's pack. One format (Yap).

1. **Folder skeleton:** `inbox/`, `projects/<job>/{raw,transcript,outputs,review}`, `assets/fonts`,
   `brand-kit.md`, `_local/`.
2. **CLAUDE.md** (aim for 10–15 KB, not 56): persona, the phase table, the 14 principles above
   as rules, where things live, a phrasebook. Keep the personal block separate and marked.
3. **Transcribe:** one script that builds a uv venv with WhisperX pinned (3.8.6 / torch 2.8.0 /
   ctranslate2 4.8.1) and writes per-word JSON. Cache per job; `--force` to redo.
4. **Cut:** transcript → segments (keep last take, drop filler); a stitch script that snaps
   boundaries to word onsets, closes long pauses, snaps to frames, renders through one ffmpeg
   graph, applies one static gain to −16 LUFS, then re-times kept words into the cut script.
5. **Measure:** OpenCV YuNet face box → head box + open zones JSON; one safe-zones module.
6. **Packs:** one `style-packs.json` (fonts by role, accent, shadow, sizes) + a loader with
   font fallback.
7. **Type builder:** one HyperFrames composition template; hook + captions + one card kind,
   all skinned from the pack; fit-size for the hook; render via `npx hyperframes@<pin>` with
   `check` as a gate and a content-hash cache.
8. **Finish:** ffmpeg composite of base + layers + SFX ducked under voice → MP4. Optional
   CapCut: VectCutAPI (Apache 2.0, fork it yourself from GitHub) with named tracks, quit check,
   never-replace versioning.
9. **Skills (6–8):** set-me-up, rough-cut, graphics-plan, beat-sheet, capcut, learn,
   report-a-problem, style-pack.
10. **Hooks (3):** session nudge (tools present, brand-kit filled), draft protection, chime.
11. **Learned prefs:** allowlisted JSON with clamps + the end-of-reel "teach my style" prompt.

### v1: the review experience
Beat sheet stills; the in-chat style plan table; a lookbook of reusable looks per pack;
sound plan (one cue per graphic arrival); music bed at a measured duck.

### v2: the visual editor
The single biggest cost (~15,000 lines). Only build it if chat-plus-stills review is not enough.
Design: stdlib HTTP server on localhost, one HTML page, four tabs (Cut / Visuals / Sound /
Finish), `POST /save` writes a review JSON the engine re-stitches from, Claude reads
back-channel files (notes, look requests).

### Skip entirely unless needed
Windows/Microsoft Store/Intel Mac shims (~3,000 lines), the signed update system (~2,500
lines), keep-changes three-way merge, Canva/DESIGN.md pack importers, voiceover and b-roll
formats, carousel/story kits, trial reels, face cover, DaVinci bridge.

### Things to do differently
- One review road, not two (the widget road is legacy; the editor supersedes it).
- A proper `pyproject.toml` + `uv.lock` instead of inline script headers and a bash-built venv.
- Pytest with a `conftest.py` from day one; the original has 237 ad-hoc scripts.
- Keep CLAUDE.md short and push rules into the skills that need them; 56 KB is read every turn.
- Write the persona for the actual person (the original is written to "she", a mom creator).

---

## 7. Dependencies and pins (as found)

| Dependency | Version / note |
|---|---|
| ffmpeg / ffprobe | any recent; videotoolbox on Mac |
| Python | 3.11 preferred, via uv |
| WhisperX | 3.8.6, torch 2.8.0, torchaudio 2.8.0, ctranslate2 4.8.1, pyannote.audio 4.0.7, model large-v3 + wav2vec2 aligners |
| faster-whisper | fallback / verify pass (base or small) |
| Node + npx | HyperFrames 0.8.181, `browser ensure` once for headless Chromium; GSAP vendored |
| OpenCV headless + numpy | YuNet face model for subject zones |
| Pillow | text measurement, stills |
| VectCutAPI | fork of sun-guannan/VectCutAPI (Apache 2.0): flask, requests, json5, imageio, psutil |
| CapCut desktop | 9.1.0+, opened once so the projects folder exists |
| Fonts | Inter, Instrument Serif, Playfair, Poppins, Bloop (pack-dependent); OFL ones bundled |
| SFX | ~43 CC0 mp3s + an index JSON (file, material, mood, description) |

No telemetry, no licence check, no machine binding exists in the code. The only outbound calls
are the update feed (once a day), the course guide and an optional logo fetch.

---

## 8. Open question for you

Which of these is the team member? It changes what gets built:

- **An editor for @ohheymattheus:** port the personal layer as-is (section 5), one brand kit,
  same packs, same house rules. The engine is a shared standard.
- **Their own creator:** generic engine only, their own brand kit interview, their own packs.
  House style rules become examples, not defaults.

And the cheaper path is still a second licence plus the personal layer copied over.
