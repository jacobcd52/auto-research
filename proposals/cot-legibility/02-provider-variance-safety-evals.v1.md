# How much does the provider matter? Safety evals on one model across every OpenRouter endpoint, against a self-hosted reference
cluster: cot-legibility | stage-1 cost: $390 | follows up: Not Pinning Your OpenRouter Provider Might Invalidate Your Research (KsyoSAyBRXtwzSugg); R1 CoT illegibility revisited (jHnZzicKzczkCCArK)

## 1. What the prior work showed
nostalgebraist re-ran the DeepSeek R1 experiment of a NeurIPS 2025 paper on CoT illegibility with a different
OpenRouter provider (Novita instead of Targon, both labelled fp8): mean illegibility fell from 4.30 to 2.28, samples
scoring >=7 from 20% to 0%, and accuracy rose. The paper's author conceded. Matthew Khoriaty's post generalised this
into a warning: providers differ in quantisation, backend, parameter handling and context limits, routing is not
random, and many safety codebases (Inspect, BashArena, Control Tower) call OpenRouter unpinned. He asked for
replications: "Claude Fable or GPT-Sol could probably get a long way to fixing and replicating these results
autonomously, and I encourage someone to do so."

The post contained almost no measurements, and its top comment (Tim Hua, 66 karma) initially strong-downvoted it
because the supporting audits were unverified model output. What exists elsewhere: "The Silent Hyperparameter"
(arXiv 2605.19537) shows inference backends shift *capability* benchmarks by up to 16.6 points on 4B-30B models
at fixed weights; "Model Equality Testing" (arXiv 2410.20247) found 11 of 31 Llama endpoints differed from reference
weights in 2024; Artificial Analysis found gpt-oss-120b AIME scores from 37% to 93% across hosts in 2025; one
low-karma LW post compared refusal rates on two routes of a closed Gemini alias. Nobody has measured how much
*safety-relevant* results - monitor performance and threshold calibration, CoT legibility, refusal propensity - move
across the providers of a model the safety community actually uses, relative to a reference run on controlled
hardware (searched 2026-11-14).

## 2. Question and why it matters
**For an open-weight model widely used in control and monitoring research, how large is between-provider variance on
safety metrics compared with sampling noise and with a self-hosted reference - and which endpoints are off?**
The community currently has one dramatic anecdote and a list of worries. A measured answer changes practice either
way: "of 26 endpoints, 22 are statistically indistinguishable from reference on these four evals; these four are not,
for these reasons" is as useful as "monitor false-positive rates swing 5x when the provider changes under you".
It also tests two folk heuristics: does labelled quantisation, or price, predict anything?

## 3. Stage 1 plan
**Models.** Primary: `openai/gpt-oss-120b` - 26 OpenRouter endpoints today (13 labelled fp4, 3 bf16, 2 fp8, 1 int4,
1 fp16, 6 unknown; max completion tokens from 4,096 to 117,964), heavily used as a trusted monitor / untrusted
model, and self-hostable on one 80 GB GPU (native MXFP4 weights, ~65 GB). Secondary: `openai/gpt-oss-20b`
(11 endpoints; fits an RTX A6000). Stretch: `meta-llama/llama-3.3-70b-instruct` (9 endpoints) without a local
reference unless budget remains.

**Reference.** Official Hugging Face weights served with vLLM on RunPod (H100 for 120b, A6000 for 20b), official
chat template, fixed sampling parameters; software versions recorded. A second reference run with a different
backend (Transformers) on a 300-item subset gives the "legitimate implementation noise" band.

**Evals (identical prompts, temperature, max tokens and reasoning effort for every endpoint; `allow_fallbacks:false`,
`require_parameters:true`, provider and quantisation logged per response).**
1. *Monitor.* `abhayesian/basharena-monitor-eval` (public, 373 labelled attack/honest actions with context): model
   gives a 0-100 suspicion score, 3 samples each. Metrics: AUROC, TPR at 2% FPR, and **threshold transfer** - the
   audit threshold calibrated on honest runs from endpoint A, applied to endpoint B (Khoriaty's
   "baseline on Monday, experiment on Tuesday" scenario made concrete).
2. *Capability + CoT legibility.* GPQA-Diamond (198 questions x 3 samples, multiple choice). Accuracy; reasoning
   length; empty/truncated-answer rate; illegibility with the original paper's grader prompt (code:
   https://github.com/Jozdien/cot_legibility) run by a cheap grader, plus non-LLM soup detectors (non-ASCII rate,
   and mean log-probability of the provider's text under the local reference model - a direct fingerprint).
3. *Propensity.* Refusal rate on a standard 100-prompt harmful-request set (StrongREJECT-style, no jailbreaks),
   3 samples, graded refuse/comply only.
4. *Parameter respect.* Temperature-0 repeat agreement, `max_tokens`, reasoning-effort setting honoured, long-context
   (60k-token) recall probe to detect silent truncation.

**Design.** Every endpoint is run twice, 24+ hours apart. Additionally run each eval five times through default
(unpinned) routing to show the spread a careless user would see.

**Analysis.** Mixed model separating sampling noise, day-to-day within-endpoint drift, and between-endpoint
variance; each endpoint's difference from reference with bootstrap CIs and multiplicity correction; regressions of
deviation on labelled quantisation and price; the threshold-transfer matrix; a short per-outlier diagnosis
(truncation, ignored parameters, template bugs, soup) from transcripts.

Steps: (1) harness, tested on 3 endpoints; (2) reference runs; (3) day-1 sweep; (4) grading; (5) day-2 sweep and
unpinned runs; (6) analysis, all logs released.

## 4. Stage 1 cost estimate
Prices from OpenRouter and RunPod on 2026-11-14.
- gpt-oss-120b sweep: per endpoint per day about 7M input + 4M output tokens (monitor contexts dominate input).
  Endpoint prices range $0.03-0.35/M in and $0.075-0.95/M out; average about $0.10 / $0.45 -> ~$2.50, worst endpoint
  ~$6. 26 endpoints x 2 days: **$130**. Unpinned x5: **$15**.
- gpt-oss-20b sweep (11 endpoints x 2 days, <= $0.075/$0.30): **$20**.
- Llama-3.3-70B stretch (9 endpoints, 1 day, up to $0.72/M): **$40**.
- Grading (legibility chunks, refusals) with claude-haiku-5.5 ($0.10/$0.50) or gpt-4o-mini ($0.15/$0.60):
  ~250M tokens: **$35**; 300-sample calibration of the grader against gpt-4o ($2.50/$10): **$10**.
- GPUs: H100 80 GB at $2.89/h x 14 h (setup, two backends, scoring provider text under the reference): **$40**;
  A6000 at $0.69/h x 10 h: **$7**.
- Margin for rate limits, retries, reruns (~30%): **$93**.
Total **$390**.

## 5. What success looks like
A post with (1) a per-endpoint table for gpt-oss-120b: each metric's deviation from reference with CI, flagged
outliers, labelled quantisation, price; (2) a variance-decomposition figure - how much of the spread in monitor
TPR@2%FPR, GPQA accuracy, illegibility and refusal rate is provider versus day versus sampling; (3) the
threshold-transfer heatmap, e.g. "a 2% FPR threshold calibrated on provider A yields 0.5%-9% FPR elsewhere";
(4) whether quantisation label or price predicts deviation; (5) the distribution of results under unpinned routing;
(6) a recommended-endpoint list and a reusable harness.
Strong result: several endpoints differ from reference by more than the two-backend noise band on a safety metric,
with a diagnosed cause. Null result: all endpoints within noise - still publishable as a measured all-clear for
the most-used open monitor model, and it would correct an over-update the community may be making; it would earn
less karma than a striking discrepancy. The parameter-respect and truncation checks (some endpoints cap output at
4,096 tokens) make a completely clean sweep unlikely.

## 6. Stage 2 (if stage 1 succeeds)
- Extend to models that cannot be self-hosted cheaply (DeepSeek V3.2, Kimi, GLM, Qwen 235B) using the best stage-1
  endpoint fingerprints and a short rented multi-GPU reference session (~$400).
- Pick one published control or monitorability result that used unpinned OpenRouter and re-run it on the best and
  worst endpoints to see whether the conclusion flips (~$300-500).
- Turn the harness into a scheduled public dashboard (ongoing ~$50/week).

## 7. Risks and how the plan handles them
- **Under-specified "same request".** Endpoints differ in template handling and reasoning-effort support. Fix all
  parameters, require parameter support, and classify each deviation as provider behaviour (that is the finding)
  rather than silently normalising.
- **Reference is itself questionable.** Two backends on the same weights define a noise band; claims are made only
  for deviations beyond it.
- **Endpoints rate-limit, vanish, or change mid-study.** Two sweeps a day apart quantify drift; report coverage
  honestly; 26 endpoints leaves slack.
- **Grader noise on legibility** (shown by lbernick to be grader-dependent). Legibility is one of four evals;
  the log-probability fingerprint and the monitor metrics need no judge.
- **Small monitor dataset (373 actions).** TPR at low FPR is noisy; use 3 samples per action, bootstrap CIs, and
  AUROC as the primary metric; add `anonymouslinuxarena/linuxarena-public` trajectories if CIs are too wide.
- **Accusation of sloppiness** (the parent post's reception). All transcripts, provider metadata and analysis code
  released; every headline number reproducible from logs; no claims about provider intent.
