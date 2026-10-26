#!/usr/bin/env bash
# Notification: a soft sound when Claude is waiting on them. Off switch: _local/chime.off exists.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f _local/chime.off ] && exit 0
last=_local/.chime-last; now=$(date +%s)
if [ -f "$last" ] && [ $((now - $(cat "$last" 2>/dev/null || echo 0))) -lt 10 ]; then exit 0; fi
echo "$now" > "$last"
( afplay /System/Library/Sounds/Glass.aiff >/dev/null 2>&1 & ) 2>/dev/null
exit 0
