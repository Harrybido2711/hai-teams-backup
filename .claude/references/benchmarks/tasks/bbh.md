# BIG-Bench Hard — benchmark card

<!-- size-budget: 8000 -->
<!-- One job, not two: the card for one benchmark. It runs long because bbh carries eight
     providers, a broken run that must not be read as a result, and the incident that produced the
     project's one-scorer rule. The split that would shrink it already happened into
     bbh-parameters.md and the benchmark's own README. Raised again when the 20-task scope
     became a recorded decision rather than a gap someone might try to close, and again for
     scorer v3 — whose entry has to carry the 0.000 lesson, or it is just a version number. -->

General task ability. Exact match against a `"Final Answer: <answer>"` prompt contract. No LLM judge.

## Paths

| | Path |
|---|---|
| Local | `Tasks_benchmarks/bbh` |
| Quest | **`/projects/p32983/Tasks_benchmarks/bbh`** — this account's own copy, synced 2026-08-30, 43 files verified byte-identical by `md5sum`. Code and data only: results live locally and in git, because results flow *down* |
| Quest — not ours | `/projects/p32983/bbh` is **`cpz1698`'s**, flat, last touched 2026-06-09. Do not write into it |

## Layout — rebuilt 2026-08-29 on the EmoBench convention

`BBH_<Slot>/` per model, holding `<vendor>_bbh_eval.py`, `run_bbh.sh`, `log.txt`/`log.err` and
`results/<task>/<model-slug>.{jsonl,csv}` + `_overall.csv`, plus a `<model-slug>_bbh_overall.csv`
roll-up. The 20 task JSONs live in `data/` and are shared. **Result files are named after the model,
not the folder**, and `--model` sets both what is called and what is written, so a copied folder
cannot relabel another model's numbers.

**All ten slots have results**, and `BBH_Gemini_Flash2.5` / `BBH_GPT_4o_mini` are named for the
superseded models they call so their numbers are not mistaken for the current slots'. The two added
2026-08-29 — `BBH_Gemini_Flash3.5lite_OpenRouter` and `BBH_GPT_5.6_Luna` — are the only runners here
that comply with the model-parameter rule; the other eight set no reasoning or output cap,
deliberately, so their rows stay comparable. Their caps are still **chosen rather than measured**,
but both ran 4,833 rows with `no_marker=0`, so nothing was truncated at them.

**20 tasks, 4,833 items, and that is the settled scope** — seven of upstream's 27 are not vendored
here, and the user decided on 2026-08-29 to keep it that way: what was run before is what this
benchmark reports on. Do not add them to "complete" it; that would leave old models at 20 tasks and
new ones at 27. Verified 2026-08-29: every example carries a non-empty `input` and `target`, and all
36,638 result rows cross-check against the data files with zero mismatches.

Full tree, the six matcher branches and the task inventory: **`Tasks_benchmarks/bbh/README.md`** —
the benchmark's own committed notes, and the place to read before touching it.

## Results — the six are complete, verified 2026-09-07

Every slot is at the full 20 tasks / 4,833 rows except Kimi. Macro is the mean of the 20 per-task
`average_score` values read from **`results/<task>/<model>_overall.csv`** — not from the slot-level
`results/*_bbh_overall.csv`, which is stale for two slots (see the traps).

| Slot | Folder | Macro | no_marker | empty | Among the six |
|---|---|---|---|---|---|
| Gemma | `BBH_Gemma` | **0.9684** | 0 | 0 | yes |
| Deepseek | `BBH_Deepseek` | **0.9616** | 0 | 0 | yes |
| XAI | `BBH_XAI` | **0.9461** | 0 | 0 | yes |
| Gemini | `BBH_Gemini_Flash3.5lite_OpenRouter` | **0.9375** | 0 | 0 | yes |
| OpenAI | `BBH_GPT_5.6_Luna` | **0.9349** | 0 | 0 | yes |
| Qwen | `BBH_Qwen` | **0.9339** | 16 | 1 | yes |
| — | `BBH_Llama` | 0.9109 | 37 | 0 | no |
| — | `BBH_GPT_4o_mini` | 0.8451 | 4 | 0 | no — superseded |
| — | `BBH_Kimi` | 0.9310 *(10 tasks)* | 1 | 1 | no |
| — | `BBH_Gemini_Flash2.5` | 0.3455 | 3,002 | 0 | no — superseded, broken run |

Qwen's 17 unusable rows are all in `dyck_languages` and are scored wrong, not dropped; that task
reads 0.696. It is what the DeepInfra repair of 2026-08-30 left of 256.

**Per-task cells live in the workbooks, not here** — `Final_Result.xlsx` § Big Bench Hard for the
six, `Results.xlsx` for all ten, each with the sources on its `Provenance` sheet. Both were
refreshed from these files on 2026-09-07: 76 cells changed in `Results.xlsx`, 0 in
`Final_Result.xlsx`, which already matched.

**bbh ran locally, not on Quest** — `sacct` has no bbh job. Quest holds the code and data only.

## Scoring — one matcher, imported, for every model

`bbh_eval_core.py::score_response`, imported by every runner so no model can be judged more or less
generously than another. It is at **`lenient_v5`**, and each version came from a correct answer
being scored 0 for how it was written. **Full history, what each branch does, and the one line
deliberately not crossed: [bbh-scoring.md](bbh-scoring.md).**

The rule of thumb worth carrying out of it: **a task at exactly 0.000 with `no_marker=0` and
`empty=0` is a scorer bug, not a result.**

## Its own traps

- **`BBH_Gemini_Flash2.5` is a broken run, not a low score.** 62% of its 4,833 responses (3,002)
  stop mid-reasoning and never emit `Final Answer:`, so no scorer can rescue them and 0.3455 is what
  it is. It is **not** re-run: the Gemini slot is now `gemini-3.5-flash-lite`, which is complete.
  The row keeps its own column in `Results.xlsx` and appears nowhere in `Final_Result.xlsx`.
- **The slot-level `results/*_bbh_overall.csv` is stale for Gemma and Qwen.** The DeepInfra repair
  of 2026-08-30 re-ran only the affected tasks and overwrote each roll-up with just those —
  `MACRO_AVG_over_5_tasks` = 0.879 for Gemma, `over_13_tasks` = 0.9146 for Qwen, against the true
  0.9684 and 0.9339. **Aggregate the per-task files instead**; that is what both workbooks now do.
- **`Final_Result.xlsx` reproduces the per-task files exactly** — all 126 six-slot cells, 0 blanks,
  checked 2026-09-07. `Results.xlsx` did not, and was refreshed from them.
- **`kimi-k2.5` and `Llama-4-Maverick` are not among the six.** bbh is the only benchmark either ran
  on; Kimi has 10 of 20 tasks. `PLAN.md` and `Final_Result.xlsx` are the coverage claim, never
  `ls`.
- **`_superseded/` in `BBH_Gemma` and `BBH_Kimi`** holds older duplicates in the pre-restructure
  format, parked rather than deleted. Never read a number out of one.
- **No `seed` anywhere, Kimi at `temperature=1`, and no reasoning or output cap on the eight older
  runners.** Nothing here is reproducible. Those caps are **deliberately still open**: setting one
  changes what the models emit and would make new rows incomparable with the 4,833 on disk. Cap them
  when bbh is re-run. Per-model parameters, with `file:line`: [bbh-parameters.md](bbh-parameters.md).

## Fixed on 2026-08-29 — do not re-report these

Four traps this page used to carry are gone with the rewrite, and are recorded only so a stale memory
of them is not acted on: the two `.sh` files that submitted a `_finish` twin rather than the runner
their name implied; the narrowed `splits` re-run lists (`--task all` is now the default and the task
list is a single constant in the core); the `None` response that raised inside the per-split handler
and discarded a whole 250-item task; and the per-runner copies of the scorer.
