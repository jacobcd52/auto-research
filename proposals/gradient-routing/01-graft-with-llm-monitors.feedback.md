# Feedback: "Does GRAFT survive a real LLM monitor?" (gradient-routing / 01)

Verdict: **keep with tweaks.** It is the most obvious follow-up to the 218-karma post and the infrastructure is real.
Three things need fixing before it is funded: a learning-rate confound that has already been called out publicly, a
weak-judge arm whose most likely outcome is uninformative, and a novelty claim that is stronger than the evidence.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Paper results (penalty -> ~30% type-2 hacks; GRAFT ~35% type-1 pre-ablation, ~0 after, ~20pp over base) | Confirmed against the post and arXiv:2610.17062 HTML. |
| Authors list LLM monitors as first limitation and ask for it | Confirmed (quotes are accurate). |
| Drori: 8/12 arms, 15% silent hacking in "Hacky reasoning", real-monitor generalisation untested | Confirmed. Note Drori himself suspects that arm is broken (its CEILING has zero invisible hacks), so "reproducing Drori's anomaly" is a weak hook. |
| `llm_judge` detector exists in `rl/rh_detectors.py`, with the two prompts and P/R comment | Confirmed (fetched from raw.githubusercontent.com). Defaults `require_thinking=True`, `temperature=0.7`, `max_tokens=4096` do need overriding. |
| `samuel500/graft-qwen3-8b-countdown-sft` and `samuel500/graft-repro-adapters` are public | Confirmed via HF API (not gated). Adapters: GRAFT lr/3 and lr 5e-4, GRAFT w/o routing lr 5e-4, five no-intervention variants, 4 seeds each. |
| Released GRAFT adapters: hack 0.00-0.02, pass@1 0.77-0.80 | Confirmed (REPRO.md: 0.011 +/- 0.004, 0.786 +/- 0.007). |
| "Heuristic penalty" reference from released data | **Not in the HF adapter repo.** No reward-penalty checkpoints are released there (the `..._reward_penalty_amountmissing_...` runs are no-intervention). Only the paper's figure inputs (`paper_data/paper_fig_inputs.tar.gz`) could supply penalty numbers; I did not open the tarball. Penalty rollouts for calibration cannot be sampled from released checkpoints. |
| Prices: H200 $5.29/h; gemma-3-12b $0.05, llama-3.1-8b $0.02 per M input | OpenRouter confirmed today. H200 price matches what Knoche paid (REPRO.md); I did not re-fetch runpod.io. |
| "205k trajectories per run" | **Wrong, by 4x.** `max_steps: 200` is optimizer steps; the sweep comment says "= 50 rollout phases" (4 optimizer steps per 1024-rollout batch). A run has ~51k task trajectories. Judge spend is about a quarter of the estimate. |
| "No GRAFT run with an LLM monitor" | **Overstated.** Nothing is published, but shawnghu says in the GRAFT post's comments that "in an earlier experiment with a toy env using an LLM judge ... we were also able to bring the rate of hacking below that of the pre-RL model". `train.py` also ships judge FP/FN diagnostics (`judge/fp_rate`, keyed to a LeetCode ground-truth channel), a `warmup_rh_detector`, and vLLM judge-port plumbing. The authors have clearly run this internally. |

Search for prior work: the web-search tool was out of budget for this session, so I relied on the arXiv API
("gradient routing", newest 25, to 2026-11-03), a title scan of the 600 newest LessWrong posts back to 2026-10-18, the
GRAFT post's comment thread, and the follow-up posts. Nothing published does this experiment. A general web search
was not done and should be repeated by the reviser.

## 1. Would it get upvoted?

Plausibly, but it is closer to a coin flip than the proposal implies. The cluster's follow-ups scored 68 (Drori), 63
(shawnghu's notes) and 38 (Knoche's LoReFT post, which had 8 seeds, a full reproduction and a new adapter). A
competent follow-up from an unknown author on this topic lands at 35-70. This one targets the headline limitation, so
it sits at the upper end if the result is crisp.

What decides it:
- A **failure mode tied to a measured monitor property** ("GRAFT with a CoT-only monitor leaves X% silent hacks in
  RETAIN", or "an FP rate of Y% costs Z points of task gain") would clear 50 comfortably.
- "GRAFT still works with a small LLM judge, and reward penalty with the same judge visibly teaches evasion" also
  clears 50.
- "GRAFT still works, and so does reward penalty" is the most likely single outcome for the weak-judge arm (see
  section 3) and reads as a 30-45 karma confirmation.

Readers who care: the GRAFT authors, people working on training-time monitoring and CoT monitorability, and the
commenters who asked how GRAFT trades off against penalising with the same monitor (williawa, Oz Amram).

## 2. Naturalness

Mainline. The authors' first limitation, their closing sentence, and Drori's "what we actually care about" all point
here. That is also the risk: the authors have the judge detector, FP/FN logging and an earlier unpublished toy result,
so a fuller version from them within weeks is likely. This argues for doing it now and keeping it small, and for
choosing an angle the authors are less likely to have (the reasoning-only monitor, C) as the centrepiece.

The proposal's section 1 should be corrected to say "no published result; the authors report an unpublished toy-env
LLM-judge run".

## 3. Pre-mortem

How the two days go. Setup on a pod using Knoche's scripts works within half a day (he documents 2.6-4 pod-hours per
seed including setup, smoke test and evals; three of his pods died on slow downloads in one region). Calibration is
cheap and fast. Training 12-13 runs needs 3-4 pods in parallel to fit in the remaining ~1.5 days; that is feasible but
leaves almost no room for a second iteration, so the monitor choice made at calibration is final.

Forecast:
- Clear positive with contrast (GRAFT holds for both monitors, penalty with the same judge retains or hides hacks): **20%**
- GRAFT holds but penalty with the same judge is also fine, so no contrast: **25%**
- Clear, interesting negative (FP starvation or silent hacks left in RETAIN): **15%**
- Ambiguous (seed variance, monitors end up degenerate, confounded comparison): **28%**
- Fails to run or to finish the grid: **12%**

Specific reasons it under-delivers:

1. **Learning-rate confound, already public.** The plan uses "paper hyperparameters": 1.67e-4 for GRAFT, 5e-4 for
   penalty. Knoche's top comment on the GRAFT post (and REPRO.md section 2-3) shows that this lr gap accounts for
   most of the difference between no-intervention and GRAFT-w/o-routing (no-intervention hacks 0.79 at 5e-4 and 0.37
   at lr/3), and that GRAFT at 5e-4 loses its capability gain (pass@1 0.51, one seed collapsed). Jake Ward
   acknowledged it. Any GRAFT-vs-penalty comparison at mismatched lr will be dismissed in the first comment.

2. **The weak-judge arm (W) is likely a non-event.** A full-transcript LLM judge is not type-blind: it will catch
   some of all three hack types. With penalty 2 and recall r spread over types, a hack's expected reward is 1 - 2r,
   which is below the honest solve rate (~0.56) once r exceeds roughly 0.25. So penalty probably just suppresses
   hacking, and there is no monitor-exploiting policy for GRAFT to beat. The paper's limitation (ii) says the
   environments were chosen so that penalty fails; a realistic judge removes that property. On the GRAFT side,
   random low recall is already covered by the paper's toy recall sweep, and a few percent of false positives sending
   honest solves to FORGET at 2x weight is unlikely to move pass@1 by more than seed noise. The expected W result is
   "both methods fine".

3. **Selecting W on a recall band re-introduces a designed monitor.** "Pick W with recall 0.3-0.8 and non-zero FP"
   chooses the error profile by hand, which undercuts "blind spots nobody designed". The per-type recall profile of
   whichever judge is chosen matters more than the aggregate and must be reported.

4. **Monitor C depends on an unverified fact: whether this policy verbalises hacks.** The policy runs with
   `enable_thinking=False` and writes its reasoning inside literal `<think>` tags in the response (the SFT data is an
   o4-mini distillation set in that format), so extraction is feasible. Whether the think text mentions test
   tampering, at step 0 and after hacking is learned, is unknown. If hacks are already silent, C flags nothing and
   GRAFT-C equals GRAFT-w/o-routing, for which released numbers exist (hack 0.22 at lr/3). The proposal has a
   fallback for this, which is good, but the fallback (code-only judge) is just a weaker W.

5. **Calibration distribution mismatch.** Calibrating on rollouts from heuristic-trained checkpoints does not predict
   judge behaviour on the policies that emerge when the judge itself shapes training. The plan logs flags against
   ground truth at each step, which covers it; the write-up should lead with the in-training curves, not the
   calibration table.

6. **Power.** Penalty and no-intervention arms are bimodal across seeds (0.41 to 0.98 for the same config). Three
   seeds cannot support "penalty retains ~X% hacks". GRAFT's deployed numbers are tight (SEM 0.004 on hack rate, 0.007
   on pass@1 over 4 seeds), so breakage of GRAFT of 10+ points is detectable with 3 seeds; differences between the
   penalty arms are not.

7. **Small implementation traps.** (a) The detector receives `batch_decode(..., skip_special_tokens=True)` text;
   confirm `<think>` tags survive decoding before building the reasoning extractor. (b) The detector is called on the
   full batch and masked afterwards (the code has a TODO about wasted API calls); restricting to rewarded samples is a
   real code change in the trainer, not a config. (c) The reward-penalty path and the routing path both read the same
   `rh_detector`, but in-training evals and `local_fseval.py` may also invoke it; make sure eval never calls the paid
   judge. (d) Unparseable judge replies default to "not flagged", which silently lowers recall under rate limiting;
   log the unparseable count per step. (e) One failed judge batch asserts and kills a 3-hour run; self-hosting the
   judge on the same H200 competes with vLLM memory set at 0.7.

8. **Already-known either way?** A positive result is what most readers expect after Drori's post; a negative result
   on C would be new. The proposal should be honest that the positive outcome is confirmatory.

## 4. Cost check

The estimate is in the right range, with two offsetting errors.
- GPU: Knoche's measured 2.6-4.1 pod-hours per seed already includes evals. 13 runs x ~3.4 h x $5.29 = ~$235, plus
  ~10 h of setup, calibration sampling and failed starts = ~$53. The separate $42 evaluation line is double-counted.
- Judge: ~51k trajectories per run, not 205k. At 1.6k tokens that is ~80M input tokens per W run and ~40M per C run,
  about $4 and $2 at $0.05/M. All twelve runs: under $25, not $90. Calibration: under $5.
- My estimate for the plan as written: **$320-380** including one rerun batch. That leaves room for the 3-4 extra runs
  recommended below while staying under $450. A cheaper GPU does not help much: 80 GB cards work for eval with a
  smaller batch, but the training settings are tuned for the H200.

## 5. Recommended changes (in priority order)

1. **Match the learning rate.** Run reward penalty at lr 1.67e-4 with the LeetCode anchor (the same recipe as GRAFT,
   routing off, penalty on), and cite Knoche's lr analysis. If budget allows only one penalty configuration, use the
   matched one; keep the paper's 5e-4 penalty as a secondary arm for monitor C only. Report GRAFT pre-ablation as well
   so that readers can see what the judge did to training.

2. **Make the reasoning-only monitor the centrepiece and give it the seeds.** Suggested grid (15-16 runs, ~$420):
   GRAFT-C x 4, penalty-C matched-lr x 4, penalty-C at 5e-4 x 2, GRAFT-W x 3, penalty-W matched-lr x 2-3. Headline
   plot: verbalised versus silent ground-truth hack rate over training for penalty-C and GRAFT-C, and silent hack rate
   after ablation. State in advance what counts as obfuscation (silent hacks rising above the no-intervention silent
   rate).

3. **Add a go/no-go gate after calibration, before any training spend.** Measure on base and no-intervention
   rollouts: fraction of hacks verbalised, per-type recall and honest-solve FP rate for each judge. If under ~10% or
   over ~95% of hacks are verbalised, C is degenerate; if W has under 1% FP and over 90% recall on every type, W is the
   heuristic monitor with extra steps. In either case switch that arm to recommendation 4 instead of the code-only
   fallback.

4. **Add a controlled false-positive arm in stage 1, not stage 2.** A wrapper that flags a fixed fraction of honest
   rewarded solves (for example 20% and 50%) on top of the heuristic monitor is a few lines and gives the dose-response
   that a single natural judge cannot. Two or three runs at a high FP rate tell readers whether FP starvation exists
   at all; without it, a null result on W is uninterpretable. This can replace the W-penalty runs if budget is tight.

5. **Do not pick W by a target recall band.** Use one named cheap judge with the repo's default prompt, unchanged, and
   report its error profile. If it is too good, that is the finding for W ("an 8B judge is effectively a perfect
   monitor in this environment") and the FP question moves to the synthetic arm.

6. **Fix the factual items.** Correct the novelty statement (authors' unpublished LLM-judge toy run); remove
   "heuristic penalty" from the list of released references or verify it is in the paper's figure-input tarball; fix
   the trajectory count; drop the double-counted eval line.

7. **De-risk the run loop.** Self-host nothing; use OpenRouter with a fixed provider and `require_thinking=False`,
   temperature 0, `max_tokens` small. Cache judge verdicts keyed by transcript hash so a crashed run can resume
   without re-paying. Make judge failure degrade to "retry then skip the step's routing" with a logged counter rather
   than an assert. Verify on a 4-step smoke test that flags are non-trivial before launching the grid.

8. **Tone down the framing.** "Real LLM monitor" on a single-turn arithmetic toy with an 8B policy is one step more
   realistic, not realistic. Title the write-up after the finding, and put the monitor's measured in-training error
   profile next to every headline number.
