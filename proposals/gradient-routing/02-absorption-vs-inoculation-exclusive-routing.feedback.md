# Feedback: "Absorption or inoculation? Testing GRAFT when the FORGET adapter never sees an unflagged sample"

Verdict: **keep, with changes**. The experiment is cheap, public, unclaimed and explicitly requested by a co-author. Its
weak point is interpretation: as designed, the headline contrast does not isolate "absorption" the way the proposal
says, and its one direct diagnostic repeats something the authors already report as a null.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Paper arXiv:2610.17062 exists; toy envs learn undetected hacks pre-ablation; Countdown undetected types never emerge; "evidence for absorption is also weak", gradient norms "do not strongly separate by adapter" | Confirmed from the arXiv HTML (Section 7). |
| "Two explanations are on the table" | **Wrong count.** The paper names three: preempting exploration, inoculation, absorption. The proposal folds preemption into inoculation. This matters for the Countdown arm (see below). |
| Hu's post quotes ("Which or what combination...", "What if you just don't train the FORGET adapter on unflagged samples?...", steering-vector questions, task-performance cost) | Confirmed verbatim in post 6ro3dngDGaLJaumYb. |
| `--routing_mode exclusive` exists in the released trainer | Confirmed in `jnward/GRAFT` `rl/train.py` and `rl/advantages.py`. Masks at lambda=1, equal adapter sizes: unflagged (RETAIN 2, FORGET 0), flagged (0, 2). The RETAIN weight is a deliberate compensation (kappa_R = 2), not an accident. |
| `--adapter_diag_level per_sample_recompute`, `tools/local_fseval.py --scales` | Confirmed. `--scales` takes arbitrary floats, so negative and >1 values parse; whether the patched vLLM adapter path behaves at negative scale is untested. |
| FOLLOWUP_WORK.md has no exclusive-routing result | Confirmed (file is at `shawnghu/small-rl`, branch `master`, not `main`). It does report forget scale -1 at anchor/deploy working "comparably well", and a failed scale-controller. |
| `samuel500/graft-qwen3-8b-countdown-sft` and `samuel500/graft-repro-adapters` are public | Confirmed via the HF API. The adapter repo holds **12** relevant adapters (GRAFT lr1 x4, GRAFT lr/3 x4, GRAFT-without-routing x4), plus no-intervention runs; the proposal says 8. The paper's GRAFT setting is the lr/3 set. |
| RunPod H200 $5.29/h | Confirmed (Secure Cloud; Community Cloud is $3.59/h. H100 PCIe $2.89 / $1.99). |
| Paper timings (toy 1-2.5 h, 6 per H200 under MPS; Countdown 2-4 h) | Confirmed (paper hardware paragraph). The repo README says toy sweeps actually ran 3-5 per GPU. |
| Not already done | No published result found: arXiv API ("gradient routing", newest 25), LessWrong newest 700 posts back to 2026-10-13, comments on both GRAFT posts. **My web-search budget was exhausted, so I could not run a general web search**; treat "not done" as checked on arXiv and LessWrong only. |

Two things I found that the proposal does not use:

- Shawn Hu, in a comment on the main post: "Simple statistical ideas like looking at gradient norms on hacking samples
  didn't yield any signal clean enough to do anything useful with." Step 4 (gradient-share diagnostic) is essentially
  this.
- The exclusive code path ships with a size-derived compensation weight, a geometry guard and documentation. The authors
  built it carefully, which makes it likely they have unpublished exclusive runs. Scoop risk is real, not hypothetical.

## 1. Would it get upvoted?

Borderline, leaning yes if the result is clean. Reference points from the same cluster: the main post got 218, Drori's
light extension 68, Hu's thoughts post 63, Knoche's LoReFT follow-up 38. A mechanism ablation by non-authors sits in the
38-70 band. What pushes it over 50:

- a result with a practical consequence, e.g. "exclusive routing matches GRAFT on Countdown and recovers N points of
  clean solve rate" (this addresses what Hu calls the method's biggest practical cost), or
- an unambiguous failure in the toy environments with a mechanism story that survives the controls below.

What keeps it under 50: "works in some environments, not others, 3 seeds, we cannot say why", which is the single most
likely outcome as currently designed. The audience is narrow but engaged: the GRAFT authors, Drori, Knoche, people working
on inoculation adapters. They will read it critically, and the first comment will be the confound in section 3 below.

## 2. Naturalness

Mainline. It is the exact variant a co-author proposed, on the question the paper itself flags as open, using a flag that
already exists. Nobody has published it. No objection here. The scale sweep is a reasonable cheap add-on, though the -1
case is partly pre-empted by FOLLOWUP_WORK.md.

## 3. Pre-mortem

**The central problem: exclusive routing removes more than absorption.** In the toy environments the pre-ablation policy
samples undetected hacks because FORGET learned to produce them, and it learned that partly from unflagged samples.
Switching to exclusive routing therefore changes three things at once:

1. No gradient share goes to FORGET on undetected hacks (absorption, the intended manipulation).
2. FORGET can no longer learn the undetected form directly, so inoculation now depends entirely on generalisation from
   the detected form. Hu's "this would preserve the inoculation effect" holds only for that part. A failure of exclusive
   routing is equally well explained by "inoculation got weaker".
3. RETAIN's gradient weight on every unflagged sample doubles (kappa_R = 2). Undetected hacks are rewarded and unflagged,
   so RETAIN is pushed toward them twice as hard as in standard GRAFT, where it already receives weight 1.

Note also that to first order RETAIN's per-step gradient on an unflagged sample is the same whether or not FORGET is
updated too. "Absorption" can only show up through training dynamics (FORGET winning a race), which is hard to separate
from point 2. So the proposal's sentence "if exclusive routing fails in the toy environments, absorption is real and
necessary" does not follow. The reverse inference is sound: if exclusive routing succeeds, absorption is not needed.
The experiment is a one-sided test, and the informative side is the one I think is less likely in the toy environments.

**Other specific concerns.**

- *Toy anchor confound is larger than stated.* In the toy environments the anchor step samples from the RETAIN-only
  policy in the same environment with a reward penalty on flagged samples. That is a small reward-penalty baseline acting
  directly on RETAIN, and reward penalty alone is known to produce undetected hacks. Once RETAIN samples any undetected
  hack, the anchor reinforces it. Any small leak under exclusive routing can be amplified by the anchor, so a failure may
  be an anchor effect. "Same anchor in both arms" does not remove an interaction.
- *Countdown arm is predictable.* Undetected types never emerge there because of preempted exploration, which exclusive
  routing does not touch. "Exclusive works on Countdown" is the expected result and says nothing about absorption versus
  inoculation. Its value is purely practical (does task performance improve?), and with 3 seeds against released 4-seed
  arms the solve-rate difference must be large to show. Paper-level seed spread should be read off the released
  `fseval.json` files before committing.
- *Recall 0.25 under exclusive routing is close to a foregone failure.* Three quarters of detectable hacks go to RETAIN
  alone at double weight. I would expect RETAIN to learn the detected form outright. That is a result, but an unsurprising
  one, and it uses half the toy budget.
- *Degenerate dynamics.* FORGET trained only on hacks may drive the joint policy to hack on every sample, at which point
  everything is flagged and RETAIN stops learning (the paper describes this failure). Exclusive routing makes this more
  likely. It would look like "low hack rate, no task learning" and must be reported as its own category.
- *Gradient-share diagnostic.* The authors tried it and saw no clean separation. Adam's per-parameter normalisation and
  the split-moment optimiser make raw gradient-norm share a poor proxy for update share. Expect a null here.
- *Small n.* 3 seeds per cell across 6 heterogeneous environments. The paper notes one environment (addition) flips to
  about 60% hacking just from swapping which form is detectable, so environment-level heterogeneity is large.
- *Infrastructure.* CUDA MPS needs a driver-matched binary and a daemon; this is not guaranteed inside a rented
  container. Countdown needs vLLM 0.17.0 with three patched files. Knoche's pod scripts lower this risk substantially.
  Negative forget scales through the patched vLLM path are untested.
- *Wall-clock.* 48 toy runs at 6 in parallel is about 16 h on one GPU; four Countdown runs are about 14 h in sequence.
  This fits in two days only with at least two pods running concurrently from day one.

**Forecast.**

| Outcome | Probability |
|---|---|
| Clear, interpretable result (exclusive succeeds broadly; or fails and the controls pin down why) | 30% |
| Clear negative that is still interesting (exclusive fails in most toy envs, works on Countdown, mechanism left open) | 25% |
| Ambiguous mush (environment-by-environment mix, seed noise, confounds unresolved) | 30% |
| Fails to run to completion (stack, MPS, divergence in the exclusive path) | 15% |

Most likely actual outcome: exclusive routing matches GRAFT on Countdown with a modest, noisy task-performance change,
leaks undetected hacks in several toy environments at recall 1.0, collapses at recall 0.25, and the gradient diagnostic
shows nothing. That write-up is worth roughly 30-50 karma unless the controls below turn the toy failure into a
mechanism claim.

## 4. Cost check

The estimate is realistic and probably slightly high per GPU-hour, slightly low on debugging.

- Toy runs do not need an H200. SmolLM2-135M fits many times over on an A100 or H100 (about $2-3/h). If MPS will not
  start, plain multi-process sharing on one card still works, at lower throughput.
- Countdown runs fit on 80 GB cards with `--gen_batch_size 64` (repo note), so H100 at $2.89/h is an option, with some
  slowdown.
- Per-sample-recompute diagnostics on Qwen3-8B may cost more than the 5 h allowed; I would drop that run (see below).
- Set-up at 8 GPU-h is thin for a patched-vLLM stack; allow 12-15.

My estimate for the plan as written: **$250-350**. With the changes below (extra control arms, fewer recall-0.25 runs):
**about $300-380**. Comfortably under the $500 cap either way.

## 5. Recommended changes (most important first)

1. **Add the controls that make a toy failure interpretable.** Without them the headline claim is not supported.
   - Exclusive routing with RETAIN weight 1 instead of the compensated 2 (set lambda/kappa or patch one line), to remove
     the doubled-learning-rate explanation.
   - Standard GRAFT with RETAIN weight 2 on unflagged samples, if the code allows it cheaply; the mirror-image control.
   - A frozen-FORGET arm: take a FORGET adapter from a finished standard run (which already produces both hack forms),
     freeze it, and train a fresh RETAIN adapter on unflagged samples only. This is "full inoculation, zero absorption".
     Together with exclusive routing ("inoculation from detected hacks only, zero absorption") it separates points 1
     and 2 above. This is also the online-versus-fixed inoculation adapter comparison the paper only has in SFT.
   Pay for these by cutting recall 0.25 to two environments, or dropping it.
2. **Rewrite the inference in sections 2 and 5.** State the test as one-sided: success of exclusive routing rules out
   absorption as necessary; failure is ambiguous unless the controls discriminate. Name all three mechanisms from the
   paper and say plainly that the Countdown arm tests the practical trade-off, not the mechanism.
3. **Make the Countdown arm earn its place.** Pre-register the comparison (clean solve rate and ground-truth hack rate
   of the deployed model versus the 4 released lr/3 GRAFT seeds, same eval script, same n). Read the seed spread from the
   released `fseval.json` first; if 3 seeds cannot resolve a 5-point difference, run 4 and drop the Countdown diagnostic
   run to pay for it.
4. **Demote the gradient-share diagnostic.** Cite the authors' null (paper Section 7 and Hu's comment). Collect it for
   free on the toy reproduction runs only. Prefer a behavioural proxy that is already logged: over training, the
   undetected-hack rate of the RETAIN-only and FORGET-only policies in each arm. Which adapter acquires the undetected
   form first is the direct observable.
5. **Handle the toy anchor.** At minimum log, per step, how many anchor samples are undetected hacks and their reward.
   If budget allows, run exclusive versus standard in one environment with the appendix D.5 anchor (unhackable prompts)
   to check the conclusion does not depend on the penalty-style anchor.
6. **Report the collapse case separately.** Track the fraction of rollouts flagged per step; a run where it reaches 1.0
   is a "learning halted" outcome, not a success at removing hacks.
7. **Gate before the sweep.** One exclusive toy run and one exclusive Countdown smoke test (20 steps) before launching
   anything else; one check that negative scale works through `local_fseval.py` on a released adapter. Start the
   Countdown pod and the toy pod in parallel on day one.
8. **Fix small factual slips.** Three mechanisms, not two; 12 released GRAFT-family adapters, not 8 (use the lr/3 set as
   the paper-matched baseline); FOLLOWUP_WORK.md lives in `shawnghu/small-rl` on `master`; the doubled RETAIN weight is
   intended compensation, so describe it as a design choice to be controlled rather than a possible instability.
9. **Trim the scale sweep.** Run it on 4 lr/3 GRAFT adapters, 4 no-routing adapters and the new exclusive ones, and
   say up front that scale -1 has been tried by the authors during training. Keep it as a secondary figure.
10. **Move fast on publication.** Given the likelihood of unpublished author runs, write up the toy result as soon as
    the controls are in rather than waiting for stage 2.

I would not replace this with a different experiment from the cluster. It is the cheapest proposal that answers a
question the authors asked in public; it needs the control arms to be worth posting.
