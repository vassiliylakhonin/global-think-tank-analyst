# Repository conventions

Contributor-facing conventions for this repo: README structure, what examples must show, how eval docs must be labelled (including the self-scoring honesty rule), and how signals are described.

Referenced from `AGENTS.md`.

## Recommended README structure

1. One-line positioning
2. Try this prompt
3. What it does
4. What it is not
5. Portfolio: how this skill composes
6. Integration status
7. Quick usage
8. Memo modes
9. Before / after
10. Examples
11. Evaluation
12. Signal archive
13. How to consume signals
14. Agent-readable endpoints
15. Naming
16. Repository structure
17. Limitations
18. Roadmap

## Examples

Examples should show:
- user question
- evidence mode
- decision context
- key judgment
- facts vs assessments
- assumptions
- uncertainty
- actor incentives / leverage
- scenarios
- options / trade-offs
- watch-next indicators
- confidence
- what would change the judgment

Examples should be navigable as a learning path, not only as a file list.

## Eval docs

Eval docs should be lightweight and honest.

Use terms like:
- review checklist
- starter rubric
- failure modes

Do not call it a validated benchmark unless benchmark cases and results actually exist.

When the downstream consumer of this skill is an AI agent, the most honest method-level validation is an **agent-eval**: same model, same question, with and without the skill attached, scored against a binary structural rubric. Existing `analyze` / MCP cases remain compatibility evidence for the older strategic-intelligence runtime; they do not validate the current evidence-packet linter. Use method-level evals in addition to (not instead of) human review when the downstream audience also includes domain practitioners.

**Self-scoring honesty:** when the author or the same model family scores an agent-eval, treat the result as a structural sanity check, not validation. Same-family judges exhibit self-preference bias and can mark binary rubric criteria "satisfied" substantially more often than a neutral judge would — even on objective criteria. This is now measured, not just suspected: on programmatically verifiable rubrics, judges were up to 50% more likely to incorrectly mark a failed criterion as satisfied when the output was their own (arXiv:2604.06996). The same study found judge ensembles reduce but do not eliminate the bias, especially on negative rubrics and subjective criteria — so an ensemble is a mitigation to disclose, not a cure to rely on. Where the claim matters, score with a different model family or disclose the self-scoring limitation explicitly. Never present a self-scored delta as external or factual validation.

## Signals

Signals are distribution examples of the skill style, not official intelligence or real-time operational guidance.

When describing signals, make clear:
- how to read the latest signal
- where the archive index lives
- where the JSON Feed lives
- that any signal can be expanded into a deeper memo using its example expansion prompt
- that current facts and cited sources must be verified before operational use
