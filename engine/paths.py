"""Two roots, kept apart so the engine can be installed once (as a plugin) and used in many folders.

CODE: where the engine's own files live (this package, its templates, shipped packs, fonts).
WORK: the designer's workspace, which holds brands/, inbox/ and _local/.

WORK resolution: $REELS_WORKSPACE if set; else the nearest folder at or above the current directory
that has a brands/ folder; else the current directory (a fresh workspace is made there on demand).
"""
import os
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]

def _find_work() -> Path:
    env = os.environ.get("REELS_WORKSPACE")
    if env:
        return Path(env).expanduser().resolve()
    here = Path.cwd().resolve()
    for p in (here, *here.parents):
        if (p / "brands").is_dir():
            return p
    return here

WORK = _find_work()

def ensure_workspace(path: Path | None = None) -> Path:
    """Make a workspace usable: brands/_agency, brands/_template, inbox/, _local/, a CLAUDE.md."""
    import shutil
    w = (path or WORK)
    (w / "inbox").mkdir(parents=True, exist_ok=True)
    (w / "_local").mkdir(exist_ok=True)
    tpl = CODE / "templates" / "workspace"
    for name in ("brands", "CLAUDE.md", ".gitignore", "README.md"):
        src, dst = tpl / name, w / name
        if dst.exists(): continue
        if src.is_dir(): shutil.copytree(src, dst)
        elif src.exists(): shutil.copy2(src, dst)
    return w
