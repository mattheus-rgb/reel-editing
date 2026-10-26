"""The platform UI bands. Everything that matters sits between them. Nothing else defines a band."""
CANVAS_W, CANVAS_H = 1080, 1920
TOP = 270      # px: reel UI (handle, audio) on a 1080x1920 canvas
BOTTOM = 300   # px: caption, like/share rail
MIN_CAPTION_PX = 44  # captions never shrink below this

def bands(w: int = CANVAS_W, h: int = CANVAS_H) -> dict:
    s = h / CANVAS_H
    top, bottom = round(TOP * s), round(BOTTOM * s)
    return {"canvas": {"w": w, "h": h}, "top": top, "bottom": h - bottom,
            "safe": {"y0": top, "y1": h - bottom, "x0": round(0.06 * w), "x1": round(0.94 * w)}}

if __name__ == "__main__":
    import json, sys
    w, h = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (CANVAS_W, CANVAS_H)
    print(json.dumps(bands(w, h), indent=2))
