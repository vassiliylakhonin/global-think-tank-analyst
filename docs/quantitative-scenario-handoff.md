# Quantitative scenario handoff

Use this guidance when a memo relies on an external model's numerical outputs.
GTTA owns the decision framing and memo; the external model owns the arithmetic.
Loading a reasoning skill does not execute a calculation or verify its inputs.

## Minimum inspectable handoff

Preserve the model name, code revision, exact command or actual tool receipt,
input/output files and scenario identifiers. Separate observations, externally
forecast quantities, planning assumptions and calculated results. Retain the
original units, period, geography and source dates. Missing material provenance
is a memo limitation; do not invent a command, model run or source to fill it.

Give source-backed inputs their existing claim/source records. Treat outputs as
derived claims with links to their load-bearing inputs; in MemoArtifact, use
`basis_claim_ids` and the appropriate provenance. Input hashes establish which
file was used, not whether a source supports its contents. Deterministic results
inherit uncertainty from their inputs, even if the arithmetic is reproducible.

## Interpret scenario comparisons

- Keep scenario IDs stable across prose, tables and attachments. Identify both
  the changed inputs and what stayed fixed; multiple simultaneous changes do
  not identify which intervention caused the difference.
- Distinguish unmet demand, spare capacity and actual throughput. A capacity
  estimate is not a forecast of cargo that customers will actually ship.
- Compare the alternatives on the decision's objective. Additional nominal
  capacity may have no operational benefit if another constraint binds.
- Describe ranking reversals and binding constraints when material. Name the
  observation or input threshold that would change the preferred option; do not
  assign probabilities unless a defensible probability model is supplied.
- Keep a better scenario outcome distinct from an optimal solution. Comparing
  a few supplied alternatives does not establish a global optimum, feasibility,
  safety, financing eligibility or approval.

## Companion example and availability

When a Corridor Bankability Analyst checkout is available, its
`docs/maritime-capacity-model.md` describes directional vessel/port/rail capacity
scenarios. The companion is access-controlled; no public documentation URL or
automatic access is assumed. It remains optional;
use an inspectable alternative model or bounded qualitative analysis if it is
unavailable. Never claim that this companion ran without an actual result.

Reasoning skills can be composed without sharing a Python environment. If MCP
adapters are used, keep separate server environments: Corridor Bankability pins
MCP 1.x, whereas GTTA's optional MCP adapter and the Central Asia & Caspian
transport skeleton require MCP 2.x. The regional skeleton does not produce
screening findings. Do not resolve the dependency mismatch by weakening version
constraints without compatibility testing.
