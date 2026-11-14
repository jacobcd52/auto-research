# Training against a mechanistic tail-risk estimate: does the true rare-event probability fall, or does the optimiser fool the estimator?
cluster: arc-estimation | stage-1 cost: $260 | follows up: Mechanistic estimation for wide random MLPs (fsG4m6sRMpomd7Rk6); Announcing the ARC White-Box Estimation Challenge (Kben8CzS4awCwNw5c)

## 1. What the prior work showed
ARC's paper (arXiv:2605.05179) estimates expected outputs of randomly initialised MLPs from the weights alone
using cumulant propagation ("kprop"), with no forward passes. Two of its results are the basis for ARC's safety
argument:
- **Low-probability estimation.** For ReLU MLPs of width 256 with 4 hidden layers, replacing the final activation
  by a threshold 1_{z>3} turns each output into a rare-event probability. With the FLOPs of 5,695 Monte Carlo
  samples, factorized K=3 kprop estimates probabilities 100 times smaller than 1/5,695 to within 30% relative
  error, and beats sampling-based baselines (including sampling plus Gaussian extrapolation) down to nearly 10^4
  times smaller.
- **Mechanistic training.** The estimates are differentiable, so one can do gradient descent on the estimate. The
  paper shows this only for a distillation loss, at width 16 -> 8, for about 250 steps, where it was slightly worse
  than SGD.

The post and paper then argue that combining the two would give models "with a greatly reduced probability of
catastrophic tail risks": SGD may never sample a rare dangerous event, whereas mechanistic training can see it
coming. That combination is not demonstrated anywhere. ARC's June overview post (Winer, alignment.org) states the
plan as "train the model until the estimate of its catastrophic behavior is acceptably small" and notes that the
estimator must therefore be adversarially robust, because the model is being optimised against it. The paper
itself warns that the estimator has guarantees only for random weights.

Existing follow-ups (checked by direct fetches of arXiv, ARC's blog, LessWrong, and the contest pages; no
search engine was available): the AIcrowd contest improves mean estimation on random weights only; I found no
public experiment that trains against a kprop tail estimate or measures estimate-versus-truth divergence under
optimisation. Code: https://github.com/alignment-research-center/mlp_cumulant_propagation (MIT; includes the
threshold activation and FLOP counting; I could not confirm the distillation loop is included, so it is rebuilt).

## 2. Question and why it matters
**If we minimise the kprop estimate of a rare-event probability by gradient descent, starting from a random
MLP, how far does the *true* probability fall compared with FLOP-matched sampling-based training, and at what
point do the estimate and the truth come apart?**

This is the smallest end-to-end test of ARC's proposed safety mechanism. Both outcomes matter:
- If the true probability falls by orders of magnitude more than under sampling baselines given the same compute,
  that is the first concrete demonstration that white-box estimates can drive down a tail risk that sampling cannot
  see, in the setting where the estimator is at its best.
- If the estimate keeps falling while the truth stalls (the optimiser finds weights where the estimator is wrong),
  that measures the adversarial-robustness gap ARC says must be closed, and shows how many steps of optimisation
  the "base case" tolerates. The size and onset of that gap is a number nobody has published.

## 3. Stage 1 plan
Reused: `mlp_kprop` (K=2 and factorized K=3 estimators, threshold activation, FLOP accounting, MLP class). Built:
the optimisation loop, baselines, and a high-sample evaluator.

**Setup.** ReLU MLP, width 256, 4 hidden layers, standard Gaussian input, He initialisation, no biases, as in the
paper. The "danger" events are z_i > 3 for 16 fixed final-layer pre-activations z_i. Objective: minimise the mean
of log p_i. To exclude the trivial solution of shrinking the weights, every weight row is re-projected to its
initial norm after each step (so each z_i keeps roughly unit scale and the tail can shrink only by changing the
shape of the distribution or the correlations feeding it). A second variant adds a task so that capacity is
contested: the other 240 outputs must keep matching a frozen copy of the initial network (distillation penalty
estimated by sampling for all methods, so only the tail term differs between methods).

**Methods compared at matched FLOPs per gradient step** (FLOPs counted with the repo's utilities; backward pass
counted as 2x forward for all):
1. kprop factorized K=3 estimate of p_i (the paper's method), differentiated with autograd.
2. kprop K=2 (Gaussian-only mechanistic estimate): shows whether the third cumulant is what matters.
3. Sampling + Gaussian extrapolation: estimate mean and variance of z_i from N samples and differentiate the
   Gaussian tail formula (the paper's strongest simple sampling baseline, and naturally differentiable).
4. Sampling + smooth surrogate: minimise the sample mean of softplus((z_i - 3)/tau), with tau tuned on separate
   seeds.
5. No tail term (control; in the task variant, shows drift from the distillation term alone).
N for methods 3 and 4 is set so FLOPs per step equal those of method 1. Same optimiser (Adam) with learning rate
tuned per method on 3 held-out seeds by final true probability; 10 evaluation seeds; 300 steps.

**Truth.** At log-spaced checkpoints (0, 1, 2, 5, 10, 20, 50, 100, 200, 300) the true p_i is measured by Monte
Carlo with 1e9 samples (1e10 at the final checkpoint for the three best methods), resolving probabilities down to about 1e-8 with usable
error bars; below that we report an upper bound. Initial p_i is about 1e-3, so there are 5 orders of magnitude of
headroom.

**Measurements.** (a) true mean log10 p versus step and versus cumulative FLOPs, per method; (b) the "Goodhart
gap" log10(p_true / p_estimated) for methods 1-3 along their own trajectories; (c) cross-evaluation: each
estimator scored on every other method's checkpoints, which separates "the weights left the estimator's valid
regime" from "the optimiser specifically attacked this estimator"; (d) what changed in the network: output
skewness and kurtosis of z_i, weight movement, singular-value outliers.

**Order of work.** Day 1 morning: reproduce the paper's low-probability figure at initialisation on 20 seeds
(go/no-go: kprop K=3 beats method 3's estimator at equal FLOPs); verify gradients of the kprop estimate against
finite differences on a width-32 network; time one optimisation step. Day 1 afternoon: learning-rate tuning.
Day 2: main runs, truth evaluation, cross-evaluation, write-up.

## 4. Stage 1 cost estimate
RunPod price looked up today: A100 80 GB at $2.09/h.
- Reproduction, gradient checks, timing: 6 GPU-h = $13.
- Tuning: 5 methods x 4 learning rates x 3 seeds x 300 steps; kprop steps dominate (wall-clock per step not yet
  known; allowance 20 GPU-h) = $42.
- Main runs: 5 methods x 2 variants x 10 seeds = 100 runs; allowance 20 GPU-h = $42.
- Truth evaluation: 100 runs x 10 checkpoints x about 3 min at 1e9 samples = 50 GPU-h; final-checkpoint
  evaluations at 1e10 samples (about 30 min each) only for the 3 best methods x 5 seeds, 15 evaluations = about
  8 GPU-h; allowance 60 GPU-h = $125.
- Subtotal about $222; margin for reruns brings the request to **$260**. No LLM API spend.

## 5. What success looks like
The headline plot is true rare-event probability versus cumulative training FLOPs for the five methods, with the
estimator's own belief overlaid for the mechanistic ones.
- Clear positive: after 300 steps, kprop K=3 training lowers the true probability by at least 10x more than the
  best sampling baseline (seed-level intervals not overlapping), in both variants. Statement: "white-box
  tail-risk training works in the base case, by a factor X at equal compute".
- Clear negative: the kprop estimate reaches, say, 1e-9 while the truth stalls near 1e-5, with the gap opening at an
  identifiable step and cross-evaluation showing the estimator is still accurate on other methods' checkpoints.
  Statement: "optimising against the estimate breaks it after about k steps; the estimator is accurate on
  random and SGD-trained weights but not on weights selected against it".
- Mixed and still publishable: kprop wins early (first tens of steps) and loses later, giving the number of steps
  the base-case estimator tolerates and motivating advice updates.
- Uninformative: all methods, including Gaussian-extrapolated sampling, reduce the tail equally and stay
  calibrated. Then the task is too easy (the tail is governed by variance alone). The row-norm constraint and the
  K=2 versus K=3 contrast are there to detect this on day 1; the remedy is a higher threshold (z > 4) or the
  contested-capacity variant only.

## 6. Stage 2 (if stage 1 succeeds)
(a) Alternate optimisation with estimator repair: add low-rank "advice" or periodic sampling-based correction and
measure how much compute keeps the estimate honest; (b) a distribution-shift test, where the rare event becomes
more likely under a shifted input covariance, which is ARC's motivating scenario; (c) width 1024 and the best
public contest estimators; (d) rare events defined on trained (not random) starting networks. About $1,500 to
$2,500 of GPU time.

## 7. Risks and how the plan handles them
- **Autograd through the factorized K=3 path fails or is too slow.** The paper trained through K=2; K=3 is
  untested for gradients. Day-1 gradient check on a small network; fallback is non-factorized K=3 at width 128, or
  K=2 as the mechanistic method with K=3 used only as an evaluator.
- **Unfair baselines.** Sampling baselines get the same FLOPs per step, separately tuned learning rates and
  temperature, and the strongest simple estimator from the paper. FLOP accounting is stated explicitly and the
  comparison is also shown per step and per wall-clock second.
- **Truth too small to measure.** 1e10 samples bound probabilities near 1e-9; anything lower is reported as an
  upper bound, and the key claims (10x differences, a stalled truth near 1e-5) sit well above the floor.
- **Trivial solutions.** Row-norm projection removes weight shrinkage; the control arm and the contested-capacity
  variant show whether reductions come at the expense of the rest of the network.
- **Over-reading a toy.** Claims are limited to random-initialised ReLU MLPs with Gaussian inputs and an
  artificial event; the write-up presents it as a test of the base case of ARC's plan, not of the plan.
- **Overlap with proposal 01.** 01 measures estimator accuracy under ordinary training; this one measures what
  happens when the estimate itself is the training signal. They share the reproduction step but answer different
  questions and either can run alone.
