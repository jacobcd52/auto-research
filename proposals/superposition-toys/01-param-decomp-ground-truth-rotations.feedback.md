# Feedback: "Can parameter decomposition recover 557 hand-coded circuits in superposition?"

Verdict: **keep, with substantial changes to the plan.** The question is good and apparently unpublished, but the
plan as written has one outright error (the planned targets cannot be built), one mis-described ground truth, and
one confound that could make the headline plot true by construction. All three are checkable on a CPU in the first
few hours, before any decomposition is trained.

What I checked (2026-11-14):
- Post text (`get_post.py LZ7YMPJueB6qjL24n`): the summary in section 1 is accurate (D=1000, T=557, d=4, S=6, L=6
  layers / 5 rotations, "first three of five rotations, or the first four at z=1", Lucius's GPT-2 remark).
- `raw.githubusercontent.com/LindaLinsefors/Rot-in-Sup/main/`: `README.md`, `plots_for_post.py`,
  `classes_and_functions.py`, `assignments.py` all return 200; I read the construction code (`CompInSup`).
- `raw.githubusercontent.com/goodfire-ai/spd/main/`: `README.md`, `docs/skill.md`, `docs/handbook.md`,
  `param_decomp/param_decomp/experiments/{tms,resid_mlp}/run.py`, `param_decomp/param_decomp/core/model.py` all 200.
  `goodfire-ai/spd` and `goodfire-ai/param-decomp` serve the same README (same repo, renamed). Tags `v1` and
  `torch-oracle` resolve. `nano_param_decomp/run.py` exists (47 kB single-file Torch VPD); only its README 404s.
- Prior-work search: arXiv API (phrases "parameter decomposition" + superposition, "circuits/computation in
  superposition", "stochastic/attribution-based parameter decomposition") and a LessWrong title scan of posts with
  karma >= 5 from 2026-07-01 to 2026-11-14. **General web search was not available to me either (search budget
  exhausted), so the "not done yet" conclusion rests on arXiv + LessWrong only**, the same limitation as the
  proposer's. I found no run of APD/SPD/VPD on a hand-coded or trained multi-layer CiS network.
- RunPod pricing page: fetched; it currently advertises community-cloud prices below the proposal's figures
  (RTX 4090 from $0.34/h, A40 $0.35/h, A5000 $0.16/h). The proposal's $0.89 / $0.59 are conservative.

## 1. Would it get upvoted?

Only with a crisp result; a merely competent one will land at 20-40 karma.

Reception of comparable posts (from the LessWrong API):
- Rotations in Superposition itself: 54. The other cluster posts: 63-65.
- "Compressed Computation under L4 Loss is likely CiS" (Ferreira da Silva, Heimersheim; a well-executed toy
  result by known people): 34.
- Third-party audits of VPD by Tom Angsten: "Do VPD's Explanations Aggregate?" 29; "VPD's Evaluation Adversary
  Finds Systematic Defects" 9.
- "Deep models reveal better strategies for superposition": 23. "MSE loss does not generate superposition": 27.
- The VPD paper post itself: 164.

So the audience (Goodfire PD team, Linsefors/Bushnaq, Heimersheim, the small CiS crowd) exists and would read it
closely, but third-party posts in this niche typically sit below 50. My estimate if stage 1 succeeds exactly as
described: about 40% chance of >50 karma. The outcome most likely to clear 50 is a clean, well-controlled negative
("ground truth has lower VPD loss than what the optimiser finds, here is the failure pattern") or a clean
"the method prefers a different, lower-loss decomposition, here it is". A plain positive ("it works on the hand-coded
net") from outsiders is a 30-40 karma post. A tuning-dependent or noise-confounded result is a 10-20 karma post.

## 2. Naturalness

Mainline. It is the screener's suggestion, and it is the obvious meeting point of two artefacts by the same
people: Lucius Bushnaq co-authored both the Rotations post and SPD/VPD, and the Rotations post was funded by
Goodfire. Bhagat et al. removed the PD team's previous CiS testbed, and Ferreira da Silva and Heimersheim say
explicitly that a PD ground-truth test is their next step on their single-layer model.

That same fact is the main scoop risk, and the proposal understates it. The people best placed to do this have had
both artefacts for 11 months. Either they have run it and not published (uninteresting, or not working), or it is
queued. The Ferreira da Silva follow-up could appear at any time and would take much of the "first ground-truth
test on real CiS" framing, though not the multi-layer / hand-coded part. I would put the chance of being visibly
scooped before a write-up at 15-20%. Not a reason to drop; it is a reason to finish stage 1 quickly and to make
the multi-layer aspect (cross-layer linking of components) the distinctive contribution.

## 3. Pre-mortem

### Three problems found in the code, in order of severity

**(a) The planned targets cannot be constructed.** `assignments.comp_in_sup_assignment` raises `MaxT` when it runs
out of low-overlap assignments. I re-implemented `maxT(Dod, S)`; it reproduces the post's headline (Dod=250, S=6
gives exactly 557, which is evidently why T=557 was chosen) and gives:

| D | D/d | S=6 | S=5 | S=4 |
|---|---|---|---|---|
| 400 | 100 | **86** | 125 | 295 |
| 600 | 150 | 176 | 287 | 627 |
| 800 | 200 | 317 | 519 | 1115 |
| 1000 | 250 | 557 | 815 | 1773 |

At D=400, S=6 the maximum is T=86, i.e. load T·d/D = 0.86. The proposal's sweep T in {100,150,200,250} at D=400,
S=6 does not exist, and no S=6 network of width <= 1000 reaches the proposed load of 2.5 (the maximum is 2.23, the
headline network). The load sweep must either move to D=800-1000 (several times more compute per run, and C in the
thousands per layer) or drop to S=4 (a different, noisier operating point than the post's). This changes the cost
and time budget and must be settled before anything else.

**(b) The ground truth is not what section 3 step 3 says.** The network the post reports (`run(capped=True)`, the
default, weights `W3`) is not a sum of per-circuit rank-<=4 terms plus minor shared terms. The code splits each
circuit's 4x4 weights into `mean_w` (the on-indicator step function and the bias-compensating shift, identical for
all circuits) and `diff_w` (the rotation, rank 2). Only `diff_w` is embedded per circuit. `mean_w` is embedded
through a single matrix `capped_embed = clamp(sum_t e_t e_t'^T, max=1) - correction`, which is clamped and
therefore is not a sum over circuits. So in the headline network the part of each circuit that carries "is this
circuit on" has no per-circuit ground truth at all; it is one shared D/d x D/d object of rank up to D/d. The
per-circuit truth is 2 rank-1 pieces per circuit per layer, not 4.
The uncapped variant `W1` (`capped=False, split=False`) is an exact sum of per-circuit terms
`unemb_t (x) w_t (x) embed_t` (rank <= 3 each), but it is the construction the authors moved away from because it
computes worse. The proposal has to choose: clean ground truth on a worse network (`W1`), or the headline network
with a ground truth that is per-circuit only for the rotation half. Labelling the rest "shared machinery" is not
enough; what a correct decomposition of `capped_embed` should look like must be stated before running, otherwise
any outcome on the indicator half is unfalsifiable.

**(c) The headline plot may be true by construction.** The network's raw output contains cross-talk noise
generated by the weights of inactive circuits (their embeddings overlap the active ones). Under an MSE
reconstruction loss on raw final-layer activations, ablating "inactive" circuits changes the output by exactly
that cross-talk, and VPD's adversarial masks will find it. So the designers' decomposition, with "circuit on" as
causal importance, is not faithful to the degree the network is noisy, and it gets less faithful as load grows,
which is the same quantity that breaks the computation. "Recovery collapses where the computation degrades" would
then be a restatement of the noise curve, not a finding about the method. The proposal's oracle check (step 4) is
the right tool but is positioned as step 4 of 8 and is not connected to this issue. Related unstated choice: is
the reconstruction target the raw D-dimensional output or the un-embedded per-circuit readout? That choice
largely determines the answer and is not in the plan.

### How two days will probably go

- Hours 0-6: install the JAX library, run shipped TMS / ResidMLP (docs say these run on CPU; W&B logging is on by
  default and must be disabled in a copied config). Likely works. Exporting the Rot-in-Sup network is easy but has
  traps: `L` in the repo counts weight matrices with `W[0]` = identity; three weight variants exist; the read-out
  subtracts the on-indicator. A parity check against the repo's own `run()` error numbers is needed.
- Hours 6-16: writing a `DecomposedModel` for a deep MLP in a strict JAX codebase tuned for LMs, with a custom
  `recon_loss_fn`. The docs tell agents to expect to write their own target and composition root. The shipped
  ResidMLP target is the nearest shape. I expect this to work but to eat most of day 1. Discovery of (a) happens
  here at the latest, forcing a re-plan to D=1000.
- Hours 16-40: sweeps. The largest published toy has ~100 ground-truth mechanisms; here there are 2T-3T rank-1
  pieces per layer (up to ~1,700 at T=557) times 3 layers, with C at 2-4x that. Convergence time at this scale is
  unknown; the proposal's 1.5-2 h per run is a guess with no reference point. The docs warn that "most apparent
  VPD nulls are under-training" and that the importance-minimality coefficient is highly sensitive. 36 two-hour
  runs are 72 GPU-hours, which needs 4-8 pods in parallel to fit in the remaining wall-clock.
- Hours 40-48: scoring against a ground truth that, per (b), is only half defined, with results that depend on the
  hyperparameter chosen.

### Forecast

| Outcome | Probability |
|---|---|
| Clear positive (>= 90% of circuits recovered over a meaningful load range, stable across seeds) | 20% |
| Clear, interesting negative (oracle beats found solution, or found solution beats oracle with an interpretable pattern) | 20% |
| Ambiguous mush (partial recovery, tuning-dependent, confounded with network noise or with ground-truth choice) | 40% |
| Fails to produce decompositions at the needed scale in two days | 20% |

Specific reasons for the mush outcome, beyond (a)-(c):
- With the capped network, rotation pieces may be recovered while the indicator half is split arbitrarily, giving
  "50% recovered" numbers whose meaning depends on the scoring convention.
- At D=1000, T=557 the average circuit is already near the trivial baseline by layer 3 for z >= 2. The function
  being decomposed is substantially noise there; any method will look bad.
- Blind hyperparameter selection is rigorous, but the library's own guidance for toys is to select with the
  ground-truth metric. A negative result selected blind will be dismissed as mis-tuned unless the best-case
  (oracle-selected) number is also reported.
- Thresholds (F1 >= 0.9, cosine >= 0.8 in every layer) are arbitrary; a result that flips with the threshold is
  not a result.
- The method under test is not pinned. "VPD" in the title, but the fallback is SPD v1, and the current JAX trainer
  uses a smooth-L0 minimality penalty that differs from the VPD paper's L_p form (stated in
  `nano_param_decomp/run.py`). A reader needs to know which objective passed or failed.

## 4. Cost check

$200 is the right order of magnitude and comfortably under the cap; compute is not the binding constraint,
wall-clock and tuning are. Adjustments:
- The load sweep has to run at D=800-1000 rather than D=400 (see 3a), with C in the thousands per layer. Allow
  3-4 h per run rather than 2 h: 36 runs x 3.5 h = ~125 GPU-h.
- A second sweep is likely, not a contingency: ~40 GPU-h.
- At the proposal's prices ($0.59-0.89/h) that is about $150-180 plus gate/baselines ~$20; at the community prices
  currently advertised it is roughly half.
My estimate: **$150-300**, so the proposal's $200 is acceptable as a central figure; I would state $300 to cover
the D=1000 runs. The TMS / ResidMLP gate and the oracle check cost nothing (CPU).

## 5. Recommended changes (most important first)

1. **Fix the target grid.** D=400, S=6 tops out at T=86. Use D=1000, S=6 with T in roughly {125, 250, 400, 557}
   (load 0.5-2.2), or D=800 with T up to 317. State the `maxT` limit in the proposal. If compute forces a smaller
   D, use S=4 and say that this is not the post's operating point.
2. **Make the oracle check the first experiment and the go/no-go gate, on CPU, before writing any trainer
   wrapper.** For each target, evaluate the designers' decomposition under masked reconstruction (random and a
   short PGD adversary over inactive-circuit masks) and compare the induced error with the network's own
   computational error. If the ground truth is not approximately faithful, the question "does VPD recover it" is
   ill-posed at that load, and the publishable finding becomes the oracle analysis itself: "the intended circuits
   of a hand-coded CiS network are not a faithful decomposition under VPD's criterion beyond load X". That is a
   cheap result that needs no training and is interesting on its own.
3. **Define the ground truth concretely per weight variant.** Run both `W1` (exact per-circuit sum; check first
   that it still computes at the chosen T) and the capped `W3`. For `W3`, score the rotation pieces (`diff_w`,
   2 rank-1 pieces per circuit) per circuit, and pre-specify what counts as correct for the shared `capped_embed`
   block, or score it separately and descriptively.
4. **Fix the reconstruction target in advance**, and report both: raw final-layer activations, and un-embedded
   per-circuit readouts. Restrict the headline claim to layers and z where the target network is itself well below
   the trivial baseline (z=1, and z=2 at lower load), so method failure is separable from network failure.
5. **Pin the method.** Primary: the current `param_decomp` JAX trainer starting from the shipped ResidMLP target
   (closest shape). Decide by hour 12 whether it works; fallback is the `v1` PyTorch SPD release, and the write-up
   must name the objective actually used. Note `nano_param_decomp/run.py` exists as a single-file Torch VPD, but
   it is LM-shaped (token ids, KL) and would need adapting.
6. **Report both blind-selected and best-case (ground-truth-selected) hyperparameters**, and show recovery as a
   distribution over circuits (F1 and cosine histograms) rather than a single thresholded fraction.
7. **Cut scope.** Stage 1 should be: oracle analysis on all targets; decomposition of two targets (one with
   T·d < D that must succeed, one in true superposition) with 3 seeds; cross-layer linking on those. Move the
   full load curve, the transcoder baseline and the shuffled-split control to "if time permits"; keep one cheap
   baseline (per-neuron or SVD split of each weight matrix) so there is a chance-level reference.
8. **Acknowledge the scoop risk** (Bushnaq is an author of both artefacts; Heimersheim's group has announced a PD
   ground-truth test) and lead the write-up with what they are least likely to publish first: the multi-layer
   linking result and the oracle-faithfulness analysis.

I would not switch to a different experiment from this cluster: the direction is the most natural one available,
and the fixes above are cheap. Without changes 1-4, though, the most likely product is a confounded plot.
