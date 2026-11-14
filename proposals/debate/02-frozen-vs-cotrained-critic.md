# Does debate training need self-play? Frozen versus co-trained critics in real RL, with a best-of-N forecast
cluster: debate | stage-1 cost: $460 | follows up: Debate with Self-Play Best-of-N Optimization (hb8pv3zyAHGJpwz9F); Research update: RL on Debate Games (6mLwAuFAE98c6R7w3); Debate Training Reduces Reward Hacking in RLAIF (BB8o7b8A4Aykeksvw)

## 1. What the prior work showed
Debate training rewards a proposer for solutions that survive a critic in front of a weak judge. The original
argument for debate rests on self-play: both sides are optimised. Three 2026 results disagree on whether
optimising the critic matters.

- **Arcadia (best-of-N proxy, no training).** With Sonnet 4.6 debaters and open-weight logprob judges on
  LiveCodeBench, ARC-AGI-1 and miniF2F, adding an unoptimised critic removes the proposer's overfitting to the
  judge. Optimising the critic (best-of-10) is within error of not optimising it: "Debate's benefits mostly
  reduce to optimizing against a fixed critique." The authors say the proxy cannot see cross-question effects
  and that they intend to compare it with real training runs. Code: https://github.com/ArcadiaImpact/debate-bon-public
- **GDM (real RL, Gemini 2.5 Flash-class policy).** Debate recovers 45% of the accuracy gap between judge-only
  training and ground-truth training. The paper states in one sentence, without numbers, that preliminary runs
  "using frozen API critics performed similar or worse than" the judge-only baseline, "indicating that
  co-training Bob with Alice is essential". Models, data and code are closed.
- **MATS (real RL, Qwen3-30B-A3B, Llama-3.1-8B judge, Hendrycks MATH).** Debate beats judge-only training
  ("consultancy") on one seed. The co-trained critic also learns to hack the judge. The authors list a
  static-critic baseline as the control they most want and have not run. Code:
  https://github.com/Debate-FP9/lw-progress-update-snapshot

So the proxy says a frozen critic is enough and the one training paper that tried says it is not, without
numbers. I found no published frozen-versus-co-trained comparison and no check of the proxy against RL.

## 2. Question and why it matters
**Under real RL, does a proposer trained against a frozen critic gain as much accuracy, and resist judge-hacking
as well, as one trained against a co-trained critic? And did the best-of-N proxy, computed before training,
predict the answer?**

If the frozen critic is enough, debate training gets simpler and cheaper, and the critic judge-hacking that both
RL papers struggle with disappears by construction. If the proposer learns to exploit the frozen critic, GDM's
unquantified claim gets its first public evidence and the proxy is shown to miss a training-only failure.
Either way, the field's cheap proxy gets its first calibration point against training.

## 3. Stage 1 plan
**Reused:** the MATS snapshot's RL environment, consultancy and PCD-2 prompts, judge parsing and maths grader;
MATH levels 4-5 (4,000 train, 512 test); Arcadia's analytic best-of-N estimators
(`metrics/accuracy_analytic.py`, `metrics/reducers.py`). **Built:** a frozen-critic option in the environment
and an adapter that feeds MATH debate pools to the Arcadia estimators.

Trained model: Qwen3-8B with LoRA on Tinker (the original 30B model is retired there, and the current 35B model
costs about 2.7 times as much per training token). Judge: frozen, served by OpenRouter.

1. **Calibrate the setup, inference only.** Run 500 consultancy and 500 PCD-2 debates at initialisation with
   candidate judges Llama-3.1-8B, Gemma-3-4b and Llama-3.2-3B. Pick the judge whose verdict accuracy is between
   65% and 85%, so that it is informative but exploitable. Check that proposer accuracy is between 30% and 70%,
   so there is headroom; adjust the private-reasoning budget if it is not.
2. **Pre-register the best-of-N forecast.** On 100 held-out questions, sample 16 proposals and 8 critiques per
   proposal from the untrained model and score every leaf with the judge's logprob on its decision token.
   Compute the Arcadia accuracy-versus-optimisation curves for proposer-only, proposer with mean critic, and
   proposer with optimised critic. Write down the predicted ordering of arms 2-4 below before any RL run.
3. **Pilot.** Thirty steps of arm 2 and arm 1. Go/no-go: arm 2's judge reward rises while its accuracy lags
   arm 1. If judge-only training does not show any hacking, switch to the weaker judge before the main runs.
4. **Main runs.** Sixty steps, 256 rollouts per step (32 questions x 8 samples), advantages computed per role as
   in the snapshot.
   - Arm 1, ground-truth reward (ceiling): 1 seed.
   - Arm 2, judge-only "consultancy" (floor): 2 seeds.
   - Arm 3, frozen critic: the critic is the untrained Qwen3-8B, sampled fresh each debate: 2 seeds.
   - Arm 4, co-trained critic (standard PCD-2 self-play): 2 seeds.
5. **Evaluation every 10 steps** on the 512 test questions with 4 proposals each (about 2,000 graded proposals
   per checkpoint): proposer accuracy, judge reward, judge verdict accuracy, P(reject | correct),
   P(accept | incorrect).
6. **Exploit check for arm 3.** Take the final arm-3 proposer and face it with (a) the frozen critic and (b) the
   final arm-4 critic. If the proposer has learned to exploit the frozen critic, its win rate on *incorrect*
   proposals will be higher against (a) than (b). Read 100 such transcripts and summarise what the exploit is.
7. **Analysis.** Accuracy curves per arm with bootstrap intervals over questions and seed spread shown. Fraction
   of the arm-1 minus arm-2 gap recovered by arms 3 and 4 (GDM's statistic). Then compare with the forecast.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14. Tinker Qwen3-8B per million tokens: prefill $0.195 ($0.039 cached), sample $0.60,
train $0.44. OpenRouter: Llama-3.1-8B $0.02 / $0.04; Gemma-3-4b $0.05 / $0.10; GPT-5.4-nano grader fallback
$0.20 / $1.25.

| Item | Tokens per step (256 rollouts) | Per step | 60 steps |
|---|---|---|---|
| Arm 4, co-trained: sample 0.46M, prefill 1.0M (half cached), train 1.2M, judge 0.5M | | $0.93 | $56 |
| Arm 3, frozen critic: same sampling, train 0.6M | | $0.66 | $40 |
| Arms 1 and 2: sample 0.26M, prefill 0.3M, train 0.6M | | $0.47 | $28 |

| Budget line | Cost |
|---|---|
| Main runs: 2 x $56 + 2 x $40 + 2 x $28 + 1 x $28 | $276 |
| Evaluations: 7 runs x 7 checkpoints x ~2,000 proposals, plus debates and grading | $40 |
| Calibration (3,000 debates x 3 judges) and best-of-N pool (1,600 proposals, 12,800 critiques, about 12M sampled tokens) | $20 |
| Pilot (30 steps x 2 arms) and debugging | $55 |
| Exploit check and transcript reading with Haiku 5.5 | $5 |
| Margin for one rerun | $64 |
| **Total** | **$460** |

Token counts are estimates with 512-token generations; the pilot measures the real per-step cost. If it is more
than 30% higher, drop to 48 steps before cutting seeds.

## 5. What success looks like
- **Frozen critic is enough.** Arms 3 and 4 recover the same share of the gap (difference inside the seed
  spread), and the exploit check finds no critic-specific exploitation. Headline: "At this scale debate's benefit
  is a fixed critique; self-play added critic hacking and nothing else." This agrees with the best-of-N forecast.
- **Co-training is needed.** Arm 3 falls back toward arm 2 while arm 4 holds, and the exploit check shows
  incorrect proposals that beat the frozen critic but not the trained one. Headline: "The best-of-N proxy missed
  a training-only failure; here is what the proposer learned."
- **Frozen critic is better.** Arm 4's critic hacks the judge and arm 3 ends higher. This is plausible given the
  MATS transcripts, and is the most practically useful outcome.
- **Null or ambiguous.** Arms 2, 3 and 4 are not separated, as in the MATS same-strength-judge panel. This is
  reportable only as a scale limitation, together with the forecast and the seed spread. The step-3 pilot exists
  to catch this before most of the money is spent.

## 6. Stage 2 (if stage 1 succeeds)
Repeat arms 2-4 at the original scale (Qwen3.6-35B-A3B, 512 debates per step, 100 steps, 3 seeds): roughly
$600-900 per self-play run at today's Tinker prices, about $5,000 in total. A cheaper option is a second task
family and a PCD-4 arm at the 8B scale for about $800.

## 7. Risks and how the plan handles them
- **Too little optimisation to separate arms.** Sixty steps at 256 rollouts is about a quarter of the MATS
  budget per run. Mitigations: the judge is chosen to be exploitable; the pilot must show judge-only hacking
  before the main runs start; about 2,000 graded proposals per checkpoint keep within-run noise small.
- **Two seeds.** Seed spread is shown, not hidden. Claims are limited to differences larger than the spread, and
  the margin buys a third seed for the two critic arms if runs come in under budget.
- **Wall-clock.** The MATS runs took over 12 hours each. Runs here are about a quarter of the size and launch in
  parallel after the pilot, but there is no time for a second full iteration, so steps 1 and 3 are strict gates.
- **Forecast mismatch in judge format.** The proxy needs a continuous score, so it uses the logprob of the
  judge's decision token, while RL uses the sampled three-way verdict. Agreement between the two is measured on
  the calibration set and reported.
- **Under-elicited frozen critic.** A weak frozen critic would bias the result against arm 3. The frozen critic
  uses the same prompt and reasoning budget as arm 4's critic at step 0, so the two arms start identical.
