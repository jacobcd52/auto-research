# Feedback: 03-probe-credit-assignment

**Verdict: major overhaul.** The headline comparison (RL-on-probe vs gradient-through-probe, same task and probe, on an LLM) is already Figure 4 of The Obfuscation Atlas, and most of the "theorem test" arms are identical to the control by arithmetic rather than by experiment. One part survives: where the probe penalty is credited on multi-token outputs, and past- vs future-looking probes. Rebuild around that or drop; as written this is the weakest of the cluster's three.

What I checked, and what I could not:

- Read in full: Steiner's post, its comments and the sequel; the Atlas HTML (arXiv 2602.15515), Sections 5.3 and Appendix D; abstracts of arXiv 2510.21531 and 2506.14261.
- Confirmed public: `Qwen/Qwen3-4B-Instruct-2507` and `google/gemma-2-2b-it` (HF API 200), Geometry of Truth data (raw GitHub 200), Aether's repo (raw 200).
- Confirmed price: gemini-2.5-flash-lite at $0.10/$0.40 per 1M on OpenRouter today.
- **Not done: a web search for prior work.** The session's search budget was exhausted before my first query. "Has anyone done this" rests on the proposer's single search plus my reading of the primary sources.
- Not re-checked: RunPod GPU prices (the proposal's L40S figure comes from NOTES and is unverified by me), and the Yeung & Ramaswamy workshop paper.

## 1. Would it get upvoted?

Probably not past 50 as written. I would guess 20–40 karma.

- **The parent post is not a high-engagement one.** Steiner's post has 73 karma and 2 comments; the research-ideas sequel has 32 karma and 3 comments. The other cluster posts sit at 56–130.
- **The modal outcome is a confirmation of a three-line proof.** Readers who accept the policy-gradient theorem learn nothing; readers who do not will not be persuaded by a Yes/No toy.
- **The "one probe, three uses, three outcomes" figure is not new.** Atlas Fig. 4 shows RL against the detector gives no more representation change than plain RL, while passing gradients through the detector gives substantially more. That is on MBPP-Honeypot, across three probes and multiple seeds, on 8B–70B models. A Geometry-of-Truth toy on a 4B model reads as a weaker replication.
- **Who would care:** Steiner, the FAR authors, Aether, and a handful of people designing probe rewards. They would care about the credit-placement and past/future-looking results, not the R-pre equivalence.

## 2. Naturalness

A test of the theorem is the obvious follow-up to Steiner's post in the abstract, and the screener suggested it. But the proposal's novelty claims are wrong in three places.

- **"None of this has been tested on a language model" is false.** So is "shown only in the author's toy model" for claim 1, and "none putting gradient-through-probe and RL-on-probe side by side on one task with one probe". Atlas Section 5.3 and Fig. 4 do exactly this with "direct gradients" runs (Appendix D, eq. 10). Steiner's post displays the Atlas result and says Appendix D "mostly scoops" his maths. NOTES rejected idea J as "mostly done by the Atlas", then merged it back in as this proposal's headline.
- **The estimator question is already addressed in Atlas Appendix D.** It covers the GRPO baseline and std normalisation, concluding that normalisation changes the scale of the update and not its direction.
- **The "theorem leaks" outcome is known RL.** An action-independent reward offset under baseline-free REINFORCE changes finite-sample dynamics while leaving the expected gradient untouched. From memory, this is Chung et al., ICML 2021, "Beyond variance reduction: understanding the true impact of baselines on policy optimization" (not re-fetched today). Finding it here would be a rediscovery in a regime nobody uses for LLM RL.

What is still open, as far as I can tell:

- Credit placement of a per-token probe penalty on multi-token outputs.
- Steiner's past-looking vs future-looking design hint (his Fig. 3).
- A head-to-head of live-policy vs frozen-base probe activations as the RL reward. The Atlas uses live activations; Aether uses frozen base.

These are real but they are a side branch of the cluster. The mainline is held-out monitor degradation, which proposal 01 addresses.

## 3. Pre-mortem

**Format A (one-token answers) contains almost no experiment.**

- **R-pre (ii) and (iii) equal C0 exactly.** The pre-answer probe score is identical for every sample in a prompt group, so a per-prompt baseline subtracts it to zero, per sample, on frozen and live activations alike. Four of the six R-pre variants will reproduce C0 to floating-point error. Passing an "equivalence test" there shows the code is deterministic.
- **R-pre (i) is C0 plus a state-dependent offset and no baseline.** It will show extra variance and possibly the known offset effect. Either way it concerns an estimator no LLM RL recipe uses.
- **R-post with one-token answers on a frozen base is a black-box classifier.** The probe is a deterministic function of (prompt, Yes/No). With λ set so honesty is optimal, the model learns honesty; one token leaves no room for obfuscated text. The outcome is known in advance.
- **G reproduces the Atlas green bars**, with one twist the plan does not handle. A frozen linear probe can be defeated by shifting all activations along the probe direction, which leaves AUROC (rank-based) at about 1.0 while fixed-threshold recall goes to zero. The plan tracks AUROC only, so G could look like "the probe survives".
- **The "pre-answer lie probe" is a truth-of-claim probe.** At the last prompt token it reads whether the user's claim is false, which is what Geometry of Truth probes detect. RL towards "always agree" need not disturb that representation, so probe AUROC will stay flat in every RL arm. That says little about lie detectors.

**Format B has one real contrast, not four.**

- Schemes (a) whole reply and (b) tokens up to t have the same expected gradient. Tokens after t cannot affect the reading at t, so (b) is reward-to-go variance reduction.
- Scheme (c) is the null by construction.
- The only real comparison is full causal credit (a/b) against myopic credit (d).
- Thirty-token confirmations of a factual claim give little room for it to matter: the lie is in the first token or two. Expect (a), (b) and (d) to all reach honesty or all reach "Yes, …" with hedging, within seed noise at n=3.

**Execution risks.**

- **Wall-clock.** The plan says 70 GPU-hours on "one rented 48 GB GPU", doubled for reruns. Two days is 48 hours. It needs 3–4 GPUs in parallel from the start. Cost is unchanged but the plan as stated does not fit.
- **Custom RL loop from scratch.** A live-activation probe rules out Tinker and Aether's code. The agents must write their own REINFORCE/GRPO, per-token advantages, activation hooks and gradient-through-probe path. That is feasible, but it is where the time goes, and token-to-activation off-by-one is the whole content of the credit arms. The proposal acknowledges this; the synthetic unit test is good.
- **λ tuning.** One-token RL either collapses to always-Yes within tens of updates or does not move. "Honest policy is optimal when the penalty is perfectly informative" still leaves a wide range, and outcomes in G and R-post will depend on λ more than on the arm.
- **Format B labels.** String rules plus a cheap judge on 30-token replies will be noisy exactly on the evasive cases that matter.

**Forecast.**

| Outcome | Probability |
|---|---|
| Surprising or design-relevant result (credit scheme matters; a leak in a recipe people use) | ~10% |
| Clean confirmation: theorem holds, G obfuscates, R-post goes honest | ~50% |
| Ambiguous mush (seed variance, λ sensitivity, Format B arms indistinguishable) | ~25% |
| Does not finish Format B or infra bugs invalidate the credit arms | ~15% |

The 50% case is the predictable one and adds little to the Atlas.

## 4. Cost check

The $150 figure is about right; I estimate $100–200.

- One-token rollouts on a 4B model at batch 256 × 300 updates take minutes, not half an hour, so Format A is over-budgeted.
- Format B plus debugging dominates.
- The judge spend is negligible at the verified gemini-2.5-flash-lite price.
- Cost is not the problem; information per dollar is.

## 5. Recommended changes

1. **Correct Section 1.** State that the Atlas already ran RL vs direct gradients on LLMs (Fig. 4) and analysed GRPO normalisation (Appendix D). Remove "none of this has been tested on a language model" and the side-by-side novelty claim.
2. **Cut the R-pre grid to a sanity check.** Keep C0, R-pre with plain REINFORCE, and one grouped variant, at an hour of compute and one paragraph in the write-up. State up front that the grouped variants are identical by construction. Drop the equivalence-test framing.
3. **Make the headline past- vs future-looking probes and credit placement.** This needs a task where the lie comes late in a longer reply, so that earlier tokens steer towards it:
   - Use replies of about 150 tokens where the model first reasons or sets up and then commits, or reuse MBPP-Honeypot text with a base-model per-token probe.
   - Train two probes on the same data: one that reads the tokens after the lie (past-looking) and one that reads the tokens before it (future-looking).
   - Run each under full causal credit and myopic credit.
   - Measure honesty, evasive-text rate, and base-model probe recall at a fixed threshold.
   - Steiner's Fig. 3 prediction (the future-looking probe can only train the lead-up) is then testable and untested, and it yields design advice.
4. **Add the live vs frozen-base activation comparison in that multi-token setting.** It is a real difference between the Atlas and Aether setups and has not been compared directly, as far as I found.
5. **Keep G as a reference arm only.** Report fixed-threshold recall and mean score shift alongside AUROC, and the retrained-probe AUROC.
6. **Use at least 5 seeds on the two or three decisive arms.** Pay for it by deleting Format A variants. Plan for 3–4 GPUs in parallel.
7. **Name the probe honestly.** A last-prompt-token probe on these prompts is a claim-truth probe. Either call it that or train it on forced-lie vs forced-honest continuations at a position after the answer begins.
8. **Funding order.** If the cluster can fund only two proposals, fund 01 and 02 ahead of this one. If the overhaul in items 3–4 is not made, drop it: the unrevised version mostly replicates a published figure on a weaker task.
