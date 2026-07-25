# Research basis

This file records the published research that motivated specific canon and runtime rules in this skill. It is provenance for *why a rule exists*, not a literature review and not a claim that the skill implements any paper's method.

**Honesty note.** These references were identified from paper abstracts and search summaries, not from full readings of every PDF. arXiv IDs and dates should be confirmed against the source before citing externally. Nothing here is a benchmark result for this skill.

## Why these rules exist

| Canon / runtime rule | Motivating finding | Reference |
|---|---|---|
| **Tag faithfulness, not tag presence** (`docs/analysis-contract.md` → Per-claim provenance; `SKILL.md` self-check; failure mode 19) | Attributed answers frequently carry citations that look correct but do not support the claim; post-rationalization is prevalent and a large share of citations are unfaithful. Tag *presence* and tag *faithfulness* are different properties. | "Correctness is not Faithfulness in RAG Attributions" — arXiv:2412.18004; "Verified Misguidance: Measuring Structural Citation Failures in Search-Augmented LLMs" — arXiv:2605.28565 |
| **Verbalized-confidence calibration is checkable** (`docs/analysis-contract.md` → Linguistic faithfulness; failure mode 20) | LLMs systematically fail to make linguistic uncertainty markers track intrinsic confidence; faithful natural-language uncertainty is a measurable property, not a style preference. | "MetaFaith: Faithful Natural Language Uncertainty Expression in LLMs" — arXiv:2505.24858; "Can LLMs Use Linguistic Uncertainty Markers to Reliably Reflect Intrinsic Confidence?" — arXiv:2605.28778; "Are LLM Decisions Faithful to Verbal Confidence?" — arXiv:2601.07767 |
| **False-premise Stop-and-request trigger** (`SKILL.md` → Stop-and-request; failure mode 21) | Abstention benchmarks show false premises and underspecified/unanswerable questions as a distinct failure class that scaling does not solve; models should detect and refuse rather than analyze a bad premise. | "AbstentionBench: Reasoning LLMs Fail on Unanswerable Questions" — arXiv:2506.09038; "The Art of Refusal: A Survey of Abstention in LLMs" — arXiv:2407.18418 |
| **Mode G — Competing Hypotheses (ACH)** (`SKILL.md` → Memo modes; failure mode 22) | Evidence-first hypothesis tracking — maintain competing hypotheses, update plausibility, converge only after sufficient diagnostic evidence — improves robustness over single-hypothesis reasoning. Mirrors classic Analysis of Competing Hypotheses tradecraft. | "LLM-as-an-Investigator: Evidence-First Reasoning for Robust Interactive Problem Diagnosis" — arXiv:2606.13220; "LLM Augmentations to support Analytical Reasoning over Multiple Documents" — arXiv:2411.16116 |
| **Spotlighting / provenance separation for retrieved content** (`AGENTS.md` → Retrieved-content trust) | Inline concatenation of retrieved text gives indirect prompt injection no boundary; provenance-based instruction hierarchy and datamarking/spotlighting materially reduce attack success. | "A Layered Security Framework Against Prompt Injection in RAG-Based Chatbots" — arXiv:2606.19660; "Document-Authored Control-Signal Impersonation" — arXiv:2606.09005 |
| **Self-scoring honesty (SPB disclosure)** (`docs/repo-conventions.md` → Eval docs; `evals/rubric.md` calibration note) | LLM judges exhibit self-preference bias, marking rubric criteria "satisfied" substantially more often for their own model family — even on objective binary criteria. Self-scored agent-evals must not be presented as external validation. | "Self-Preference Bias in Rubric-Based Evaluation of LLMs" — arXiv:2604.06996; "Reliability without Validity: ... LLM-as-a-Judge ... Agreement, Consistency, and Bias" — arXiv:2606.19544 |

## What this is not

- Not a claim that this skill was evaluated with any of these methods.
- Not a benchmark, accuracy, or compliance-usefulness claim.
- Not a substitute for the honesty rules in `AGENTS.md`. If a future change cites a result here as evidence of skill quality, that is a misuse of this file.
