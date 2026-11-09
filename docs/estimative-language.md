# Estimative probability language (optional)

This is an additive convention. It does not replace the Low / Moderate / High
confidence labels in the analysis contract, and no existing memo, benchmark or
published result changes because of it.

## Two separate things

ICD 203 separates two ideas that memos often blur:

- **Likelihood**: how probable the event or condition is. Expressed with a
  probability term, ideally with a number.
- **Confidence**: how well the evidence supports the judgment (source quality,
  corroboration, gaps, analyst disagreement). Expressed as Low / Moderate / High.

A memo may say "likely (about 70%), moderate confidence". Keep both.

## Term table

Terms and bands follow the ICD 203 (2015) estimative-language table
(<https://www.dni.gov/files/documents/ICD/ICD-203.pdf>). Use a term only for a
judgment about a future or unobserved event. Do not use it for facts.

| Term | Probability band |
|---|---|
| Almost no chance | 1-5% |
| Very unlikely | 5-20% |
| Unlikely | 20-45% |
| Roughly even chance | 45-55% |
| Likely | 55-80% |
| Very likely | 80-95% |
| Almost certain | 95-99% |

Rules:

1. When the claim is load-bearing, add a point value or a range inside the band
   ("likely, ~70%"). The term alone cannot be scored.
2. Use one term per judgment. Do not stack hedges ("could possibly likely").
3. Low / Moderate / High stays valid on its own. A numeric probability is
   optional, never required for a memo to pass.
4. A number is a judgment, not a measurement. Tie it to the evidence in the
   claim ledger, and say what would move it.

## Honest limit

No calibration is claimed. The forecast log in [`forecasts/`](../forecasts/README.md)
starts empty. Until enough forecasts resolve, probabilities in memos are
uncalibrated analyst judgments. Verbalized model confidence is known to be weakly
related to accuracy (see [`research-basis.md`](research-basis.md)), so treat model-generated
numbers with extra suspicion.
