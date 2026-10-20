"""Tests for scripts/workspace.py: area discovery, change mapping and release tags."""

import importlib.util
from pathlib import Path

import pytest

_SPEC = importlib.util.spec_from_file_location(
    "workspace", Path(__file__).resolve().parents[1] / "scripts" / "workspace.py")
workspace = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(workspace)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "crates" / "dsse").mkdir(parents=True)
    (tmp_path / "crates" / "dsse" / "Cargo.toml").write_text('[package]\nname = "dsse"\nversion = "0.1.4"\n')
    (tmp_path / "crates" / "README.md").write_text("crates\n")
    (tmp_path / "packages" / "vocab").mkdir(parents=True)
    (tmp_path / "packages" / "vocab" / "pyproject.toml").write_text(
        '[project]\nname = "agent-evidence-vocabulary"\nversion = "0.6.0"\n')
    (tmp_path / "crates" / "dsse" / "npm").mkdir()
    (tmp_path / "crates" / "dsse" / "npm" / "package.json").write_text('{"name": "dsse", "version": "0.1.0"}\n')
    (tmp_path / "vectors").mkdir()
    (tmp_path / "release.toml").write_text(
        '[[unit]]\nprefix = "dsse"\nname = "dsse"\nregistry = "crates.io"\ndirectory = "crates/dsse"\n\n'
        '[[unit]]\nprefix = "agent-evidence-vocabulary"\nname = "agent-evidence-vocabulary"\n'
        'registry = "pypi"\ndirectory = "packages/vocab"\n\n'
        '[[unit]]\nprefix = "jcs-admit"\nname = "jcs-admit"\nregistry = "crates.io"\n'
        'directory = "crates/jcs-admit"\n\n'
        '[[unit]]\nprefix = "dsse-npm"\nname = "dsse"\nregistry = "npm"\ndirectory = "crates/dsse/npm"\n')
    return tmp_path


def test_areas_are_the_directories_with_their_own_checks(repo: Path) -> None:
    assert workspace.areas(repo) == ["crates/dsse", "packages/vocab", "vectors"]


def test_a_change_inside_an_area_selects_only_that_area(repo: Path) -> None:
    got = workspace.changed(["crates/dsse/src/lib.rs"], repo)
    assert got == {"crates/dsse": True, "packages/vocab": False, "vectors": False}


def test_documentation_outside_areas_selects_nothing(repo: Path) -> None:
    got = workspace.changed(["README.md", "docs/LAYOUT.md", "crates/README.md"], repo)
    assert not any(got.values())


def test_a_shared_file_selects_every_area(repo: Path) -> None:
    got = workspace.changed([".github/workflows/ci.yml"], repo)
    assert all(got.values())


def test_a_crate_tag_resolves_to_its_unit(repo: Path) -> None:
    got = workspace.release_target("dsse-v0.1.4", repo)
    assert got["directory"] == "crates/dsse" and got["registry"] == "crates.io"


def test_a_python_tag_resolves_to_its_unit(repo: Path) -> None:
    got = workspace.release_target("agent-evidence-vocabulary-v0.6.0", repo)
    assert got["name"] == "agent-evidence-vocabulary" and got["version"] == "0.6.0"


def test_an_npm_tag_resolves_to_its_unit_and_not_the_crate(repo: Path) -> None:
    got = workspace.release_target("dsse-npm-v0.1.0", repo)
    assert got["prefix"] == "dsse-npm" and got["registry"] == "npm" and got["version"] == "0.1.0"


@pytest.mark.parametrize("tag, message", [
    ("dsse-v0.1.5", "does not match"),
    ("dsse-0.1.4", "is not <prefix>-v"),
    ("dsse-npm-v0.1.4", "does not match"),
    ("nothing-v1.0.0", "names no single unit"),
    ("jcs-admit-v0.1.2", "does not exist"),
])
def test_a_bad_tag_is_refused(repo: Path, tag: str, message: str) -> None:
    with pytest.raises(SystemExit, match=message):
        workspace.release_target(tag, repo)


def test_the_vocabulary_python_tag_resolves_in_this_repository() -> None:
    got = workspace.release_target("agent-evidence-vocabulary-python-v0.6.0")
    assert got["name"] == "agent-evidence-vocabulary" and got["registry"] == "pypi"
    assert got["prefix"] == "agent-evidence-vocabulary-python"


def test_the_repository_itself_reads_cleanly() -> None:
    assert isinstance(workspace.areas(), list)
    with pytest.raises(SystemExit, match="names no single unit|does not match"):
        workspace.release_target("dsse-v0.0.0")
