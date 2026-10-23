# Other readers of this case

Each reader below ran on its own inputs or on the 16 fixtures here. Its author keeps its code and its result names.
We record what we reran and on which source pins.

## A reader written from the contract alone

`ogasurfproject-jpg` wrote a second reader for these fixtures from [the input contract](INPUT-CONTRACT.md) and the 16 fixture inputs at `042d9ba`.
The implementer did not see this reader, its tests, the manifest or the qualification outputs.
The reader is [`horizon-shield@5037ecf8`, `workers/hs-ledger/nenrin/approved-sql-reader-v0/`](https://github.com/ogasurfproject-jpg/horizon-shield/tree/5037ecf8a2195f2f17f1b47ca3d2b5f49ea0a0e0/workers/hs-ledger/nenrin/approved-sql-reader-v0); `reader.py` has SHA-256 `fc87a6ece18c71d839f6e6b08cfb2d66b56e0dda47e2b5535d5e686bc0fa0b86`.
He posted the run in [the case thread](https://github.com/probityai/agent-evidence/issues/27#issuecomment-6247269456).

On 2026-10-23 we reran it with CPython 3.13.15 (`python3 -I -B reader.py <fixture>`) over the 16 fixtures. They are byte-identical at `042d9ba` and here. The counts match his report:

| Compared with the manifest | Agree |
|---|---|
| Exit code | 16 of 16 (2 exit 0, 14 exit 1) |
| `result` string | 4 of 16 |
| `later_state` | 15 of 16 (`changed` for `supplied_state_differs`) |

His reader never splits a pair of fixtures that the manifest keeps together. It groups two sets that the manifest separates: the three outcome cases, and an incomplete audit with a missing application record.

He also found two places where the contract allowed another reading that would flip an exit code. The definition of `recorded_commit_matches` did not say that `granted: false` or `application: null` prevents it. The manifest named eleven result values, and the contract named two of them. The contract now states both rules and lists every result in the order the reader checks it. `tests/test_contract.py` fails when that list and the reader disagree.

## The Motebit approval triad

`hakimlabs` posted a tool-call approval triad from [`motebit/motebit@3ed6e6d`](https://github.com/motebit/motebit/tree/3ed6e6d2da617d775fe9431c36020efc24749fe6/examples/interop/approval-triad): a signed approval, a tool-invocation receipt and an execution receipt, with one control and six negatives.
On 2026-10-13 we ran its reader with Python 3.13.15 and PyNaCl. All 7 cases reproduced `expected.json`, and `test_reader.py` rejected all 114 single-field mutants.
The triad joins this case at the tool-call level. Its approval and execution are joined on equal field values, not by a digest of the approval.
