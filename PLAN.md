# hai-teams — repository map

What this repo holds: a benchmark suite for evaluating LLMs against the **team-process taxonomy**
(transition / action / interpersonal processes, plus general task ability). Each benchmark is a
vendored copy of an upstream project plus this project's own runners; the runs execute on the
**Quest** SLURM cluster against six commercial providers, and the reported numbers converge in
`Final_result.xlsx` — with `Tempo_results.xlsx` holding the wider record of every model ever run (see
[Two workbooks](#two-workbooks-tempo_results-is-wide-final_result-is-what-is-reported)).

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
│   ├── papers/                          the judge literature's PDFs (2025–2026)
│   ├── JUDGE_SELECTION.md               the main judge document: decision, pilot and the judge record
│   └── PILOT_FINALISTS.md               the pilot's three finalists compared, and the case for Haiku 5.5
├── .claude/                             INDEX, tools, agents, references, workflows (see below)
├── CLAUDE.md                            planner rules only; `.claude/INDEX.md` is the entry point
├── AGENTS.md                            situation → fastest first move, for Claude and Codex alike
├── PLAN.md                              this file
├── README.md
├── Tempo_results.xlsx                   every model ever run — the wide record
├── Final_result.xlsx                    the selected models (five since 2026-10-05) — what gets reported
├── Criteria_results.xlsx                accuracy beside the six criteria, per benchmark × selected model — built, never hand-edited (`.claude/references/criteria-runs.md`)
└── quest_pull.log                       gitignored
```

The four category folders are **not** arbitrary grouping: they are the rows of the tracker that
drives this project, so a benchmark's folder states which team process it is evidence for.

## Two workbooks: Tempo_results is wide, Final_result is what is reported

Stated by the user, 2026-08-29; the user renamed the files on 2026-10-05 (`Results.xlsx` →
`Tempo_results.xlsx`, `Final_Result.xlsx` → `Final_result.xlsx`). Both workbooks carry the same six
sheets — `Big Bench Hard`, `MMLU`, `DocVQA`, `Emo`, `NegotiationToM`, `Awareness` — and differ only
in which model columns they are allowed to hold.

- **`Tempo_results.xlsx` records every model that has appeared in an experiment**, including ones that
  were tried and then dropped, and the two that were *replaced*. Its `Emo` sheet is the visible
  case: eight columns, the six slots plus `gemini-2.5-flash` and `gpt-4o-mini` in their own right. A
  leftover column is not a retracted result, the same way a leftover CSV is not — see
  `.claude/references/benchmarks/tasks/bbh.md`.
- **`Final_result.xlsx` records only the selected models** — one per vendor slot, named below —
  and it is the workbook a reported number is taken from. **Five since 2026-10-05: XAI is out.**

**XAI was removed from `Final_result.xlsx` on 2026-10-05 — provisionally.** The user's decision,
made after a discussion with their mentor, and it may be revisited. Every XAI column was dropped from
every sheet of `Final_result.xlsx`; nothing was deleted, because `grok-3-mini` keeps its column on
every sheet of `Tempo_results.xlsx`. Restoring it is a column copy, not a re-run. The rest of this
repo still says "the six" in many places; read that as the six vendor slots, of which five are
currently reported.

### The six, by name

Confirmed with the user 2026-08-29. The slot names are the workbook's column headers; the model id is
what a runner actually calls. **Two slots were re-pointed and the workbook has not caught up** — see
the warning under the table.

| Slot | Model id | Route | Where the recipe is |
| --- | --- | --- | --- |
| Gemini | `gemini-3.5-flash-lite` | OpenRouter (`google/gemini-3.5-flash-lite`) | `references/model-calls.md` |
| OpenAI | `gpt-5.6-luna` | OpenAI platform, `reasoning_effort="low"` | `references/model-calls.md` |
| XAI — **not in `Final_result.xlsx` since 2026-10-05, provisional** | `grok-3-mini` | xAI | `references/model-parameters.md` |
| Qwen | `Qwen/Qwen3.5-9B` | Together, `reasoning={"enabled": False}` | `references/model-parameters.md` |
| Gemma | `google/gemma-4-31B-it` | DeepInfra | `references/model-calls.md` |
| Deepseek | `deepseek-reasoner` | DeepSeek | `references/model-calls.md` |

**Row 2 of every sheet names the model behind each column.** In `Final_result.xlsx` it is `Model` —
one settled model id per slot, the same five on every sheet. In `Tempo_results.xlsx` it is `Model / config`,
because there a slot can hold a different model on one sheet than on another, and the config that
produced the number is part of what the number means.

**`Final_result.xlsx` never borrows a number from a model that is not selected. A blank means the
selected model has not been run on that sheet**, and it stays blank until it is. That rule is what
makes the two files different in practice: `gemini-2.5-flash` and `gpt-4o-mini-2024-07-18` are
superseded but are still what `NEG_Gemini` and `NEG_GPT` call, so their numbers never fill the
`NegotiationToM` sheet's `Gemini` and `OpenAI` columns of `Final_result.xlsx`. Nothing is lost —
those runs keep their columns in `Tempo_results.xlsx`. `Emo`, `Big Bench Hard`, `MMLU` and `DocVQA`
are all filled for both slots. On `NegotiationToM`, `OpenAI` is filled since 2026-10-12
(`NEG_GPT_5.6_Luna`, job 9644711) and **`Gemini` is the one gap a run closes**:
`NEG_Gemini_Flash3.5lite_OpenRouter` passed its pilot that day and its full run, job 9682468, was
submitted. `Awareness` is filled for all five since 2026-10-12, and DocVQA's Deepseek blank is
a modality ceiling.

The `Emo` result for `gpt-5.6-luna` is at the settled `low` since 2026-10-12 (`results/`, EU 0.690,
EA 0.685, overall 0.6875). The earlier default-`medium` arm (0.71) keeps its own column,
`GPT-5.6-Luna-medium`, in `Tempo_results.xlsx`: on EA it scored higher (p=0.008), and the user kept
`low` so luna runs one config on every benchmark (`.claude/references/model-parameters.md`).

**bbh is complete for all six slots** — `BBH_Gemini_Flash3.5lite_OpenRouter` (0.9375) and
`BBH_GPT_5.6_Luna` (0.9349), added 2026-08-29, have their full 20 tasks, so the Gemini and OpenAI
columns of `Final_result.xlsx` are filled on that sheet and no longer belong to the superseded
models. Those two keep columns of their own in `Tempo_results.xlsx`, and `gemini-2.5-flash`'s is a broken
run — 62% truncated before the answer, 0.3455 — kept as a record and not re-run
(`.claude/references/benchmarks/tasks/bbh.md`).

**MMLU is complete for every model that has a runner** — 13 subjects, 3,943 items, verified
2026-09-07 — with two exceptions that are not gaps: `MMLU_Llama` never produced rows, and Llama was
never among the six. `OpenAI` (0.9176) and `Gemini` (0.9135) both finished, both on a single route
and both reported.

**DocVQA is complete too, as of 2026-09-10** — `gpt-5.6-luna` (ANLS 0.8635) and
`gemini-3.5-flash-lite` (0.9394) ran on the four-column ceiling that benchmark has, so every sheet
that *can* be filled for the current pair was, apart from NegotiationToM, which was added to the
workbooks on 2026-10-05. `Awareness` was recorded for all five on 2026-10-12. MMLU's open item is not coverage but scoring: only its two newest slots
import the shared matcher, the other seven carry their own runner's `==`, and the uniform rescore is
offline work (`.claude/references/benchmarks/tasks/mmlu.md`).

`kimi-k2.5` and `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` were run on bbh only (llama also
on MMLU) and were never among the six.

So running a new model adds a column to `Tempo_results.xlsx` and **does not** earn one in
`Final_result.xlsx` unless that model is one of the six. Numbers still land in `Tempo_results.xlsx` first;
`Final_result.xlsx` is the selection made from it, not a separate measurement.

Both were rebuilt on 2026-08-29 from the result files on disk, and each carries a **`Provenance`
sheet** naming the source file behind every column and the reason behind every blank. Read that sheet
before trusting or extending a number; it is the part of the workbook that says where a cell came
from. The extras `Tempo_results.xlsx` holds and `Final_result.xlsx` does not: `XAI` on every sheet
(since 2026-10-05), `Kimi` and `Llama` on `Big Bench Hard`, `Llama` on `MMLU`, and the superseded
`Gemini-2.5-Flash` and `GPT-4o-mini` on `Big Bench Hard`, `MMLU`, `DocVQA`, `Emo` and
`NegotiationToM`.

**A blank cell means no usable number, not a zero.** `Awareness`/`Qwen` perspective is a real 0 —
170 refusals, kept by the user's decision (`Awareness_in_LLM/FULL_RUN_NOTES.md`). `MMLU`/`Qwen` and `MMLU`/`Gemma` **are no longer blank** — both always had
all 13 subjects on disk and it was their roll-up CSVs that were empty and partial, which is why the
sheet is now built from the per-subject files. `DocVQA` has no XAI or Deepseek run **and will not under the current six**: it is an image benchmark and those two are text-only, so those blanks are a ceiling rather than a gap (`.claude/references/model-calls.md`). `NegotiationToM`'s `Gemma` column is filled but carries a belief caveat — thinking off costs that task ~12.7 points — stated on the `Provenance` sheet.

**`Big Bench Hard` is now scored uniformly, and its numbers were refreshed to match.** Every model
on that sheet comes from `BBH_*/results/*_bbh_overall.csv` under the one shared lenient matcher
(scorer tag `lenient_v2`), so the sheet is reproducible from a single source and the old
strict-vs-lenient caveat is gone. The refresh moved one column a long way: `gemini-2.5-flash` fell
from the 0.9122 the workbook used to carry to **0.3387**, because 3,002 of its 4,833 stored responses
never emitted `Final Answer:` — a broken run no scorer can rescue, and the run behind the old number
is not on disk. It is kept in `Tempo_results.xlsx` as a record; the model is superseded and will not be
redone.

## Benchmark index

| Folder                                             | Benchmark      | Team process                               | Upstream                      | LLM judge?                                           | Result files present for                                       |
| -------------------------------------------------- | -------------- | ------------------------------------------ | ----------------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| `Transition_.../Awareness_in_LLM`                | AwareBench     | mission analysis, formulation and planning | HowieHwong/Awareness-in-LLM   | no — its 60 judged rows were dropped 2026-10-05 | all five selected models, full run 2026-10-12; recorded |
| `Transition_.../Multi-party_Goal_Tracking_bench` | mpgt-eval      | goal specification                         | AddleseeHQ/mpgt-eval          | no — human review                                   | none yet (vendored 2026-08-19)                                 |
| `Transition_.../LLMs-Planning_bench`             | PlanBench      | strategy formulation                       | karthikv792/LLMs-Planning     | no — VAL/PDDL validator                             | none yet                                                       |
| `Action_.../Wonderbread_bench`                   | Wonderbread    | monitoring progress toward goals           | HazyResearch/wonderbread      | **yes** — QA, SOP generation, SOP improvement | judge pilot only — `gpt-5.6-luna` on a 10% sample, four candidate judges; GPT responses generated 2026-10-19, judged by all candidates (jobs 4482838, 4506836); choice open (`JUDGE_SELECTION.md` §6.4) |
| `Action_.../Multi-challenge_bench`               | MultiChallenge | coordination                               | ekwinox117/multi-challenge    | **yes** — every item                          | judge pilot only — `gpt-5.6-luna` on a 10% sample, four candidate judges; GPT responses generated 2026-10-19, judged by all four (job 4482838); choice open (`JUDGE_SELECTION.md` §6.4) |
| `Interpersonal_.../NegotiationToM`               | NegotiationToM | conflict management                        | HKUST-KnowComp/NegotiationToM | no — EM + micro/macro F1                            | GPT, Gemini, Gemma, Qwen, Deepseek, XAI                        |
| `Interpersonal_.../EmoBench`                     | EmoBench       | affect management                          | Sahandfer/EmoBench            | no — MCQ accuracy                                   | OpenAI, Gemini, Gemma, Qwen, Deepseek, XAI                     |
| `Tasks_.../DocVQA`                               | DocVQA         | general task ability                       | docvqa.org (registered download; baselines at mineshmathew/DocVQA) | no — ANLS                                           | OpenAI, Gemini, Qwen, Gemma — the four that take an image       |
| `Tasks_.../bbh`                                  | BIG-Bench Hard | general task ability                       | BIG-Bench Hard                | no — exact match                                    | 7 providers incl. Llama                                        |
| `Tasks_.../mmlu`                                 | MMLU           | general task ability                       | hendrycks/test                | no — accuracy                                       | 7 providers incl. Llama                                        |

"Result files present" means CSV/JSONL output exists on disk under that provider's name — it is not a
claim that the run is complete or that its numbers have been audited. `LLM_as_judge/JUDGE_SELECTION.md`
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
| `AGENTS.md`                                          | the fast path for any agent, Claude or Codex: situation → first move → the file that holds the detail. An index keyed by symptom; it holds no knowledge of its own |
| `.claude/INDEX.md`                                   | the entry point: project goal and stage in one page, the terms this project uses in a specific way, and the three files always read first |
| `.claude/tools/README.md`                            | the dictionary of what can be dispatched — five baseline workflows, eleven skills and six agents, one row each, with a detail file per workflow |
| `.claude/references/sync-and-consistency.md`         | the three sync layers — local↔local, local↔Quest, local↔git — what enforces each, and when the Quest one applies at all |
| `.claude/references/doc-check.md`                    | what every consistency-check finding means and how to clear it — read this when a commit is blocked |
| `.claude/references/benchmarks/<group>/<name>.md`    | per-benchmark operating detail: Quest path, layout, verified counts, output naming, run order, its own traps — one page for each of the ten, plus a group page for what a process folder's benchmarks share. The rest of `.claude/` is benchmark-agnostic on purpose |
| `LLM_as_judge/JUDGE_SELECTION.md`                    | the main judge document: which benchmarks need a judge, the literature, the chosen judges and the pilot comparing them, and the filled judge record (§7) — the PDFs are in `LLM_as_judge/papers/` |
| `LLM_as_judge/PILOT_FINALISTS.md`                    | the judge pilot's finalists — Kimi K2.6, Haiku 4.5, Haiku 5.5 — side by side, and the case for and against Haiku 5.5 |
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
├── skills/       the steps — analyse-benchmark · write-runner · quest-sync · submit-run
│                 check-run · kill-and-resync · pull-results · audit-results · rescore-offline
│                 record-results · sync-pass
├── agents/       the roles — watcher · evaluator · executor · reviewer · tracker · summarizer
├── workflows/    the baselines — new-runner · launch-run · monitor-run · fix-run · finish-run
└── memory/       gitignored — personal environment only
```

Three layers, each with one job: `CLAUDE.md` states rules, `INDEX.md` orients, the two READMEs route.
A README lists and points; it never explains. The main session is the planner; no subagent can
dispatch another. Workflows are committed baselines — each phase names its agent and the skill it
follows, and none holds a benchmark-specific path — so they are adapted to a task, not multiplied.

## Conventions worth not rediscovering

- **A vendored folder carries no `.git`.** A nested repo is recorded by the parent as a bare gitlink,
  so not one of its files would be committed. Strip `.git` before adding one. **The file that
  recorded each copy's upstream URL and commit is no longer in the tree**, so vendored provenance is
  currently unrecorded — re-establish it before relying on any claim about which upstream a folder
  came from.
- **Remotes:** `origin` and `backup` are ours and both get pushed; `upstream` (cpzambo/hai-teams) is
  the collaborator's and is fetch-only in practice.

## Open work

1. **Judge record — done 2026-08-19; one document since 2026-10-19.** `LLM_as_judge/JUDGE_SELECTION.md`
   is the only judge document — the user had the folder cut to it on 2026-10-19. Its §7 is the
   filled record for MultiChallenge and Wonderbread, its §1 names the seven benchmarks that need
   none and why AwareBench's judged rows were dropped (2026-10-05). Three findings from writing the
   record changed downstream work: Wonderbread's judge covers **SOP Generation** as well as QA (so
   the call budget scales with SOP length, not item count); MultiChallenge's harness raises
   `TypeError` before its first API call; Wonderbread's SOP-Improvement scorer never runs.
2. **AwareBench run.** Scope is decided (AwareEval, not `New/`, and without the 60
   `mission_open-ended` rows). All five selected models ran in full on Quest on 2026-10-12 —
   4,015 rows each, `COMPLETE 1`; confirmed and recorded in both workbooks the same day. Open:
   criteria 4–5 need repeat runs on a subsample, not yet run; a
   known scorer gap is documented, not applied (`Awareness_in_LLM/FULL_RUN_NOTES.md`).
   `.claude/references/benchmarks/transition/awarebench.md`.
3. **Two benchmarks have no runner.** PlanBench and Multi-party Goal Tracking are vendored but have
   no per-provider harness, no SLURM script, and no results. Wonderbread and MultiChallenge have
   the judge pilot's runners (2026-10-19): `gpt-5.6-luna` on a 10% sample of each, graded by the
   four candidate judges and compared by the advisor's rule — cheap if they agree, expensive only
   if it is clearly better (`LLM_as_judge/JUDGE_SELECTION.md` §6.4). GPT's responses were
   generated on Quest 2026-10-19 (jobs 4480406, 4480407) and judged by all four the same day (jobs
   4482838, 4506836). Kimi K2.6 or Haiku 5.5 is the open choice (`LLM_as_judge/PILOT_FINALISTS.md`).
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
