# Definition of done

GTTA has no single finish line. “Done” depends on the claim being made. The
three maturity axes are defined in [`maturity-framework.md`](maturity-framework.md),
and the current evidence is recorded in [`STATUS.md`](../STATUS.md).

## Claim gates

| Intended claim or action | Minimum evidence | Not required |
|---|---|---|
| Merge a method or runtime change | Tests for the changed interface, repository checks, documentation, and no unexplained compatibility break | Practitioner review |
| Publish a GitHub release candidate | R2 and M2 | Positive eval delta; practitioner review |
| Publish a stable package through the declared channel | R3 and M2 | Practitioner review |
| Say the method improves structural discipline | M3, with the model/settings, cases, scorer, result, and limitations disclosed | Practitioner review, if the claim remains structural |
| Say practitioners find the workflow useful | U2 and the exact review scope stated | A benchmark score |
| Say the workflow is production-proven or operationally reliable | U3 plus system-specific safety and operational evidence outside this repository | Nothing currently in this repo is sufficient |

Passing `gtta check-contract` or `gtta check-artifact` means only that the
declared structure conforms. It is never evidence that claims are true or that
the memo is safe to use without review.

## Merge checklist for executable contract changes

- The public interface is versioned and documented.
- New invariants have positive and negative regression tests.
- CLI and MCP adapters use the same implementation rather than copying rules.
- The built-wheel smoke test exercises the installed interface.
- Rule severity and compatibility follow
  [`contract-release-criteria.md`](contract-release-criteria.md).
- `STATUS.md` changes only when committed evidence changes.

## Deferred external review

Lack of access to practitioners is a declared `U0` constraint, not a hidden
project blocker. Work may continue on R and M. Until external records exist,
the repository must not describe itself as practitioner-validated, production
proven, or operationally reliable.
