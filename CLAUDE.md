hai-teams — planner rules

## What this project is

A benchmark suite measuring whether LLMs can do the things a **team-process taxonomy** names —
*transition* processes (mission analysis, planning, goal specification), *action* processes
(monitoring progress, coordination), *interpersonal* processes (conflict, affect) — with general task
ability alongside them as a baseline. Ten benchmarks, each a vendored upstream repo plus this
project's own per-model runners. Runs execute on Northwestern's **Quest** SLURM cluster against eight
commercial models. Every model that runs gets a column in `Results.xlsx`; the six selected models
are what `Final_Result.xlsx` holds, and that is where a reported number is taken from. `PLAN.md` has
the split.

The work is empirical and the failures are quiet: a job that reports success while writing empty
rows, a scorer that penalises formatting, a number carried from one benchmark to another. Most rules
in this file exist because one of those already happened.

**Read [`.claude/INDEX.md`](.claude/INDEX.md) first.** It orients in one page and routes onward:
[`.claude/tools/README.md`](.claude/tools/README.md) for what can be dispatched,
[`.claude/references/README.md`](.claude/references/README.md) for what to read before acting.

This file holds **what the job is and the rules it runs under**. Each phase below names the file to
read and the tool to reach for — it points, it never copies. Anything explaining *how* to do
something belongs in a reference; anything cataloguing *what exists* belongs in the index. A summary
of either, pasted back here, is the thing that made this file 11 KB once before.

## What this project asks of you

Five things, in the order work moves through them. `.claude/INDEX.md` routes each to what it needs.

The project's memory is `.claude/references/` — committed, so it survives the session, and readable
by subagents, which your context is not. **The loop is the same in every phase: read the reference
before acting, and write what the work taught back into it afterwards.** A lesson left in a
transcript dies when the session ends.

**Retrieve, don't read.** `check_docs.py --brief <term>…` returns the matching sections whole;
`--model <id>` gathers one model across every file; `--impact <term>` is the work list before an
edit. Writing one runner touches six references, ~44 KB, of which about 15% gets used — reading them
all wastes context, and reading fewer is how a model was adopted with no invocation recipe. Open a
whole file when you are *editing* it; retrieve when you are *using* it. Pass the command to a
subagent rather than a list of filenames.

**1 · Analyse a new benchmark's repo.** Establish paths, counts, scoring and traps from the code.
Read the code before the paper; a value inferred from what a benchmark "probably" does is not a
finding, and an unestablished field is written as unestablished.

- *Memory* — read `references/benchmarks/README.md` for the page template and what is already
  covered, plus the benchmark's own committed notes named on its group page. Write a new page under
  `references/benchmarks/<group>/`, **and its row in the group index in the same edit**.
- *Tools* — `summarizer` when the answer needs a lot of reading and none of it belongs in context;
  `Explore` to locate files. No executor: nothing is being changed yet.

**2 · Write the per-model scripts and the template answer.** One runner per model, built from what is
already recorded rather than from scratch.

- *Memory* — `references/script-skeleton.md` for the runner shape and the invariants a diff is
  checked against; `references/model-calls.md` for how to reach that model at all — client,
  `base_url`, key, model id; `references/model-parameters.md` for the thinking and output limits
  **every** runner must set; `references/provider-gotchas.md` for that client's failure modes; the benchmark's
  page for counts, task names and output naming.
- *Tools* — `executor` once the change is decided, given the decision and not the problem;
  `reviewer` before it goes anywhere; the `verify-change` workflow when the change is meant to
  prevent a class of failure and has not yet been proven wrong.

**3 · Upload to Quest and run — but not before the user has verified the scripts.** Verification is
theirs, not yours. **Do not transfer and do not submit until they say the scripts are done**, however
ready the code looks. Phases 1, 2 and 5 need no such permission; this one always does.

**A real run executes on Quest. Local execution is for `--limit` smoke tests only** — the user's
rule, 2026-08-30, set after a full bbh sweep was run locally instead: correct data, but tied to one
laptop staying awake, invisible to Quest, and the cluster idle throughout. Probing a provider's
parameter surface and rescoring stored rows offline are still local work — they cost no cluster
time and make no run.

- *Memory* — `references/quest-cluster.md` for transfers, `md5sum`, SLURM and the two ways the
  pre-submit gate lies; the benchmark's page for its remote path and run order, which are not
  inferable from the local tree.
- *Tools* — `run-model` is the default and owns both sync directions; `run-fast` when it must finish
  today; `scale-shards` when the right parallelism is the open question; `executor` for a single
  decided submit.

**4 · Monitor the run.** Dispatch the agents, and turn a procedure into a workflow once it repeats —
a check you had to remember to run is a check that will be skipped.

- *Memory* — `references/handoffs.md` for what a dispatch must carry and the `STATUS:` vocabulary
  each agent returns; the benchmark's page for the counts to judge progress against.
- *Tools* — `check-status` first: read-only, two agents, cheap enough to repeat and safe beside a
  running supervisor. `watcher` for raw state, `evaluator` for whether the numbers can be believed,
  `fix-broken-run` when it has to be killed. `tracker` writes the outcome to the problem log.

**5 · Keep everything in sync.** Not a phase — the thing that runs through the other four. The
obligation is the next section; `references/sync-and-consistency.md` is the three layers and when
each applies, `references/doc-check.md` is what a check finding means, and
`check_docs.py --impact <term>` is what you run **before** editing to find every file a change
touches.

## Who decides

The planner is this session, not a subagent. **None of this project's six agents holds the `Agent`
tool** — checked against their `tools:` lines, 2026-08-22 — so none can dispatch another, and each
starts with no memory of the last. **Sequencing, and the decision to start or stop a job, stay
here.** Agents report; the planner acts on the report.

That guarantee is a property of those six definitions, not of subagents in general: a general-purpose
agent dispatched with the full tool set can spawn others, and the moment one is used the planner is
no longer the only thing sequencing work.

Every agent ends with a `STATUS:` line from a fixed vocabulary, so a dispatch can be branched on
without re-reading prose. Do not invent a second wording for a state that already has one.

## Standing authorisation: a broken run gets killed, not waited out

Granted 2026-07-29. **Do not ask before doing this:** `scancel` the affected job → fix and verify
locally → overwrite on Quest, confirming with `md5sum` → resubmit.

Letting a known-bad job run to the wall wastes the quota *and* the wall-clock slot. A Qwen pilot
burned 3h10m for 315 rows and 105 empty responses because the real fix had never left the laptop.

**Decide the checkpoint's disposition before resubmitting, and say which you chose.** Resume keeps
every row the old code wrote. One result set holding two configurations is worse than redoing rows.

## Every task ends with a sync pass

Synchronisation is not something big changes get and small ones skip. It is how this project stays
coherent, so **a task is not finished until the pass is done** — the same pass, every time.

**Sync per finished change, not per batch of them.** Two documents disagree because one was edited
and the other, which describes it, was not — and the window in which that is cheap to notice is the
commit. Every contradiction found in this repo so far began as an edit left sitting while the next
one started.

| Layer               | When it applies                                                                                                                 | What "done" means                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 1 · local ↔ local | **always**                                                                                                                | the consistency check passes, or every finding is declared with a reason          |
| 2 · local ↔ Quest | **only when the task changed something that also exists on Quest** — a runner, a shared core, an sbatch script, a config | Quest matches local, proven with`md5sum`, core and runners transferred together |
| 3 · local ↔ git   | **always**                                                                                                                | committed and pushed to`origin` and `backup`                                  |
| 4 · results ↔ record | **only when a model has finished a whole benchmark *and* the user has confirmed the run** | that model's numbers are in its benchmark page and in both workbooks, rebuilt from the result files on disk |

A change that touches only local files — documentation, notes, a script that never leaves the laptop
— skips layer 2 and nothing else.

**Layer 4 waits for the user, always.** A finished run is not a result until they say it is — the
same gate as phase 3, for the same reason: whether the numbers can be believed is their call, not
yours. Once they confirm it, that model reaches the record in **one** edit — the benchmark's own
page, `Results.xlsx`, and `Final_Result.xlsx` if it is one of the six — because a model recorded in
one of the three and not the others is exactly the drift the pass exists to catch. The user's rule,
2026-09-07.

**Skipping is a judgement you state, not one you make silently.** Say which layers you ran and why
any was skipped, in the report. An unstated skip cannot be told apart from having forgotten, and a
fixed pass is only worth having because it removes the chance to forget.

Detail on any of the four, and when layers 2 and 4 apply at all:
`.claude/references/sync-and-consistency.md`.

## Rules that hold on every task

- **Never submit without proving Quest matches local.** Two ways the automatic hook does not save
  you. It **fails open** — a warning that the check could not run is not a pass, and a stale path
  makes it protect nothing while still looking wired up. And it **only checks NegotiationToM**:
  `check_quest_sync.py` resolves that one directory and globs `NEG_*`, so an `sbatch` for any other
  benchmark passes a gate that compared someone else's files and said nothing about yours. Verified
  2026-08-22 — the hook is live and compares 41 files, all of them NegotiationToM's.
- **A sync's unit is the whole change, not one file.** Every locally modified file since the last
  transfer goes up together and is verified together — the shared core and its runners always, since
  the runners import the core. The user's rule, 2026-09-07.
- **Code flows up to Quest, results flow down.** Never the reverse.
- **Name a results directory after the model that produced it.** The user's convention, 2026-08-22.
  It is what makes our output distinguishable from the results a vendored copy shipped with — an
  unnamed `results/` is upstream's, and reporting one as ours is the mistake this prevents.
- **Every finished change is committed and pushed, to `origin` *and* `backup`.** Standing rule from
  the user, 2026-08-22, and it applies to any kind of change — code, results, documentation. A change
  that is finished and not pushed is a change that exists in one place. Do not batch a day's work
  into one commit at the end, and do not leave a modification sitting in the working tree.
  **`upstream` (cpzambo/hai-teams) is the collaborator's and is never pushed to.**
- **Stage explicit paths for git. Never `git add -A`** — an unattended loop that did swept unreviewed
  work into commits named "watcher checkpoint" and pushed them to both remotes. The rule above raises
  how *often* you commit; it does not relax what you are allowed to stage.
- **One scorer per benchmark, and it is the lenient one.** Standing rule from the user, 2026-08-29.
  Every model in a benchmark is judged by the same matcher, imported from that benchmark's shared
  core rather than copied into each runner. A strict scorer measures formatting, not reasoning:
  rescoring bbh's stored responses moved three models by 0.19–0.64. `references/script-skeleton.md`
  rule 7.
- **Judge a run by rows written, not by job state.** SLURM reports RUNNING for a process hung inside
  an API call, and a job can exit `COMPLETED 0:0` with every row empty.
- **Report evidence, not assertion.** Include the output. A partial result described accurately beats
  a claim of completion. Where uncertain, name the observation that would settle it.

## Rules that keep the documentation usable

The three routing files (`INDEX.md`, `references/README.md`, `tools/README.md`) are indexes. They
list and point; they do not explain.

- **A fact lives in exactly one place.** When something moves into a reference or a tool file, delete
  it from where it was — do not leave a summary behind. Two copies drift, and then an agent has to
  decide which is right.
- **Adding a file means adding its routing row in the same edit**, phrased as a condition an agent
  can recognise in its own task, not as a topic name. Nothing routes to it means nothing reads it.
- **Size is a signal, not a wall.** ~5 KB is the default nudge to consider splitting, and a file
  that is legitimately bigger declares its own with `<!-- size-budget: N -->`. The check reports it
  and never blocks. It used to block, and the cost was real: one file hit the limit four times in
  two days and each fix deleted the sentence explaining *why* a rule existed. Split when a file has
  two jobs, not when it crosses a number.
- **When a run exposes something an agent should have known, edit the file** — the reference for
  knowledge, the workflow for a check that should have caught it. A lesson left in a transcript dies
  with the session.
- **Before editing, grep what you are changing across the whole tree — that grep is the work list.**
  `python3 .claude/scripts/check_docs.py --impact <term>` prints it. An instruction names one file
  and usually touches several: the restructure of 2026-08-22 named `CLAUDE.md` and moved eight.
- **The commit is the checkpoint.** `.githooks/pre-commit` runs `check_docs.py` — links, orphans,
  structure, size, and the facts that must have exactly one home. A finding is either fixed or
  **declared in `.claude/doc-exceptions.json` with a reason**; nothing is left merely known. What
  each finding means and how to clear it: `.claude/references/doc-check.md`.
