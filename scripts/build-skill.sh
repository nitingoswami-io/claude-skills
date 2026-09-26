#!/usr/bin/env bash
# Zip a skill folder into dist/<name>.skill for Claude Desktop.
#
# Usage: ./scripts/build-skill.sh <skill-name>
# Example: ./scripts/build-skill.sh market-teardown

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <skill-name>" >&2
  exit 2
fi

skill="$1"
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
src="$repo_root/$skill"
out_dir="$repo_root/dist"
out="$out_dir/$skill.skill"

if [[ ! -d "$src" ]]; then
  echo "error: skill directory not found: $src" >&2
  exit 1
fi

if [[ ! -f "$src/SKILL.md" ]]; then
  echo "error: $src/SKILL.md is missing — every skill must have a SKILL.md" >&2
  exit 1
fi

mkdir -p "$out_dir"
rm -f "$out"

# Zip from the parent so the archive root is <skill>/SKILL.md, not just SKILL.md.
(
  cd "$repo_root"
  zip -qr "$out" "$skill" -x "*.DS_Store" -x "$skill/README.md"
)

echo "built: $out"
unzip -l "$out"
