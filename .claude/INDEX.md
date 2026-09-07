# hai-teams — start here

**Goal, in one line:** evaluate LLMs against the *team-process taxonomy* (transition / action /
interpersonal processes, plus general task ability), running on Northwestern's **Quest** SLURM
cluster against six commercial providers, with every reported number taken from `Final_Result.xlsx`
— the six selected models — while `Results.xlsx` keeps a column for every model ever run (`PLAN.md`).

Read this file, then only what the task needs. Nothing else is loaded up front — that is the design,
not an omission.

## What the work is

Five phases — analyse a new benchmark, write the per-model scripts, upload and run on Quest, monitor,
and keep everything in sync. **They are listed in `CLAUDE.md`, which is already in your context**,
each with the reference it reads and the tool it reaches for. Not repeated here.

One of them has a gate that is not technical: **phase 3 does not start until the user has verified
the scripts.** Phases 1, 2 and 5 are local work and need no permission.

Two files are read on every task regardless of phase:
[`references/README.md`](references/README.md), the map of what to read when, and
`references/shared-context.md`, which says which document is authoritative on what.

**Working on a specific benchmark? Read its page and its group page** —
[`references/benchmarks/`](references/benchmarks/README.md). The rest of `.claude/` is deliberately
benchmark-agnostic; every number, path and task name belonging to one benchmark lives on its own
page, and carrying one across benchmarks is the mistake that split is there to prevent.

## Where the project is

- **Working scope right now (2026-08-22): the local tree.** Quest is not being checked or synced;
  the transfer happens once local is settled. That does not relax any rule about *how* a sync is
  done when it happens — it means the sync has not happened yet.
- **Running now:** nothing is assumed. Check, don't remember — `check-status`, or `squeue -u uwr0681`.
- **All ten benchmarks have a knowledge-base page**; three of them have no runner at all, so work
  there starts at phase 1 or 2 rather than 3.
- **Two runners comply with the model-parameter rule; every other one does not.** bbh's
  `BBH_GPT_5.6_Luna` and `BBH_Gemini_Flash3.5lite_OpenRouter` (added 2026-08-29) negotiate their
  surface and set a cap; their caps are chosen rather than measured, but both have since run all
  4,833 rows with `no_marker=0`, so nothing was truncated at them. The
  rest set no thinking or output cap, and bbh's eight leave it open **deliberately**: setting one
  changes what the model emits and would make new rows incomparable with the 4,833 already on disk.
  See [`references/model-parameters.md`](references/model-parameters.md).
- Per-benchmark state, provider coverage and open work: `PLAN.md`.

## Terms this project uses in a specific way

| Term | Means |
|---|---|
| **kill-and-resync** | standing authorisation to `scancel` a known-bad job, fix locally, overwrite on Quest with `md5sum` confirmation, resubmit — without asking first |
| **sync check** | proving every code file on Quest matches local before a submit. A `PreToolUse` hook runs it automatically and **fails open**, so a stale path silently protects nothing. Contract and the two ways the check lies: `references/quest-cluster.md` |
| **gate** | a workflow phase that is allowed to refuse — `fix-broken-run` returns without submitting when the reviewer says no. Why they are built that way: `tools/create-workflow.md` |
| **`STATUS:` line** | the fixed vocabulary every agent ends its report with, so a dispatch can be branched on without re-reading prose. `references/handoffs.md` |
| **pilot** | a small fraction of the data run first and reviewed before the full run commits hours to a config. The script name is on the benchmark's page |
| **shard tag** | `{model}_shard{N}of{M}.jsonl` in an output filename. Without it every shard overwrites the last |
| **halt marker** | `BILLING_HALT` / `QUOTA_HALT` / `FAILURE_HALT` in a model folder — the cheapest signal there is, cleared at the start of each run so one that exists is about the current run |
| **checkpoint** | resume skips any UID already present. After a prompt or decoding change, **archive** it rather than resuming, or one result set holds two configurations |

## Last major change

**2026-08-19** — benchmarks reorganised into the four team-process folders (`269bbfe`), local only.
That divergence is what blinded the pre-submit gate, which found zero files and exited 2 while still
looking wired up.

**2026-08-23** — the divergence closed for **the three directories this account owns**. On Quest,
`DocVQA` → `Tasks_benchmarks/DocVQA`, `EmoBench-master` → `Interpersonal_processes_benchmarks/EmoBench`,
`NegotiationToM` → `Interpersonal_processes_benchmarks/NegotiationToM`. **The rest of
`/projects/p32983` belongs to other accounts** — `bbh`, `mmlu`, `LLMs-Planning-main`, both
`*_DocVQA` copies and `pythonenvs` are `cpz1698`'s, `eval` is `wxw6517`'s, `gen-ai-ngt` is
`gdg0095`'s. They stay flat at the top level and must not be moved. Any Quest path remembered from
before this date is stale.

**2026-08-22** — agent-facing docs split three ways: this file (orientation), `references/`
(knowledge), `tools/` (what to dispatch). `CLAUDE.md` holds rules only.
