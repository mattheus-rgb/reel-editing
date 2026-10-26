# Composition template

One HyperFrames composition per layer. `build.py` copies this folder to `projects/<job>/layers/<name>/`
and fills the tokens: `__TEXT__`, `__FONT__`, `__SIZE__`, `__COLOR__`, `__SHADOW__`, `__Y__`, `__DUR__`.
Keep it a transparent 1080x1920 canvas; the base footage is composited underneath later.
