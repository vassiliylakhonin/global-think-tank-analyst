# scripts/

Development and CI helper scripts. Not part of the published skill.

| Script | Purpose | Used in CI |
|---|---|---|
| `check.py` | Run every supported repository check through one command | Yes |
| `validate_skill_package.py` | Guard skill discovery fields, the canonical symlink, and plugin manifests synchronized with each other and with the released version in `CHANGELOG.md` | Yes |
| `validate_runtime_resources.py` | Guard packaged EN/RU skill resources against drift from the root canon | Yes |
| `sync_runtime_resources.py` | Copy canonical skill files into the installable Python package | No (explicit build step) |
| `test_wheel_install.py` | Unpack the built wheel into an isolated import path and verify resources, CLI, contract checker, and MCP tools | Yes |
| `agent_eval.py` | Validate, prepare, import offline Antigravity responses, and score the 12-case paired structural agent-eval; it never calls a model API | Yes (case validation) |
| `validate_signals.py` | 4-file consistency check across signals/ (index, feed, latest, individual signal) | Yes |
| `test_signal_pipeline.py` | Unit tests: generator index output must satisfy `validate_signals.py` | Yes |
| `validate_examples.py` | Evidence-mode and retrieval-date discipline for examples/ | Yes |
| `validate_json.py` | Parse-check all repository JSON files | Yes |
| `validate_evidence_packet_handoff.py` | Validate the synthetic claim/source packet and primary Agenda composition language | Yes |
| `validate_codex_sync.py` | Guard shared-section sync between canonical and Codex skill files | Yes |
| `check_markdown_links.py` | Validate local Markdown targets and known author-site links | Yes |
| `generate_policy_risk_signal.py` | Draft a policy-risk signal from public feeds (OpenAI API, opens PR) | No (manual `workflow_dispatch` only) |

Run the same checks as CI from the repository root:

```bash
python3 scripts/check.py
```

`validate_skill_package.py` checks repository-owned packaging invariants. It is
not a complete implementation of the Agent Skills or Agent Plugins schemas.

For package changes, run the installed-artifact gate as well:

```bash
python3 -m pip install -e ".[test,mcp]"
python3 scripts/sync_runtime_resources.py
python3 -m build --wheel
python3 scripts/test_wheel_install.py
```
