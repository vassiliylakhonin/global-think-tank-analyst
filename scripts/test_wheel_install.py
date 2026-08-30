#!/usr/bin/env python3
"""Smoke-test the built wheel as an installed artifact, outside the repo."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    wheels = sorted((ROOT / "dist").glob("global_think_tank_analyst-*.whl"))
    if len(wheels) != 1:
        return fail(f"expected exactly one wheel under dist/, found {len(wheels)}")

    with tempfile.TemporaryDirectory(prefix="gtta-wheel-smoke-") as temp_dir:
        temp = Path(temp_dir)
        target = temp / "site-packages"
        target.mkdir()
        with ZipFile(wheels[0]) as archive:
            archive.extractall(target)

        probe = """
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import gtta
from gtta.resources import get_mode_template, get_skill_prompt
assert Path(gtta.__file__).is_relative_to(Path(sys.argv[1])), gtta.__file__
en = get_skill_prompt('en')
ru = get_skill_prompt('ru')
assert len(en) > 20_000, len(en)
assert len(ru) > 5_000, len(ru)
assert 'Mode G' in get_mode_template('G')
from gtta.mcp_server import app as mcp_app
assert {tool.name for tool in asyncio.run(mcp_app.list_tools())} == {
    'check_memo_contract', 'get_mode_template', 'get_skill_prompt'
}
from typer.testing import CliRunner
from gtta.cli import app as cli_app
result = CliRunner().invoke(cli_app, ['new', '--mode', 'G', '--topic', 'Probe'])
assert result.exit_code == 0, result.output
assert 'Competing Hypotheses' in result.output
from gtta.discipline import check_contract
valid_memo = 'Evidence mode: reasoning-only\\n[analyst-judgment] Draft.\\nModerate confidence.'
assert check_contract(valid_memo).passed
checked = CliRunner().invoke(cli_app, ['check-contract', '-', '--json'], input=valid_memo)
assert checked.exit_code == 0, checked.output
print('ok: installed wheel exposes complete resources, CLI, and MCP tools')
"""
        completed = subprocess.run(
            [sys.executable, "-c", probe, str(target)],
            cwd=temp,
            env={**os.environ, "PYTHONPATH": ""},
            text=True,
        )
        return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
