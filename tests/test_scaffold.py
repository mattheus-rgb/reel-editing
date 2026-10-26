"""Smoke tests for the scaffold itself; real pipeline tests arrive with each script."""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_safe_zones_scale():
    out = subprocess.run([sys.executable, ROOT / "engine/measure/safe_zones.py", "540", "960"], capture_output=True, text=True, check=True)
    b = json.loads(out.stdout)
    assert b["top"] == 135 and b["bottom"] == 960 - 150

def test_neutral_pack_roles():
    sys.path.insert(0, str(ROOT))
    from engine.packs.load import role
    for r in ("hook", "caption", "takeover", "aside"):
        assert role("Neutral", r)["size"] > 0

def test_prefs_allowlist():
    sys.path.insert(0, str(ROOT))
    from engine.learn import prefs
    assert prefs.get("caption.zone") == "under_chin"
    assert prefs._coerce("music.duck_db", "-30") == -18.0

def test_every_skill_has_frontmatter():
    for s in (ROOT / ".claude/skills").iterdir():
        text = (s / "SKILL.md").read_text()
        assert text.startswith("---\nname: " + s.name), s.name

def test_brand_kit_blanks_counted():
    assert (ROOT / "brand-kit.md").read_text().count("{{") >= 20
