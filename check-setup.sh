#!/usr/bin/env bash
# Reports what is missing and prints the line that installs it. Changes nothing.
missing=0
need() { # name, command, install line, job
  if command -v "$2" >/dev/null 2>&1; then
    printf "  ok   %-8s %s\n" "$1" "$4"
  else
    printf "  MISSING %-8s %s\n         install: %s\n" "$1" "$4" "$3"; missing=$((missing+1))
  fi
}
echo "Checking tools:"
need brew    brew   '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"' "installs the rest"
need ffmpeg  ffmpeg "brew install ffmpeg" "cuts, joins and levels footage"
need ffprobe ffprobe "brew install ffmpeg" "reads footage"
need uv      uv     "brew install uv" "builds the Python toolbelt"
need node    node   "brew install node" "runs the graphics renderer"
need npx     npx    "brew install node" "runs the graphics renderer"
echo
if [ -d .venv ]; then echo "  ok   toolbelt  (.venv present)"; else echo "  MISSING toolbelt   install: uv sync"; missing=$((missing+1)); fi
if [ -d node_modules/hyperframes ]; then echo "  ok   renderer  (node_modules/hyperframes)"; else echo "  MISSING renderer   install: npm install"; missing=$((missing+1)); fi
blanks=$(grep -c '{{' brand-kit.md 2>/dev/null || echo 0)
echo
echo "Brand kit blanks: $blanks  (0 = set up; otherwise say 'build my homebase')"
echo
if [ "$missing" -eq 0 ]; then echo "All tools present."; else echo "$missing thing(s) to install."; exit 1; fi
