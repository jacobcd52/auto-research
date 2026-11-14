# Feedback: "What do 1,000 rollouts buy you? Amortised resampling as the downstream test for global CoT analysis"

Reviewer verdict: **major overhaul**. The core question is sound and cheap, but the plan as written is too broad for two days, contains two factual errors that affect the design, and its most upvotable component (importance recovery) is the one most likely to fail as designed. A narrower version built around ground truth that already exists is worth funding at about $150–250.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Parent post: ~1,000 rollouts, 7 prompts, ~100 prefixes × 150 resamples, graph has best mean RMSE, roughly ties Gemini 3 Pro with 20 rollouts, constant 50% beats several baselines, 1,000-rollout Gemini run on one prompt at ~$280 | Confirmed from the post text |
| "Finding downstream tasks to test methods against is a priority" | Confirmed (post and README) |
| Future-work doc asks "What can we learn from 500 that we can't learn from 10?" and rates cheaper importance scores highly | Confirmed (doc exported as text). The importance item has 4 stars |
| Code public at Centrattic/global-cot-analysis | Confirmed via raw.githubusercontent (README, `src/main.py`, `src/generation/generate_responses.py`, `src/utils/model_utils.py`) |
| Traces repo contains rollouts and prefix ground truth | **Not verifiable** from this sandbox (github.com 403, raw README 404), same as the proposer found |
| "Subject model gpt-oss-20b throughout, as in the post" | **Wrong.** The post says "bagel", one of the six test prompts, was generated with Claude Sonnet 4.5 |
| "The authors' code pins a provider" for prefill | True, but the pin is `wandb/fp4`, and **that provider is no longer listed** among OpenRouter's gpt-oss-20b endpoints today (current: Darkbloom, AkashML, PrimeIntellect, DekaLLM, CoreWeave, DeepInfra, Parasail, SiliconFlow, Bedrock, Groq) |
| "Their seven prompts" are in the reused code | The public repo's `PROMPT_FILTERS` contains only `hex` and an example. The seven prediction prompts are in the post appendix and must be re-entered by hand. The post also says the authors are "happy to share our research code", which implies the deployment repo is not the full research code; whether the no-clustering and Gemini baselines are in it is unverified |
| Prices: gpt-oss-20b $0.03/$0.13, gpt-6-luna $0.10/$0.50 (1.05M ctx), gemini-4-hydrogen $1.5/$7.5, gpt-4o-mini $0.15/$0.60 | Confirmed against OpenRouter `/api/v1/models` today |
| uzaymacar/math-rollouts public | Confirmed: ungated, MIT, 20 problems × correct and incorrect base solutions for two open models (deepseek-r1-distill-qwen-14b, deepseek-r1-distill-llama-8b) |
| "I found no follow-up" | The LessWrong post has 0 comments and 0 pingbacks. arXiv API queries for the method name and for prefix/rollout outcome prediction returned nothing relevant. **My web-search budget was exhausted in this session, so the novelty check is limited to arXiv API queries and LessWrong; treat it as weaker than a full search.** |

## 1. Would it get upvoted?

Probably not above 50 as written. My estimate is 15–20%.

- The parent post got 52 karma and zero comments with Neel Nanda as co-author. A baseline audit of it by an unknown author starts well below that. The companion benchmark post got 59.
- The headline the plan can most reliably deliver is "a logistic regression on prefix embeddings matches or beats the semantic graph". The authors already said the graph is "too large, dense, and messy to reliably tell us anything meaningful" and that "none of the methods perform very well". Confirming that with one more baseline is a footnote, not a post.
- The probe result is not new in kind. Zur et al. (arXiv 2511.04527) already report that hidden activations predict a model's future outcome distribution during CoT; Zhang et al. (2504.05419) and Chan et al. (2507.12428) show probes predicting final correctness or alignment mid-reasoning; the companion benchmark post compares probes with text methods at length.
- The one component with a real audience is part B: importance scores without per-sentence resampling. Thought Anchors and Thought Branches users would care. But the plan's own version only helps someone who already has 1,000 rollouts on the same prompt, which is a narrow regime, and it is the part most likely to return noise (section 3).

A version that could clear 50: "Sentence importance from a probe, validated against Thought Anchors' own resampling data, across problems", with the graph comparison as a secondary section.

## 2. Naturalness

Mainline in intent. It answers a question the authors wrote down themselves and tests their four-star idea. Supervised value regression on free labels is the obvious missing baseline and any reader of the post would ask for it.

Less natural parts:
- The LLM-in-context scaling arms. The post already found 1,000 rollouts no better than 20 for Gemini. Repeating it with a cheap 1M-context model is unlikely to change the conclusion and is the largest single API cost.
- Cross-prompt training on six puzzles and testing on the seventh. Six training prompts is not a meaningful sample for generalisation; the result will be near base rate and uninformative.
- Part C is outcome prediction on a sycophancy-flavoured prompt, not a sycophancy measurement. It is fine as a domain check but it is not what makes the project safety-relevant.

I found no evidence that this exact experiment has been done, with the search caveat above.

## 3. Pre-mortem

How two days will likely go: the first half-day goes to getting the authors' pipeline running, re-entering prompts, and finding a provider whose completions endpoint honours a reasoning-channel prefill for gpt-oss-20b now that `wandb/fp4` is gone. Rollouts and ground truth are then regenerated (the traces repo may or may not help). Regressors and the probe get built on day one evening. Scaling graphs, LLM arms, part B and part C all compete for day two, and at least one is dropped or done thinly.

Rough outcome probabilities for the plan as written:

| Outcome | Probability |
|---|---|
| Clear positive (clean method ordering and importance recovered well above noise) | 15% |
| Clear negative that is still interesting (simple predictors match the graph; importance not recoverable; cleanly shown) | 30% |
| Ambiguous mush (methods within error bars of each other, importance ratio noisy) | 40% |
| Fails to run to a reportable state | 15% |

Specific failure reasons, most important first:

1. **Train/test leakage in the inherited design.** The post samples its ~100 test prefixes from the same 1,000 rollouts used to build the graph. Every test prefix therefore has its own source rollout, with its own outcome, in the training pile. A nearest-neighbour or gradient-boosted model on prefix embeddings will find it; so will the graph's top-20 match. The proposal does not mention holding the source rollout out. Without that, the supervised numbers are inflated and the scaling curve depends on whether a subset happens to include the source rollout.
2. **Part B is underpowered by construction.** Importance is a difference of two estimates, each with SE up to 0.05 at 100 resamples, so the difference has SE up to 0.07. Most chunks have true importance near zero. Spearman correlation over mostly-null items is dominated by noise, the split-half ceiling (50 vs 50 resamples, difference SE ~0.10) will itself be low, and "more than half the ceiling" becomes a ratio of two noisy numbers. Smooth predictors such as a whole-prefix embedding will also change little between adjacent prefixes, so their predicted differences are mostly estimator jitter. Only 60 rollouts on 4 prompts back the claim.
3. **The "1% of the cost" claim does not hold up.** The predictor needs 1,000 rollouts on the same prompt first. Resampling one rollout fully costs about 3,000 rollouts here. The saving only appears when many traces on one fixed prompt are analysed, and cross-prompt transfer, which would make it a tool, cannot be tested with seven prompts.
4. **Effects are small relative to noise in part A.** The post's methods were bunched near a constant predictor. With ~100 prefixes per prompt, an RMSE gap of a few points is within bootstrap error on a single prompt. The stated success criterion "7 of 10 prompts" is not significant on its own (sign test p ≈ 0.17).
5. **"Bagel" breaks the design.** It is a Sonnet 4.5 prompt: no activations for the probe, and resampling from a thinking prefix on a closed model is not something to count on. Either drop it or regenerate it with gpt-oss-20b, in which case its base rate may no longer be interesting.
6. **The reproduction gate is ill-defined.** Published RMSEs exist only as points in a figure, and regenerated data will come from a different provider and quantisation. "Match the published RMSE on two prompts" cannot be checked precisely.
7. **Probe hardware.** gpt-oss-20b ships MXFP4-quantised. I recall, without having checked it this session, that plain `transformers` loading without the MXFP4 kernels falls back to bf16 at roughly 48GB. A 24GB card is a risk; a 48GB card costs about the same.
8. **Scope.** Five method families × four pile sizes × three subsets × ten prompts, plus cross-prompt, plus two new ground-truth collections, plus about 100 graph builds through an LLM-merge pipeline. This is exactly the long fragile pipeline the programme warns about.
9. **Unsurprising either way.** "Probe beats text" and "simple supervised beats hand-built graph" are both what most readers would predict.

## 4. Cost check

The total is realistic and is not the binding constraint. My estimate for the plan as written is $250–400, under the $500 cap.

- Generation lines are fine. 180k resamples at ~400 input and ~300 output tokens is about $10 at current prices.
- The LLM-in-context line is understated. The all-1,000 condition alone is 10 prompts × 100 prefixes × 3 repeats × ~$0.04 = $120, against $60 budgeted for all conditions. It fits only with prompt caching (rollouts first, prefix last) or the batch endpoint at half price. Add about $45 for the 30/100/300 arms across three subsets.
- Graph construction at 1.5M gpt-4o-mini tokens per graph is a guess; nothing in the README supports it. Measure on the first graph before launching 100 of them.
- If prefill through OpenRouter fails, running gpt-oss-20b under vLLM on the GPU already rented for the probe is cheaper and cleaner than Tinker, and gives text and activations from the same weights.

The overhauled version below should cost about $150–250.

## 5. Recommended changes

In order of importance:

1. **Rebuild part B on Thought Anchors' public data and make it the headline.** `uzaymacar/math-rollouts` already holds 100 resamples per sentence for 20 problems × 2 base solutions on two open models that fit a 48GB card. Every resample is a labelled rollout, so the "pile" exists and the importance ground truth is already paid for. Train a value probe and a text value regressor on resample outcomes, split by problem (train on 15, test on 5, rotated), and score predicted adjacent-sentence differences against the released importance. This gives a real cross-problem test, hundreds of base-solution sentences instead of 60 rollouts, and zero generation cost. The proposer deferred this to stage 2 over leakage; a problem-level split removes that concern. If it works across problems it is a usable tool; if it works only within problem, that is a clear, honest negative.
2. **Fix the leakage in part A.** For every test prefix, remove its source rollout from all training piles and from the graph's candidate set. Report with and without, since the difference is itself informative about the post's numbers.
3. **Cut part A to what answers the question.** Keep: base rate, the graph predictor, one text regressor (prefix embedding plus logistic regression), one probe, and the scaling curve at N = 30, 100, 300, 1,000. Drop TF-IDF variants, the six-train-one-test cross-prompt arm, and the stronger-LLM arm. Keep at most one LLM-in-context condition (20 retrieved rollouts).
4. **Correct the model claim.** Drop "bagel" or state that it is regenerated with gpt-oss-20b. Five gpt-oss-20b test prompts plus the AIME dev prompt is thin, so add 6–10 new puzzle prompts screened for 20–80% accuracy; rollouts cost cents.
5. **Settle generation on day one.** Test a completions-endpoint prefill on two current providers in the first hour. If it is not exact, serve the model locally with vLLM on the rented GPU and generate everything there.
6. **Replace the reproduction gate.** Use "the graph predictor beats the base-rate predictor by a stated margin on regenerated data for two prompts", not a match to figure-read numbers.
7. **Fix the statistics in advance.** Paired bootstrap over prefixes, clustered by prompt, for every method comparison; report RMSE within the 10–50% determinism bucket separately, since deterministic prefixes dominate otherwise. For importance, report precision and recall on sentences whose true importance is distinguishable from zero, not Spearman over all sentences.
8. **Make part C conditional.** Run the sycophancy prompts only if parts A and B finish by the end of day one. If run, add the paired no-user-preference arm so the outcome is a sycophancy effect and not just a verdict.
9. **Drop the "1% of the cost" framing** unless the cross-problem result in change 1 supports it. State the amortisation break-even honestly: how many traces must be analysed on one prompt before the pile pays for itself.
10. **Rent a 48GB card**, not 24GB, and verify activation extraction on one rollout before anything else depends on it.

If the funder must choose within this cluster, the benchmark follow-up (proposal 01) is the stronger bet; this one is worth funding only in the overhauled form and at the lower price.
