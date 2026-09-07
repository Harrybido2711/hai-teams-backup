# hai-teams — repository map

What this repo holds: a benchmark suite for evaluating LLMs against the **team-process taxonomy**
(transition / action / interpersonal processes, plus general task ability). Each benchmark is a
vendored copy of an upstream project plus this project's own runners; the runs execute on the
**Quest** SLURM cluster against six commercial providers, and the reported numbers converge in
`Final_Result.xlsx` — with `Results.xlsx` holding the wider record of every model ever run (see
[Two workbooks](#two-workbooks-results-is-wide-final_result-is-what-is-reported)).

Last verified against the working tree on 2026-08-19, after the reorganisation in `269bbfe`.

## Top level

```
hai-teams/
├── Transition_processes_benchmarks/     7,788 files · 563M
│   ├── Awareness_in_LLM/                mission analysis — AwareBench
│   ├── LLMs-Planning_bench/             strategy formulation — PlanBench
│   └── Multi-party_Goal_Tracking_bench/ goal specification — mpgt-eval
├── Action_processes_benchmarks/         1,332 files · 50M
│   ├── Wonderbread_bench/               monitoring progress toward goals
│   └── Multi-challenge_bench/           coordination — MultiChallenge
├── Interpersonal_processes_benchmarks/  804 files · 121M
│   ├── NegotiationToM/                  conflict management
│   └── EmoBench/                        affect management
├── Tasks_benchmarks/                    5,765 files · 3.5G
│   ├── DocVQA/                          document VQA (3.5G — the page images)
│   ├── bbh/                             BIG-Bench Hard
│   └── mmlu/                            MMLU
├── Random_stuff/                        1,032 files · 75M — parked, not part of the taxonomy
│   ├── SQA Release 1.0/ · TruthfulQA-main/ · sycophancy-eval-main/
├── LLM_as_judge/                        judge methodology, not a benchmark
│   ├── JUDGE_RECORD.md                  the filled record for all three judged benchmarks
│   └── JUDGE_SUMMARY.md                 its two-page version, for discussion
├── .claude/                             INDEX, tools, agents, references, workflows (see below)
├── CLAUDE.md                            planner rules only; `.claude/INDEX.md` is the entry point
├── PLAN.md                              this file
├── README.md
├── Results.xlsx                         every model ever run — the wide record
├── Final_Result.xlsx                    the six selected models — what gets reported
└── quest_pull.log                       gitignored
```

The four category folders are **not** arbitrary grouping: they are the rows of the tracker that
drives this project, so a benchmark's folder states which team process it is evidence for.

## Two workbooks: Results is wide, Final_Result is what is reported

Stated by the user, 2026-08-29. Both workbooks carry the same five sheets — `Big Bench Hard`,
`MMLU`, `DocVQA`, `Emo`, `Awareness` — and differ only in which model columns they are allowed to
hold.

- **`Results.xlsx` records every model that has appeared in an experiment**, including ones that
  were tried and then dropped, and the two that were *replaced*. Its `Emo` sheet is the visible
  case: eight columns, the six slots plus `gemini-2.5-flash` and `gpt-4o-mini` in their own right. A
  leftover column is not a retracted result, the same way a leftover CSV is not — see
  `.claude/references/benchmarks/tasks/bbh.md`.
- **`Final_Result.xlsx` records only the six selected models** — one per vendor slot, named below —
  and it is the workbook a reported number is taken from.

### The six, by name

Confirmed with the user 2026-08-29. The slot names are the workbook's column headers; the model id is
what a runner actually calls. **Two slots were re-pointed and the workbook has not caught up** — see
the warning under the table.

| Slot | Model id | Route | Where the recipe is |
| --- | --- | --- | --- |
| Gemini | `gemini-3.5-flash-lite` | OpenRouter (`google/gemini-3.5-flash-lite`) | `references/model-calls.md` |
| OpenAI | `gpt-5.6-luna` | OpenAI platform, `reasoning_effort="low"` | `references/model-calls.md` |
| XAI | `grok-3-mini` | xAI | `references/model-parameters.md` |
| Qwen | `Qwen/Qwen3.5-9B` | Together, `reasoning={"enabled": False}` | `references/model-parameters.md` |
| Gemma | `google/gemma-4-31B-it` | DeepInfra | `references/model-calls.md` |
| Deepseek | `deepseek-reasoner` | DeepSeek | `references/model-calls.md` |

**Row 2 of every sheet names the model behind each column.** In `Final_Result.xlsx` it is `Model` —
one settled model id per slot, the same six on every sheet. In `Results.xlsx` it is `Model / config`,
because there a slot can hold a different model on one sheet than on another, and the config that
produced the number is part of what the number means.

**`Final_Result.xlsx` never borrows a number from a model that is not selected. A blank means the
selected model has not been run on that sheet**, and it stays blank until it is. That rule is what
makes the two files different in practice: `gemini-2.5-flash` and `gpt-4o-mini-2024-07-18` are
superseded but are still what the bbh, MMLU, DocVQA and NegotiationToM runners call, so on those
three sheets the `Gemini` and `OpenAI` columns of `Final_Result.xlsx` are **empty**. Nothing is lost
— those runs keep their columns in `Results.xlsx`. **`Emo` is the one sheet already run on the
current pair**, so there the two slots are filled. Closing the other three means re-running them, not
editing a header.

One caveat inside that: the `Emo` result for `gpt-5.6-luna` is the **default `medium`** arm.
The settled effort is `low`, and `results_eLow` has EU (0.650) but no EA, so **no complete EmoBench
score exists at the settled config** — one EA run at `effort=low` closes it.

**bbh is complete for all six** — `BBH_Gemini_Flash3.5lite_OpenRouter` (0.9375) and
`BBH_GPT_5.6_Luna` (0.9349), added 2026-08-29, have their full 20 tasks, so the Gemini and OpenAI
columns of `Final_Result.xlsx` are filled on that sheet and no longer belong to the superseded
models. Those two keep columns of their own in `Results.xlsx`, and `gemini-2.5-flash`'s is a broken
run — 62% truncated before the answer, 0.3455 — kept as a record and not re-run
(`.claude/references/benchmarks/tasks/bbh.md`). **bbh, MMLU and DocVQA are what the "least filled"
line above is about; bbh is now off that list.**

`kimi-k2.5` and `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` were run on bbh only (llama also
on MMLU) and were never among the six.

So running a new model adds a column to `Results.xlsx` and **does not** earn one in
`Final_Result.xlsx` unless that model is one of the six. Numbers still land in `Results.xlsx` first;
`Final_Result.xlsx` is the selection made from it, not a separate measurement.

Both were rebuilt on 2026-08-29 from the result files on disk, and each carries a **`Provenance`
sheet** naming the source file behind every column and the reason behind every blank. Read that sheet
before trusting or extending a number; it is the part of the workbook that says where a cell came
from. The extras `Results.xlsx` holds and `Final_Result.xlsx` does not: `Kimi` and `Llama` on
`Big Bench Hard`, `Llama` on `MMLU`, and the superseded `Gemini-2.5-Flash` and `GPT-4o-mini` on
`Emo`.

**A blank cell means no usable number, not a zero.** `Awareness` is blank throughout — no model has
been scored on it yet. `MMLU`/`Qwen` is blank because `qwen_overall_results.csv` was written empty,
`MMLU`/`Gemma` covers 8 of 13 subjects because the other five were never written, and `DocVQA` has no
XAI or Deepseek run at all.

**`Big Bench Hard` is now scored uniformly, and its numbers were refreshed to match.** Every model
on that sheet comes from `BBH_*/results/*_bbh_overall.csv` under the one shared lenient matcher
(scorer tag `lenient_v2`), so the sheet is reproducible from a single source and the old
strict-vs-lenient caveat is gone. The refresh moved one column a long way: `gemini-2.5-flash` fell
from the 0.9122 the workbook used to carry to **0.3387**, because 3,002 of its 4,833 stored responses
never emitted `Final Answer:` — a broken run no scorer can rescue, and the run behind the old number
is not on disk. It is kept in `Results.xlsx` as a record; the model is superseded and will not be
redone.

## Benchmark index

| Folder                                             | Benchmark      | Team process                               | Upstream                      | LLM judge?                                           | Result files present for                                       |
| -------------------------------------------------- | -------------- | ------------------------------------------ | ----------------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| `Transition_.../Awareness_in_LLM`                | AwareBench     | mission analysis, formulation and planning | HowieHwong/Awareness-in-LLM   | **yes** — 60 of 4,075 rows                    | none yet; output templates and the paper baseline are in place |
| `Transition_.../Multi-party_Goal_Tracking_bench` | mpgt-eval      | goal specification                         | AddleseeHQ/mpgt-eval          | no — human review                                   | none yet (vendored 2026-08-19)                                 |
| `Transition_.../LLMs-Planning_bench`             | PlanBench      | strategy formulation                       | karthikv792/LLMs-Planning     | no — VAL/PDDL validator                             | none yet                                                       |
| `Action_.../Wonderbread_bench`                   | Wonderbread    | monitoring progress toward goals           | HazyResearch/wonderbread      | **yes** — QA, SOP generation, SOP improvement | none yet (vendored 2026-08-19)                                 |
| `Action_.../Multi-challenge_bench`               | MultiChallenge | coordination                               | ekwinox117/multi-challenge    | **yes** — every item                          | none yet (vendored 2026-08-19)                                 |
| `Interpersonal_.../NegotiationToM`               | NegotiationToM | conflict management                        | HKUST-KnowComp/NegotiationToM | no — EM + micro/macro F1                            | GPT, Gemini, Gemma, Qwen, Deepseek, XAI                        |
| `Interpersonal_.../EmoBench`                     | EmoBench       | affect management                          | Sahandfer/EmoBench            | no — MCQ accuracy                                   | OpenAI, Gemini, Gemma, Qwen, Deepseek, XAI                     |
| `Tasks_.../DocVQA`                               | DocVQA         | general task ability                       | docvqa.org                    | no — ANLS                                           | OpenAI, Gemini                                                 |
| `Tasks_.../bbh`                                  | BIG-Bench Hard | general task ability                       | BIG-Bench Hard                | no — exact match                                    | 7 providers incl. Llama                                        |
| `Tasks_.../mmlu`                                 | MMLU           | general task ability                       | hendrycks/test                | no — accuracy                                       | 7 providers incl. Llama                                        |

"Result files present" means CSV/JSONL output exists on disk under that provider's name — it is not a
claim that the run is complete or that its numbers have been audited. `LLM_as_judge/JUDGE_RECORD.md`
carries the judge verdict and the evidence behind it.

## The shape that repeats inside a benchmark folder

Two layouts, both this project's own work sitting beside the vendored upstream:

```
NegotiationToM/                          EmoBench/  ·  bbh/       mmlu/  ·  DocVQA/
├── NEG_GPT/                             ├── EMO_Gemini/          ├── <provider>_eval.py
│   ├── gpt_neg_eval.py                  ├── EMO_Gemma/           ├── <provider>_eval_script.sh
│   ├── run_negotiation.sh   (sbatch)    ├── EMO_Qwen/            ├── <task>.json         (data)
│   └── results/                         ├── EMO_Deepseek/        └── <provider>_<task>.csv
├── NEG_Gemini/ NEG_Gemma/ NEG_Qwen/     ├── EMO_XAI/
│   NEG_Deepseek/ NEG_XAI/               ├── OpenAI_result/
├── neg_eval_core.py    (shared core)    ├── data/
├── preflight.py · merge_neg_results.py  └── Output template/
└── NegotiationToM.json (data)
```

**bbh left the right-hand column on 2026-08-29** and was rebuilt on the middle one's convention:
`BBH_<Slot>/` per model holding `<vendor>_bbh_eval.py`, `run_bbh.sh`, `log.txt`/`log.err` and
`results/<task>/<model-slug>.{jsonl,csv}`, with the 20 task JSONs in `data/` and a shared
`bbh_eval_core.py` that owns the scorer. Two slots are named for the superseded model they call
(`BBH_Gemini_Flash2.5`, `BBH_GPT_4o_mini`) so their numbers are not read as the current slots'.
Details, and why Gemini's rows there cannot be used: `Tasks_benchmarks/bbh/README.md`.

One rule matters more than the layout: the per-provider runners **import the shared core**, so a
runner transferred to Quest without `neg_eval_core.py` fails at import. Sync them together or not at
all (`CLAUDE.md`).

## Where the documentation lives

Each file is authoritative on one thing; nothing is duplicated between them.

| File                                                   | Authoritative on                                                                                                                              |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE.md`                                          | planner **rules** only — who decides, the kill-and-resync authorisation, the invariants that hold on every task, and the discipline that keeps the docs usable |
| `.claude/INDEX.md`                                   | the entry point: project goal and stage in one page, the terms this project uses in a specific way, and the three files always read first |
| `.claude/tools/README.md`                            | the dictionary of what can be dispatched — nine workflows and six agents, one row each, with a detail file per workflow |
| `.claude/references/sync-and-consistency.md`         | the three sync layers — local↔local, local↔Quest, local↔git — what enforces each, and when the Quest one applies at all |
| `.claude/references/doc-check.md`                    | what every consistency-check finding means and how to clear it — read this when a commit is blocked |
| `.claude/references/benchmarks/<group>/<name>.md`    | per-benchmark operating detail: Quest path, layout, verified counts, output naming, run order, its own traps — one page for each of the ten, plus a group page for what a process folder's benchmarks share. The rest of `.claude/` is benchmark-agnostic on purpose |
| `LLM_as_judge/JUDGE_DOCUMENTATION_RULE.md`           | the thirteen fields that must be recorded about any judge before its numbers are used                                                         |
| `LLM_as_judge/JUDGE_RECORD.md`                       | the filled record — every judge in the suite: what it is, what it is shown, what its numbers mean, and which seven benchmarks need no record |
| `LLM_as_judge/JUDGE_SUMMARY.md`                      | the two-page version of that record: the findings, the cost per model, and the open decisions                                                 |
| `LLM_as_judge/GPT_LLM_AS_JUDGE_GUIDE.md`             | how to*build* a judge with GPT — pairwise setup, structured output, position bias                                                          |
| `Interpersonal_.../NegotiationToM/negotiation.md`    | current NegotiationToM results, dataset traps, reasoning-token cost, silent-failure catalogue                                                 |
| `Interpersonal_.../NegotiationToM/ISSUES.md`         | problems already hit, what was rejected, what shipped                                                                                         |
| `Interpersonal_.../NegotiationToM/DATA_NOTES.md`     | cutoff tiling, the`"None"` sentinel, expected row counts                                                                                    |
| `Transition_.../Awareness_in_LLM/AWARENESS_NOTES.md` | AwareBench task-by-task anatomy, its traps, and the run plan                                                                                  |
| `Tasks_.../DocVQA/OPENAI_EVAL_NOTES.md`              | the DocVQA quota incident and its fix                                                                                                         |
| `.claude/references/*.md`                            | operating knowledge — Quest/SLURM, provider gotchas, runner skeleton, handoffs                                                               |

## The agent layer

```
.claude/
├── INDEX.md      orientation — read first; routes to the two READMEs below
├── tools/        what can be dispatched: README (index) + one detail file per workflow
├── references/   what to read before acting: README (map) + quest-cluster · provider-gotchas
│                 script-skeleton · handoffs · shared-context · external-patterns
│   └── benchmarks/  one page per benchmark, grouped by process folder — transition · action
│                     interpersonal · tasks. Everything true of one benchmark and not the others
├── agents/       watcher · evaluator · executor · reviewer · tracker · summarizer
├── workflows/    run-model · run-fast · fix-broken-run · verify-change · scale-shards
│                 compare-providers · check-status · harvest-patterns
└── memory/       gitignored — personal environment only
```

Three layers, each with one job: `CLAUDE.md` states rules, `INDEX.md` orients, the two READMEs route.
A README lists and points; it never explains. The main session is the planner; no subagent can
dispatch another. Workflows are committed so they outlive the session that wrote them.

## Conventions worth not rediscovering

- **A vendored folder carries no `.git`.** A nested repo is recorded by the parent as a bare gitlink,
  so not one of its files would be committed. Strip `.git` before adding one. **The file that
  recorded each copy's upstream URL and commit is no longer in the tree**, so vendored provenance is
  currently unrecorded — re-establish it before relying on any claim about which upstream a folder
  came from.
- **Remotes:** `origin` and `backup` are ours and both get pushed; `upstream` (cpzambo/hai-teams) is
  the collaborator's and is fetch-only in practice.

## Open work

1. **Judge record — done 2026-08-19.** `LLM_as_judge/JUDGE_RECORD.md` is the single filled record:
   all thirteen fields for Wonderbread, MultiChallenge and AwareBench, plus verbatim prompts. The
   seven benchmarks with no LLM judge get no record — they are named in its opening section. Three
   findings from writing them change downstream work: Wonderbread's judge covers **SOP Generation**
   as well as QA (so the call budget scales with SOP length, not with item count); MultiChallenge's
   harness raises `TypeError` before its first API call and needs a one-line patch; and AwareBench's
   judge prompts are not in the repo at all — they must be transcribed from paper Figures 8–10
   before that run can be faithful.
2. **AwareBench run.** Scope is decided (AwareEval, not `New/`) and the output templates are written,
   but no generation has run. Budget per model: 4,075 generation calls + 120 judge calls.
3. **Three benchmarks have no runner.** Multi-party Goal Tracking, Wonderbread and MultiChallenge are
   vendored but have no per-provider harness, no SLURM script, and no results.
4. **Provider coverage is uneven.** DocVQA has two providers where bbh and mmlu have seven; whether
   that gap is closed is a scope decision, not an oversight to fix silently.
5. **The pre-submit Quest gate covers one benchmark.** `check_quest_sync.py` hardcodes
   NegotiationToM and globs `NEG_*`, so an `sbatch` for any other benchmark gets *in sync* from a
   comparison that never looked at it. Deferred on 2026-08-22 because the working scope is local;
   **fix it before the first non-NegotiationToM submit**, by taking the benchmark as an argument and
   reading its remote path and globs from its page.
6. **`quest-cluster.md` is 7.5 KB, past the ~5 KB split rule.** Declared in
   `.claude/doc-exceptions.json` rather than excused: the split has a decision in it — transfer and
   the gate on one side, SLURM and reading live state on the other.
