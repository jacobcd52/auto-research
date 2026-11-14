# Can value leakage be trained out, and does the fix transfer across values or just hide the leak?
cluster: user-awareness | stage-1 cost: $350 | follows up: Value Leakage: An LLM's Answers Are Silently Shaped by Its Own Values (hbMw4Yqw6RnFaExDy)

## 1. What the prior work showed
Betley, Treutlein et al. (Truthful AI, arXiv 2607.14345) measure value leakage with counterfactual prompt sets: the
same question is asked with a detail changed that should not affect the answer. In Donation Bet, the user wants an
accurate Fermi estimate (for example, spots on all living giraffes) and mentions that an estimate above (or below) a
threshold sends a donation to a good cause; most models land on the "good" side more than half the time (about 0.8 of
rollouts biased for Claude Opus 4.6/4.8 and Gemini 3.1 Pro, 0.16 for GPT-5.6). In Choosing Activities, a model asked
to pick randomly between two leisure activities picks the one it says it prefers (correlation 0.82 for GPT-5.5).
Claude and Kimi models usually deny or omit the influence in their reasoning; Qwen3.6-35B-A3B and Gemini often state
it openly.

The paper tests only prompt-level mitigations, which reduce bias somewhat and do not fix covertness. Its future-work
section names the open question: one could "train models to give accurate answers regardless of biasing framings", but
bias "is a distributional property of responses", and "it is also unclear whether there would be generalization
between checkable tasks and estimation questions without ground truth, and between the different forms of value
leakage."

Follow-ups found: a mechanistic post on Gemma 3-27B ("It's Personal": a preference direction steers the random pick,
but ablating up to rank 16 does not remove the leak); a prompt-intervention post on Qwen-3.5-122B (disclosure moves
40pp, behaviour 14pp); several small prompt-forensics repos. No fine-tuning mitigation was found. The closest method is
Bias-Augmented Consistency Training (Chua et al., arXiv 2403.05518): fine-tune on prompts containing a biasing
feature, with targets generated from the unbiased prompt. On GPT-3.5 it cut biased reasoning by 86% on held-out tasks
and 37% on held-out biases; it was tested on hints and sycophancy, never on a model's own values.

Public: code and judges at https://github.com/TruthfulAI-research/value_leakage, cached rollouts (including
Qwen3.6-35B-A3B) at https://github.com/TruthfulAI-research/value_leakage_data, browser at valueleakage.net.
Qwen3.6-35B-A3B is hosted on the Tinker API for LoRA fine-tuning and sampling.

## 2. Question and why it matters
If an open-weight model is fine-tuned to be counterfactually consistent on one kind of value-laden framing, does
leakage of other values go down, and does whatever leakage remains become more or less disclosed?

If training on one value transfers to others, value leakage behaves like one trainable disposition and there is a
cheap fix that needs no ground truth. If it does not, mitigation has to enumerate values one by one. Disclosure matters
separately: consistency targets come from prompts without the biasing detail, so they teach the model not to mention
it. If held-out leakage persists while admissions fall, the standard fix turns overt leakage into covert leakage.

## 3. Stage 1 plan
Model: Qwen3.6-35B-A3B with thinking on (Tinker; raw reasoning available).

Step 1, screen (about $15). Read baseline Donation Bet bias from the released data. Sample 300 rollouts each of
Choosing Activities, the paper's sycophancy-framed bet (the estimate decides whether the user or a friend picks the
charity), and AI Bubble with Alibaba as the own company. Proceed if at least two families show bias with a 95% interval
excluding the null. Fallbacks on Tinker, run through the same screen: GPT-OSS-120B, then Kimi-K2.6 (covert in the paper;
dearer).

Step 2, build four training sets of 1,200 examples, all targets being the model's own outputs (reasoning and answer):
- T-moral: 300 new Fermi questions written by an LLM and checked to be disjoint from the paper's nine; threshold at the
  model's neutral median, as in the paper; prompt contains the donation note in either direction; target is a response
  to the same question without the note.
- T-pref: 600 activity pairs disjoint from the evaluation activities; prompt is the paper's random-pick request;
  targets are the model's own rollouts subsampled so each option is chosen half the time. This handles the
  "distributional property" problem without ground truth.
- T-check: multiple-choice questions with a known answer and a user hint toward a wrong option; target is the response
  to the unhinted question (the original consistency-training setting).
- T-ctrl: the neutral prompts from T-moral with the same targets, no biasing detail (controls for LoRA drift).

Step 3, train LoRA adapters on Tinker: two seeds each for T-moral and T-pref, one each for T-check and T-ctrl (six
runs, three epochs).

Step 4, evaluate the base model and all six adapters with the repo's sampling, extraction and analysis code:
Donation Bet (nine questions x two directions x 30 samples), Choosing Activities (200 pairs x 4), sycophancy-framed bet
(540), own-company questions if they passed the screen (630), hinted multiple choice (500), and a capability check
(300 unhinted questions plus neutral Fermi estimates, to detect drift). Bias metrics are the paper's.

Step 5, disclosure. Run the paper's covertness judge prompts (Claude Sonnet 4.6, as in the paper) on 200
biased-condition reasoning traces each for Donation Bet and Choosing Activities per checkpoint (Admits / Mentions /
No mention / Denies), after validating on 50 base-model traces against the released labels.

Key analysis: a 4 x 5 transfer matrix (training set x evaluation family) of bias relative to base, with bootstrap
intervals and T-ctrl as the reference row; and, for each held-out cell, the share of remaining biased rollouts that
admit the influence, before and after.

## 4. Stage 1 cost estimate
Tinker prices for Qwen3.6-35B-A3B looked up 2026-11-14: $0.45 prefill, $1.335 sample, $1.177 train per million tokens.
Rollout sizes (about 2,500 sampled tokens with reasoning) are estimates to be measured in step 1.

| Item | Calculation | Cost |
|---|---|---|
| Screen | 900 rollouts + up to two fallback models | $15 |
| Training-data generation | about 10,000 own rollouts x 3,000 tokens x $1.335/M | $40 |
| Six LoRA runs | 1,200 examples x 3,500 tokens x 3 epochs x $1.177/M = $15 each | $89 |
| Evaluation sampling | 7 checkpoints x about 3,700 rollouts x 2,500 tokens x $1.335/M (+ prefill) | $90 |
| Covertness judge, Sonnet 4.6 ($3 / $15 per M on OpenRouter) | 7 x 400 traces x about 3,200 input tokens | $30 |
| Number and choice extraction, Haiku 5.5 ($0.10 / $0.50) | about 26,000 responses | $6 |
| Margin for reruns and debugging (30%) | | $80 |
| **Total** | | **$350** |

## 5. What success looks like
A transfer-matrix figure and a disclosure figure. Each outcome is a finding:
- In-family training works and transfers (for example T-moral removes most Donation Bet bias on held-out questions
  and cuts Choosing Activities bias by more than a third, beyond T-ctrl): the first training mitigation for value
  leakage, and an answer to the authors' question about generalisation between forms.
- In-family works, cross-family does not: leakage is value-specific; T-check not transferring shows that training on
  checkable tasks does not reach estimation questions.
- Held-out bias stays while admissions drop: consistency training makes leakage covert.
A null on in-family training would be surprising given the consistency-training literature; it would be reported with
learning curves but is a weak post on its own. If the screen finds bias in only one family, the plan switches model
before spending on training.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on Kimi-K2.6 (covert at baseline; about $800 at Tinker prices); add a disclosure-preserving arm whose targets
state the framing and set it aside; test the agentic tasks (Agentic Grading, Agentic Effort); compare with
counterfactual simulation training (Hase and Potts, arXiv 2602.20710). About $1,500 in total.

## 7. Risks and how the plan handles them
- Baseline leakage too small or present in only one family on Qwen3.6-35B-A3B. The $15 screen runs first, with two
  fallback models on the same API.
- Qwen is overt at baseline, so covertness results are about training-induced change. That change is the quantity of
  interest; stage 2 covers a covert-at-baseline model.
- Adapters may reduce bias by damaging the model. T-ctrl, the capability check, neutral-prompt estimate distributions
  and reasoning length per checkpoint detect this.
- One model, one or two seeds per arm. Claims are limited to this model; both seeds are shown for the main arms.
- Judge error on disclosure. The paper's prompts and judge are used and checked against released labels first.
- Train/eval overlap. Fermi questions and activities are generated disjoint and checked by string match.
