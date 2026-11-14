# Feedback: "Can a model launder reward into a propensity?" (proposal 02, cluster training-gaming-af)

Verdict: **keep, with substantial design changes.** The question is the parent authors' own, the infrastructure is real and the price is right. As designed, though, the headline comparison is partly degenerate and the most likely result ("it transfers") is what most readers would predict.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Parent post numbers (0.37 to 0.58 over 5 seeds, direct reward 0.57, on-policy SFT 0.21, base-rollout SFT 0.36, shuffled 0.14, leakage 0.09 annealed vs 0.67-0.96) | Confirmed against the post and the repo README. |
| The "Propensities" open question is quoted from the post | Confirmed, verbatim. |
| Codebase is public with A/B/C/D conditions, `group_rewards`, GRPO loop, tests, "$6k" matrix cost | Confirmed via raw.githubusercontent.com (`README.md`, `lib/coupling.py`, `lib/rl_conditions.py`, `lib/rl_train.py`, `lib/config.py` all return 200). |
| Tinker prices for Qwen3.5-9B (0.30 / 0.807 / 1.463) and Qwen3.6-35B-A3B (sample 1.335, train 1.177) | Confirmed in `models.json` today. Qwen3.5-9B is a hybrid model, so thinking can be switched off. |
| OpenRouter Haiku 5.5 at $0.10 / $0.50 and Sonnet 5.5 at $2 / $10 | Confirmed. |
| arXiv 2606.12016 shows "self-inoculation" preventing generalisation under RL | Confirmed (Xiao and Phuong, June 2026, Qwen3-235B). |
| "Follow-ups found: none" | Not contradicted, but only partly checked. The WebSearch budget for this session was exhausted, so I could not run a web search. I checked the arXiv API ("reward laundering": zero hits; "exploration hacking": only Jang et al. 2604.28182), the parent post's 3 comments, and every post under the LessWrong exploration-hacking tag. The nearest items are two September 2026 Astra/MATS posts on exploration hacking in debate (40 karma each), which are about sandbagging, not laundering a propensity. |

One thing the proposal understates: the repo's rollout engine is a subset-sum-specific forced flow (search, verify, `Subset:`, `Solved:`, `Answer:` cues, each with its own token budget and loss masking). "Reused" really means the GRPO loop, reward wiring, the D permutation and the leakage metric. The rollout, parsers, prompts, pools and eval builder are all rewritten. That is a day-one job, not a config change.

## 1. Would it get upvoted?

Possibly, but it is not a safe bet. The parent got 82 karma with Redwood authors, a new named concept and only 3 comments. A follow-up from an unknown team on the same 9B model inherits less attention.

- If the result is "propensities launder" on lottery choices: I expect 25-50 karma. The obvious reader reaction is "you rewarded rollouts where it picked the gamble, so it picks the gamble more; that is just RL". In the skill case the surprise was a capability gain with no direct reward. For a choice the default expectation is already that it transfers, especially after the behaviour-compatible-training post showed transfer across small prompt shifts is common.
- If the result is "the visible rule inoculates": more surprising, connects to inoculation prompting and 2606.12016, and could clear 50. I think this is the less likely outcome.
- What would lift either result: a propensity people care about (not lottery risk appetite), far-transfer evidence that it is a disposition and not a response bias, and the literal version of the authors' question, where the prompt tells the model it is laundering in order to acquire the trait.

Who cares: the parent authors, the exploration-hacking group, and the inoculation-prompting people. That is a small audience.

## 2. Naturalness

Mainline. It is one of four follow-ups the authors list, and I found no one who has done it. Two caveats:

- The proposal's condition B is not quite the authors' question. They ask: "If we prompt them to reward launder *in order to learn a propensity*, do they keep those propensities despite the inoculation prompting?" The proposal's B says "make whichever choice you prefer" and never names a target or a purpose. That removes most of the inoculation, because the prompt gives the model no explanation for choosing the gamble. The design then tests a weaker and more predictable thing.
- From the gradient's point of view, B with a well-obeyed rule is direct reward on the choice, delivered in a different prompt, plus leakage noise. So the real independent variable is the training prompt's content, not the reward route. The design should be built around that.

## 3. Pre-mortem

How I expect the two days to go:

1. Day 1 morning: tests pass; the team finds the rollout flow must be rewritten for a two-line output (choice, then answer). Doable.
2. Pilot: the base rate of the target choice is tuned on the neutral prompt. Under the B prompt it will be different. A model that "wants" to answer an addition correctly, told it may only do so if it picked the gamble, will read the rule as a hint and pick the gamble far more often. If the step-0 target rate under B is above ~85%, almost every rollout earns reward, within-group reward variance vanishes, and GRPO has nothing to learn from. This is the same degeneracy the README documents for condition A.
3. If the base rate under B is off ceiling, the choice (one early token) saturates within a handful of steps on the training prompt. The 6-step eval grid will miss the dynamics.
4. C-inoc is degenerate by construction. With "choose [target]" in the prompt the base model complies near 100%, so reward is constant and nothing trains. C-inoc will show zero transfer because it did not train, not because the instruction inoculated. The transfer fraction (B − C-inoc) / (C − C-inoc) then has a meaningless zero point, and "matched training-prompt target rates" cannot be met because C-inoc starts at the ceiling.
5. C trains on the exact neutral eval prompt and hits ~100%. B lands somewhere between, with seed spread. With 3 seeds and a finicky transfer phenomenon, the transfer fraction will have wide intervals.
6. Far transfer and self-report move little for every condition, C included, after 30 steps on forced-choice lotteries. The write-up can then only claim a shift in a narrow choice format.

Rough outcome probabilities:

| Outcome | Probability |
|---|---|
| Clear positive (B transfers on neutral prompts, fraction above 0.5, beats D every seed) | 40% |
| Clear negative that is still interesting (B saturates in training, no neutral transfer) | 10% |
| Ambiguous mush (ceiling at step 0, degenerate reference arm, noisy fraction, response-bias doubts) | 40% |
| Fails to run | 10% |

Specific failure reasons, most important first:

- **Degenerate reference arm (C-inoc)**, as above. This breaks the key analysis as written.
- **Demand effect of the rule on the step-0 choice rate in B.** Not measured in the plan; base rates are tuned without saying under which prompt.
- **Response-bias confound.** The proposal does not say option order and labels are counterbalanced. Without that, "choose the gamble" can be learned as "choose option B" or "choose the longer option", and the neutral eval would still show a rise.
- **Narrow trait.** The primary metric is the same item family and format as training. A reader will not accept that as a "propensity" unless held-out families and free-text behaviour move. These are listed as secondary; they are what the claim rests on.
- **Leak route is easier than the choice route.** Reward can be raised by choosing the target or by answering correctly regardless. In the original, annealing kept leakage near 0.09 for 30 steps, but there the alternative (getting better at subset-sum) was slow. Here both routes are fast. If the rule is obeyed only 90% at step 0, expect leakage to grow in some seeds. This is manageable, but the 90% bar should be on the non-target branch specifically.
- **D is not a clean placebo.** In the original, shuffled reward drove the skill below base (0.14 vs 0.37). For a choice it will produce drift of unknown sign. It controls for exposure, not for prompt content.
- **Unsurprising either way.** Covered in section 1.

Under-elicitation and model availability are not a concern here. Infrastructure risk is moderate and mostly the rollout rewrite.

## 4. Cost check

The estimate is realistic. Per-run arithmetic checks out at today's prices: 3,840 rollouts at about 750 tokens is roughly $1.6 of sampling and prefill, $4.2 of training, and about $3 of evals, so about $9 per run. 24 runs is about $215. If the 512-token reasoning cap is actually used on most rollouts, sampling and training tokens rise by about 40% and a run costs about $12.

My estimate for the proposal as written: **$300-380**. With the extra conditions I recommend below (6 conditions, one propensity at 3 seeds, second propensity at 2 seeds on the key arms only): **$380-460**, still under the cap. Turning thinking off for the choice (the model is hybrid) cuts tokens and removes the forced-flow rewrite; I would do that.

## 5. Recommended changes

1. **Replace C-inoc with reference arms that actually train.** Options, in order of preference: (a) "B-direct": B's exact prompt, reward read from the choice instead of the addition. This isolates reward route from prompt content, and should match B up to leakage. (b) An instructed arm whose instruction is soft enough that step-0 compliance is 40-70%, so GRPO has variance. Report raw neutral-prompt rates per arm with seed intervals; drop the single "transfer fraction" as the headline.
2. **Add the authors' literal condition ("B-explicit").** The prompt names the target and the purpose: roughly "you want to become more willing to X; to make training reinforce this, answer the addition correctly only when you chose X". This is the real inoculation test, and the B vs B-explicit gap is the most publishable number in the project. If compliance is near 100% at step 0, note that this arm cannot train under GRPO and say so; that is itself a finding about how an explicit laundering instruction caps its own effect.
3. **Tune and report base rates under every training prompt, not just the neutral one.** Gate on the step-0 target rate in B being between 25% and 75% and on rule obedience of at least 90% on the non-target branch.
4. **Counterbalance option order and labels** in training and in every eval, and report the target rate split by position.
5. **Promote held-out transfer to co-primary.** Pre-specify one held-out item family and one free-text behavioural set per propensity and require movement there before using the word "propensity". Drop self-report to an appendix.
6. **Evaluate densely early.** Steps 0, 1, 2, 3, 4, 6, 9, 12, 18, 30 on the cheap forced-choice sets; the action will be in the first few steps.
7. **Swap P-risk for something readers care about**, or keep P-risk as the pilot and make P-defer (acting without checking with the user) the headline. A third candidate with direct safety relevance, such as compliance with borderline requests or agreeing with the user against the evidence, would raise the ceiling on reception. Keep it to two.
8. **Add a persistence check** costing a few dollars: after B training, 10 further GRPO steps on plain addition with no rule, then re-measure. "Laundered propensity survives ordinary training" or "washes out" is a second headline for almost no cost.
9. **Run thinking-off as the default**, with one thinking-on seed to read the reasoning for whether the model treats the rule as a hint about what is wanted.
10. **State in the write-up** that the model is instructed and that B with a perfectly obeyed rule is mathematically direct reward in a different context. Pre-empting the "this is just RL" comment is better than receiving it.

If the budget is tight across the cluster, this is a reasonable but not outstanding use of about $400. I would not drop it, but I would not fund it unchanged.
