"""The written result list must match what the reader returns, in the stated order."""

import ast
import json
import re
from pathlib import Path

from sql_illustration.check import assess

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (ROOT / "docs/INPUT-CONTRACT.md").read_text()
MANIFEST = json.loads((ROOT / "fixtures/manifest.json").read_text())


def section(heading):
    start = CONTRACT.index(heading)
    rest = CONTRACT[start + len(heading) :]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


def listed_results():
    names = []
    for line in section("## Result values").splitlines():
        if re.match(r"^\d+\. ", line):
            names += re.findall(r"`([a-z_]+)`", line.split(":", 1)[1])
    return names


def function(name):
    tree = ast.parse((ROOT / "sql_illustration/check.py").read_text())
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)


def returned_literals(function_name):
    func = function(function_name)
    return {
        n.value.value
        for n in ast.walk(func)
        if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant)
    } | {
        c.value
        for n in ast.walk(func)
        if isinstance(n, ast.Return) and isinstance(n.value, ast.IfExp)
        for c in (n.value.body, n.value.orelse)
        if isinstance(c, ast.Constant)
    }


def document():
    return json.loads((ROOT / "fixtures/matching-commit.json").read_text())


def test_listed_results_are_every_fixture_result():
    names = listed_results()
    assert len(names) == len(set(names)) == 11
    assert set(names) == {case["expected_result"] for case in MANIFEST["cases"]}


def test_listed_order_matches_the_reader_after_a_single_match():
    func = function("_matched_result")
    in_source_order = [
        n.value.value
        for n in sorted(ast.walk(func), key=lambda n: getattr(n, "lineno", 0))
        if isinstance(n, ast.Return) and isinstance(n.value, ast.Constant)
    ]
    assert len(in_source_order) == 8
    assert [n for n in listed_results() if n in in_source_order] == in_source_order


def test_listed_later_states_are_every_value_the_reader_returns():
    lines = section("## Result values").splitlines()
    line = next(x for x in lines if x.startswith("`later_state`"))
    assert set(re.findall(r"`([a-z_]+)`", line)) - {"later_state", "result"} == returned_literals(
        "_later"
    )


def test_not_granted_comes_before_a_missing_application_record():
    doc = document()
    doc["approval"]["granted"] = False
    doc["application"] = None
    assert assess(doc)["result"] == "approval_not_granted"


def test_a_missing_application_record_prevents_a_matching_commit():
    doc = document()
    doc["application"] = None
    assert assess(doc)["result"] == "application_record_missing"
