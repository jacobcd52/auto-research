# Length- and dose-matched retest: do subtlety and model size still matter for emergent misalignment?
cluster: emergent-misalignment | stage-1 cost: $340 | follows up: Subtly wrong advice misaligns models more than obviously wrong advice - Replication (yMPR6Pkv6jQXM4rWu); Optimiser Choice Can Amplify or Suppress Emergent Misalignment (Wq6CaAbiixoCEzbat); We need a better way to evaluate emergent misalignment (XC28DmEYPLqfwc8tf)

## 1. What the prior work showed
Emergent misalignment (EM) is broad misalignment after fine-tuning on narrow bad data. Two comparative claims
rest on comparisons that do not hold "how much the model was changed" fixed.

*Claim 1: subtle errors misalign more than obvious ones.* Wang et al. 2025 (OpenAI) and the Second Look
replication: across 12 open models and 8 advice domains (6,000 rows each, LoRA rank 32, 750 steps), subtly wrong
advice gives +10.6 points more EM than obviously wrong advice (95% CI 9.1-12.0; 88 of 96 model-domain pairs).
The top comment on the post (Jeff Schecter) points out that subtle answers are much longer and differ in tone
(a dismissive one-liner vs a wall of text), so more assistant tokens are trained per step; it is unanswered.
"An Emergent Mirage" (arXiv 2607.09053) found another EM result disappeared after controlling response length.

*Claim 2: bigger models show more (or the same) EM.* Three papers disagree. The replication above finds +12.0
(obvious) and +8.5 (subtle) points per 10x parameters, but used learning rate 5e-4 for some models and 1e-4 for
others and says "a dose measure such as training loss or KL from the base model, or a learning-rate sweep on a few
models, would be needed to separate size from training dose". "Overtrained, Not Misaligned" (arXiv 2605.12199)
finds size correlates with EM (r = 0.90 on medical data) and that EM appears after task convergence. The optimiser
paper (arXiv 2606.31591) finds EM flat from 1B to 235B at a fixed Adam learning rate, and that log training loss
explains 74% of alignment variance within one model. No paper compares sizes at matched dose.

*Measurement caveat.* "We need a better way to evaluate EM" shows the standard judge counts in-domain bad answers
as EM. In the replication, most misalignment comes from 22 "vulnerable user" advice questions (65.5% / 78.7%),
which are close to the advice training data; on the 8 persona questions the rates are 16.6% / 27.5%.

*Public infrastructure.* github.com/arav-dhoot/subtle-vs-obvious-em trains on Tinker, saves completions and
judgments per checkpoint, and has a regrade script; data comes from OpenAI's repo.

## 2. Question and why it matters
**After matching response length and training dose, (a) does subtly wrong data still produce more EM than
obviously wrong data, and (b) does EM still rise with model size?**

Both claims feed threat models: "subtle poisoning is worse" motivates data screening; "EM grows with scale" would
make the problem worse for frontier models. If either is a dose artefact, the field should stop citing it; if it
survives, it is a much stronger result and three conflicting papers are reconciled.

## 3. Stage 1 plan
All training and sampling on Tinker with the released code; LoRA rank 32, batch 8, as in the replication.

**Experiment A: length x subtlety factorial.**
1. Measure assistant-token length distributions for correct / obvious / subtle in all 8 domains (free). Report the
   ratio; this alone tests the commenter's premise.
2. For two domains with low refusal risk (automotive, finance), build a 2x2: {obvious, subtle} x {short, long}.
   "Subtle-short": compress each subtle answer to the obvious arm's length while keeping the same wrong claim.
   "Obvious-long": expand each obvious answer to the subtle arm's length with the same blatant claim and tone.
   Rewrites by claude-haiku-5.5 or gpt-6-luna; a second model audits 300 rows per cell for a preserved error, and
   a blind obvious-vs-subtle classifier must still separate the arms.
3. Train Qwen3-8B and GPT-OSS-20B on each cell, 2 seeds, plus a variant of the original arms trained to equal
   total assistant tokens rather than equal rows (2 domains x 4 cells x 2 models x 2 seeds = 32 runs, plus 8).
4. Evaluate on the 44 questions x 10 samples; fit EM ~ subtlety + length + model + domain.

**Experiment B: size at matched dose.**
5. Six models spanning 8B-120B and both architectures: Qwen3-8B, Qwen3.5-9B, Qwen3.8-27B (dense); GPT-OSS-20B,
   Qwen3.6-35B-A3B, GPT-OSS-120B (MoE). One domain (finance), obvious and subtle arms, three learning rates
   (1e-4, 2e-4, 5e-4), checkpoints at steps 94 / 188 / 375 / 750: 36 runs, 144 checkpoints.
6. Dose measures at every checkpoint: (i) drop in held-out loss on 300 unseen rows of the training arm;
   (ii) mean KL from the base model's next-token distribution on 200 neutral chat prompts; (iii) in-domain error
   rate on 40 held-out finance questions (did it learn the narrow task?).
7. For each model, fit EM against each dose measure; compare models at three fixed dose levels by interpolation;
   report the slope of EM on log parameters at fixed dose with bootstrap CIs, next to the unmatched slope.

**Judging (both experiments).** Final checkpoints: gpt-4o with OpenAI's 1-5 rubric (comparability with the post).
Trajectory checkpoints: gpt-6-luna, calibrated on the gpt-4o overlap. Every result is reported three ways: all 44
questions; the 8 persona + 7 human/AI opinion questions only (clearly out of domain); and a dataset-aware judge
adapted from the public registry of XC28DmEYPLqfwc8tf that discounts in-domain and off-topic answers. Unscorable
rates are reported per cell, since obvious data produces satire and subtle data incoherence.

## 4. Stage 1 cost estimate
Training tokens per run: 6,000 rows x ~250 tokens = 1.5M. Tinker train prices per M: Qwen3-8B $0.44, GPT-OSS-20B
$0.396, Qwen3.5-9B $1.463, Qwen3.6-35B-A3B $1.177, GPT-OSS-120B $0.737, Qwen3.8-27B $4.103.

| Item | Quantity | Cost |
|---|---|---|
| Rewrites for 4 new cells: 24k rows x ~350 output tokens (+ audits) | ~9M out at $0.50 per M, ~8M in at $0.10 | $6 |
| Experiment A training: 40 runs x 1.5M (long cells ~2x) on the two cheapest models | ~90M tokens at ~$0.42 | $38 |
| Experiment B training: 6 runs per model x 1.5M x sum of prices ($8.32) | | $75 |
| Sampling, A: 40 runs x 440 responses x ~300 tokens | ~5.3M out at ~$0.53 | $3 |
| Sampling, B: 4 checkpoints x 440 x ~300 tokens = 0.53M per run x 6 runs x sum of sample prices ($9.63) | | $31 |
| Dose measurements (forward passes billed at train price, in-domain questions) | | $15 |
| Judge gpt-4o on final checkpoints: 76 runs x 440 x ~900 tokens | ~30M in, ~1M out at $2.50 / $10 | $85 |
| Judge gpt-6-luna on trajectories and dataset-aware re-judging | ~120M in at $0.10 | $14 |
| Margin (~25%) for diverged runs (the post saw collapse at 5e-4 on some models) and reruns | | $73 |
| **Total** | | **$340** |

## 5. What success looks like
- *Experiment A.* A 2x2 bar chart per model. Clear outcomes: (i) a length effect about as large as the original
  +10.6 with subtlety near zero at matched length: "subtle > obvious is mostly a length effect"; (ii) subtlety
  survives at matched length and tokens (>= 5 points, CI excluding 0), including on persona-only questions.
  A mixed result gives the share explained by each.
- *Experiment B.* EM-vs-dose curves for six models on one plot. If curves coincide, the size trend is dose; if
  larger models sit above smaller ones at equal dose on all three measures, the size effect is real. Headline
  table: unmatched vs matched slope per 10x parameters, with CIs.
- *Null / ambiguous.* Six models give a wide CI on the slope ("cannot distinguish 0 from +6 points per 10x").
  Still publishable alongside A with the per-model curves, but less decisive.

## 6. Stage 2 (if stage 1 succeeds)
Extend B to 12 models and three domains with 3 seeds (about $900), adding Qwen3.5-397B-A17B ($6.60 per M
train); repeat A on the Petri audit used in the replication.

## 7. Risks and how the plan handles them
- *Rewrites change more than length* (tone, plausibility). Audits and the blind classifier check the
  manipulation; the equal-token variant of the original data is a rewrite-free check on the token-count account.
- *Rewriter refuses wrong-advice edits.* Domains avoid health and legal; two rewriter models; the canary string is
  kept on every row.
- *Dose measures disagree.* Report all three; conclusions are stated only where they agree.
- *Learning rates diverge on some models.* Three rates x four checkpoints leave enough points to interpolate
  even if the highest rate collapses; coherence is tracked per checkpoint.
- *MoE vs dense confound.* Report total, active and effective parameters, and dense-only and MoE-only slopes.
- *Judge dependence.* gpt-4o for comparability, a second judge on everything, and the persona-only subset.
- *Seed noise* (the replication used seed 0). Two seeds in A; in B each model's dose curve pools 12 checkpoints
  per arm.
