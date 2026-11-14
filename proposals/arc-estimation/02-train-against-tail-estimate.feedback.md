# Feedback: 02 — Training against a mechanistic tail-risk estimate

Verdict: **major overhaul**. The question is good and, as far as I can tell, undone. The experimental design as
written will most likely produce an uninformative result, for reasons that are fixable before any GPU is rented.

## What I checked

- **Paper claims: confirmed** against arXiv:2605.05179 v3 (HTML fetched today). Sec 6.6: width 256, 4 hidden
  layers, threshold 1_{z>3}, N = 5,695, under 30% relative error at 100x below 1/N, beats baselines to nearly
  10^4x below; 205 seeds. Sec 6.7 / App. H: distillation 16 -> 8, K=2 basic kprop, 256 steps, SGD batch 36,
  "slightly less efficient" than SGD. Sec 7.2 argues the tail-risk application but does not run it. The
  abstract's "greatly reduced probability of catastrophic tail risks" quote is accurate.
- **Two details the proposal omits that matter for the design** (App. G and H):
  - "MC + Gaussian extrapolation ... performs similarly to using cumulant propagation to estimate the mean and
    variance", i.e. proposal method 2 (kprop K=2) and method 3 are near-duplicates as estimators.
  - There is a fourth baseline, **MC + cumulant extrapolation** (sampled mean, variance and third cumulant pushed
    through the same Hermite formula). It is the paper's strongest sampling baseline, it is differentiable, and
    the proposal leaves it out while calling Gaussian extrapolation "the strongest simple sampling baseline".
  - App. H already names the bias-versus-variance issue: the mechanistic estimate "has bias but no variance",
    which "may favor stochastic gradient descent". That is the Goodhart mechanism in the authors' words.
- **Code: public, partially confirmed.** `raw.githubusercontent.com/alignment-research-center/mlp_cumulant_propagation/main/`
  serves `README.md`, `src/mlp_kprop/{mlp,factor_k3,kprop_harmonic,flop_utils,wick}.py` and
  `scripts/kprop_by_width.py`. `heaviside` exists (threshold at 0, so z > 3 needs a bias of -3 on the last
  layer; biases are supported). Six guessed script names for the low-probability and distillation experiments
  all 404, so those loops are probably not released (not certain; I could not list the directory). The README
  sets `torch.set_grad_enabled(False)`, and `factor_k3.py` uses in-place methods (`add_factors_`,
  `contract_wick_`). **Nobody has confirmed that autograd runs through the factorized K=3 path**; the paper
  trained only through basic K=2 at width 8. I did not run the code.
- **Prices.** RunPod pricing page fetched today shows $1.99 among the listed prices near the A100 entry; the
  proposal's $2.09/h is within 5% either way. No effect on the conclusion.
- **Prior art.** WebSearch was unavailable to me as well (shared budget exhausted), so this is again direct
  fetches only: arXiv API queries for "cumulant propagation", "mechanistic training", "mechanistic estimation",
  "low probability estimation" + training, "wide random MLPs" returned nothing relevant after the paper itself;
  LessWrong comments on the paper post contain no such experiment. **Not checked:** contest technical reports,
  Twitter/X, ARC internal follow-ups, anything after June on alignment.org beyond what NOTES.md records. Novelty
  is probable, not established. ARC obviously could have run this in an afternoon and may have unpublished
  results; that cuts both ways (they would care about the answer, but may say "we knew").
- **One numerical check I ran** (numpy, 3 random nets, 2e6 samples each, the proposal's exact architecture):
  across the 768 final-layer outputs, P(z > 3) has median 1.5e-4, 5th-95th percentile from 0 (below 5e-7) to
  6e-2, and 19% of outputs had zero hits in 2e6 samples. The per-output mean of z has standard deviation 1.13
  across outputs, larger than the typical within-output standard deviation of z (0.82). So "initial p_i is about
  1e-3" is wrong: 16 fixed outputs will span more than five orders of magnitude, and the spread is driven by the
  **mean** of z, not its shape.

## 1. Would it get upvoted?

If it produced a clean result, yes, plausibly 50-100 karma. The cluster posts got 86 (paper), 168 (contest) and
185 (AlgZoo); the audience is small but engaged, and ARC staff answer comments. "First end-to-end test of
mechanistic training against a tail risk" with a single plot of true versus believed probability is a legible
headline, and the negative version ("the estimate went to 1e-9 while the truth stayed at 1e-5") is the more
shareable of the two. A third-party technical follow-up to an 86-karma paper post would normally land at 30-70,
so it needs the clean plot. A result of the form "everything went to zero and all methods tied" earns nothing.

## 2. Naturalness

Mainline. The paper's Sec 7.2 and the post both describe exactly this combination and do not run it; Winer's
overview names adversarial robustness of the estimator under optimisation as a requirement. It is the obvious
next experiment and more central to ARC's safety argument than proposal 01. I found no evidence it has been
done, with the search caveats above.

## 3. Pre-mortem

The design has four concrete defects. The first two are close to fatal as written.

**(a) The task has a trivial exact solution that the row-norm projection does not block.** Hidden activations
are ReLU outputs, hence non-negative. A final-layer row with all entries non-positive gives z <= 0 always, so
p = 0 exactly, at unchanged row norm. Short of that, the optimiser only needs to rotate each of the 16 final rows
against the mean-activation direction to shift the mean of z down by a few units; my numbers above show the mean
already dominates p at initialisation. Hidden rows can likewise be rotated to make pre-activations mostly
negative, shrinking activation scale with norms fixed. This is a first-moment effect that K=2 kprop, Gaussian
extrapolation and the softplus surrogate all see perfectly. The claim that "the tail can shrink only by changing
the shape of the distribution or the correlations feeding it" is false.

**(b) The "contested capacity" variant is not contested.** The 16 danger outputs have their own final-layer
rows, which the distillation penalty on the other 240 outputs does not touch. The optimiser moves those 16 rows
and leaves everything else alone. Raising the threshold to z > 4, the proposal's other remedy, does not help
either.

Consequence of (a) and (b): with learning rate tuned "by final true probability", every method picks a rate
that drives p below the 1e-9 measurement floor within tens of steps. The headline plot is five curves hitting
the floor, and the Goodhart gap is unmeasurable because truth is an upper bound. The proposal lists this as the
"uninformative" outcome; I think it is the modal one.

**(c) The objective "mean of log p_i" is ill-defined for the kprop estimate.** The K=3 threshold estimate is a
Gaussian tail plus a Hermite/Edgeworth correction proportional to the third cumulant
(`heaviside_wick_coef` = higher `relu_wick_coef`), which is not constrained to be positive. The paper's Figure 4
has relative errors above 100% at small p, consistent with wrong-sign estimates. Minimising log of this gives
NaN as soon as an estimate crosses zero, and gradient descent will push it there. Any clamp or softplus the
agents add silently changes what is being optimised and is exactly where the "Goodhart" behaviour will live, so
it has to be specified in advance. Related: with p_i spanning 1e-2 to below 1e-9 at step 0, mean log p is
dominated by outputs whose truth cannot be measured.

**(d) Baselines.** Methods 2 and 3 are near-duplicates per the paper; the paper's best sampling baseline
(cumulant extrapolation) is missing; and FLOP-matching gives sampling about 5,695 samples per step, about 1.7e6
over 300 steps, so for p >= 1e-5 plain sampling sees the event many times and the motivating "SGD never samples
it" regime is never entered.

**Other risks.** Autograd through factorized K=3 fails or needs a rewrite of in-place ops (moderate; the
fallbacks in section 7 are sensible but K=2-only removes the comparison that matters). Wall-clock per kprop step
is unknown and dominated by pure-Python overhead per the paper; backward through it could be several seconds
per step, which is still fine for 300 steps. Truth evaluation in fp32 at 1e9-1e10 samples is routine. Five
methods x two variants x tuning in two days is more than needed.

**Forecast, as written:** clear positive 5%; clear, interesting negative 15% (most likely via the estimate going
negative or NaN, which is a real finding but a shallow one); ambiguous mush or "all methods hit the floor" 60%;
fails to run usefully (autograd/K=3 problems eat the time) 20%.

**Forecast with the changes below:** clear positive 15%; interesting negative or mixed (measured gap with onset
step) 45%; mush 25%; fails to run 15%. Note the positive outcome is the less likely one: the paper's own
distillation result and its bias-without-variance remark both point toward the estimator being exploited.

## 4. Cost check

$260 is realistic for the plan as written; compute is not the constraint. With the redesign (smaller initial
probabilities, hence 1e10-1e11 samples per truth evaluation, but far fewer runs) I estimate $250-400: roughly
10 h setup and timing, 30 h training and tuning, 80-120 h truth evaluation on an A100 at about $2/h, plus
margin. Stays under $500. Measure the per-step wall-clock and the 1e9-sample evaluation time in the first hour
and cut seeds, not checkpoints, if either is 3x worse than assumed.

## 5. Recommended changes (in order of importance)

1. **Make the tail the only thing left to optimise.** Freeze the final-layer rows of the danger outputs and add
   a penalty (sampled, identical for all methods) that pins each danger output's mean and variance to their
   initial values, or equivalently require all outputs including the danger ones to keep matching the frozen
   teacher in MSE. Then lowering p requires changing third- and higher-order structure through the hidden
   layers, which is the regime where the paper says K=3 has its advantage. Report the pinned moments over
   training to show the constraint held. State plainly that this construction is chosen to make Gaussian
   methods blind; the informative comparison is then K=3 kprop versus sampled-cumulant extrapolation.
2. **Fix the objective.** Minimise a specified, sign-safe function of the estimate (for example the sum of p_i
   over outputs selected to start in one decade, or log of a softplus-floored estimate with the floor stated),
   and log the raw signed estimate. Treat "estimate crosses zero at step k" as a reported outcome.
3. **Choose danger outputs by initial probability, not by index.** Pick outputs (or per-output thresholds) so
   that true p_0 sits in a narrow band, and run two bands: about 1e-4 (sampling sees it; sanity regime) and
   about 1e-6 to 1e-7 (FLOP-matched sampling sees it at most a handful of times in the whole run; the regime the
   safety argument is about). Budget 1e10-1e11 truth samples for the low band.
4. **Replace the baseline set.** Keep: K=3 factorized kprop; MC + cumulant extrapolation (paper's strongest);
   MC + Gaussian extrapolation; plain sampled surrogate; no-tail control. Drop kprop K=2 as a training method
   (keep it as an evaluator in the cross-evaluation). Tune learning rates on a criterion that does not reward
   hitting the floor, e.g. true p at a fixed FLOP budget chosen so the best method is still measurable.
5. **Day-1 go/no-go, in this order:** (i) autograd through factorized K=3 at width 32 against finite
   differences; (ii) reproduce Figure 4 at initialisation; (iii) run 20 steps of the unconstrained task as
   written and confirm the trivial mean-shift collapse, which is a two-line negative control worth one sentence
   in the write-up; (iv) only then the constrained task. If (i) fails after half a day, switch to non-factorized
   K=3 at width 64-128 rather than to K=2.
6. **Cut scope.** One task variant (the constrained one), two probability bands, four methods plus control,
   5-8 seeds. Keep cross-evaluation (c); it is the measurement that distinguishes "left the valid regime" from
   "attacked this estimator" and is the most interesting part of the proposal. Drop (d) unless time remains.
7. **Fix the factual slips in the text:** initial p_i is not "about 1e-3" (median about 1.5e-4, spanning more
   than five decades); Gaussian extrapolation is not the paper's strongest sampling baseline; cite App. H's
   bias-versus-variance remark as the prior expectation.
8. **Relation to proposal 01.** If only one of the two is funded, I would fund this one after the redesign: it
   tests the claim the safety case rests on, and a measured estimate-truth gap under optimisation is a number
   ARC has said it needs. Without the redesign, fund 01 instead.
