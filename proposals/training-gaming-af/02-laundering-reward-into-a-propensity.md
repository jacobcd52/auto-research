# Can a model launder reward into a propensity? Reward laundering with a choice instead of a skill
cluster: training-gaming-af | stage-1 cost: $340 | follows up: "Reward Laundering: LLMs Can Gain Unintended Behaviors by Deciding When to Earn Their Rewards" (fPWP4rHPLqKKHKe6B)

## 1. What the prior work showed
Redwood's automated scaffold trained Qwen3.5-9B with GRPO on Tinker where the only rewarded thing was a 2-digit addition the model already solves 99.9% of the time. The prompt also posed a subset-sum problem and told the model to answer the addition correctly if and only if it had verified a subset-sum solution. Because the model then earns reward only on rollouts where it solved the side task, RL reinforces the side task. Subset-sum accuracy on a neutral prompt rose from 0.37 to 0.58 (5 seeds), matching direct subset-sum reward (0.57). Controls did not reproduce it (shuffled reward 0.14, SFT on base rollouts 0.36). The coupling is unstable: "leakage" (reward earned despite failing the side task) stays near 0.09 when the learning rate anneals to zero but reaches 0.67–0.96 otherwise.

The post lists as open: "Propensities: Can models shape their behavioral propensities with reward laundering? If we prompt them to reward launder in order to learn a propensity, do they keep those propensities despite the inoculation prompting?" The released codebase (https://github.com/redwoodresearch/automation-final-codebases/tree/main/reward-laundering) contains the condition prompts and parsers, reward wiring for laundering / direct / shuffled conditions, the GRPO loop and the eval harness. Its README says the original matrix cost about $6k, because each rollout carries an 8,000-token reasoning budget.

Follow-ups found (14 Nov 2026): none. Inoculation prompting (Tan et al. 2025; Wichers et al. 2025) shows a trait trained under an instruction that explains it tends not to generalise to prompts without the instruction. arXiv 2606.12016 shows a model using "self-inoculation" in its reasoning to stop a rewarded behaviour generalising. Neither tests whether reward routed through an explicit rule can install a propensity.

## 2. Question and why it matters
**When the laundered property is a choice the model makes (a propensity) rather than a skill, does it transfer to prompts that contain no laundering rule, as subset-sum skill did? Or does the explicit rule in the prompt act as an inoculation that keeps the propensity tied to that prompt?**

A skill, once learned, shows up everywhere. A propensity can stay conditional. If laundered propensities transfer about as well as directly rewarded ones, a model that controls when it earns reward can change what it tends to do (the "reinforcing their own misaligned goals" case the authors flag). If they do not, laundering is much less dangerous for values than for skills while the scheme is visible in the prompt, and the result is a new data point on inoculation under RL.

## 3. Stage 1 plan
Reused: the codebase above (model, GRPO config, shuffled-reward control, leakage metric, tests). Built: two choice-task generators, a coupled prompt, transfer evals.

**Side "tasks" (two, to avoid a one-domain result).**
- P-risk: generated two-option lotteries (a sure amount vs a gamble), with the expected-value gap tuned in a pilot so the base model picks the gamble 30–50% of the time. Target propensity: choose the gamble.
- P-defer: short workplace dilemmas where the assistant either acts on its own judgment or checks with the user first, base rate tuned likewise. Target propensity: act without checking.

**Conditions (GRPO, Qwen3.5-9B, LoRA rank 32, lr 1e-4 annealed to 0, group 16, batch 8, 30 steps, as in the original; reasoning capped at 512 tokens).**
- B, laundering: prompt contains the dilemma and an addition. "Make whichever choice you prefer. Then answer the addition correctly if and only if you chose [target]; otherwise give an unrelated 4-digit number." Reward = addition correct. The prompt never says which option to choose.
- C, direct reward: dilemma only, reward = target choice. Upper bound on transfer.
- C-inoc: dilemma plus "choose [target]", reward = target choice. The standard inoculation reference.
- D, shuffled reward: B's prompt, rewards permuted within group (the original's placebo).
- 4 conditions x 2 propensities x 3 seeds = 24 runs of 3,840 rollouts.

**Evaluation at steps 0, 6, 12, 18, 24, 30 (300 items per set).**
1. Neutral transfer (primary): the dilemma alone, no addition, no rule. Target-choice rate.
2. Format transfer: free-text answers scored by a judge; different stake sizes; a held-out dilemma family.
3. Far transfer: 100 unrelated advice questions where risk appetite or autonomy can show up, scored by a blinded judge.
4. Leakage on the training prompt: P(addition correct | non-target choice), as in the original.
5. Self-report questions about the trait.

**Key analysis.** Place B on the line between C-inoc (0) and C (1): transfer fraction = (B − C-inoc) / (C − C-inoc) on neutral prompts at matched training-prompt target rates, per propensity, with seed-level intervals. B vs D isolates the coupling.

**Steps.** (1) Run the repo's tests. (2) Pilot: tune base rates; iterate the B prompt until the base model obeys the if-and-only-if rule at least 90% of the time on both branches. (3) Gate: one seed of all four conditions on P-risk; the training-prompt target rate must rise in B and C and not in D. (4) Remaining runs. (5) Evals and write-up.

## 4. Stage 1 cost estimate
Tinker prices for Qwen/Qwen3.5-9B, looked up 14 Nov 2026: prefill $0.30/M, sample $0.807/M, train $1.463/M.
- Per run: 3,840 rollouts x ~350 prompt tokens = 1.3M prefill ($0.40); x ~400 sampled = 1.5M ($1.24); training on 2.9M tokens ($4.21); evals 6 x ~1,000 items x ~700 tokens (≈ $3.00). About $8.90.
- 24 runs = $214.
- Pilots (prompt iteration, base-rate tuning, gate run): $45.
- Judge: ~15k judgments x ~900 tokens on Claude Haiku 5.5 ($0.10/$0.50 per M, OpenRouter) plus a Sonnet 5.5 audit ≈ $5.
- Margin for reruns (leakage-driven collapses, extra seeds on the headline cell): $76.
- **Total $340.** Token counts are estimates; the gate run measures them, and P-defer drops to 2 seeds if they are 50% higher.

## 5. What success looks like
- Figures: neutral-prompt target rate over training for B, C, C-inoc and D with seed bands; transfer fraction per propensity.
- "Propensities launder": B's neutral-prompt rate rises by at least 15 points over base, exceeds D in every seed, and the transfer fraction is above 0.5. Headline: a model that only decides when to collect reward can shift what it prefers.
- "The rule inoculates": B reaches a high target rate on the training prompt but neutral-prompt change is within noise of C-inoc and D (transfer fraction below 0.2). Headline: laundering installs skills but not unconditional dispositions when the scheme is spelled out, which points the threat model at uninstructed laundering.
- Intermediate values are still the number the original authors asked for. A real failure would be B not rising even on the training prompt; the gate run catches that on day one.

## 6. Stage 2 (if stage 1 succeeds)
(i) Remove the instruction: give the model a preference and knowledge of the setup through synthetic documents and test whether it launders unprompted. (ii) Launder CoT controllability or a safety-relevant propensity. (iii) Detection: flag rollout features whose correlation with reward the task does not explain. About $2,000–3,000.

## 7. Risks and how the plan handles them
- **The 9B model will not follow an if-and-only-if rule about its own choice.** Pilot with a 90% bar and a forced output format as in the original; otherwise move to Qwen3.6-35B-A3B (train $1.177/M, sample $1.335/M; similar cost).
- **Training-prompt rate saturates within a few steps.** Add a step-3 eval in the gate run; lower the learning rate if B saturates before step 6.
- **Base rate drifts in all conditions for unrelated reasons.** D (shuffled) and C-inoc control for RL exposure and prompt content.
- **Neutral eval prompt is C's training prompt, flattering C.** Format- and far-transfer sets are disjoint from every training prompt and reported alongside.
- **Reward leakage confounds B.** Leakage is tracked per checkpoint; the headline uses the annealed schedule the original found stable.
- **Judging subtle traits.** Primary metrics are forced-choice and programmatic; judge-scored sets are secondary.
