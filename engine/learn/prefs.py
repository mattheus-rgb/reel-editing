#!/usr/bin/env python3
"""Learned preferences: an allowlist with bounds. Builds call get(); the learn skill calls add/forget.

    uv run engine/learn/prefs.py fields
    uv run engine/learn/prefs.py add caption.zone above --note "captions above the head" [--brand acme]
    uv run engine/learn/prefs.py list | forget N | get caption.zone

Scoped per brand. Each entry is written twice: brands/<brand>/learned.json (what builds read) and a
bullet in that brand's brand-kit.md Part E (what the client reads). `--brand _agency` teaches every
brand; a brand's own value wins over the agency's. Never learnable: register, hook copy, placements.
"""
import json, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engine.brand import chain, paths

def _store(brand): return paths(brand)["learned"]
def _kit(brand): return paths(brand)["kit"]

FIELDS = {  # field: (kind, allowed or (lo, hi), default)
    "caption.zone":       ("choice", ["under_chin", "above"], "under_chin"),
    "caption.size_scale": ("range", (0.8, 1.4), 1.0),
    "hook.size_scale":    ("range", (0.8, 1.3), 1.0),
    "sfx.density":        ("choice", ["none", "light", "full"], "light"),
    "music.duck_db":      ("range", (-18.0, -8.0), -12.0),
    "camera.push":        ("choice", ["none", "slight", "slow"], "slight"),
}

def _load(brand: str) -> list:
    st = _store(brand)
    return json.loads(st.read_text()) if st.exists() else []

def _save(brand: str, items: list) -> None:
    st = _store(brand); st.parent.mkdir(parents=True, exist_ok=True); st.write_text(json.dumps(items, indent=2))

def _coerce(field: str, value: str):
    kind, allowed, _ = FIELDS[field]
    if kind == "choice":
        if value not in allowed: sys.exit(f"{field} must be one of {allowed}")
        return value
    v = float(value); lo, hi = allowed
    return min(max(v, lo), hi)

def get(field: str, brand: str | None = None):
    for layer in chain(brand):                     # the brand, then _agency
        for it in reversed(_load(layer["root"].name)):
            if it["field"] == field: return it["value"]
    return FIELDS[field][2]

def add(field: str, value: str, note: str = "", brand: str | None = None) -> None:
    if field not in FIELDS: sys.exit(f"not learnable: {field}. Fields: {', '.join(FIELDS)}")
    b = brand or chain()[0]["root"].name
    items = _load(b)
    items.append({"n": len(items) + 1, "field": field, "value": _coerce(field, value),
                  "note": note, "date": datetime.date.today().isoformat()})
    _save(b, items)
    kit = _kit(b)
    if kit.exists():
        text = kit.read_text().rstrip("\n")
        kit.write_text(f"{text}\n- {items[-1]['n']}. {note or field} ({field} = {items[-1]['value']})\n")
    print(f"learned for {b}: {field} = {items[-1]['value']}")

def forget(n: int, brand: str | None = None) -> None:
    b = brand or chain()[0]["root"].name
    items = [it for it in _load(b) if it["n"] != n]; _save(b, items)
    kit = _kit(b)
    if kit.exists():
        kit.write_text("\n".join(l for l in kit.read_text().splitlines() if not l.startswith(f"- {n}. ")) + "\n")
    print(f"forgot {n} for {b}")

if __name__ == "__main__":
    a = sys.argv[1:]
    brand = a[a.index("--brand") + 1] if "--brand" in a else None
    if brand: i = a.index("--brand"); del a[i:i+2]
    if not a or a[0] == "fields": print("\n".join(f"{k}: {v[0]} {v[1]} (default {v[2]})" for k, v in FIELDS.items()))
    elif a[0] == "list": print(json.dumps(_load(brand or chain()[0]["root"].name), indent=2))
    elif a[0] == "get": print(get(a[1], brand))
    elif a[0] == "add":
        note = a[a.index("--note") + 1] if "--note" in a else ""
        add(a[1], a[2], note, brand)
    elif a[0] == "forget": forget(int(a[1]), brand)
    else: sys.exit(__doc__)
