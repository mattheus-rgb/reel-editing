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

def test_brand_template_blanks_counted():
    assert (ROOT / "brands/_template/brand-kit.md").read_text().count("{{") >= 20

def test_brand_resolution_order(tmp_path=None):
    import shutil
    sys.path.insert(0, str(ROOT))
    from engine import brand
    from engine.learn import prefs
    name = "zz-test-brand"
    if (brand.BRANDS / name).exists(): shutil.rmtree(brand.BRANDS / name)
    brand.new(name); brand.use(name)
    try:
        assert prefs.get("sfx.density", name) == "light"          # engine default
        prefs.add("sfx.density", "full", "t", brand="_agency")    # agency layer
        assert prefs.get("sfx.density", name) == "full"
        prefs.add("sfx.density", "none", "t", brand=name)         # brand wins
        assert prefs.get("sfx.density", name) == "none"
        assert brand.job_dir(f"{name}/x", create=True).parent == brand.paths(name)["projects"]
    finally:
        shutil.rmtree(brand.BRANDS / name)
        prefs.forget(1, brand="_agency")
        brand.ACTIVE.unlink(missing_ok=True)
