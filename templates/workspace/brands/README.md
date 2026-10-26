# Brands

One folder per client brand. The engine is shared; everything that makes a reel sound and look like a
client lives here.

```
brands/
├── _agency/        house defaults every brand inherits (kit, packs, learned prefs)
├── _template/      copied to start a new brand: "new brand <name>"
└── <brand>/
    ├── brand-kit.md     the client's voice, look, transcriber fixes, learned bullets
    ├── packs.json       their style packs (optional; falls back to _agency, then Neutral)
    ├── learned.json     taught preferences for this brand only
    ├── fonts/           their licensed fonts (never committed)
    └── projects/<job>/  their reels (never committed)
```

Resolution order for any setting: the brand → `_agency` → the engine default.
The active brand is `_local/active-brand`; "switch to <brand>" changes it, and every job name can
also be given as `<brand>/<job>`.
