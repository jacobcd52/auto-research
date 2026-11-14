# Feedback: 04 — "How much weak CoT grading does it take? A dose-response test of the linear-scaling assumption"

**Verdict: major overhaul.** The question is good and comes straight from Buck's review, but the stage-1 design does not test Buck's assumption. In the chosen environment the headline result for magnitude dilution follows from arithmetic, and the "vanilla policy gradient" comparison arm cannot be built as described on Tinker. The regime that matters (a CoT term that is small relative to persistent task-reward variance) is deferred to stage 2. Swap it into stage 1.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Buck's "quantitative question" and footnote-5 linear-scaling quotes | Verified verbatim against the post text. |
| Anthropic 8% of episodes (Mythos, Opus 4.6, Sonnet 4.6) | Verified in Buck's post. |
| "1.5% of trajectories for GPT-5.4 Thinking" | Matches Buck, but not the OpenAI post as it reads today: "less than 0.6% of GPT-5.4 Thinking samples and less than 1.5% of GPT-5.4 mini samples". Cite OpenAI directly and note the discrepancy. |
| OpenAI stress tests: standard-strength confidence reward gave no clear change; cheating penalty fired on about 5% falling to 2% | Verified on alignment.openai.com/accidental-cot-grading. |
| Tinker gpt-oss-20b $0.18 / $0.45 / $0.396 | Verified on the Tinker pricing page. |
| GPT-6 Luna $0.10 / $0.50 | Verified on the OpenRouter price list. |
| Tinker importance-sampling loss takes per-token advantages | Verified in the Tinker docs. |
| "Reused: the hint QA environment of Drori et al." | Overstated. Drori et al. (arXiv 2511.11584) ran Qwen3-4B on MMLU with six hint templates, batch 12, 3,200 episodes, and penalised the *output*, not the CoT. The paper says code is at "this repository", but I could not confirm the URL or that it is reachable. On gpt-oss-20b with a CoT penalty and Tinker this is a rebuild from the paper's appendix (hint list and judge prompt are printed there). It is small, but it is not reuse. |
| "A search found no dose-response study or open-weight replication" | **Not verified.** My web-search budget was exhausted before any query ran, so I have no independent novelty check. The only comment on Buck's post is unrelated. This needs re-checking before funding, especially for Redwood or OpenAI follow-ups to the review. |

## 1. Would it get upvoted?

Borderline: I put about 35% on more than 50 karma as written, and about 50% if redesigned as below.

- The audience is real. Buck's review got 76 and the GDM post got 131 four days ago. Buck, Ryan Greenblatt and the OpenAI authors would read a clean empirical test of footnote 5.
- The headline the proposal most expects ("in GRPO-style training a 30x smaller CoT effect is not 30x safer") would be attacked in the first comment. When the task reward is constant within a group, the std-normalised advantage is identical for every m > 0. That is an identity, and a reader can see it without an experiment.
- Nobody knows whether frontier pipelines normalise advantages per prompt group. If they normalise per batch, or not at all, the amplification does not apply. The post would be making a claim about an implementation detail of a small-scale recipe.
- The "all slopes near -1" outcome would be read as "linear scaling holds in a toy with no competing reward variance". That is weak support for a claim about a 1e-4 variance ratio.

## 2. Naturalness

The question is mainline. Buck asks it explicitly and says he knows of no evidence against linear scaling. The specific experiment is a side-step from it, for two reasons.

- **Buck's assumption is about the CoT term's share of total reward variance.** His example is a CoT effect with a standard deviation 1e-4 that of the total reward. The hint environment is chosen so that task reward saturates: baseline hint-following is required to exceed 80%, and training pushes it to about 100%. The CoT term is then nearly all of the within-group variance at every m. The experiment dilutes the penalty's absolute size but never its share of variance.
- **OpenAI's own ladder is already a crude closed-pipeline dose-response.** Standard strength gave no clear change; stronger pressure, or the CoT pressure alone, moved the CoT. That is the "small relative to the rest of the objective" regime, and it is the one this proposal skips.

## 3. Pre-mortem

**How it plays out.**

1. Day 1 morning: rebuild the hint environment on gpt-oss-20b. Baseline hint-following above 80% with randomised (mostly wrong) answers is doubtful without task-reward training first, and Chen et al. report that hint verbalisation is often low. The team rephrases hints and probably adds a task-only warm-up. The warm-up itself shifts verbalisation.
2. The undiluted arm suppresses verbalisation in tens of steps.
3. Normalised-magnitude arms finish at about the same speed for all m. At 95% hint-following, about two-thirds of 8-rollout groups have no task-reward variance, and in those groups m cancels exactly.
4. The un-normalised arm also shows a shallow slope, for a reason the proposal does not anticipate (Adam, below).
5. Frequency arms slow down, but by less than 1/p. The p = 0.03 points hit the cap or the budget rule and are censored or dropped.
6. The write-up reports slopes whose explanation is optimiser and normaliser arithmetic.

**Rough probabilities.**

| Outcome | Probability |
|---|---|
| Clear positive result that readers find informative | 20% |
| Clear negative that is still interesting | 15% |
| Ambiguous mush, or a result explainable by arithmetic | 45% |
| Fails to run cleanly in two days | 20% |

**Specific failure reasons, most serious first.**

- **The "vanilla policy gradient" arm is not vanilla on Tinker.** Tinker offers AdamW (default eps 1e-12) and Dimuon, not plain SGD. Adam's update is invariant to the scale of the gradient. Once task reward is saturated, an un-normalised advantage of size m gives a gradient proportional to m, and Adam divides the scale back out. So this arm will also tend towards slope 0, and the planned normalised-versus-un-normalised contrast collapses. The proposal's prediction of slope -1 for this arm is probably wrong for a reason unrelated to Buck's argument.
- **Frequency dilution is confounded by the same two mechanisms.** A group with one penalised rollout out of 8 gets a z-scored advantage of about -2.6 on that rollout, so rare penalties are amplified per episode. Adam then rescales whatever is left. Expect a slope between 0 and -1 that depends on group size and beta2, not on anything general.
- **Learning rate is tuned to be fast.** Suppression in 30-80 steps is far from Buck's "small learning rates" limit. Any non-linearity found can be dismissed as a large-step artefact.
- **Drift over long runs.** 1,500-step runs on a 4-way multiple-choice task with a LoRA will drift in CoT length and verbalisation. The control is two seeds, and T50 "relative to control" is undefined if the control itself falls by half.
- **Censoring.** If scaling is linear, the most diluted points need 1,000-2,600 steps and hit the 1,500 cap. Those are the points that give the slope its leverage, and they are the first ones the budget rule drops.
- **Single seed in the un-normalised arm.** RL seed variance in time-to-suppression is easily 2x.
- **Monitor evasion in place of suppression.** Schulz's result with the same model family shows gpt-oss learns to jailbreak weak monitors. The proposal tracks this with a held-out monitor only at the end; it needs to be tracked throughout, since T50 is defined on the training monitor.
- **Wall-clock.** A step is sampling 128 rollouts, 128 monitor calls and one Tinker clock cycle. I could not find a published clock-cycle duration; at 30-40 s per step, 1,500 steps is 12-17 hours. That fits only if the long runs start on day 1, but they depend on the learning-rate tuning from the undiluted arm, so the schedule has no slack.

## 4. Cost check

Unit prices and the per-step arithmetic are right: I get about $0.046 per step. The expected step count is optimistic.

- The $305 expectation assumes heavy early stopping. Controls never stop early: 3,000 steps, $140.
- If scaling is roughly linear (one of the hypotheses under test), frequency arms run about 5,000 steps over two seeds and the un-normalised arm about 2,500. With normalised arms at about 800 and controls at 3,000, that is about 11,300 steps, or $520, before tuning and margin.
- So the cheap case is the one where the proposal's favoured hypothesis is true. Otherwise the budget rule cuts the most diluted points.

My estimate: $350-500, landing at the cap in the linear world with the 30x points lost. The redesign below is cheaper (about $250-300) because it needs fewer long runs.

## 5. Recommended changes

1. **Make persistent task-reward variance the core of stage 1.** Move the stage-2 item "add irreducible task-reward noise" into stage 1 and drop the saturating design. Simplest version: keep the hint task but pay the task reward with probability q (or add zero-mean noise of fixed standard deviation sigma to every episode's reward). Then vary the ratio of penalty size to sigma over 30x. This is Buck's actual quantity.
2. **Simulate first, for free.** Before any Tinker spend, run a tabular or tiny-MLP bandit with the same reward structure, group size, normaliser and Adam settings. Write down the predicted T50 curves for each arm. The LLM experiment is worth paying for only where the simulation's prediction is non-obvious or where LLM behaviour could plausibly depart from it. Publish the simulation alongside.
3. **Fix the optimiser story.** State that Tinker is AdamW-only and that "vanilla policy gradient" is not available. Either treat Adam as the realistic case and derive what linear scaling means under it (signal-to-noise against other reward variance), or include one arm with a very small learning rate and many steps as the closest available check of the small-step limit.
4. **Cut the arm count.** Suggested set: two noise levels (saturated and high-noise) x three magnitudes (1, 0.1, 0.03) x normalised and mean-baseline, two seeds, plus three control seeds. Drop the 4-point frequency sweep to two points (p = 1 and p = 0.1), or defer it. Give every arm at least two seeds.
5. **Add a warm-up phase and a gate.** Train on task reward only until hint-following is stable, checkpoint, and branch all arms from that checkpoint. Gate: if verbalisation at the checkpoint is below 50%, or the control drifts by more than a third over 300 steps, stop and report that.
6. **Measure with a held-out monitor throughout**, not only at the end, and define T50 on the held-out monitor.
7. **Correct the framing.** Say the environment is rebuilt from Drori et al.'s appendix. Cite the OpenAI figures directly (below 0.6% for GPT-5.4 Thinking). State up front that per-group std normalisation makes m irrelevant when task reward ties, and present the experiment as measuring how far that holds once reward is noisy.
8. **Redo the novelty search before funding.** I could not run one.

If only one RL project in this cluster is funded, proposal 01 (uninstructed process judge) is the more natural and more timely choice. This one is worth funding only in the redesigned form, where either outcome bears on Buck's footnote.
