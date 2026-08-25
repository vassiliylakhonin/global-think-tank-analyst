# Integration: Agenda Intelligence MD

This recipe shows how to compose **Global Think Tank Analyst** (this repo, horizontal reasoning skill) with **[Agenda Intelligence MD](https://github.com/vassiliylakhonin/agenda-intelligence-md)** (primarily a deterministic evidence-packet linter).

Use this skill to draft the strategic-risk memo. Then extract externally checkable claims and caller-supplied source text into an evidence packet before human review.

## Primary v1.3 path — lint the claim/source packet

The handoff contract and selection rules live in [`../evidence-packet-handoff.md`](../evidence-packet-handoff.md). A runnable synthetic packet lives at [`../../examples/evidence-packet-handoff.json`](../../examples/evidence-packet-handoff.json).

```bash
pip install "agenda-intelligence-md>=1.3.0"
agenda-intelligence check examples/evidence-packet-handoff.json --format json
agenda-intelligence check examples/evidence-packet-handoff.json --strict
```

The linter reports broken source references, declared-quote mismatches, weak lexical support, unmatched numbers, and reviewer actions. It reports packet completeness, not factual truth.

## Compatibility paths

The older strategic-intelligence schemas, scoring commands, and MCP tools below remain available for callers that already depend on them. They are compatibility workflows, not the primary first-run path, and their heuristic scores do not measure current evidence-packet linter performance.

### Older memo and evidence-pack capabilities

| Capability | Command | Input | Output |
|---|---|---|---|
| Schema validation of a structured brief | `agenda-intelligence validate-brief brief.json` | JSON conforming to `agenda-brief.schema.json` | Pass/fail + schema errors |
| Schema validation of an evidence pack | `agenda-intelligence validate-evidence pack.json` | JSON conforming to `evidence-pack.schema.json` | Pass/fail + schema errors |
| Structural quality score (heuristic, 0–100) | `agenda-intelligence score brief.json` | JSON brief | Score + per-signal breakdown |
| Evidence-aware structural score | `agenda-intelligence score brief.json --evidence pack.json` | JSON brief + evidence pack | Score + claim-level evidence support |
| Markdown structural score | `agenda-intelligence score memo.md` | Markdown with the protocol's signals | Score |
| MCP server for the same operations | `agenda-intelligence-mcp` | stdio transport | `validate_brief`, `validate_evidence`, `score_output`, `get_protocol`, `list_lenses`, `get_lens`, `source_plan` |

Scoring is a **heuristic structural rubric**. It does not verify factual truthfulness. These commands remain useful for regression and existing integrations, but should not be confused with `agenda-intelligence check <evidence-packet.json>`.

### Compatibility recipe A — score a markdown memo for structure

Cheapest path. Works directly on a memo written with this skill, no JSON projection required. Best for quick "does the memo even hit the structural bar" checks.

```bash
# 1. Draft the memo with this skill (in any AI agent)
#    Save the result as memo.md.

# 2. Score it
agenda-intelligence score memo.md
```

What the score is good at:
- catching missing signal classification, watch-next, or main uncertainty;
- flagging memos that read as background essays rather than decision-shaped output.

What the score is not:
- not a factual check;
- does not establish that the memo is correct;
- not a benchmark.

### Compatibility recipe B — validate and score a structured brief

Stricter path. Project the memo into a JSON brief that conforms to `agenda-brief.schema.json`, then validate and score. Best for pipelines that ingest memos and need machine-readable validation.

A minimal projection of a Global Think Tank Analyst memo into an `agenda-brief.json`:

```json
{
  "bottom_line": "<the memo's executive takeaway, one sentence>",
  "signal_classification": "compliance_relevant_development",
  "what_changed": "<the main fact or development the memo turns on>",
  "why_it_matters": "<the decision relevance, one sentence>",
  "affected_actors": ["<actor 1>", "<actor 2>"],
  "main_uncertainty": "<the dominant unresolved question>",
  "scenarios": [
    {
      "name": "Baseline",
      "description": "<scenario description>",
      "indicators": ["<indicator 1>", "<indicator 2>"]
    }
  ],
  "watch_next": ["<watch-next indicator 1>", "<watch-next indicator 2>"],
  "evidence_mode": "reasoning_only",
  "confidence": "medium"
}
```

Mapping notes (this skill ↔ agenda-brief schema):

| This skill (memo field) | `agenda-brief.json` field |
|---|---|
| Executive takeaway / Key judgment | `bottom_line` |
| Why it matters / Decision context | `why_it_matters` |
| The main fact or development | `what_changed` |
| Actors and incentives | `affected_actors` |
| Key unknowns | `main_uncertainty` |
| Scenarios | `scenarios[]` |
| Watch-next indicators | `watch_next` |
| Evidence mode (`live-source-backed`, `user-provided sources`, `illustrative source packet`, `reasoning-only`) | `evidence_mode` (use `source_backed`, `user_provided`, `illustrative`, or `reasoning_only`) |
| Confidence (Low / Moderate / High) | `confidence` (`low` / `medium` / `high`) |

Then:

```bash
agenda-intelligence validate-brief brief.json
agenda-intelligence score brief.json
```

The projection is lossy on purpose. The full memo (options, trade-offs, actor incentives detail, "what would change the judgment") stays in the markdown; the JSON is a structural surface for validators.

### Compatibility recipe C — add an evidence pack for claim-level audit

When the memo was produced in `live-source-backed` or `user-provided sources` mode, you can pair the brief with an `evidence-pack.json` and get claim-level support feedback.

```bash
agenda-intelligence validate-evidence pack.json
agenda-intelligence score brief.json --evidence pack.json
```

In `reasoning-only` or `illustrative source packet` mode, do **not** assemble a fake evidence pack to make the score look better. That is exactly the failure mode this skill's evidence rules try to prevent. If there are no real sources, lower the confidence and skip the evidence step.

### Compatibility recipe D — call from an MCP-aware agent

Agenda Intelligence MD ships an MCP stdio server: `agenda-intelligence-mcp`. An MCP-aware agent (Claude Code, Cursor, Codex with MCP, etc.) can use it to call `validate_brief`, `validate_evidence`, `score_output`, and related tools as part of the agent loop.

Pattern:

1. Agent uses Global Think Tank Analyst as its system / project instruction.
2. Agent drafts the memo.
3. Agent serializes the brief into JSON (Recipe B mapping).
4. Agent calls `validate_brief` and `score_output` via MCP.
5. If validation fails or the score is too low, the agent re-drafts with the gap explicitly named.

For exact MCP setup, see the [Agenda Intelligence MD integrations docs](https://github.com/vassiliylakhonin/agenda-intelligence-md/tree/main/docs/integrations).

## Honest limits of this composition

- Neither tool verifies factual truth. The composition catches *structural* and *evidence-discipline* failures, not *factual* failures.
- The `agenda-brief.schema.json` is narrower than a full Global Think Tank Analyst memo. Validating the JSON projection is not the same as validating the memo.
- The score is heuristic. Treat it as a smoke-test signal, not as a quality grade you can publish.
- Agenda Intelligence MD's CLI surface evolves on its own schedule. Re-check `agenda-intelligence --help` for current commands.
- Neither tool replaces qualified review for legal, compliance, sanctions, or investment decisions.

## See also

- [Agenda Intelligence MD on GitHub](https://github.com/vassiliylakhonin/agenda-intelligence-md)
- [`SKILL.md`](../../SKILL.md) — canonical skill behavior
- [`AGENTS.md`](../../AGENTS.md) — project rules
- [`evals/`](../../evals/) — human review checklist, failure modes, starter rubric
