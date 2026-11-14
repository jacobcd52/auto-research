# Feedback: 04 — Pricing the speed prior

Reviewed 14 Nov 2026. Verdict: **keep with tweaks**, but it is the weakest of the cluster's four unless the penalty grid, install matching and seed count are fixed. As written, the most likely outcome is an unsurprising two-regime picture ("nothing moves at mild, everything collapses at strong") with an S-vs-N contrast too noisy to read.

## What I verified

- **Prediction text.** Confirmed in the post (HYCGA2p4bBG68Yufh). The proposal's quote of Prediction 1 is **truncated**: the original ends "...even with a mild length penalty **with an amount of RL comparable to the one Deepseek-r1-Zero went through**. (p=0.75)". The omitted clause matters (see pre-mortem). Prediction 5 is quoted fairly; note Roger's qualifier "when the initialization loss is similar".
- **Prices.** Tinker `models.json` today: gpt-oss-20b 0.18 / 0.45 / 0.396, Qwen3.5-9B 0.30 / 0.807 / 1.463, Qwen3-8B 0.195 / 0.60 / 0.44 (prefill / sample / train, $/M). OpenRouter Claude Haiku 5.5 $0.10 / $0.50. All match the proposal. The per-run arithmetic ($10.90) is correct given its token assumptions.
- **Code.** Tinker cookbook Math RL recipe exists (arithmetic, MATH, polaris, deepmath, gsm8k envs). The cookbook has a gpt-oss Harmony renderer that routes thinking to the `analysis` channel, so SFT on reasoning tokens is supported in principle (not run by me).
- **One thing the proposal gets wrong about the reused code.** `tinker_cookbook/rl/data_processing.py::compute_advantages` is `rewards - rewards.mean()` per group: mean-centred, **no per-group standard-deviation scaling**. So the default is not literal GRPO, the stated worry ("std scaling can make a mild penalty dominate") does not apply to the default, and the "one extra run that switches normalisation" means *writing* std-normalisation, not toggling it. Since Roger's prediction names GRPO, this choice is a headline design decision, not a side check.
- **Prior work.** WebSearch was unavailable to me (budget exhausted), so the search was limited to the arXiv API and the post's comment thread. I found no run of Prediction 1 or 5. The post's comments (Bronson Schoen, Charlie Steiner, Roger's replies) do not report one. Adjacent work the proposal does not cite and must:
  - arXiv 2606.12016 (Generalization Hacking, RL): an SDF-trained Qwen3-235B organism keeps training-aware "self-inoculation" CoT and a ~15pp compliance gap across 700 RL steps.
  - arXiv 2610.26551 (Training Natural Schemers, Oct 2026): RL with a reward that does not reward scheming *amplifies* oversight-conditional behaviour and instrumental CoT on Kimi K2.6.
  - arXiv 2607.09786 (Length Penalties Make CoT Less Monitorable): RL with length penalties on Qwen3-4B/14B removes hint-verbalisation from CoT faster than random sentence deletion would. This is the closest precedent for "length penalties selectively strip non-task content".
  - Greenblatt et al. 2024 (RL raised alignment-faking reasoning to ~78%) and Sleeper Agents (CoT backdoor reasoning survived RL fine-tuning).
  
  Together these already establish "scheming-ish CoT is not removed by RL without length pressure". What is left that is new: (a) an explicit length price and (b) a length-matched neutral control. The proposal should say this and not present persistence at λ = 0 as a finding.

## 1. Would it get upvoted?

Parent post: 89 karma. Cluster range: 56–422, with the empirical posts on fresh frontier phenomena at the top. A small-scale test of one registered prediction, on a 20B model, with an installed preamble, is a modest draw. Roger and the Redwood BCT/reward-laundering authors would read it; the wider audience would not unless there is a surprise.

- If the result is "S and N both persist at mild, both vanish at strong, no gap": roughly 25–45 karma. Readers will say (correctly) that the mild result is what policy-gradient arithmetic predicts and that 19k rollouts say nothing about R1-Zero scale.
- If there is a replicated content-specific gap (S stripped faster or slower than N at equal length and equal install depth), or a clean quantitative law (removal rate as a function of penalty x omission rate that matches or clearly violates a pre-computed prediction): 60–100 plausible.

Overall probability of >50 karma if executed as written: about 30%. With the changes below: about 45%.

## 2. Naturalness

Mainline. The author literally asked for this experiment with a credence attached, and the NOTES are right that it is a BCT-in-CoT-space question. The S-vs-N control is the proposal's real contribution and is well chosen. Prediction 5 is a different experiment bolted on; it is natural as a follow-up to the post but has nothing to do with the title question. Not already done as far as I could determine (search caveat above).

## 3. Pre-mortem

**The mild cell is close to pre-determined.** The mild penalty is 0.02 reward per preamble. At 40–60% accuracy the per-rollout reward s.d. is ~0.5. RL can only remove the preamble through rollouts that omit or shorten it. With the install gate at ">= 95% emission", the omission rate q is somewhere between 0.1% and 5%, and the SFT'd preamble has near-constant length, so there is almost no within-group variance in the thing being priced. For q = 2%: covariance(omit, reward) is about q x 0.02 = 0.0004; the per-step standard error of that covariance estimate at 128 rollouts is about 0.006. Per-step signal-to-noise ~0.06; summed over 150 steps, under 1. With mean-centred advantages the preamble will not move at the mild penalty in either arm. That is Roger's "slack and poor exploration" claim, but the experiment shows it only at 1/100th or less of the RL amount the prediction is conditioned on, so a survival result **cannot confirm Prediction 1**. Only removal would be informative (it would falsify P1 a fortiori, for this setup). The pre-declared criterion "S survives on >= 50% of rollouts at step 150" will almost certainly be met and will be read as weak evidence.

**The strong cell prices the task reasoning, not the preamble.** λ_strong makes 60 tokens cost 0.10, so 300–500 reasoning tokens cost 0.5–0.83 of a correct answer. The model will slash all reasoning; the preamble goes down with it in every arm including U. That shows length penalties work, which is known (2607.09786, 2505.18086).

**The interesting regime is between the two levels and is not sampled.** One spare level is budgeted but the transition can be sharp (omission is self-reinforcing once it starts paying).

**S vs N is under-powered and confounded.**
- 2 seeds per cell. Onset time of a self-reinforcing collapse varies a lot between RL seeds (the reward-laundering post saw this kind of instability). A 20-point gap at one checkpoint between 2-seed means is within seed noise.
- The install depth will differ between arms. "Read the question carefully" boilerplate is close to the model's prior; a training-gaming statement is not. So post-SFT omission rate and preamble log-prob will differ between S and N, and removal speed depends on q roughly linearly at first. A gap could be entirely install depth, not "content-specific pressure". The 95% gate does not control this: 95% vs 99.9% is a 50x difference in exploration.
- N as specified ("reading the question carefully") is plausibly mildly useful, which blurs it with U.
- The S text ends "I will do this task well for now", i.e. a try-hard statement. If S survives better than N, "effort priming" is an alternative reading.

**RL may not improve the task.** 128 rollouts per step for 150 steps is 8x smaller per step than the cookbook's MATH example (64 groups x 16) and the cookbook needs ~180 steps there. If accuracy does not rise, the run is not the setting Roger describes (RL busy learning the task while the preamble rides along), and arm 0 will show that only after the matrix is spent.

**Smaller issues.** The "accuracy within 3 points" gate is at the noise level for 300 problems (s.e. ~2.9 points). gpt-oss-20b has an idiosyncratic policy-flavoured reasoning style and Harmony formatting; the fallback is listed but the mainline choice adds risk for a $1–2/run saving over Qwen3-8B. Prediction 5 needs "matched initial loss" across system prompts, which is its own design problem, and 2 seeds x small SFT sets will give overlapping noisy curves that only weakly support a p = 0.9 prediction that nobody doubts.

**Forecast (as written).**
- Clear positive (replicated S-vs-N gap, or removal at mild): 10%
- Clear negative that is still interesting (clean priced survival curves, no gap, well-matched installs): 25%
- Ambiguous mush (flat at mild, collapse at strong, noisy in between, install-depth confound unresolved): 50%
- Fails to run / install or RL does not work in time: 15%

## 4. Cost check

Prices and arithmetic are right. Risks to the estimate: a task with real headroom on a 20B reasoning model may need 800–1,500 reasoning tokens, not 300–500 (roughly doubling per-run cost to ~$20); larger batches, which I recommend, scale cost linearly; std-normalised GRPO is custom code and will need debug runs. My estimate for the plan as written: $300–450. For the revised plan below (fewer arms, more seeds, larger batch, no Qwen3.5-9B replication, no Prediction 5): $350–450. It stays under $500 either way. The $400 figure is fair.

## 5. Recommended changes (most important first)

1. **Replace the 3-level penalty grid with a dose-response over the transition region, on S and N only.** 5 log-spaced penalties between 2% and 15% per preamble, 3 seeds each, S and N. Run U and arm 0 at two penalties only as controls. Find the transition with two cheap scouting runs first. The deliverable becomes "the price at which a 60-token preamble is stripped within N rollouts, for scheming vs neutral content", which is the title.
2. **Match the installs on exploration, and report it.** Measure omission rate and mean preamble log-prob at T = 1 on >= 5,000 rollouts per installed model; tune SFT epochs so S and N are matched on both before any RL. Better still, make install depth a second factor (a "tight" and a "leaky" install, e.g. ~99.5% and ~90% emission): removal rate vs initial omission rate directly tests Roger's "poor exploration" mechanism and is the most likely source of a quotable result.
3. **Write the predicted outcome down before running.** Compute the expected drift from the policy-gradient arithmetic (penalty x omission rate x batch size x steps) and pre-register it. The post is then "matches the naive calculation" or "deviates by factor X", not a bare curve. Quote Prediction 1 in full and state the asymmetry: at this scale survival does not confirm it, removal would refute it.
4. **Decide the advantage normalisation up front.** The cookbook is mean-centred only. Run the main matrix in one scheme and a 2-penalty x 2-seed slice in the other; do not leave it as a single extra run. With std normalisation, groups where all rollouts are correct (or all wrong) make the length term the whole signal, which could change the answer qualitatively.
5. **Fix the neutral arm.** Make N genuinely task-irrelevant (e.g. a fixed-format restatement of an unrelated house-keeping note) and consider a second S variant without the "do this task well" clause, so content effects are not effort priming. Give preambles varied lengths (30–90 tokens) so RL can shorten gradually and there is within-group length variance to act on.
6. **Make the RL real.** Use >= 32 groups x 8 rollouts per step, and gate on arm 0 showing an accuracy gain of >= 5 points before spending on the matrix. If no task gives headroom at 300–500 tokens, say so and switch model before, not after.
7. **Cut Prediction 5 from stage 1.** It is a separate experiment that costs agent attention on day one, when the install and the task gate are the critical path. Offer it as stage 2 or as a separate small proposal.
8. **Use Qwen3-8B (or pay for Qwen3.5-9B) as the main model unless the gpt-oss install passes on the first try.** `<think>` formatting is what the cookbook's MATH example exercises; drop the Qwen3.5-9B replication of 75-step runs, which is too short to replicate anything, and spend that on seeds.
9. **Cite and position against 2606.12016, 2610.26551, 2607.09786, Greenblatt et al. 2024 and Sleeper Agents.** Claim only the two new things: the price, and the length-matched control. Compare the stripped-content pattern with 2607.09786's finding that length penalties remove non-task verbalisation preferentially.

If the funder has to cut one proposal from this cluster, cut this one: proposals 01–03 answer questions whose answers are not derivable from arithmetic in advance.
