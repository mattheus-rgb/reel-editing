---
name: learn
description: Teach the engine something that carries to the next reel. Use when they say "remember that", "from now on", "always do it like that", "learn my pattern", "make this my default", "/learn", "/learn list", "/learn forget N", or at the end of every reel when teach.py has notes.
user-invocable: true
argument-hint: "[list | forget N | <what to remember>]"
---

# Learn

Two halves, always both: the record the builds apply, and the bullet in the brand's kit.
Scope first: "for this brand" (default, the active brand) or "for every brand" (`--brand _agency`).

- **Add:** map their words to an allowlisted field (`uv run engine/learn/prefs.py fields`): caption
  zone or size, hook size, SFX density, music duck, camera push. `uv run engine/learn/prefs.py add
  <field> <value> --note "<their words>" [--brand _agency]` writes `brands/<brand>/learned.json`
  AND a bullet in that brand's `brand-kit.md` Part E. If no field fits, say so and offer a pack edit or a plan-time note instead.
- **List:** `prefs.py list`. **Forget:** `prefs.py forget N` removes both halves.
- **End of reel:** `uv run engine/learn/teach.py offer <job>` prints candidate rules from their notes.
  ONE pick-many box; `teach.py keep <ids>`, then `teach.py done <job>`. Never re-ask on the same reel.

Never learnable: the register, hook copy, pixel placements.

**Next:** it applies on the next reel for that brand.
