#!/usr/bin/env python3
"""The Studio: a local page where the editor sees every client brand and every reel, switches the
active brand, starts a new one, and opens folders. Nothing leaves the machine.

    uv run engine/studio/server.py open     # start if needed, print the link, open the browser
    uv run engine/studio/server.py serve    # run in the foreground (used by .claude/launch.json)
    uv run engine/studio/server.py state    # the JSON the page shows
    uv run engine/studio/server.py stop

Binds 127.0.0.1 only. Port: STUDIO_PORT, else 48150, else a free one; written to _local/studio.json.
POSTs are accepted only from the page itself (Origin must match).
"""
import json, os, re, signal, socket, subprocess, sys, time, webbrowser
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engine import brand as B

HERE = Path(__file__).resolve().parent
STATE = ROOT / "_local" / "studio.json"
SAFE = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}$")

# The stages a job passes through, and the file that proves each one happened.
STAGES = [
    ("footage", "raw"),
    ("words", "transcript/words.json"),
    ("cut", "outputs/{job}.mp4"),
    ("plan", "plans/graphics.json"),
    ("layers", "layers"),
    ("final", "outputs/{job}.final.mp4"),
]

def _kit_blanks(kit: Path) -> int:
    return kit.read_text().count("{{") if kit.exists() else -1

def _kit_field(kit: Path, label: str) -> str:
    if not kit.exists(): return ""
    m = re.search(rf"^- {re.escape(label)}:\s*(.+?)\s*(?:\(.*\))?\s*$", kit.read_text(), re.M)
    v = m.group(1).strip() if m else ""
    return "" if v.startswith("{{") else v

def _jobs(brand: str) -> list[dict]:
    out = []
    pdir = B.paths(brand)["projects"]
    if not pdir.is_dir(): return out
    for j in sorted(pdir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if not j.is_dir() or j.name.startswith("."): continue
        stages = []
        for name, rel in STAGES:
            p = j / rel.format(job=j.name)
            stages.append({"name": name, "done": p.exists() and (not p.is_dir() or any(p.iterdir()))})
        done = [s["name"] for s in stages if s["done"]]
        intent = (j / "intent.md")
        out.append({"name": j.name, "stage": done[-1] if done else "new", "stages": stages,
                    "intent": intent.read_text().strip().splitlines()[0][:120] if intent.exists() else "",
                    "updated": int(j.stat().st_mtime), "path": str(j)})
    return out

MEDIA = {".mov", ".mp4", ".m4v", ".wav", ".mp3", ".m4a", ".jpg", ".jpeg", ".png", ".gif"}
TEXTY = {".json", ".md", ".ttf", ".otf"}

def _entry(path: Path, where: str, brand: str = "", job: str = "") -> dict:
    st = path.stat()
    return {"name": path.name, "where": where, "brand": brand, "job": job,
            "kind": "video" if path.suffix.lower() in (".mov", ".mp4", ".m4v") else
                    "audio" if path.suffix.lower() in (".wav", ".mp3", ".m4a") else
                    "image" if path.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif") else
                    "font" if path.suffix.lower() in (".ttf", ".otf") else "file",
            "size": st.st_size, "updated": int(st.st_mtime), "path": str(path),
            "rel": str(path.relative_to(ROOT))}

def files() -> dict:
    """Every file the Studio can reach: inbox clips, each reel's footage, cuts, plans, layers and
    finals, and each brand's kit, packs and fonts. Nothing outside this folder."""
    out = []
    inbox = ROOT / "inbox"
    if inbox.is_dir():
        for f in sorted(inbox.iterdir(), key=lambda p: p.name.lower()):
            if f.is_file() and not f.name.startswith(".") and f.suffix.lower() in MEDIA:
                out.append(_entry(f, "inbox"))
    for brand in ["_agency"] + B.list_brands():
        bp = B.paths(brand)
        for name in ("brand-kit.md", "packs.json", "learned.json"):
            if (bp["root"] / name).exists(): out.append(_entry(bp["root"] / name, "brand", brand))
        if bp["fonts"].is_dir():
            for f in sorted(bp["fonts"].iterdir()):
                if f.is_file() and f.suffix.lower() in TEXTY: out.append(_entry(f, "fonts", brand))
        if not bp["projects"].is_dir(): continue
        for j in sorted(bp["projects"].iterdir()):
            if not j.is_dir() or j.name.startswith("."): continue
            for sub, label in (("raw", "footage"), ("outputs", "outputs"), ("layers", "layers"),
                               ("beat-sheet", "beat sheet"), ("plans", "plans"), ("transcript", "transcript")):
                d = j / sub
                if not d.is_dir(): continue
                for f in sorted(d.rglob("*")):
                    if f.is_file() and not f.name.startswith(".") and f.suffix.lower() in MEDIA | TEXTY:
                        out.append(_entry(f, label, brand, j.name))
            if (j / "intent.md").exists(): out.append(_entry(j / "intent.md", "plans", brand, j.name))
    return {"files": out, "root": str(ROOT), "count": len(out), "bytes": sum(f["size"] for f in out)}

def state() -> dict:
    active = B.current(strict=False)
    brands = []
    for name in ["_agency"] + B.list_brands():
        p = B.paths(name)
        kit = p["kit"]
        fonts = [f.name for f in p["fonts"].iterdir()] if p["fonts"].is_dir() else []
        packs = []
        if p["packs"].exists():
            try: packs = list(json.loads(p["packs"].read_text()).get("packs", {}))
            except json.JSONDecodeError: packs = ["(packs.json unreadable)"]
        learned = json.loads(p["learned"].read_text()) if p["learned"].exists() else []
        jobs = _jobs(name) if name != "_agency" else []
        brands.append({
            "name": name, "agency": name == "_agency", "active": name == active,
            "display": _kit_field(kit, "Name") or name,
            "what": _kit_field(kit, "One line on what you do"),
            "register": _kit_field(kit, "Usual register"),
            "pack": _kit_field(kit, "Style pack") or ("Neutral" if not packs else packs[0]),
            "kit_blanks": _kit_blanks(kit), "packs": packs, "fonts": fonts,
            "learned": len(learned), "jobs": jobs, "path": str(p["root"]),
        })
    inbox = sorted((f.name for f in (ROOT / "inbox").iterdir()
                    if f.is_file() and f.suffix.lower() in (".mov", ".mp4", ".m4v")), key=str.lower) if (ROOT / "inbox").is_dir() else []
    return {"active": active, "brands": brands, "inbox": inbox, "root": str(ROOT), "time": int(time.time())}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = (HERE / "studio.html").read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
        elif self.path == "/api/state":
            self._json(state())
        elif self.path == "/api/files":
            self._json(files())
        elif self.path == "/ping":
            self._json({"ok": True})
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        origin = self.headers.get("Origin", "")
        host = self.headers.get("Host", "")
        if origin and origin != f"http://{host}":
            return self._json({"error": "refused"}, 403)
        n = int(self.headers.get("Content-Length", 0) or 0)
        data = json.loads(self.rfile.read(n) or b"{}")
        try:
            if self.path == "/api/use":
                b = data.get("brand", "")
                if b == "_agency" or not (B.BRANDS / b).is_dir(): raise ValueError("no such brand")
                B.ACTIVE.parent.mkdir(exist_ok=True); B.ACTIVE.write_text(b + "\n")
            elif self.path == "/api/new":
                b = data.get("brand", "").strip().lower().replace(" ", "-")
                if not SAFE.match(b) or b.startswith("_"): raise ValueError("name: letters, digits and dashes")
                if (B.BRANDS / b).exists(): raise ValueError("that brand exists")
                import shutil
                shutil.copytree(B.BRANDS / "_template", B.BRANDS / b)
                (B.BRANDS / b / "projects").mkdir(exist_ok=True); (B.BRANDS / b / "fonts").mkdir(exist_ok=True)
                B.ACTIVE.parent.mkdir(exist_ok=True); B.ACTIVE.write_text(b + "\n")
                note = _commit(f"brands/{b}", f"Add brand {b}")
                return self._json({"ok": True, "note": note, "state": state()})
            elif self.path == "/api/open":
                p = Path(data.get("path", "")).resolve()
                if ROOT not in p.parents and p != ROOT: raise ValueError("outside the engine")
                if sys.platform == "darwin": subprocess.Popen(["open", str(p)])
            elif self.path == "/api/say":
                # The page asks Claude for something: queued for the chat to read with `studio say`.
                q = ROOT / "_local" / "studio-says.json"
                items = json.loads(q.read_text()) if q.exists() else []
                items.append({"t": int(time.time()), "text": str(data.get("text", ""))[:500]}); q.write_text(json.dumps(items))
            else:
                return self._json({"error": "not found"}, 404)
            self._json({"ok": True, "state": state()})
        except Exception as e:  # the page shows the reason
            self._json({"error": str(e)}, 400)

def _commit(rel: str, message: str) -> str:
    """Commit one brand folder's tracked files (kit, packs). Footage and fonts stay ignored."""
    if not (ROOT / ".git").exists():
        return "not committed: this folder is not a git repository"
    try:
        subprocess.run(["git", "add", rel], cwd=ROOT, check=True, capture_output=True)
        r = subprocess.run(["git", "commit", "-q", "-m", message], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            return "not committed: " + (r.stderr or r.stdout).strip().splitlines()[-1][:120]
        return f"committed as \"{message}\" (push when you are ready: git push)"
    except Exception as e:
        return f"not committed: {e}"

def _port() -> int:
    if os.environ.get("STUDIO_PORT"): return int(os.environ["STUDIO_PORT"])
    for p in (48150,):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", p)) != 0: return p
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0)); return s.getsockname()[1]

def _running() -> int | None:
    if not STATE.exists(): return None
    try:
        info = json.loads(STATE.read_text())
        with socket.create_connection(("127.0.0.1", info["port"]), timeout=0.5):
            return info["port"]
    except Exception:
        return None

def serve() -> None:
    port = _port()
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps({"port": port, "pid": os.getpid()}))
    print(f"STUDIO LINK: http://127.0.0.1:{port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()

def open_() -> None:
    port = _running()
    if port is None:
        subprocess.Popen([sys.executable, __file__, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        for _ in range(40):
            time.sleep(0.1); port = _running()
            if port: break
    if port is None: sys.exit("the studio did not start; run: uv run engine/studio/server.py serve")
    url = f"http://127.0.0.1:{port}/"
    print(f"STUDIO LINK: {url}")
    try: webbrowser.open(url)
    except Exception: pass

def stop() -> None:
    if STATE.exists():
        try: os.kill(json.loads(STATE.read_text())["pid"], signal.SIGTERM); print("stopped")
        except Exception: print("not running")
        STATE.unlink(missing_ok=True)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "open"
    if cmd == "serve": serve()
    elif cmd == "open": open_()
    elif cmd == "state": print(json.dumps(state(), indent=2))
    elif cmd == "files": print(json.dumps(files(), indent=2))
    elif cmd == "stop": stop()
    elif cmd == "say":
        q = ROOT / "_local" / "studio-says.json"
        print(q.read_text() if q.exists() else "[]"); q.unlink(missing_ok=True)
    else: sys.exit(__doc__)
