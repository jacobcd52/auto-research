# Feedback: 01-kprop-under-training

Verdict: **keep, with substantial tweaks.** The degradation map is a natural, cheap, apparently undone follow-up.
The advice arm as costed cannot produce the headline it promises, the metric has a bug, and the default estimand
(mean output of a trained regressor) has a trivial baseline that will embarrass the write-up unless it is changed.

## What I checked

Search caveat: the WebSearch tool was refused for me too (shared budget exhausted), so the novelty check is again
first-party fetches only. A reviser with search should still look for contest technical reports and blog posts.

| Claim in proposal | Status |
|---|---|
| arXiv:2605.05179, v3 dated 2026-11-02, authors, title | Confirmed (arXiv abs page). |
| Width 256, 4 hidden layers, beats Monte Carlo over 7 orders of magnitude of FLOPs | Confirmed (Fig. 1 text; "in some cases by a factor of over 100"; mean over **5** seeds). |
| LPE: threshold 1_{z>3}, N = 5,695, under 30% relative error 100x below 1/N, 205 seeds | Confirmed (Sec. 6.6, Fig. 4; width 256). |
| Distillation: width 16 teacher, width 8 student, K=2, slightly worse than SGD (batch 36) | Confirmed (Sec. 6.7, App. H; 256 steps). Paper also says the method "would not work well for the entirety of training". |
| "Advice" / base case and inductive step framing | Confirmed in the post text. |
| Christiano "except perhaps in the extremely overtrained regime"; Hilton on offline fitting; Martres and phoenix asking for trained MLPs; Jaburi on non-Gaussian errors | All confirmed verbatim via LessWrong GraphQL comments. Jaburi and Christiano did not really "debate which obstacle is binding"; Jaburi asked one question. Soften that sentence. |
| Repo public, MIT, has `mlp_kprop`, `factor_k3.py`, `flop_utils.py`, bias support, `heaviside` | Files fetched from raw.githubusercontent.com (main). `linear_kprop(..., bias=)` exists and `mlp_kprop` passes each layer's bias; `factored_nonlin_kprop_k3` docstring says it accepts the linear step's output "with non-identity metric and bias already applied". Licence text not re-fetched (GitHub API blocked). |
| LPE / distillation scripts in repo | Not there (`scripts/lpe.py`, `low_prob.py`, `distill.py` all 404); only `kprop_by_width.py`, `form_df.py`, `plot.py`. Must be rewritten, as NOTES says. |
| RunPod A100 80 GB $2.09/h | Confirmed (A100 PCIe Secure Cloud $2.09/h; Community Cloud $1.19/h). |
| No follow-up exists | Nothing found: arXiv API queries ("cumulant propagation", "mechanistic estimation", "white-box estimation", WhestBench, author lists) return no follow-up; alignment.org RSS has nothing after 2026-06-09; no later LessWrong posts by Hilton, Wu, Lecomte on this. Hilton wrote in June that ARC hopes "to say more about all of this in the not-too-distant future", and Christiano returned to ARC in August, so a scoop by ARC is a live risk. |

Three things the proposal did not notice, found in the code and paper:

1. **`mlp_kprop` defaults to `use_avg_metric=True`**, which sets the layer metric to `mlp.init_scale[l] * I`, i.e.
   it replaces W W^T by its expectation under He initialisation. On trained or spiked weights this silently injects a
   random-weight assumption. If left on, R will collapse for a boring reason and the write-up will report an artefact
   of a default flag as a finding. Run with `use_avg_metric=False` (and report both).
2. `HEAVISIDE` in `mlp.py` is `x > 0` with no threshold argument. The tail readout must be built with a bias on the
   last pre-activation; it is easy, but it is not "the same code".
3. `scripts/kprop_by_width.py` defaults to widths up to 128 and ground truth of 2^34 (1.7e10) samples, not 1e9. The
   paper's Appendix I time axis for width 256 runs to about 100 s per estimate on B200 GPUs.

## 1. Would it get upvoted?

Borderline. My estimate is 35-40% for more than 50 karma if stage 1 lands as described.

- The cluster's scores flatter the topic. The 168 and 185 are ARC announcements (a $100k contest, a model zoo). The
  post this actually follows up, the paper linkpost, got 86 with 5 comments, and ARC's random-products post got 56.
  The audience that reads cumulant-propagation details is small. An outside empirical note on the same topic will
  usually score below the original.
- Who cares: ARC staff, contest participants (dozens of teams; two asked for trained MLPs in the comments), and
  people sceptical of the "base case" strategy. That is a real but narrow constituency.
- The direction of the main result is already predicted by the authors: the paper says the method will not work
  through training, and Christiano says current algorithms are not good enough for trained models. "It degrades" is
  therefore not news. What could be news is the quantitative shape: how many steps, lazy versus rich, and which
  statistic predicts it. A post reaches 50+ only if it has one crisp, slightly surprising figure, for example "the
  advantage survives the whole lazy regime but dies within N steps of feature learning, and off-diagonal
  pre-activation correlation alone predicts the loss across all conditions".
- The advice result as designed (exact conditioning restores a synthetic layer-1 spike) is a mathematical identity
  plus bookkeeping. ARC readers will not count it as progress on the inductive step unless it helps on a network that
  was actually trained.

## 2. Naturalness

Mainline. The post itself names trained networks as the essential next step, the screener's note asks for exactly
this probe, and two contest participants requested it. Nobody appears to have published it. This is the obvious
first measurement and the proposer has not contrived it.

Two qualifications. First, ARC almost certainly has these curves internally, so the value is in being public and
reproducible, not in discovery. Second, the advice mechanism here (condition on input directions, quadrature over
them) is not what ARC means by advice: their sketch is a structured weight distribution updated incrementally with
each gradient step. Call the arm "conditioning on known low-rank input structure", not a test of ARC's inductive
step, or the comments will make that point for you.

## 3. Pre-mortem

How it plays out. Day 1 morning: install with `uv`, learn `HTensor` and the `kind` / `factor` flags, reproduce the
init curve at width 256. This works; the code is clean and documented. Day 1 afternoon: synthetic spikes, training
loops, ground truth. Day 2: trajectories, advice, plots. Pure numerics with no external dependencies, so the chance
of not running at all is low. The risk is in what the numbers mean.

Forecast:
- Clear positive (clean map, one predictor collapses the curves, advice helps on something trained): **20%**
- Clear negative that is still interesting (dies fast in every regime with a clean dose-response; advice only
  rescues the synthetic case): **35%**
- Ambiguous mush (noisy R, regime-dependent curves with no collapsing predictor, results that depend on flag and
  estimand choices): **35%**
- Fails to run or to finish the grid: **10%**

Specific failure modes, most important first:

1. **The advice arm cannot reach the promised numbers.** Factorized K=3 costs about 30 n^3 L^2 FLOPs, i.e. several
   thousand forward passes at width 256 (the paper equates it to N = 5,695 samples), and the paper's best advantage
   at initialisation is "a factor of over 100" in some cases. Advice multiplies cost by q^r. With q = 8, r = 2 that
   is 64x; with q = 16, r = 2 it is 256x, which exceeds the entire initial advantage. So even if conditioning
   restores initialisation-level accuracy perfectly, R with advice is at most roughly (initial advantage) / q^r,
   which is about 1 to 2 for r = 2 and below 1 for 256 nodes. The proposal's example outcome "two directions of
   advice restore a 30x advantage at 64x the cost" would need a 1,900x advantage before advice. As costed, the
   likely table reads "advice restores accuracy but not the advantage over sampling", and a reader will ask why
   that was not computed on paper beforehand.
2. **Trivial baseline on the main estimand.** For a network trained by regression, E[f(x)] is pulled towards E[y],
   which the experimenter knows (zero for odd g, a closed form for the multi-index targets). "Output E[y]" costs zero
   FLOPs and its sample-equivalent count is at least Var[f] / loss, growing as training proceeds. On the mean-output
   estimand both kprop and sampling will lose to this constant late in training. This is Hilton's offline-fitting
   objection in miniature. The tail-probability readout has the same problem in milder form, since P(g(u.x) > t) is
   computable from the target.
3. **Metric bug.** N_eq is defined per coordinate as Var / (estimate - truth)^2 and then "averaged over output
   coordinates and seeds". The mean of 1 / error^2 is dominated by coordinates where the error happens to be near
   zero and has no finite expectation for a roughly Gaussian error. NOTES has the right form (variance over mean
   squared error). As written the main metric would be noise.
4. **Scalar outputs give almost no data.** T2 and T3 have a scalar target. If the network has one output, each
   checkpoint yields one squared error per seed, so the MSE comes from 10 numbers and is uncertain by a factor of
   2 or more, and the crossing step for R = 1 is correspondingly blurred. The paper averages over 256 output neurons.
5. **`use_avg_metric` default** (above) produces a spurious collapse.
6. **The proposed predictors are probably not the right ones.** Kprop is an expansion around a Gaussian with small
   cross-neuron correlations. A layer-1 spike is tracked exactly at second order; what it breaks is the smallness of
   off-diagonal pre-activation correlations in which the nonlinear step is truncated. Weight movement, outlier
   singular values and kurtosis are proxies. Without the direct quantity, the "one predictor collapses the curves"
   deliverable is likely to fail and the result reads as mush.
7. **Deeper layers acquire structure immediately.** ReLU activations have a non-zero mean, so the first gradient
   steps add near-rank-one updates to every layer, aligned with the mean-activation direction, not only to layer 1.
   Layer-1 advice on a fully trained network will most likely show partial or no recovery, leaving the advice arm
   with only its synthetic sanity check.
8. **Lazy/rich matched-loss control may be unattainable.** At width 256 with 4,096 online steps, a lazy network on a
   single-index or random-teacher target learns little beyond the linear component. "The same loss reduction with
   small weight movement" may not exist for T2 and T3. Lazy training also needs the output centred (f minus f at
   initialisation), since these networks have non-zero mean output; forgetting this changes the estimand.
9. **Ground truth.** 1e9 samples gives a noise floor at N_eq near 1e9 and usable resolution to about 1e8, whereas the
   paper used 2^34. Fine for factorized K=3 on degraded networks, but the theta = 0 cells for the best variants may
   sit near the censoring limit, which weakens the very sanity check they are for. Accumulate sums in float64;
   float32 running means over 1e9 samples will not resolve relative errors of 1e-4 of a standard deviation.
10. **Wall-clock.** About 920 checkpoints x 3 variants x 2 readouts is roughly 5,500 kprop calls, plus up to 15,000
    for advice. Factorized K=3 should take seconds each; unfactorized K=3 at width 256 is an n^4 computation that
    the paper's own plots put at tens of seconds on a faster GPU. The 12 GPU-hour allowance is tight if unfactorized
    K=3 is run on every cell.

## 4. Cost check

The estimate is realistic and compute is not the binding constraint. The price is verified. Ground truth at about 3
minutes per network on an A100 is plausible (6.6e14 FLOPs at an effective 3-4 TFLOP/s in fp32). I would budget:

- Ground truth, 920 networks: $95 (or about $55 on Community Cloud at $1.19/h).
- Kprop sweeps, with unfactorized K=3 restricted to a subset: $30-60.
- Advice: $15-30.
- Reproduction, debugging, one full rerun of a broken grid: $40-60.

My estimate: **$200-250**, well inside the $500 cap. I would ask for $250, not $160; the first full grid will be
rerun at least once after someone finds the metric flag or a readout bug. Cutting the grid as recommended below
brings it back near $160.

## 5. Recommended changes

1. **Change the primary estimand to per-neuron mean activations of the last hidden layer** (256 coordinates, the
   WhestBench target), with the mean output and tail probability as secondary. This removes the trivial-baseline
   problem, gives 256 squared errors per network instead of 1, and makes the released checkpoints directly usable by
   contest participants. Whatever estimand is used, include the zero-FLOP baselines ("predict E[y]", "predict the
   initialisation-time value") in every plot.
2. **Fix the metric**: N_eq = (mean over coordinates of Var_i) / (mean over coordinates of squared error), or the
   paper's variance-normalised MSE averaged over coordinates, computed per seed and then summarised across seeds on a
   log scale. State this exactly in the plan.
3. **Do the advice arithmetic before running anything and redesign the arm around it.** Report two separate
   quantities: accuracy recovered (N_eq with advice against N_eq at initialisation) and efficiency R including the
   q^r cost. Use r = 1 as the main case and find the smallest q that converges (4 to 6 nodes may suffice for a
   smooth conditional mean). Also try K=2 inside the quadrature, which is about 10x cheaper per call. Drop the
   sentence promising a 30x advantage with two directions. Compare against sampling given the same advice
   (stratified over s), since that is the fair baseline.
4. **Add two bridging conditions so the advice arm can say something about trained networks**: train only the first
   layer with the rest frozen at random (advice should work), and freeze the first layer while training the rest
   (advice should not). Together with the synthetic spikes and full training this gives an interpretable 2x2 instead
   of a likely unexplained null.
5. **Set `use_avg_metric=False` for all non-random weights** and report the initialisation numbers under both
   settings in Step 0. List every non-default flag in the write-up.
6. **Add the mechanistically motivated predictor**: RMS and maximum off-diagonal correlation of pre-activations per
   layer (from samples, or from K=2 kprop itself, which also tests whether the estimator can diagnose its own
   failure). Pre-register it as the primary collapse variable, with the three existing proxies as comparisons.
7. **Shrink the grid to protect the two-day budget.** Drop T3 and the rank-4 spike from stage 1 (keep them as
   stretch), run unfactorized K=3 only at initialisation and on a 10% subset, and use 8 checkpoints (0, 1, 4, 16,
   ..., 4096). Spend the saved time on the bridging conditions and on 2^32 or more ground-truth samples for the
   theta = 0 and early-step cells.
8. **Replace "matched loss reduction" in the lazy/rich control** with matching on training steps while reporting
   loss, relative weight movement and the correlation predictor; centre the lazy network's output and say so.
9. **Reframe the claims.** Present it as "an independent, reproducible degradation map plus a costed test of the
   simplest conditioning fix", say plainly that ARC predicted degradation and that this is not ARC's notion of
   advice, and correct the description of the Jaburi-Christiano exchange. Lead the post with the single figure of R
   against the correlation predictor.
10. A reviser with working search should spend ten minutes checking for Phase 1/2 contest write-ups and any ARC
    post on trained networks before funding; if ARC has published trajectory results, drop this and fund proposal 02
    (training against the estimate) alone.
