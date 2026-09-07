"""Gemini 3.5 Flash-Lite via **Google AI Studio** (native google-genai) — MMLU runner.

**Why this folder exists.** `MMLU_Gemini_Flash3.5lite_OpenRouter/` ran on 2026-08-30 and its
OpenRouter balance ran out mid-run: 2,188 of 3,943 rows came back empty with HTTP 402
(`limit_source: openrouter_credits`, "requested up to 8192 tokens, but can only afford 8119"), and
the four subjects after `Miscellaneous` are 100% empty. That folder is kept untouched as the record
of what OpenRouter produced. **This folder starts as a copy of it and is finished on the native
route** — the user's decision, 2026-09-07, taken knowing the two routes are not the same condition.

**There is no scorer in this file.** Scoring is `mmlu_eval_core.score_response`, the one lenient
matcher every model in this benchmark is judged by.

**The result set here is deliberately mixed-route, and every row says which route wrote it.**
Rows carried over from OpenRouter have `reasoning_effort=minimal` and a `backend=` field in their
`config` column; rows written here have `route=google_aistudio` and `thinking_budget=128`. That is
the whole reason the route is written per row rather than per run: nothing else could tell them
apart afterwards. `references/model-calls.md` measured the difference — OpenRouter's
`reasoning.effort="minimal"` spent zero thinking across 400 items, while a native `thinking_budget`
of 128 let 48 of 400 think anyway. Anywhere this column is reported, say it is two routes.

**The four config keys the resume compares are identical to the stored rows** — `max_tokens=8192`,
`model=google/gemini-3.5-flash-lite`, `prompt=v2`, `seed=42` — which is what lets
`core.load_checkpoint` accept the carried-over rows instead of refusing them. `reasoning_effort` is
deliberately NOT declared here: it is not a parameter this route has, and declaring it to make the
config match would be recording a value that was never sent.

`--model` stays `google/gemini-3.5-flash-lite`, OpenRouter's spelling, because it names the result
files and the carried-over rows are already under that slug. The native API takes the id without
the vendor prefix, so the prefix is stripped at the call and nowhere else.

**No pruning is needed before resuming.** `core.load_checkpoint` counts an empty row as not done and
retries it — that is what "an empty row is not a done row" in its docstring means.

**`minimal` is the thinking floor; there is no off.** `thinking_budget=0` is rejected 400
INVALID_ARGUMENT on this model. **Omit `temperature`, `top_p`, `top_k`** — 3.x guidance is to
remove, not tune.
"""

import argparse
import json
import os
import sys
import threading

from dotenv import load_dotenv
from google import genai
from google.genai import types

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(MODEL_DIR))
import mmlu_eval_core as core  # noqa: E402

# OpenRouter's spelling of the id, kept because it names the result files the carried-over rows are
# already in. API_MODEL is what the native endpoint is actually asked for.
DEFAULT_MODEL = "google/gemini-3.5-flash-lite"
MODEL = DEFAULT_MODEL

THINKING_BUDGET = 128        # 0 is rejected 400 on flash-lite; 128 measured zero thought tokens
THINKING_LEVEL = "minimal"   # used only where the SDK exposes thinking_level instead

# Must equal the stored rows on every key, or load_checkpoint refuses to resume. max_tokens is the
# name MMLU's row schema uses for the visible-output cap; on this route it is sent as
# max_output_tokens. Same cap, same number, different SDK spelling.
CONFIG = {"max_tokens": 8192, "seed": 42}

AUTH_MARKERS = ("API key not valid", "ACCESS_TOKEN_TYPE_UNSUPPORTED", "PERMISSION_DENIED",
                "API_KEY_INVALID", "UNAUTHENTICATED")
# Permanent request-shape failures. Retrying these five times an item across 3,943 items is how a
# run spends hours proving the same thing over and over — provider-gotchas.md.
FATAL_MARKERS = ("INVALID_ARGUMENT", "Extra inputs are not permitted", "validation error")

load_dotenv(core.ENV_PATH)
# Its own key, not GEMINI_API_KEY: that one is the 2.5 run's and is a different quota.
api_key = os.getenv("GEMINI_FLASH_LITE_API_KEY")
if not api_key:
    sys.exit("GEMINI_FLASH_LITE_API_KEY is not set in %s" % core.ENV_PATH)
# A request timeout, because `timeout=` is the only guard this SDK offers and a job hung inside one
# call reports RUNNING to SLURM with an empty log for as long as it takes (quest-cluster.md).
client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=300_000))

_USAGE = {"thinking_tokens": 0, "prompt_tokens": 0, "output_tokens": 0, "calls": 0,
          "max_tokens_finish": 0}
_USAGE_LOCK = threading.Lock()


def _thinking_config():
    """Chosen from what THIS SDK exposes, never by trying one field and catching an exception.

    google-genai is pydantic: a wrong field raises ValidationError, which a `except TypeError` guard
    never catches. That exact mistake retried a permanent config error three times an item for 20
    items before anyone looked (provider-gotchas.md). Quest's build is 1.49.0 and has
    `thinking_budget`; 2.19 has `thinking_level`.
    """
    fields = set(getattr(types.ThinkingConfig, "model_fields", None) or {})
    if "thinking_budget" in fields:
        return types.ThinkingConfig(thinking_budget=THINKING_BUDGET)
    if "thinking_level" in fields:
        return types.ThinkingConfig(thinking_level=THINKING_LEVEL)
    sys.exit("This google-genai build exposes no thinking cap (ThinkingConfig fields: %s). Upgrade "
             "the SDK, or decide explicitly to run without one and record that — do not delete this "
             "guard." % sorted(fields))


def visible_text(resp):
    """The answer parts only.

    `resp.text` warns and concatenates whenever the response carries non-text parts — this model
    returns a `thought_signature` part on every call — so the parts are read directly and anything
    flagged `thought` is dropped. MMLU's row schema has no column for a thought summary, so it is
    counted in the usage totals and not stored.
    """
    try:
        return "".join(p.text for p in resp.candidates[0].content.parts
                       if getattr(p, "text", None) and not getattr(p, "thought", False))
    except Exception:
        return getattr(resp, "text", "") or ""


def call(prompt):
    api_model = MODEL.split("/")[-1]      # native endpoint takes the id without the vendor prefix
    cfg = _thinking_config()

    def once():
        try:
            resp = client.models.generate_content(
                model=api_model, contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=cfg,
                    max_output_tokens=CONFIG["max_tokens"],
                    seed=CONFIG["seed"],
                ),
            )
        except Exception as e:
            err = str(e)
            if any(m in err for m in AUTH_MARKERS):
                sys.exit("auth failure, not retrying — fix the key and resubmit:\n  %s" % err[:400])
            if any(m in err for m in FATAL_MARKERS):
                sys.exit("permanent request-shape failure, not retrying:\n  %s" % err[:400])
            raise

        finish = ""
        try:
            finish = str(resp.candidates[0].finish_reason or "")
        except Exception:
            pass
        with _USAGE_LOCK:
            _USAGE["calls"] += 1
            try:
                um = resp.usage_metadata
                _USAGE["thinking_tokens"] += um.thoughts_token_count or 0
                _USAGE["prompt_tokens"] += um.prompt_token_count or 0
                _USAGE["output_tokens"] += um.candidates_token_count or 0
            except Exception:
                pass
            if "MAX_TOKENS" in finish.upper():
                _USAGE["max_tokens_finish"] += 1

        text = visible_text(resp).strip()
        # Thinking ate the whole budget: billed, nothing to score. Distinguished from a wrong answer
        # because the fix is a larger cap, not a better prompt.
        if not text and "MAX_TOKENS" in finish.upper():
            print("    empty response, finish_reason=%s — raise the output cap" % finish, flush=True)
        return text

    return core.retry(once, label="gemini35lite-google")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Run MMLU for Gemini 3.5 Flash-Lite via Google AI Studio (native SDK).")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help="model id; it is BOTH what is called and what the result files are named "
                         "after. Keep the google/ prefix: it is the slug the carried-over rows are "
                         "already written under, and it is stripped before the native call")
    ap.add_argument("--subject", default="all",
                    help="'all' or a comma-separated list of subject names")
    ap.add_argument("--sleep", type=float, default=0.0, help="seconds between calls")
    ap.add_argument("--limit", type=int, default=0,
                    help="only the first N items of each subject - a smoke test, not a run. It "
                         "does NOT resume, and it writes to the untagged filename, so never point "
                         "it at a folder holding real rows")
    ap.add_argument("--prompt", default="v2", choices=["v1", "v2"],
                    help="prompt version; part of the run config, so a resume across a change of "
                         "it is refused rather than silently mixing two prompts")
    ap.add_argument("--shard", type=int, default=0, help="this shard's index, 0-based")
    ap.add_argument("--total-shards", dest="total_shards", type=int, default=1,
                    help="how many shards the work is split across. Must stay 5 to resume this "
                         "run: each shard reads back its own _shard<N>of5 checkpoint")
    ap.add_argument("--workers", type=int, default=1,
                    help="concurrent request streams. 5 is this project's standing limit and a "
                         "measured fix, not a convention - see quest-cluster.md")
    args = ap.parse_args()

    MODEL = args.model
    subjects = core.SUBJECTS if args.subject == "all" else [s.strip() for s in args.subject.split(",")]
    unknown = [s for s in subjects if s not in core.SUBJECTS]
    if unknown:
        raise SystemExit("unknown subject(s): %s\nknown: %s" % (unknown, core.SUBJECTS))

    cap = _thinking_config()
    print("Gemini 3.5 Flash-Lite (Google AI Studio): model=%s api_model=%s subjects=%d prompt=%s "
          "shard=%d/%d thinking=%s max_output_tokens=%d seed=%s"
          % (MODEL, MODEL.split("/")[-1], len(subjects), args.prompt, args.shard,
             args.total_shards, cap, CONFIG["max_tokens"], CONFIG["seed"]), flush=True)
    os.makedirs(os.path.join(MODEL_DIR, "results"), exist_ok=True)
    # Named for the route so it cannot overwrite the OpenRouter run's record of what it negotiated.
    with open(os.path.join(MODEL_DIR, "results", "google_params.json"), "w") as fh:
        json.dump({"model": MODEL, "api_model": MODEL.split("/")[-1], "route": "google_aistudio",
                   "max_output_tokens": CONFIG["max_tokens"], "seed": CONFIG["seed"],
                   "thinking": str(cap)}, fh, indent=2)

    try:
        core.run_subjects(MODEL_DIR, MODEL, call, subjects=subjects, sleep_between=args.sleep,
                          limit=args.limit, workers=args.workers, prompt_version=args.prompt,
                          shard=args.shard, total_shards=args.total_shards,
                          config=dict(CONFIG, model=MODEL),
                          per_row_config=lambda: {"route": "google_aistudio",
                                                  "thinking_budget": THINKING_BUDGET})
    finally:
        with _USAGE_LOCK:
            print("usage this shard: %s" % _USAGE, flush=True)
        with open(os.path.join(MODEL_DIR, "results",
                               "google_usage_shard%dof%d.json" % (args.shard, args.total_shards)),
                  "w") as fh:
            json.dump(_USAGE, fh, indent=2)
    print("done ->", os.path.join(MODEL_DIR, "results"), flush=True)
