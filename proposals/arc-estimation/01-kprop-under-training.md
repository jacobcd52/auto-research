# How long does ARC's white-box estimator keep beating sampling once an MLP is trained, and does low-rank "advice" buy it back?
cluster: arc-estimation | stage-1 cost: $160 | follows up: Mechanistic estimation for wide random MLPs (fsG4m6sRMpomd7Rk6); Announcing the ARC White-Box Estimation Challenge (Kben8CzS4awCwNw5c)

## 1. What the prior work showed
ARC's paper (arXiv:2605.05179, v3 of 2026-11-02) estimates the expected output E_{x~N(0,I)}[f(x)] of a randomly
initialised MLP from its weights alone, by "cumulant propagation" (kprop): approximate cumulants of the
activations up to order K are pushed through the layers with Hermite expansions, and no input is ever run. For
ReLU MLPs with 4 hidden layers and width 256, the best variants (factorized K=3) reach a given mean squared error
with fewer floating-point operations (FLOPs) than Monte Carlo sampling across 7 orders of magnitude of budget.
With the last ReLU replaced by a threshold 1_{z>3}, the same code estimates rare-event probabilities 100 times
below 1/N to within 30% at the cost of N = 5,695 samples. Code is public (MIT):
https://github.com/alignment-research-center/mlp_cumulant_propagation.

Everything is at initialisation. The only trained-network evidence is one "mechanistic distillation" curve (width
16 teacher, width 8 student, about 250 steps), which was slightly less efficient than SGD; the authors guess this is
because the estimator has guarantees only for random weights. ARC frames the random case as the base case of an
induction whose inductive step, i.e. updating the estimator with "advice" as training adds structure, is unsolved.
The follow-up contest (WhestBench, AIcrowd) also uses only random MLPs. In its comments two participants asked for
a trained-MLP track; Jacob Hilton replied that it is hard to design; Paul Christiano wrote that current
algorithms are probably not good enough for trained models "except perhaps in the extremely overtrained regime".

What already exists as follow-up (checked by direct fetches of arXiv, the ARC blog, LessWrong author pages and
comment threads, the contest pages; a web search engine was not available): the contest itself (random weights,
deeper networks; dozens of teams), an ARC post on random products (not about MLP training), and a June overview
post. I found no public measurement of how kprop accuracy changes along a training trajectory, and no public test of
any advice mechanism.

## 2. Question and why it matters
**As a width-256 MLP is trained, how quickly does the released estimator lose its advantage over sampling, what
property of the weights predicts the loss, and is the advantage restored by a cheap, explicit piece of advice
(the few input directions in which the first layer has become structured)?**

ARC's whole programme rests on the base case extending through training, and nobody outside ARC knows whether the
released method dies after one gradient step, survives the whole lazy regime, or degrades gracefully. Each outcome
is informative:
- If the advantage survives substantial training in some regimes, the base case reaches further than the paper
  claims, and the contest's random-weight setting is less artificial than critics said.
- If it collapses as soon as features are learned but returns with r-dimensional advice, that is a small working
  instance of the inductive step ("structure plus randomness") with a measured cost.
- If advice does not help, the experiment tells us which obstacle is binding (higher-layer structure, non-Gaussian
  activations), which is what Christiano and Louis Jaburi debated in the comments without data.

## 3. Stage 1 plan
Reused: ARC's `mlp_kprop` package (estimators at K=2, K=3, factorized K=3; FLOP counting in `flop_utils.py`;
`MLP` class; sample cumulants). Built: training loops, the metric, the advice wrapper (about 100 lines).

**Metric.** Training changes output scale, so raw MSE is not comparable across checkpoints. For each network and
estimator we report the sample-equivalent count N_eq = Var_x[f_i(x)] / (estimate_i - truth_i)^2, averaged over
output coordinates and seeds, and the efficiency ratio R = FLOPs(Monte Carlo with N_eq samples) / FLOPs(estimator).
R > 1 means the estimator beats sampling. Ground truth is Monte Carlo with 1e9 samples (about 6.6e14 FLOPs per
network; minutes on one GPU), which resolves N_eq up to about 1e8; cells above that are reported as censored.

**Step 0 (half day): reproduce.** Reproduce the paper's width-256, 4-hidden-layer MSE-versus-FLOPs figure at
initialisation with 20 seeds and confirm R > 1 for factorized K=3. Measure wall-clock per kprop call; if it is
too slow at width 256, drop to width 128 for the grid (decision recorded before any trained-network result).

**Step 1: dose-response with synthetic structure (no training).** Add controlled perturbations to random
weights and sweep their strength theta from 0 until R < 1: (a) rank-one spike theta·u v^T in layer 1; (b) the same
in layer 3; (c) rank-4 spike; (d) dense small perturbation with the same Frobenius norm (control: is it structure
or mere distance from init that matters?); (e) per-neuron biases. 10 seeds x 8 strengths x 5 types.

**Step 2: real training trajectories.** ReLU MLPs, 4 hidden layers, width 256, Gaussian inputs, online
SGD/Adam, checkpoints at steps 0, 1, 2, 4, ..., 4096; 10 seeds per condition:
- T1 random-teacher regression (the paper's distillation task at realistic width);
- T2 single-index target y = g(u·x) and T3 rank-4 multi-index target, where the first layer is known to pick up
  low-rank spikes aligned with the target directions;
- for T1 and T2, a lazy-versus-rich control: the same loss reduction reached with small weight movement (large
  output scale, small learning rate) or large movement (standard scale).
At each checkpoint: R for K=2, K=3, factorized K=3, for the mean output and for a tail probability (threshold
readout with truth between 1e-5 and 1e-2). Also record candidate predictors: relative weight movement per layer,
number and size of singular values outside the Marchenko-Pastur bulk, excess kurtosis of sampled pre-activations.
Key analysis: R against training step and against each predictor; the step at which R crosses 1; which predictor
gives a single curve across tasks and regimes (rank correlation, with seeds as the unit).

**Step 3: advice.** For checkpoints where R < 1, give the estimator the top r <= 2 structured input directions V
(outlier right singular vectors of the first-layer weights). Because x conditioned on V^T x = s is Gaussian with
mean V s and covariance I - V V^T, the expectation is exactly an r-dimensional Gauss-Hermite quadrature over s of
conditional expectations, each one kprop call on a network with an isotropic input in the complement and a
first-layer bias W_1 V s. Cost is q^r kprop calls (q = 8 to 16 nodes). Report R with advice, including the extra
FLOPs. Controls: random directions V of the same rank (advice must be the right directions to help); the
synthetic layer-1 spike from Step 1 (where advice should fully restore R, a correctness check); the layer-3 spike
(where it should not).

**Deliverables.** Plots of R versus training step per regime, the dose-response curves, the advice table, and
the checkpoints with 1e9-sample ground truth released in the WhestBench data format so others can test estimators.

## 4. Stage 1 cost estimate
Prices from runpod.io/pricing today: A100 80 GB $2.09/h.
- Step 0 reproduction and timing: 4 GPU-h = $8.
- Ground truth: about 400 synthetic + 520 trained checkpoints (4 conditions + 2 controls, 13 checkpoints, 10
  seeds, minus overlap) at roughly 3 minutes each = 46 GPU-h = $96. If time is short, 1e8 samples for cells where
  N_eq is clearly below 1e6 cuts this by about half.
- Training (tiny) and kprop runs (wall-clock unknown; allowance): 12 GPU-h = $25.
- Advice runs (up to 256 kprop calls on about 60 checkpoints): 6 GPU-h = $13.
- Subtotal about $142; storage and reruns margin brings the request to **$160**. No LLM API spend.

## 5. What success looks like
A clear result is a figure showing, per training regime, the step (and weight-movement level) at which factorized
K=3 stops beating sampling, with seed-level error bars, plus one predictor that collapses the curves. Examples of
post-worthy statements: "kprop still beats sampling by 10x after the loss has fallen 90% in the lazy regime but
loses within 8 steps in the rich regime"; "a layer-1 spike of strength theta > 0.3 x the bulk edge is enough to
lose, and two directions of advice restore a 30x advantage at 64x the cost"; or "advice restores the synthetic
spike but not the trained network, because by then layers 2-4 carry outliers too".

A null on the advice arm (no recovery) is still publishable alongside the degradation map, since the map itself is
new. The weak outcome is R < 1 for every perturbation however small, including the dense control; that would
suggest an implementation or ground-truth problem and Step 0 plus the theta = 0 cells exist to exclude it. If it is
real, "the advantage is destroyed by any O(1) departure from Gaussian weights" is a strong and simple negative.

## 6. Stage 2 (if stage 1 succeeds)
(a) Advice for structure in deeper layers: propagate a low-dimensional conditioned subspace through the network
(deduction-projection style) instead of only at the input; (b) incremental advice updated per gradient step,
measured over full training; (c) a public "trained split" for WhestBench with held-out training distributions to
blunt the offline-fitting objection; (d) apply the best contest estimators if their code is public. Roughly $1,000
to $2,000, mostly GPU time for ground truth at width 1024.

## 7. Risks and how the plan handles them
- **Released code does not accept the needed inputs** (non-zero biases or a conditional input on the factorized
  path). `linear_kprop` takes a bias and `mlp_kprop` takes an input mean and covariance; the advice wrapper is
  written to need only an isotropic input plus a first-layer bias. Checked in Step 0 on a 16-wide network against
  brute-force sampling.
- **Ground-truth noise mistaken for estimator error.** Report the censoring threshold; use two independent 1e9
  runs on a subset to confirm the noise floor.
- **kprop too slow at width 256.** Pre-registered fallback to width 128 and fewer checkpoints; the paper's own
  experiments ran at 256, so the forward estimate is known to be feasible.
- **Over-claiming from one architecture.** Claims are restricted to ReLU MLPs with Gaussian inputs at one width
  and depth; the dense-perturbation control and the lazy/rich contrast guard against attributing the effect to the
  wrong cause. Ten seeds per cell, seed-level bootstrap intervals.
- **ARC may have unpublished internal results.** Likely, but nothing is public; an independent, reproducible map
  with released checkpoints is useful to contest participants regardless.
