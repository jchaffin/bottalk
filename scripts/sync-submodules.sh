#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git submodule sync --recursive 2>/dev/null || true

for name in agents frontend; do
  if [[ ! -d "$name/.git" ]] && [[ ! -f "$name/.git" ]]; then
    echo "Skip $name (not checked out). Run: git submodule update --init"
    continue
  fi
  echo "==> $name"
  git -C "$name" fetch origin
  git -C "$name" checkout master
  git -C "$name" pull --ff-only origin master
done

echo ""
echo "Next: git status — if agents/frontend changed, git add agents frontend && git commit -m 'Bump submodules'"
