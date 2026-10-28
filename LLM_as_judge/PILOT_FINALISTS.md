# Judge pilot finalists — Kimi K2.6, Haiku 4.5 and Haiku 5.5 compared, and the case for Haiku 5.5

<!-- size-budget: 11000 -->
<!-- The three-way comparison and the argument built on it, kept together so the case can be read
     against its evidence in one place. -->

**Written 2026-10-28, at the user's request.** This file holds the judge pilot's results for its
three finalists. The pilot's design, Sonnet 5.5's result and everything else about judges stay in
[JUDGE_SELECTION.md](JUDGE_SELECTION.md) — §6.4 for the pilot, §6.2 for the bake-off, §8 for what is
open. Numbers come from `Action_processes_benchmarks/judge_comparison/report.md`, which
`compare_judges.py` rebuilds from the result rows, unless marked otherwise.

**Disclosure.** Written by Claude (Anthropic), arguing for a Claude model, as the user asked. Read
§4, the case against it, with the same weight as §3.

## 1. Bottom line

- **Proposed: Claude Haiku 5.5 as the working judge, with Kimi K2.6 as the named fallback.** Both are
  provisional until the bake-off on human-labelled data (JUDGE_SELECTION §6.2). The choice is the
  user's and the advisor's.
- **Why.** On the scores GPT receives, Haiku 5.5 and Kimi agree. Kimi agrees more closely with the
  humans, consistently, but n = 30 cannot confirm the margin. Haiku 5.5 costs about a sixth as much,
  is more stable than Kimi, and runs on its maker's own endpoint. The advisor's rule says: if the
  judges give about the same results, take the cheap one.
- **What would reverse it.** Haiku 5.5 failing a bake-off bar that Kimi passes. Or the behaviour in
  §3.1 — failing criteria that point at context the judge cannot see — turning out to be systematic.
- **Haiku 4.5 is out.** It is never closer to the humans than Kimi on any judgeable measure, and it
  is the most expensive of the three.

## 2. Side by side

The pilot judged `gpt-5.6-luna` on a 10% sample, three replicates per judge. All judges also graded
upstream's 30 human-labelled Wonderbread QA answers and 30 SOP pairs, the *anchors*. MultiChallenge
has no human labels, so there only agreement between judges is measured.

| | Haiku 4.5 | Haiku 5.5 | Kimi K2.6 |
|---|---|---|---|
| ***GPT's scores*** | | | |
| MultiChallenge macro / micro (23 common items) | 44.5 / 47.8 | 36.1 / 43.5 | 44.5 / 47.8 |
| SOP F1 — td / td_kf / td_kf_act | 0.67 / 0.88 / 0.93 | 0.59 / 0.90 / 0.93 | 0.64 / 0.88 / 0.91 |
| QA mean, 12 answers, 1 best — compl. / sound. / clar. / compact. | 2.08 / 2.08 / 1.08 / 1.08 | 1.83 / 1.42 / 1.00 / 1.33 | 1.58 / 1.50 / 1.08 / 1.00 |
| ***Against the humans (anchors, n = 30)*** | | | |
| QA QWK — compl. / sound. / clar. / compact. | 0.42 / 0.16 / **0.36** / 0.56 | 0.42 / 0.20 / 0.26 / 0.12 | **0.63** / **0.32** / 0.26 / **0.74** |
| QA QWK, mean of the four | 0.38 | 0.25 | **0.49** |
| SOP precision / recall, MAE | 0.193 / 0.185 | 0.224 / 0.145 | **0.175** / **0.116** |
| SOP precision / recall, Pearson | 0.76 / 0.67 | 0.72 / **0.79** | **0.82** / 0.76 |
| SOP mean precision (humans: 0.515) | 0.708 | 0.730 | 0.682 |
| ***Stability — share of units whose replicates disagree*** | | | |
| MultiChallenge / SOP on GPT / SOP anchors | 0% / 1.0% / 1.4% | 7.4% / 7.1% / 8.1% | 14.8% / 8.1% / 10.5% |
| ***Cost and running*** | | | |
| billed in the pilot | $7.69 | $0.93 | $5.41 |
| full run per evaluated model (sample's billed cost, anchors excluded, × 10) | ≈ $50 | ≈ $6 | ≈ $35 |
| backend | Anthropic | Anthropic | Crusoe (third party, pinned) |
| `temperature` | 0 | not accepted | 0 |
| reasoning | off — its default | off — default is on | off — default is on |
| unparsed | none | 4 of 3,162 SOP lines | none |

For scale, upstream's GPT-4 judge on the same anchors scores QA QWK 0.78–0.92 and SOP MAE 0.112 /
0.078.

**Paired bootstrap over the 30 anchors** (4,000 resamples, computed 2026-10-19; not part of
`compare_judges.py`):

- Kimi minus Haiku 5.5 on the QA mean: +0.24 [−0.01, +0.37].
- Kimi's SOP precision MAE is below Haiku 5.5's by 0.05 [0.00, 0.10].
- Kimi's SOP recall MAE is below Haiku 4.5's by 0.07 [0.01, 0.13].
- No single QA criterion separates any two judges.

## 3. The case for Haiku 5.5

1. **Where the pilot can tell, it gives GPT the same scores as Kimi.**
   - *SOP:* per-ablation F1 is within 0.08 across all three judges, and the ablations come out in
     the same order. Line decisions agree 89.6% between Haiku 5.5 and Kimi (κ 0.69), the lowest
     of the three pairs; the other two pairs agree 91.1–92.2%.
   - *MultiChallenge:* the 8-point macro gap is one item (§3.1).
   - *QA is the exception.* On GPT's 12 answers, Haiku 5.5 and Kimi differ by up to 0.33 on the 1–3
     scale, in completeness and compactness. Twelve answers cannot separate the judge from noise.
2. **Kimi's lead against the humans is consistent but not established.** The QA interval crosses
   zero, and the SOP precision interval touches it. Of the eight measures, Kimi leads six, Haiku
   5.5 leads SOP recall correlation, and Haiku 4.5 leads QA clarity — which no judge can do
   (JUDGE_SELECTION §8).
3. **It costs about a sixth of Kimi and an eighth of Haiku 4.5.** The saving buys replicates. At
   linear scaling (our arithmetic), five replicates of Haiku 5.5 cost ≈ $10 per evaluated model,
   under a third of Kimi's three.
4. **It is more stable than Kimi.** 7–8% of units disagree across its replicates, against 8–15% for
   Kimi, which is the least stable judge even at temperature 0 on unquantised weights.
5. **It is simpler to run reproducibly.**
   - Kimi K2.6 is served by 17 providers, at int4 to bf16. Unpinned, one smoke run's rows came from
     two of them.
   - Kimi's maker's endpoint returns whitespace in JSON mode and refuses `temperature`. So Kimi
     depends on one third-party backend, Crusoe, staying up and unchanged.
   - Haiku 5.5 runs on its maker's own endpoint.
6. **It keeps the set of evaluated models open.** Kimi is eligible as a judge only while Kimi is not
   evaluated on MultiChallenge or Wonderbread (JUDGE_SELECTION §5), and Kimi already has Big Bench
   Hard results in this suite. No Claude model is evaluated anywhere in it.

### 3.1 MultiChallenge: the gap is one item

On the 23 items every judge labelled, Haiku 5.5 passes 10 and the other two pass 11.

- **Why one item moves the macro by 8 points.** The one difference, `6781aa539eb3af0ed43b68c3`, is
  in Reliable Version Editing, which has 3 common items. One item is therefore 33 points on that
  axis and 8.3 points on the four-axis macro — the whole gap from 44.5 to 36.1. Micro moves 4.3
  points.
- **Haiku 5.5 split on it:** FAIL, FAIL, PASS. Haiku 4.5 and Kimi passed it on all three replicates.
- **The item.** The criterion asks whether the response uses "the first tagline from each section of
  the second draft", and quotes the three taglines. GPT's response contains all three, with
  trailing periods.
- **Why it failed.** Both FAIL replicates give the same reason: the second draft "is not provided in
  the prompt", so under strict evaluation the claim "cannot be verified". Upstream's judge prompt
  (`Action_processes_benchmarks/Multi-challenge_bench/src/evaluator.py`) gives the judge only the
  final response and the criterion, with "Be VERY STRICT!" and no conversation. Haiku 5.5 read the
  missing context as grounds to fail; the other two checked the quoted text.
- **It is not stricter overall.** Across all 27 items, its disagreements with Haiku 4.5 are 2 each
  way, and with Kimi 1 each way (McNemar p = 1.0). On `6765f48aa02fd129919eef9e` it passes on all
  three replicates where both others fail.

## 4. The case against it, and how each point is handled

| Risk | Evidence | Handling |
|---|---|---|
| Worst on QA compactness | QWK 0.12; mean 1.73 against the humans' 1.17 — it marks concise answers down | If it fails the bake-off bar there, compactness gets its own judge (Kimi, 0.74) or human scoring (JUDGE_SELECTION §6.2, rule 5) |
| Lowest QA agreement overall | QWK mean 0.25 against Kimi's 0.49 | As above. The corrected pass rate (§6.3) absorbs a measured error rate, at the price of a wider interval |
| Worst SOP precision MAE | 0.224 against 0.175 | All three credit about 0.2 more precision than the humans (upstream's GPT-4: 0.02); the correction applies to whichever judge is chosen |
| No `temperature` control | 7–8% of units disagree across replicates | Three replicates at minimum, with a majority vote; more are cheap (§3, point 3) |
| Ran with its default reasoning off | Never tested with reasoning on | Kimi also ran with its default reasoning off, so the comparison is not tilted by this |
| Fails criteria that point at unseen context | One item, 2 of 3 replicates (§3.1) | n = 1. Bake-off labels should over-sample MultiChallenge criteria that refer to earlier turns |
| No outside evidence | Zero papers; released 2026-10-07 (JUDGE_SELECTION §5) | The bake-off supplies it; until then the choice is provisional |
| Same maker as the author of this case | The disclosure above | The bake-off's bars are fixed before any result is seen |

## 5. Kimi K2.6 and Haiku 4.5

- **The case for Kimi is agreement with the humans.** It is closest on six of eight measures, and
  it is the best compactness judge by far (QWK 0.74, against 0.56 and 0.12). If agreement with the humans
  decides, rather than the scores GPT receives, Kimi is the choice. Its costs: ≈ $35 per evaluated
  model, the least stability of the three, dependence on one third-party backend, and Kimi can then
  never be evaluated on these two benchmarks.
- **Haiku 4.5 is the most stable** (0–1.4% at temperature 0), but it is closest to the humans only
  on QA clarity, which is not judgeable. It is never ahead of Kimi on a judgeable measure and costs
  ≈ $50 per evaluated model, so it is out under the advisor's rule.

## 6. What would settle the open points

- **Run Haiku 5.5 with reasoning on**, over the 27 MultiChallenge items × 3 replicates. It costs
  cents and is a local provider probe. It shows whether §3.1 comes from the model or from our
  configuration.
- **Run the bake-off** (JUDGE_SELECTION §6.2). This file informs that decision; it does not replace
  it.
