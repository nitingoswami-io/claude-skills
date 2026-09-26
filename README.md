# claude-skills

A small, growing collection of [Claude Skills](https://docs.claude.com/en/docs/claude-code/skills) built for real work and released for anyone to use, adapt, and remix.

Each skill in this repo is a self-contained folder with a `SKILL.md` manifest, supporting references, and its own README. Skills are opinionated — they encode a specific way of doing a specific thing well, so you can install one and get a good result on your first try.

## Skills in this repo

| Skill | What it does |
|---|---|
| [`market-teardown/`](market-teardown/) | Turn your research on any market, product, or startup idea into a data-dense, verdict-driven teardown article (~1,500 words) plus a companion feed post. |

More skills will be added over time. See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to propose one.

## Install a skill

Every skill in this repo works in both Claude Code and Claude Desktop.

### Claude Code

Copy the skill folder into your Claude Code skills directory:

```bash
git clone https://github.com/<your-username>/claude-skills.git
cp -r claude-skills/market-teardown ~/.claude/skills/market-teardown
```

Skills placed under `~/.claude/skills/` are auto-discovered on the next Claude Code session. The skill fires when your prompt matches the trigger phrases in the skill's `description:` frontmatter (see the skill's own README for examples).

### Claude Desktop

Claude Desktop expects skills as a single `.skill` zip archive. Build one:

```bash
git clone https://github.com/<your-username>/claude-skills.git
cd claude-skills
./scripts/build-skill.sh market-teardown
```

That writes `dist/market-teardown.skill`. Add it to Claude Desktop via **Settings → Capabilities → Skills → Add skill** (or the equivalent path for your app version) and point it at the built file.

## Repo layout

```
claude-skills/
├── README.md                 # you are here
├── LICENSE                   # MIT
├── CONTRIBUTING.md           # how to propose changes or new skills
├── scripts/
│   └── build-skill.sh        # zip a skill folder into dist/<name>.skill
└── <skill-name>/             # one directory per skill
    ├── SKILL.md              # manifest + instructions (required)
    ├── README.md             # human-facing docs (required)
    ├── references/           # supporting docs Claude reads on demand
    └── assets/               # templates, snippets, etc.
```

Each skill directory is the source of truth. Zipped `.skill` bundles are build artifacts and are gitignored.

## Why open-source

Good skills are hard to write. The craft is in the instructions — the small structural rules and refusals that separate a competent output from a generic one. Publishing them lets other people benefit from that work, and lets me improve mine by learning from how they get adapted.

If you extend one of these skills or build something interesting on top, I'd love to see it. Open an issue or PR.

## License

MIT. See [LICENSE](LICENSE). Use freely, credit appreciated but not required.

## Author

By [Nitin Goswami](https://github.com/nitingoswami-io). Feedback, issues, and pull requests welcome.
