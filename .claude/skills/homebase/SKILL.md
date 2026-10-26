---
name: homebase
description: The brand-kit interview. Use when they say "build my homebase", "set up my brand kit", "redo my brand kit", "homebase", or when brand-kit.md still has blanks and they agree to fill it.
---

# Homebase

Fills `brand-kit.md` by conversation, one part at a time. Their words go in, not yours.

1. Read `brand-kit.md`. Only ask about fields still blank (`{{...}}`).
2. **Part A** (who): name, pronouns, handles, what they do, who for, what those people are stuck on.
   One question box per part, not per field.
3. **Part B** (sound): tone words, a line they would say, one they never would, spelling,
   contractions, banned words, punctuation, usual register, how a reel ends.
4. **Part C** (look): offer Neutral as the pack to start; accent colour; captions under chin or above
   head; camera; sound density; music.
5. **Part D**: words the transcriber will get wrong (their name, brand names).
6. Write each answer into the kit as given. Then `grep -c '{{' brand-kit.md` should print 0.
7. Offer one real clip so they see their kit on their own footage.

Never invent an answer to fill a blank. A field they skip stays blank and the engine uses a default.

**Next:** drop a clip in `inbox/` and say "edit this reel".
