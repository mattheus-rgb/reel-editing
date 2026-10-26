#!/usr/bin/env python3
"""(v1) Write an editable CapCut draft: main track per kept line, each layer its own named track, each cue its own clip.

Reads:   outputs/<job>.mp4 + layers/*.mov + plans/sound.json
Writes:  a new draft version in CapCut's projects folder
Done when: every element is its own clip on its own track; nothing compounded; CapCut was quit for the write.

Contract: runs as `uv run engine/capcut/draft.py <job> [flags]`, touches only brands/<brand>/projects/<job>/, prints one line
per thing it did, never asks a question (Claude asks). Exit 0 on success, 1 on a real failure,
and a warning line (never an exit) for a check that merely flagged something.
"""
import argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
from engine.brand import job_dir  # jobs live under brands/<brand>/projects/<job>

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("job", help="<job> under the active brand, or <brand>/<job>")
    ap.add_argument("--force", action="store_true", help="redo even if cached")
    args = ap.parse_args()
    job_dir(args.job)
    print(f"[{Path(__file__).stem}] not built yet. Contract is in this file's docstring.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
