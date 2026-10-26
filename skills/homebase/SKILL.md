---
name: homebase
description: Fills a client brand's kit from its brief. Use when they say "build the homebase for <brand>", "set up <brand>'s brand kit", "new brand <name>", "redo <brand>'s kit", "homebase", or when the active brand's brand-kit.md still has blanks and they agree to fill it.
---

# Homebase

Fills `brands/<brand>/brand-kit.md` for one client, one part at a time. The client's words go in
(from their brief, site, past posts or the editor's notes), never invented ones.

0. No folder yet: `uv run "${CLAUDE_PLUGIN_ROOT:-.}"/engine/brand.py new <brand>`, then `brand.py use <brand>`.
1. Read the brand's `brand-kit.md`. Only ask about fields still blank (`{{...}}`). If the editor has a
   client brief or brand guide, read it first and propose answers for approval rather than asking.
2. **Part A** (who): name, pronouns, handles, what they do, who for, what those people are stuck on.
   One question box per part, not per field.
3. **Part B** (sound): tone words, a line they would say, one they never would, spelling,
   contractions, banned words, punctuation, usual register, how a reel ends. The client's voice, not
   the editor's.
4. **Part C** (look): offer Neutral as the pack to start; accent colour; captions under chin or above
   head; camera; sound density; music.
5. **Part D**: words the transcriber will get wrong (the speaker's name, the brand, product names).
6. Write each answer into the kit as given. Then `grep -c '{{' brands/<brand>/brand-kit.md` prints 0.
7. Their licensed fonts go in `brands/<brand>/fonts/`; a pack of their own via `engine/packs/write.py`.
8. Offer one real clip so the editor sees the brand's kit on the client's footage.

Never invent an answer to fill a blank. A field they skip stays blank and the engine uses a default.

**Next:** drop the client's clip in `inbox/` and say "edit this reel" (the brand stays active).
