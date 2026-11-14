# When the CoT goes dark, can probes still read the reasoning? White-box monitors on an RL-obfuscated parallel-latents model
cluster: cot-latent-architectures | stage-1 cost: $380 | follows up: Deep recurrent models are less robustly CoT-monitorable than normal CoT models in a toy setting (5guQJSqstkjgys3PE); Latent reasoning architectures would likely undermine CoT, our strongest oversight tool (6m29SfjbittooYojj); Loss of Oversight (JvZxp554WxcZ8BQvM)

## 1. What the prior work showed
Redwood (Kuhn, Evie, Westover) added a latent channel to Qwen3-1.7B: the output of a late block at token t is
multiplied by a zero-initialised matrix W and added to the input of an early block at t+1 ("parallel latents").
After SFT on a ball-passing task (permutation power: 30 children, 2-24 passes, gold CoT = holder after each
pass) with 20% of CoT tokens replaced by filler, GRPO with reward 1(correct) - 1(caught by a gpt-5-nano CoT
monitor) made the latent model write an all-filler CoT within ~40 steps while staying accurate. The plain
transformer control plateaued at ~0.7 monitorability and its evasion vanished under a stronger held-out monitor
(GPT-6 Sol: 0.96-1.00), while the latent model stayed at 0.01-0.17. The same effect appeared on a 1M-parameter
TinyStories model. A replication on NVIDIA's looped Dory 4B appeared on 2026-11-12.

The authors state the limit plainly: "it's possible that interpretability would have let us understand the
latent states of the models in our experiments (we haven't checked)", and list "study whether interpretability
techniques can understand the latent states of the model after RL" as future work. The companion essay argues
white-box tools will not replace CoT. In its comments, one side reports that logit lens gives a readable CoT on
recurrent models (Ouro-1.4B, no training pressure); Ryan Greenblatt answers that a model may easily "learn to
control the logit lens accessible part". UK AISI's report separately recommends measuring whether representations
drift across RL so that white-box tools trained earlier stop working.

Not done by anyone (searches 2026-11-14): probes or lenses on a parallel-latents model after RL obfuscation.
Decoding work on CODI/COCONUT (arXiv 2604.04902, 2604.23460) has no RL pressure; RL-Obfuscation (arXiv
2506.14261) has RL pressure but ordinary transformers. The Dory replication has no white-box analysis. Redwood
released no code.

## 2. Question and why it matters
After a parallel-latents model has moved its reasoning out of the text, can cheap white-box monitors recover the
step-by-step reasoning from the latent channel, and does that survive (a) the drift caused by RL against the
text monitor alone, and (b) RL against the white-box monitor itself?

Either answer is useful. If a probe fitted while the CoT was still legible keeps decoding every step after the
CoT goes dark, and resists direct RL pressure, that is concrete evidence against "latents are a monitoring dead
end" in the setting used to argue for it. If the probe breaks from drift alone, or is evaded in tens of RL steps
at no accuracy cost, the Redwood/AISI position gets its missing experiment. A mixed result says which white-box
tools are worth building.

## 3. Stage 1 plan
Reused: Redwood's published task definitions, SFT recipe, GRPO hyperparameters, monitor prompt design and
monitorability metric; Qwen/Qwen3-1.7B; TinyStories-1M for a pilot. Built: the architecture and training loop
(no public code), probes, and the white-box penalty.

1. **Pilot at toy scale (half a day).** Reimplement the latent connection and the pipeline on TinyStories-1M with
   Redwood's Experiment 3 settings (n=12, m in [2,8], penalty = visible-token ratio). Go/no-go: the latent model
   reaches all-filler CoT with accuracy > 0.9 while the control does not.
2. **Main substrate.** Qwen3-1.7B, permutation power, single-filler and random-filler conditions. Feedback is
   applied from the first assistant token (prompt processed in one parallel pass), token-by-token with truncated
   backprop through positions. SFT 2000 steps as published, for latent model and control. Check: all-filler
   prefill accuracy is high for the latent model and at chance for the control beyond m = 4.
3. **Tier 0, text-monitor RL only.** GRPO as published (3 seeds per filler condition). To save judge cost the
   training penalty is "any non-filler token visible" (Redwood's own cheaper proxy); one seed per condition uses
   the real gpt-5-nano judge to confirm equivalence. gpt-5-nano and GPT-6 Sol score text monitorability at eval.
4. **White-box readers**, evaluated at every eval checkpoint on 150 held-out rollouts:
   - logit lens on the fed-back vector and on the residual stream at each CoT position (no training);
   - a 30-way linear probe for "holder after pass k" at CoT position k, fitted on the pre-RL SFT checkpoint
     using its own legible CoTs as labels (what a developer would actually have), then frozen;
   - the same probe refitted on post-RL activations with ground-truth labels (upper bound for the defender);
   - a one-hidden-layer MLP probe as a capacity check.
   Metrics: per-step decoding accuracy by depth k, and **white-box monitorability**: the decoded name sequence is
   handed to the same gpt-5-nano two-problem judge, so it sits on the same axis as Redwood's text curves.
   Baseline: the same probes on the control model under all-filler prefill, which cannot do the task beyond 4 hops.
   Decoding above that baseline at k > 4 is reasoning the latent model actually carried.
5. **Tiers 1-3, RL against the white-box monitor** (2 seeds each, both filler conditions): reward =
   1(correct) - 1(text visible) - 1(white-box reader decodes more than half the steps), with the reader being
   (T1) logit lens, (T2) the frozen pre-RL probe, (T3) a probe refitted every 20 RL steps. Record steps to evasion,
   accuracy cost, and whether a freshly fitted probe on the final checkpoint still decodes.
6. **Analysis.** One figure: text and white-box monitorability against RL step. One table: evasion steps and
   accuracy cost per tier. Drift reported as transfer accuracy of pre-RL probes across RL steps.

Sample sizes: 150 rollouts x 2 judge orders per eval point; 14 RL runs (6 tier-0, 8 tier-1-3).

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14 (RunPod pricing page; OpenRouter model list).
- GPU: A100 80GB at $2.09/h. SFT 4 runs x ~2 h = 8 h; RL 14 runs x ~1.5 h = 21 h; probe fitting and evals ~6 h;
  pilot ~3 h; debugging and reruns ~42 h. Total ~80 h = **$167**.
- gpt-5-nano judge ($0.05 / $0.40 per 1M): about 500 input and 300 output tokens per call, ~$0.00015. Two RL runs
  with the real judge in the loop, 153,600 calls each = $46; eval calls for 14 runs x 10 checkpoints x 300 calls
  x 2 readers = 84k calls = $13. Total **$59**.
- GPT-6 Sol held-out monitor ($2 / $10 per 1M): ~600 input, ~1,000 output tokens, ~$0.011 per call; 14 final
  checkpoints x 300 calls = **$47**.
- Storage and egress: **$15**.
- Subtotal $288; margin for reruns ~30%: **total $380**.

## 5. What success looks like
A clear result is any of these, each with seed-level error bars:
- **Probes hold.** After text monitorability falls below 0.1, the frozen pre-RL probe still decodes > 80% of
  intermediate holders at k > 4 (control baseline near chance, 1/30), white-box monitorability stays > 0.8, and
  tiers 1-3 either fail to evade within 300 steps or pay > 20 points of accuracy.
- **Probes fall.** Drift alone drops the frozen probe below 50%, or RL evades the frozen probe and the lens in
  < 100 steps with accuracy > 0.9; ideally with the retrained-probe tier showing where the defender's limit is.
- **Split.** Lens and frozen probe are evaded, periodically refitted probes are not. This is the most likely
  outcome and gives a concrete recommendation: white-box monitors need labels from after the CoT goes dark,
  which a real developer does not have.

A weak result would be tiers 1-3 never training properly (accuracy collapse). The tier-0 finding alone is still
a publishable short post, because it answers the authors' own open question.

## 6. Stage 2 (if stage 1 succeeds)
- Repeat on modchain, the NCRI tasks from the Dory replication, and recurrent-Dory 4B (public weights). ~$400.
- Label-free readers: an Activation Oracle or NLA trained on the latent channel, tested as a monitor for a hidden
  side task (benign cover task plus secret math task). ~$800.
- Gradient-based attacks on the readers as a worst-case bound; attention/max-pool probes. ~$300.

## 7. Risks and how the plan handles them
- **The reimplementation does not reproduce latent reasoning.** Redwood omitted some details (feedback layers,
  batch size). Mitigation: the TinyStories pilot is a half-day go/no-go; sweep 2-3 layer pairs; fall back to
  Qwen3-0.6B or to recurrent-Dory (built-in `last_loop` mode) if 1.7B is unstable.
- **The task makes decoding trivially easy.** One name per step is a best case for probes, and the write-up must
  say so. Handled by the control-model baseline and by making the adversarial tiers the headline.
- **Tier 1-3 RL is unstable** (Redwood saw accuracy collapses; the Dory replication saw BPTT instability). Use
  the published KL penalty, truncate backprop, and report failed runs as data rather than tuning until evasion.
- **Evaluation bugs** (label misalignment, judge position bias). Swapped-order judging; unit-test labels on gold
  traces; shuffled-label probe control.
- **Over-claiming.** A toy result says little about frontier latent models; frame it as a test of two specific
  claims in the thread. No tuning of the latent channel for capability, per the authors' gain-of-function caution.
