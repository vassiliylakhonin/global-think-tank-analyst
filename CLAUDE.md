@AGENTS.md

# Claude Code working rules

This repository is Global Think Tank Analyst.

It should remain a strategic-risk analysis skill for AI agents.

It is a domain reasoning layer and behavior contract, not:
- a generic prompt pack;
- a CLI tool;
- a framework;
- a factuality verifier;
- an MCP server;
- an eval infrastructure project;
- a legal, sanctions, compliance, or investment-advice product.

## How to work in this repo

Before editing, inspect relevant project files when present:
- README.md
- AGENTS.md
- SKILL.md
- llms.txt
- examples/
- docs/
- signals/
- evals/

Prefer small, safe, reviewable changes.

Do not rewrite the project unless explicitly asked.

Preserve the existing project positioning and terminology unless there is a clear inconsistency.

## Preserve project boundaries

Do not add or imply:
- live source retrieval;
- factuality verification guarantees;
- legal, sanctions, compliance, or investment advice;
- production-grade guarantees;
- benchmark claims;
- MCP server functionality;
- CLI validation;
- schemas or scoring infrastructure.

If validation, scoring, schemas, CLI, MCP, or CI checks are discussed, present them as possible future work only when explicitly requested, or point to the appropriate companion project if the repository already documents one.

## Content rules

When editing docs, examples, or skill instructions:
- separate facts, assessments, assumptions, scenarios, and unknowns;
- preserve evidence-mode labels and uncertainty language;
- do not fabricate citations, dates, policy changes, sanctions details, incidents, metrics, or benchmark results;
- avoid hype and unsupported claims;
- keep the project credible, conservative, and decision-useful.

## Definition of done

Before finishing, report:
1. what changed;
2. why it matters;
3. what was not changed;
4. how I can verify it;
5. risks or follow-ups.
