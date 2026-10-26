#!/usr/bin/env python3
"""Learned preferences: an allowlist with bounds. Builds call get(); the learn skill calls add/forget.

    uv run engine/learn/prefs.py fields
    uv run engine/learn/prefs.py add caption.zone above --note "captions above my head"
    uv run engine/learn/prefs.py list | forget N | get caption.zone

Each entry is written twice: _local/learned.json (what builds read) and a bullet in brand-kit.md
Part E (what they read). Never learnable: register, hook copy, pixel placements.
"""
import json, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / "_local" / "learned.json"
KIT = ROOT / "brand-kit.md"

FIELDS = {  # field: (kind, allowed or (lo, hi), default)
    "caption.zone":       ("choice", ["under_chin", "above"], "under_chin"),
    "caption.size_scale": ("range", (0.8, 1.4), 1.0),
    "hook.size_scale":    ("range", (0.8, 1.3), 1.0),
    "sfx.density":        ("choice", ["none", "light", "full"], "light"),
    "music.duck_db":      ("range", (-18.0, -8.0), -12.0),
    "camera.push":        ("choice", ["none", "slight", "slow"], "slight"),
}

def _load() -> list:
    return json.loads(STORE.read_text()) if STORE.exists() else []

def _save(items: list) -> None:
    STORE.parent.mkdir(exist_ok=True); STORE.write_text(json.dumps(items, indent=2))

def _coerce(field: str, value: str):
    kind, allowed, _ = FIELDS[field]
    if kind == "choice":
        if value not in allowed: sys.exit(f"{field} must be one of {allowed}")
        return value
    v = float(value); lo, hi = allowed
    return min(max(v, lo), hi)

def get(field: str):
    for it in reversed(_load()):
        if it["field"] == field: return it["value"]
    return FIELDS[field][2]

def add(field: str, value: str, note: str = "") -> None:
    if field not in FIELDS: sys.exit(f"not learnable: {field}. Fields: {', '.join(FIELDS)}")
    items = _load()
    items.append({"n": len(items) + 1, "field": field, "value": _coerce(field, value),
                  "note": note, "date": datetime.date.today().isoformat()})
    _save(items)
    if KIT.exists():
        text = KIT.read_text().rstrip("\n")
        KIT.write_text(f"{text}\n- {items[-1]['n']}. {note or field} ({field} = {items[-1]['value']})\n")
    print(f"learned {field} = {items[-1]['value']}")

def forget(n: int) -> None:
    items = [it for it in _load() if it["n"] != n]; _save(items)
    if KIT.exists():
        KIT.write_text("\n".join(l for l in KIT.read_text().splitlines() if not l.startswith(f"- {n}. ")) + "\n")
    print(f"forgot {n}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "fields": print("\n".join(f"{k}: {v[0]} {v[1]} (default {v[2]})" for k, v in FIELDS.items()))
    elif a[0] == "list": print(json.dumps(_load(), indent=2))
    elif a[0] == "get": print(get(a[1]))
    elif a[0] == "add":
        note = a[a.index("--note") + 1] if "--note" in a else ""
        add(a[1], a[2], note)
    elif a[0] == "forget": forget(int(a[1]))
    else: sys.exit(__doc__)
