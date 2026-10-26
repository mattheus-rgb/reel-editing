#!/usr/bin/env bash
# PreToolUse: refuse any destructive touch to CapCut's draft folder. Drafts are versioned, never deleted.
payload=$(cat)
draft_dir="com.lveditor.draft"
echo "$payload" | grep -q "$draft_dir" || exit 0
tool=$(echo "$payload" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_name",""))' 2>/dev/null)
case "$tool" in
  Write|Edit|MultiEdit)
    echo "Refused: never hand-edit a CapCut draft. Build a new version through engine/capcut/draft.py." >&2; exit 2 ;;
  Bash)
    if echo "$payload" | grep -Eq 'r''m |r''mdir|r''mtree|unlink|os\.re''move|-de''lete'; then
      echo "Refused: never remove anything inside CapCut's draft folder. Versions are kept; use engine/capcut/safety.py." >&2; exit 2
    fi ;;
esac
exit 0
