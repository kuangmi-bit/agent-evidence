"""Published run records carry no absolute local path.

Literal roots are built from parts so this file holds none for the repository scans.
"""

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "record_paths", ROOT / "scripts" / "record_paths.py")
record_paths = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(record_paths)

S = "/"
REFUSED = [
    S + "home" + S + "someone" + S + "work",
    S + "Users" + S + "someone" + S + "x",
    "C:" + "\\" + "Users" + "\\" + "someone",
    "~" + S + "Documents",
    S + "mnt" + S + "data",
    S + "blue" + S + "group" + S + "u",
    S + "root" + S + "case",
]


@pytest.mark.parametrize("path", REFUSED)
def test_every_local_root_is_found(path: str) -> None:
    assert record_paths.find_local_path(f"run at {path} done") is not None


@pytest.mark.parametrize(
    "text",
    ["site/experiments/x/report.json", "../.build/result", "https://example.invalid/home/page",
     "see the foo/tmp/bar file", "a~/b"],
)
def test_repo_relative_paths_and_urls_pass(text: str) -> None:
    assert record_paths.find_local_path(text) is None


def test_ci_homes_pass_and_a_person_home_does_not() -> None:
    assert record_paths.find_local_path(S + "home" + S + "runner" + S + "w") is None
    assert record_paths.find_local_path(S + "home" + S + "gate" + S + "w") is None
    assert record_paths.find_local_path(S + "home" + S + "alice" + S + "w") is not None


def test_scratch_is_found_unless_allowed() -> None:
    scratch = S + "tmp" + S + "x"
    assert record_paths.find_local_path(scratch) is not None
    assert record_paths.find_local_path(scratch, allow_scratch=True) is None


def test_relativize_rewrites_under_the_root_and_refuses_outside(tmp_path: Path) -> None:
    assert record_paths.relativize(tmp_path / "a" / "b.json", tmp_path) == "a/b.json"
    with pytest.raises(ValueError, match="no repo-relative form"):
        record_paths.relativize(tmp_path.parent / "elsewhere", tmp_path)


# Recorded CI logs and frozen reports keep the scratch directories their runs used,
# so the scan allows /tmp. Every other root is refused in every published record.
RECORD_SUFFIXES = (".json", ".jsonl", ".log", ".txt", ".stderr", ".stdout", ".xml")


def _tracked_records() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z", "site"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode()
    return [ROOT / n for n in out.split("\0") if n.endswith(RECORD_SUFFIXES)]


def test_the_scan_sees_the_published_records() -> None:
    names = {p.relative_to(ROOT).as_posix() for p in _tracked_records()}
    assert "site/experiments/remora-e7-pip-0.25.0-2026-10-23/report.json" in names
    assert len(names) > 100


def test_no_published_record_carries_an_absolute_local_path() -> None:
    leaks = []
    for path in _tracked_records():
        text = path.read_text(encoding="utf-8", errors="replace")
        found = record_paths.find_local_path(text, allow_scratch=True)
        if found is not None:
            leaks.append(f"{path.relative_to(ROOT)}: {found!r}")
    assert not leaks, "\n".join(leaks)
