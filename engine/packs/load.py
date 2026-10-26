#!/usr/bin/env python3
"""Resolve a pack role to real values. A build with no resolvable pack fails loud.

    from engine.packs.load import role
    role("Neutral", "hook") -> {"font_file": Path, "size": 72, "case": ..., "color": ..., "shadow": ...}

Lookup order: brands/<brand>/packs.json, then brands/_agency/packs.json, then the shipped
engine/packs/packs.json. Fonts: the brand's fonts/, then _agency's, then assets/fonts.
A missing font file falls back to the pack's headline font with ONE warning line, never silently.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from engine.brand import chain

def _packs(brand: str | None = None) -> dict:
    merged = json.loads((HERE / "packs.json").read_text()).get("packs", {})
    for layer in reversed(chain(brand)):          # _agency first, then the brand overrides
        p = layer["packs"]
        if p.exists():
            merged.update(json.loads(p.read_text()).get("packs", {}))
    return merged

def _font_dirs(brand: str | None = None) -> list[Path]:
    return [l["fonts"] for l in chain(brand)] + [ROOT / "assets" / "fonts"]

def pack(name: str, brand: str | None = None) -> dict:
    packs = _packs(brand)
    if name not in packs:
        sys.exit(f"no style pack named {name!r}; known: {', '.join(sorted(packs))}")
    return packs[name]

def _find_font(name: str, brand: str | None) -> Path | None:
    for d in _font_dirs(brand):
        if (d / name).exists():
            return d / name
    return None

def role(pack_name: str, role_name: str, brand: str | None = None) -> dict:
    p = pack(pack_name, brand)
    r = p["roles"].get(role_name)
    if r is None:
        sys.exit(f"pack {pack_name!r} has no role {role_name!r}")
    want = p["fonts"][r["font"]]
    font_file = _find_font(want, brand)
    if font_file is None:
        fallback = p["fonts"]["headline"]
        print(f"warning: font {want} not found in any fonts folder; using {fallback}", file=sys.stderr)
        font_file = _find_font(fallback, brand) or (ROOT / "assets" / "fonts" / fallback)
    return {**r, "font_file": font_file, "color": p["colors"]["light"],
            "accent": p["colors"]["accent"], "shadow": p["shadow"], "motion": p["motion"].get(role_name)}

if __name__ == "__main__":
    a = sys.argv[1:]
    name, rn = (a[0], a[1]) if len(a) > 1 else ("Neutral", "hook")
    brand = a[2] if len(a) > 2 else None
    out = role(name, rn, brand); out["font_file"] = str(out["font_file"])
    print(json.dumps(out, indent=2))
