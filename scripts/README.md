# scripts/

Development and CI helper scripts. Not part of the published skill.

| Script | Purpose | Used in CI |
|---|---|---|
| `validate_signals.py` | 4-file consistency check across signals/ (index, feed, latest, individual signal) | Yes |
| `validate_examples.py` | Evidence-mode and retrieval-date discipline for examples/ | Yes |
| `validate_json.py` | Parse-check all repository JSON files | Yes |
| `generate_policy_risk_signal.py` | Automated weekly policy-risk signal generation (OpenAI API, opens PR) | Yes (scheduled workflow) |
