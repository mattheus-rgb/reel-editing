#!/usr/bin/env python3
"""Resolve a pack role to real values. A build with no resolvable pack fails loud.

    from engine.packs.load import role
    role("Neutral", "hook") -> {"font_file": Path, "size": 72, "case": ..., "color": ..., "shadow": ...}

Lookup order: engine/packs/user-packs.json (theirs) then engine/packs/packs.json (shipped).
A missing font file falls back to the pack's headline font with ONE warning line, never silently.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def _packs() -> dict:
    merged = {}
    for name in ("packs.json", "user-packs.json"):
        p = HERE / name
        if p.exists():
            merged.update(json.loads(p.read_text()).get("packs", {}))
    return merged

def pack(name: str) -> dict:
    packs = _packs()
    if name not in packs:
        sys.exit(f"no style pack named {name!r}; known: {', '.join(sorted(packs))}")
    return packs[name]

def role(pack_name: str, role_name: str) -> dict:
    p = pack(pack_name)
    r = p["roles"].get(role_name)
    if r is None:
        sys.exit(f"pack {pack_name!r} has no role {role_name!r}")
    font_dir = ROOT / json.loads((HERE / "packs.json").read_text()).get("font_dir", "assets/fonts")
    font_file = font_dir / p["fonts"][r["font"]]
    if not font_file.exists():
        fallback = font_dir / p["fonts"]["headline"]
        print(f"warning: font {font_file.name} not in {font_dir}; using {fallback.name}", file=sys.stderr)
        font_file = fallback
    return {**r, "font_file": font_file, "color": p["colors"]["light"],
            "accent": p["colors"]["accent"], "shadow": p["shadow"], "motion": p["motion"].get(role_name)}

if __name__ == "__main__":
    name, rn = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("Neutral", "hook")
    out = role(name, rn); out["font_file"] = str(out["font_file"])
    print(json.dumps(out, indent=2))
