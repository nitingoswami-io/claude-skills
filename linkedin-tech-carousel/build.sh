#!/usr/bin/env bash
# Build this skill into a .skill archive for Claude Desktop upload.
# Run from anywhere: `./linkedin-tech-carousel/build.sh` or `cd linkedin-tech-carousel && ./build.sh`.
# Output: ./dist/<skill-name>.skill (next to this script).

set -euo pipefail

skill_dir="$(cd "$(dirname "$0")" && pwd)"
name="$(basename "$skill_dir")"
parent="$(dirname "$skill_dir")"
out="$skill_dir/dist/$name.skill"

if [[ ! -f "$skill_dir/SKILL.md" ]]; then
  echo "error: $skill_dir/SKILL.md is missing — every skill must have a SKILL.md" >&2
  exit 1
fi

mkdir -p "$skill_dir/dist"
rm -f "$out"

# Zip from the parent so the archive root is <name>/SKILL.md, not just SKILL.md.
# Exclude local build outputs, this script, and the human-facing README from the shipped archive.
(
  cd "$parent"
  zip -qr "$out" "$name" \
    -x "$name/dist/*" \
    -x "$name/build.sh" \
    -x "$name/README.md" \
    -x "*.DS_Store" \
    -x "*__pycache__*"
)

echo "built: $out"
unzip -l "$out"
