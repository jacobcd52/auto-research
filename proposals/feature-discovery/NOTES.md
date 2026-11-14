# feature-discovery — reading notes and brainstorm

Cluster: "SAEs and feature-discovery alternatives" (4 posts). Written 2026-11-14.

Caveat on the literature check: the WebSearch tool was unavailable for this session (shared search budget
exhausted), so the "already done?" check used only direct fetches: arXiv abs/html pages and the arXiv API,
LessWrong GraphQL (posts, comments, authors' later posts), raw.githubusercontent.com READMEs, the Hugging Face
API, openrouter.ai and runpod.io. A reviser with search access should re-check for independent follow-ups to
Exemplar Partitioning and to the gate-lift / amp-score work (queries I could not run: "exemplar partitioning
k-means baseline AxBench", "channel amplification score transcoder", "condensation score SAE").

## 1. Posts as read (verified, not the screener's summary)

### 1.1 Announcing Gemma Scope 2 (YQro5LyYjDzZrBCdb, 2025-12-22, 96 karma)
- Tooling release, no findings. JumpReLU SAEs (resid, MLP-out, attn-out) and MLP transcoders (with / without
  affine skip) for every layer of all 10 Gemma 3 models (270m, 1b, 4b, 12b, 27b; PT and IT). Per layer: widths
  16k and 262k, two L0s. At four depths (25/50/65/85%) a wider sweep incl. 65k and 1m residual SAEs. Also CLTs
  (270m, 1b) and "weakly causal" crosscoders over 4 layers. Matryoshka loss + frequency penalty.
- Authors say they have deprioritised fundamental SAE research; the release is "a tool for the community".
- Verified on HF (API, no auth needed): `google/gemma-scope-2-1b-pt` is ungated, folders `resid_post`,
  `resid_post_all`, `mlp_out`, `mlp_out_all`, `attn_out`, `attn_out_all`, `transcoder`, `transcoder_all`,
  `clt`, `crosscoder`. For 1b the sweep layers are 7, 13, 17, 22. `transcoder/` has widths 16k/65k/262k x
  L0 small/medium/big x {plain, `_affine`}. `resid_post/` has 16k/65k/262k/1m and a `..._262k_l0_medium_seed_1`
  second seed. Each folder: `config.json`, `params.safetensors` (151 MB at 16k), `examples.safetensors`.
- Configs (fetched): transcoder L13 reads `model.layers.13.pre_feedforward_layernorm.output` and predicts
  `model.layers.13.post_feedforward_layernorm.output`; resid SAE is on `model.layers.13.output`; mlp_out SAE on
  `post_feedforward_layernorm.output`. So Gemma 3 has sandwich norms around the MLP — matters for any
  Jacobian-based measurement.
- Gemma weights: `google/gemma-*` repos are gated ("manual"), which the programme's "no accounts/approvals"
  rule excludes. Ungated mirrors verified: `unsloth/gemma-2-2b`, `unsloth/gemma-2-2b-it`,
  `unsloth/gemma-3-1b-pt`, `unsloth/gemma-3-1b-it`, `unsloth/gemma-3-270m`. Gemma-3-1b: 26 layers,
  d_model 1152, MLP width 6912, gelu_pytorch_tanh.
- arXiv API search for "gemma scope 2" returned only two unrelated application papers; no systematic
  third-party evaluation found (but see caveat above).

### 1.2 Elementary Condensation (JKexLeze9kNhCYYzT, 2026-04-08, 51 karma, Jan)
- Operationalises Eisenstat's condensation score: a representation is a list of (concept, scope) pairs; score
  = excess bits read over all queries (subsets of token positions). Features are binarised by a swept
  threshold, scope assigned by mutual information with token positions, top-k features kept, raw tokens also
  stored at singleton scopes, score reported relative to the trivial representation.
- Results: planted 8-token toy (7 binary flags, rate 15%, 6 dims): SAE reaches 86% of oracle and its best
  threshold is the true 15%; PCA and random fall short. TinyStories 8-word openings (4-layer model and GPT-2
  small): SAE > PCA > random, small gaps. Induction prompts (5 words + repeat, 50-word pool, GPT-2 small):
  PCA beats SAE clearly, because the shared concept is a 50-way categorical and the SAE shatters it into
  one-hots; shrinking the pool to 8 shrinks PCA's lead. Three null settings (open-web windows, independent
  slot fills, addition) give no method better than trivial.
- Author's stated gaps: ~a dozen unprincipled pipeline choices; binarisation loses information; scopes are
  2^N; "the biggest gap is that I have not tested the paper's actual theorem" (two good-scoring
  representations agree — e.g. two SAE seeds, Theorem 5.8); prediction that split-feature families show up as
  scope collisions and that merging them improves the score; using the score as a training objective.
- No code link in the post. No comments. Author's later posts (checked via GraphQL) are unrelated; no follow-up.

### 1.3 Exemplar Partitioning (RroeHBSkBXXDsrryq, 2026-05-16, 70 karma, Jessica Rumbelow; arXiv 2605.14347)
- Method: leader clustering of centred, unit-normalised activations in one streaming pass; an activation
  joins the nearest exemplar if within a cosine threshold (the p-th percentile of pairwise distances), else
  becomes a new exemplar. Each region keeps exemplar, region mean, count, coherence.
- IMPORTANT: the paper is now at v3 (17 Sep 2026) and has moved well past the post. The post's headline was
  AUROC 0.881 (exemplar, "token-mean contrast" selection rule, LLM-regenerated test set). v3's headline is
  **0.937** at p1 (K=5,796) using the **region mean** under AxBench's SAE-A rule (pick the region with the
  best training-set AUROC, max-pooled cosine over tokens) on AxBench's shipped held-out set, vs SAE-A 0.911,
  canonical SAE 0.755, DiffMean/Probe 0.946, BoW 0.931, Prompt 0.921. Exemplar readout at p1 is only 0.832;
  the README explains "a single activation gives a spiky max-over-positions score that lets one generic
  region win the training-set selection for many concepts".
- Already done by the author in v3 (so NOT open): Llama-3.1-8B replication; base-vs-IT harmful/benign region
  analysis with permutation null, matched-K and TF-IDF k-means controls; region-mean "swap" intervention
  (compliance 0.00 -> 0.88 Gemma / 0.91 Llama at L14, with random-span and benign-span controls, n=32); Taboo
  secret-word organisms (19/21 with a recognisable region, but the best region is chosen post hoc using the
  secret); SAEBench sparse probing / core / RAVEL adapter; 5-seed stability with a per-region predictor;
  direction correspondence with Gemma Scope (about 1 in 5 regions has a strong SAE match at p10).
- NOT done (checked by grepping the v3 HTML): any *null dictionary* on AxBench — no random-activation,
  random-direction, k-means or token-embedding candidate set scored under the same selection rule; no
  K-matched comparison (EP K=5,796 vs SAE 16,384, and a different build corpus); **no AxBench steering
  numbers** although the repo ships `--axbench-modes latent,steering,steering_test`; no alternative distance
  metric (listed as future work); no stability-filtered dictionaries (future work).
- Comments: Riya Tyagi (7 karma) raises exactly the selection concern — "the AxBench results select the best
  region, which only shows the existence of a good region" — and asks for TPR/TNR at the native threshold.
  Rumbelow replies that good tests should be causal (steering, patching) and that hers are "by no means
  conclusive yet". Stanislav Fort notes the OOD use resembles Mahalanobis-distance OOD detection.
- Public assets (verified): code `https://github.com/jessicarumbelow/exemplar-partitioning` (README readable
  via raw.githubusercontent.com; pip-installable `ep` package; `python -m scripts.build_partitions ... --eval
  axbench --axbench-selection auroc --axbench-act-cache-dir ...`). Prebuilt dictionaries
  `https://huggingface.co/datasets/J-RUM/exemplar-partitioning`: gemma-2-2b L12 p in {1,2,4,8,10}, L20 p10;
  gemma-2-2b-it L4 p4, L12 p10, L20 p in {1,2,4,8,10} (L20 p1 pickle is 1.77 GB; gemma-2-2b L12 p1 is 6.0 GB);
  files are Python pickles (load in an isolated process). The p0.5 build is not released. AxBench data:
  `https://huggingface.co/datasets/pyvene/axbench-concept500` (`2b/l20/{train,test}/data.parquet`, ~10 MB
  each), code `https://github.com/stanfordnlp/axbench`. Gemma Scope for Gemma-2-2B: `google/gemma-scope-2b-pt-res`
  has `layer_20/width_16k` and `layer_20/width_65k` only.
- AxBench reference numbers (fetched from arXiv 2501.17148 HTML), Gemma-2-2B L20. Detection AUROC: ReFT-r1
  0.965, DiffMean 0.946, Probe 0.946, BoW 0.931, Prompt 0.921, SAE-A 0.911, LAT 0.809, SAE 0.755, PCA 0.712.
  Steering overall (harmonic mean of concept/instruct/fluency, 0-2): Prompt 0.731, ReFT-r1 0.509, DiffMean
  0.178, SAE 0.151, SAE-A 0.132, LAT 0.130, Probe 0.091, PCA 0.083. Judge is gpt-4o-mini; 10 Alpaca-Eval
  instructions per concept, half to pick the steering factor and half held out. Evaluation set has hard
  negatives; training set has 72 positive + 72 negative texts per concept.

### 1.4 In search of natural features (SNAKJuN8FdoEaWeFC, 2026-08-23, 56 karma, Dmitry Vaintrob)
- Amp / "error-correction" score for a unit direction v at an MLP: E[v^T J v | v.z > a] - E[v^T J v | v.z < a],
  J the MLP Jacobian, whitened metric (eps 0.1). Claims in the post: random ~ 0 < real activations < SAE
  features, coarser features higher (parent 0.140 vs child 0.104); gradient ascent from 100k+ token
  activations converges to exactly four maxima ("the", whitespace, word-continuation "Names of Man", abstract
  noun "Names of God") at gpt2-small noLN layer 6; 3-6 maxima across layers, GPT-2 sizes and Llama; bigram-only
  data recovers most of them. Author: "the most likely way in which the results would turn out to be
  uninteresting" is "this is actually just PCA with bells and whistles"; asks for criticism and bug-finders.
- The repo (`https://github.com/mvaintrob/denoising-tomography`, README and RESULTS.md readable via raw
  URLs) is more careful than the post and already contains much of the obvious stress-testing:
  covariance-matched ("coloured") random nulls; lift ladder at GPT-2 block 8: coloured 0.04, single
  activations 0.17, **SAE features 0.09-0.13**, token means and supervised probes 0.2-0.3 (so in that protocol
  SAE features do NOT beat raw activations, and a two-line mean-difference probe beats every SAE arm); the
  frequency and granularity trends are conditioning artifacts that vanish when conditioning on true encoder
  on-events; the flow "manufactures lift ~0.7 on a RANDOM-INIT model"; the endpoint library is layer-global
  (own-anchor recovery 83% vs foreign 76%); it is a weights x corpus object (unigram corpus dissolves it,
  TinyStories lacks the name attractor); surrogate flow objective and raw lift disagree on rankings. Uses
  `apollo-research/gpt2_noLN` (ungated, verified) and the jbloom feature-splitting GPT-2 SAEs. Runs on one GPU.
- Comments: David Africa (20 karma) replicated block 6, ran all blocks of GPT-2 small-XL (median attractor
  count 1, 1, 3, 3.5; zero at random init — note this conflicts in spirit with the repo's random-init floor
  finding, different protocols), and found a perturbation added along an attractor persists LESS through
  later MLPs when the attractor is naturally active. Vaintrob: whitening matters (fewer maxima without).
- Not done anywhere I could find: (a) a ground-truth test — a model where we know which directions the MLP
  nonlinearly denoises — of whether lift ranks them above nulls and whether the flow recovers them or
  collapses to a few basins; (b) transcoder features (dictionaries trained on the MLP's input-output map)
  as an arm; (c) any model with public transcoders + SAEs at matched layers, e.g. Gemma 3 with Gemma Scope 2.
  Author's later posts (PIRAMID, circuit priors) do not revisit this.

## 2. Prices looked up (2026-11-14)
- RunPod on-demand (runpod.io/pricing): A40 48 GB $0.59/h; RTX A6000 48 GB $0.69/h; L40 $0.82/h; L40S
  $1.09/h; RTX 4090 $0.89/h; A100 PCIe 80 GB $2.09/h; H100 PCIe $2.89/h.
- OpenRouter ($/M tokens in/out): openai/gpt-4o-mini 0.15/0.60; anthropic/claude-haiku-5.5 0.10/0.50;
  openai/gpt-5-mini 0.25/2.00; anthropic/claude-haiku-4.5 1.00/5.00; anthropic/claude-fable-5.2 8/40.

## 3. Brainstorm (all candidates, with verdicts)

1. **Null-dictionary ladder for EP on AxBench detection + first AxBench steering numbers for EP.** PROPOSED
   (01). Cheap (~$150), all infrastructure released, directly answers the top comment and the author's own
   "tests should be causal" reply; the headline 0.937 sits 0.006 above a bag-of-words classifier, which makes
   "how much is selection among thousands of real-activation directions?" a live question. Interesting either
   way: either a random-activation codebook matches EP (deflating "EP beats SAEs" into a benchmark artefact,
   and saying something about AxBench detection generally) or EP's density-calibrated cover genuinely beats
   k-means/random at matched K (first evidence the partition itself matters).
2. **Gate lift on ground truth and on transcoders (planted toy + Gemma-3-1b with Gemma Scope 2).** PROPOSED
   (02). Cheap (~$100). Combines two posts' assets. The repo already did the easy deflations, so the added
   value has to be new arms: a toy with known gated vs pass-through features, and transcoder read/write
   directions. Riskier than 01: the metric has many knobs, and Gemma's sandwich norms complicate the Jacobian.
3. Replicate / bug-hunt the four ur-features across layers and sizes. REJECTED: David Africa's comment and
   the repo's own experiments 07-11 already cover replication, scaling across GPT-2 sizes, corpus dependence
   and random-init floors.
4. "Is it just PCA?" for the ur-features. FOLDED into 02 as a control (PCA arm in both toy and Gemma) rather
   than a stand-alone project; alone it is too narrow for a post.
5. Test condensation's agreement theorem with two SAE seeds; scope-collision signature of feature splitting.
   REJECTED for now: no released code, the pipeline has ~12 admitted arbitrary choices to re-derive, works
   only for N=8 token windows with positional structure, and audience interest is modest (51 karma, 0
   comments). A null would be uninterpretable (score vs pipeline). Would reconsider if the author releases
   code. Gemma Scope 2's `_seed_1` SAEs would be the natural asset.
6. Condensation score as an SAE training objective. REJECTED: speculative ("elegant or completely cursed"),
   not a 2-day project.
7. EP with other distance metrics (Euclidean, Mahalanobis) as a test of the linear representation
   hypothesis. REJECTED as a stand-alone: without a ground-truth criterion the comparison reduces to "which
   metric scores higher on AxBench", which proposal 01 shows may not discriminate; could be a stage-2 arm of 01.
8. Blind EP audit of the Taboo organisms (auditor not told the secret) vs the SAE/logit-lens baselines of
   Cywinski et al. REJECTED: incremental on the author's v3 result, needs gemma-2-9b-it organisms (gated
   base), and overlaps with the auditing-benchmarks / activation-oracles clusters.
9. EP nearest-exemplar distance as OOD / jailbreak monitor vs Mahalanobis. REJECTED: large existing
   literature (Fort's comment), unlikely to be novel enough.
10. EP fine-tuning audits on emergent-misalignment or other model organisms. REJECTED here: plausible but
    overlaps other clusters (model diffing), and proposal 01's result should come first — if random-activation
    codebooks do as well, the audit should use those.
11. Generic "audit a safety behaviour in Gemma 3 with Gemma Scope 2" or SAEBench-style evaluation of the
    release. REJECTED: no specific question, not a follow-up to a finding; GDM's technical report covers
    standard metrics.
12. Stability-filtered fine EP dictionaries (the paper's own future work). FOLDED into 01 as an optional arm
    (cheap once the ladder exists).
13. Gemma Scope 2 crosscoder vs EP for base-vs-IT diffing. REJECTED: the released crosscoders are cross-layer,
    not cross-model, so the comparison does not exist off the shelf.

## 4. Why two proposals
Two candidates cleared the bar and are clearly distinct (benchmark-validity audit of a clustering dictionary
vs a Jacobian-based naturalness score tested on ground truth and transcoders). 01 is the stronger: lower
risk, sharper question, larger audience. 02 is more speculative but cheap and uses Gemma Scope 2, which
otherwise goes unused in this cluster.
