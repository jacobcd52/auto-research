# belief-geometry — reading notes and brainstorm

Research lead notes, 2026-11-14. Caveat on search coverage: the WebSearch tool was unavailable this session
(shared budget exhausted), so related-work checks were done directly against the arXiv API, the LessWrong
GraphQL API, raw.githubusercontent.com, the Hugging Face API and the Simplex blog. arXiv coverage is decent;
non-arXiv follow-ups (personal blogs, Twitter, unlisted repos) may have been missed. A reviser with search
should re-check for (a) a Simplex "abstraction / shared factors across nonergodic components" paper and
(b) any in-context *mixture-of-HMM* probing of LLMs.

## Post 1: The Geometry of Nonergodic Composition (JfJ4WTRHmooPBWRFv, Ray/Riechers/Shai, 2026-09-10, 87 karma)
Original with interactive figures: https://belief-updates.pub/nonergodic-geometry/

Verified content
- Theory: a nonergodic composition = direct sum (block-diagonal) of component HMMs with mixture prior. The
  Bayes belief over the joint hidden state always decomposes as the concatenation of w_c * eta_c
  (w_c = posterior weight of component c, eta_c = belief over that component's states given it is active).
  Projected onto one component's coordinates the reachable beliefs form a cone: the component's own belief
  simplex scaled by w_c ("telescoping"). Prediction: "eventually sparse, multi-dimensional features".
- Experiment (single setup): two Mess3 components over the same 3-token alphabet, 50/50, BOS + 127 tokens,
  component fixed per sequence. Mess3 parameters as extracted from the blog's MathML: component 1
  x=0.15, alpha=0.6; component 2 "x=0.5, alpha=0.66" (the x=0.5 looks odd for Mess3; re-read from the blog
  before reuse).
- Model: 4-layer TransformerLens HookedTransformer, d_model=128, 4 heads (d_head 32), gated-GELU MLP width 512,
  RMS norm, rotary positions, n_ctx 128, vocab 4. Init: Gaussian std 0.02 (about 3.5x smaller than the
  TransformerLens default 0.8/sqrt(d_model) ~ 0.07). AdamW betas (0.9, 0.999), no weight decay, constant
  lr 1e-3, batch 512. Loss within ~1e-4 nats/token of optimal by step 10k and at the step-45k checkpoint.
- Result: linear map from residual stream (after block 3 of 4) to the 6-entry weighted belief vector has
  held-out R^2 ~ 0.985 (~0.99 after the final block); untrained network ~0.45 ("from recent-token features
  alone"); block 1 never rises much above the untrained level. 1-R^2 falls roughly as (excess loss)^0.6.
- Authors' own caveats / pointers: (i) footnote 10: the telescoping embedding is NOT forced; an alternative
  with one normalized geometry per component plus a separate "which component" simplex carries the same
  information in the same number of dimensions. The post only reports the joint-vector R^2, which does not
  discriminate these. (ii) "canonical low-dimensional representations emerge most cleanly when we initialize
  weights to be small" (rich vs lazy regime). (iii) Named future directions: many components with partially
  shared structure; components with internal factorization ("should discover those parts"); continuum of
  components (bag of coins; "subject of a post to come"); refinement of the SAE picture ("sparse dense
  subspaces").
- No code or checkpoints are linked from the post. LLMs were used to run the experiments.

Comments (read all)
- Andy Arditi: shared structure across components ("personas" = sampled human minds) is the interesting case.
  Eric Michaud: Simplex is "thinking a lot about this direction right now" (nonergodic components that are
  factored processes with factors shared across components).
- Paul Riechers: "We'll have some work out on this soon" — minimal model of abstraction = nonergodic
  composition + factored representations; says networks learn shared subspaces reused across scenarios as
  combinatorics push against available dimensions. => HIGH SCOOP RISK for any toy "shared factors" project.
- Sam Bright-Thonney: what happens when the number of components exceeds capacity (task-diversity threshold,
  memorizing vs generalizing ICL; cites arXiv 2412.01003 and 2306.15063)? Riechers: actively working on it.

## Post 2: Generalized belief states in transformers (4f9p7brLdnTMFuwfB, Artemy Kolchinsky, 2026-10-31, 74 karma)
Verified content
- Defines a generalized belief state (GBS): low-dimensional state that is sufficient for next-token
  prediction and recurrently updatable; no reference to a ground-truth HMM; maps may be nonlinear. Linear
  GBS = generalized HMM, found by SVD of the Hankel matrix. Proposition: recurrent + next-token-sufficient
  implies sufficient for the whole future.
- Key architectural point: a transformer's recurrent state is the KV cache (plus current token), NOT the
  residual stream. "GBS abstraction" = decoder D (cache -> GBS) and encoder E (GBS -> cache) that commute with
  prediction and update.
- Running example MRRXOR (RRXOR plus random hidden-state jumps with probability eps; 5 hidden states;
  the next-token distribution depends only on one belief direction, "PC3", while the full belief is 4-D).
- Transformer: 4 pre-LN layers, width 64, one attention head of width 8, ReLU MLP 256, RoPE, BOS, 32-token
  contexts, 100k Adam updates, batch 512, lr 1e-3 warmup+cosine. Recurrent state at position 16 is
  1,027-dimensional. Decoder: 8 learned queries per layer through the model's own attention + MLP
  (34,052 params). Encoder: affine map from 4 GBS coords to a 16-entry cache (5,135 params). Shows the
  decoded geometry matches the GHMM and that writing an encoded state into the cache steers subsequent
  predictions (single qualitative steering figure; no quantitative table in the post).
- Section 5 critique of Shai et al. 2024: belief states are "not always recovered with high fidelity from the
  residual stream"; in the author's repo the held-out R^2 on MRRXOR depends on architecture and split.
  Hypothesised reasons the residual stream often does contain beliefs: it writes the keys/values, and the
  cache "leaks" into it, more so with more layers/heads/width. Footnote: for Mess3 the belief is an affine
  function of the next-token distribution, so recovery there is expected.
- Suggested future work: structure of the learned decoder/encoder (how GBS is spread over layers, heads,
  positions); position-dependent encoder; why transformers are biased to low-dimensional recurrent
  representations.

Comments
- Vadim Fomin: toy transformer on an automaton with a hidden bit (https://wadimiusz.me/nerode/): the bit is
  linearly recoverable from the current residual stream when needed for the next token and, for most seeds,
  much harder to recover during stretches where it is not needed, though the model still uses it later.
  Plans a weights-only extraction.
- topological-manifold: wants the framework tested on "hard-to-fake" tasks (open models, IOI / entity
  tracking). Author agrees it is a good suggestion.
- whileitlasts: even for Mess3, linear belief recovery is not trivial because logits are not linear in the
  probabilities (colab linked in the comment).

Public artifacts (verified reachable via raw.githubusercontent.com on 2026-11-14)
- https://github.com/artemyk/belief-state — self-contained PyTorch: MRRXOR transformer training + held-out
  linear belief probes with controls. README results (eps=0.05, uniform weighting, mean +- sd over 5 seeds):
  random-split belief R^2: large (4L, d64, learned pos) 0.90+-0.04; small (2L, d32) 0.64+-0.10;
  large RoPE 0.97+-0.01; small RoPE 0.72+-0.04. Next-token-distribution control 0.97-1.00; shuffled-belief
  control ~0.01-0.02; untrained network 0.17-0.26. Position-extrapolation splits are much worse for RoPE
  (large negative R^2 for 2nd->1st half). Checkpoints are committed under runs/ (e.g.
  runs/L4_d64_rope/eps0.05/s0.pt, ~0.6 MB, pinned commit 5b5ffd193f73691d4be56f0248ffa84be459f33f).
- https://github.com/artemyk/gbs — decoder/encoder fitting (`python -m gbs fit/evaluate`,
  `examples/belief_state.py --quick --plot`); adapter supports causal softmax attention with RoPE or learned
  positions and multiple heads; BOS always visible; other model families need their own `CacheModel` adapter.
  No pretrained abstraction weights; no PyPI release.
- https://github.com/Astera-org/simplexity — Simplex's library (generative processes, training, Hydra
  configs). Not verified whether a nonergodic-composition process class is included; it is ~30 lines to write.
- https://github.com/adamimos/epsilon-transformers — older Shai et al. 2024 code (TransformerLens).
- github.com HTML/API is blocked from this sandbox; raw.githubusercontent.com works.

## Related work and existing follow-ups (checked)
- Balcells, Lee, Rastogi, Riechers, Shai, Poncini, "Large Language Models Develop Belief State Geometry
  In-Context", arXiv 2609.17376 (2026-09-15, 87 pp). Six open LLMs (Qwen3.5-9B, Qwen3.5-4B, Llama-3.1-8B,
  Llama-3.2-3B, Gemma-4-E4B, Gemma-4-E2B) prompted with 20,000-token sequences from 40 single HMMs
  (families Mess3, Arch, Wing, Strata; letters F/Q/V space-separated so each is one token). OLS probes fit
  per sequence on positions >= 15,000 (1,000 train / 4,000 test positions), 10 sequences; peak R^2 0.83-0.99;
  controls: shuffled beliefs, random targets, NTP / log-NTP, short-suffix (0-HMM / 1-HMM) beliefs; patching
  and steering on the probe subspace; tuned lens. Converged KL to ground truth 0.009-0.018 nats on the main
  examples. Weaker on Gemma-4-E2B. Explicitly separates "level 1" inference (which process; Xie et al.) from
  "level 2" (state within the process) and studies only level 2 with ONE ergodic HMM per context. No
  mixture / nonergodic condition (the words "nonergodic" and "mixture of" do not appear in the text). No code
  URL in the PDF. Future work they list: scale dependence; factored processes.
  => "do LLMs have belief geometry at all" is DONE; "do LLMs show the telescoping geometry over sources
  inferred in context" is OPEN.
- Levinson, "Finding Belief Geometries with Sparse Autoencoders", arXiv 2604.02685: SAE + k-subspace
  clustering + simplex fitting; validated on a toy multipartite-HMM transformer; 13 candidate clusters in
  Gemma-2-9B, 5 pass a barycentric-prediction test. => unsupervised/SAE angle is partly done.
- Shai et al., "Transformers learn factored representations", arXiv 2602.02385 (ICML 2026): orthogonal
  subspaces per factor. Ehrlich et al., "Beliefs in feedback", arXiv 2611.02047 (2026-11-01): factored
  beliefs for interacting agents, with causal steering. => factorization in toys is DONE.
- Piotrowski et al., "Constrained belief updates explain geometric structures in transformer
  representations", arXiv 2502.01954: attention implements a parallelised partial Bayesian update (Mess3 family).
- Riechers et al., "Next-token pretraining implies in-context learning", arXiv 2505.18373 (nonergodic sources,
  behavioural/loss level).
- Kowalyshyn et al., "Belief or Circuitry? Causal Evidence for In-Context Graph Learning", arXiv 2605.08405:
  LLM contexts mixing random walks from two graphs; both topologies in orthogonal PCA subspaces; patching and
  steering of the "graph family" signal. Closest existing thing to in-context source inference in LLMs, but no
  ground-truth belief target and no cone/weight-scaling test.
- Dai et al., arXiv 2506.07298 (LLMs learn HMMs in context) and 2607.22646 (algorithm extraction, "Principal
  Activations Probe"). Bigelow et al., "Stories in Space", arXiv 2605.12412 (belief trajectories in stories).
- No arXiv hit for KV-cache belief decoding other than the post itself; no systematic test of which part of
  the belief state the residual stream carries.

## Prices and availability looked up (2026-11-14)
- RunPod on-demand (https://www.runpod.io/pricing): A100 PCIe 80 GB $2.09/hr; A100 SXM 80 GB $2.19/hr;
  H100 PCIe 80 GB $2.89/hr; L40S 48 GB $1.09/hr; RTX 4090 24 GB $0.89/hr; RTX A6000 48 GB $0.69/hr;
  A40 48 GB $0.59/hr; RTX A5000 24 GB $0.27/hr.
- Lambda (https://lambda.ai/pricing, prices effective 2026-11-16): A100 40 GB $1.99/hr; A6000 $1.09/hr;
  H100 (8x HGX) $4.59/GPU/hr.
- Hugging Face: Qwen/Qwen3.5-9B, Qwen/Qwen3.5-4B, Qwen/Qwen3.5-9B-Base, google/gemma-4-E4B are NOT gated;
  meta-llama/Llama-3.1-8B is gated ("manual" approval) — avoid, agents cannot obtain approvals.
  Qwen publishes residual SAEs (e.g. Qwen/SAE-Res-Qwen3.5-9B-Base-W64K-L0_50) if a stage 2 wants them.
- No API spend is needed for either proposal (white-box work on rented GPUs).

## Brainstorm (all candidates, with verdicts)
1. **Which part of the belief state is in the residual stream? (now-relevant vs future-only subspaces;
   residual stream vs KV cache)** — the two posts in this cluster disagree on exactly this, the released
   repos make it nearly turnkey, toy-scale and cheap, and either outcome is informative. WRITTEN as proposal 02.
2. **Telescoping cones for sources inferred in context by real LLMs** — combines post 1's theory with the
   Balcells et al. LLM pipeline; the mixture case is the part they set aside; strongest link to LLM
   "persona/source" inference; has a cheap behavioural gate. Higher variance than (1) but a bigger result.
   WRITTEN as proposal 01.
3. Cone vs "cylinder" test in the toy model alone (footnote-10 alternative; does the model keep tracking the
   state of a ruled-out component?). Good and cheap, but too small for a standalone post; folded into
   proposal 01 as the toy positive control and into proposal 02 as one of the processes.
4. Many components / task-diversity threshold (K = 2..1024 Mess3 components from the continuous family;
   when does the model switch from K cones to a parameter posterior?). Interesting, feasible, but Simplex has
   announced a post on the continuum case and Riechers says they are working on it; behavioural version is
   already in the ICL literature (2412.01003, Raventos et al. 2306.15063). Rejected: scoop risk + novelty
   mostly in the probe target design, which is not obvious for the "generalizing" regime.
5. Shared factors across nonergodic components (abstraction). Rejected: Simplex says a paper is coming "soon"
   and reports the main result informally in the comments.
6. Compositions with internal factorization (post's own suggestion). Rejected: near-certain outcome given
   2602.02385 and 2611.02047; low information.
7. SAEs / "sparse dense subspaces" on the toy nonergodic model (do SAE latents split by component, tile the
   cones?). Rejected as a standalone: Levinson 2604.02685 covers the method; outcome mostly a known
   tiling story. Possible stage 2 of proposal 01 using Qwen's public SAEs.
8. GBS abstraction on a real LLM task (IOI / entity tracking), as a commenter asked. Rejected for stage 1:
   the intrinsic process of an LLM has no known low-dimensional GBS, the encoder must write an entire KV
   cache, and the released adapter only supports the toy architecture; too fragile for two days.
9. GBS decoder/encoder on the Balcells in-context-HMM setting (LLM KV cache). Rejected for stage 1 for the
   same engineering reason; listed as stage 2 of proposal 02.
10. Weights-only extraction of the recurrent state (Fomin's idea). Rejected: Fomin says he is doing it; open-ended.
11. Structure of the learned GBS decoder/encoder across layers/heads (author's suggestion). Partly inside
    proposal 02 (which layers' caches carry which belief directions); not a standalone result.
12. Rich vs lazy regime (init scale) effect on belief geometry. Folded into proposal 02 as one factor.
13. Natural-text nonergodicity (language / genre / author as components; posterior-scaled subspaces in LLMs).
    Rejected: no ground-truth posterior or per-source belief state, so the cone prediction cannot be scored
    without circularity; the synthetic in-context version (proposal 01) keeps ground truth.
14. LoRA-fine-tune an LLM on a nonergodic HMM mixture and probe. Rejected: adds a training step and answers a
    less interesting question than in-context inference in the untouched model.

Why two proposals: both clear the bar, cost well under $500, and are distinct (01 = pretrained LLMs,
in-context source inference, cone-scaling test; 02 = toy transformers, where belief information lives,
residual stream vs KV cache). Shared ingredient is only the 2xMess3 process.
