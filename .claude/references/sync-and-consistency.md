# Keeping things in sync

<!-- size-budget: 6500 -->
<!-- One job — the four layers and when each applies — and it grew a layer on 2026-09-07 rather
     than a second job. Layer 4 carries its own procedure because it is the only layer nothing
     automatic checks: no hook fires when a finished model is left out of a workbook. -->

One instruction usually touches more files than it names, and drift is silent by default.

Layer 1 also **reports what mentions the files being committed and was not committed with them**.
That is where drift starts, and the commit is the last cheap moment to see it. It is a report, not a
failure: a mention often needs nothing.

| Layer | What must match | Enforced by | Fires |
|---|---|---|---|
| 1 · local ↔ local | documents with each other | `scripts/check_docs.py` via `.githooks/pre-commit` | every commit |
| 2 · local ↔ Quest | code on disk with code on the cluster | `scripts/check_quest_sync.py` via the `PreToolUse` hook | any command containing the submit keyword |
| 3 · local ↔ git | the working tree with both remotes | the rule in `CLAUDE.md`; `.githooks/post-commit` reports | every finished change |
| 4 · results ↔ record | a finished model's rows with its benchmark page and both workbooks | the rule in `CLAUDE.md`; nothing automatic checks it | the user confirms a model's completed run |

Layer 1 rides on layer 3 on purpose: since every finished change has to be committed, the commit is
the one moment every change reliably passes through.

## Does layer 2 apply to this task?

Layers 1 and 3 always run. Layers 2 and 4 are the conditional ones. Layer 2's test is narrow: **did
this task change a file that also exists on the cluster?** A runner, a shared core, an sbatch script or a
config: yes. Documentation, a benchmark page, a local-only script, a note: no.

**When the answer is yes, the unit is the whole change, not the file that made it yes** — every
file this task modified that also exists on the cluster goes up together and is hashed together
(`CLAUDE.md`). Half a change on Quest is drift that no later check attributes to this task.

Two ways to get it wrong: answering *no* because nothing is running — irrelevant, the question is
whether the file exists in both places, since the next submit reads whatever is there; and answering
*yes* by transferring under a live job — a wasted transfer, because the process has already imported
its modules. Cancel first.

Whichever way it goes, **state it**. Silence is indistinguishable from having forgotten.

## Layer 2 — know what it does not cover

The submit gate **fails open** and currently **checks one benchmark only**; both limits, and the
contract of the hook, are in [quest-cluster.md](quest-cluster.md). Closing the second one is item 5
of `PLAN.md` § Open work and is required before the first submit for any other benchmark. A gate
that reports *in sync* after comparing someone else's files is worse than no gate, because nobody
doubts a green result.

## Layer 4 — a finished model reaches the record

**Trigger:** a model has finished a whole benchmark — every task, every row — *and* the user has
confirmed the run is good. Both halves are required. Rows on disk are not a result until the user
says so, the same gate as phase 3 and for the same reason: whether the numbers can be believed is
theirs to judge. Do not write a model into the workbooks on the strength of a job that merely
exited.

**Then, in one edit, the model reaches three places:**

1. **Its benchmark's page** under `references/benchmarks/<group>/` — the results table: coverage,
   the headline score, and the unusable-row counts (`no_marker`, `empty`) that say whether the score
   can be read at face value. Per-task cells stay in the workbooks; the page holds the summary and
   the caveats.
2. **`Results.xlsx`** — always. Every model that has run gets a column here, selected or not.
3. **`Final_Result.xlsx`** — only if the model is one of the six. A model that is not selected never
   earns a cell here, and a blank stays blank until the *selected* model runs.

**Rebuild the cells from the result files on disk, never from another summary.** Aggregate the
per-task output, not a roll-up written by a previous run: bbh's slot-level `*_bbh_overall.csv` was
overwritten by a repair that re-ran five of twenty tasks, and reading it put Gemma into
`Results.xlsx` 0.089 low. The benchmark's page names its own authoritative file.

**Update the `Provenance` row in the same edit.** A number whose source row still describes the
previous run is worse than a blank, because nobody doubts it. Say the source file, the scorer tag,
the coverage, and what is left unusable.

**Then check the claims that outlive the run.** `PLAN.md` and `INDEX.md` carry per-benchmark
coverage sentences, and a finished model falsifies whichever one said it had not run.
`check_docs.py --impact <benchmark>` is that work list.

## Layer 3

Committed and pushed to both `origin` and `backup`, per `CLAUDE.md`. `post-commit` only reports what
is unpushed; it never pushes, because publishing stays a decision someone makes.

## Disagreeing with the check

`git commit --no-verify` exists. Using it says the fix is the *next* commit, not that the finding was
wrong. A check bypassed routinely is the check to change — edit `check_docs.py` and say so.

## When the check itself fails

What each finding means, how to clear it, how to declare an exception, and the two contradictions no
mechanical check can see: [doc-check.md](doc-check.md).
