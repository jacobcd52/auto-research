# Does tie training beat plain regularisation on real preference data? Verbosity in UltraFeedback DPO
cluster: single-i2qTgh | stage-1 cost: $340 | follows up: Tie training can make DPO/RLHF-trained AIs generalize better (i2qTghrkyY9xdcCFq)

## 1. What the prior work showed
The paper (arXiv 2605.11134, ICML 2026) proves, for policies with utility linear in fixed features, that DPO and RLHF put weight on every feature correlated with true value, even with clean labels and infinite data. The fix is *tie training*: add pairs of equal true value with random labels, loss unchanged. The only LLM evidence is synthetic: Llama-3.2-1B-Instruct choosing between hotels, with spurious fields (street number, lobby size) correlated 0.99 with value. Strict-only DPO scores 92 / 74 / 64% (in-distribution / correlation removed / correlation reversed); adding 30% high-contrast ties gives 92 / 83 / 87%.

Follow-ups so far are synthetic or off-topic: "Selective Tie Learning" (arXiv 2610.35787) chooses which ties to add, on the hotel task plus an emoji task at 1B scale; RiskAverseOOD (arXiv 2607.02755) uses an SFT variant for risk aversion. The authors list real-world data and verbosity as future work, and a commenter asks for "a real test". I found none (caveat: arXiv API and direct fetches only; keyword web search was unavailable).

Two facts make the real-data question open. First, Chen et al. (arXiv 2409.17431) found that adding tied pairs to plain DPO *degraded* task performance and acted as stronger regularisation toward the reference model. So ties may simply mean "train less", and the original LLM experiment has no control for that (no higher beta, fewer steps, or random labels on non-tied pairs). Second, in real data the ties are certified by the same fallible judge that made the strict labels (the commenter's objection).

## 2. Question and why it matters
**On natural preference data, does tie training reduce a real spurious reliance (verbosity) more than generic regularisation does at the same cost to preference fit?**

Verbosity is the best-documented DPO shortcut (Singhal et al. 2310.03716; BA-DPO 2609.35044 shows lengthening at 8B scale on human labels). If tie training beats the regularisation frontier, labs have a near-free fix using tie labels they already discard. If it sits on the frontier, it reduces to "use a larger beta". If natural ties fail but constructed ties work, the judge-bias objection is confirmed and the practical recipe changes. Each outcome is a clear post.

## 3. Stage 1 plan
**Reused:** Tinker cookbook DPO recipe, which already loads UltraFeedback (https://tinker-docs.thinkingmachines.ai/cookbook/preferences/dpo-guide/); `openbmb/UltraFeedback` (MIT; 63,967 prompts x 4 completions with GPT-4 `overall_score`); `allenai/multipref` (human 5-way labels) for evaluation; the paper's hyperparameters (LoRA, beta 0.1, lr 1e-5, 1 epoch, 30% ties). **Built:** pair sampler, tie constructor, probes, analysis.

In a 500-prompt sample of UltraFeedback I checked, 18% of pairs tie exactly on score, the winner is longer in 61% of strict pairs, and 55% of ties differ in length by over 30%.

**Model:** Qwen3-8B on Tinker (thinking disabled), LoRA.

**Arms** (same 8,000 strict pairs, 3 seeds each unless noted):
1. Strict-only DPO (baseline).
2. + 30% natural ties (equal GPT-4 score, random labels).
3. + 30% natural ties selected for large length contrast ("informative").
4. + 30% constructed ties: an LLM rewrites a response to roughly half or double length keeping content fixed; a second model verifies equal quality; random labels.
5. Control, data volume: + 30% extra strict pairs.
6. Control, label noise: + 30% extra *non-tied* pairs with random labels.
7. Control, regularisation frontier: strict-only at beta 0.2, 0.5, 1.0 and at 25/50/75% of steps (1 seed each, checkpoints saved).
8. Named-feature baseline: strict pairs subsampled so the winner is longer exactly 50% of the time.
9. Amplified setting: strict pairs subsampled so the winner is longer 90% of the time, with arms 1-4 repeated (2 seeds). This guarantees a large effect to mitigate.

**Metrics** (all on held-out prompts):
- *Length-opposed accuracy.* Held-out strict pairs split into length-aligned (winner longer) and length-opposed (winner shorter), 1,500 each, scored by which response gets the higher DPO implicit reward. This mirrors the paper's in-distribution vs adversarial splits. Repeated on MultiPref pairs with a clear human majority.
- *Length weight.* Implicit-reward gap between long and short members of 1,000 held-out verified constructed ties (zero means length-blind).
- *Behaviour.* Mean tokens generated on 500 held-out prompts, relative to the base model.
- *Quality.* Pairwise win rate against the base model on those prompts (gpt-5-mini, both orders, length-neutral rubric); plus accuracy on 300 short-answer questions as a judge-free check.
- *Off-radar features.* About eight surface features (lists, headers, opening affirmations, closing offers, hedges, apologies): win-correlation in the strict data and each arm's implicit-reward weight. This tests the claim that ties shrink untargeted features, where arm 8 should not.

**Key analysis:** plot length weight and length drift against in-distribution preference accuracy for every arm-7 checkpoint; this is the frontier. Tie arms are selective only if they fall below it by more than seed and bootstrap noise. Arm 6 separates "ties" from "any random labels". Arms 2 vs 4 separate judge-certified from constructed ties.

**Order:** (1) pilot: one strict-only run, confirm length drift and a length-opposed accuracy gap; (2) build ties and probes, hand-read 50 constructed ties; (3) arms 1-8; (4) arm 9; (5) evaluation and frontier analysis; (6) write-up.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14. Tinker Qwen3-8B: train $0.44, sample $0.60, prefill $0.195 per million tokens.
- Training: about 800 tokens per pair; 8,000-11,400 pairs is 6.4-9.1M tokens, $2.80-$4.00 per run. About 50 runs (arms 1-6 and 8: 21; frontier 6; amplified 8; pilots and reruns 15) at $4 = **$200**.
- Reference log-probabilities, computed once and cached: about 20M prefill tokens = **$4**.
- Evaluation per checkpoint: implicit-reward probes about 4M prefill tokens ($0.80) plus 500 generations ($0.25); 60 checkpoints = **$63**.
- Judge: 1,000 calls per final checkpoint x about 1,300 input and 60 output tokens on gpt-5-mini ($0.25 / $2.00) = $0.45; 35 checkpoints = **$16**.
- Tie construction: 4,000 rewrites on claude-sonnet-4.6 batch ($1.50 / $7.50), about 2M in and 1.6M out = $15; verification on gpt-5-mini $3 = **$18**.
- Subtotal $301; margin for failed runs **$39**. **Total $340.**

## 5. What success looks like
One figure (frontier plus each arm with error bars) and one table (length-opposed accuracy, length weight, length drift, win rate).
- *Clear positive:* ties at least halve length weight and drift relative to strict-only, raise length-opposed accuracy, and beat frontier checkpoints of equal in-distribution accuracy; arm 6 does not.
- *Clear deflation:* tie arms lie on the frontier and match arm 6: generic shrinkage, as Chen et al. suggest.
- *Judge-bias result:* constructed ties work; natural ties leave a residual positive length weight.
- *Off-radar result:* ties do, or do not, shrink untargeted features that length-balancing leaves alone.

A null is publishable provided strict-only DPO does learn length; the amplified arm exists to make sure there is something to remove. An ambiguous outcome would be effects within seed noise everywhere; with 1,500 pairs per split the bootstrap interval on an accuracy is about +/-2.5 points, so differences under about 4 points will not be claimed.

## 6. Stage 2 (if stage 1 succeeds)
About $1,500-2,500: (a) sycophancy versions with purpose-built preference data and standard sycophancy evals; (b) classical RLHF: train a reward model with and without ties, measure its length weight, then RL a policy against it; (c) a controlled biased-judge study where strict labels and ties come from judges of differing bias; (d) larger models (Qwen3.8-27B, $4.10 per million training tokens).

## 7. Risks and how the plan handles them
- *No baseline verbosity effect on Qwen3-8B.* The pilot checks this for under $10; fall back to the amplified setting as the main experiment.
- *GPT-4 labels are themselves length-biased.* Report MultiPref human-label and short-answer results alongside; the constructed-tie length weight does not depend on GPT-4 labels.
- *Constructed ties are not really ties.* Second-model verification, hand-read sample, verified subset only.
- *Judge length bias.* Both orders, length-neutral rubric, win rate stratified by length difference.
- *Implicit-reward scoring bugs* (chat template, thinking tokens). Unit-test that the base model scores exactly zero reward and that our scorer reproduces the recipe's training accuracy.
- *Over-claiming from 3 seeds.* Pre-specify the frontier comparison; report every arm, including nulls.
