"""Packaging invariants: the analytical method must survive `pip install`.

`gtta` version 1.4.0 shipped a wheel containing only Python modules. `SKILL.md`
lived at the repository root and was never packaged, while the prompt builders
resolved it with `Path(__file__).parent.parent.parent` and returned the string
"You are a strategic-risk analyst." when it was missing. Every installed copy
therefore ran on a 33-character stub, silently.

Tests that exercise the repository working tree cannot catch that: the file is
right there. Only a test that builds the distribution and reads it back can.
"""

import shutil
import subprocess
import sys
import venv
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MINIMUM_INSTALLED_METHOD_LENGTH = 20000


@pytest.fixture(scope="module")
def wheel(tmp_path_factory):
    """Build a real wheel from the repository."""
    pytest.importorskip("build", reason="`build` ships in the [test] extra")
    dist = tmp_path_factory.mktemp("dist")
    subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist), str(ROOT)],
        check=True,
        capture_output=True,
    )
    wheels = list(dist.glob("*.whl"))
    assert len(wheels) == 1, f"expected one wheel, got {wheels}"
    return wheels[0]


def test_wheel_contains_the_analytical_method(wheel):
    names = zipfile.ZipFile(wheel).namelist()
    for expected in ("gtta/skills/SKILL.md", "gtta/skills/SKILL_RU.md"):
        assert expected in names, (
            f"{expected} missing from the wheel. The method is the product; a wheel "
            f"without it installs an empty shell. Wheel contents: {sorted(names)}"
        )


def test_wheel_ships_the_method_at_full_length(wheel):
    with zipfile.ZipFile(wheel) as archive:
        text = archive.read("gtta/skills/SKILL.md").decode("utf-8")
    assert len(text) > MINIMUM_INSTALLED_METHOD_LENGTH, (
        f"packaged SKILL.md is {len(text)} characters. A symlink that was archived "
        "as a link rather than resolved would land here."
    )


@pytest.mark.skipif(shutil.which("python3") is None, reason="needs a python3 on PATH")
def test_installed_package_returns_the_method_not_a_stub(wheel, tmp_path):
    """The end-to-end check the 1.4.0 defect required.

    Install the built wheel into a throwaway environment with no repository on
    `sys.path`, then ask it for the prompt the README tells users to ask for.
    """
    env_dir = tmp_path / "venv"
    venv.create(env_dir, with_pip=True)
    python = env_dir / "bin" / "python"
    subprocess.run(
        [str(python), "-m", "pip", "install", "--quiet", str(wheel)],
        check=True,
        capture_output=True,
    )

    probe = (
        "from gtta.skill import get_skill_prompt;"
        "en = get_skill_prompt('en'); ru = get_skill_prompt('ru');"
        "print(len(en), len(ru))"
    )
    # cwd is deliberately outside the repository: importing from the source tree
    # would reintroduce exactly the blind spot this test exists to remove.
    result = subprocess.run(
        [str(python), "-c", probe],
        check=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    english, russian = (int(value) for value in result.stdout.split())
    assert english > MINIMUM_INSTALLED_METHOD_LENGTH, (
        f"installed package returned {english} characters for the English method. "
        "This is the 1.4.0 stub failure."
    )
    assert russian > 2000


def test_missing_method_raises_instead_of_returning_a_placeholder(monkeypatch, tmp_path):
    """A quiet fallback is the defect, not the mitigation."""
    from gtta import skill

    monkeypatch.setattr(skill, "SKILLS_DIR", tmp_path / "absent")
    with pytest.raises(skill.SkillNotAvailableError):
        skill.get_skill_prompt("en")


def test_truncated_method_raises(monkeypatch, tmp_path):
    stub = tmp_path / "skills"
    stub.mkdir()
    (stub / "SKILL.md").write_text("You are a strategic-risk analyst.")

    from gtta import skill

    monkeypatch.setattr(skill, "SKILLS_DIR", stub)
    with pytest.raises(skill.SkillNotAvailableError):
        skill.get_skill_prompt("en")
