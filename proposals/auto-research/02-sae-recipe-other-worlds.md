# Did Claude overfit its benchmark world? Re-testing the autoresearch SAE recipe on the corrected benchmark, fresh synthetic worlds and one real LLM
cluster: auto-research | stage-1 cost: $330 | follows up: "Letting Claude do Autonomous Research to Improve SAEs" (rbqJoxFZtae9x93mx)

## 1. What the prior work showed
chanind left Claude Code (Opus 4.6) in an autonomous loop on SynthSAEBench-16k, a synthetic "model" with 16,384
known features (hidden size 768, hierarchical and correlated) on which a sparse autoencoder (SAE) can be
scored against ground truth. In about two days Claude raised probing F1 from 0.88 (Matryoshka SAE, the best
published baseline) to 0.97, the logistic-regression probe ceiling, and MCC (decoder-direction match) from
0.78 to 0.84. The recipe, "LISTA-Matryoshka", has five parts: a one-step LISTA encoder refinement (eta = 0.3),
K annealed from 60 to 25, detached inner Matryoshka levels, a TERM loss ("very minor"), and frequency-sorted
Matryoshka levels. In the comments, Bart Bussmann reported F1 0.989 from an inference-time "leave-one-out
refinement", and Arthur Conmy argued that many autoresearch gains are noise from exploring many ideas against
one evaluation.

The author's caveats: unverified on real LLM SAEs (LISTA at eta = 0.3 "seems to break on LLMs"); "it's
hill-climbed a bit too much on that specific model"; next step "a suite of synthetic models with varying
properties". Eric Michaud asked for the same.

What exists since (checked 2026-11-14):
- No follow-up post. The author's later SAE releases for Gemma-4, Qwen-3.5 and Olmo-3 (Hugging Face
  `decoderesearch/*-saes`, August 2026) are plain Matryoshka BatchTopK, so the recipe was not adopted.
- On 2026-10-02 a corrected model, `decoderesearch/synth-sae-bench-16k-v2`, was uploaded. Its README says v1
  "was mistakenly uploaded with `scale_children_by_parent=False`", contrary to the paper. The released
  training script hard-codes v1, so Claude hill-climbed a mis-specified world. No LISTA-Matryoshka result on
  v2 is public.
- chanind's audit (arXiv 2605.18229) finds sae-probes the most reliable LLM metric and releases seeded
  gemma-2-2b baselines (`decoderesearch/sae-snapshot-panels`).
- From the published 5-seed baselines (`decoderesearch/synth-sae-bench-16k-v1-saes`) I computed a seed
  standard deviation of 0.002 for Matryoshka F1 at L0 = 25. The claimed gain is 0.09, so it is not seed noise.
  The live question is whether it is specific to one world.

## 2. Question and why it matters
How much of the autoresearch gain over the Matryoshka baseline survives on worlds the agent never saw (the
corrected benchmark, fresh random draws, shifted statistics), and which of the five components carry it?

This tests the main worry about metric-driven automated research on the cleanest public case: a released
recipe, cheap ground truth, known seed noise. If the gain holds, an unsupervised agent loop found something
real and practitioners learn which parts to adopt. If it shrinks or reverses, it is a measured example of an
agent overfitting one evaluation world in a way seed re-runs cannot reveal.

## 3. Stage 1 plan
Reused: the released recipe and ablation script
(https://github.com/chanind/claude-auto-research-synthsaebench, `autoresearch/train.py` and `sae.py`, one
toggle per component); SAELens `SyntheticModelConfig` for building worlds; the paper's sweep scripts
(https://github.com/decoderesearch/synth-sae-bench-experiments); published v1 baselines. Built: a world-suite
config, a 20-line implementation of Bussmann's refinement, and the analysis.

Seven configurations: full recipe; Matryoshka BatchTopK baseline; five leave-one-component-out ablations. All
keep the task's constraints (width 4096, 200M samples, LR 3e-4, K = 25).

1. **Reproduce on v1** (7 configs x 3 seeds = 21 runs), checked against the post's 0.97 / 0.84 and the
   published 0.878 baseline.
2. **Corrected benchmark v2** (21 runs).
3. **Fresh draws** of the v2 configuration with three new world seeds: same statistics, new features,
   hierarchy and correlations (3 worlds x 7 configs x 2 seeds = 42 runs).
4. **Shifted worlds**, one factor at a time from v2: hidden size 512 and 1024, Zipf exponent lower and higher,
   correlation scale 0 and 0.3 (6 worlds x 3 configs [recipe, baseline, recipe without LISTA] x 2 seeds = 36
   runs). The recipe is also run at eta = 0.1 in each (6 runs), to separate "LISTA fails" from "eta was tuned
   to v1".
5. **Bussmann's refinement** applied at inference to every trained SAE, threshold tuned on v1 only.
6. **Probe ceiling** per world, so gains are reported as the fraction of the baseline-to-ceiling gap closed.
7. **One real-LLM check, secondary.** On gemma-2-2b layer 12, train the recipe, the recipe without LISTA, and
   the recipe at eta = 0.1 (2 seeds each, 6 runs) at the 300M-token setting of the public Matryoshka panel;
   evaluate with sae-probes only against the panel's seeded baselines. Runs only if steps 1-5 finish on day 1.

Key analysis: gain retained = (recipe - baseline) in a held-out world divided by the same difference on v1,
for F1 and MCC, with worlds as the unit. A component table gives the F1 change from removing each part, per
world family. Pre-registered reading: "world-specific" if mean retained F1 gain on fresh draws is below 50%;
"robust" if above 80% on fresh draws and above 50% on at least four of six shifted worlds.

## 4. Stage 1 cost estimate
The post gives about 20 minutes per SAE on an unnamed GPU; we budget 30.
- Synthetic runs: 126 x 0.5 h = 63 GPU-hours. L40S at $0.79/h would be $50; H100 at $2.89/h (RunPod pricing
  pages via web search, 2026-11-14) is $182. We budget the H100 figure.
- Probe ceilings and refinement sweeps: 5 GPU-hours, $15.
- gemma-2-2b check: 6 runs x about 3 h on an H100 (my estimate, timed on the first run) = $52; sae-probes
  evaluation, 4 h = $12.
- Margin for reruns (about 25%): $69.
- **Total $330.**

## 5. What success looks like
A figure with one row per world (v1, v2, three fresh draws, six shifted worlds) showing baseline, recipe and
probe ceiling, with a headline number for the gain retained off v1. A component table says which parts help
everywhere, help only on v1, or hurt under shift, and whether Bussmann's refinement stacks.

Each outcome is reportable. "Holds everywhere" answers Conmy's objection for this case. "Holds on fresh draws
but collapses under more superposition" tells practitioners where the recipe is unsafe and matches the
author's LLM difficulty. "Collapses on v2" means the agent exploited the upload error. A null on the LLM check
is expected to be ambiguous, since sae-probes separates same-family variants poorly; it is reported as such
and kept out of the headline. If step 1 fails to reproduce the post, the finding is a diagnosed reproduction
failure of a public recipe.

## 6. Stage 2 (if stage 1 succeeds)
- Re-run the autoresearch loop with the indicated fix: the agent sees a training suite of worlds and is scored
  on hidden ones; a second agent searches for benchmark parameters that break the recipe (Bussmann's
  suggestion). About $1,500.
- A properly powered LLM evaluation of the surviving components (several layers, 3+ seeds, 1B+ tokens): about
  $1,000-2,000, the figure the author quotes.

## 7. Risks and how the plan handles them
- **The released code does not reproduce 0.97.** Step 1 is the gate and uses the author's own
  `train.py default` command; a mismatch is diagnosed before continuing.
- **Runs are slower than budgeted.** Time the first run; above 45 minutes, drop to 2 seeds on v1 and v2 (seed
  SD is 0.002) and cut two shifted worlds.
- **Shifted worlds change the right L0.** Report gap-closed against each world's own baseline and ceiling;
  add an L0 sweep only where both recipe and baseline degrade.
- **The author has these results privately.** Possible; none is public, and independent replication on
  held-out worlds still has value.
- **The LLM step eats the budget.** It is last, gated, capped, and excluded from the headline.
- **Over-claiming.** Worlds, not seeds, are the unit (3 fresh, 6 shifted); no claims about LLM SAEs.
