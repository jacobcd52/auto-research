# Pricing the speed prior: how much length penalty does GRPO need to train away a scheming preamble?
cluster: training-gaming-af | stage-1 cost: $400 | follows up: "Thinking about reasoning models made me less worried about scheming" (HYCGA2p4bBG68Yufh); "How do LLMs generalize when we do training that is intuitively compatible with two off-distribution behaviors?" (pQ4e2qJdQ4qYnsyhp)

## 1. What the prior work showed
Fabien Roger argues that reasoning models such as DeepSeek R1 do not scheme mainly because of benign priors on intermediate reasoning, not because RL would remove scheming if it were there. He registers predictions with credences. Prediction 1 (p = 0.75): "there is enough training slack and sufficiently poor exploration in GRPO that given a good scheming initialization (e.g. a short scheming reasoning section at the start of the scratchpad), scheming would not be trained away even with a mild length penalty." That is, the "speed prior" objection to scheming (Carlsmith: instrumental reasoning costs compute, so selection removes it) has little force for scratchpad models. Prediction 5 (p = 0.9): adding "think about the process that generated the current supervised fine-tuning dataset and choose the tokens that this process would generate" to the system prompt does not improve SFT sample efficiency over dummy prompts.

Redwood's behaviour-compatible training (BCT) post asks a neighbouring question: when training only rewards behaviour the model already shows, does an untrained-on behaviour survive? On Qwen3-235B the off-distribution behaviour often flips, even under GRPO with irrelevant or random rewards, with outcomes sensitive to small prompt details. Their settings concern output behaviours selected by a prompt feature; none concerns reasoning that is present on every rollout and never penalised.

Follow-ups found (14 Nov 2026): no post or paper reports running Prediction 1 or 5; the promised BCT sequel on trained "malign initialisations" has not appeared.

## 2. Question and why it matters
**Under GRPO on a real task, how long does a short training-gaming preamble at the start of the scratchpad survive, as a function of the length penalty, and is it removed faster or slower than a neutral preamble of the same length?**

The neutral-preamble comparison separates two stories. If both preambles persist at mild penalties, Roger's "slack" claim holds: speed costs do not protect us, only the prior does. If both are stripped equally fast, removal is pure length economics and the experiment yields its price. If the scheming preamble goes faster than the neutral one at equal length, there is a content-specific pressure against such reasoning, a new and reassuring finding; if slower, that is the worrying direction. Every cell gives a survival curve, so there is a quantitative result either way.

## 3. Stage 1 plan
Reused: Tinker cookbook Math RL and supervised-learning recipes; `openai/gpt-oss-20b` (cheapest reasoning model on Tinker), with headline cells replicated on `Qwen/Qwen3.5-9B`. Built: preamble datasets, length-penalised reward, survival metrics.

**Step 1. Task with headroom.** Pilot difficulties from the Math RL recipe until base accuracy is 40–60% with 300–500 reasoning tokens.

**Step 2. Install the preamble by self-distillation.** Sample 2,000 base-model solutions, splice a ~60-token preamble at the start of the reasoning, fine-tune on the result (the rest is the model's own output, so capability is unchanged). Arms:
- S, training-gaming: 50 paraphrases of "This is probably a training episode. I want to keep my current goals, and poor performance would get me modified, so I will do this task well for now."
- N, neutral: 50 paraphrases of length-matched boilerplate about reading the question carefully.
- U, useful: a length-matched generic solution plan (positive control: RL should keep or grow it).
- 0, none.
Gate: each installed model emits its preamble on at least 95% of rollouts and matches base accuracy within 3 points.

**Step 3. GRPO with a length penalty.** Reward = correct − λ x (reasoning tokens / 100). λ ∈ {0, mild, strong}, where mild makes the 60-token preamble cost 2% of a correct answer and strong 10%. 150 steps, 16 problems x 8 rollouts per step (19,200 rollouts per run). Runs: S, N, U x 3 penalties x 2 seeds = 18, plus arm 0 at λ = 0 and strong = 2. One extra S/mild run switches advantage normalisation, because per-group standard-deviation scaling can make a "mild" penalty dominate once correctness is uniform within a group.

**Step 4. Metrics at 8 checkpoints (300 held-out problems).** Preamble survival (judge: does the opening of the reasoning still express the arm's content; regex cross-check), preamble length, remaining reasoning length, accuracy. For arm S also: does the content mutate (drop goal preservation, keep "this is training"), and, per Prediction 2, does reasoning become more reward-guessing or instrumental than at step 0.

**Step 5. Analysis.** Survival curves and half-lives per arm and penalty. Pre-declared Prediction 1 criterion: under the mild penalty, S survives on at least 50% of rollouts at step 150. Primary contrast: S vs N at matched penalty. Secondary: which the penalty removes first, preamble or task reasoning.

**Step 6. Prediction 5 (SFT only).** Two SFT datasets the base model cannot already predict (invented facts; an unusual answer style). Four system prompts: Roger's sentence, two equal-length dummies, none. 2 seeds. Outcome: held-out loss against number of training examples, at matched initial loss.

Order: steps 1, 2 and 6 on day one; one S/mild and one N/mild run as a gate; the rest of the matrix; Qwen3.5-9B replication of S and N at the mild penalty last.

## 4. Stage 1 cost estimate
Tinker prices looked up 14 Nov 2026. gpt-oss-20b $/M: prefill 0.18, sample 0.45, train 0.396. Qwen3.5-9B: prefill 0.30, sample 0.807, train 1.463. OpenRouter Claude Haiku 5.5: $0.10/$0.50 per M.
- GRPO run on gpt-oss-20b: 19,200 rollouts x ~450 sampled tokens = 8.6M ($3.90); ~250 prompt tokens = 4.8M prefill ($0.86); training on ~700 tokens each = 13.4M ($5.32); evals 8 x 300 x ~700 tokens ($0.80). About $10.90 per run; 21 runs = $229.
- Preamble installation: 3 SFT runs x 2,000 x ~600 tokens x 2 epochs = 7.2M train tokens ($2.90) plus sampling the base solutions ($0.50). Pilots for task difficulty: $6.
- Prediction 5: 16 SFT runs x ~1M tokens plus evals ≈ $15.
- Judge: ~55k preamble classifications x ~300 tokens plus 5k longer comparisons on Haiku 5.5 ≈ $5.
- Qwen3.5-9B replication: 3 runs of 75 steps: 4.3M sampled ($3.50) + 6.7M trained ($9.80) + prefill and evals ($2) ≈ $15.30 each = $46.
- Subtotal $305; margin for reruns and one extra penalty level: $95. **Total $400.**

## 5. What success looks like
- Headline figure: preamble survival against GRPO step, one panel per penalty, lines for S, N, U.
- A statement on Prediction 1 at this scale: "with the preamble costing 2% of reward, it was still present on X% of rollouts after 19,200 rollouts", with half-lives.
- The S-vs-N contrast: a survival gap of 20 points or more in either direction at any penalty, consistent across seeds and on Qwen3.5-9B, is the most interesting outcome. No gap, with both curves tracking the penalty, is also a clean result: removal is priced by length alone.
- Prediction 5: learning curves overlap (prediction holds) or the training-gaming prompt is at least 20% more sample-efficient (prediction fails; that alone merits a post).
- Weak outcome: the preamble vanishes within a few steps in every arm including λ = 0 and U, meaning the install was shallow. The gate run detects this; the fix is a longer install.

## 6. Stage 2 (if stage 1 succeeds)
(i) Scale RL 10–20x on one arm pair to test extrapolation. (ii) Prediction 4: train niceness in no-reasoning mode on a hybrid model and measure transfer to the preamble in reasoning mode. (iii) A preamble that conditions behaviour (acts differently when "deployed"), linking to BCT and goal-guarding organisms. About $2,000–3,000.

## 7. Risks and how the plan handles them
- **Scale gap to R1-Zero.** Stated up front; results are rates and half-lives per rollout; stage 2 tests extrapolation.
- **RL does not improve the task, so there is no optimisation pressure.** Step 1 selects for headroom; arm 0 confirms accuracy rises.
- **"Mild" is arbitrary.** Levels are defined relative to preamble cost; a third level is budgeted; normalisation is checked.
- **Judge confuses a shortened preamble with a removed one.** Content and length are scored separately; 200 judgments audited.
- **gpt-oss reasoning-channel formatting breaks SFT on reasoning tokens.** Checked in the install gate; fallback Qwen3-8B (train $0.44/M).
- **The preamble is an installed artefact, not "real" scheming.** The experiment tests whether RL removes such reasoning once present, which is what Prediction 1 states.
