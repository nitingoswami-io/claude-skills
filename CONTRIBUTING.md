# Contributing

Thanks for the interest. This repo takes three kinds of contributions.

## 1. Report an issue

If a skill produces a bad result, misses a case, or doesn't fire when it should, open an issue with:

- The skill name
- Your prompt (or a redacted version)
- What you got, and what you expected

Screenshots or the raw model output are welcome but not required.

## 2. Improve an existing skill

Small, focused PRs are best. A good improvement usually looks like one of:

- A sharper trigger phrase in the `description:` frontmatter (with a case that fails today)
- A structural rule that fixes a common failure mode
- A worked example that shows the skill applied to a different domain

Keep the skill's core discipline intact. If you want to reshape the whole approach, open an issue first — it's easier to discuss the redesign before code.

## 3. Contribute a new skill

New skills are welcome. To keep the repo coherent, each skill folder must contain:

```
<skill-name>/
├── SKILL.md              # YAML frontmatter (name, description) + instructions
├── README.md             # what it does, install, adapt notes, one example
├── references/           # optional: supporting docs the skill reads
└── assets/               # optional: templates the skill uses
```

`SKILL.md` should follow the [Claude Skills spec](https://docs.claude.com/en/docs/claude-code/skills):

```yaml
---
name: skill-name
description: >-
  One paragraph. Names the concrete outputs, lists trigger phrases, and
  gives 2–3 example prompts. This is what Claude matches against.
---
```

Before opening the PR:

1. Test the skill end-to-end in a fresh Claude Code session (or in Claude Desktop after building the `.skill`).
2. Confirm the trigger fires on the example prompts in your README.
3. Run `grep -rniE 'your-name|your-project|/Users/'` inside the skill folder — no personal references.

## Style

- Instructions in `SKILL.md` are prose, not bullet lists of vague guidelines. Say what to do; give an example.
- References are read on demand — put the deep detail there so `SKILL.md` stays scannable.
- Every skill's README should show one concrete example of its output, or link to one in `references/`.

## License

By contributing, you agree that your contribution will be licensed under the MIT License that covers the rest of the repo.
