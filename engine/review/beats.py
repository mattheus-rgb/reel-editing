#!/usr/bin/env python3
"""Numbered stills of every planned beat with a legend. --cut-only for the rough cut.

Reads:   plans/graphics.json (or cuts.json) + outputs/<job>.mp4
Writes:  beat-sheet/sheet.jpg + beat-sheet/beats.json
Done when: one still per beat, legend: number, time, element, words, motion; readable on a phone.

Contract: runs as `uv run engine/review/beats.py <job> [flags]`, touches only brands/<brand>/projects/<job>/, prints one line
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
