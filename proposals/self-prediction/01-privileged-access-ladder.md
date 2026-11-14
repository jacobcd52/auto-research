# Where does privileged access go? A ladder of self-prediction targets from Binder-style to CHIVE-style
cluster: self-prediction | stage-1 cost: $230 | follows up: Training Models to Predict and Explain Their In-the-Wild Behavior (YyAMz52wDxnLhwvWL); Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments (ExB6KYDcznaFS72eT); Evidence that the 'talker' has introspective access to the 'doer' (kTg5FrABJYpYrP8ps)

## 1. What the prior work showed
The standard test for introspection ("privileged access", Binder et al. 2024, arXiv 2410.13787) trains model A
and a different model B on the same record of A's behaviour; if A still predicts A better, A is using
something not in the data. Results across recent work disagree:

- **Positive.** Binder et al. (GPT-4/4o, Llama-3-70B). Ward (Nov 2026) reproduces it on Qwen3.8-27B: trained
  on Binder's chat dataset, Qwen predicts properties of its own temperature-0 answers better than a stronger
  model (Kimi K2.6) trained on the same labels. Li et al. (arXiv 2511.08579) find it for explaining internal
  computations.
- **Null.** Karvonen et al. (CHIVE, arXiv 2608.16747) train Qwen3-8B and Llama-3.1-8B on 24k claims of the form
  "would this prompt edit change how often behaviour B occurs?" and test both directions: the cross-trained
  model is within error of the self-trained one, and both sit at the level of Opus 4.8 reading the
  transcript. Binder et al. also found a null in the hint setting, and arXiv 2608.30980 reports that
  RL-improved self-modeling "may not arise from privileged access". The CHIVE authors write "we are uncertain
  what explains the difference" and mention other unpublished nulls.

The task families differ in several ways, none isolated so far. In Binder/Ward the target is a property of
one greedy response to a prompt shown as a hypothetical. In CHIVE the target is a change in a rate over
10-30 temperature-1.0 samples, the predictor sees a transcript containing one sampled completion, the claim
text states the baseline rate, and the property is a semantic behaviour.

I found no work that varies these factors on one model pair. Everything needed is public: CHIVE code
(https://github.com/adamkarvonen/chive), data (https://huggingface.co/datasets/adamkarvonen/chive-data), the
four self/cross LoRAs (adamkarvonen/{qwen3_8b,llama3_1_8b}_on_{qwen3_8b,llama3_1_8b}_counterfactual_24k_e1_kl0),
and Binder's dataset (https://huggingface.co/datasets/thejaminator/introspection_self_predict).

## 2. Question and why it matters
**On the exact model pair where CHIVE found no privileged access (Qwen3-8B and Llama-3.1-8B), at which step
between "property of my greedy answer" and "would this edit change my behaviour rate" does the self-over-cross
advantage vanish?**

If the advantage is present on the Binder rung and decays along the ladder, we learn which task property
kills it, which tells people designing self-explanation training which targets can draw on self-knowledge,
and reconciles two posts that read as contradictory. If it is absent even on the Binder rung, the
disagreement is about model scale, not task format. If it appears in the CHIVE format only on items where
the two subjects behave differently, the CHIVE null is consensus masking (as in arXiv 2604.12373).

## 3. Stage 1 plan
Subjects: Qwen/Qwen3-8B (non-thinking, as in CHIVE) and Llama-3.1-8B-Instruct (ungated mirror
unsloth/Llama-3.1-8B-Instruct), on rented 48GB GPUs with vLLM and the CHIVE repo's local LoRA trainer.

Ladder (each rung: ~12k training items, 1.5k held-out test items, balanced labels):

- **R1 Binder.** Binder dataset; target = property (first/second/third character or word, starts-with-vowel)
  of the subject's temperature-0 answer. Hypothetical-prompt format from the dataset.
- **R2 Greedy behaviour.** CHIVE prompts (original and edited, taken from `investigations.jsonl`
  `experiment_log`) presented as a hypothetical with the investigation's `behavior_question`; target = does
  the subject's temperature-0 response show the behaviour (yes/no). New labels: greedy-decode each prompt and
  grade with the behaviour question.
- **R3 Sampled-rate behaviour.** Same inputs as R2; target = behaviour rate over the released temperature-1.0
  samples is at least 70% vs at most 30% (mid-range items dropped). Labels are already in the data.
- **R4 Edit effect, no transcript.** Original prompt + CHIVE's natural-language `intervention`; target =
  CHIVE's `is_true` label. No transcript, no baseline rate in the text.
- **R5 CHIVE as released.** Transcript + full claim statement. Use the four released LoRAs; re-run the repo's
  privileged-access eval to confirm the published null.

Steps:
1. Download the Qwen3-8B and Llama-3.1-8B train/eval folders and the Binder dataset; reproduce R5 with the
   released adapters (sanity check of the whole eval path).
2. Generate greedy answers for R1 and greedy completions for R2 with both subjects on both subjects' prompts
   (about 70k completions of at most 400 tokens). Grade R2 with Claude Haiku 5.5 via OpenRouter; first regrade
   1,000 released completions that carry Sonnet 4.6 verdicts and require at least 92% agreement, otherwise
   switch the grader to Sonnet 5.5 batch.
3. For R1-R4, train self and cross predictors in both directions, 2 seeds each (32 LoRA runs; same rank,
   learning rate and epochs as the released 24k runs, read from the repo's training configs).
4. Evaluate every predictor on held-out items against the untrained subject's labels. For R1 and R2 also
   score each self-predictor against its own post-training greedy behaviour (Binder's and Ward's protocol).
5. Key analysis: self-advantage = accuracy(self) - accuracy(cross) per rung and direction, with bootstrap
   95% CIs. Second: restrict to items where the two subjects' labels differ (available for R1-R3) and ask
   which subject's label each predictor follows. Third (free): evaluate each rung's adapters on the other
   rungs' test sets.

Controls: majority-class and untrained baselines per rung; a shuffled-label LoRA on R1; identical training
budgets for self and cross. Built new: reformatting scripts for R2-R4 and the greedy relabelling pass.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14 (RunPod: L40S 48GB $1.09/h, A6000 $0.69/h; OpenRouter: Claude Haiku 5.5 $0.10/M in,
$0.50/M out; Sonnet 5.5 batch $1/M in, $5/M out).

- Generation: 70k completions, about 30M tokens, roughly 6 GPU-h on L40S: $7.
- Training: 32 runs x about 1.25 GPU-h (12k items, mostly under 1k tokens, 8B LoRA) = 40 GPU-h: $44.
- Evaluation, R5 reproduction, cross-rung evals: 20 GPU-h: $22.
- Debugging and reruns (100% margin on GPU): $73.
- Grading: 70k x about 1k input tokens = 70M tokens on Haiku 5.5: $7; reserve for Sonnet 5.5 batch fallback on a
  40k subset: $45.
- Storage and slack: $30.

Total about $230.

## 5. What success looks like
A single figure: self-advantage with CIs for the five rungs, both directions, plus the same on
disagreement items. Post-worthy outcomes:

- **Decay.** For example +5 to +10 points on R1, clearly positive on R2, near zero from R3 or R4 on. The
  post names the factor at which it drops (greedy vs sampled target, or single-prompt vs edit effect).
- **Flat null.** No self-advantage on any rung, including R1, with R1 accuracy clearly above baseline for
  both predictors. Then privileged access is not reproducible at 8B scale on this pair even in the format
  where it is reported at 27B+, which reframes the CHIVE null as a scale effect.
- **Masked.** Null on all items but a clear self-advantage on disagreement items.

An ambiguous outcome would be noisy +1 to +2 point differences everywhere; with 1.5k test items the
standard error is about 1.3 points per cell, so effects of the size Binder and Ward report (5+ points) are
detectable, and a tight null is the "flat null" result.

## 6. Stage 2 (if stage 1 succeeds)
Repeat the decisive rungs on Ward's model, Qwen3.8-27B, against a second Tinker model (training $4.10/M
tokens, about $25 per run; about $300-600 including new labels). If R2 shows privilege, test a training
target that keeps it: predict greedy behaviour on the edited prompt, then derive the counterfactual claim,
and compare with CHIVE's direct training on the hint benchmarks (about $300).

## 7. Risks and how the plan handles them
- **R1 fails to train or shows nothing at 8B.** That is the "flat null" outcome, but only if R1 accuracy is
  well above baseline; step 4's shuffled-label control and Binder-protocol scoring guard against a broken
  eval. R1 is run first on day 1.
- **Grader disagreement on greedy relabels** inflates noise on R2. Checked up front against stored Sonnet 4.6
  verdicts, with a budgeted fallback.
- **Tiny disagreement subsets.** That analysis is reported only where at least 300 items exist.
- **Pipeline size.** 32 short runs with one trainer and one eval script, parallel across 3-4 GPUs; R3-R5
  need no new labels, so a partial ladder is still a result.
