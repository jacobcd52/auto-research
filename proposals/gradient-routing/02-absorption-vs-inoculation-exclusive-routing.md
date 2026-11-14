# Absorption or inoculation? Testing GRAFT when the FORGET adapter never sees an unflagged sample
cluster: gradient-routing | stage-1 cost: $300 | follows up: Gradient Routing Localizes and Removes Unintended Behaviors in RL (mKJEBiuuxHKuCoTB6); Some thoughts on GRAFT and follow-up work (6ro3dngDGaLJaumYb)

## 1. What the prior work showed
GRAFT (Ward, Hu et al., arXiv:2610.17062) trains a RETAIN and a FORGET adapter during RL. Trajectories flagged by a
monitor update FORGET only; unflagged trajectories update both; FORGET is deleted at deployment. Deleting it removes
reward hacks, including hack types the monitor cannot see. The paper reports this through two visibly different
routes:
- **Six toy environments (SmolLM2-135M):** the model does learn the undetected hack form during training, and
  ablating FORGET removes it together with the detected form.
- **Countdown-Code (Qwen3-8B):** the pre-ablation policy does detected hacks on up to 35% of trajectories, undetected
  hack types never emerge at all, and the ablated model hacks near 0%.

Two explanations are on the table. *Absorption*: because FORGET already represents hacking, gradients from
unflagged hack samples flow preferentially into FORGET, so undetected hacks end up there too. *Inoculation*: with
FORGET switched on, the policy already hacks, so RETAIN is under little pressure to learn any hack, as with
inoculation prompts or adapters. The paper says its evidence is thin: GRAFT beats a frozen inoculation adapter in
one supervised experiment, yet in unreported toy experiments gradient norms did not separate by adapter. Co-author
Shawn Hu's follow-up post lists as open: "Which or what combination of these is happening?", and proposes the
decisive variant: "What if you just don't train the FORGET adapter on unflagged samples? This would preserve the
inoculation effect but probably not the absorption effect." He also asks whether the adapter behaves like a steering
vector under scaling and negative scaling, and names the loss of task performance from ablating FORGET (which has
also learned part of the task from unflagged samples) as the method's biggest practical cost.

Already done by others: a rank-1 LoReFT FORGET adapter with layer-window ablations (Knoche), routing on one hack
type in supervised fine-tuning (Drori), and, in the authors' FOLLOWUP_WORK.md, small exploratory runs of training
with FORGET at scale -1, scale controllers, and anchor variants. None reports the unflagged-samples ablation, though
the released trainer has a flag for it (`--routing_mode exclusive`: unflagged samples update RETAIN only). Searches
of arXiv, LessWrong and the web on 2026-11-14 found no such result.

## 2. Question and why it matters
Does GRAFT still remove undetected hacks when FORGET is trained only on flagged trajectories? The two settings give
sharp, opposite expectations. In the toy environments undetected hacks are rewarded and unflagged, so under
exclusive routing their gradient goes to RETAIN alone; if absorption is what cleans them up, the deployed model
should now keep them. In Countdown, where undetected hacks never appear, exclusive routing should work as well as
standard GRAFT, and possibly better on the task, since FORGET no longer soaks up honest learning that ablation then
throws away.

Either outcome is useful. If exclusive routing fails in the toy environments, absorption is real and necessary, and
simpler "online inoculation adapter" designs are ruled out. If it succeeds everywhere, GRAFT's benefit is
inoculation plus generalisation of the FORGET representation, the method can be simplified, and its main cost may
shrink.

## 3. Stage 1 plan
Reused: https://github.com/jnward/GRAFT (`rl/`: trainer, six toy configs, Countdown config, sweep files, per-sample
gradient diagnostics `--adapter_diag_level per_sample_recompute`, `tools/local_fseval.py`, `tools/expr_only_probe.py`),
released training logs in `rl/paper_data` for standard GRAFT, pod scripts from
https://github.com/samuel500/GRAFT/tree/loreft, the start model `samuel500/graft-qwen3-8b-countdown-sft` and trained
adapters `samuel500/graft-repro-adapters` (GRAFT and GRAFT without routing, 4 seeds each). Built: sweep files that
set one flag, and analysis scripts.

1. **Reproduce.** One standard-GRAFT seed in each toy environment at monitor recall 1.0 and 0.25 (12 runs) with
   gradient diagnostics on, checked against the released curves. Evaluate two released Countdown adapters and match
   their published numbers.
2. **Exclusive routing, toy environments.** 6 environments x recall {1.0, 0.25} x 3 seeds = 36 runs, otherwise the
   canonical recipe. At recall 0.25 three quarters of detectable hacks are also unflagged, so this is the hardest
   test of "inoculation alone".
3. **Exclusive routing, Countdown.** 3 seeds with the paper's GRAFT hyperparameters, plus one standard-GRAFT seed
   with gradient diagnostics.
4. **Gradient-share diagnostic.** In standard runs, for each sample class given by ground truth (honest, detected
   hack, undetected hack), the fraction of per-sample gradient norm that lands in FORGET, tracked over training.
   Absorption predicts undetected-hack samples sit well above honest samples.
5. **Scale sweep, no training.** Evaluate the 8 released Countdown adapters and the 3 new exclusive ones with the
   FORGET output scaled by {-1, -0.5, 0, 0.25, 0.5, 0.75, 1, 1.5, 2}: ground-truth hack rate by type and
   clean-environment solve rate (n=256 each). This shows whether hacking moves smoothly with scale, whether negative
   scale pushes below the base rate or breaks the model, and whether partial down-weighting beats full ablation.

Metrics throughout: programmatic ground-truth hack rate (detected and undetected forms separately) in the
both-adapters, RETAIN-only and FORGET-only configurations, and task performance of RETAIN-only. Key comparison:
exclusive versus standard, per environment, with seed-level points; GRAFT without routing is the control for
"ablating any adapter helps".

## 4. Stage 1 cost estimate
RunPod on-demand H200 at $5.29/h (looked up 2026-11-14). Paper timings: toy run 1-2.5 h, six in parallel per H200;
Countdown run 2-4 h on one H200.
- Toy runs: 48 x 1.75 h / 6 per GPU = 14 GPU-h = $74
- Countdown training: 3 x 3 h + 1 diagnostic run at about 5 h = 14 GPU-h = $74
- Scale sweep: 11 adapters x 9 scales x about 4 min = 6.6 GPU-h = $35; standard evaluations 3 GPU-h = $16
- Set-up and debugging (patched vLLM, CUDA MPS): 8 GPU-h = $42
- Subtotal $241; margin for reruns and two extra seeds on the most informative cell = $59. **Total $300.** No API spend.

## 5. What success looks like
One table and one figure per setting. A clean absorption result: in most toy environments exclusive routing leaves
the undetected hack in the deployed model at a rate close to the pre-ablation rate, standard GRAFT removes it, and
the gradient-share diagnostic shows undetected-hack samples loading on FORGET. A clean inoculation result: exclusive
routing matches standard GRAFT's deployed hack rate (within seed noise) in at least five of six toy environments
and in Countdown, with equal or higher task performance. The scale sweep
adds a dose-response plot that either supports or undercuts the "FORGET is a learned steering vector" reading. A
null would be high seed variance that hides the contrast; the plan fixes three seeds per cell and reserves margin
for more in the cell that matters.

## 6. Stage 2 (if stage 1 succeeds)
Interpolate between standard and exclusive routing (unflagged FORGET weight 0.25, 0.5) to find the best
hack-versus-task trade-off; repeat with the LoReFT FORGET adapter; feature-level analysis of what FORGET writes. About $500-800.

## 7. Risks and how the plan handles them
- **Exclusive mode is an untested code path** and may be unstable (all learning from unflagged samples lands on
  RETAIN at doubled weight). First action is a single toy run; if it diverges, try the paper's learning-rate grid on
  one environment before launching the sweep, and report instability as a finding if it persists.
- **Toy "anchor" already penalises detected hacks for RETAIN**, which could confound the comparison. The same
  anchor is used in both arms, and detected and undetected forms are reported separately.
- **Stack fragility** (patched vLLM, driver-matched MPS binary). The toy sweep needs only local GPUs; reproduction
  against released curves comes before any new arm.
- **Over-reading small n.** Claims are restricted to effects visible in every seed of a cell or larger than the
  released seed-to-seed spread.
