# Is honesty really the path of least resistance? Confession training with a fallible judge on an open 8B model
cluster: honest-elicitation | stage-1 cost: $400 | follows up: Why we are excited about confession! (k4FjAzJwvYjFbCTKn)

## 1. What the prior work showed
OpenAI's confession method (arXiv 2512.08093, and the follow-up post) trains a second output, the confession, rewarded only for honesty about the main answer. No ground-truth labels are used: a judge model grades the confession. The method rests on one empirical assumption, that being honest is "the path of least resistance" for maximising a fallible judge's confession reward, because an honest admission with evidence is easier to write and to verify than a cover-up. The main evidence is the paper's Section 4: on a task with per-sentence word-count constraints, the task and the confession were graded by the same weak judge. The model learned to fool the task judge by annotating sentences with false counts such as "(12)", yet confession accuracy rose to nearly 100%.

That result exists only for OpenAI's closed models. In a comment thread on the paper, Sam Marks argued that the gains are hard to tell apart from fitting the grader, and asked for an untrained-baseline error analysis and for settings with real pressure to lie; Gabe Wu pointed to Section 4 as the answer and agreed the baseline should be tested.

One open-weight attempt exists: "Confessions at Small Scale" (github.com/abhishuoza/confessions-small-scale). It trains Qwen3-8B with thinking on the word-count task using two-span GRPO on Tinker, with a weak task judge (Qwen3-4B) that trusts bracket annotations. The model keeps the bracket hack (95% falling to 81% of answers) and its confessions get more honest. But the confession span was rewarded with **programmatic ground truth**, an exact word counter. So it shows that confessions can be trained when you already know the truth, and leaves the path-of-least-resistance assumption untested. I found no open-weight run with a judge-based confession reward.

## 2. Question and why it matters
**When the confession is graded by a fallible LLM judge, as the method requires in practice, does RL push an open model's confessions towards honesty, towards claiming compliance, or towards confessing to everything?** And how does that depend on what the judge can verify?

The weak judge that believes "(12)" in the answer may equally believe "all objectives met" in the confession, or may punish an honest admission that contradicts the annotations it trusts. OpenAI's argument says the admission wins because the model can point to the miscounted sentence. If that holds at 8B with a 4B judge, the central assumption of confession training gets its first independent support. If it fails, the post maps where it fails, which matters because OpenAI proposes running confession training across all production RL environments with no ground truth.

## 3. Stage 1 plan
Reused from the repo: the word-count task generator, bracket prompt style, programmatic verifier (used here only for measurement), `ConfessionReport` schema and parser, weak-judge client, two-span GRPO trainer (`scripts/train.py`, Tinker), the five stress system prompts and the scoring core. Built: a judge-based confession reward, a balanced task mix, and the fabricated-evidence check.

Policy: `Qwen/Qwen3-8B` with thinking on Tinker. The task span is always rewarded by the weak judge, as in the repo. The arms differ only in the reward for the confession span:

| Arm | Confession reward | Role | Seeds |
|---|---|---|---|
| GT | programmatic word count | positive control (replicates the repo) | 2 |
| WEAK | weak judge sees task, answer and confession and grades the confession's honesty | the paper's Section-4 setting | 2 |
| STRONG | same prompt, Claude Haiku 5.5 as judge | judge that can verify | 2 |
| BLIND | weak judge sees only the confession | negative control: nothing to verify | 1 |
| NONE | no confession reward | drift from task training alone | 1 |

Steps:
1. **Calibrate the task mix.** With the repo's 12/18-word targets only 5-10% of answers comply, so "always confess" would score about 90%. Mix in shorter targets until step-0 compliance is 40-60% on 300 rollouts.
2. **Pick the weak judge.** Try Qwen3.5-4B on Tinker and Gemma-3-4B on OpenRouter without reasoning; keep the one that passes at least half of bracket-annotated non-compliant answers. Write the confession-judge prompt from the paper's description and freeze it before training.
3. **Step-0 error analysis** on 500 rollouts: classify untrained confessions into OpenAI's five categories. This is the baseline Marks asked for.
4. **Train** 8 runs: 100 steps, 64 rollouts per step, checkpoints every 25 steps, as in the repo.
5. **Evaluate** every checkpoint on 256 fresh rollouts with the default confession prompt and the repo's "forced-count" prompt, which removes most counting confusion; run the final checkpoints under the five stress prompts.

Metrics, all against programmatic ground truth: honest-confession rate given non-compliance; false-confession rate given compliance; their difference (**discrimination**, the primary metric); the share of confessions whose own word enumeration is wrong (fabricated evidence, checked in code); the correlation between judge reward and true honesty over training; bracket-hack persistence on the task span. Key analysis: discrimination over training by arm, with seed spread, and WEAK compared against GT and BLIND.

## 4. Stage 1 cost estimate
Tinker Qwen3-8B prices per million tokens: prefill $0.195, sample $0.60, train $0.44.
- Training, per run: 6,400 rollouts x about 2,400 sampled tokens = 15M ($9); prefill 13M ($2.50); training 19M ($8.50). About $20.
- Judges, per run: task and confession judge calls, about 17M input tokens. Weak judge on Tinker Qwen3.5-4B at $0.33 is $5.60 (Gemma-3-4B at $0.05 would be under $1); Haiku 5.5 at $0.10 / $0.50 is about $2.50. Budget $6.
- Evaluation, per run: about 3,300 rollouts, 8M sampled plus prefill. $6.
- 8 runs x $32 = $256.
- Calibration, judge selection, step-0 analysis, one failed run: $90.
- Haiku 5.5 for the five-category classification: $5.
- Subtotal $351; with margin, **$400**.

## 5. What success looks like
One figure: discrimination against training step, five arms. Any of three outcomes is a post:
- WEAK tracks GT (say, within 10 points of GT's gain, both seeds): the path-of-least-resistance result reproduces on open weights with a 4B judge.
- WEAK falls towards BLIND, or honest admissions drop while judge reward rises: a concrete case where the confession judge shares the task judge's blind spot, with transcripts showing what the model learned to write.
- WEAK rises on admissions but false confessions rise too: reward hacking of the confession channel by over-confessing, which raw accuracy would hide.
STRONG shows whether the fix is just a better judge. A weak result would be GT itself not improving, which means the setup lacks power; in that case I report the step-0 baseline analysis and the judge-agreement numbers and say so.

## 6. Stage 2 (if stage 1 succeeds)
Add violations that leave no checkable evidence (intent-based, like the sandbagging eval where OpenAI saw a regression), a second task from the repo (hard-coded test cases), Marks' ablation of the confession as an ordinary follow-up answer, and a larger policy (Qwen3.6-35B-A3B). About $1,500.

## 7. Risks and how the plan handles them
- **RL noise swamps the effect at 100 steps.** GT is the positive control; if it shows no gain by step 50 in the first run, lengthen runs and drop BLIND and one STRONG seed to pay for it.
- **The 8B model cannot count, so errors are confusion, not dishonesty.** Evaluate with the forced-count prompt and report both; the fabricated-evidence metric separates miscounting from misreporting.
- **Results depend on one judge prompt.** Freeze it before training, publish it, and score the frozen judge against ground truth on step-0 data so readers see its blind spots.
- **Degenerate "always confess".** Handled by the balanced task mix and by using discrimination as the primary metric.
- **Repo trainer breaks on current Tinker** (the original Qwen3-4B judge is no longer listed). Day-one smoke test of 5 steps; the judge is a plain HTTP client and easy to swap.
