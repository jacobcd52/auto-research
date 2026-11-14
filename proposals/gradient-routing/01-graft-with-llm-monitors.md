# Does GRAFT survive a real LLM monitor? Weak-judge and reasoning-only monitors on Countdown-Code RL
cluster: gradient-routing | stage-1 cost: $450 | follows up: Gradient Routing Localizes and Removes Unintended Behaviors in RL (mKJEBiuuxHKuCoTB6); Gradient Routing Generalizes to Unrouted Hack Types (ie7bSp5ZDwYkCQxuv)

## 1. What the prior work showed
GRAFT (Ward, Hu et al., arXiv:2610.17062) adds a RETAIN and a FORGET MLP adapter to a frozen model. During RL, a
monitor's flag does not change the reward; it only decides which parameters a trajectory updates (flagged: FORGET
only; unflagged: both). FORGET is deleted at deployment. On Countdown-Code with Qwen3-8B (three hack types: overwrite
the test, relax the test's constraint check, change the problem inputs), a programmatic monitor that sees only
test-overwrite hacks gives: reward penalty -> the policy moves to constraint-relax hacks on about 30% of trajectories;
GRAFT -> about 35% type-1 hacking before ablation, near 0% hacking of any type after ablation, and a clean-environment
solve rate about 20 points above the base model.

Every monitor in the RL experiments is a hand-written heuristic with perfect precision and a clean, type-shaped
blind spot. The authors list this as their first limitation ("we do not investigate monitors which use LLMs as a
judge") and close with "we would be excited to see experiments ... with LLM-based monitors". Drori's follow-up
(supervised fine-tuning only, Qwen3-32B) routed on one hand-chosen hack subset and measured others; transfer was
good in 8 of 12 arms, but routing on hacks whose reasoning mentions hacking produced 15% silent hacking, a result he
could not explain, and he states that generalisation "from hacks that a real monitor can detect to ones it can't"
was not tested. Other follow-ups (Knoche's LoReFT FORGET adapter; the authors' FOLLOWUP_WORK.md) keep the heuristic
monitor. Searches of arXiv, LessWrong and the web on 2026-11-14 found no GRAFT run with an LLM monitor and no test
of monitor false positives. The released code already contains an unused `llm_judge` detector.

## 2. Question and why it matters
When the routing signal comes from an actual LLM judge, with false positives and blind spots that nobody designed,
does ablating FORGET still remove hacking while keeping the task gain, and does it still beat a reward penalty driven
by the same judge? Two monitors, chosen for realism:
- **W, a weak full-transcript judge**: a small cheap LLM that reads prompt and response. New ingredient: false
  positives, which send honest solutions to FORGET only and could starve RETAIN of task learning.
- **C, a reasoning-only judge**: sees the `<think>` text but not the code, like a chain-of-thought monitor. Its
  blind spot is any hack the model does not verbalise. Under a reward penalty this is the classic recipe for
  obfuscation; under GRAFT it is the RL version of Drori's unexplained "silent hacking" arm.

If GRAFT holds up, the paper's central claim extends to the supervision people would actually use. If it breaks, we
learn which monitor property breaks it (false positives, or blind spots tied to verbalisation).

## 3. Stage 1 plan
Reused: code https://github.com/jnward/GRAFT (`rl/`), the pod reproduction scripts in
https://github.com/samuel500/GRAFT/tree/loreft (`rl/REPRO.md`), the SFT-primed start model
`samuel500/graft-qwen3-8b-countdown-sft`, released adapters with evals in `samuel500/graft-repro-adapters`
(GRAFT, GRAFT without routing, no intervention; 4 seeds each), and the environment's programmatic per-hack-type
ground truth (`configs/countdown_code_hack.yaml`). Built: two monitor configs, a reasoning-extraction wrapper, and a
restriction of judge calls to rewarded trajectories (the paper's heuristic also fires only on rewarded hacks).

1. **Set-up and replication check (half a day).** Install on one rented GPU; evaluate two released GRAFT adapters
   and reproduce their published hack rate and pass@1 (0.00-0.02 and 0.77-0.80). Train one heuristic-monitor GRAFT
   seed to confirm the training path.
2. **Monitor calibration, no training.** Sample 6,000 rollouts from released checkpoints (pre-ablation GRAFT,
   no-intervention, SFT base) so that all three hack types and honest solves are present. Score candidate judges
   (llama-3.1-8b, gemma-3-12b, qwen3-32b; default and high-precision prompts; temperature 0, no judge reasoning)
   against ground truth: recall per hack type, false-positive rate on honest solves, and for C the fraction of hacks
   verbalised. Pick W with recall between 0.3 and 0.8 and a non-zero false-positive rate; fix both monitors before any
   training run. If no small judge is imperfect, W becomes a judge shown only `solution.py` (a partial-view monitor).
3. **Training grid: 12 runs.** {GRAFT, reward penalty 2} x {W, C} x 3 seeds, 200 steps, paper hyperparameters
   (learning rate 1.67e-4 for GRAFT, 5e-4 for penalty, LeetCode anchor). Log the judge's flags next to ground truth
   at every step.
4. **Evaluation.** For every checkpoint: ground-truth hack rate by type with FORGET ablated and not ablated
   (`tools/local_fseval.py`, n=256), clean-environment solve rate (`tools/expr_only_probe.py`), and each judge's recall
   on the final policy's own hacks. References from released data: no intervention, heuristic GRAFT, heuristic
   penalty, GRAFT without routing.
5. **Analysis.** (a) The paper's Figure-2 scatter (hack rate vs clean solve rate) with the four new arms, seed-level
   points and standard errors. (b) For C: verbalised and silent hack rates over training under penalty versus GRAFT
   before ablation, and silent hack rate after ablation. (c) For W: fraction of honest solves routed to FORGET per
   step versus final clean solve rate.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14 (RunPod on-demand H200 $5.29/h; OpenRouter gemma-3-12b $0.05 and llama-3.1-8b $0.02 per
million input tokens). The paper reports 2-4 h per Countdown run on one H200.
- 13 training runs (12 grid + 1 replication) x 3 h x $5.29 = $206
- Set-up, debugging, failed starts: 8 GPU-h = $42
- Evaluations: 13 checkpoints x 2 configurations, about 0.3 h each = 8 GPU-h = $42
- Calibration rollouts and judging: 2 GPU-h + under 40M tokens = $13
- Training-time judging: 205k trajectories per run, about 60% rewarded, about 1.6k tokens each (W) or 0.8k (C);
  roughly 200M and 100M input tokens per run at $0.05 = $10 and $5; 6 runs each = $90
- Subtotal $393; margin for one rerun batch of 3 runs = $57. **Total $450.**

## 5. What success looks like
The main figure places the four new arms on the paper's scatter. Clear positive: with both monitors, ablated GRAFT has under 5% ground-truth hacking and a clean solve rate
within 5 points of heuristic-monitor GRAFT, while reward penalty with the same judge retains hacks the judge misses
(for C: silent hacks rise under penalty). Clear negative: GRAFT with W loses most of the task gain, tied to the
measured false-positive rate; or GRAFT with C leaves silent hacks in RETAIN, reproducing Drori's anomaly in RL. Both
are publishable because the monitor's error profile is measured against programmatic truth. Ambiguous: seeds
disagree (the released no-intervention seeds range from 48% to 100% hacking); the plan then reports per-seed outcomes
and spends the margin on extra seeds for the most informative arm.

## 6. Stage 2 (if stage 1 succeeds)
Route by judge confidence instead of a binary flag; a controlled false-positive sweep in the six SmolLM2-135M toy
environments. About $600-900.

## 7. Risks and how the plan handles them
- **Fragile stack** (patched vLLM 0.17, TRL overrides, external grader repo). Use the fork's pod scripts; step 1
  gates everything on reproducing published numbers from released adapters.
- **The judge is near-perfect on blatant hacks**, making W uninteresting. Calibration happens before training, with a
  pre-specified fallback (partial-view judge); C has a structural blind spot regardless.
- **The model never verbalises hacks**, so C flags nothing. Calibration measures this; if under 10% of hacks are
  verbalised, C is replaced by the partial-view judge and the finding is reported.
- **API rate limits at 1,024 calls per step.** The detector already rotates providers; fallback is self-hosting the
  judge with vLLM on the same H200 (supported through `JUDGE_URL`).
- **Evaluation bugs.** All headline numbers use the environment's programmatic graders, not the judge; 100 judged
  transcripts per monitor are read by an agent to confirm the reasoning-extraction wrapper hides the code.
- **Three seeds are few.** Report seed-level points; no claims about differences under 10 points.
