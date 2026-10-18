# Contributing to {{slug}}

Thanks for looking under the hood. This repo is a **learning demo**: it's kept small on purpose so each stage stays visible. Read [`docs/DESIGN.md`](docs/DESIGN.md) first. It explains the architecture, the flows and how the demo maps to the CoALA agent framework.

## Ways to help

- **Try an idea from Next steps.** Section 10 of the design doc lists extensions, each with what it teaches. Fork the repo, build one, and open a pull request.
- **Report a problem.** [Open an issue]({{repo}}/issues/new) with what you ran, what you expected and what happened. Paste the exact command and any error.
- **Improve the docs.** Fix a step in *Run & verify* that didn't work for you, or clarify a diagram.

## Workflow

1. [Fork the repo]({{repo}}/fork) and clone your fork:
   ```bash
   git clone https://github.com/<you>/{{slug}}.git
   cd {{slug}}
   ```
2. Create a branch: `git checkout -b feat/<short-name>`.
3. Follow *Run & verify* in `docs/DESIGN.md` and make sure every check in its table still passes.
4. If you change behaviour, update `docs/DESIGN.md`. Update the figures in `docs/figures/` too, if they're affected.
5. Open a pull request against `main`. Describe the change and say which check you ran.

## Ground rules

- Keep it a demo: no new services or frameworks unless the change is about them.
- Don't commit secrets. `.env` stays local; add new variables to `.env.example`.
- Be kind in reviews and issues.

By contributing, you agree that your contributions are licensed under the repository's license.
