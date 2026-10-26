#!/usr/bin/env bash
# Builds dist/reel-editing-<version>.zip: the plugin folder, without git, venvs, caches or workspaces.
set -e
cd "$(dirname "$0")"
v=$(python3 -c 'import json;print(json.load(open(".claude-plugin/plugin.json"))["version"])')
mkdir -p dist; out="dist/reel-editing-v$v.zip"; rm -f "$out"
tmp=$(mktemp -d); mkdir "$tmp/reel-editing"
rsync -a --exclude .git --exclude .venv --exclude node_modules --exclude dist --exclude /_local --exclude /inbox \
  --exclude /brands --exclude /projects --exclude __pycache__ --exclude .pytest_cache --exclude '.DS_Store' --exclude '*.mp4' --exclude '*.mov' \
  ./ "$tmp/reel-editing/"
# The symlinks under .claude/ are for working in this repo; a plugin install does not need them.
rm -rf "$tmp/reel-editing/.claude"
( cd "$tmp" && zip -qr "$OLDPWD/$out" reel-editing )
rm -rf "$tmp"
echo "$out  $(du -h "$out" | cut -f1)"
