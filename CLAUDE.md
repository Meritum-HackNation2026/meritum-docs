# CLAUDE.md

@AGENTS.md

The three rules from AGENTS.md apply to every change in this repo:

1. Write each article, then pass it through the `humanizer` skill (`.claude/skills/humanizer/SKILL.md`, embedded mode) before committing. The same goes for commit messages and PR text.
2. The Meritum design system wins over any other style choice; load the `meritum-ui` skill (meritum-monorepo, `.claude/skills/meritum-ui/`) before touching CSS, HTML components, diagrams or icons.
3. Facts come from the product document and the repos, never from memory. Never edit pages marked `Wygenerowane przez scripts/generate.py`.
