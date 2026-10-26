---
name: set-me-up
description: First-run setup. Use when they say "set me up", "setup", "first run", "get me set up", "I just downloaded this". Installs the tools for them, builds the toolbelt and the renderer, then offers the brand-kit interview.
---

# Set me up

One warm line, then do the work. Ask before each install; never type their password.

1. `"${CLAUDE_PLUGIN_ROOT:-.}"/check-setup.sh`. It only reports. Read what it flags.
2. **Homebrew missing:** the one step they do themselves. Give them the line from `SETUP.md`, wait.
3. For each missing tool, name its job in one line ("ffmpeg cuts and joins your footage"), get an OK,
   `brew install <tool>`.
4. In the engine folder (`cd "${CLAUDE_PLUGIN_ROOT:-.}"`): `uv sync`, then `uv sync --extra speech`
   (say it takes a few minutes, send them off).
5. There too: `npm install`, then `npx hyperframes browser ensure`.
6. `"${CLAUDE_PLUGIN_ROOT:-.}"/check-setup.sh` again until it passes.
6b. Make this folder the workspace: `uv run "${CLAUDE_PLUGIN_ROOT:-.}"/engine/studio/server.py open`
   creates `brands/`, `inbox/` and `_local/` here on first run and prints the Studio link.
7. Fill `brands/_agency/brand-kit.md` with the house defaults (the `homebase` skill on `_agency`),
   then make the first client: "new brand <name>" and its homebase.

**Next:** "new brand <name>", then drop a clip in `inbox/` and say "edit this reel".
