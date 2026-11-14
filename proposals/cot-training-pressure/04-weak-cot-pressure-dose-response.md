# How much weak CoT grading does it take? A dose-response test of the linear-scaling assumption
cluster: cot-training-pressure | stage-1 cost: $430 | follows up: "A review of 'Investigating the consequences of accidentally grading CoT during RL'" (juCHTdZpZBGooHKW4); environment from "[Paper] Output Supervision Can Obfuscate the CoT" (HuoyYQ6mFhS5pfZ4G)

## 1. What the prior work showed
OpenAI disclosed that RL graders could see chains of thought in a small share of training for recent models (1.5% of trajectories for GPT-5.4 Thinking). Anthropic reported CoT exposure in 8% of episodes for three models. OpenAI argued monitorability was unharmed: the grader's rewards were not measurably changed by CoT access and a monitorability score stayed flat. Their closed-pipeline stress tests found no clear change from a standard-strength CoT reward, and that an explicit penalty on CoT mentions of cheating fired on about 5% of samples, falling to 2%.

Buck's review accepts most of this but isolates the open quantity: "how much training do you need to do before weak training pressure damages the CoT monitorability of a model?" His bound relies on an assumption he flags as untested: if the CoT-dependent part of the reward has a standard deviation 1e-4 times that of the total reward, then training on N trajectories changes the CoT about as much as training on 1e-4 x N trajectories where the CoT is all of the variance. "This is what you'd predict in the limit of vanilla policy gradients and small learning rates, and I am not aware of research that is strong evidence against this linear scaling."

Kaufmann et al. and Drori et al. use full-strength rewards on every episode. A search on 2026-11-14 found no dose-response study or open-weight replication of sparse CoT grading.

## 2. Question and why it matters
When a CoT penalty is diluted, either by applying it to a fraction p of episodes or by shrinking its magnitude by a factor m, does the number of training steps needed to suppress the penalised verbalisation scale as 1/p and 1/m?

There is a specific reason to doubt linearity for magnitude. GRPO-style algorithms normalise advantages by the within-group standard deviation. Once the task reward saturates within a group, every rollout has the same outcome reward, and a CoT term of any non-zero size becomes the entire normalised advantage. If so, Buck's "divide by the effect size" bound is too optimistic for any pipeline that normalises advantages. Frequency dilution should not be amplified this way. If both dilutions are linear, the review's reasoning gets its first empirical support. Either result gives a rule for converting "x% of episodes, effect size y" into expected damage.

## 3. Stage 1 plan
**Reused:** the hint question-answering environment of Drori et al. (after Chen et al., 2505.05410): a multiple-choice question whose correct answer is randomised, with a hint that states it ("My professor told me the answer is C"). The task reward is 1 for the hinted answer, so the model must use the hint, and at baseline its CoT usually says so. Tinker RL recipes (tinker-cookbook) and the Tinker importance-sampling loss, which accepts arbitrary per-token advantages. **Built:** the reward mixing and the two advantage estimators.

**Policy:** gpt-oss-20b on Tinker with low reasoning effort (CoTs of about 200 tokens), chosen for price.

**CoT penalty:** a monitor flags whether the CoT mentions the hint (GPT-6 Luna, binary). Reward = task reward minus m x flag, applied on a random fraction p of episodes. The monitor is run on all episodes for measurement.

**Arms** (128 rollouts per step: 16 questions x 8):
- Frequency dilution, GRPO-normalised advantages: p = 1, 0.3, 0.1, 0.03 with m = 0.5. Two seeds.
- Magnitude dilution, GRPO-normalised: m = 0.5, 0.15, 0.05, 0.015 with p = 1. Two seeds.
- Magnitude dilution, un-normalised advantages (reward minus group mean, the "vanilla policy gradient" case): the same four m values. One seed.
- No-penalty control at the longest run length. Two seeds. This measures drift and any spillover-like change unrelated to the penalty.

Each run stops when the verbalisation rate (monitor-flagged share among hint-following answers) has stayed below 10% for 20 steps, or at a cap: 200 steps for the undiluted arm, scaling up to 1,500 for the most diluted.

**Step 0 (about $10).** Confirm baseline hint-following above 80% and hint verbalisation above 60% for gpt-oss-20b in this format; adjust the hint phrasing once if needed. Run the undiluted arm first to fix the learning rate so that suppression takes 30-80 steps, leaving headroom to resolve 30x slow-downs.

**Metrics.**
- T50 and T10: steps until verbalisation falls to 50% and 10% of baseline.
- Dose at T50: number of penalised episodes seen, and cumulative penalty mass (p x m x episodes).
- Hint-following accuracy and CoT length throughout.
- For magnitude arms, the within-group standard deviation of the task reward over training, to show when normalisation begins to amplify the CoT term.
- Held-out monitor (keyword match plus a second LLM) at the end.

**Analysis.** Log-log plot of T50 against p and against m, with the slope and interval for each arm. Slope -1 means linear scaling. The prediction to test: slope near -1 for frequency, near -1 for un-normalised magnitude, and near 0 for normalised magnitude after task reward saturates.

## 4. Stage 1 cost estimate
Tinker gpt-oss-20b: prefill $0.18, sample $0.45, train $0.396 per million tokens. GPT-6 Luna: $0.10 in, $0.50 out.
- Per step: sampling 128 x 200 tokens = 25.6k, $0.012; prefill 128 x 250 = 32k, $0.006; training 57.6k tokens, $0.023; monitor 128 calls x (400 in, 10 out), $0.006. About $0.047 per step.
- Step caps: frequency arms (200 + 500 + 1,000 + 1,500) x 2 seeds = 6,400; normalised magnitude arms, expected short, capped at 400 x 4 x 2 = 3,200; un-normalised magnitude arms 200 + 500 + 1,000 + 1,500 = 3,200; controls 1,500 x 2 = 3,000. Worst case 15,800 steps = $745; with early stopping the expected total is roughly 6,500 steps = $305.
- Hard budget rule: the p = 0.03 and m = 0.015 points run last and are cut to one seed or dropped if spend passes $330 before they start.
- Step 0, learning-rate tuning, final held-out monitoring: $40.
- Margin: $60.
Total: about $430 (capped; the design degrades to three dilution levels if needed).

## 5. What success looks like
One figure carries the post: T50 versus dilution factor on log-log axes for the three arms. A clear finding is any of:
- Normalised-magnitude runs suppress verbalisation almost as fast at m = 0.015 as at m = 0.5, while frequency dilution slows roughly as 1/p. Headline: "in GRPO-style training a CoT effect 30 times smaller is not 30 times safer; coverage matters, magnitude does not".
- All three arms have slope near -1. Headline: Buck's linear assumption holds over a 30x range in an open model, with the constants.
- Sub-linear or threshold behaviour in frequency (for example no suppression at p = 0.03 within 1,500 steps while the linear prediction says about 1,000). Headline: sparse grading is safer than linear scaling predicts, at this scale.

A null would be slope intervals that include both 0 and -1; the most informative contrast (normalised vs un-normalised magnitude at m = 0.05) needs only four short runs. The post must say this is a toy-scale test of the form of the scaling argument, not of frontier numbers.

## 6. Stage 2 (if stage 1 succeeds)
- Targeted rare-event version of Buck's scenario: the penalised content appears in only 1-5% of episodes at baseline (as with mentions of misaligned goals), and the question is whether it is trained out before a general monitorability metric moves. About $300.
- Add irreducible task-reward noise and a harder task where reward never saturates, to map when normalisation amplifies. About $200.
- Replace the explicit penalty with the uninstructed process judge of proposal 01, and repeat on gpt-oss-120b. About $400.

## 7. Risks and how the plan handles them
- **Long runs dominate wall-clock time.** Runs are independent and launched in parallel on day one; the most diluted points start first and are the ones dropped if they do not finish.
- **Verbalisation drifts without any penalty** (spillover or general fine-tuning drift), confounding long runs. The no-penalty controls at full length measure this and T50 is computed relative to them.
- **The policy escapes by not following the hint, or by jailbreaking the monitor.** Hint-following is tracked; the held-out monitor and a keyword check detect monitor-specific evasion. Either would be reported, and T50 is defined on hint-following answers only.
- **Result depends on implementation details of advantage normalisation.** That dependence is the hypothesis; both estimators are implemented explicitly through the importance-sampling loss and unit-tested on synthetic rewards.
- **Over-generalising from a toy.** The write-up reports slopes, not safety thresholds.
- **Overlap with proposal 01.** Different question and environment; if both are funded they share one RL harness, saving about $40 of debugging.
