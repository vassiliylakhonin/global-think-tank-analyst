# Policy Risk Signal — YYYY-MM-DD

<!-- title: short title under 80 chars -->

> Template. Copy this file to `signals/YYYY/YYYY-MM-DD.md` (or
> `YYYY-MM-DD-<topic>.md` if multiple signals fall on the same day) and replace
> the heading date and the `title` marker above.
>
> The `<!-- title: ... -->` marker is not decoration: `signals/index.json`,
> `signals/feed.json`, and `signals/latest.md` are built from it, and
> `scripts/validate_signals.py` fails CI when the recorded title does not appear
> verbatim in the signal. Run `python3 scripts/validate_signals.py` before
> opening the pull request.

```text
Date: YYYY-MM-DD
Domain: [sanctions / trade / regulatory / geopolitical / strategic]
Region: [country / corridor / market]
Evidence mode: live-source-backed / user-provided sources / illustrative source packet / reasoning-only
Confidence: Low / Moderate / High
```

## Signal

What happened, in 2–4 sentences. Be specific. No decoration. Every signal in the
archive uses this heading; the generator in
`scripts/generate_policy_risk_signal.py` requires it.

## Why it matters

The decision context this signal touches. Who would care, and why.

## Signal vs noise

What makes this a *signal* and not just news. Why this event is informative beyond the immediate headline.

## Who gains leverage

Actors whose options expand because of this event.

## Who loses leverage

Actors whose options narrow.

## Key uncertainty

The single most important unresolved question that this signal does not answer.

## Scenarios (if useful)

- Baseline: …
- Alternative: …
- Disconfirming: …

## Watch next

Concrete, observable indicators that would update the picture. Not "monitor closely."

## Sources

If `live-source-backed` or `user-provided sources`, list the sources actually used here. If `illustrative source packet`, label the constructed packet. If `reasoning-only`, write:

> No live sources were checked for this signal.

## Confidence and limitations

Why the confidence level, and what would raise or lower it.

## What would change the judgment

Specific evidence whose appearance would force a re-write of the signal.

## Disclaimer

Public example of the Global Think Tank Analyst skill style. Not official intelligence. Not legal, compliance, sanctions, or investment advice.
