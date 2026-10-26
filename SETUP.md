# Setting up the engine

Open this folder in Claude Code and say **"set me up"**. Claude runs the checker, installs what it
flags (it asks before each install), builds the speech tools, fetches the render browser, then offers
the brand-kit interview. This page is the same road for when you want to see it written out.

## Tools, and the one job each does

| Tool | Job | Install (Mac) |
|---|---|---|
| Homebrew | installs the rest | the one step you type yourself: see brew.sh |
| ffmpeg | cuts, joins, levels, writes every video file | `brew install ffmpeg` |
| uv | builds the Python toolbelt and the speech tools | `brew install uv` |
| Node | runs the graphics renderer | `brew install node` |

Then:

```bash
./check-setup.sh            # reports only
uv sync                     # the toolbelt
uv sync --extra speech      # the speech tools (slow the first time)
npm install                 # the renderer, pinned
npx hyperframes browser ensure
```

## Where the folder lives

Keep it out of iCloud Drive. A plain `~/projects/` folder is right.

## Then

Say **"build my homebase"** and answer the interview. It fills `brand-kit.md`, the one file that is yours.
