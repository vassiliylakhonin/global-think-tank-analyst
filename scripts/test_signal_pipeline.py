#!/usr/bin/env python3
"""Unit tests for the signal pipeline: generator output must satisfy the validator.

The generator writes signals/index.json, signals/feed.json, and signals/latest.md;
scripts/validate_signals.py then rejects the result if any of them disagrees with
the markdown. Nothing used to check that agreement before a pull request was open,
and two defects lived in that gap: a title that was normalized out of the source
file, and a second run on one date overwriting the first signal.

These tests run the generator's index builders and the validator against a
throwaway tree, so a regression fails locally and in CI instead of in the weekly
automated pull request.
"""

from __future__ import annotations

import contextlib
import importlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

generator = importlib.import_module("generate_policy_risk_signal")
validator = importlib.import_module("validate_signals")


SIGNAL_TEMPLATE = """# Policy Risk Signal — {date}

<!-- title: {title} -->

```text
Date: {date}
Domain: sanctions
Region: EU
Evidence mode: reasoning-only
Confidence: Moderate
```

## Signal

Body text.

## Sources

No live sources were checked for this signal.
"""


@contextlib.contextmanager
def signal_tree():
    """Point both modules at a temporary repository root."""
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)
        signals = root / "signals"
        (signals / "2026").mkdir(parents=True)
        saved = {}

        def repoint(module, **values):
            saved[module] = {key: getattr(module, key) for key in values}
            for key, value in values.items():
                setattr(module, key, value)

        repoint(
            generator,
            ROOT=root,
            SIGNALS_DIR=signals,
            ARCHIVE_PATH=signals / "README.md",
            LATEST_PATH=signals / "latest.md",
            INDEX_JSON_PATH=signals / "index.json",
            FEED_JSON_PATH=signals / "feed.json",
        )
        repoint(validator, ROOT=root, SIGNALS_DIR=signals)
        try:
            yield root, signals
        finally:
            for module, values in saved.items():
                for key, value in values.items():
                    setattr(module, key, value)


def write_signal(signals: Path, name: str, date: str, title: str) -> str:
    path = signals / "2026" / name
    path.write_text(SIGNAL_TEMPLATE.format(date=date, title=title), encoding="utf-8")
    return f"signals/2026/{name}"


class TitleMarker(unittest.TestCase):
    def test_returns_marker_verbatim(self):
        markdown = SIGNAL_TEMPLATE.format(date="2026-01-05", title="Ownership is the gate")
        self.assertEqual(generator.signal_title(markdown), "Ownership is the gate")

    def test_missing_marker_is_a_named_failure(self):
        markdown = "# Policy Risk Signal — 2026-01-05\n\n## Signal\n\nA sentence. Another.\n"
        with self.assertRaises(SystemExit) as caught:
            generator.signal_title(markdown, source="signals/2026/x.md")
        self.assertIn("signals/2026/x.md", str(caught.exception))
        self.assertIn("title", str(caught.exception))

    def test_over_long_marker_is_rejected(self):
        long_title = "x" * (generator.TITLE_LIMIT + 1)
        markdown = SIGNAL_TEMPLATE.format(date="2026-01-05", title=long_title)
        with self.assertRaises(SystemExit):
            generator.signal_title(markdown)


class OutputPath(unittest.TestCase):
    def test_first_signal_of_the_day_keeps_the_plain_name(self):
        with signal_tree() as (_, signals):
            path = generator.signal_path(signals / "2026", "2026-01-05", "Some title")
            self.assertEqual(path.name, "2026-01-05.md")

    def test_second_signal_of_the_day_gets_a_topic_suffix(self):
        with signal_tree() as (_, signals):
            write_signal(signals, "2026-01-05.md", "2026-01-05", "First")
            path = generator.signal_path(signals / "2026", "2026-01-05", "Ownership is the gate")
            self.assertEqual(path.name, "2026-01-05-ownership-is-the-gate.md")

    def test_repeated_topic_does_not_overwrite(self):
        with signal_tree() as (_, signals):
            write_signal(signals, "2026-01-05.md", "2026-01-05", "First")
            write_signal(signals, "2026-01-05-topic.md", "2026-01-05", "Topic")
            path = generator.signal_path(signals / "2026", "2026-01-05", "Topic")
            self.assertEqual(path.name, "2026-01-05-topic-2.md")


class GeneratedArchivePassesValidation(unittest.TestCase):
    def build(self, signals, entries):
        for name, date, title in entries:
            rel = write_signal(signals, name, date, title)
            generator.update_archive(date, rel, title)
        generator.update_agent_indexes()

    def validate(self):
        """Run the validator, keeping its success line out of the test output."""
        with contextlib.redirect_stdout(io.StringIO()):
            validator.main()

    def test_single_signal(self):
        with signal_tree() as (_, signals):
            self.build(signals, [("2026-01-05.md", "2026-01-05", "Ownership is the gate")])
            self.validate()

    def test_two_signals_sharing_a_date(self):
        with signal_tree() as (_, signals):
            self.build(
                signals,
                [
                    ("2026-01-05.md", "2026-01-05", "First title"),
                    ("2026-01-05-second.md", "2026-01-05", "Second title"),
                ],
            )
            self.validate()

    def test_title_with_markup_characters_stays_verbatim(self):
        # An earlier version ran the marker through html.unescape() and whitespace
        # collapsing, so a title like this stopped matching its own source file.
        with signal_tree() as (_, signals):
            self.build(signals, [("2026-01-05.md", "2026-01-05", "Tariffs &amp; quotas: the binding gate")])
            self.validate()


if __name__ == "__main__":
    unittest.main(verbosity=2)
