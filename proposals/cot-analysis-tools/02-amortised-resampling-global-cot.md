# What do 1,000 rollouts buy you? Amortised resampling as the downstream test for global CoT analysis
cluster: cot-analysis-tools | stage-1 cost: $280 | follows up: "Global CoT Analysis: Initial attempts to uncover patterns across many chains of thought" (q9g9zuudd3Pvw2cbj)

## 1. What the prior work showed
Tyagi, Ivanova, Conmy and Nanda study a "global CoT": about 1,000 reasoning traces from one model (mostly gpt-oss-20b) on one fixed prompt. Their main method, semantic step clustering, chunks every trace, clusters chunks by sentence embedding plus LLM merge judgements, and turns each trace into a walk on a graph (35x compression).

The one quantitative test is prediction: given a prefix of a CoT, predict the fraction of continuations that end in the correct answer. Ground truth is 150 resamples for each of about 100 prefixes per prompt, on seven prompts (one for tuning, six hand-written puzzles for test). The graph-based predictor had the best mean RMSE. It roughly tied Gemini 3 Pro shown 20 random rollouts and beat embedding-similarity baselines. But the authors note that no method did well: a constant 50% guess beat several baselines. Gemini with all 1,000 rollouts in context was tried on one prompt only, at about $280 per prompt.

The authors write that "finding downstream tasks to test methods against is a priority". Their linked future-work document asks, unanswered, "What can we learn from 500 [rollouts] that we can't learn from 10?", and rates "importance scores cheaper than Thought Branches" as a potentially major contribution. (Thought Anchors and Thought Branches measure how much each sentence matters by resampling from every sentence, which costs hundreds of rollouts per sentence.)

I found no follow-up. Missing from the post: any supervised predictor (each rollout labels all of its own prefixes with its final outcome for free), activation probes, any curve over the number of rollouts, and any prompt that is not a math or logic puzzle. Code is public (https://github.com/Centrattic/global-cot-analysis), with the traces at https://github.com/Centrattic/global-cot-traces.

## 2. Question and why it matters
**Given a pile of rollouts on one prompt, how well can you predict what resampling would show, how does that scale with the size of the pile, and does the graph help compared with simple learned predictors?**

Resampling is the trusted way to study CoT causally and its cost is the main obstacle. A predictor trained on a rollout pile that approximates resampling outcomes would make sentence-importance analysis nearly free. If simple predictors beat the graph, graph construction is not needed for this purpose and the field gets a usable tool. If the graph wins as rollouts increase, global CoT analysis gains its first solid quantitative support. If only an activation probe beats the base rate, outcomes are not readable from text here. The dull outcome is everything at the noise floor; section 7 covers it.

## 3. Stage 1 plan
Subject model gpt-oss-20b throughout, as in the post. Reused: the authors' code for rollouts, prefix resampling, graph building and graph prediction; their seven prompts; their released traces. Built: the new predictors, the scaling harness, and new ground truth for parts B and C.

**Part A: baseline audit on the seven original prompts.** Compare, by RMSE against the 150-resample ground truth (noise floor: binomial SE up to 0.041):
1. Base rate and constant 50%.
2. The authors' graph predictor and no-clustering baselines (reproduced from their code).
3. Value regressors: every prefix of every rollout labelled by that rollout's own final correctness; logistic regression or gradient boosting on (a) an embedding of the whole prefix, (b) embeddings of the last three chunks plus position, (c) TF-IDF.
4. LLM in context: 20 random rollouts, 20 retrieved most-similar rollouts, 100, and all 1,000, using a cheap 1M-context model (openai/gpt-6-luna).
5. Value probe: linear probe on gpt-oss-20b residual activations at the last prefix token, trained on the same free labels (24GB GPU).

**Scaling.** Each method at N = 30, 100, 300, 1,000 rollouts, three random subsets each.

**Cross-prompt.** Train methods 3 and 5 on six prompts and test on the seventh with zero rollouts from it.

**Part B: importance recovery.** On four prompts, take 15 held-out rollouts each and resample 100 times from every chunk boundary (about 30 per rollout). True importance of a chunk is the change in P(correct) across it. Score each method's predicted changes by Spearman correlation and by recall of the three largest true jumps, against a split-half noise ceiling.

**Part C: one safety-flavoured prompt family.** Take Scruples moral-dilemma items with a stated user preference (the sycophancy setup of the companion benchmark post). Screen about 60 items and keep three where gpt-oss-20b sides with the user 30–70% of the time. Generate 1,000 rollouts and 100 prefixes × 150 resamples each. The outcome is "agrees with the user". Repeat part A.

Order: reproduce the authors' graph numbers on two prompts; then A, scaling, B, C.

## 4. Stage 1 cost estimate
| Item | Calculation | Cost |
|---|---|---|
| Part B ground truth | 4 × 15 × 30 × 100 = 180k resamples; ~72M input + 54M output tokens at $0.03 / $0.13 per M (OpenRouter gpt-oss-20b) | $10 |
| Part C rollouts and resamples, screening | ~50k rollouts, under 40M tokens | $5 |
| Regenerating original ground truth if not in the traces repo | 7 × 100 × 150 resamples | $5 |
| Fallback: prefix resampling on Tinker if OpenRouter prefill misbehaves | 60M tokens × $0.45/M | $27 |
| Graph construction for scaling runs | ~150 graphs × ~1.5M gpt-4o-mini tokens | $40 |
| LLM in-context baselines | 10 prompts × 100 prefixes; all-1,000 condition ~400k tokens × $0.10/M = $0.04 per call, three repeats, plus smaller conditions | $60 |
| One stronger model at 20 and 100 rollouts | ~1,000 calls × ~40k tokens × $1.5/M (gemini-4-hydrogen) | $60 |
| GPU for value probe | 24GB card, ~20 h incl. setup × ~$0.7/h | $15 |
| Margin (~25%) | | $58 |
| **Total** | | **$280** |

Prices from OpenRouter `/api/v1/models` and the Tinker pricing page, 2026-11-14.

## 5. What success looks like
- A table and one scaling plot (RMSE vs number of rollouts, one line per method, noise floor marked) across ten prompts.
- A clear ordering, for example: "a logistic regression on prefix embeddings with 300 rollouts beats the semantic graph with 1,000 on at least 7 of 10 prompts", or the reverse; and whether the activation probe beats all text methods.
- Part B: predicted importance correlating with true importance at more than half the noise ceiling (enough to claim "resampling importance at about 1% of the cost"); or a clean negative, where prefix-level prediction works but adjacent-prefix differences cannot be recovered.
- Part C: the same ranking on sycophancy prompts, plus how early in the CoT the eventual agreement with the user becomes predictable.

If all text methods sit near the base rate but the probe does not, that is still a result. If everything, probe included, sits at the base rate, the project yields only a short negative note.

## 6. Stage 2 (if stage 1 succeeds)
- Validate the best amortised predictor against the public Thought Anchors resampling data (uzaymacar/math-rollouts) and Thought Branches blackmail rollouts (~$100).
- Use it to produce importance maps on safety-relevant prompts at scale (eval awareness, reward hacking on open models) and check the top anchors by targeted resampling (~$400).
- Package it as a drop-in command in the authors' codebase.

## 7. Risks and how the plan handles them
- **Everything at the noise floor.** The post's own numbers were close to a constant predictor. Early check after part A on two prompts: if the best RMSE is not 20% below the base-rate predictor, move budget to part C and stratify by prefix determinism as the authors did.
- **Importance is a difference of two noisy estimates.** 100 resamples per boundary and a split-half ceiling; report relative to the ceiling, not raw correlation.
- **Graph pipeline does not reproduce** (LLM merge judgements, provider changes). Gate: match the published RMSE on two prompts; otherwise use the authors' released graphs at N = 1,000 and say so.
- **Prefill on gpt-oss-20b through OpenRouter is provider-dependent.** The authors' code pins a provider; fallback is Tinker raw-token sampling, budgeted above.
- **Traces repo contents unverified** (could not be listed while writing this). Regeneration is budgeted.
- **Limited interest.** The parent post drew modest attention. Lead the write-up with the tool (cheap importance scores) and the sycophancy prompts, not the baseline audit.
