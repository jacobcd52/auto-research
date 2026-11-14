# arc-estimation: reading notes and brainstorm

Research lead notes, written 2026-11-14. Everything below marked "verified" was fetched directly today;
anything else is my inference.

**Search caveat.** The WebSearch tool was unavailable (the shared search budget for this run was already used
up), so the related-work check was done only through direct fetches of first-party sources: arXiv abstract/HTML
pages and the arXiv export API, the LessWrong GraphQL endpoint (posts + all comments), alignment.org/blog,
the AIcrowd challenge and leaderboard pages, raw.githubusercontent.com READMEs/source, the Hugging Face dataset
API and the public GCS bucket listing. A reviser with search access should re-check novelty, especially for
(a) contest technical reports from Phase 1/2 of the White-Box Estimation Challenge and (b) any ARC post after
June 2026 on trained networks.

## 1. The three posts

### 1.1 AlgZoo: uninterpreted models with fewer than 1,500 parameters (x8BbjZqooS4LFXS8Z, 2026-01-26, 185 karma)
- ARC releases a zoo of tiny RNNs/transformers (8 to 1,408 parameters) trained on four algorithmic tasks:
  2nd argmax (RNN), argmedian (RNN), median (RNN), longest cycle (transformer).
- ARC's definition: an "explanation" of a trained model = a *mechanistic estimate* of its loss/accuracy (deductive,
  from the weights, not from sampled inputs). Two quality metrics: (i) MSE versus compute, compared with Monte
  Carlo sampling; (ii) surprise accounting (bits), which defines "full understanding".
- Case study, 2nd-argmax ReLU RNNs M_{d,n} (hidden size d, sequence length n, no biases; h_{t+1} = ReLU(W_hh h_t +
  W_hi x_t), logits = W_oh h_n; Gaussian inputs):
  - M_{2,2}: 10 parameters, error rate about 1 in 13,000; fully understood by enumerating linear regions; about 40
    bits of surprise.
  - M_{4,3}: 32 parameters, 98.5% accuracy; understood via approximate symmetries plus brute force; roughly matches
    sampling in MSE-vs-compute; handcrafted version gets 99.99%.
  - M_{16,10}: 432 parameters, 95.3% accuracy; NOT understood. ARC found an isolated subcircuit (neurons 2, 4, 6,
    7, 1) computing running max and "leave-one-out max" features, and a 22-neuron handcrafted model at 99%, but no
    mechanistic accuracy estimate.
- Explicit challenge from the post: design a mechanistic estimator for the accuracy of M_{16,10}
  (`example_2nd_argmax()`, plus `zoo_2nd_argmax(16, 10, seed=0..4)`) that matches sampling in MSE versus compute.
  Suggested cheap MSE protocol: add noise to the weights (enough to change accuracy noticeably) and average squared
  error over noisy models; better but costlier: average over training seeds.
- Comments (verified): Nicholas Goldowsky-Dill fit neurons {1,6,7,8} with a running-max / second-running-max linear
  model (R^2 = 0.992) - descriptive, not an estimate. Martin Keane: ReLU activation-pattern sequence D[t] is
  stable after the max "impulse"; effective linear operators Phi_post per (max position, 2nd position); gist at
  https://gist.github.com/mrsirrisrm/d6850ff8647d1ed2f67cc92d5bce3ed0 . Hilton asked whether this can be turned
  into a mechanistic estimate; nobody did. **Hilton, 2026-08-17: "I don't recall seeing any specific effort on these
  models in the last six months outside of the comments on this post ... we are not much closer to succeeding at
  the challenge."** So the challenge is still open as of that date.

### 1.2 Mechanistic estimation for wide random MLPs (fsG4m6sRMpomd7Rk6, 2026-05-07, 86 karma)
- Linkpost for arXiv:2605.05179 (Wu, Lecomte, Winer, Robinson, Hilton, Christiano), "Estimating the expected
  output of wide random MLPs more efficiently than sampling"; v3 dated 2026-11-02 (I read the v3 HTML).
- Task: given weights of a He-initialised MLP (ReLU default; no biases in the main setting), estimate
  E_{x~N(0,I)}[f(x)] without running the model. Method: cumulant propagation ("kprop") - propagate approximate
  cumulants (order up to K) layer by layer using Hermite/Wick expansions, drop terms that are small relative to
  cost; "factorized" variants for K=3, K=4.
- Results: theory - beats Monte Carlo by a factor polynomial in width at fixed depth. Experiments - ReLU MLP, 4
  hidden layers, width 256: best kprop variants beat Monte Carlo across 7 orders of magnitude of FLOP budget.
  Low-probability estimation (Sec 6.6): final ReLU replaced by threshold 1_{z>3}; with FLOPs equal to Monte Carlo
  with N = 5,695 samples, factorized K=3 gets under 30% relative error for probabilities 100x below 1/N, and beats
  all baselines (zero, MC, MC + Gaussian extrapolation, MC + cumulant extrapolation) down to about 10^4 x below 1/N;
  205 seeds. Mechanistic distillation (Sec 6.7): random teacher width 16 -> student width 8, 4 hidden layers, K=2,
  about 250 gradient steps; works but is slightly less efficient than SGD with batch size 36 at matched FLOPs. The
  paper attributes this to the estimator only having guarantees at initialisation.
- Stated limitations: weights must be random; depth dependence is poor (Appendix D); wall-clock is often worse than
  Monte Carlo (Sec 6.8/App. I). **The paper has no experiment on trained or partially trained networks other than
  that one distillation curve**; Sec 7.2 says extension would need a "structure versus randomness" treatment and
  leaves it to future work. The post says the same ("advice" pointing out which higher-order deviations to
  track; a structured weight distribution as a compression of the weights).
- Comments (verified): Hilton confirms tensor-network diagrams appear in the algorithm; emanuelr proposes
  AlphaEvolve-style automation; Hilton announces the contest idea.

### 1.3 Announcing the ARC White-Box Estimation Challenge (Kben8CzS4awCwNw5c, 2026-06-02, 168 karma)
- Contest with AIcrowd ("WhestBench"): given weights of a random Gaussian ReLU MLP, estimate per-neuron mean
  post-ReLU activation, minimising MSE under an analytic FLOP budget metered by `flopscope`. Any method allowed.
- Timeline (verified from comments/starter kit): warm-up June 2026 (width 256, 8 hidden layers per the post text
  rendering; the FLOP cap was 6.8e10); Phase 1 from 2026-06-23 to end of July, $50k ($25k/$10k/$5k + $10k
  algorithmic-contribution prize), depth raised to 32 hidden layers; Phase 2 after that with >= $100k. The starter
  kit README today says: width 1024, depth 16, budget 2^41 FLOPs per MLP (about 6.5e4 forward passes), score =
  final-layer MSE against N = 1e9 Monte Carlo ground truth times max(0.1, FLOPs used / budget), flopscope 0.12.3,
  dataset tag `v2-phase2`.
- Hilton (2026-06-23): best warm-up submissions were variants of ARC's factorized K=3 cumulant propagation plus
  learned networks consuming cumulant estimates as features; many LLM-assisted.
- Leaderboard (verified today): dozens of teams, many with 60-110 submissions each, latest entries dated late
  September to late October 2026. The contest is crowded and has prize money behind it.
- Relevant comments: Guillaume Martres and "phoenix" asked for a trained-MLP track. Hilton: a trained-MLP contest
  is hard to design because, given a fixed distribution over trained models, people can fit predictors offline.
  Christiano: current random-network algorithms are "not yet good enough that you should expect it to be possible
  to analyze trained models in a convincing way, except perhaps in the extremely overtrained regime"; the random
  case is the base case and they want to know early if it fails. Louis Jaburi: errors in trained models will not
  look Gaussian.

### 1.4 Other ARC posts found (context, not in the cluster)
- "Mechanistic estimation for expectations of random products" (LW 7RyAefESvb6BQ3tMz, 2026-05-15, 56 karma;
  alignment.org) - deduction-projection estimators for random halfspace intersections, #3-SAT, permanents.
- "A Mike's-Eye View of ARC's Research" (alignment.org, 2026-06-09, Michael Winer) - pipeline: detect structure
  during training -> convert to advice for an MSP estimator -> estimate probability of catastrophe -> optimise the
  model against the estimate; says explicitly that the estimator must be adversarially robust because the model
  is trained against it.
- No ARC blog post after 2026-06-09 on alignment.org/blog; no LessWrong post by Jacob_Hilton or Wilson Wu after
  2026-06-02. arXiv API queries for "matching sampling principle", "mechanistic training", "low probability
  estimation" + neural, "cumulant" + "trained networks" + MLP returned no follow-up papers. (arXiv:2609.03026
  "ObserverBench" uses the phrase "mechanistic estimates" but is about intervention selection in LLMs, unrelated.)

## 2. Public artefacts (verified)

| Artefact | Where | Status |
|---|---|---|
| AlgZoo code | https://github.com/alignment-research-center/alg-zoo (README and `alg_zoo/*.py` readable via raw.githubusercontent.com; github.com HTML is 403 from this sandbox) | MIT-0 licence. API: `example_2nd_argmax()`, `zoo_2nd_argmax(hidden, seq_len, seed=, n_seqs=)`, `zoo_argmedian`, `zoo_median`, `zoo_longest_cycle`, `handcrafted_2nd_argmax(n)`, `train(task_name, hidden_size=, seq_len=, seed=)` |
| AlgZoo checkpoints | `gs://arc-ml-public/alg/zoo`, publicly listable over HTTPS (`https://storage.googleapis.com/storage/v1/b/arc-ml-public/o?prefix=alg/zoo/`) | Files named `<task>_<d>_<n>_<n_seqs>_<seed>.pth`, about 4 KB each. First 1,000 objects are all 2nd_argmax with (d, n) in {2,16,32} x {2,3,4,5,6,8,10} (listing truncated; more exist, e.g. (4,3) is loadable per the post). Checkpoints at 0, 2^20 ... 2^29 of 2^30 training sequences; 5 seeds each. Trained on an A100 with PyTorch 2.9.1 |
| ARC notes on M_{4,3} and M_{16,10} | Google Drive PDFs + a Colab linked from the post | Not fetched (Drive); assume readable by a browser but do not depend on them |
| Cumulant propagation code | https://github.com/alignment-research-center/mlp_cumulant_propagation | MIT. `src/mlp_kprop/` with `mlp.py` (activations: relu, gelu, sigmoid, tanh, abs, sgn, square, cube, **heaviside**), `kprop_harmonic.py` (`mlp_kprop(mlp, K_in, k_max)`; `K_in` is a dict {1: mean, 2: covariance}; **biases are supported** in `linear_kprop`), `factor_k3.py`, `factor_k4.py`, `flop_utils.py`, `cumulants.py` (sample cumulants). Scripts: `kprop_by_width.py`, `form_df.py`, `plot.py`. I could NOT confirm that scripts for the low-probability or distillation experiments are in the repo (guessed filenames 404); assume those loops must be rewritten (they are short) |
| Paper | https://arxiv.org/abs/2605.05179 (v3) | read |
| Contest | https://www.aicrowd.com/challenges/arc-white-box-estimation-challenge-2026 ; starter kit https://github.com/AIcrowd/whest-starterkit (MIT); harness https://github.com/AIcrowd/whestbench ; FLOP meter https://github.com/AIcrowd/flopscope (MIT, on PyPI) | Submitting requires an AIcrowd account (agents cannot). Local scoring works without one |
| Contest data | https://huggingface.co/datasets/aicrowd/arc-whestbench-public-2026 (CC-BY-4.0, not gated; splits `mini` = 100 MLPs and `full`; tag `v2-phase2`) | public; includes N = 1e9 Monte Carlo ground truth |
| Top contest submissions / tech reports | not found | unknown whether public; needs a search |

## 3. Prices looked up today

- RunPod on-demand (https://www.runpod.io/pricing): A100 PCIe 80 GB $2.09/h; A100 SXM $2.19/h; H100 PCIe $2.89/h;
  RTX 4090 $0.89/h; A40 48 GB $0.59/h; RTX A5000 24 GB $0.27/h; L4 $0.69/h.
- Lambda (https://lambda.ai/pricing): A100 40 GB $1.99/h; A10 24 GB $1.29/h; A6000 $1.09/h.
- No LLM API or Tinker spend is needed for any idea below (all are numerical experiments on small MLPs/RNNs).
- Scale check: a width-256, 5-linear-layer MLP forward pass is about 2 x 5 x 256^2 = 6.6e5 FLOPs; 1e9 samples =
  6.6e14 FLOPs, i.e. on the order of one to a few minutes on an A100 in fp32. Width-256 kprop tensors of order 3 have
  1.7e7 entries (fits easily). Wall-clock of the released kprop per call at width 256 is NOT known (paper says it is
  slower than Monte Carlo per FLOP) - first thing to measure.

## 4. Brainstorm (all candidates, including rejected)

Legend: feasibility = can a Claude-agent team do it in about 2 days for <= $500; value = would the result interest
LessWrong/ARC readers whichever way it comes out.

1. **Does cumulant propagation keep beating sampling as an MLP is trained, and does cheap low-rank "advice" buy it
   back?** (screener's suggestion, sharpened.) Run the released estimators on training checkpoints of width-256
   MLPs across lazy/rich regimes and synthetic spikes; measure sample-equivalent efficiency; test a concrete
   first-layer advice mechanism (condition on spike directions, quadrature, kprop on the conditional Gaussian).
   Feasible (pure numerics, released code, about $150). Natural next step - the paper and both posts name trained
   networks as the open problem, two commenters asked for it, and nothing public measures it. Interesting both
   ways. **-> Proposal 01.**

2. **Train against the mechanistic tail-probability estimate: does the true tail probability fall, or does the
   optimiser Goodhart the estimator?** The paper's safety story ("mechanistic training" against rare dangerous
   events) is argued, not demonstrated: LPE is shown only at initialisation, and training only for a distillation
   loss at width 16 -> 8. Minimise the kprop estimate of P(z > 3) under a norm constraint, track true probability
   with 1e9-1e10 samples, compare with FLOP-matched sampling baselines. Feasible (about $260) but with more
   moving parts than #1 (differentiating through factorized K=3, fair baselines). High value either way: first
   demonstration, or a measured estimate-truth decoupling, which is exactly the "adversarially robust estimator"
   requirement in Winer's post. **-> Proposal 02.**

3. **Attack the AlgZoo M_{16,10} challenge directly** (post's own suggestion). ARC calls success "a major research
   breakthrough"; Hilton says there was marginal progress in seven months including by motivated humans. A 2-day
   agent team is unlikely to succeed, and a proposal promising it would over-claim. Rejected as stated.

4. **AlgZoo "ladder": where between 32 and 432 parameters do automated deductive estimators stop matching
   sampling?** Build the noise-perturbation MSE-vs-FLOPs harness ARC describes; run a ladder of estimators on
   the zoo grid (d in {2,4,16,32}, n in {2..10}): plain MC; improved black-box (stratified/antithetic/QMC);
   Rao-Blackwellised hybrids that integrate the last k inputs exactly (the network is piecewise linear in each
   input, so k = 1 is an exact 1-D integral with <= d + n breakpoints); full region enumeration for small n.
   Feasible and nearly free (CPU). Value: moderate - it would quantify ARC's qualitative statement that brute
   force blows up exponentially, and would show how much of "matching sampling" is achievable by partially deductive
   estimators, but the most likely outcome ("constant-factor gains at k = 1-2, then blow-up") is what ARC already
   says, and whether hybrids count as "mechanistic" is disputable. Third-ranked; not written up because the cluster
   allows two proposals and #1/#2 have clearer, less predictable outcomes. Worth reviving if a slot opens: cost
   under $50.

5. **Enter the White-Box Estimation Challenge.** Rejected: needs an AIcrowd account (agents cannot create one);
   dozens of teams with 60-110 submissions each and $100k+ in prizes are already hill-climbing with LLMs; marginal
   contribution of two days is small; leaderboard rank is not a LessWrong post.

6. **Analyse the contest: depth/width phase diagram of released estimators versus Monte Carlo.** Rejected: ARC
   already documents poor depth scaling (Appendix D) and built Phase 1 around it; top submissions are not confirmed
   public, so this would only re-measure ARC's own baselines.

7. **A trained-MLP split for WhestBench.** Attractive (two commenters asked) but Hilton's objection is real
   (offline-fitted predictors on a fixed trained distribution) and designing a contest is not a 2-day research
   result. Folded into Proposal 01 as a by-product: checkpoints + ground truth released in the WhestBench format,
   and stage 2.

8. **Narrow / deep random networks.** Rejected as a standalone: this is exactly the contest's Phase 1/2 target.

9. **Other activations / architectures (tanh, GELU, attention) at initialisation.** The repo already supports
   several activations and the paper reports them (tanh appears 14 times); transformers would require new theory.
   Rejected: incremental or too hard.

10. **Surprise accounting for the Goldowsky-Dill / Keane partial explanations of M_{16,10}.** Would turn commenters'
    descriptive fits into ARC's metric. Rejected: needs a deductive derivation of correlations from weights (the
    hard part Hilton pointed out); likely ends as an inconclusive partial account.

11. **AlgZoo across training checkpoints: when does structure appear?** The zoo has checkpoints at 2^20..2^29
    sequences. One could track when the leave-one-out-max subcircuit forms. Rejected: descriptive interpretability
    with no estimate; weak link to ARC's metric; modest interest.

12. **Learned (amortised) estimators for AlgZoo accuracy** (train a network mapping weights -> accuracy over the
    noise distribution). Rejected: this is precisely the "offline-fitted predictor" that ARC regards as beside the
    point, and it does not transfer.

13. **Mechanistic distillation at larger width / more steps (replicate and extend Fig. 5).** Partly subsumed by #1
    (accuracy along a training trajectory) and #2 (training against the estimate). Not separate.

14. **Human-readable hand analysis of a mid-sized AlgZoo model (e.g. M_{16,3} or M_{16,4}) to full surprise
    accounting.** Possible in principle for n = 3 (cones in R^3 have closed-form solid angles), but 16 neurons x 3
    steps gives many regions; the result would be a long technical note of interest mostly to ARC. Rejected on
    expected-karma grounds; could be a stage-2 of #4.

## 5. Design facts a reviser will need

- Scale-free metric for trained networks: sample-equivalent count N_eq = Var_x[f_i(x)] / MSE_i (averaged over
  output coordinates i and seeds), and efficiency ratio R = (FLOPs of Monte Carlo with N_eq samples) / (FLOPs of
  the estimator). R > 1 means the estimator beats sampling. This avoids confounding by output scale changing
  during training. Ground-truth noise must be far below estimator error: with N_gt samples the floor is N_eq <=
  about N_gt/10, so N_gt = 1e9 lets us resolve N_eq up to about 1e8.
- First-layer advice is exact: for orthonormal V in R^{n x r}, x | V^T x = s is Gaussian with mean V s and
  covariance I - V V^T, and `mlp_kprop` takes an arbitrary input mean and covariance. So
  E[f] = integral over s ~ N(0, I_r) of E[f | s], computed by Gauss-Hermite quadrature with q^r nodes, each node
  one kprop call. Whether the factorized K=3 code path accepts non-isotropic input is unverified (there is a
  `get_all_terms_iso` function, suggesting some paths assume isotropy) - check first; fallback is the
  non-factorized `mlp_kprop` at K = 2, 3, or rotating the input basis and absorbing the covariance into W_1
  (x = V s + P z is equivalent to a first layer with bias W_1 V s and weights W_1 P on isotropic z in the (n - r)-
  dimensional complement, which keeps the input isotropic).
- Known theory to cite for why first-layer spikes are the natural first test: one large gradient step on a
  single-index target adds an approximately rank-one spike to the first-layer weights (Ba et al. 2022,
  arXiv:2205.01445; Damian et al. 2022, arXiv:2206.15144) - from memory, not re-fetched today.
- LPE in the paper is implemented by swapping the final activation for the threshold 1_{z>3} (the repo's
  `heaviside` nonlinearity, shifted), so a tail probability is just a "mean output" for kprop.
