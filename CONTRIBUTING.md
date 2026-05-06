# Contributing

Thanks for contributing.

## Ground rules

- Keep the skill decision-focused and evidence-disciplined.
- Do not add fabricated sources or unsupported certainty patterns.
- Prefer concise, practical improvements over framework bloat.
- Keep agent guidance runtime-neutral unless a section is explicitly for a specific tool.
- When adding examples, make them useful in at least one real user workflow.

## Development workflow

1. Create a branch from `main`.
2. Edit `SKILL.md`, `AGENTS.md`, `llms.txt`, and docs if behavior changes.
3. Keep changes scoped and explain the decision value.
4. Open a PR with before/after examples.

## PR checklist

- [ ] `name` and `description` remain valid in frontmatter
- [ ] Behavior change is documented in `CHANGELOG.md`
- [ ] `AGENTS.md`, `SKILL.md`, `codex/SKILL.md`, and `llms.txt` remain aligned when agent behavior changes
- [ ] Prompts/examples stay decision-oriented
- [ ] No claims of external verification unless truly performed
