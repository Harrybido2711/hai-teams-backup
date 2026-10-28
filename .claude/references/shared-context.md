# Shared context

Read what bears on your task before acting. These are committed, so they arrive with a clone and
stay in sync as the project moves — prefer them over anything remembered from a previous session.
**If one of them contradicts what you were told, say so rather than silently picking one.**

## Which document is authoritative on what

| Document | Authoritative on |
|---|---|
| `.claude/references/benchmarks/<group>/<name>.md` | **Everything specific to one benchmark** — its Quest path, layout, expected counts, output paths, run order and its own traps. Read the page for the benchmark you are working on, and its group page with it; a number from another page is not transferable |
| `.claude/references/benchmarks/README.md` | The index of all ten pages, and what a page is required to establish before its numbers are used |
| `LLM_as_judge/JUDGE_SELECTION.md` | **Everything about LLM judges** — which benchmarks need one, the literature, which judge model and why, the pilot comparing the four candidates, and the filled judge record a judged number needs before it is used (§7). Fifteen 2026 top-venue papers, PDFs in `LLM_as_judge/papers/` |
| `LLM_as_judge/PILOT_FINALISTS.md` | **The judge pilot's three finalists side by side** — Kimi K2.6, Haiku 4.5 and Haiku 5.5 on GPT's scores, agreement with the humans, stability and cost, and the case for and against Haiku 5.5. Read it when choosing the judge, or when a judge's pilot number is needed |
| `PLAN.md` | Repo map: what each folder is, provider coverage, and the state of each run |

A benchmark's own `*_script.md` / `*_SCRIPT.md` is authoritative on what a task *means*, but their
file listings go stale — verify listings against the tree.

## Repo layout

Benchmarks are grouped by the team process they measure — the grouping is the tracker's, so a
folder states what a benchmark is evidence for (reorganised 2026-08-19; paths before that date in
older notes are stale):

```
Transition_processes_benchmarks/   Awareness_in_LLM, LLMs-Planning_bench, Multi-party_Goal_Tracking_bench
Action_processes_benchmarks/       Wonderbread_bench, Multi-challenge_bench
Interpersonal_processes_benchmarks/ NegotiationToM, EmoBench
Tasks_benchmarks/                  DocVQA, bbh, mmlu
Random_stuff/                      SQA Release 1.0, TruthfulQA-main, sycophancy-eval-main
```

`PLAN.md` at the repo root is the map: what each folder is, which benchmark needs a judge, and what
state each run is in. Vendored folders carry no `.git` of their own, and the file that recorded which
upstream commit each came from is **no longer in the tree** — treat vendored provenance as unrecorded
until someone re-establishes it.

**On Quest nothing moved.** The remote layout is still flat under `/gpfs/projects/p32983/`, so a
remote path inferred from the local tree is wrong. Each benchmark's remote path is on its page.

Every benchmark uses **one folder per model** — a Python eval script, a SLURM `.sh`, a `results/`
directory. Copy the closest existing folder and swap the client; do not invent a new structure,
because the cross-model summary CSVs depend on this shape.

```
<BENCH>_<Provider>/            e.g. EMO_Qwen/, NEG_GPT/
├── <provider>_<bench>_eval.py
├── run_<bench>.sh
└── results/<TASK>/
```

Some benchmarks additionally factor their shared logic into a core module that every runner imports.
Where one exists, the core and the runners are transferred together or not at all — the page says
which file it is.

## Telling our results from the vendored copy's

**A results directory of ours is named after the model that produced it** — `NEG_GPT/`,
`EMO_Gemma/`, `OpenAI_result/`, `mmlu/llama/`. Stated by the user 2026-08-22 as a standing
convention, and it holds across every folder in the tree.

So a `results/` or `experimental_results/` directory that carries **no model name is upstream's
output**, shipped with the vendored copy. It is not evidence that anything ran here, and its numbers
are not ours to report. PlanBench ships two such directories and Wonderbread one.

## Counting rows

**Expected counts are per benchmark and live on its page.** Do not carry one benchmark's totals to
another, and do not infer a total from what a directory happens to contain.

Two ways a results directory lies, both hit in practice and both general:

- **A finished job proves nothing about whether its data is usable.** A run once exited
  `COMPLETED 0:0` with a perfect row count while two of its three tasks were 100% empty — the
  provider's credits had run out. Report the **non-empty `raw_response` rate and the null-`pred`
  count**, not just row counts.
- **Verify from the `.jsonl`, not the `.csv`.** Reasoning models emit newlines inside
  `raw_response`, so `cut -d, -f1` on the CSV mis-parses and can report *more* unique uids than
  rows. That false alarm looked model-specific and nearly triggered a needless re-run.
