# hai-teams — start here

**Goal, in one line:** evaluate LLMs against the *team-process taxonomy* (transition / action /
interpersonal processes, plus general task ability), running on Northwestern's **Quest** SLURM
cluster against six commercial providers, with every reported number taken from `Final_result.xlsx`
— the selected models — while `Tempo_results.xlsx` keeps a column for every model ever run (`PLAN.md`).

Read this file, then only what the task needs. Nothing else is loaded up front — that is the design,
not an omission. **Hit a problem, or a task done before?** [`../AGENTS.md`](../AGENTS.md) maps the
situation to the first move and the file that holds the detail.

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

- **Sync state — audited 2026-10-12.** Local, `origin` and `backup` agree. NegotiationToM's luna and
  flash-lite runners and the per-row usage in `neg_eval_core.py` went to Quest and into git on
  2026-10-12, then their review fixes (`0813b65`): 49 code files each side, none differing, and
  Quest's `NegotiationToM/.env` now holds `OPENAI_API_KEY` and `OPENROUTER_API_KEY` (backup
  `.env.bak.20261012122040` beside it). AwareBench went to Quest the same day (`6fafdc5`), and its five full
  runs came back down into git (`a07bf58`, `873590a`), md5-identical to Quest. EmoBench
  has two code files on Quest only (`EMO_Gemini/gemini_emo_eval.py`, `run_emobench.sh`) — reported,
  not pulled. **Re-run `python3 .claude/scripts/sync_audit.py --fetch` rather than trusting this
  line.**
- **Running now:** nothing is assumed. Check, don't remember — `monitor-run`, or `squeue -u uwr0681`.
- **All ten benchmarks have a knowledge-base page**; two of them — PlanBench and mpgt — have no
  runner at all, so work there starts at phase 1 or 2 rather than 3. Wonderbread and MultiChallenge
  have the **judge pilot**'s runners only (2026-10-19): `gpt-5.6-luna` on a 10% sample, graded by
  the four candidate judges. GPT's responses were generated and judged on Quest 2026-10-19 (jobs
  4482838, 4506836); which judge to adopt is open — Kimi K2.6 or Haiku 5.5
  (`LLM_as_judge/PILOT_FINALISTS.md`).
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
| **gate** | a workflow phase that is allowed to refuse — `fix-run` and `launch-run` return without submitting when the reviewer says no, `finish-run` without recording until the user confirms. Why they are built that way: `tools/create-workflow.md` |
| **`STATUS:` line** | the fixed vocabulary every agent ends its report with, so a dispatch can be branched on without re-reading prose. `references/handoffs.md` |
| **pilot** | a small fraction of the data run first and reviewed before the full run commits hours to a config. The script name is on the benchmark's page |
| **shard tag** | `{model}_shard{N}of{M}.jsonl` in an output filename. Without it every shard overwrites the last |
| **halt marker** | `BILLING_HALT` / `QUOTA_HALT` / `FAILURE_HALT` in a model folder — the cheapest signal there is, cleared at the start of each run so one that exists is about the current run |
| **checkpoint** | resume skips any UID already present. After a prompt or decoding change, **archive** it rather than resuming, or one result set holds two configurations |

## Last major change

**2026-10-05** — the tool layer was rebuilt (`b73ca66`). **Skills are the steps** (eleven, in
`.claude/skills/`), **agents the roles** (the same six), **workflows the baselines** — five
(`new-runner`, `launch-run`, `monitor-run`, `fix-run`, `finish-run`), each phase naming its agent and
its skill, adapted to the task rather than multiplied. **The nine earlier workflow names no longer
exist** — `run-model`, `run-fast`, `fix-broken-run`, `check-status`, `verify-change`,
`scale-shards`, `compare-providers`, `harvest-patterns`, `watch-live-runs`. Anything naming them is
stale, except `references/external-patterns.md`, which is history. Same day: `AGENTS.md` (situation
→ first move, for Claude and Codex), memory cut to personal preferences only, and
`scripts/sync_audit.py` for the three-way check.

**2026-08-19 / 08-23** — benchmarks regrouped into the four team-process folders (`269bbfe`), first
locally, then on Quest for this account's directories, which now sit under
`Interpersonal_processes_benchmarks/` and `Tasks_benchmarks/`. **The rest of `/projects/p32983`
belongs to other accounts** — `bbh`, `mmlu`, `LLMs-Planning-main`, both `*_DocVQA` copies and
`pythonenvs` are `cpz1698`'s, `eval` is `wxw6517`'s, `gen-ai-ngt` is `gdg0095`'s — and stays flat.
A Quest path remembered from before 2026-08-23 is stale; the local-only move is what once blinded
the pre-submit gate.

**2026-08-22** — agent-facing docs split three ways: this file (orientation), `references/`
(knowledge), `tools/` (what to dispatch). `CLAUDE.md` holds rules only.
