#!/usr/bin/env python3
"""Check that every skill folder is a self-contained, MIT-licensed unit.

Run from the repo root:  python3 scripts/check_skills.py
Exits 1 if any check fails. Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOLDER = "Nitin Goswami"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Placeholders and local paths that must not ship in a public skill.
PERSONAL = re.compile(r"/Users/|<your-username>")
TEXT_SUFFIXES = {".md", ".mdx", ".py", ".sh", ".json", ".txt", ".html", ".yml", ".yaml", ".mjs", ".js"}


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            out[key] = km.group(2).strip()
        elif key and line.startswith(" "):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def check_license(path: Path, errors: list) -> None:
    if not path.is_file():
        errors.append(f"{path.relative_to(ROOT)}: missing")
        return
    text = path.read_text()
    if not text.startswith("MIT License"):
        errors.append(f"{path.relative_to(ROOT)}: not an MIT license")
    if not re.search(rf"Copyright \(c\) \d{{4}} {re.escape(HOLDER)}", text):
        errors.append(f"{path.relative_to(ROOT)}: copyright line must name {HOLDER} and a year")


def skill_dirs() -> list:
    return sorted(p.parent for p in ROOT.glob("*/SKILL.md"))


def main() -> int:
    errors: list = []
    check_license(ROOT / "LICENSE", errors)

    skills = skill_dirs()
    if not skills:
        errors.append("no skill folders found")
    readme = (ROOT / "README.md").read_text()

    for d in skills:
        name = d.name
        fm = frontmatter((d / "SKILL.md").read_text())
        if fm.get("name") != name:
            errors.append(f"{name}/SKILL.md: frontmatter name must be '{name}' (got {fm.get('name')!r})")
        if not NAME_RE.match(name):
            errors.append(f"{name}: folder name must be lowercase and hyphens only")
        desc = fm.get("description", "").lstrip(">-| ").strip()
        if len(desc) < 80:
            errors.append(f"{name}/SKILL.md: description is missing or too short to trigger on")

        check_license(d / "LICENSE", errors)
        rd = d / "README.md"
        if not rd.is_file():
            errors.append(f"{name}/README.md: missing")
        else:
            rtext = rd.read_text()
            for heading in ("## Install", "## Contributing", "## License"):
                if heading not in rtext:
                    errors.append(f"{name}/README.md: add a '{heading}' section")
        if not (d / "build.sh").is_file():
            errors.append(f"{name}/build.sh: missing")
        if f"({name}/)" not in readme:
            errors.append(f"README.md: '{name}' is not listed in the skills table")

        for f in d.rglob("*"):
            if f.is_file() and f.suffix in TEXT_SUFFIXES and "dist" not in f.parts:
                for i, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
                    if PERSONAL.search(line):
                        errors.append(f"{f.relative_to(ROOT)}:{i}: personal path or placeholder")

    for e in errors:
        print(f"FIX {e}")
    print(f"{len(skills)} skill(s) checked, {len(errors)} problem(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
