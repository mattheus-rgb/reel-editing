#!/usr/bin/env bash
# SessionStart: one short briefing of what needs attention. Says nothing when all is well.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
notes=()
for t in ffmpeg ffprobe uv node npx; do
  command -v "$t" >/dev/null 2>&1 || notes+=("$t is not installed: suggest 'set me up'.")
done
[ -d .venv ] || notes+=("The Python toolbelt is not built (no .venv): 'uv sync'.")
[ -d node_modules/hyperframes ] || notes+=("The renderer is not installed: 'npm install'.")
blanks=$(grep -c '{{' brand-kit.md 2>/dev/null || echo 0)
if [ "${blanks:-0}" -gt 0 ]; then
  notes+=("brand-kit.md has $blanks blank fields: suggest 'build my homebase' once, then edit anyway.")
fi
if [ -s _local/learned.json ]; then
  notes+=("_local/learned.json has learned preferences; builds apply them (see 'learn').")
fi
[ ${#notes[@]} -eq 0 ] && exit 0
printf '%s\n' "${notes[@]}" | python3 -c '
import json,sys
txt=sys.stdin.read().strip()
print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Engine briefing:\n"+txt}}))'
