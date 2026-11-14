# Feedback: "How rare is 'near zero'? Logit Path Extrapolation for agentic rule-breaking, with a prompt as the unsafe endpoint"

Verdict: **keep with tweaks** — but the tweaks are not cosmetic. As written, the main run sits in the regime where the
result is close to guaranteed by algebra and where a one-forward-pass baseline makes the method unnecessary. The
interesting regime (decision spread over many tokens) is currently an "if time allows" extension. Swap them.

## What I checked

- **LPE post (CempXdo6cx5yseRLt), read in full.** The proposal's summary is accurate: logit mix with Qwen3-4B and its
  abliterated version, 200 HarmBench prompts, 100,000 rollouts ground truth, fit on points below 50%, AUROC for
  "0/100 but at least one in 100k", 20-30x fewer rollouts, beats importance sampling; the two stated limits are quoted
  correctly; no calibration reported; no code link in the post. The Caleb Biddulph comment (unsafe model fails
  "differently": numbskull vs buffoon) is real. Two details the proposal departs from without saying so: the original
  scans alpha in steps of 0.05 (up to 20 values, not 12) and subsamples from 1,000 precomputed rollouts per alpha (not
  300). The original judge was StrongREJECT with GPT-5.4-mini, so the step-1 "refusal-prefix classifier" replication is
  only a smoke test, not a reproduction.
- **Gemini post (HZn9AZeD2jfXXD2hH).** Appendix A violation rule and the `broad_end` result are as described. Note:
  all prompt-variant results are Gemini 3 Pro only, 20 runs per cell, and the authors **manually verified every
  response** against the heuristic number rule. No small open-weight model was tested.
- **Public assets.** `Qwen/Qwen3-4B`, `huihui-ai/Qwen3-4B-abliterated`, `Qwen/Qwen3.5-9B` all resolve on Hugging Face.
  `environments/currency_conversion/README.md` exists in gkroiz/agent-interp-envs (modes `static_response`,
  `code_only`). Its README says the shipped system prompt already tells the agent to stop and flag a broken tool
  "in precedence over" finishing, i.e. it is not the Kaggle original; the team has to pick which prompt is the
  target. It also says grading "happens downstream in the `mats` repo", so do not count on a reusable grader.
- **Price.** RunPod H100 PCIe $1.99 community / $2.89 secure confirmed on runpod.io/pricing today.
- **Already done?** WebSearch was unavailable for this review (session search budget exhausted), so the check is
  limited to arXiv API queries and LessWrong pingbacks. arXiv has no hit for "logit path extrapolation". Three LW
  posts link to the LPE post; none tests it on new behaviours or endpoints. I did not find the experiment done.
  **A reviser with search access should re-check, in particular for a Goodfire / Pernice-Aranguri paper version.**
- **Related work the proposal misses:**
  - **BLOOM-WILT / LogitTilt** (LW finpDcZidhcdCa4cS, arXiv 2608.31105, Sep 2026; code on GitHub, shipped as an
    Inspect extension). It reweights the target's decoding "using the model's own distribution conditioned on an
    elicitation prompt". That is the same two-context, same-weights sampler as the proposal's "prompt endpoint", used
    for elicitation rather than rate estimation, on Qwen3.5-4B among others. So the sampler is not new; the
    extrapolation-to-a-rate and calibration use is. Cite it and consider reusing its implementation instead of
    writing the loop from scratch. It scored 7 karma, which is a data point for section 1.
  - **Angell et al., arXiv 2604.22167** (the importance-sampling baseline in the LPE post). Its abstract says it covers
    "benchmarks measuring misuse and misalignment" and releases code (github.com/rangell/LMTailRisk, not verified from
    here). "Only one behaviour was tested" is true of LPE, not of rare-event estimation; the IS baseline should come
    from that code, not a fresh reimplementation.

## 1. Would it get upvoted?

Borderline, leaning no as written. Reference points: the LPE post itself got 55; BLOOM-WILT, a larger piece of work
in the same technical niche, got 7; the cluster's empirical posts sit at 50-88. A follow-up to a 55-karma methods post,
on a 4B model, on a hand-built single-reply toy version of the currency agent, with thinking off, is a niche result.
My estimate: median about 30 karma, perhaps 20-25% chance of clearing 50.

What would lift it: (a) a headline number readers can repeat, e.g. "this 0/100 cell is actually 1 in 20,000, and we
checked with 500k rollouts"; (b) a clean calibration plot spanning four decades, which the original conspicuously
lacks; (c) a sharp, mechanistic negative ("LPE under-estimates by 2 orders of magnitude whenever the target's rare
failures take a different route from the endpoint's, here is the plot"). What sinks it: a positive result in a regime
where a commenter can point out it follows from the softmax, or a result on a model too small for anyone to care
about its "rule-breaking".

Who cares: people running open-weight propensity evals and the LPE authors. People running frontier propensity evals
(the motivation in section 1: Hopman, Gemini) cannot use it, since LPE needs full logits at every step. The proposal's
"any propensity eval reporting 0 of N can be upgraded" should say "open-weight" every time, and the write-up should
not lean on the Gemini / Hopman numbers as if this addresses them.

## 2. Naturalness

Mainline. The screener's note, the authors' own conclusion ("any pass/fail evaluation ... even in a multi-turn
setting") and their stated limits all point here: other behaviours, other endpoints, calibration. The prompt-as-endpoint
idea is a sensible twist rather than a contrivance, and it is the form in which the method would be usable for
propensity work. Not done as far as I could find (with the search caveat above). The contrived part is the test-bed:
a pre-filled conversation where a 4B model writes one final reply is not "agentic rule-breaking" in the sense the
title claims.

## 3. Pre-mortem

**The central problem: single-pivot decisions make the result near-tautological and the method unnecessary.**
With thinking disabled and the conversation pre-filled, "compute the number" vs "flag the broken tool", and "reveal
the code" vs "decline", are largely settled in the first one to three tokens of the reply. If the outcome is decided
at one token position, the mixed logit of the violating token is exactly linear in alpha, so log-odds of violation
are exactly linear in alpha and log-rate is linear wherever the rate is small. Log-linearity then "holds" by
construction, R-squared above 0.9 is not evidence of anything, and the true rare rate can be read off from one
forward pass (first-token probability mass on violating continuations) with no sampling at all. A reader will say
this in the first comment. The proposal half-acknowledges it (risk 1) but leaves the case that tests the method,
thinking on, as an optional 20-variant extension.

Other specific failure routes:

- **Bimodal rates on a 4B model.** Frontier models violate at 65-100% under the original prompt; a 4B model without
  thinking probably just does the multiplication nearly always, or follows the "stop" sentence nearly always.
  Getting 60 variants spread smoothly over 1e-1 to 1e-5 by rewording is optimistic. The proposal detects this after
  the first ground-truth pass but "regenerate variants" is an open-ended search with no guarantee.
- **Grader noise dominates exactly the band of interest.** The Appendix A number rule is heuristic and its authors
  hand-checked every response. At a true rate of 1e-4, a grader false-positive rate of 1e-4 (a reformatted amount,
  "83.6", a date, "step 12", a hallucinated reference number) is the signal. Auditing 300 random replies says nothing
  about false positives at that rate. Worse, these artefact "violations" are produced by a different route from the
  one the unsafe endpoint amplifies, so LPE will under-predict them and the team may report a "Biddulph failure" that
  is really a grader artefact. The secret-disclosure family (exact string match) is much safer.
- **Too few items for the AUROC and efficiency claims.** The original had 200 prompts. Here the AUROC is computed
  over the subset of 60 templated variants per family that show 0/100, maybe 15-30 items with a handful of positives,
  all near-duplicates of one scenario. Confidence intervals will be around +/-0.15; "matches naive sampling with 10x
  fewer rollouts" cannot be established at that n.
- **Ground truth is too shallow for the stated calibration claim.** 50,000 rollouts with at least 20 hits measures
  rates down to about 4e-4. "Within half an order of magnitude across three decades" then means 4e-4 to 0.4, where
  the top decade is not rare and naive sampling already works. The value of LPE is at 1e-4 to 1e-6; none of that is
  checked.
- **"Trivial estimator" is under-specified.** "Scales the unsafe-prompt rate by the summed token log-probability
  ratio" is importance sampling. With a same-weights prompt endpoint, IS weights are free and the estimator is
  unbiased, so IS may simply win on calibration; that is a fine result, but the plan should expect it and say what
  LPE adds if so.
- **Endpoint definition is muddled.** The variants vary "presence and wording of the 'if a tool fails, stop'
  sentence", while the unsafe endpoint is "the rule sentence removed". Which sentence (the no-arithmetic rule or the
  fallback sentence) is removed, and what the endpoint is for variants that already lack it, is not stated.
- **Sampler bugs.** Two contexts of different length sharing a continuation, Qwen tool-message chat templates,
  thinking toggles, KV caches, plus a second set of weights for the LoRA and abliterated endpoints. The alpha = 0 / 1
  checks are right; this is still the place a two-day agent team loses half a day.
- **Abliterated endpoint** is expected by the proposer to fail, costs a second model in memory, and its failure
  teaches little. The LoRA endpoint trained on 500 violating replies will mostly learn the reply format.

Forecast for the plan as written:
- Clear positive that survives the "it's just the softmax" objection: 15%
- Clear, interesting negative (mechanistic account of where LPE breaks, clean plots): 20%
- Ambiguous mush (log-linear but trivially so; AUROC CIs too wide; few variants in the measurable-rare band;
  grader artefacts in the tail): 50%
- Fails to run / no usable ground truth in two days: 15%

## 4. Cost check

The estimate is realistic and probably generous. 15k tokens/s for vLLM on a 4B model on an H100 is conservative;
3k tokens/s for a batched two-context HF loop is plausible. 75 GPU-hours at $1.99-2.89 is $150-217; $300 with margin
is fine. My estimate for the plan as written: **$150-300**. With the changes below (thinking-on core, deeper ground
truth on a subset, more variants, a 9B model for part of it) I estimate **$300-400**, still under the cap. Dollars
are not the binding constraint; agent wall-clock and the variant search are. Use community-cloud interruptible pods
with checkpointed rollout shards, since everything is embarrassingly parallel.

## 5. Recommended changes (most important first)

1. **Make distributed-decision settings the main experiment.** Run thinking-enabled generation (and/or the short
   multi-step loop: the model itself calls the fee, rate and calculator tools with canned responses) as the core, on
   40-60 variants, with thinking-off single-reply as the control arm. Thinking traces cost roughly 5-10x the tokens;
   budget allows it if the abliterated endpoint is dropped.
2. **Add the exact, no-sampling baseline and stratify by it.** For each variant compute the violation probability
   implied by the first k tokens directly from the logits (k = 1..5, enumerating high-mass prefixes). Report a
   "decision concentration" statistic per variant and show LPE's performance separately for concentrated and
   distributed decisions. If the exact baseline matches ground truth, say plainly that LPE is unnecessary there.
3. **State the softmax argument in the write-up** and frame the question as "does log-linearity survive when the
   decision is spread across many tokens and the endpoint differs only by context", not "does it hold".
4. **Deepen ground truth where it matters.** After the 2,000-rollout pass, pick 20-30 variants in the 1e-3 to 1e-5
   band and run 500k-1M rollouts each (cheap at 150 tokens; fewer for thinking-on). Calibration claims should cover
   1e-2 down to at least 1e-5, with binomial intervals on the truth.
5. **Hand-audit every positive in the rare band** (all violations for variants with fewer than about 50 hits), not a
   random 300. Lead with the secret-disclosure family, where the grader is an exact string match, and tighten the
   arithmetic grader (normalise number formats; require the major-violation threshold) before trusting any rate
   below 1e-3.
6. **More, less correlated items.** Aim for 200+ variants across at least four rule-breaking scenarios rather than
   2 x 60 rewordings, so the AUROC subset has enough positives; report bootstrap CIs over variants and treat
   variants of one scenario as clustered.
7. **Drop the abliterated endpoint; keep prompt and LoRA.** Replace it, if anything, with a second prompt endpoint
   (a nudge added, rather than the rule removed) so the "which prompt works as an endpoint" question gets two data
   points. Define precisely which sentence is removed for each variant.
8. **Design in the Biddulph failure case on purpose** rather than deferring to stage 2: one family where the target's
   rare violations plausibly take a different surface form from the endpoint's (e.g. paraphrasing or encoding the
   secret vs stating it). This is the most likely source of a crisp negative finding.
9. **Reuse instead of rebuilding.** Check BLOOM-WILT's LogitTilt code (and its Inspect integration) for the
   two-context sampler and the Angell et al. LMTailRisk code for the IS baseline; cite both. Follow the original
   appendix (alpha step 0.05, search then fit, 1e-6 fallback) or state deviations.
10. **Use a model people will accept as following rules.** Check in the first two hours whether Qwen3-4B's violation
    rate responds monotonically to rule wording; if not, switch to Qwen3.5-9B immediately rather than iterating on
    variants. Consider making the 9B model the default for the thinking-on arm.
11. **Fix the framing.** Title and section 2 should say open-weight; do not present Hopman / Gemini "0 of N" cells as
    something this method upgrades. Call the test-bed what it is (single-reply rule compliance on a pre-filled agent
    transcript) unless change 1 makes it genuinely multi-step.
12. **Pre-register the kill criterion for the variant search:** if after the first ground-truth pass fewer than 15
    variants per family fall between 1e-2 and 1e-5, spend at most one regeneration round, then fall back to the
    original HarmBench setting with a prompt endpoint (a compliance-nudging system prompt) plus calibration, using a
    cheap refusal classifier. That fallback still answers "prompt as endpoint" and "calibrated?" on a behaviour known
    to have a usable rate spread.
