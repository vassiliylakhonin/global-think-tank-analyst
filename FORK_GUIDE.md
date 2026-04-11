# Fork Guide (15 minutes)

This guide helps you adapt `global-think-tank-analyst` to your own domain quickly.

## 1) Fork and clone

```bash
gh repo fork vassiliylakhonin/global-think-tank-analyst --clone
cd global-think-tank-analyst
```

## 2) Rebrand (2 minutes)

Edit:
- `SKILL.md` frontmatter `name`, `description`, `homepage`
- `README.md` title + first paragraph

Naming tip:
- Keep it specific: `regional-risk-analyst`, `startup-strategy-analyst`, `nonprofit-policy-analyst`

## 3) Adapt domain scope (5 minutes)

In `SKILL.md`, update:
- Primary domain and audience
- High-relevance domains section
- Output examples and terminology

Examples:
- **Government/policy**: diplomacy, sanctions, national security, treaty options
- **Startup/VC**: market timing, competitor moves, regulatory risk, GTM options
- **Nonprofit**: donor alignment, implementation risk, safeguarding, MEAL implications

## 4) Keep output contract stable (3 minutes)

Preserve decision-useful structure:
- Executive summary
- Assumptions + confidence
- Alternative hypotheses
- Risks + indicators to watch
- Action options / recommendations

## 5) Add your examples (3 minutes)

Create or edit files in `examples/`:
- `examples/queries.md`
- `examples/adaptations.md`

Include at least 3 domain-specific prompts with expected output style.

## 6) Publish

```bash
git checkout -b feat/domain-adaptation
git add .
git commit -m "feat: adapt skill for <your-domain>"
git push -u origin feat/domain-adaptation
```

Then publish your adapted skill in ClawHub/GitHub with before/after examples.

---

## Fast adaptation checklist

- [ ] Name and description are domain-specific
- [ ] README clearly states target users and use-cases
- [ ] SKILL.md frameworks match your domain
- [ ] 3+ examples added
- [ ] Confidence + assumptions preserved
- [ ] License kept (MIT)
