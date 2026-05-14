# Review Records

This directory is reserved for external practitioner review records.

It is currently a scaffold. It does not contain completed external reviews and
does not claim external validation.

## What Belongs Here

Add a record only after a real domain practitioner has reviewed a case packet
and has given explicit permission for the chosen attribution level.

A review record should capture:

- case packet reviewed;
- reviewer role or relevant expertise;
- review date;
- attribution level;
- publication permission;
- verdict;
- strongest findings;
- required revisions;
- maintainer response.

## What Does Not Belong Here

Do not add:

- self-reviews by the author;
- LLM-generated praise or critique presented as external validation;
- private feedback without permission to publish;
- marketing testimonials;
- benchmark scores unless a real benchmark exists;
- customer, counterparty, transaction, or personal data.

## Attribution Levels

Use the most conservative level the reviewer permits:

- `public-name` - reviewer agrees to be named publicly.
- `role-only` - reviewer agrees to role / expertise attribution only.
- `anonymized` - reviewer agrees to anonymized public summary.
- `private` - do not publish the review record.

If the allowed level is `private`, do not commit the review record.

## File Naming

Use stable, descriptive names:

```text
reviews/YYYY-MM-DD-case-slug-reviewer-scope.md
```

Example:

```text
reviews/2026-06-15-central-asia-fintech-risk-role-only.md
```

Do not include private names, organizations, or sensitive identifiers in the
filename unless the reviewer explicitly approved public attribution.

## Current Status

No completed external reviews are stored in this directory.

Use [TEMPLATE.md](TEMPLATE.md) for future records.

