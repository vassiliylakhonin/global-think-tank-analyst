# scripts/

Development and CI helper scripts. Not part of the published skill.

| Script | Purpose | Used in CI |
|---|---|---|
| `check.py` | Run every supported repository check through one command | Yes |
| `validate_skill_package.py` | Guard skill discovery fields, the canonical symlink, and synchronized plugin manifests | Yes |
| `validate_signals.py` | 4-file consistency check across signals/ (index, feed, latest, individual signal) | Yes |
| `validate_examples.py` | Evidence-mode and retrieval-date discipline for examples/ | Yes |
| `validate_json.py` | Parse-check all repository JSON files | Yes |
| `validate_evidence_packet_handoff.py` | Validate the synthetic claim/source packet and primary Agenda composition language | Yes |
| `validate_codex_sync.py` | Guard shared-section sync between canonical and Codex skill files | Yes |
| `check_markdown_links.py` | Validate local Markdown targets and known author-site links | Yes |
| `generate_policy_risk_signal.py` | Automated weekly policy-risk signal generation (OpenAI API, opens PR) | Yes (scheduled workflow) |

Run the same checks as CI from the repository root:

```bash
python3 scripts/check.py
```

`validate_skill_package.py` checks repository-owned packaging invariants. It is
not a complete implementation of the Agent Skills or Agent Plugins schemas.
