# Is it really belief propagation? Dissociating loopy BP, exact inference and enumeration in Astra's no-CoT logic solving
cluster: cot-nocot-capability | stage-1 cost: $220 | follows up: "Astra appears to perform belief-propagation-like inference without CoT" (PAHqDoFrp9fybcSn2); "Astra's no-CoT limits track speculative depth, not step count" (WFc3NkuPaYFrYuaZd)

## 1. What the prior work showed
- MBaert gave GPT-6 Astra randomised Boolean problems equivalent to decoding a 2-error-correcting BCH code: a noisy assignment ("exactly 2 of these are incorrect") plus xor constraints, answer immediately with the full assignment, no chain of thought. Astra solves instances with 10+ variables given a few hundred filler tokens; GPT-5.6 Sol manages about 4 variables. GPT-6.1 Sol also benefits from filler.
- In a "soft" version (each variable has a stated prior, find the most likely assignment), Astra's success correlates strongly with how close the exact posterior marginals are to the MAP assignment, and invalid answers rise when the top two solutions are close. This suggests it computes approximate marginals and thresholds them.
- Using prompt caching, he re-queried the same prefix with more and more filler and asked for per-variable confidence. The reports oscillate and then converge to values close to the exact marginals (brute-forced). He notes the trajectories are "quite different from textbook belief propagation" and that he has reached the limit of what he can learn black-box.
- Not done: the post never runs belief propagation (BP) on the same instances. Loopy BP on small dense parity-check graphs is frequently wrong or non-convergent, which makes the hypothesis testable: a BP-like process should inherit BP's instance-specific failures. No follow-up post has done this (checked LessWrong through 2026-11-14).

## 2. Question and why it matters
On instances where loopy BP, exact marginal inference and solution enumeration make different predictions, which one does Astra's no-CoT behaviour follow?

- If Astra's answers and confidences track loopy BP's beliefs, including on instances where BP is wrong, that is unusually specific black-box evidence about an algorithm running inside a forward pass, and it predicts where hidden inference fails (short cycles, weak priors).
- If Astra is right where BP is wrong and tracks exact marginals, the "BP-like" label is misleading and something closer to exact parallel inference is happening, which is a stronger capability claim.
- If accuracy depends on the number of valid solutions rather than graph structure, the mechanism is closer to parallel enumeration (the "width" story for filler).

## 3. Stage 1 plan
Reused: the task formats and prompts quoted in MBaert's post (hard "exactly k incorrect" and soft-prior BCH tasks; the confidence-report prompt; the cached-prefix trajectory method) and his generator if it is in github.com/MaartenBaert/LatentMathBench. Built: instance generator with reference solvers (about 300 lines): brute-force exact marginals and MAP; sum-product loopy BP (flooding schedule, damping 0 and 0.5, up to 100 iterations); min-sum; Gallager bit-flipping; a one-step local heuristic (prior adjusted by directly attached constraints only).

Models: GPT-6 Astra (main), GPT-6.1 Sol (cheap replication, also filler-sensitive), GPT-5.6 Sol at small sizes as a non-looped contrast.

Instance sets (soft-prior task, 7–13 variables):
- Set D (disagreement): instances where thresholded converged-BP beliefs differ from the exact MAP in at least one variable, or BP oscillates, while the exact answer is well separated (top solution at least 4x the runner-up, as in the original). Matched Set A (agreement) instances with the same number of variables, constraint density and MAP margin where BP is correct. 300 of each.
- Set T (trees versus cycles): parity constraints whose factor graph is a tree (BP exact) with controlled diameter 2–10, and cyclic graphs matched on size. Tests whether filler needed grows with the number of message-passing rounds BP needs.
- Set E (enumeration): fixed number of variables and BP difficulty, number of valid assignments varied from 2 to 2,048 by removing constraints.

Conditions: filler N in {0, 100, 300, 1000, 3000} dots after the question; 2 samples per item at each N. Confidence reports collected on Sets D and A at the largest N, and cached-prefix trajectories on 40 instances.

Steps:
1. Build solvers and validate them against each other on trees (BP must equal brute force).
2. Replicate two headline numbers from the post (accuracy versus variables with 300 dots; success versus marginal/MAP gap) as a gate.
3. Run Sets D/A, T, E.
4. Analyses:
   - Double dissociation: on Set D, fraction of Astra answers matching (i) exact MAP, (ii) BP's thresholded beliefs, (iii) neither, per variable and per instance, compared with Set A.
   - Regression of Astra's reported per-variable probability on exact marginal, BP belief, min-sum belief and local heuristic (restricted to variables where they differ by more than 0.15).
   - Filler-to-converge: smallest N at which Astra is correct versus BP iterations to convergence and versus tree diameter, controlling for variable count.
   - Set E: accuracy versus log number of solutions at fixed N.
   - Trajectories: compare the order in which variables settle with the order in BP (rank correlation), not just the end state.

Controls: variable-name and constraint-order shuffles; zero reasoning tokens on every response; a "priors only" condition to measure baseline probability reporting.

## 4. Stage 1 cost estimate
OpenRouter prices looked up 2026-11-14 (per 1M tokens): Astra $10 input, $1 cached input, $50 output; GPT-6.1 Sol $2 / $10; GPT-5.6 Sol $4 / $20.
- Main runs on Astra: (600 + 300 + 300) instances x 5 N x 2 samples = 12,000 calls x ~1.2k input tokens = 14.4M tokens: $144 uncached; using a cached prefix for the question and extending filler brings repeated-prefix tokens to $1/M, estimated $70. Outputs (~40 tokens with confidences): 0.5M tokens: $25.
- GPT-6.1 Sol same grid: 14.4M x $2 = $29 + outputs $5.
- GPT-5.6 Sol small sizes: $10.
- Trajectories: 40 instances x 30 filler steps on Astra, cached: $10.
- Subtotal ~$150; x1.45 for the replication gate, prompt iteration and reruns: $220.
(Solver development and instance generation are CPU-only.)

## 5. What success looks like
- A bar chart for Set D: share of Astra's answers equal to exact MAP versus BP's (wrong) answer versus neither, with Set A alongside. A clear result is either at least 60% matching BP's wrong answer (BP-like, inherits BP failures) or at least 70% matching exact MAP with no accuracy penalty relative to Set A (not BP).
- Regression coefficients on disagreement variables: one predictor dominating (standardised weight more than twice the others).
- Set T: required filler rising with tree diameter (iterative propagation) or flat (parallel).
- Set E: accuracy flat in number of solutions (not enumeration) or falling steeply (enumeration).
Ambiguous outcome: Astra matches neither on Set D and confidences are too noisy to regress; a reportable negative but less likely to be widely read.

## 6. Stage 2 (if stage 1 succeeds)
- If BP-like: test transfer to non-Boolean inference with the same structure (small Bayesian networks in natural language, e.g. "who is lying" puzzles and evidence-weighing scenarios relevant to monitors and eval-awareness judgements) and check whether the same structural failure predictors hold (~$600).
- If exact-like or enumeration-like: scale variables and solution counts to find the capacity limit and its dependence on filler; compare with GPT-6.1 Sol and Gemini 4 Argon (~$400).
- White-box analogue on an open looped model (Dory 4B or Ouro 2.6B, LoRA-tuned on these tasks if needed): probe per-loop beliefs against BP iterations (~$500 GPU).

## 7. Risks and how the plan handles them
- Too few clean disagreement instances at sizes Astra can solve. Mitigation: generation is free; short BCH codes have many short cycles so BP failures are common; if needed, weaken priors or add redundant constraints to induce failures while keeping the exact answer well separated.
- "Converged BP" is schedule-dependent, so the BP prediction is not unique. Mitigation: use a small family (flooding, damped, min-sum) and report matches to any member; Set D requires all members to disagree with exact MAP.
- Verbal confidence is a noisy readout. Mitigation: the primary dissociation uses the answered assignment, not confidences; confidences are secondary.
- Astra is at chance on Set D. Mitigation: choose sizes where Set A accuracy is 60–90%; selective failure where BP fails is itself informative against matched Set A.
- Original result does not replicate via OpenRouter (caching, model updates). Mitigation: step-2 gate; core runs do not need caching.
- Narrow audience. Mitigation: short post led by the single dissociation figure and what it implies about where hidden inference breaks.
