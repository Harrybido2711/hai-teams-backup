# Keeping things in sync

One instruction usually touches more files than it names, and drift is silent by default.

Layer 1 also **reports what mentions the files being committed and was not committed with them**.
That is where drift starts, and the commit is the last cheap moment to see it. It is a report, not a
failure: a mention often needs nothing.

| Layer | What must match | Enforced by | Fires |
|---|---|---|---|
| 1 · local ↔ local | documents with each other | `scripts/check_docs.py` via `.githooks/pre-commit` | every commit |
| 2 · local ↔ Quest | code on disk with code on the cluster | `scripts/check_quest_sync.py` via the `PreToolUse` hook | any command containing the submit keyword |
| 3 · local ↔ git | the working tree with both remotes | the rule in `CLAUDE.md`; `.githooks/post-commit` reports | every finished change |

Layer 1 rides on layer 3 on purpose: since every finished change has to be committed, the commit is
the one moment every change reliably passes through.

## Does layer 2 apply to this task?

Layers 1 and 3 always run. Layer 2 is the only conditional one, and the test is narrow: **did this
task change a file that also exists on the cluster?** A runner, a shared core, an sbatch script or a
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

## Layer 3

Committed and pushed to both `origin` and `backup`, per `CLAUDE.md`. `post-commit` only reports what
is unpushed; it never pushes, because publishing stays a decision someone makes.

## Disagreeing with the check

`git commit --no-verify` exists. Using it says the fix is the *next* commit, not that the finding was
wrong. A check bypassed routinely is the check to change — edit `check_docs.py` and say so.

## When the check itself fails

What each finding means, how to clear it, how to declare an exception, and the two contradictions no
mechanical check can see: [doc-check.md](doc-check.md).
