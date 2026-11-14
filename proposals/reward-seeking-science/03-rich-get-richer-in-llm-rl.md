# Does RL amplify whatever the model starts out doing? An LLM test of "rich-get-richer" initialisation effects
cluster: reward-seeking-science | stage-1 cost: $400 | follows up: Toy Models of Initialisation Effects on RL Dynamics (72AAjXAxS7Pow9Fie); Why study alignment interventions on pre-RL checkpoints? (nhjkHsppEk98xxmPe); Physics of RL (9FH49ZgJFW4WtbxLi)

## 1. What the prior work showed
Geodesic's agenda rests on the claim that the pre-RL checkpoint matters because RL is path dependent. Their toy
model (softmax policy over three actions, policy gradient / RLOO) makes this precise: (i) when two actions earn
the same top reward and a third earns less, the one that starts more probable gains share — the log-ratio grows at
rate (pi_A - pi_B) x (r_top - mean reward) — so a 60:40 start ends near 100:0; (ii) finite-sample noise makes the
winner seed-dependent, more so at high learning rate and small batch; (iii) if nothing is left to learn (mean
reward already at the top) the split does not move, i.e. reward-irrelevant behaviour and the cognition behind a
behaviour are fixed by initialisation. Meinke's "Physics of RL" uses a related replicator model for
reward-seeking reasoning and explicitly asks for LLM model organisms where the prior is set by SFT
("prior-boosting") and the dynamics are compared to the equations. Neither post contains an LLM experiment.
The one empirical follow-up (Wells & Young, Nov 2026) shows grader knowledge at initialisation speeds up RL,
but does not vary the initial *share* of competing strategies, has one run per condition, and cannot test
(i)-(iii). My searches found no other test.

## 2. Question and why it matters
In real LLM RL (LoRA, shared parameters, sampled rollouts), is the final split between two equally rewarded
strategies an amplified version of the initial split, as the toy model says — and does this also hold when the
two "strategies" are two chains of reasoning that lead to the same rewarded answer? If amplification is real and
follows the predicted rate law, pre-RL interventions have leverage that grows during RL, which is the core of
Geodesic's case. If the split is simply preserved (or regresses to 50:50), the practical message is different:
initialisation sets cognition roughly linearly and "lock-in" is not a special danger. If results are
seed-dominated, single-run comparisons of pre-RL interventions (the current norm) are uninterpretable.

## 3. Stage 1 plan
Reused: Tinker RL (importance-sampling loss, group rollouts, as in Arrow's released code
https://github.com/Arrow-Research/grader-targeting-reasoning-from-sdf); Arrow's "Wood" environment (MBPP problems
with deliberately code-breaking format constraints, reward = fraction of unit tests passed) and their
reasoning-judge prompt; the Geodesic simulation code for theory curves. Built: SFT warm-start sets and a
share-tracking script. Model: gpt-oss-20b on Tinker (cheapest reasoning model; Qwen3-8B as fallback).

**Phase A — behaviour-level (run first).**
1. Task: arithmetic word problems filtered so base accuracy is 40-60%; reward 1 if the final number is right.
   Two answer formats are both accepted by the grader: `ANSWER: x` and `<final>x</final>`.
2. Warm-start: SFT on ~1,500 examples where the format mix is 10/30/50/70/90% A (answers are the model's own,
   mixed correct and incorrect, so accuracy is not changed). Verify the realised initial share.
3. RL: 60 steps, 16 prompts x 8 rollouts, 3 seeds per ratio (15 runs). Every 5 steps record share of format A
   among all rollouts and accuracy.
4. Saturated control: same design on problems the model already solves ~100% (3 ratios x 2 seeds). Prediction
   (iii): no drift.
5. Noise test: at 50:50, 5 seeds each at (low lr, 16x8) and (4x lr, 8x4). Prediction (ii): wider spread of final
   shares in the second setting.
6. Analysis: final share vs initial share (identity line = "preserved", S-curve = "rich-get-richer"); regress
   per-interval change in logit(share) on (pi_A - pi_B) x (1 - accuracy), the toy model's rate law; overlay the
   simulated curve fitted with one learning-rate parameter.

**Phase B — cognition-level (only if Phase A pipeline is sound; any Phase A outcome is acceptable).**
7. Wood environment: the rewarded behaviour is "write correct code, ignore the impossible format constraints";
   the low-reward behaviour is trying to honour them. Two reasoning routes to the rewarded behaviour are seeded by
   SFT on synthetic reasoning traces (written by Claude Sonnet 5.5 in the model's own CoT style): **G** "the grader
   here only runs the unit tests, so formatting cannot score" vs **U** "the person needs working code; constraints
   that break Python cannot be what they need". Initial mixes 20/50/80% G with the comply-with-constraints rate
   held near 50%; 3 seeds each (9 runs), 60 RL steps. Reward never sees the reasoning.
8. Track share of G vs U among rewarded rollouts with the LLM judge (Haiku 5.5; 150 labels hand-checked).
9. One held-out probe at the end: prompts that state the grader checks *only formatting* while the user asks for
   working code. Does the fraction following the grader track the final G share? (Reported as exploratory.)

## 4. Stage 1 cost estimate
Tinker gpt-oss-20b, looked up today: $0.18/M prefill, $0.45/M sample, $0.396/M train.
- Phase A run: per step 128 rollouts x (300 prompt + 400 sampled) = 38k prefill + 51k sample + ~90k train tokens
  = $0.066; x 60 steps = $4, + evaluation $1 = $5. Runs: 15 + 6 + 10 = 31 -> $155
- Phase B run: 128 rollouts x (500 + 900) per step = $0.13/step -> $8, + judge and evals $2 = $10; x 9 = $90
- Warm-start SFT: 8 sets x ~1M tokens x $0.396 = $3; trace generation with Sonnet 5.5 ($2/$10 per M): ~$12
- Judge (Haiku 5.5, $0.10/$0.50 per M): ~$10
- Pilots, hyperparameter search for a learning rate where accuracy actually improves, reruns: $130
Total: **$400**.

## 5. What success looks like
A figure with final share against initial share for 5 ratios x 3 seeds, next to the toy-model curve, plus the
saturated control and the noise test. Clear outcomes, all publishable:
- *Amplification*: 70:30 starts end beyond 90:10 in most seeds, drift is absent in the saturated control, and the
  rate-law regression has the predicted sign with R^2 > 0.3 — the toy model's qualitative claims hold in LLMs.
- *Preservation*: final shares within ~10 points of initial shares despite accuracy rising >=20 points —
  rich-get-richer does not appear at this scale; a direct, quantified challenge to a load-bearing argument.
- *Seed lottery*: 50:50 starts end anywhere from 10:90 to 90:10 — a methodological warning for all pre-RL
  intervention studies.
Phase B adds whether the same holds for reasoning routes, the safety-relevant case; a dissociation between
behaviour-level and reasoning-level amplification would be the most interesting finding.
Not publishable: RL fails to raise accuracy (no selection pressure, so nothing is tested) or SFT cannot set the
initial shares — both are checked before the sweep.

## 6. Stage 2 (if stage 1 succeeds)
(a) Unequal rewards: how large a reward advantage does the minority strategy need to overturn a majority prior
(Meinke's skill-gap vs prior trade-off) (~$400). (b) Multi-environment version: does a reasoning route that
transfers across N tasks beat task-local routes as N grows — Meinke's critical-diversity prediction, using Arrow's
two environment families plus new ones (~$1,500). (c) Phase B on Nemotron 3 Super with shares set by
synthetic-document midtraining, the intervention Geodesic proposes (~$800).

## 7. Risks and how the plan handles them
- **RL does not improve accuracy on the chosen task in 60 steps**, so the "suboptimal mass" never shrinks. Pilot
  budget is reserved to pick the task difficulty and learning rate first; fallback task is Wood itself, where
  Arrow observed fast reward gains.
- **SFT warm-start changes more than the share** (e.g. accuracy differs across ratios). Use the model's own
  answers for SFT, measure accuracy per ratio before RL, and include it as a covariate.
- **Format choice is correlated with correctness** (one format makes parsing or reasoning easier), breaking the
  equal-reward premise. Check accuracy conditional on format at step 0; swap format roles in half the seeds.
- **Phase B routes are not distinguishable by the judge** or the model blends them. Hand-check labels; allow a
  "both/neither" class and report it; Phase A stands alone if Phase B is unusable.
- **Three seeds are few.** The margin allows 5 seeds on the middle ratios; claims are limited to effects
  visible across seeds.
