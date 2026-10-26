#!/usr/bin/env python3
"""Make a pack from a parent plus overrides. Never touches an existing pack without --force.

Reads:   --name X --from Neutral --set colors.accent=#... --set roles.hook.font=...
Writes:  engine/packs/user-packs.json (theirs, gitignored)
Done when: a derived pack loads by role; the parent is byte-identical afterwards.

Contract: runs as `uv run engine/packs/write.py <job> [flags]`, touches only projects/<job>/, prints one line
per thing it did, never asks a question (Claude asks). Exit 0 on success, 1 on a real failure,
and a warning line (never an exit) for a check that merely flagged something.
"""
import argparse, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def job_dir(job: str) -> Path:
    d = ROOT / "projects" / job
    if not d.is_dir():
        sys.exit(f"no such job: {job} (expected {d})")
    return d

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("job")
    ap.add_argument("--force", action="store_true", help="redo even if cached")
    args = ap.parse_args()
    job_dir(args.job)
    print(f"[{Path(__file__).stem}] not built yet. Contract is in this file's docstring.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
