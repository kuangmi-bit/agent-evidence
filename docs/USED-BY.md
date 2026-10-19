# Used by

Outside projects whose own public repository runs `agent-evidence-vectors` in CI or pins it. Each row links the file that does it, in their repository, so you can check it without trusting this page.

| Project | What runs | Proof |
| --- | --- | --- |
| [ogasurfproject-jpg/horizon-shield](https://github.com/ogasurfproject-jpg/horizon-shield) | Pins `agent-evidence-vectors==0.20.0` and replays the RFC 8785 canonicalization corpus against its A2A walk client on every change to it | [workflow run 39180799548](https://github.com/ogasurfproject-jpg/horizon-shield/actions/runs/39180799548), commit `6b4841af9083` |
| [MoltyCel/moltrust-api](https://github.com/MoltyCel/moltrust-api) | Replays the `a2a-jcs-v01` corpus through `agent-evidence-vectors` in its `a2a-jcs-conformance` workflow | [pull request 721](https://github.com/MoltyCel/moltrust-api/pull/721), merge commit `36fee0b45c64` |

Counts and dates are read from the public endpoints. A pull request that is open, or a project that only mentions us, is not a row.

## Add your project

Open a pull request that adds a row, or tell us in an issue. A row needs a link to the file in your repository that runs or pins the package.
