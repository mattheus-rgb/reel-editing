#!/usr/bin/env python3
"""Which brand a job belongs to, and where its files are.

    uv run engine/brand.py list
    uv run engine/brand.py use acme-coffee        # sets _local/active-brand
    uv run engine/brand.py current
    uv run engine/brand.py new acme-coffee        # copies brands/_template

Library:
    from engine.brand import current, paths, job_dir
    paths("acme-coffee") -> {"root", "kit", "packs", "learned", "fonts", "projects"}
    job_dir("the-pricing-one")            # under the active brand
    job_dir("acme-coffee/the-pricing-one") # explicit

Resolution for settings is brand -> _agency -> engine default; callers use `chain(brand)` to get
the folders to look in, in that order.
"""
import shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.paths import CODE, WORK
ROOT = WORK
BRANDS = WORK / "brands"
ACTIVE = WORK / "_local" / "active-brand"
TEMPLATE = CODE / "templates" / "workspace" / "brands" / "_template"
RESERVED = {"_agency", "_template"}

def list_brands() -> list[str]:
    if not BRANDS.is_dir(): return []
    return sorted(p.name for p in BRANDS.iterdir() if p.is_dir() and p.name not in RESERVED)

def current(strict: bool = True) -> str | None:
    """The active brand. With strict=False, None when there is none (lookups then use _agency only)."""
    if ACTIVE.exists():
        b = ACTIVE.read_text().strip()
        if (BRANDS / b).is_dir():
            return b
    brands = list_brands()
    if len(brands) == 1:
        return brands[0]
    if not strict:
        return None
    sys.exit("no active brand. Say 'switch to <brand>' (uv run engine/brand.py use <brand>). "
             f"Known: {', '.join(brands) or 'none; make one with: new <brand>'}")

def use(brand: str) -> None:
    if not (BRANDS / brand).is_dir() or brand in RESERVED:
        sys.exit(f"no brand folder brands/{brand}")
    ACTIVE.parent.mkdir(exist_ok=True); ACTIVE.write_text(brand + "\n")
    print(f"active brand: {brand}")

def new(brand: str) -> None:
    dest = BRANDS / brand
    if dest.exists():
        sys.exit(f"brands/{brand} already exists")
    src = BRANDS / "_template" if (BRANDS / "_template").is_dir() else TEMPLATE
    shutil.copytree(src, dest)
    (dest / "projects").mkdir(exist_ok=True); (dest / "fonts").mkdir(exist_ok=True)
    print(f"made brands/{brand}; now 'build my homebase' fills its brand-kit.md")

def paths(brand: str) -> dict:
    r = BRANDS / brand
    return {"root": r, "kit": r / "brand-kit.md", "packs": r / "packs.json",
            "learned": r / "learned.json", "fonts": r / "fonts", "projects": r / "projects"}

def chain(brand: str | None = None) -> list[dict]:
    """The folders to consult, most specific first: the brand, then _agency."""
    b = brand or current(strict=False)
    return ([paths(b)] if b else []) + [paths("_agency")]

def split_job(job: str) -> tuple[str, str]:
    if "/" in job:
        b, j = job.split("/", 1); return b, j
    return current(), job

def job_dir(job: str, create: bool = False) -> Path:
    b, j = split_job(job)
    d = paths(b)["projects"] / j
    if create:
        d.mkdir(parents=True, exist_ok=True)
    elif not d.is_dir():
        sys.exit(f"no such job: {j} in brand {b} (expected {d})")
    return d

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "list":
        cur = ACTIVE.read_text().strip() if ACTIVE.exists() else ""
        for b in list_brands(): print(("* " if b == cur else "  ") + b)
    elif a[0] == "current": print(current())
    elif a[0] == "use": use(a[1])
    elif a[0] == "new": new(a[1])
    else: sys.exit(__doc__)
