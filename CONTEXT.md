# Global Think Tank Analyst

This context defines the language for the **horizontal strategic-risk reasoning skill** inside the broader Agenda Intelligence stack. It exists to keep reasoning-method scope, evidence discipline, and naming distinct from the product shell and the vertical specialists.

## Language

**Global Think Tank Analyst**:
The horizontal reasoning skill that teaches an AI agent how to produce policy-risk, sanctions, regulatory, geopolitical and trade memos with explicit evidence boundaries, uncertainty, scenarios, actor incentives, and watch-next indicators.
_Avoid_: Vertical specialist, MCP server, validation engine, sanctions-screening product

**Reasoning Method**:
The portable memo-architecture and analytical workflow this skill teaches: decision framing, fact / assumption / assessment separation, evidence labels, memo modes, self-check.
_Avoid_: Domain database, regional doctrine, source-retrieval engine

**Policy Risk Memo Architect**:
The named method GTTA implements. Used inside Agenda Intelligence MD's `analyze` as the default reasoning module when no other method is specified.
_Avoid_: Generic prompt template, separate product, region-specific framework

**Memo Mode**:
A reusable output shape (executive brief, decision-briefing pack, red-team memo, scenario brief, monitoring memo) selected by the agent based on decision context.
_Avoid_: Document template without analytical commitments, freeform summary

**Agenda Intelligence MD**:
The product shell and evidence-discipline layer that vendors this skill, routes geography to vertical specialists, validates output structure, audits evidence, and scores outputs where implemented.
_Avoid_: Parent skill, source retriever, factual verifier, compliance product

**Vertical Specialist**:
A regional or sector reasoning skill (Central Asia + Caspian, Gulf + Middle East) that composes on top of GTTA's horizontal method and adds domain depth. Routed automatically by `analyze` when the geography matches.
_Avoid_: Replacement for GTTA, source database, standalone analyst

**Evidence Mode**:
The label that states what kind of evidence was available during a memo workflow (`live-source-backed`, `user-provided sources`, `illustrative source packet`, `reasoning-only`).
_Avoid_: Retrieval capability, factual truth status, source guarantee

**Per-claim Provenance Tag**:
The mandatory two-axis tag on every factual claim. Axis A names source type (`[primary]`, `[secondary]`, `[user-provided]`, `[inference]`, `[analyst-judgment]`); Axis B is optional action flags (`[verify]`, `[stale-risk: YYYY-MM]`).
_Avoid_: Flat tag list, conflation of source-type with reliability-state, bulk-attribution footnote

**Linguistic Faithfulness**:
The rule that the decisiveness of language must match the stated confidence and provenance tag. Over-confident framing of inferences and over-hedging of verified facts are both honesty-rule violations.
_Avoid_: Style guideline, tone preference

**Three-value Response Logic**:
Answer / Flag-but-don't-use / Stop-and-request — replaces the binary "answer or refuse" default. Silence about known doubt is treated the same as confident assertion.
_Avoid_: Binary refusal logic, blanket caveats

**Signal**:
A short public artifact in the `signals/` archive that demonstrates the skill's analytical style on a current strategic-risk topic. Signals are distribution examples, not official intelligence or operational guidance.
_Avoid_: Real-time intelligence product, monitored feed, current-facts source-of-truth

**Agent-eval Delta**:
The validation methodology: same model, same question, run with and without the skill loaded, scored against a binary structural rubric tied to `agenda-memo.schema.json`. Canonical methodology lives in the product shell at `agenda-intelligence-md/docs/agent-eval-methodology.md`.
_Avoid_: Aggregate benchmark, model-quality comparison, accuracy claim, practitioner validation

**Practitioner Review**:
External review by a domain practitioner (policy, sanctions, regulatory) recorded under `reviews/`. Author self-review does not count. This is GTTA's stricter validation axis relative to the vertical-specialist Bar 1 / Bar 2 framework.
_Avoid_: Self-scored validation, internal QA, automated check

**Maturity Framework**:
GTTA uses `VALIDATION_PLAN.md` (case packets → practitioner feedback). Vertical specialists use a separate two-bar Definition of Done. The frameworks are not interchangeable; portfolio write-ups must state which one is being referenced.
_Avoid_: Bar 1 / Bar 2 (that vocabulary belongs to the vertical-specialist canon)
