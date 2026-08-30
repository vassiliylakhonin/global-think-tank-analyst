# Maturity framework

GTTA reports maturity as three independent coordinates. A single bar was
misleading because a package can be releasable without practitioner evidence,
and practitioner enthusiasm cannot prove that a build is reproducible.

The current coordinates and supporting evidence live in [`STATUS.md`](../STATUS.md).
The claim-specific gates live in
[`definition-of-done.md`](definition-of-done.md).

## R — release readiness

| Level | Meaning |
|---|---|
| R0 | Source exists, but no repeatable package or automated gate exists. |
| R1 | Package builds locally and automated source tests exist. |
| R2 | A versioned release candidate is built, smoke-tested as an installed artifact, published on GitHub, and covered by green CI. |
| R3 | The package is installable from its declared public channel through a reproducible, authenticated release workflow. |

R measures distribution integrity. It does not say that the analytical method
improves output or that practitioners find it useful.

## M — method evidence

| Level | Meaning |
|---|---|
| M0 | The method is prose-only and has no explicit testable contract. |
| M1 | Rules, examples, and failure modes are explicit, but conformance is mostly manual. |
| M2 | A versioned deterministic contract, structured artifact, regression tests, and a predeclared paired evaluation set exist. No positive quality delta is implied. |
| M3 | A disclosed same-task baseline/skill evaluation has been executed under controlled settings and supports a bounded, predeclared structural-improvement claim. Results and limitations are published. |

M measures evidence about observable method behavior. Deterministic checks can
establish structure and declaration coverage; they cannot establish factual
truth, source adequacy, or decision quality.

## U — external usefulness evidence

| Level | Meaning |
|---|---|
| U0 | No attributable external practitioner review is recorded. |
| U1 | One relevant external practitioner has reviewed a complete case packet and the response is recorded with consent. |
| U2 | At least two independent relevant practitioners have reviewed case packets; recurring findings and resulting changes are recorded. |
| U3 | Evidence exists from repeated real workflows over time, including known failures and revisions. |

U measures whether the workflow appears useful to people doing relevant work.
Author self-review, LLM feedback, stars, downloads, and CI do not raise U.

## Why GTTA no longer uses Bar 1 / Bar 2

The vertical-specialist sibling repositories may retain their own Bar 1 / Bar 2
criteria. Those bars combine source depth, specialist examples, and validation
in ways suited to those repositories. Transplanting them here obscured the
difference between shipping software, testing a horizontal reasoning method,
and obtaining external feedback.

Within GTTA, unqualified `Bar 1`, `Bar 2`, and “the canon” language is retired.
Portfolio comparisons must name the repository and its native framework rather
than map one score onto another.
