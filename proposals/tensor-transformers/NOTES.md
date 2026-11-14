# NOTES — cluster `tensor-transformers` (Tensor / bilinear transformers)

Research lead notes, written 2026-11-14. Everything here was read directly (posts via `scripts/get_post.py`,
arXiv abstract pages / API, Hugging Face API, raw.githubusercontent.com, pricing pages) unless marked "not verified".

**Search limitation.** The WebSearch tool was unavailable for this session (shared budget exhausted), so the
novelty check rests on: arXiv API keyword/author queries, the author's LessWrong post list, the post comments,
the author's public repos and Hugging Face account. I did NOT do a general web search, so a follow-up published
on a blog, X, or under unusual keywords could have been missed. A reviser with search should re-check the two
novelty claims flagged "NOVELTY TO RE-CHECK" below.

## 1. The posts

### Post A — "Tensor-Transformer Variants are Surprisingly Performant" (hp9bvkiN3RzHgP9cq, 2026-01-12, 87 karma, Logan Riggs)
- Architecture. Bilinear MLP `D(Lx ⊙ Rx)` (no elementwise nonlinearity) vs SwiGLU `D(swish(Lx) ⊙ Rx)` vs
  ReLU MLP. Bilinear attention: pattern `(xQ1K1ᵀxᵀ) ⊙ (xQ2K2ᵀxᵀ)` with no softmax; the "dumbest" variant ties the
  two (squared attention).
- Experiment. Fork of an older modded-nanoGPT commit; four ~500M-parameter (18 layers, 9 heads, d=1152) models on
  FineWeb, crossing {SwiGLU, Bilinear} MLP x {softmax, bilinear} attention; compared at CE 3.0. Bilinear vs SwiGLU
  MLP: basically the same. Bilinear attention: about 4% more batches (with ~10% more parameters). Author's overall
  estimate "15% worse to 10% better".
- At GPT-2-small scale (12 layers, 6 heads, d=768) the tensor variants were "much worse"; the author attributes
  this to modded-nanoGPT hyperparameters being overfit to softmax at that size and says a larger sweep is needed.
  (The screener's summary omits this.)
- Caveats stated: softmax had a CUDA kernel (per-step speed treated as equal); bilinear attention has 2x Q/K;
  differential-attention baseline performed "100% worse" (possibly a bug); bilinear attention is
  O(seq * d_h^3) vs O(seq^2 * d_h).
- Total spend reported: about $500 on 8 H100s for all experiments.
- Stated future work: scaling laws (explicitly deprioritised), "actually doing interp w/ these models", circuits
  on tensor networks.
- Comments worth knowing: Redwood ran similar unpublished experiments in 2022 (Tao Lin); a suggestion to write a
  Triton kernel; a (self-corrected) thread on scale invariance and steering vectors; philip_b asks why CP form
  rather than a full tensor; the author confirms Q/K normalisation is NOT a tensor-network operation
  ("a small portion of the model isn't a tensor network").

### Post B — "If you're interpreting <1B parameter models, you should use a tensor transformer" (expsAXaBgiqgitFe6, 2026-09-02, 54 karma, Logan Riggs)
- Position piece: small-model interp researchers (SLT, comp mech, ARC, natural abstractions) should train tensor
  transformers; "conservatively 90% as efficient"; allows linear algebra over the whole network (tensor
  similarity paper).
- Explicit testable remark: SwiGLU and bilinear layers "have no global Lipschitz constant", so "results like
  finetuning away the normalization (arXiv 2409.13710) might not generalize to these SOTA archs since this was
  only run on single-encoder MLPs."
- Claims bilinear attention gives denser attention patterns, "a better inductive bias for eg chess or othello".
- Candid admission: "I can't even interpret a GPT-2 small sized tensor transformer"; toy algorithmic tasks are
  "STILL REALLY HARD".

### Closely related posts by the same author (read; not in the cluster)
- "When Are Two Networks the Same? Tensor Similarity for Mechanistic Interpretability" (Yzw6KDQc336CpHmGi,
  2026-05-29, 45 karma) / arXiv 2605.15183 (Gonzalez, Albuquerque, Wroe, Cohen, Riggs Smith, Dooms). Weights-only
  cosine similarity on the contracted tensor; equals expected inner product of outputs under Gaussian inputs.
  Experiments: backdoor insertion on SVHN (checkpoint-by-checkpoint heatmaps; per-class slice identifies class 9),
  catastrophic forgetting, modular arithmetic grokking, a 2-layer attention-only LM (differences seen, "we didn't
  explore what those differences correspond to"). Stated gap: "Tensor sim can tell us where the differences are
  ... but we still don't know what the difference is."
- "Ambitious Mech Interp w/ Tensor-transformers on toy languages [Project Proposal]" (GncmyuKmp526RJpmj,
  2026-05-01): toy language built from known primitives (bigrams, skip-trigrams, induction) + 2-layer attn-only
  tensor model; a Pivotal fellowship stream. So "toy language with known DGP + weight reading" is ALREADY the
  author's active programme.
- "Mech Interp is a Verifiable Task If..." (QxHuKtfGfzn8uokoR, 2026-09-21): says tensor networks do not solve the
  basis problem; working in repo `loganriggs/tensor_language` on the 500M model.

## 2. What is public (verified)

Code
- `https://github.com/loganriggs/modded-nanogpt` (training code for Post A; `train_gpt2.py`). README readable via
  raw.githubusercontent.com. Upstream README: 124M model to 3.28 val loss in 7.8 min on 8xH100 (~1 H100-hour).
- `https://github.com/loganriggs/tensor_language` — public. `model.py` (bilinear attention, rotary, multiplicative
  causal mask, no softmax), `deep_model.py` (`DeepModel` with `["attn","mlp",...]` spec, `BilinearMLP`, norm off
  by default because RMSNorm is not polynomial), `lm_train.py`, small in-repo checkpoints, tokenised corpora.
  `jacclust/` = the author's current programme (57 "ticks"): Jacobian clustering and bilinear-secant SAEs on the
  `Elriggs/gpt2-bilinear-*` checkpoints. Its SUMMARY.md reports many nulls on real models (Jacobian clustering
  reduces to input cosine on real MLPs; head-dependent attention results). `jacclust/tt_model.py` loads the
  Elriggs checkpoints; `jacclust/metric.py` implements the exact weights-only Jacobian kernel.
- `https://github.com/tdooms/tensor-similarity` — public ("tensor-mars"); `uv sync`; families
  `seed-convergence`, `curriculum-shift`, `language-similarity`, `subset-training`. README compute envelope:
  language-similarity on 2-layer checkpoints costs about 3.5 s per pair on one GPU. It pulls
  `melephant/2l-bilinear-attn-normalised-v2` (HF API returned an auth error for that repo when I queried it
  anonymously — may be private/gated; do not depend on it).
- LN-removal code: `https://github.com/ApolloResearch/gpt2_noLN` (from the abstract of arXiv 2409.13710).

Checkpoints (Hugging Face, `Elriggs/...`, all public, `config.json` + `pytorch_model.bin`)
- 500M class (18l-9h-1152): `gpt2-bilinear-sqrd-attn-18l-9h-1152embd` (bilinear MLP + bilinear attention, the
  full tensor variant; config says `bilinear_attn: true`), `gpt2-bilinear-18l-9h-1152embd`,
  `gpt2-swiglu-18l-9h-1152embd-v2`, `gpt2-swiglu-sqrd-attn-18l-9h-1152embd`, `gpt2-bilinear-swiglu-18l-9h-1152embd`.
- 124M class (12l-6h-768): `gpt2-12l-6h-768embd` (baseline), `gpt2-mlp2-*`, `gpt2-bilinear-12l-6h-768embd`,
  `gpt2-bilinear-sqrd-attn-12l-6h-768embd`, `gpt2-bilinear-swiglu-12l-6h-768embd`, `...-swiglu-sqrd-attn-...`.
  Naming is inconsistent (author says so); read each `config.json`.
- Small: `Elriggs/simplestories-bilinear-attn` (1L and 2L attention-only), `Elriggs/bilinear_atnn_only_2L_Pile`
  (2 layers, d=512, 16 heads, vocab 5000, 8.3M params, 1000 log-spaced checkpoints, 5B tokens of DSIR-filtered Pile).
- Real SwiGLU models: `HuggingFaceTB/SmolLM2-135M` (Apache-2.0; Llama architecture, hidden 576, 30 layers, 9 heads
  with 3 KV heads, intermediate 1536, `hidden_act: silu`, RMSNorm, tied embeddings, vocab 49152); `SmolLM2-360M`.
- Datasets: `HuggingFaceFW/fineweb-edu`, `SimpleStories/SimpleStories` (MIT), `roneneldan/TinyStories`,
  `stanford-crfm/DSIR-filtered-pile-50M` — all public, ungated.

Related papers (abstracts read)
- 2410.08417 Bilinear MLPs enable weight-based mech interp (Pearce, Dooms, et al., ICLR 2025). Full text checked:
  an appendix ALREADY fine-tunes away the SwiGLU gate (Swish-beta, beta -> 0 over the first 30% of 400M tokens)
  on TinyLlama-1.1B on one A40: final loss 2.217 vs 2.168 for a continued-training baseline (about +0.05), one
  schedule only, "we plan to extend this".
- 2409.13710 You can remove GPT2's LayerNorm by fine-tuning: GPT-2 small, 500M tokens, about 0.05 CE cost.
- 2507.02559 LN removal scaled to GPT-2 XL (+0.03 CE); LN-free GPT-2 family released. Both are GELU MLP + softmax.
- 2410.18613 polynomial replacements for softmax attention (from-scratch training, not conversion).
- 2504.02667 chi-nets / ODT; 2605.08934 compositional interpretability; 2605.08891 / 2510.16820 bilinear
  autoencoders; 2509.01874 SQS activation; 2305.03452 technical note on bilinear layers; 2605.24033 verifiable
  transformers (LN removal on a sparsemax/LeakyReLU GPT-2-scale model).
- arXiv queries that returned nothing relevant after Post A: "bilinear attention" + interpretability, "tensor
  network" + "mechanistic interpretability" (only 2505.20132 position paper), bilinear + "weight-based".

Prices looked up 2026-11-14
- RunPod community cloud per GPU-hour: RTX 4090 $0.34, A6000 $0.33, RTX 5090 $0.69, L40S $0.79, A100 PCIe $1.19,
  A100 SXM $1.39, H100 PCIe $1.99, H100 NVL $2.59, H100 SXM $2.69. (Secure-cloud figures on the same page:
  H100 PCIe $2.89, A100 PCIe $2.09.)
- Lambda on-demand: H100 SXM about $4.59-4.79, A100 40GB $1.99, A6000 $1.09.
- OpenRouter per 1M tokens (in/out): claude-haiku-5.5 $0.10/$0.50, claude-sonnet-5.5 $2/$10,
  claude-fable-5.2 $8/$40, gemini-3-flash-preview $0.50/$3. (Neither proposal needs much API spend.)

## 3. Brainstorm (all candidates, with verdicts)

1. **Tensorize a pretrained SwiGLU LLM by fine-tuning; per-component cost ladder (gate, softmax, norm).**
   Extends the TinyLlama gate-removal appendix (MLP only, one schedule) to attention and normalisation, and tests
   Post B's explicit conjecture that norm removal may not transfer to GLU architectures. Cheap (SmolLM2-135M on one
   GPU), clear metric (CE vs continued-training control), informative either way, yields a reusable artefact.
   Risk: softmax -> polynomial attention conversion may not converge well; that is itself the finding.
   NOVELTY TO RE-CHECK: nobody has converted pretrained softmax attention to bilinear attention, or removed
   RMSNorm from a SwiGLU model. -> PROPOSAL 01.
2. **Head-to-head: does the tensor architecture make a concrete audit (data-free backdoor trigger recovery)
   easier than a standard architecture with generic methods?** Directly tests Post B's "you should use a tensor
   transformer". Tensor similarity paper did detection on SVHN and stopped at "where, not what"; trigger/target
   recovery in language tensor-transformers, against strong generic baselines (weight-diff SVD, trigger inversion
   by search) on matched standard models, is not done. Small models, cheap. Risk: method-building; strawman
   baselines. NOVELTY TO RE-CHECK. -> PROPOSAL 02.
3. **Fair-hyperparameter rerun at GPT-2-small scale** (is the "much worse" result at 124M a tuning artefact?).
   Feasible: about 1 H100-hour ($2-2.7) per 124M run, so a 60-run sweep is about $160 before margin. A natural
   next step and the "90% as efficient" figure in Post B rests on one size. Rejected for a slot because (a) the
   author explicitly deprioritises scaling/perf work, (b) a result of the form "gap shrinks from X% to Y% after
   tuning" is modest, (c) sweeps on an old fork with 8-GPU DDP assumptions are fiddly. Good third choice if a
   reviser wants to swap; could be folded into proposal 02 as a by-product (matched small models are trained there).
4. **Reverse-engineer a toy algorithmic / toy-language tensor transformer from weights.** This is the author's own
   active programme (Pivotal stream, `tensor_language`, 57 ticks with many nulls). Open-ended, hard to score, high
   over-claiming risk, and likely duplicates in-progress work. Rejected.
5. **Verify a hand-written circuit with tensor similarity** (write the Fourier modular-addition algorithm as a
   tensor, compute similarity to the trained model). Elegant but the tensor-similarity paper already covers
   modular arithmetic frequencies and claims "verifying faithfulness" in the abstract; marginal novelty, niche.
   Rejected (partly absorbed into proposal 02's use of tensor similarity).
6. **Scale tensor similarity to the released 124M / 500M checkpoints** (e.g. seed-to-seed or fine-tune diffing).
   Unclear numerics at depth 12-18 (polynomial degree 2^L; the recursive algorithm's cost and conditioning at
   that depth are not documented), only one seed of each released model. Too risky as a core plan. Rejected.
7. **Othello/chess inductive-bias claim** (bilinear attention better on board games). Cheap, but a narrow
   capabilities-flavoured comparison with little safety interest. Rejected.
8. **Scale-invariant steering in tensor transformers** (comment thread). The commenter retracted the main idea;
   what is left (smoothness of steering response) is thin. Rejected.
9. **Triton/CUDA kernel + O(seq d_h^3) bilinear attention benchmark.** Engineering, not safety research. Rejected.
10. **Differential-attention baseline debugging** (the "100% worse" result). Bug-hunt; low interest. Rejected.
11. **SAE / transcoder comparison on tensor vs standard 124M models** (are SAE features cleaner on the tensor
    variant?). The author's bilinear-secant SAE line is in progress; activation-SAE comparisons across
    architectures are confounded by loss differences at 124M (tensor variants much worse there). Rejected.
12. **Distil a real LLM on a narrow task into a small tensor network ("task-AI")** and audit it. Appealing
    framing from both posts but too many moving parts for 2 days; no clear success metric. Stage-2 material for
    proposal 01. Rejected for stage 1.

## 4. Why two proposals
Both clear the bar and are distinct: 01 is a conversion/training study on a real pretrained model (does the
tensor form cost anything after pretraining; does norm removal transfer); 02 is an interpretability-payoff study
on small models (does the tensor form buy anything on a concrete audit). Ordered 01 first because its pipeline
is simpler and its success criteria are less dependent on method-building.
