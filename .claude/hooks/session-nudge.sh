#!/usr/bin/env bash
# SessionStart: one short briefing of what needs attention. Says nothing when all is well.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
notes=()
for t in ffmpeg ffprobe uv node npx; do
  command -v "$t" >/dev/null 2>&1 || notes+=("$t is not installed: suggest 'set me up'.")
done
[ -d .venv ] || notes+=("The Python toolbelt is not built (no .venv): 'uv sync'.")
[ -d node_modules/hyperframes ] || notes+=("The renderer is not installed: 'npm install'.")
brand=$(cat _local/active-brand 2>/dev/null | tr -d '[:space:]')
if [ -n "$brand" ] && [ -d "brands/$brand" ]; then
  notes+=("Active brand: $brand. Name it before the first cut; 'switch to <brand>' changes it.")
  blanks=$(grep -c '{{' "brands/$brand/brand-kit.md" 2>/dev/null || echo 0)
  [ "${blanks:-0}" -gt 0 ] && notes+=("brands/$brand/brand-kit.md has $blanks blank fields: suggest 'build the homebase for $brand' once, then edit anyway.")
  [ -s "brands/$brand/learned.json" ] && notes+=("brands/$brand/learned.json has learned preferences; builds apply them.")
else
  n=$(ls -d brands/*/ 2>/dev/null | grep -v '/_' | wc -l | tr -d ' ')
  if [ "$n" -eq 0 ]; then notes+=("No client brands yet: 'new brand <name>' makes one from brands/_template.");
  else notes+=("No active brand ($n exist). Ask which brand before the first cut, or 'switch to <brand>'."); fi
fi
notes+=("The Studio page shows every client and reel: they can say 'open my studio'.")
[ ${#notes[@]} -eq 0 ] && exit 0
printf '%s\n' "${notes[@]}" | python3 -c '
import json,sys
txt=sys.stdin.read().strip()
print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Engine briefing:\n"+txt}}))'
