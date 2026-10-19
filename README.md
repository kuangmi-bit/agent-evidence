# Agent Evidence

[![CI](https://img.shields.io/github/actions/workflow/status/probityai/agent-evidence/ci.yml?label=CI)](https://github.com/probityai/agent-evidence/actions/workflows/ci.yml)
[![Licence](https://img.shields.io/github/license/probityai/agent-evidence)](LICENSE)
[![Stars](https://img.shields.io/github/stars/probityai/agent-evidence?style=flat)](https://github.com/probityai/agent-evidence/stargazers)
[![vectors on PyPI](https://img.shields.io/pypi/v/agent-evidence-vectors?label=vectors)](https://pypi.org/project/agent-evidence-vectors/)
[![vectors per month](https://img.shields.io/pypi/dm/agent-evidence-vectors?label=vectors%20per%20month)](https://pepy.tech/projects/agent-evidence-vectors)
[![vectors total](https://static.pepy.tech/badge/agent-evidence-vectors)](https://pepy.tech/projects/agent-evidence-vectors)
[![vocabulary on PyPI](https://img.shields.io/pypi/v/agent-evidence-vocabulary?label=vocabulary)](https://pypi.org/project/agent-evidence-vocabulary/)
[![admission on PyPI](https://img.shields.io/pypi/v/agent-evidence-admission?label=admission)](https://pypi.org/project/agent-evidence-admission/)
[![dsse on crates.io](https://img.shields.io/crates/v/dsse?label=dsse)](https://crates.io/crates/dsse)
[![dsse downloads](https://img.shields.io/crates/d/dsse?label=dsse%20downloads)](https://crates.io/crates/dsse)
[![jcs-admit on crates.io](https://img.shields.io/crates/v/jcs-admit?label=jcs-admit)](https://crates.io/crates/jcs-admit)
[![jcs-admit downloads](https://img.shields.io/crates/d/jcs-admit?label=jcs-admit%20downloads)](https://crates.io/crates/jcs-admit)

The open specification layer for evidence about AI agents: conformance vectors, a term vocabulary, admission rules, a conformance board, and the `jcs-admit` and `dsse` crates that canonicalize and sign records. It is maintained by Probity AI, under the [governance](GOVERNANCE.md) in this repository.

It is for people who build or check an agent-evidence verifier, and for projects that sign or canonicalize JSON records about what an agent did.

## Install

Pin the parts you use:

```bash
uv add agent-evidence-vectors==0.20.0
pip install agent-evidence-vectors==0.20.0
cargo add dsse@0.1.4 jcs-admit@0.1.2
```

## Try it

Run every vector of the default corpus through the bundled reference verifier. You need [uv](https://docs.astral.sh/uv/); nothing is cloned or built:

```bash
uvx agent-evidence-vectors==0.20.0
```

The run prints one row per vector and ends with:

```text
totals: 288 vectors, 288 pass, 0 fail; report written to conformance-report.json
```

Verified by Probity (github.com/probityai/probity). The `probityai` command line is planned, not yet released: `uv add probityai`, then `pip install probityai`.

## Status

This repository is new. Each part moves here from its own repository with its full history, one at a time, and keeps its registry name and its own version line. Until a part arrives, its old repository is where it lives and releases:

| Part | Registry name | Current home |
| --- | --- | --- |
| Conformance vectors | `agent-evidence-vectors` (PyPI) | [probityai/agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors) |
| Vocabulary | `agent-evidence-vocabulary` (PyPI) | [probityai/agent-evidence/packages/vocabulary](https://github.com/probityai/agent-evidence/tree/main/packages/vocabulary) |
| Admission rules | `agent-evidence-admission` (PyPI) | [probityai/agent-evidence/packages/admission](https://github.com/probityai/agent-evidence/tree/main/packages/admission) |
| DSSE envelopes | `dsse` (crates.io) | [probityai/agent-evidence/crates/dsse](https://github.com/probityai/agent-evidence/tree/main/crates/dsse) |
| JSON admission and RFC 8785 | `jcs-admit` (crates.io, PyPI) | [probityai/agent-evidence/crates/jcs-admit](https://github.com/probityai/agent-evidence/tree/main/crates/jcs-admit) |

Moved repositories are archived, not deleted: their tags, releases, Actions and pages keep working.

## Documentation

| I want to | Read |
| --- | --- |
| See where each part lives and how it is released | [Layout and releases](docs/LAYOUT.md) |
| Contribute a change | [Contributing](CONTRIBUTING.md) |
| Become a maintainer | [Governance](GOVERNANCE.md) |
| Report a vulnerability | [Security](SECURITY.md) |
| See who runs the vectors in CI | [Used by](docs/USED-BY.md) |
| Get the Verified by Probity badge | [Verified badge](docs/VERIFIED-BADGE.md) |

## Licence

Each directory carries its own licence file, and it applies to that directory. Files outside every such directory are under the [Apache License 2.0](LICENSE).
