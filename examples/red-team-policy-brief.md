# Red-team policy brief (illustrative)

> **Illustrative example.** Evidence mode: `reasoning-only`. No live sources were checked.

**User question:** Red-team the claim that supply-chain sanctions risk for our European technology firm is "manageable."

```text
Question: Stress-test the claim that supply-chain sanctions risk is manageable.
Decision: Whether the executive team should accept the current risk posture.
Audience: Board risk committee.
Time horizon: 12 months.
Evidence mode: reasoning-only.
```

EVIDENCE ACCESS LIMITED: no live verification performed in this environment.

## Target claim

> "Supply-chain sanctions risk is manageable. Our partners are diligent, our SKUs are non-sensitive, and exposure is limited to a small share of revenue."

## Strongest reasons it may be wrong

1. **[inference] Diligence is partner-attested, not partner-tested.** Most "diligent" claims rely on supplier self-certification rather than independent or stress-tested verification. A single compromised distributor in a corridor can change the picture.
2. **"Non-sensitive" SKUs migrate.** Dual-use list scope is a moving target. SKUs considered non-sensitive at design-in can be added to controlled lists during a product's commercial life.
3. **[inference] Revenue share understates blast radius.** A small revenue share can produce a disproportionate reputational and regulatory blast: investigations consume executive bandwidth and trigger correspondent-bank caution across unrelated geographies.
4. **Concentration risk hidden in payment rails.** Multiple "different" partners may share one or two correspondent banks. A single bank action can cascade.
5. **Time-of-check is wrong.** Risk is being judged against today's designations, not against the rate of new designations relevant to the firm's corridors.

## Alternative explanations for current calm

- The firm's operations are below the priority threshold for enforcement — *for now*.
- Comparable peers have not yet been named, suppressing the visible base rate.
- Recent absence of incidents reflects favorable enforcement cycle, not robust controls.

## Missing assumptions in the claim

- That partner KYC is comparable in quality to the firm's own KYC.
- That dual-use list composition is approximately stable.
- That "limited revenue share" is the right risk denominator (it isn't — operational disruption is).
- That secondary effects via banks are out of scope.

## Evidence that would strengthen the claim

- Independent third-party audit results on top distributors.
- Mapping of payment rails to correspondent banks, with concentration measured.
- Documented stress test against scenarios where 1–2 named designations cascade.
- Continuous monitoring of designation cadence relevant to the corridor.

## Evidence that would weaken the claim

- A peer firm enforcement action in the same corridor.
- New dual-use list additions covering SKU families currently considered non-sensitive.
- Correspondent-bank inquiry letters or enhanced-due-diligence escalation.

## Revised judgment

[analyst-judgment] The claim "manageable" is defensible **only with caveats** that the original framing omits. A more honest version:

> "Sanctions exposure is currently *contained at the visible perimeter*, but is undermeasured in two places: (a) correspondent-bank concentration and (b) the rate of dual-use list change. Without those measurements, 'manageable' is a posture, not a finding."

## Watch-next indicators

- Peer enforcement actions.
- Correspondent-bank EDD requests.
- New designations affecting the corridor.
- Dual-use list updates touching SKU families.

## Confidence

**Confidence: Moderate.** The red-team logic is internally coherent, but the evidence mode is reasoning-only and no firm-specific controls, vendors, or payment data were tested.

## Limitations

Reasoning-only and illustrative. Not legal or compliance advice.
