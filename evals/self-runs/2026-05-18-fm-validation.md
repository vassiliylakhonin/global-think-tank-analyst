# Self-run — FM-A / FM-B fresh-context validation

**Date:** 2026-05-18
**Runner:** project author (Vassiliy Lakhonin), via four parallel Claude subagent runs and two parallel critic-test runs.
**Purpose:** Satisfy decision gates in [`../self-critique-draft.md`](../self-critique-draft.md) for two observed failure modes before deciding whether to integrate the proposed critic addition into `SKILL.md`.
**Status:** **AUTHOR SELF-REVIEW. NOT EXTERNAL VALIDATION.** See [`README.md`](README.md) and [`../../VALIDATION_PLAN.md`](../../VALIDATION_PLAN.md).

---

## 1. Setup

Six total fresh-context runs were executed against the published skill files (`AGENTS.md` + `SKILL.md`), in parallel subagents with no shared conversation history:

| Run | FM under test | Critic applied | Mode | Prompt domain |
|---|---|---|---|---|
| A1 | FM-A (table-cell tag drift) | No | E (Decision Briefing Pack) | UAE electronics distributor, Iran-linked sanctions |
| A2 | FM-A | No | E | Same prompt as A1 |
| B1 | FM-B (ceremonial Rule 2 vs Step 5) | No | B (Standard Memo) | Kazakh metals exporter, CBAM revenue-vs-barrier question |
| B2 | FM-B | No | B | Same prompt as B1 |
| AC1 | FM-A | Yes (proposed critic bullet appended to self-check) | E | Same as A1 |
| AC2 | FM-A | Yes (same critic) | E | Same as A1 |

Prompts were designed to maximally surface each FM:
- **For FM-A**: Mode E with explicit demand for full options table, risk register, actor incentives table, watchlist, and per-claim provenance tags. Five-plus tables in the output, with strong layout pressure to compress per-cell tags.
- **For FM-B**: Question framed with two plausible interpretive frames (revenue instrument vs softenable trade barrier), explicit user request to commit to a primary view and present the alternative — direct invitation for the agent to either apply Workflow Step 5 (correct) or hedge via Rule 2 on both interpretations (FM-B).

## 2. Results

### FM-A — table-cell provenance tag drift

| Run | Tables produced | Per-cell tags present | Bulk-attribution used | Verdict |
|---|---|---|---|---|
| A1 (no critic) | 6 | 2/6 (Risks, Options) | 3/6 (Decision Map, Actors, Scenarios — footnoted "all cells: [analyst-judgment]") | **Partial reproduction.** Agent aware of rule, compensates with bulk-attribution. |
| A2 (no critic) | 5 | 1/5 (Actors, partial) | 0/5 | **Full reproduction.** Tags dropped from Decision Map, Risks, Options, Risk Register entirely. |
| AC1 (with critic) | 6 | 6/6 (introduced explicit "Provenance" column in each table) | 0/6 | **Critic resolved.** Per-row tags present; no bulk-attribution. |
| AC2 (with critic) | 4 | 4/4 (per-row, some per-cell) | 0/4 | **Critic resolved.** Less consistent than AC1 but no failure-mode reproduction. |

**FM-A reproduction rate (no critic): 2/2 fresh-context observations** (one partial, one full). Memory entry [`project_canon_rule_failure_modes_observed.md`] is confirmed and strengthened: FM-A is real and stable across fresh-context runs.

**Critic-resolution rate: 2/2.** The proposed self-check bullet for FM-A resolves the failure in both observations. Agents converged independently on adding a dedicated "Provenance" column to each table, which is a defensible design choice.

**Length impact:** No material inflation. AC1 ≈ 5500 words vs A2 baseline ≈ 5800 words. AC2 ≈ 5600 words. Both critic runs are within ±5% of baseline length. Negative-test condition (no regression on length) is met.

### FM-B — ceremonial Rule 2 application where Workflow Step 5 was correct

| Run | Two interpretive frames presented | Primary view committed | Rule 2 ("Flag-but-don't-use") used | Verdict |
|---|---|---|---|---|
| B1 (no critic) | Yes | Yes — "CBAM is a hardening non-revenue trade barrier" with explicit "Why the primary view still wins for this decision" | No | **No reproduction.** Clean Step 5 application. |
| B2 (no critic) | Yes | Yes — "CBAM functions primarily as a non-revenue trade barrier with growing fiscal-instrument characteristics", primary view explicitly preferred over alternative | No | **No reproduction.** Clean Step 5 application. |

**FM-B reproduction rate (no critic): 0/2 fresh-context observations.** Current canon already prevents FM-B in fresh context. Both agents committed to a primary view with named alternative, exactly as Workflow Step 5 prescribes.

The two prior floor-test observations noted in memory may have been produced under different conditions (longer conversation history, user pressure, different model state, pre-source-conflict-rule canon). Whatever caused them, the failure mode does not reproduce against the current `SKILL.md` in fresh context.

## 3. Decision-gate status (per `self-critique-draft.md` §5)

| Gate | Status | Notes |
|---|---|---|
| 1. Original floor-test prompts/outputs located | ❌ Cannot satisfy | Floor-test artifacts not stored in repo; treat as an unresolved limitation, not a blocker, because the fresh-context evidence is independent. |
| 2. Two additional fresh-context reproductions of FM-A | ✅ Met | A1 partial + A2 full. |
| 2. Two additional fresh-context reproductions of FM-B | ❌ Not met (0/2) | FM-B does not reproduce. |
| 3. Critic resolves FM-A | ✅ Met | AC1 and AC2 both show per-row/per-cell tags restored, no bulk-attribution. |
| 3. Critic resolves FM-B | N/A | FM-B not reproduced; no failure for the critic to resolve. |
| 4. Negative test — no spurious rewrites, no length inflation >5% | ✅ Met | Critic runs are within ±5% of baseline length and do not appear to over-correct. |

## 4. Integration decision

- **FM-A self-check bullet → INTEGRATE into `SKILL.md`.** Evidence supports it: two reproductions without critic, two resolutions with critic, no length regression.
- **FM-B self-check bullet → DO NOT INTEGRATE.** The failure mode does not reproduce in fresh context against current canon. Adding a critic for a non-reproducing FM would add token cost without observed benefit. If FM-B is observed again in a future floor-test, re-open this analysis with that prompt/output captured.

## 5. What this self-run does and does not establish

**Does establish:**
- FM-A is real, reproduces in fresh context against current canon, and the proposed critic resolves it without length inflation. Justifies integration.
- FM-B does not reproduce in fresh context against current canon. Justifies non-integration pending new evidence.

**Does not establish:**
- That FM-A reproduces across other models (only Claude was tested).
- That FM-A reproduces across all memo modes (only Mode E was tested; Mode B with one risk table might or might not show the same pattern).
- That FM-B has been ruled out under all conditions — only in fresh single-turn context with this specific prompt structure.
- External validity. This is the project author running tests; treat as engineering self-test, not as evidence of cross-reviewer robustness.

## 6. Honesty notes

- Six subagent runs in one session is not a labeled benchmark. It is a small, structured engineering test designed to satisfy named decision gates the author had written down in advance.
- Per-FM sample size is two without critic and two with critic. Two is the minimum the draft asks for. It is also a small sample for any statistical claim, which is why no statistical claim is made here.
- The author wrote the draft, the prompts, and the analysis. Confirmation bias is a real concern; mitigation here is that the FM-B negative result (which the author did not predict in advance and which contradicts the draft's symmetric framing of the two FMs) was kept, not edited out.
