# Installing the reel-editing plugin

The plugin is this folder. It carries the engine's skills, hooks and Python toolbelt. Each designer
also gets a **workspace**: any folder they open in Claude Code, where their clients' brands, inbox and
reels live. The plugin makes the workspace on first use.

## For the organisation (one of three ways)

**A. From GitHub (recommended).** Everyone adds the marketplace once, then installs:

```bash
claude plugin marketplace add mattheus-rgb/reel-editing
claude plugin install reel-editing@reel-editing --scope user
```

Pin a version with `mattheus-rgb/reel-editing#v0.3.0`.

**B. From the ZIP.** Unzip it somewhere stable (not a Downloads folder), then:

```bash
claude plugin marketplace add /path/to/reel-editing
claude plugin install reel-editing@reel-editing --scope user
```

**C. Pre-enabled for everyone** through managed settings (the admin console, MDM, or
`managed-settings.json`):

```json
{
  "extraKnownMarketplaces": {
    "reel-editing": { "source": { "source": "github", "repo": "mattheus-rgb/reel-editing" } }
  },
  "enabledPlugins": { "reel-editing@reel-editing": true }
}
```

To try it for one session without installing: `claude --plugin-dir /path/to/reel-editing`.

## For each designer, after the plugin is installed

1. Make a folder for your clients (for example `~/reels/`), open it in Claude Code.
2. Say **"set me up"**. It installs ffmpeg, uv and Node if missing (Homebrew is the one step you type
   yourself), builds the toolbelt inside the plugin, and turns this folder into a workspace:
   `brands/`, `inbox/`, `_local/`, and a `CLAUDE.md` carrying the engine's rules.
3. Say **"open my studio"**. Add your first client there, then "build the homebase for <client>".
4. Drop the client's clip in `inbox/` and say **"edit this reel"**.

Skills are namespaced: `/reel-editing:studio`, `/reel-editing:learn`, `/reel-editing:report-a-problem`.
Plain phrases ("open my studio", "edit this reel") work without the prefix.

## What the plugin needs on the machine

Mac (Apple Silicon). ffmpeg, uv, Node 18+, Python 3.11 via uv, CapCut desktop for the CapCut route.
Nothing leaves the machine; the Studio binds 127.0.0.1 only.

## Updating

```bash
claude plugin marketplace update reel-editing
claude plugin update reel-editing@reel-editing
```

Workspaces are untouched by updates: brands, inbox and reels live in the designer's folder, not in
the plugin.
