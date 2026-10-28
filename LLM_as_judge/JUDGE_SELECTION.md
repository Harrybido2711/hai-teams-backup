# Judge selection — which benchmarks need an LLM judge, what the literature says, and which model we use

<!-- size-budget: 48000 -->
<!-- The one judge document, by the user's decision of 2026-10-19: the argument, the decision, the
     pilot, and the record every judged number needs. Large because it is all of them. -->

**Status, 2026-10-19.**
- **This is the main judge document.** On 2026-10-19 the user had `LLM_as_judge/` cut to this one
  file. On 2026-10-28 they asked for the pilot's finalists to be written up beside it, so the
  three-way comparison now lives in [PILOT_FINALISTS.md](PILOT_FINALISTS.md). What the others held
  now lives here: the documentation rule and the filled judge record
  (§7), the decided and open questions (§1, §8), and the paper list (§9). The per-paper, page-cited
  extractions were not carried over; the PDFs are in `papers/`.
- **The provisional default judge is Claude Haiku 4.5** — the pilot argues against it (§6.4).
- **The final choice is made by a bake-off on our own human-labelled data.** That bake-off has not
  run yet, and the human labels it needs have not been collected.
- **A smaller judge pilot comes first (§6.4).** `gpt-5.6-luna`'s responses to a 10% sample were
  generated and judged on 2026-10-19 (jobs 4482838, 4506836). Result (§6.4): GPT's scores barely
  depend on the judge; against the humans Kimi K2.6 is closest, consistently but not decisively;
  Haiku 4.5 is never better than Kimi and costs more; Sonnet 5.5 is dropped. Kimi K2.6 or Haiku 5.5
  is the open choice (§8). Probing changed two facts below — Kimi K2.6's price, and Sonnet 5.5's
  refusals (§6.1).

## Summary

1. **Two of the suite's ten benchmarks need an LLM judge:** MultiChallenge and Wonderbread. Between
   them they have three judged tasks. Every judge model they shipped with is retired, so a
   substitute is forced.
2. **The substitute must not share a family with any model we evaluate.** For MultiChallenge it
   must not be lenient; for SOP Generation it must not be over-strict; and it must be cheap enough
   for SOP Generation's call volume.
3. **Fifteen papers from 2026 top venues** show three things:
   - A light judge is viable for narrow, one-item-per-call questions like ours.
   - Its main risk is passing responses that should fail.
   - Which way a judge errs depends on the judge, so it has to be measured, not assumed.
4. **Four out-of-family candidates go to a bake-off:** Claude Haiku 4.5, Claude Sonnet 5.5, Kimi
   K2.6 and Claude Haiku 5.5. We take the cheapest one that passes a bar fixed in advance, and
   prefer one judge for all three tasks.
5. **Reported scores will be corrected for the judge's measured error rates,** with confidence
   intervals, and declared as not comparable to the original papers' numbers.

---

## 1. Which benchmarks need an LLM judge

The rule: a benchmark needs a judge record wherever **a model's opinion enters the score** (§7).
Then the number cannot be recomputed from the dataset and the responses alone.

**Seven of the ten need no judge.** Each is scored against a key or by a symbolic checker:

| Benchmark | How it is scored | Scoring code |
|---|---|---|
| BIG-Bench Hard | Exact match on the extracted final answer | `openai_eval.py:42` |
| MMLU | Accuracy on the parsed letter | `openai_eval.py:43`; `*_rescore.py` re-scores offline |
| DocVQA | ANLS against the gold answer list | `openai_eval.py:103, 116, 225` |
| EmoBench | MCQ accuracy, majority vote over four answer-order permutations | `OpenAI_result/openai_emo_eval.py:116-153` |
| NegotiationToM | Grouped exact match (Desire, Belief) and micro/macro F1 (Intention) | `neg_eval_core.py:14, 899-912` |
| PlanBench | The VAL/PDDL validator — plan validity is decidable | `plan-bench/response_evaluation.py:74, 104-107, 139, 229` |
| Multi-party Goal Tracking | Exact match on gold `[MASK]` strings, with the residue reviewed by **a human**, not a model | described in the paper only |

**Two things look like a judge and are not.** mpgt's "manual review" is a person — substituting a
model there redefines the metric. And a `--model GPT4` flag in a benchmark's task runner names the
**model under test**: four of Wonderbread's six subtasks (demo segmentation, demo validation, SOP
ranking, and the generation side of the judged two) use it that way.

**Three shipped with a judge.** One of them has since been dropped:

| Benchmark | Judged part | Status |
|---|---|---|
| **MultiChallenge** | All 273 items | **Kept.** It has no gold answers; its human-written per-item rubric was accepted as the reference by the user on 2026-10-05 |
| **Wonderbread** | Question Answering and SOP Generation | **Kept**. A third judged subtask, SOP Improvement, has a scorer that never executes, so it is out of scope (§7.5) |
| AwareBench | 60 of 4,075 rows (`mission_open-ended`) | **Dropped 2026-10-05** by the user. The 60 rows have no per-item reference or rubric — one general instruction judges all of them — and the paper's own scores for them are 33.33 under one evaluator prompt and 61.67 under the other. The paper weights its 15 dimensions equally, so those 60 rows carried 1/15 of the headline; dropping them raises the paper's own 13 models by about 3 points and flips one pair of ranks. Consequences for the run: `AWARENESS_NOTES.md` §5.0 |

That leaves **three judged tasks**:

| Task | What the judge decides | Calls per evaluated model | Reference given to the judge | Original judge |
|---|---|---:|---|---|
| **MultiChallenge** | YES/NO: does the final response satisfy one human-written rubric question? | 273 | The rubric only; no gold answer exists | `gpt-4o-2024-08-06` |
| **Wonderbread QA** | A 1–3 score (1 = best) on each of four criteria: completeness, soundness, clarity, compactness | 480 | A human answer, for completeness and soundness only | `gpt-4-0125-preview` |
| **Wonderbread SOP Generation** | For each line of one procedure, the index of the matching line in the other, or −1, in both directions. Precision, recall and ordering are tallies of these decisions | ~3,100 per input ablation | The human-written gold SOP | `gpt-4-1106-preview` |

SOP Generation's count is 162 rank-1 gold demos × about 19 lines per pair, once per input ablation;
upstream runs three (task description; + screenshots; + screenshots and actions).

**Substitution is forced.** All of these snapshots are retired, so an exact reproduction is
impossible at any price. A substituted judge must be declared (§7.6). Its numbers are not
comparable to the published ones and are never tabulated beside them.

## 2. What the replacement judge has to get right

These requirements follow from the three tasks, before any paper is read.

| # | Requirement | Why |
|---|---|---|
| R1 | **No family in common with any evaluated model** | A judge that grades its own family's outputs can favour them. Our models come from six vendor slots, listed in [PLAN.md](../PLAN.md) |
| R2 | **Few false PASSes on MultiChallenge** | Humans pass only about 23% of responses. A lenient judge inflates every score, and raw agreement hides it: an always-FAIL judge already agrees with humans about 77% of the time |
| R3 | **No under-matching on SOP Generation** | A judge that refuses valid matches lowers both precision and recall |
| R4 | **Cheap at SOP Generation's volume** | About 3,100 calls per model per ablation. The user prefers a light judge if the evidence allows one |
| R5 | **Stable and declared** | A pinned snapshot, repeated runs to measure stability, and every setting logged |

R2 and R3 pull in opposite directions: MultiChallenge is safest with a strict judge, SOP Generation
with one that is not over-strict. That is why the judge's error direction has to be measured
separately on each task.

## 3. The literature

**Selection.**
- Only papers accepted at a 2026 top venue: ICLR, ICML, ACL, EMNLP, NeurIPS or COLM. An arXiv first
  release in 2025 is allowed; 2024 is not.
- Each acceptance was confirmed on an official source: the conference's accepted-paper data, the
  ACL Anthology, or EMNLP 2026's programme sheet.
- Fifteen papers were kept: five from ICML, three each from ICLR and COLM, two from ACL, and one
  each from NeurIPS and EMNLP. Each was read in full.
- The benchmark's own paper, MultiChallenge (Findings of ACL 2025), is used as a primary source.
- The PDFs are in `papers/`. One, Peng (*RuVerBench*), is under arXiv's default non-exclusive
  licence; both git remotes are public, so it stays local (`papers/.gitignore`).

The fifteen answer three questions:

| Question | Papers |
|---|---|
| Which judge model? | Gosai (*Audio MultiChallenge*), Wen (*IF-RewardBench*), Pombal, Li (*Preference Leakage*), Roytburg, Naik, Krumdick |
| How should the judging call be posed? | Sharma (*ResearchRubrics*), Peng (*RuVerBench*), Ananthram (*PoSh*), Chang (*How2Everything*) |
| How should the judge be validated, and its scores reported? | Lee, Chen, Li J. (*Sparse Overlap*), Schwinn |

Full titles, venues and arXiv links are in §9.

## 4. What the literature established

Each finding below gives what the paper found, then what it changes for us. Numbers are the
papers'. Our own reasoning is marked *(our inference)*.

**F1 — Judges favour their own family, so family exclusion is a sound precaution.**
- **Self-preference survives objective rubrics.** On fully objective rubric items, judges were more
  than 50% more likely to pass a failed item when the output was their own, and the effect extends
  to the judge's family (Pombal).
- **Shared training data matters more than shared family.** Judges favoured models trained on
  their outputs: "inheritance" leaked nearly as much as being the same model, and more than being
  in the same family (Li).
- **But part of the measured effect is weakness.** Once the items a judge itself gets wrong are
  controlled for, only 51% of earlier self-preference findings stay significant (Roytburg).

*Consequence:* exclude every evaluated family (R1). The exclusion costs little, because strong
out-of-family judges exist. Also check, per evaluated model, whether a judge is softer on some
models' outputs than on others.

**F2 — Narrow, one-item-per-call questions are where light judges hold up.**
- **Small judges hold up on final answers.** A 9B judge was 6.6 points behind the best on final
  answers, but 17.8 behind on long coding trajectories (Peng).
- **Per-unit questions beat holistic frontier judging.** A 14B judge asking one question per unit
  beat holistic GPT-4o (Ananthram).
- **A checklist removes the multi-turn penalty.** Judges given a per-constraint checklist lost
  nothing on multi-turn items (Wen).
- **A correct reference can let a small judge beat a large one.** A 7B judge with a human reference
  beat GPT-4o without one (Krumdick).
- **The rubric beat the whole conversation by a wide margin.** MultiChallenge's own rubric judge
  agreed with humans 93.95% of the time. A judge given the whole conversation without a rubric
  agreed 37.33% (Sirdeshmukh).

*Consequence:* all three of our tasks already have this shape, so a light judge is defensible (R4).
Keep one item per call: putting 4–5 rubric items in one call cost 9–35 points on long inputs
(Peng).

**F3 — A light judge's main risk is passing what should fail.**
- **Small judges accept more flawed answers.** Small judges accepted flawed proofs 13.3 points more
  often than frontier judges, but rejected correct ones only 1.1 points more often (Naik).
- **Every judge catches violations less well than it confirms compliance.** Across 14 judges, F1 on
  the "violated" class ranged 0.15–0.68, against 0.75–0.91 on the "followed" class; humans scored
  0.744 on "violated" (Wen).
- **Haiku is more lenient than Sonnet.** On HealthBench's failed rubric items, Claude Haiku passed
  0.12 of them and Claude Sonnet 0.03 (Pombal).

*Consequence:* the bake-off ranks judges on their false-PASS rate, not on agreement (R2).

**F4 — Which way a judge errs depends on the judge, not just its size.**
- **Agreement hides strictness.** On reference-anchored procedure checking, Claude Opus 4.5 had
  only 6.1% false PASS but 38.2% false FAIL. Its pass rate was 34.5%, against 51% for humans. A
  6.5-point spread in agreement across judges hid a 26-point spread in pass rates (Chang).
- **Strictness can flip between domains.** One judge can be strict on one domain and permissive on
  another (Peng).

*Consequence:* measure both error directions on every task. A judge that is safe for MultiChallenge
can be harmful for SOP Generation (R2 vs R3).

**F5 — Wording changes results, so prompts stay verbatim.**
- **Small wording changes move scores.** A one-line strict/flexible suffix moved accuracy by −9.2 to
  +11.8 points (Peng). Swapping the prompt moved balanced accuracy by 27 points (Naik).
- **Rewritten rubrics do worse.** Rubric text expanded by an LLM lowered agreement with humans by
  15–22 points (Sharma).

*Consequence:* keep every upstream prompt, rubric and reference verbatim, so the judge model is the
only thing that changes. Never let an LLM rewrite them.

**F6 — Validation needs several raters on shared items.**
- **Little overlap picks the wrong judge.** When only 5% of items were labelled by more than one
  human, the validation reached the wrong verdict 25% of the time. It picked the wrong best of ten
  judges 65% of the time (Li J.).
- **The recipe.** At least 25% overlap, three to five raters, and overlap items chosen by
  stratifying on the first rater's label. At our scale of ~200 items, 100 double-labelled items give
  85–87% reliable verdicts; 50 give only 53–61%.
- **Reliable labelling needs a codebook.** Human agreement on judging procedures rose from α 0.273
  to 0.593 only after an iterated codebook and a qualification test (Chang).

*Consequence:* per benchmark, one rater labels ~200 items and two more label a shared panel of ~100.
Write and pilot a codebook before labelling.

**F7 — A raw judge pass rate is biased; correct it.**
- **The correction.** Measure the judge's specificity and sensitivity against human labels. Then
  report the Rogan–Gladen corrected pass rate, with an interval that carries the calibration
  uncertainty (Lee).
- **The per-model check.** When calibration items are a random sample of the same responses, the
  PPI++ estimator is more efficient (Chen).
- **Do not expect the correction to beat human labels.** In Lee's analysis, a judge plus calibration
  beats human-only labels only when the judge is quite accurate. At MultiChallenge's ~23% pass rate
  that means q ≳ 0.88 *(our arithmetic)*. None of seven current judges reached that region, Claude
  Haiku 4.5, Sonnet 4.6 and Opus 4.6 included (Lee).

*Consequence:* report the corrected rate and interval as the headline, with the raw judge rate
labelled as raw.

**F8 — Judge accuracy shifts with the model being judged.**
- **Which model wrote the output matters.** It moved judge accuracy more than which attack produced
  it (Schwinn). Judge rankings also changed with the generating model (Peng).
- **Agreement among judges is not correctness.** In Schwinn's study, judges were nearly unanimous
  and still wrong.

*Consequence:* draw the validation set evenly across evaluated models, and report judge error per
model.

## 5. From the findings to the candidates

**Excluded (F1):** every model from the six vendor slots.
- **The families:** Google (Gemini, Gemma), OpenAI (including GPT-oss), Alibaba Qwen, DeepSeek and
  xAI. xAI's removal from the reported results is provisional, so it is still treated as evaluated.
- **What this removes:** the top judge in several of the papers — o4-mini, Gemini-3-Pro, GPT-5.4.
- **Kimi and Llama stay eligible, on one condition.** Each has been run on other benchmarks in this
  suite (Big Bench Hard; Llama also on MMLU), but neither is one of the six. They stay eligible only
  while neither is run on MultiChallenge or Wonderbread.

**The remaining models, ranked by evidence.** The ranking weighs four things:
- how many of the fifteen papers tested the model as a judge;
- how close those tasks are to ours;
- whether the exact version we would call was tested;
- whether the model is light.

| Tier | Model | Papers | Assessment |
|---|---|---:|---|
| **A — bake-off** | 1 · Claude Haiku 4.5 | 3 | The only direct evidence on a MultiChallenge-style task: κ 0.808 against human graders, level with GPT-4.1 (Gosai). Its known weakness is leniency (F3) |
| | 2 · Claude Sonnet 5.5 | 5, on versions 4.5/4.6 | The most papers, and the strictest Claude judge. Version 5.5 itself is untested |
| | 3 · Kimi K2.6 | 1 | 2nd of 18 judges on rubric verification, level with Claude Opus 4.7 (Peng). Cheap; one paper only |
| | 4 · Claude Haiku 5.5 | 0 | Released 2026-10-07 and untested. Included only because it costs a tenth of Haiku 4.5 |
| **B — not recommended** | Claude Opus | 4 | Strong but not light, and fail-biased on procedures (F4). Useful as a reference |
| | GLM | 2 | Inconsistent, and weak at catching violations (Wen) |
| | Mistral Medium | 1 | Below Haiku 4.5 on the same task (Gosai) |
| **C — evidence against** | Llama | 5 | Consistently weak. Strong only when given a human reference (Krumdick) |

MiniMax and Cohere have no 2026 top-venue evidence. **No paper compares all four Tier A
candidates on the same task**, which is why the bake-off is needed.

## 6. The decision

### 6.1 Default and shortlist

| Role | Model | Price in / out per M tokens | Cost per full pass, all three tasks, five models |
|---|---|---|---:|
| **Default light judge (provisional)** | Claude Haiku 4.5 | $1 / $5 | ~$21 |
| Cheapest candidate, untested | Claude Haiku 5.5 | $0.10 / $0.50 | ~$2 |
| Cheap challenger | Kimi K2.6 | $0.70 / $3.50 on the pinned backend | ~$14 |
| Escalation if the light judges fail | Claude Sonnet 5.5 | $2 / $10 | ~$41 |

- **Where the costs come from:** OpenRouter list prices without reasoning tokens, one ablation of
  SOP Generation. Prices read 2026-10-08, Kimi's again 2026-10-19.
- **What costs the most:** human labelling (~400 labels per benchmark), not the API calls.
- **A settings difference:** Haiku 5.5 and Sonnet 5.5 accept no `temperature` setting on OpenRouter.
  For them, stability comes from repeated runs, not from temperature 0.

**Probed on OpenRouter, 2026-10-19,** with each benchmark's real judge prompts, before the judge
pilot (§6.4). The configurations that came out of it are `judge_core.JUDGES` in
`Action_processes_benchmarks/judge_core.py`.

| | Haiku 4.5 | Haiku 5.5 | Sonnet 5.5 | Kimi K2.6 |
|---|---|---|---|---|
| reasoning by default | off | **on** (322 tokens on one MultiChallenge item) | adaptive; **cannot be disabled** ("Reasoning is mandatory") | **on** (773) |
| pinned at | off | off | `effort: low` (0 tokens on every probe) | off |
| `temperature` | 0 | not listed — **silently dropped** if sent; refused (404) under `require_parameters` | not listed | 0 |
| backend, pinned, no fallback | Anthropic | Anthropic | Anthropic | **Crusoe** (bf16) |
| price in / out per M on that backend, 2026-10-19 | $1 / $5 | $0.10 / $0.50 | $2 / $10 | **$0.70 / $3.50** (the 10-08 figure, $0.44 / $2.45, was another backend's) |
| SOP Generation's line-matching prompt | answers | answers | **refuses — every real pair, every backend** | answers |

- **Reasoning at the lowest level each allows.** The upstream judges had no hidden reasoning,
  MultiChallenge's and SOP Generation's prompts already ask for visible reasoning, and it keeps the
  comparison between models rather than between thinking budgets. A reasoning-on arm (§6.2's "Haiku
  4.5 with a small budget") is not in the pilot.
- **Every call carries `provider.require_parameters=true`,** so no backend that would ignore a
  setting is ever chosen, **and is pinned to one backend with `allow_fallbacks=false`.** Kimi K2.6
  is served by 17 providers at int4, fp4, fp8 and bf16; unpinned, the smoke rows of one Kimi run
  came from two of them. Its maker's own endpoint (Moonshot AI) returns whitespace for
  MultiChallenge's JSON-mode call (3 of 3, schema and object mode) and refuses `temperature`, so
  Kimi runs on Crusoe — the unquantised weights, three identical answers in three at temperature
  0. The Claude models run on Anthropic's own endpoint.
- **Sonnet 5.5's refusal** is `finish_reason: content_filter` with `message.refusal`: "blocked as it
  seems to violate Anthropic's Terms of Service restrictions on reverse engineering or duplicating
  model outputs". The same on a synthetic and on upstream's real SOP pairs, and on every backend
  tried (Anthropic, Google, Azure, Claude Platform on AWS). QA's prompt passes (504 of 504 pilot
  calls). MultiChallenge's passed the probe and the smoke run but not the pilot: **11 of 81 calls
  refused**, same message, on 6 of 27 items (four Instruction Retention, two Reliable Version
  Editing) — and not consistently: one item was refused on one replicate and answered on the other
  two, so a refusal is a per-call outcome, not a property of the item. Those 11 are billed ($0.045);
  the SOP refusals are not. The likeliest trigger for SOP is the prompt's `"scratchpad": think step by step` field *(our inference,
  untested)*. Rewording upstream's prompt to get past it would break F5, so it stays verbatim and a
  refusal is recorded as its own status, which leaves Sonnet 5.5 unable to judge SOP Generation —
  one reason the pilot drops it (§6.4).
- **Claude fences JSON mode** (```` ```json … ``` ````) on OpenRouter; upstream's bare `json.loads`
  would have raised on it. The pilot's parser strips fences.

**Disclosure.** This analysis was written with Claude (Anthropic), and three of the four candidates
are Claude models. They are candidates because of the family-exclusion rule and the evidence above.
The bake-off decides.

### 6.2 How the final choice is made

1. **Five configurations** run on the same human-labelled items:
   - Haiku 4.5 without reasoning;
   - Haiku 4.5 with a small reasoning budget;
   - Haiku 5.5;
   - Kimi K2.6;
   - Sonnet 5.5.
2. **Validation sets** (F6, F8), drawn evenly across evaluated models:

   | Task | Primary rater | Two more raters |
   |---|---|---|
   | MultiChallenge | ~200 items | ~100 of them |
   | Wonderbread QA | the existing 30-item human-vs-GPT-4 sample, plus ~100 new items | 50 of the new items |
   | SOP Generation | every line decision, both directions, for ~12 demos | half the demos |

3. **Acceptance bars, fixed before any result is seen.** All are proposals, to adjust before
   running.
   - *MultiChallenge:*
     - specificity (1 − false PASS) ≥ 0.90 and sensitivity ≥ 0.85, each with an interval;
     - the leave-one-human-out test passed with three raters;
     - no evaluated model's false-PASS rate above 1.5× the lowest.
   - *Wonderbread QA:*
     - per criterion, agreement on the 30-item sample no more than 5 points below the original
       GPT-4 judge's;
     - the leave-one-human-out test passed on the new items.
     - A criterion where no judge passes is human-scored or reported as unvalidated, never given a
       lower bar. Clarity and compactness, which have no reference, are the likely cases.
   - *SOP Generation:* set before running, from false-match and miss rates in each direction. No
     published figure exists for line-level matching.
4. **Selection rule.** Among the configurations that pass, rank on the same items by false-PASS
   rate and Youden's J. Take the cheapest whose numbers are not meaningfully worse than the best.
5. **One judge for all three tasks — proposed 2026-10-12.**
   - *Within a benchmark, one judge for every evaluated model:* required.
   - *Across the three tasks:* preferred. Take the cheapest candidate that passes all three bars.
     Only a task where it fails gets its own judge, declared in that benchmark's record.

### 6.3 How results will be reported

- **Corrected pass rate as the headline.** Per evaluated model, the Rogan–Gladen corrected pass rate
  with its interval; the raw judge rate beside it, labelled raw; and a per-model PPI++ estimate as a
  check (F7).
- **The judge's error rates are published.** Specificity, sensitivity and agreement with humans, per
  task and per evaluated model.
- **Everything is declared.** The judge's model id, snapshot, settings and number of replicates go
  into the record (§7.6). Every number is marked as not comparable to the original paper's.

### 6.4 The judge pilot — set up 2026-10-19, before the bake-off

The advisor's design, agreed with the user on 2026-10-19: run the four candidates on one evaluated
model's responses first, and choose by a simple rule — **if the four give about the same results,
use the cheap one; if they differ a lot and the expensive one is better, use the expensive one.**
The user's reading of it for Sonnet 5.5 (2026-10-19): **if Sonnet comes out about the same as the
others, it is not considered further.**

- **What is judged.** `gpt-5.6-luna` on a simple random sample of 10% within each subsection —
  MultiChallenge's four axes (27 items), Wonderbread QA's eleven question templates (12) and SOP
  Generation's four websites (16 demos × 3 ablations). The user set the bounds at 5–10%; the top was
  taken because 5% of MultiChallenge is 14 items.
- **How.** Each benchmark's own judge prompt verbatim, each judge at its §6.1 configuration, three
  replicates. Code, counts and run order: the two benchmark pages under
  `.claude/references/benchmarks/action/`; the comparison is `Action_processes_benchmarks/compare_judges.py`.
- **Where "better" comes from.** For Wonderbread, all four judges also grade upstream's two
  human-labelled samples (30 QA answers, 30 SOP pairs), so agreement with *humans* is measured, at a
  few cents a judge. **MultiChallenge has no human labels on disk**, so there the pilot measures
  only cost, stability and agreement between judges. Agreement is not correctness (F8), so where
  the judges disagree on MultiChallenge, "better" needs the disagreeing items labelled by a person.
- **What it is not.** It is not §6.2's bake-off: one evaluated model instead of five, no three-rater
  panel, no acceptance bar fixed in advance. Its numbers choose between candidates; they are not
  reported scores.
- **Size and cost.** GPT's responses cost $0.62 (generated 2026-10-19). Its 48 SOPs come to 1,054
  lines over both directions, so about 5,500 judge calls per judge, nine-tenths of them SOP line
  matching. From the smoke run's billed calls, per judge: Haiku 4.5 ≈ $6, Kimi K2.6 ≈ $4, Sonnet
  5.5 ≈ $1.4 (its SOP calls are refused, unbilled; billed in the end $1.37), Haiku 5.5 ≈ $0.8 —
  about $13 in all. Four to five hours, the four judges in parallel. **The estimate was never set
  against the account:** the OpenRouter key had $15 bought and much of it spent, and job 4482838
  halted on billing at 13:34–13:56 after $6.35, every judge's SOP sample unfinished (Kimi's anchor
  too). Resumed after a top-up (job 4506836, 15:18–19:06). Billed in the end: Haiku 4.5 $7.69,
  Kimi K2.6 $5.41, Sonnet 5.5 $1.37, Haiku 5.5 $0.93 — $15.39.
- **Result for Sonnet 5.5** — MultiChallenge and QA finished for all four judges on 2026-10-19 (job
  4482838); SOP is the other three's. Report: `Action_processes_benchmarks/judge_comparison/`.
  - *MultiChallenge*: on the 23 items every judge labelled, Sonnet's macro is 46.7 against 36.1–44.5
    for the others; its agreement with each of them is κ 0.83–0.91, McNemar p ≥ 0.5 — no measurable
    difference. The 4 items it left without a majority verdict are its refusals.
  - *QA, against the 30 human-labelled answers* (QWK, completeness / soundness / clarity /
    compactness): Sonnet 0.55 / 0.38 / 0.07 / 0.33; Kimi K2.6 0.63 / 0.32 / 0.26 / 0.74; Haiku 4.5
    0.42 / 0.16 / 0.36 / 0.56; Haiku 5.5 0.42 / 0.20 / 0.26 / 0.12. Sonnet leads only on soundness,
    by 0.06 at n = 30.
  - *Cost per judged unit*: $0.015 (MultiChallenge) and $0.023 (QA) — 2–20× the others.
  - **Under the user's rule it is dropped**: no better where it answers, absent on SOP and on 4 of
    27 MultiChallenge items, and the most expensive. Proposed 2026-10-19; the user's confirmation is
    pending.
- **Result for the other three** — every set complete, 2026-10-19 (job 4506836). GPT's scores
  barely depend on the judge. Against the humans Kimi K2.6 is closest, by a margin n = 30 cannot
  confirm. Haiku 4.5 is out: never better than Kimi, and dearer. Kimi if agreement with the humans
  decides, Haiku 5.5 if the outcomes do — the user's and the advisor's call (§8). **The numbers,
  and the case for and against Haiku 5.5, are in [PILOT_FINALISTS.md](PILOT_FINALISTS.md)**
  (2026-10-28).

## 7. The judge record — what must be documented, and what is

A judge-scored number is not reproducible unless the judge itself is documented. **Nothing from a
judged benchmark enters `Tempo_results.xlsx` until its record is filled.**

### 7.1 The rule

The specification as given, word for word. The rest of §7 expands it and never rewords it; if the
two disagree, this block wins.

```text
For each benchmark, record the following:

Grading Setup
Grading model: What model graded the answers? Record the exact model name and version, when available.
Material shown to the model: Did it receive the question, tested answer, correct answer, background documents, or previous conversation?
Human comparison: Were model grades compared with human judgments? Record the sample size, potential few shot examples, agreement measures, and who the human graders were (students, researchers, etc.).
Grading instructions: Copy the complete instructions given to the model, including any examples.
Scoring criteria: What qualities was the model asked to consider, such as correctness, relevance, clarity, safety, or completeness?
Score meanings: What scale was used, and was each score clearly defined?

Comparison and Scoring Process
Type of judgment: Did the model score one answer, compare two answers, rank several answers, or give a pass/fail decision?
Repeated grading: Was each answer graded once or multiple times? Record how disagreements across runs were resolved.
Use of a correct answer: Was the model given a reference answer? If so, how was that answer created and checked?
Final score calculation: How were ratings combined across questions, criteria, models, or repeated runs? Note how ties and failed grading attempts were handled.

Replication Details
Generation settings: Record all reported settings that may affect grading, including randomness settings, number of grading runs, and any fixed random number.
Output handling: How was the model's response converted into a score? Record required formatting, extraction rules, and treatment of malformed responses.
Software and access: Record the code, software packages, service used to access the model, and date of evaluation.
```

Thirteen fields, numbered A1–A6, B1–B4, C1–C3 in that order. Three rules make a record worth having:

1. **Every field cites its source** — a file path with a line number, a paper section, or the
   words `not stated upstream`. Never blank, never inferred from what a benchmark "probably" does.
2. **Prompts are verbatim.** The copy of record is the vendored source at the cited lines — the
   exact text the pilot's runners read and send — not a transcription here, which would be a
   second copy that can drift. Direction of every scale is its own fact (A6): a 1–3 scale where 1
   is best and one where 3 is best look identical in a table and invert every conclusion.
3. **Where code and paper disagree, record both** and say which our run follows. Code first: it is
   what produced the published numbers.

Anything decided here because upstream never specified it is written `our choice: <value> (<date>)`.
Upstream bugs are recorded where they are found.

### 7.2 MultiChallenge — record

Source: `ekwinox117/multi-challenge@5ccefcca` (2025-02-05), vendored at
`Action_processes_benchmarks/Multi-challenge_bench`; read 2026-08-19. 273 items, `PASS_CRITERIA` =
`"YES"` on all of them.

| Field | Upstream | Source |
|---|---|---|
| A1 Grading model | `gpt-4o-2024-08-06`, OpenAI `beta.chat.completions.parse`, `temperature=0`; hard-coded | `src/evaluator.py:30-35`; `src/models/openai.py:31-37` |
| A2 Material shown | the tested model's **final response** and the item's `TARGET_QUESTION` (the rubric, in the `<CRITERIA>` slot). Withheld: the conversation, the final user turn, the axis, `PASS_CRITERIA`; no system message | `src/evaluator.py:40-43` |
| A3 Human comparison | not in the repo. The paper: the rubric judge agreed with humans 93.95%; the whole conversation without a rubric 37.33% | Sirdeshmukh, Table 4 |
| A4 Instructions | one variant, one user turn, no few-shots, "Be VERY STRICT!" | `src/evaluator.py:11-24` (`JUDGE_PROMPT`) |
| A5 Criteria | none named — the instance rubric is the criterion | `src/evaluator.py:19` |
| A6 Scale | binary YES/NO (`Literal`); an item passes on `verdict == PASS_CRITERIA` — direction is per item, though all 273 say YES | `src/evaluator.py:7-9, 78` |
| B1 Judgment | pass/fail on one answer; free-text reasoning stored, never scored | `src/evaluator.py:7-9, 44` |
| B2 Repeats | one judge call per (item, attempt); `--attempts k` samples k responses, combined any-pass (pass@k) | `main.py:31-32`; `src/result_parser.py:27-30` |
| B3 Reference | none exists; the human-written rubric replaces it | data schema |
| B4 Final score | per axis % passed; headline = **macro** mean of the four axes (113 / 69 / 50 / 41 items). A failed judgment is scored NO | `src/result_parser.py:9-38` |
| C1 Settings | `temperature=0`, structured output; no seed, retry or timeout; `max_tokens=4096` never reaches the API (D1). A generation error is stored *as the response* ("… FAIL THIS QUESTION") and judged | `src/evaluator.py:30-35`; `src/data_loader.py:44-51` |
| C2 Output | schema-enforced; a refusal or API error becomes NO silently | `src/evaluator.py:80-90` |
| C3 Software | `openai==1.53.0`, `pydantic==2.10.6`; OpenAI API; never executed as vendored | `requirements.txt` |

**Discrepancies and decisions.**
- **D1 — the harness does not run.** `Evaluator` passes `max_tokens` to a constructor that takes no
  such argument: `TypeError` before the first call. `our choice: remove the kwarg (2026-08-19)`.
- **D2 — one judge error corrupts the headline.** The error handler writes `axis='NA'`, which becomes
  a fifth axis at 0% and divides the macro by 5. `our choice: a judge error is its own status, never
  a verdict or an axis (2026-08-19)`.
- **D3 — the attempt index is wrong whenever `--attempts > 1`** (a leaked loop variable).
  `our choice: one attempt (2026-08-19)` — under any-pass, false PASSes compound as 1 − (1 − FPR)^k.
- **D4 — the docstring's axis names are stale** (`REFINEMENT, EXPLICIT IF, …`); the data's are
  `INFERENCE_MEMORY, INSTRUCTION_RETENTION, SELF_COHERENCE, RELIABLE_VERSION_EDITING`.
- **D5 — what the judge sees.** `our choice: follow the code — final response and rubric only, no
  conversation (2026-08-19)`; the published numbers were produced that way.
- **D6 — `PASS_CRITERIA` is vestigial but kept,** so a future data row saying "NO" cannot silently
  invert its own item.
- A generation error is retried, never sent to the judge as text. Implemented in
  `Multi-challenge_bench/mc_eval_core.py`.

### 7.3 Wonderbread QA (Judge 1) — record

Source: `HazyResearch/wonderbread@ed052c67` (2025-07-30), vendored at
`Action_processes_benchmarks/Wonderbread_bench`; read 2026-08-19. 120 items, four calls each.

| Field | Upstream | Source |
|---|---|---|
| A1 Grading model | the label `'GPT4'`, resolved to `gpt-4-0125-preview` (text); `temperature=0`, `max_tokens=4096`, `SYSTEM_PROMPT` prepended | `question_answering/eval.py:33, 42, 51, 60`; `wonderbread/helpers.py:454-462, 487-494` |
| A2 Material shown | question + response to all four criteria; the **Human Label only to completeness and soundness**; never the screenshots, trace, SOP or application. The clarity and compactness prompts still say they are given a human label, and compactness's third few-shot prints one | `question_answering/prompts.py:102-107, 149-155, 173` |
| A3 Human comparison | **on disk**: a 30-item sample scored by humans and by the GPT-4 judge — exact agreement 86.7% / 93.3% / 96.7% / 96.7%, Spearman 0.860 / 0.876 / 0.802 / 0.886 (completeness / soundness / clarity / compactness). Who the humans were: not stated | `data/experimental_results/question_answering/human_correlation/` |
| A4 Instructions | four variants, one per criterion, each with three worked examples | `question_answering/prompts.py:1-191` |
| A5 Criteria | completeness, soundness, clarity, compactness — four separate calls. The docstrings' "score this metric harshly" is never sent | `question_answering/eval.py:27-61` |
| A6 Scale | integer 1–3, **1 = best, 3 = worst**, every point defined. The authors' radar plot fixes the axis at 0–3, so a smaller polygon is the better model | `prompts.py:14-17, 65-68, 114-117, 160-163` |
| B1 Judgment | absolute score of one answer; the bare number, no explanation | `question_answering/eval.py:63-75` |
| B2 Repeats | one call per (item, criterion) — 480 per model | `question_answering/eval.py:63-75` |
| B3 Reference | `Human Label` in `data/qa_dataset.csv`; provenance not documented | `data/qa_dataset.csv` |
| B4 Final score | per criterion, micro mean over items; no composite. A response NaN or under 5 characters is written `"NA"` unjudged | `question_answering/eval.py:29-30, 85-95` |
| C1 Settings | sequential; no seed; a rate limit retries by unbounded recursion; any other API error kills the run, and the CSV is written only after the loop | `wonderbread/helpers.py:454-471` |
| C2 Output | the raw completion string is stored as the score — no parse | `question_answering/eval.py:27-61` |
| C3 Software | `openai` client, `OPENAI_API_KEY`; never executed as vendored | `setup.py` |

`our choice: parse into {1,2,3} with a parse-failure status; checkpoint every row (2026-08-19)` —
`Wonderbread_bench/wb_eval_core.py`.

### 7.4 Wonderbread SOP Generation (Judge 2) — record

| Field | Upstream | Source |
|---|---|---|
| A1 Grading model | `gpt-4-1106-preview` — a different snapshot from QA's — through the JSON-mode helper | `sop_generation/eval_completion.py:15, 92`; `wonderbread/helpers.py:512-527` |
| A2 Material shown | one line of one SOP (the Query) and the **whole other SOP** as an indexed list; nothing else | `sop_generation/metrics.py:64-96`; `eval_prompts.py:73-104` |
| A3 Human comparison | no line-level study. **Per-SOP human precision and recall exist** for 30 generated SOPs, beside GPT-4's (`manual_eval_*` vs `auto_eval_*`); raters not described *(corrected 2026-10-19 — the August record said none)* | `data/experimental_results/sop_generation/human_correlation/sample_human_eval.csv` |
| A4 Instructions | one variant, no few-shots, JSON with `scratchpad` and `index` | `sop_generation/eval_prompts.py:44-104` |
| A5 Criteria | whether a line captures the Query's primary objective | same |
| A6 Scale | an index; −1 = no match | `sop_generation/metrics.py:97-152` |
| B1–B2 Judgment, repeats | a mapping decision, one call per line in **both directions** — p + g calls per demonstration; no repeats | `sop_generation/metrics.py:64-96` |
| B3 Reference | the human-written gold SOP per demonstration (`SOP - <demo>.txt`) | demo folders |
| B4 Final score | precision = matched generated lines / generated; recall = matched gold lines / gold; ordering = generated lines matched in non-decreasing gold order / generated; F1 from P and R. Line counts are taken **after `preprocess_sop`, which strips everything up to the first "."** | `sop_generation/eval.py:19-45`; `metrics.py:97-178`; `eval/run_sop_generation.py:229` |
| C1–C2 Settings, output | JSON mode, `max_tokens=4096`, **no temperature — the API default 1.0**; a malformed answer is regenerated once, then raises. Completions are cached by name, so an edited prompt returns old answers | `sop_generation/eval_completion.py:43-81` |
| C3 Software | as QA | — |

**Decisions.** `our choice: temperature 0 where the judge allows it, and no cache (2026-08-19)`.
`our choice: keep preprocess_sop's strip, for comparability (2026-10-19)`. `our choice: strip JSON
fences; an index outside the list is a parse failure, not a match (2026-10-19)`. Implemented in
`wb_eval_core.py`.

### 7.5 Wonderbread SOP Improvement (Judge 3) — out of scope

`gpt-4-turbo` with a six-criterion 1–5 rubric, in `wonderbread/benchmark/eval/eval_rubric.py`, and
**the file cannot run**: it imports a module that is not in its folder (line 10) and a package that
does not exist (line 17), calls a three-argument function with two (lines 74-78, 241), and shadows
its own prompt (line 24). It hard-codes `model_name = "Claude3"` (line 95), discards the gold SOP it
is passed, and `eval()`s the model's output. The same rubric ships with opposite polarities —
"1 (best) to 5 (worst)" in `sop_generation/eval_prompts.py:22`, "1 (worse) to 5 (best)" in
`eval_rubric.py:34`. `our choice: exclude SOP Improvement rather than write a scorer from the paper
(2026-08-19)`.

### 7.6 The substituted judges

All three upstream snapshots, and MultiChallenge's `gpt-4o-2024-08-06`, are retired. The judges that
replace them are declared in §6.1 — model id, backend, reasoning, temperature, price — and run under
`Action_processes_benchmarks/judge_core.py::JUDGES`, which writes the full configuration onto every
judge row. For the pilot: `N_REPS=3` replicates, a unit's label by strict majority (QA: the median
when every replicate answered), refusals and parse failures as statuses of their own, never scored.
Each benchmark's pages under `.claude/references/benchmarks/action/` hold its run order and counts.

### 7.7 What writing the record changed

Three facts that were wrong or unknown before, all found by reading code rather than papers:

1. **Wonderbread's judge covers SOP Generation, not only QA**, on a different GPT-4 snapshot, with a
   cost that follows the tested model's verbosity rather than the item count.
2. **Two of the three judge harnesses do not run as vendored** — MultiChallenge (D1) and SOP
   Improvement (§7.5). The published numbers were not produced by the code as released, so a run of
   ours says what it patched.
3. **The same 1–5 rubric ships with both polarities.** Why A6 records direction separately.

## 8. What is still open

- **Which judge: Kimi K2.6 or Haiku 5.5** (§6.4; the case for each, [PILOT_FINALISTS.md](PILOT_FINALISTS.md)) — the user's and the advisor's decision. Haiku 4.5
  and Sonnet 5.5 are out on the pilot's evidence, Sonnet pending the user's confirmation.
- **The bake-off and the human labels.** Neither exists yet. Until both do, any judge is a
  provisional choice, not a result.
- **Haiku 5.5 is untested anywhere.** No published evaluation of it exists.
- **Kimi K2.6 has one supporting paper,** and none on a short YES/NO rubric like MultiChallenge's.
- **MultiChallenge task version.** In March 2026 the authors revised 54 tasks and moved their own
  judge to Gemini 2.5 Pro. Whether we use the revised tasks or our vendored February-2025 set is the
  user's decision. Either way the Gemini judge is excluded.
- **Wonderbread's data for a full run.** `gold_demos.zip` is 33 GB, nine-tenths of it video. The
  pilot reads only SOPs, traces and screenshots, which Zenodo also ships as a 5.7 GB archive, and
  takes only the sampled demos from it by byte range (291 MB). Whether a full run is in scope, and
  whether it is multimodal or text-only, is still the advisor's question. The judge is text-only
  either way.
- **Wonderbread QA clarity is not judgeable on this evidence.** Every candidate's QWK is 0.07–0.36
  and the human labels are nearly constant (mean 1.10), so κ cannot separate judges there. It will
  be human-scored or reported as unvalidated. Compactness is judgeable (Kimi K2.6 0.74).
- **Upstream's GPT-4 judge agrees with the QA human labels far better than any candidate** (QWK
  0.78–0.92 against 0.07–0.74, same 30 answers). Whether the labels were made with GPT-4's scores in
  view is unestablished; if they were, "agreement with humans" there partly measures agreement with
  GPT-4.
- **MultiChallenge disagreements need a person.** The pilot can say whether the four judges agree
  there; if they do not, which one is right is a labelling question (§6.4).

## 9. Papers

The arXiv identifier is given; the venue was confirmed as described in §3. PDFs in `papers/`.

| # | Paper | Venue | arXiv |
|---|---|---|---|
| 1 | Gosai et al., *Audio MultiChallenge* | ACL 2026 | [2512.14865](https://arxiv.org/abs/2512.14865) |
| 2 | Wen et al., *IF-RewardBench* | ACL 2026 | [2603.04738](https://arxiv.org/abs/2603.04738) |
| 3 | Pombal et al., *Self-Preference Bias in Rubric-Based Evaluation of LLMs* | COLM 2026 | [2604.06996](https://arxiv.org/abs/2604.06996) |
| 4 | Li et al., *Preference Leakage: A Contamination Problem in LLM-as-a-judge* | ICLR 2026 | [2502.01534](https://arxiv.org/abs/2502.01534) |
| 5 | Roytburg et al., *Are LLM Evaluators Really Narcissists?* | ICML 2026 | [2601.22548](https://arxiv.org/abs/2601.22548) |
| 6 | Naik et al., *Do We Need Frontier Models to Verify Mathematical Proofs?* | COLM 2026 | [2604.02450](https://arxiv.org/abs/2604.02450) |
| 7 | Krumdick et al., *No Free Labels* | COLM 2026 | [2503.05061](https://arxiv.org/abs/2503.05061) |
| 8 | Sharma et al., *ResearchRubrics* | ICLR 2026 | [2511.07685](https://arxiv.org/abs/2511.07685) |
| 9 | Peng et al., *Can LLM-as-a-Judge Reliably Verify Rubrics in Agentic Scenarios?* | EMNLP 2026 | [2606.29920](https://arxiv.org/abs/2606.29920) |
| 10 | Ananthram et al., *PoSh* | ICLR 2026 | [2510.19060](https://arxiv.org/abs/2510.19060) |
| 11 | Chang et al., *How2Everything* | ICML 2026 | [2602.08808](https://arxiv.org/abs/2602.08808) |
| 12 | Lee et al., *How to Correctly Report LLM-as-a-Judge Evaluations* | ICML 2026 | [2511.21140](https://arxiv.org/abs/2511.21140) |
| 13 | Chen et al., *Efficient Inference for Noisy LLM-as-a-Judge Evaluation* | ICML 2026 | [2601.05420](https://arxiv.org/abs/2601.05420) |
| 14 | Li, Mukherjee & Pal, *LLM Judge Validation Under Sparse Overlap* | NeurIPS 2026 | [2609.31857](https://arxiv.org/abs/2609.31857) |
| 15 | Schwinn et al., *A Coin Flip for Safety* | ICML 2026 | [2603.06594](https://arxiv.org/abs/2603.06594) |
| — | Sirdeshmukh et al., *MultiChallenge* (the benchmark's own paper) | Findings of ACL 2025 | [2501.17399](https://arxiv.org/abs/2501.17399) |
