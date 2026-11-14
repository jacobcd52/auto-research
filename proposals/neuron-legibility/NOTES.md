# NOTES — cluster `neuron-legibility` (Are neurons already clean? Evaluating neuron explanations)

Written 2026-11-14. Sources read directly: the three cluster posts and their top comments (LessWrong GraphQL),
Cammarata's essay (already-clean.goodfire.com), Goodfire's follow-up technical report and its public atlas data files,
two later LW posts, arXiv abstracts/HTML, the bonsai-interp README/FINDINGS, Hugging Face API, OpenRouter price list,
RunPod pricing page. **Caveat: the WebSearch tool was unavailable for this session (shared search budget exhausted),
so the prior-work check relied on a listing of all LW posts since 2026-10-10 filtered by title keywords, arXiv API
keyword queries, and following links from the posts. A Twitter/X-only or non-arXiv follow-up could have been missed.**

## 1. Reading notes

### Post 1 — Linkpost: Neural Networks Are Already Clean (x4kvabkF2Jk8GLZp8, 220 karma, Yair Halberstadt, 2026-10-15)
- Only quotes Cammarata's and roon's tweets; asks how real the advance is and how it helps alignment.
- The linked essay (https://already-clean.goodfire.com/, Nick Cammarata, Goodfire): vision models (InceptionV1 retrained,
  ConvNeXt 92k/7M/28.6M params, DINOv2) and LMs (Qwen3-32B audit, a dense Qwen, Kimi K3). Headline LM numbers:
  "roughly 90% of neuron poles have one main job", ~7% two related jobs, 2-4% unexplained; "closer to 97%" for strong
  activations (small samples). Claims weak activations rarely matter: in medium ConvNeXt, removing weakest 75% of
  activations moves accuracy 72%->71%; removing strongest 7% -> 4%. Argues older simulation-score metrics are "too
  demanding". Proposes "recursive generalization" instead of superposition. Each SwiGLU neuron has a positive and a
  negative pole, read separately.
- Comments worth noting: Neel Nanda and StefanHex sceptical of "neurons is all we need", worried that max-activating
  examples tell an incomplete story; johnswentworth wants a full neuron-by-neuron artifact; Manic Pixie: most neurons
  having one concept != most concepts having a neuron; Julian Bradshaw spot-checked claims against "the 1000 Qwen3
  neurons he provided data for".

### Post 2 — Neural networks are not already clean (Dkh7pXKjoNWkkxQDz, 368 karma, leogao, 2026-10-17)
- Two specific failure modes of judging a neuron by its activating examples:
  (a) **recall / sufficiency**: every firing fits pattern X does not imply every X fires the neuron; "very common for
  neurons that look like they activate on X to actually only activate on a very specific subset of X that is hard to
  characterize compactly. If you forced the neuron to always activate on X, it would degrade the model."
  (b) **magnitudes / weak activations**: "My best guess ... is that ablating small neuron activations quite
  substantially degrades model performance" — footnote: "It's surprising that my result here is different from Nick's,
  and it seems worth tracking down the source of the divergence." He says he hopes to share something concrete soon.
- Proposed standard: write a rubric, simulate the neuron, substitute simulated activations, measure **downstream KL on
  a large dataset** (KL, not loss delta, because errors can cancel in loss; footnote suggests comparing neurons
  relatively or substituting large batches of neurons at once since single-neuron effects are tiny).
- No experiments in the post.

### Post 3 — Twitch Plays: AI Interpretability of Bonsai-8B (ozbbzsh49wvgfbCDp, 82 karma, moridinamael, 2026-10-19)
- Claude Opus 5.5 agent + Twitch chat label neuron poles of Bonsai-8B (PrismML 1-bit model derived from Qwen3-8B;
  36 layers x 12,288 neurons = 442,368 neurons, 884,736 poles). Tests are pre-registered (committed before run), CI
  re-scores, labels can be challenged; "leak bet" inverse solver searches for text that fires the neuron without matching
  the label. Repo https://github.com/moridinamael/bonsai-interp (raw files fetchable via raw.githubusercontent.com;
  github.com HTML returned 403 from this sandbox), map https://moridinamael.github.io/bonsai-interp/.
- From README/FINDINGS.md: toolchain loads exact 1-bit weights; corpus scan of 8M tokens takes ~1 GPU-hour on an 8 GB
  GPU; a "sweep" of 16 poles costs ~$1 of agent usage; `scripts/download_models.sh --all` fetches the precision ladder
  (prism-ml/Bonsai-8B-unpacked, prism-ml/Ternary-Bonsai-8B-unpacked, Qwen/Qwen3-8B). FINDINGS 2026-10-17: neuron
  identity survives QAT in layers 5-33 (best-match-is-same-index 92-99% for 1-bit vs Qwen3-8B, 47% at L35), so the
  ladder is a paired comparison; perplexity 28.7 / 32.7 / 36.7 (FP / ternary / 1-bit) on one passage. Pilot: 19 of 24
  poles "one main job" on first reading (not blind-tested).

### Follow-ups that ALREADY exist (must not duplicate)
- **Goodfire technical report, "Neurons as an Interpretable Basis"** (Tigges, Kowal, McGrath, Lewis, Cammarata;
  2026-11-10; https://www.goodfire.com/research/neurons-as-an-interpretable-basis ; markdown at .../article.md; LW
  linkpost GPDhwwsFoZGwbcvdS, 29 karma). Model: **Qwen3.6-35B-A3B** (MoE: 40 layers, 256 experts/layer, 512
  neurons/expert, 8 routed + 1 shared expert per token; ~5.26M routed neurons). Verified details:
  - Weak-activation ablation: keeping router-weighted top-320 of 4,096 routed neurons per token per layer (ablating
    92.2%) gives loss 1.940 vs 1.886 (+0.054, "2.9%") and **KL 0.140** on 8.4M web tokens; top-64/expert: +0.066, KL
    0.152; top-32: +0.146, KL 0.263; P25-P75 mean-ablation: +0.010. Non-reasoning benchmarks near parity; reasoning
    evals fail through loops unless lightly fine-tuned (91M SFT + 9M RL tokens). **MoE only; no dense model.** They say
    "Weak activations may not be entirely irrelevant ... we leave investigation of them to future work."
  - Description evaluation: detection (Opus 5.5 picks the firing snippet of a pair; control snippet is one where the
    neuron stays below its p90, drawn from same-expert or random text): 0.914 all bands, 0.946 vs random, 0.885 vs
    same-expert, 496 poles. Simulation (486 poles): simulator model "Jev" predicts token-level activations from the
    description, these are substituted, and KL damage recovered is reported relative to a "10-level oracle ceiling":
    **p97-99 not evaluated; p99-99.9: 56%; p99.9-99.99: 64%; p99.99+: 76%; top-1000: 73%**; the headline 73% pools only
    bands >= p99.9. Evaluation windows are sampled **conditional on the neuron firing**, plus 40 random corpus windows
    per pole "to measure the damage caused when the simulator predicts firings that should not occur". Input synthesis:
    for 94% of neurons generated text beats the max in a 10B-token corpus (primary mode only). Descriptions are produced
    by an agent ("Neuron Scientist": Fable 5.0/5.1, Opus 5.5 or GPT-6 Sol) that explicitly optimises KL-recovered on a
    training split.
  - **What it does NOT test**: text that matches the description but on which the neuron is silent (leogao's failure
    mode (a)). Controls are random/same-expert text, which almost never contains the described concept; firing windows
    are sampled by the neuron, not by the description. No simulation below p99; no dense model.
  - **Public atlas** (verified by download, gzip-compressed JSON served from static.goodfire.ai):
    base `https://static.goodfire.ai/neuron-atlas/2026-11-09-082204/`
    - `public_atlas_data/index.json`: 3,244 neurons / 6,488 poles with category and one-line description
      (categories: mono 4,042; poly 1,922; dark 346; none 178). Layers 4, 9, 14, 19, 24, 30, 36, 39 (838 neurons in L14,
      ~320-360 in each other layer).
    - `subcircuit_modes_index.json`: 5,477 poles with verdict (2,122 monosemantic / 3,355 polysemantic), modes with
      labels and firing shares, `main_damage_share`.
    - `subcircuit_modes_data/<pid>.json` (pid like `L14_E100_N452__pos`): firing threshold `theta`, per-mode
      descriptions, subcircuit readings, `kl_neuron_mean`, unified description, judge accuracies.
    - `public_atlas_data/islands/poles/<pid>.json`: example windows with **per-token activations**, `act`,
      `a_over_theta`, focal index; Opus mode predicates.
    - `ns11_pages/data/index.json`: Goodfire's own **simulatability score for 585 poles** (median 0.61, IQR 0.50-0.73,
      2% negative, 74% above 0.5; 290 pos / 295 neg; 57-90 per layer).
    - No code, no corpus, no weights hooks released; simulator "Jev" is not a public model as far as I could find.
- **neverix, "Takes on 'Already Clean'"** (p6kaX6LqfTHFqC6r6, 26 karma) + paper arXiv:2610.24521 "Comparing Sparsified
  MLPs and Transcoders: Many Transcoder Features Are Neurons in Disguise" (Gemma 3 1B/4B/27B, Gemma 2 2B, Gemma 4 26B
  A4B, Qwen 3, Llama 3.1 8B / 3.2 1B). Sparsifies MLP activations layer-wise with top-k ~32-64 **plus a learned linear
  correction**, per-layer replacement; quotes "L0 about 32 per layer/token with KL around 0.5 (transcoders ~2.0)". Says
  "preliminary evidence that MoE MLPs are only usable at a lower sparsity", low activations out of scope. Doubts the
  descriptions can be used for enumerative safety.
- Arora, Wu, Steinhardt, Schwettmann, arXiv:2601.22594 "Language Model Circuits Are Sparse in the Neuron Basis"
  (task circuits of ~10^2 neurons; not a global weak-activation ablation). OpenAI 2023 neuron-explainer (correlation
  simulation scores; revisions section) is the original baseline. arXiv:2512.18092 "Faithful and Stable Neuron
  Explanations" and CoSy (2405.20331) evaluate explanations on synthetic/vision inputs, not LM-neuron recall on natural
  text.
- Bonsai repo itself does pre-registered positive-vs-near-miss sentence tests and "leak bets" per label — i.e. a
  small-scale synthetic recall/precision check, but no aggregate natural-text recall number and no causal (KL) scoring.
- Not found: any independent third-party re-scoring of the Goodfire atlas; any dense-model replication of the
  weak-activation ablation; leogao's promised concrete result (not posted on LW as of 2026-11-14).

## 2. Verified facts for a reviser

Models (Hugging Face API, all ungated unless noted):
- Qwen/Qwen3.6-35B-A3B — apache-2.0, 35.95B params, 71.9 GB repo. Needs >72 GB VRAM in bf16 (96 GB card, or 2x48 GB).
- Qwen/Qwen3-0.6B, -1.7B, -4B, -8B (8.2B), -14B (14.8B, 29.6 GB), -32B (dense); Qwen/Qwen3-30B-A3B (MoE, 61 GB).
- prism-ml/Bonsai-8B-unpacked (16.4 GB safetensors, apache-2.0), prism-ml/Ternary-Bonsai-8B-unpacked, Bonsai-8B-gguf.
- meta-llama/Llama-3.1-8B is gated ("manual") — avoid as a dependency.
Prices looked up 2026-11-14:
- OpenRouter ($/M tokens in/out): anthropic/claude-opus-5.5 4/20 (batch 2/10); claude-sonnet-5.5 2/10 (batch 1/5);
  claude-haiku-5.5 0.10/0.50; claude-fable-5.2 8/40 (batch 4/20); openai/gpt-6.1-terra 1/5; openai/gpt-6-luna
  0.10/0.50; google/gemini-4-hydrogen 1.5/7.5; qwen/qwen3.6-35b-a3b 0.10/0.90 (hosted inference only, no activations).
- RunPod on-demand: RTX Pro 6000 96 GB $2.69/h; H100 PCIe 80 GB $2.89/h; H100 NVL 94 GB $3.19/h; A100 PCIe 80 GB
  $2.09/h; H200 141 GB $5.29/h; L40S 48 GB $1.09/h; RTX A6000 48 GB $0.69/h; A40 48 GB $0.59/h; RTX 4090 $0.89/h.
Other:
- Goodfire detection eval window: 60 tokens before the marked token, the token, 8 after. Rerunning the model on the
  short window alone loses ~15% of exemplar firings (context matters) — any replay check must expect this.
- theta for a census pole is the census threshold; for the opposite pole 0.65 x its own p99.9.

## 3. Brainstorm (all candidates, with verdicts)

1. **Description-conditioned recall audit of the Goodfire atlas (the "X matches Y is not commutative" test).** Sample
   natural text by the *description* (retrieval + blind judge), then look at whether the neuron fires; then measure the
   KL cost of forcing it to fire there, and re-compute simulation KL-recovered under description-conditioned sampling.
   Achievable (public descriptions, thetas, examples, Goodfire's own sim scores for 585 poles; public weights; forward
   passes only; ~$400). Directly tests the one failure mode leogao names that the tech report did not test. Interesting
   either way. **-> Proposal 01.**
2. **Do weak activations matter in dense models? Reproduce Goodfire's ablation sweep across dense Qwen3 sizes, the MoE
   models, and the Bonsai precision ladder, with KL and loss.** Addresses the explicitly flagged leogao-vs-Cammarata
   divergence; Goodfire is MoE-only, neverix hints MoE differs. Cheap (~$200), simple pipeline, no LLM judging.
   **-> Proposal 02.**
3. Full leogao metric on a small dense model: auto-explain every neuron in one layer, simulate all of them at once
   over the full activation range, report KL. Rejected for stage 1: needs a description pipeline built from scratch
   (Goodfire's agent harness is unreleased) and ~10^8+ simulator tokens for a whole layer; result would be dominated by
   "our cheap explainer is worse than Goodfire's". The batched full-range simulation idea is folded into Proposal 01
   on Goodfire's own descriptions instead.
4. Audit the Bonsai map labels with causal scoring. Rejected as a standalone: the repo already runs pre-registered
   tests and QC, the map is small and crowd-driven, labels are one-liners written for sentence tests rather than
   simulation, and the audience is smaller (82 karma). Bonsai is used in Proposal 02 as a paired precision ladder.
5. 1-bit vs full-precision legibility comparison (are Bonsai neurons cleaner/sparser than Qwen3-8B's?). Partly folded
   into Proposal 02 (sparsity/weak-activation dependence across the ladder). A description-quality comparison would
   need the missing explainer pipeline (see 3).
6. Independent re-derivation of the "90% of poles have one main job" number with a blind agent on a dense model.
   Rejected: the number depends on rater thresholds ("what counts as one thing"), which is exactly what the critique
   says is unreliable; a second vibes-based percentage would not move anyone.
7. Recursive generalization vs superposition by watching neurons across training checkpoints. Rejected: needs
   checkpoint series of a real LM plus an explainer; multi-week scope; neverix says he is already looking at Olmo.
8. Manic Pixie's question — what fraction of *concepts* (e.g. SAE/transcoder features, or a list of entities) have a
   dedicated neuron? Interesting, but arXiv:2610.24521 already measures the transcoder-feature-to-neuron
   correspondence across 13 transcoders; an entity-list version is a plausible stage 2 of Proposal 01, not a stage 1.
9. Alignment-relevant neuron search (RogerDearnaley: emergent-misalignment "toxic persona" neurons). Rejected here:
   already active elsewhere (persona-neuron and refusal-neuron work cited by neverix: arXiv:2605.08513,
   willmayner.com/persona-neurons), and it does not test the cluster's central dispute.
10. Reproduce Goodfire's simulation score exactly for the 585 scored poles. Rejected as the main aim: "Jev" and the
    corpus are not public, so an exact reproduction is impossible, and a near-reproduction is low-information. A
    firing-conditioned arm is kept in Proposal 01 only as a calibration baseline.
11. Colorado/Tornado-style rare-mode hunt (how many neurons have a hidden unrelated mode?). Goodfire's mode-clustering
    already does this at scale on 5,477 poles; duplicate.

## 4. Why two proposals
Both clear the bar: each isolates one of leogao's two named failure modes, each reuses public artifacts, each is
forward-pass-only, and each gives a number the two camps disagree about in advance. They are distinct projects
(01 = are the descriptions sufficient conditions, on Goodfire's MoE atlas, LLM-judge heavy; 02 = do weak activations
carry causal weight, dense vs MoE vs quantised, no descriptions or judges at all).
Main shared risk: leogao or Goodfire publishes the same measurement first; both proposals are still useful as
independent replications on public artifacts.
