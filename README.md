# claude-skills

A small, growing collection of [Claude Skills](https://docs.claude.com/en/docs/claude-code/skills) built for real work and released for anyone to use, adapt, and remix.

**Each skill is a fully self-contained folder.** Everything a skill needs — its manifest, references, build script, license, and README — lives inside its own directory. You can `git clone` this repo and cherry-pick a single skill folder into `~/.claude/skills/` without dragging the rest of the repo along. Skills are opinionated: they encode a specific way of doing a specific thing well, so you install one and get a good result on your first try.

## Skills in this repo

| Skill | What it does |
|---|---|
| [`market-teardown/`](market-teardown/) | Turn your research on any market, product, or startup idea into a data-dense, verdict-driven teardown article (~1,500 words) plus a companion feed post. |

More skills will be added over time. See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to propose one.

## Install a skill

Every skill in this repo works in both **Claude Code** (the CLI) and **Claude Desktop** (the app). Pick the one you use.

The examples below use `market-teardown`. Swap in whatever skill you're installing.

### 1) Claude Code

Copy the skill folder into your local skills directory:

```bash
git clone https://github.com/<your-username>/claude-skills.git
cp -r claude-skills/market-teardown ~/.claude/skills/market-teardown
```

Restart Claude Code. It picks up the skill automatically — no separate enable step. The skill fires whenever your prompt matches the trigger phrases in its `description:` frontmatter (see the skill's own README for example prompts).

### 2) Claude Desktop

Two easy paths — Option A is the fastest.

**Option A — Ask Claude to install it for you.**

1. Open a new chat in Claude Desktop.
2. **Drag the entire `market-teardown/` folder into the chat** — or attach it with the paperclip / `+` button. Make sure you attach the folder itself, not just `SKILL.md` — this skill has supporting files under `references/` and `assets/` that need to be included, and pasting `SKILL.md` alone will drop them.
3. Say: *"Please install this as a skill."*

Claude will validate the frontmatter, show you a review card, and save it in one click. This is the easiest way and catches formatting mistakes before upload.

**Option B — Upload the zip yourself.**

1. Build the `.skill` archive using the skill's own build script:
   ```bash
   git clone https://github.com/<your-username>/claude-skills.git
   cd claude-skills/market-teardown
   ./build.sh
   ```
   That produces `dist/market-teardown.skill` inside the skill folder.
2. In Claude Desktop, go to **Settings → Capabilities → Skills**, click **Upload skill**, and choose the file. (Menu names may vary slightly by app version.)
3. Wait ~1–2 minutes for the security scan.
4. When the skill turns green, toggle it on.
5. Test it in a new chat — e.g. *"teardown of on-device inference economics"* — and the skill should fire.

**If the skill doesn't fire**, check that **Code execution and file creation** is enabled under Settings — skills require it.

**Updating a skill you already installed?** Just upload the new `.skill` file in its place; it replaces the previous version.

**Common mistakes** (from Anthropic's own guidance):

- Zip structure — the archive must contain the skill *folder* at its root, not the loose files. Each skill's `build.sh` gets this right for you.
- Frontmatter — `SKILL.md` must start with a valid YAML `---` block that has both `name` and `description`.
- `name` field — lowercase and hyphens only, no spaces or capitals.
- `description` field — must be specific enough that Claude knows when to trigger it.

## Repo layout

```
claude-skills/
├── README.md                 # you are here — index of skills
├── LICENSE                   # MIT (covers the repo as a whole)
├── CONTRIBUTING.md           # how to propose changes or new skills
└── <skill-name>/             # one directory per skill — fully self-contained
    ├── SKILL.md              # manifest + instructions (required)
    ├── README.md             # human-facing docs (required)
    ├── LICENSE               # MIT (travels with the folder)
    ├── build.sh              # zips this folder into dist/<name>.skill
    ├── references/           # supporting docs Claude reads on demand
    ├── assets/ or examples/  # templates, sample inputs, etc.
    └── scripts/              # optional: runnable code the skill invokes
```

Each skill directory is the source of truth. Zipped `.skill` bundles are build artifacts and are gitignored.

## Why open-source

Good skills are hard to write. The craft is in the instructions — the small structural rules and refusals that separate a competent output from a generic one. Publishing them lets other people benefit from that work, and lets me improve mine by learning from how they get adapted.

If you extend one of these skills or build something interesting on top, I'd love to see it. Open an issue or PR.

## License

MIT. See [LICENSE](LICENSE). Use freely, credit appreciated but not required.

## Author

By [Nitin Goswami](https://github.com/nitingoswami-io). Feedback, issues, and pull requests welcome.
