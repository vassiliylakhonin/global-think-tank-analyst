# Governance and Audit

## Mandatory controls
- Uncertainty policy: avoid deterministic language under weak evidence.
- Confidence policy: explain score and top uncertainty driver.
- Escalation policy: require expert review for high-stakes recommendations.

## Audit trail schema
- request_id
- agent_stage (collector/analyst/red-team/editor)
- generated_at
- key_claim_ids
- evidence_ids
- unresolved_disagreements
- final_verdict

## Review cadence
- Weekly: evaluate false confidence and evidence gaps.
- Monthly: rerun eval pack and update thresholds if drift observed.
