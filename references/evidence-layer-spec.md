# Evidence Layer Spec

## Required per key claim
- `claim_id`
- `claim_text`
- `source_url`
- `source_title`
- `source_date` (YYYY-MM-DD)
- `source_type` (official/report/research/media/other)
- `reliability_score` (1-5)
- `confidence_impact` (low/medium/high)

## Rules
1. No key claim without evidence pointer.
2. If evidence is weak, mark explicitly and lower confidence.
3. Distinguish observed fact vs inference.
4. Include data freshness note for time-sensitive topics.

## Output block
```json
{
  "evidence_note": [
    {
      "claim_id": "C1",
      "source_url": "https://...",
      "source_date": "2026-04-10",
      "reliability_score": 4
    }
  ]
}
```
