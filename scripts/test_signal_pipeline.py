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
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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


WORKING_FEED = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>Example</title>
<item><title>Working item</title><link>https://good.example/1</link>
<description>Summary text.</description><pubDate>Mon, 05 Jan 2026 00:00:00 GMT</pubDate></item>
</channel></rss>
"""

SOFT_404 = b"<!DOCTYPE html><html><head><title>Page not found</title></head><body>404</body></html>"


@contextlib.contextmanager
def sources_config(entries):
    """Point the generator at a temporary sources.json."""
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "sources.json"
        path.write_text(json.dumps({"sources": entries}), encoding="utf-8")
        saved = generator.SOURCES_PATH
        generator.SOURCES_PATH = path
        try:
            yield path
        finally:
            generator.SOURCES_PATH = saved


def fake_fetch(url, timeout=20):
    if "good.example" in url:
        return WORKING_FEED
    if "soft404.example" in url:
        return SOFT_404
    raise OSError("connection refused")


class CollectSnippets(unittest.TestCase):
    """The generator must never pass fetch errors to the model as evidence.

    Regression test for the defect where an empty or failed source set was
    appended to the prompt as "SOURCE FETCH NOTES" and sent to the model with
    evidence mode `live-source-backed`.
    """

    def test_all_sources_failing_returns_no_snippets(self):
        entries = [
            {"name": "Dead A", "url": "https://deada.example/feed", "focus": "x"},
            {"name": "Dead B", "url": "https://deadb.example/feed", "focus": "y"},
        ]
        with sources_config(entries):
            with mock.patch.object(generator, "fetch_url", side_effect=fake_fetch):
                snippets, failures = generator.collect_snippets()
        self.assertEqual(snippets, "")
        self.assertEqual(len(failures), 2)
        self.assertNotIn("SOURCE FETCH NOTES", snippets)

    def test_partial_failure_keeps_errors_out_of_snippets(self):
        entries = [
            {"name": "Good Source", "url": "https://good.example/feed", "focus": "x"},
            {"name": "Dead Source", "url": "https://dead.example/feed", "focus": "y"},
        ]
        with sources_config(entries):
            with mock.patch.object(generator, "fetch_url", side_effect=fake_fetch):
                snippets, failures = generator.collect_snippets()
        self.assertIn("SOURCE: Good Source", snippets)
        self.assertNotIn("Dead Source", snippets)
        self.assertEqual(len(failures), 1)
        self.assertIn("Dead Source", failures[0])

    def test_soft_404_html_counts_as_failure(self):
        entries = [{"name": "Soft404", "url": "https://soft404.example/feed", "focus": "x"}]
        with sources_config(entries):
            with mock.patch.object(generator, "fetch_url", side_effect=fake_fetch):
                snippets, failures = generator.collect_snippets()
        self.assertEqual(snippets, "")
        self.assertEqual(len(failures), 1)

    def test_disabled_sources_are_skipped(self):
        entries = [
            {"name": "Good Source", "url": "https://good.example/feed", "focus": "x"},
            {"name": "Dead Source", "url": "https://dead.example/feed", "focus": "y",
             "enabled": False, "disabled_reason": "404"},
        ]
        with sources_config(entries):
            with mock.patch.object(generator, "fetch_url", side_effect=fake_fetch):
                snippets, failures = generator.collect_snippets()
        self.assertIn("SOURCE: Good Source", snippets)
        self.assertEqual(failures, [])


class GenerationRefusal(unittest.TestCase):
    """main() refuses to draft a live-source-backed signal on empty or partial evidence."""

    def run_main(self):
        with mock.patch.object(sys, "argv", ["generate_policy_risk_signal.py", "--dry-run"]):
            with mock.patch.object(generator, "fetch_url", side_effect=fake_fetch):
                generator.main()

    def test_refuses_when_no_source_produces_snippets(self):
        entries = [{"name": "Dead A", "url": "https://deada.example/feed", "focus": "x"}]
        with sources_config(entries):
            with self.assertRaises(SystemExit) as caught:
                self.run_main()
        self.assertIn("no live evidence", str(caught.exception))

    def test_refuses_on_partial_evidence(self):
        entries = [
            {"name": "Good Source", "url": "https://good.example/feed", "focus": "x"},
            {"name": "Dead Source", "url": "https://dead.example/feed", "focus": "y"},
        ]
        with sources_config(entries):
            with self.assertRaises(SystemExit) as caught:
                self.run_main()
        message = str(caught.exception)
        self.assertIn("Partial evidence", message)
        self.assertIn("Dead Source", message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
