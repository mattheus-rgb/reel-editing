#!/usr/bin/env python3
"""Run the renderer's own check on a composition. A failure is a warning line unless --strict.

Reads:   layers/<name>/
Writes:  stdout; exit 0 either way unless --strict
Done when: an animation aimed at nothing or text past the edge is named in one line and the render proceeds.

Contract: runs as `uv run engine/render/gate.py <job> [flags]`, touches only brands/<brand>/projects/<job>/, prints one line
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
