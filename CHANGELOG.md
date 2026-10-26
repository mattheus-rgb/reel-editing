# Changelog

## v0.3.0 — 2026-10-26

- Installable as a Claude Code plugin (`.claude-plugin/plugin.json`, `skills/`, `hooks/hooks.json`,
  a marketplace file) from GitHub, a ZIP, or managed settings for the whole organisation.
- The engine's code and a designer's workspace are separate folders: brands, inbox and reels live in
  whatever folder they open; the Studio makes it a workspace on first run, with the rules as its CLAUDE.md.
- `build-zip.sh` builds the distributable ZIP; `INSTALL.md` has the three install routes.

## v0.2.0 — 2026-10-26

- The Studio is minimalist and follows the system's light or dark setting.
- A Files tab lists everything the Studio can reach inside the folder: inbox clips, each reel's
  footage, cuts, plans, layers and finals, each brand's kit, packs and fonts; filter by kind, open any.

## v0.1.2 — 2026-10-26

- A brand added on the Studio page is committed to git at once (its kit and packs; footage and fonts
  stay out). The page says so, or says why not.
- Pressing Enter in the new-client box adds once, not twice.
- Every page action explains itself when the Studio server is not running.

## v0.1.1 — 2026-10-26

- The Studio has a How to tab: the road, what to say, how brands resolve, the stage bar, the rules,
  and what to do when something goes wrong. The page says so plainly when its server is not running.

## v0.1.0 — 2026-10-26

The multi-brand scaffold, with a Studio page.

- One engine, one folder per client under `brands/`; settings resolve brand → agency → default.
- The Studio: a local page listing every client and reel, with brand switching, new clients,
  folder opening and notes for Claude.
- Rules, nine skills, the brand-kit template, three hooks, safe zones, the Neutral pack loader and
  bounded learned preferences are real; the pipeline scripts are stubs carrying their contracts.
