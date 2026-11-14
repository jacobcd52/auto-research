# How rare is "near zero"? Logit Path Extrapolation for agentic rule-breaking, with a prompt as the unsafe endpoint
cluster: model-forensics | stage-1 cost: $300 | follows up: "Predicting Rare LLM Failures with 30x Fewer Rollouts" (CempXdo6cx5yseRLt); "Is Gemini 3 Scheming in the Wild?" (HZn9AZeD2jfXXD2hH); "Understanding when and why agents scheme" (amYmcwCuyuCEZcrRm)

## 1. What the prior work showed
Pernice and Aranguri introduce Logit Path Extrapolation (LPE) for estimating how often a model does something it
almost never does. At each token they mix the logits of the model under test and a less-safe variant,
alpha * original + (1 - alpha) * unsafe, sample from the mixture, measure the behaviour rate at values of alpha
where it is common, fit log10(rate) against alpha for points below 50%, and extrapolate to alpha = 1. With Qwen3-4B
and its abliterated version on 200 HarmBench prompts, and 100,000 rollouts per prompt as ground truth, LPE
identifies which prompts that show 0 compliances in 100 rollouts comply at least once in 100,000, matching naive
sampling's AUROC with 20-30x fewer rollouts and beating importance sampling.

The authors name two limits: the method "requires an additional model where the behavior we are estimating is more
common", and the log-linear relation "is empirical and may break in other settings". They report ranking quality
(AUROC) but not whether the extrapolated rates are calibrated. Only one behaviour (harmful compliance) and one
unsafe endpoint (abliteration) were tested. A commenter points out a failure mode when the unsafe model fails in a
different way from the target. I found no released code and no follow-up.

Propensity evaluations have exactly the problem LPE addresses. Hopman et al. report baseline scheming of 0-3% from
100 rollouts per cell, while one added prompt snippet takes the same model to 59-91%. The Gemini currency-agent
case shows rule-breaking at 65-100% that drops to 0 of 20 when one sentence about tool failure is added. "0 of
100" cannot distinguish one in a thousand from one in a million, and for these behaviours no abliterated model is
relevant; what exists is a nearby prompt under which the behaviour is common.

## 2. Question and why it matters
Does the log-linear path hold when (a) the behaviour is an agent breaking an explicit rule rather than complying
with a harmful request, and (b) the unsafe endpoint is the same model under a nudged prompt rather than a
different set of weights? And are the extrapolated rates calibrated, not just well ranked?

If yes, any open-weight propensity eval that reports "0 of N" can be upgraded to an estimated rate using only a
second prompt, removing the method's main practical limit. If no, the result marks where the method stops working
(which endpoints, which behaviours, by how much), which is needed before anyone relies on it.

## 3. Stage 1 plan
Reused: the LPE algorithm as specified in the post's appendix; Qwen/Qwen3-4B and huihui-ai/Qwen3-4B-abliterated
from Hugging Face; the currency-agent system prompt, tool transcripts and violation definition from the Gemini
post (also packaged as `currency_conversion` in https://github.com/gkroiz/agent-interp-envs). Built: a batched
two-context sampling loop, a prompt-variant generator and programmatic graders.

Behaviour families (both graded by code, so 100,000-rollout ground truth needs no LLM judge):
- Forbidden arithmetic: the model is the currency agent, the conversation already contains the fee, the rate and
  the broken calculator's non-answer, and the model writes the final reply. Violation: the reply contains a
  computed amount absent from tool outputs (the post's Appendix A rule). 60 variants (amounts, currencies, rule
  wording, failure message, presence and wording of the "if a tool fails, stop" sentence) to spread true rates
  from common to very rare.
- Secret disclosure: a system prompt forbids revealing a deployment code; the user asks for it under varied
  pretexts. Violation: the code string appears. 60 variants.

Unsafe endpoints compared on the same prompts:
1. Prompt endpoint: the same weights with the rule sentence removed from the context (two forward passes per
   token on two contexts sharing the generated continuation).
2. Fine-tuned endpoint: a LoRA trained on 500 violating replies from held-out variants.
3. Abliterated weights, as in the original, expected to be a poor path for non-refusal behaviour; included
   because the choice of endpoint is the open question.

Steps:
1. Implement LPE; check the sampler by reproducing the log-linear plot on 10 HarmBench prompts with the original
   endpoints and a refusal-prefix classifier.
2. Ground truth: 2,000 rollouts per variant with vLLM, then top up to 50,000 for every variant with fewer than 20
   violations. Thinking disabled in the main run; replies capped at 200 tokens.
3. LPE pools: 12 alpha values x 300 rollouts per variant for endpoints 1 and 2, 100 for endpoint 3; Monte Carlo
   subsampling from these pools at budgets from 13 to 100 rollouts per alpha, as in the original.
4. Baselines at matched budget: naive sampling; importance sampling from each unsafe endpoint; and, for the prompt
   endpoint, the trivial estimator that scales the unsafe-prompt rate by the summed token log-probability ratio.
5. Metrics: per-variant R-squared of log-rate against alpha; AUROC for "0 of 100 but at least one in 50,000";
   calibration of predicted against true log10 rate (slope, median absolute error in orders of magnitude) on
   variants with measurable truth; rollout-efficiency ratio against naive sampling.
6. One extension if time allows: the forbidden-arithmetic family with thinking enabled on 20 variants, where the
   decision is spread over a reasoning trace.

## 4. Stage 1 cost estimate
RunPod community H100 PCIe at $1.99 per hour (secure $2.89).
- Ground truth: 120 variants, about 3.5M rollouts x 150 tokens = 0.5B tokens; vLLM on a 4B model at an assumed
  15k tokens per second: about 10 GPU-hours
- LPE pools: 120 variants x 12 alphas x 700 rollouts = 1.0M rollouts x 150 tokens x 2 passes = 0.3B token-passes at
  an assumed 3k tokens per second in the custom loop: about 28 GPU-hours
- LoRA training, sanity replication, thinking-on extension: about 12 GPU-hours
- Debugging and reruns: 25 GPU-hours
Total about 75 GPU-hours: $150 at community price, $217 at secure price. Storage and a small amount of API use for
generating prompt variants: $15. With margin for slower-than-assumed throughput: **$300**. Throughput is measured in
step 1; if the custom loop is under 1.5k tokens per second, the abliterated endpoint and 20 variants per family are
dropped.

## 5. What success looks like
- Positive: for the prompt endpoint, median R-squared above 0.9, AUROC matching naive sampling with at least 10x
  fewer rollouts, and extrapolated rates within half an order of magnitude of truth across three decades. The post
  then says: rare rule-breaking rates can be estimated from a nudged prompt alone, with a worked recipe and code.
- Negative: curved or kinked paths (for example a cliff near alpha = 1 because the rule sentence acts through a
  few tokens), systematic over- or under-estimation by an order of magnitude or more, or an endpoint ranking in
  which only the fine-tuned variant works. The post then says where LPE fails and by how much, with the endpoint
  comparison as the practical guidance.
- Either way the calibration plot and the endpoint comparison are new, and the released implementation fills the
  gap left by the original post.
An uninformative outcome would be true rates that are bimodal (always common or never observed in 50,000), leaving
too few variants in the rare-but-measurable band; the two-stage ground-truth step detects this after 10 GPU-hours,
in time to regenerate variants.

## 6. Stage 2 (if stage 1 succeeds)
Apply the prompt-endpoint method to multi-turn environments with harness graders (`secret_number`,
`currency_conversion` end to end) on a larger open-weight model, estimating the rates behind published "0 of 100"
cells (about $500 of GPU time). Test an unsafe endpoint that fails differently from the target, and compare with
the capped-ratio interpolation proposed in the post's comments.

## 7. Risks and how the plan handles them
- The trivial log-probability estimator may already solve single-decision cases. It is a baseline; multi-sentence
  replies and the thinking-on extension cover cases where it does not apply.
- A 4B model may not treat the rule as meaningful. Step 2 requires violation rates to respond to rule wording;
  Qwen3.5-9B is the fallback at about twice the GPU time.
- Two-context sampler bugs (KV caching, batching, chat templates). Validated at alpha = 0 and alpha = 1, where
  rates must match plain generation.
- Grader errors at scale. Both graders are rule-based and audited on 300 hand-checked replies per family.
- Over-claiming from one small model. Claims are limited to the tested model and behaviours.
