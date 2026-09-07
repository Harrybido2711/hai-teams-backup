# MMLU — benchmark card

<!-- size-budget: 7000 -->
<!-- One job — the card for one benchmark — and it runs long for reasons bbh's does: nine slots,
     two coexisting layouts, two prompts that are not interchangeable, two scorers still in play,
     and a broken run kept as a record beside the folder that finished it. Raised 2026-09-07 when
     the results table landed; the split that would shrink it is a scoring page like bbh's, and
     that is worth doing when the uniform rescore happens, not before. -->

General task ability, multiple choice. Accuracy. No LLM judge.

## Paths

| | Path |
|---|---|
| Local | `Tasks_benchmarks/mmlu` |
| Quest | **`/projects/p32983/Tasks_benchmarks/mmlu`** — this account's own copy, synced 2026-08-30, 29 files verified byte-identical by `md5sum`. Code and data only |
| Quest — not ours | `/projects/p32983/mmlu` is **`cpz1698`'s**, flat, last touched 2026-06-09. Do not write into it |

## Layout — rebuilt 2026-08-29 on the EmoBench convention

`MMLU_<Slot>/` per model, holding `<vendor>_mmlu_eval.py`, `run_mmlu.sh` and
`results/<Subject>/<model-slug>.{jsonl,csv}` + `_overall.csv`. The 13 subject JSONs live in `data/`
and a shared `mmlu_eval_core.py` owns the scorer, both prompts and the write path.

**Two layouts coexist, and only the newest slots use the one described above.** The seven older
slots are flat — `<vendor>_<Subject>.csv` beside a `<vendor>_overall_results.csv` roll-up — while
`MMLU_GPT_5.6_Luna`, `MMLU_Gemini_Flash3.5lite_OpenRouter` and `MMLU_Gemini_Flash3.5lite_Google`
use `results/<Subject>/`. Count the subject CSVs, never the roll-up: **Gemma's covers 8 of 13
subjects and Qwen's is an empty file, yet both have all 13 on disk** — the same trap bbh's
slot-level roll-up carries.

**`MMLU_Gemini_Flash3.5lite_Google`, added 2026-09-07, is where the Gemini slot is being finished.**
The OpenRouter run of 2026-08-30 wrote all 3,943 rows but 2,188 of them empty: its balance ran out
mid-run (HTTP 402, `limit_source: openrouter_credits`) and the four subjects after `Miscellaneous`
are 100% empty. `MMLU_Gemini_Flash3.5lite_OpenRouter/` is kept **untouched as the record of that
run**; this folder began as a byte-identical copy of its `results/` and is being completed on the
native Google AI Studio route, which the user chose on 2026-09-07 knowing the two routes are not
the same condition. **Every row's `config` column names its route** — carried-over rows carry
`reasoning_effort=minimal` and `backend=`, new ones `route=google_aistudio` and
`thinking_budget=128` — so the mix is legible rather than silent. Report it as two routes.

`MMLU_Llama` has a runner and no subject CSVs at all.

## Expected counts

**13 subjects, 3,943 items**, counted 2026-08-29. Sizes are very uneven (100 to 895), so the
macro-average over subjects the workbook reports is **not** the same as pooling all items.
`answer` in the data is an **index as a string** — `"2"` means `choices[2]`.

## Results — every model that has a runner has run, verified 2026-09-07

All 13 subjects / 3,943 items each. Macro is the mean of the 13 per-subject scores, read from the
per-subject files — **never from `<vendor>_overall_results.csv`**, which is stale for two slots.

| Slot | Folder | Macro | empty | Scorer | Among the six |
|---|---|---|---|---|---|
| OpenAI | `MMLU_GPT_5.6_Luna` | **0.9176** | 0 | `mmlu_lenient_v1` | yes |
| Deepseek | `MMLU_Deepseek` | **0.9174** | 0 | per-runner `==` | yes |
| Gemini | `MMLU_Gemini_Flash3.5lite_Google` | **0.9135** | 0 | `mmlu_lenient_v1` | yes — **two routes** |
| Gemma | `MMLU_Gemma` | **0.9071** | 3 | per-runner `==` | yes |
| XAI | `MMLU_XAI` | **0.9018** | 0 | per-runner `==` | yes |
| Qwen | `MMLU_Qwen` | **0.8802** | 20 | per-runner `==` | yes |
| — | `MMLU_Gemini_Flash2.5` | 0.8811 | 0 | per-runner `==` | no — superseded |
| — | `MMLU_GPT_4o_mini` | 0.8011 | 0 | per-runner `==` | no — superseded |
| — | `MMLU_Llama` | — | — | — | no — never produced rows |
| — | `MMLU_Gemini_Flash3.5lite_OpenRouter` | 0.607 (unusable) | 2,188 | `mmlu_lenient_v1` | no — the broken run, kept as a record |

**Gemini's column is two routes and is kept out of `Final_Result.xlsx`** — the user's decision,
2026-09-07. It is a model result in `Results.xlsx` and nothing more until a single-route run exists.

**Two scorers are still in play here, and that is the open item.** Only the two newest slots import
`mmlu_eval_core`; the other seven carry the score their own runner wrote with `==`. Until a uniform
rescore is run, a small gap between two columns may be the scorer rather than the model — the exact
condition the one-scorer rule exists to remove, and bbh moved by 0.19–0.64 when it was fixed there.
The rescore is offline work: the responses are all on disk.

Per-subject cells live in the workbooks, `Results.xlsx` for all nine columns and `Final_Result.xlsx`
for the five of the six it carries, each with its sources on the `Provenance` sheet.

## Two prompts, and they are not interchangeable

v1 (Deepseek, GPT-4o-mini, Gemini-2.5) shows the choices as a raw list and asks for the answer
**text**; v2 (Gemma, Llama, Qwen, XAI) labels them `A.`–`D.` and asks for a **letter**. Four runners
were asked for a letter and three for the text — a materially different task, not a formatting
difference. **New runs default to v2**, which leaves Deepseek alone on v1 among the six. The prompt
version is part of the run config and a resume across a change of it is refused.

## Scoring — one matcher, imported, for every model

`mmlu_eval_core.py::score_response`, `mmlu_lenient_v1`. **MMLU had exactly bbh's split**: the
`*_eval.py` runners compared text with `==` while a separate `*_rescore.py`, written for only three
of seven providers, accepted a letter, an index or letter-plus-text. Seven branches now, all naming
the same choice a different way; the two loosest fire only when the model emitted `Final Answer:`.
Built on the lessons bbh paid for across five scorer versions — [bbh-scoring.md](bbh-scoring.md).

## Its own traps

- **The rescore scripts are the cheap path.** A scoring change does not need a rerun: `*_rescore.py`
  re-derives the numbers from stored responses. Check for one before spending a provider call.
- **A `dotenv/` directory sits among the provider subdirectories** — it is not a provider.
