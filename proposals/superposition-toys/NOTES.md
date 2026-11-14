# superposition-toys cluster: reading notes and brainstorm

Written 2026-11-14. All four cluster posts were read in full via `scripts/get_post.py` (and, for numbers lost when
MathJax is stripped, via the LessWrong GraphQL `contents.markdown` field). Follow-up search: LessWrong GraphQL
(comments on the cluster posts; every post by the cluster authors; title scan of all posts in the windows
2025-12-10..2026-02-20 and 2026-05-01..2026-11-14), the arXiv API, and raw.githubusercontent.com for repo READMEs.
**The WebSearch tool was unavailable (session search budget exhausted), so there was no general web search.**
github.com HTML pages return 403 from here; raw.githubusercontent.com works.

## 1. What the four posts say (verified against the text)

**Rotations in Superposition** (LZ7YMPJueB6qjL24n, Linsefors & Bushnaq, 2025-12-15, 54 karma).
Hand-codes a ReLU MLP of width D that implements T conditional 2-D rotation circuits in superposition, to test the
"Circuits in Superposition 2" construction (post FWkZYQceEzL84tNej). Each small circuit has d=4 neurons per layer,
L=6 layers (5 rotations): two neurons re-compute a Boolean on-indicator alpha through a step function, two rotate
x by a per-circuit random angle if alpha=1. Headline network: D=1000, T=557 (so T*d > D), each circuit neuron spread
over S=6 network neurons; inputs have z=1,2,3 active circuits. Results: average circuit beats the trivial baseline
(|dx|>=1) for the first 3 of 5 rotations (4 if z=1); worst case: all circuits OK for 2 rotations at z=1, 1 at z=2,
and at z=3 at least one circuit fails immediately. Errors grow superlinearly with depth ("seizure": noise switches
on extra ReLUs); the theory's linear prediction holds only while errors are small. Key variables: T d^2/D^2, z, L.
Takeaway: "independent circuits in superposition are costly"; fitting T ~ 2D/d was already hard, far from the
asymptotic T = O~(D^2/d^2). Speculation: memorised look-ups are shallow and share neurons when they share an
answer; Lucius reports that in parameter decompositions of GPT-2 Small it is rare to have more rank-1 circuit
pieces than neurons per layer. No experiments on trained networks and none with interpretability methods.
Code: https://github.com/LindaLinsefors/Rot-in-Sup (README fetched; `plots_for_post.py` builds the T=557, D=1000,
d=4 network on CPU from `classes_and_functions.py` (`CompInSup`, `RotSmallCircuits_4d`) and `assignments.py`).

**A tale of three theories** (siu22scEfuKxpSgfK, Vaintrob, 2026-01-25, 63 karma). Informal. Task: denoise a 2-hot
or 3-hot boolean vector plus small Gaussian noise through Linear(d->h) | phi | Linear(h->d), phi(x)=tanh(x)^3, no
biases, re-balanced loss (plain MSE degenerates to outputting zero), effectively infinite data. With h>d (no
superposition) weights converge to a few exact values; with h<d (shown: h=1024, d=3072) encoder weights fall into
three clusters (around 0 and about +-1.5) and the sign matrix S in {-1,0,1}^(h x d) is claimed to be essentially iid
random with a theory-predicted density p (same sign within a row); the continuous weights are then perturbed by
"pinning fields" from that frozen disorder, predicted Gaussian within clusters (visibly not quite Gaussian at this
size). Mean-field theory is "in the background" and not given; a formal paper with Zohar Ringel is planned. GELU +
softmax-loss variant shows correlated blobs ("2-particle mean field"); h=512, d=768 shows unexplained regular
structure. Stated next steps: features with different importance/size/noise or correlations; deeper sparse boolean
computation (Adler-Shavit arXiv 2409.15318). Code: https://github.com/mvaintrob/clean-denoising-experiments
(README fetched: `python main.py config.json`, example configs in `nice_stuff/`).

**Neural Networks learn Bloom Filters** (buxBdp8NtHGgBwabv, Alex Gibson, 2026-05-09, 64 karma).
Task: sample k distinct tokens n_i from a vocab and weights alpha_i > l > 0; input x = sum_i alpha_i W_E[n_i]
(W_E learned); 1-layer residual ReLU MLP; minimise KL to the uniform distribution on the k tokens. Trained config:
d_vocab=5000, d_model=d_hidden=256, k=10, alpha in [0.5, 3.0], 500,000 steps, batch 4096, AdamW, cosine LR from
2e-3, bfloat16; final total-variation distance 0.031. Findings: W_E*mlp_in entries are bimodal (about 0 or about
3.0) = a binary hash per token; the negative-entry mask of W_U*mlp_out-side matrix is exactly the transpose of the
hash mask; hidden layer clamps the union of hashes to a near-indicator; outputs fall in two clusters (clean, or one
false positive sharing mass ~uniformly); tokens missing the union by one hash bit get ~1% mass; in 100,000 sets no
token not fully covered got >0.03; a one-bit miss costs about -1.75 logits. Hand construction: token i gets a
random size-d subset S_i, W_E = T on S_i, mlp_in = Id, mlp_out = -Id, uniform negative bias, W_U = W_E^T; width
O(k log(d_vocab/eps)). Admitted gaps: predicted per-token logit spread is +-0.5, which under-predicts how uniform
the real output is; no proof. Observation: within a forward pass overlapping hashes are *good* (smaller union).
Author's further work: (1) fully understand the 1-layer model; (2) "What is the scaling for the density of the
hashes that the model learns? How does this relate to theoretical Bloom filter density?"; (3) what do real LLMs do.
**No code link in the post** (checked markdown for URLs). Only comment: Lucius Bushnaq, "would like more of this".

**Challenge: Hand coding weights for efficient sequence memorisation** (KWtchKwwnJkd4bwCi, Linsefors & Bushnaq,
2026-07-23, 65 karma). Random (token1, token2) -> label facts; architecture for the challenge: two embedding
matrices summed -> ReLU (d neurons) -> unembedding, no bias/norm/residual; n_input_vocab=2d, n_output_vocab=d.
Ablation at d=16: the MLP matters most (+60% to +373% facts); attention is no better than summing two embeddings.
Trained capacity ~ d^2/log d. Fits (Fig. 5): acc=1: trained 5.66 d^2.06/log d, hybrid 1.56 d^2.07/log d,
hand-coded 2.17 d^1.55/log d, rand-emb 0.151 d^2.24/log d; acc>=0.9: trained 9.42 d^1.97/log d, hybrid
2.20 d^2.02/log d, hand-coded 1.16 d^1.93/log d, rand-emb 0.278 d^2.21/log d. Headline gaps: hand-coded 9.7x and
hybrid 3.5x below trained at 90% accuracy; at 100% accuracy hand-coded is ~27x below at d=128. Construction: each
label owns S ~ sqrt(d) neurons; embeddings in {-1,0,1} chosen so all of a label's neurons are *inactive* on its
facts; readout weight -2. Trained nets instead use patterns of *active* neurons; at moderate load their embedding
weights are trimodal. Appendix A: exact construction for d = n_input_vocab+1. Dugan et al. (arXiv 2512.00207,
"Constructing Efficient Fact-Storing MLPs for Transformers") is a better construction the authors found late.
Code: only `hand_coded_models/hc2.py` is cleaned
(https://raw.githubusercontent.com/LindaLinsefors/Memory-Toy-Models/master/hand_coded_models/hc2.py, 21.5 kB, HTTP
200; repo has no README).
Comments (important): **Lucius, 2026-07-29: "Dan Braun and me have had a lot of success ... getting agents to grind
on the challenge ... They've already found hand-coded solutions that IIRC seem to perform basically as well as the
trained solutions, sometimes a little better. I've now switched to having them hunt for solutions that also look
like the trained solution ... Waiting to post any of that until I've verified it".** Nothing posted by 2026-11-14.
Logan Riggs: closed-form-ish solution for bilinear layers, could not transfer to ReLU. Jesse Li: Appendix-A
extension storing ~1/4-1/2 of all pairs. Ameya Panchal: the "MLP+norm, no residual, no bias, ReLU" outlier is a
trainability failure (transplanted weights reach 100% on 672 facts vs trained ceiling 504; out-bias rescues it);
https://github.com/Ameya-bit/mem-toy-scratch.

## 2. Related / later work found
- Ferreira da Silva et al., "Compressed Computation under L4 Loss is likely Computation in Superposition"
  (LW cTRKj3giaZN5Ysyx2, 2026-07-15; arXiv 2607.04800; code github.com/FranciscoHS/toy-model-cis-code, README on
  `master` returns 200). First *trained* CiS toy: 50 ReLU neurons computing ReLU of 100 sparse features; trained
  solution = sparse binary codeword over 5-7 neurons per feature, decoder ~ scaled pseudoinverse; 3-scalar
  description recovers the loss. They note the original compressed-computation model was built as a testbed for
  parameter decomposition and then shown (Bhagat et al., LW ZxFchCFJFcgysYsT9) not to contain CiS; using their new
  model as a PD ground truth is "what we plan to use it for next". So as of July 2026 there was no published test of
  parameter decomposition on a network known to compute in superposition.
- Linsefors & philh, "MSE loss does not generate superposition" (cfwAK4Qvjne4RjB74, 2026-07-27): Linda has been
  training CiS toy models with noise; MSE gives no pressure towards superposition; use L4 or cross-entropy.
- Goodfire parameter decomposition: SPD (arXiv 2506.20790), VPD ("Interpreting Language Model Parameters", LW
  eAQZaiC3PcBhS4HjM, 2026-05-05, 164 karma), "Exploration: fine-tuning with parameter decomposition"
  (ieoWstubDQWLrMnhH). Code https://github.com/goodfire-ai/spd (README and docs/skill.md fetched): library
  `param_decomp/` (JAX), core trainer is target-agnostic via a `DecomposedModel` protocol
  (`param_decomp/core/model.py`); ships TMS and ResidMLP toy targets with runnable roots
  (`param_decomp/experiments/tms/run.py`, `.../resid_mlp/run.py`), plus LM targets; `docs/handbook.md` and
  `docs/skill.md` are written as agent-facing guides to implementing a new target. SPD v1 (PyTorch) release:
  https://github.com/goodfire-ai/param-decomp/releases/tag/v1. (README links a `nano_param_decomp/` folder; its
  README path returned 404, so do not rely on it.)
- Alex Gibson, "Ping pong computation in superposition" (g9uMJkcWj8jQDjybb, 2025-12-29): zero-error z=1
  construction with T = D^2/d^2.
- arXiv 2605.12426 "Geometric Factual Recall in Transformers" (2026-05): structured (bijection) facts need only
  logarithmic embedding dimension; the MLP acts as a relation-conditioned selector. Relevant to "structured facts".
- arXiv 2512.00207 (Dugan et al.): encoder-decoder construction matching GD facts-per-parameter asymptotics.
- Other superposition posts in the window (not follow-ups to the cluster): "Deep models reveal better strategies
  for superposition" (CTnWy28cGYkeEjFWL), "How much superposition is there?" (JawMNDrcRsRrDcXFd), "Confirming
  Claims of Superposition and Adversarial Examples in Toy Models" (rwu73dCE3uWjieijK).
- Found no follow-up to the Bloom-filter post (no later post by Gibson; arXiv query "Bloom filter" AND
  superposition returned nothing), no trained-network or interpretability follow-up to Rotations, and no public
  follow-up post to the memorisation challenge or the frustration post (Vaintrob's later posts are on NN-Bayes
  circuit priors and the PIRAMID agenda).

## 3. Prices looked up (2026-11-14, runpod.io/pricing, on-demand pods)
RTX A5000 24 GB $0.27/h; RTX 3090 $0.50/h; A40 48 GB $0.59/h; RTX 4090 24 GB $0.89/h; L40S 48 GB $1.09/h;
RTX 5090 $1.39/h; A100 PCIe 80 GB $2.09/h; H100 PCIe 80 GB $2.89/h. No API spend is needed for either proposal.

## 4. Brainstorm (all candidates, with verdicts)
1. **Parameter decomposition on the hand-coded Rot-in-Sup network (known ground-truth circuits).** Screener's
   suggestion. Both codebases public; nobody has published PD on a verified CiS network; result matters either
   way to the PD agenda. Risk: PD tuning. -> **Proposal 01.**
2. **Bloom filter: hash-density law, phase boundary, structured (Zipfian / real-LM) top-k sets, finishing the
   mechanism.** Directly the author's open questions 1-2; tiny models; no code released but the spec is complete.
   -> **Proposal 02.**
3. Better hand-coded memorisation constructions. Rejected: the authors' own agents reportedly already match
   trained capacity (unpublished); Dugan et al. exists. High scoop risk, low marginal value.
4. Reverse-engineer what trained memorisation MLPs do. Rejected for the same reason (the authors have switched
   their agents to exactly this).
5. Memorisation capacity with structured or non-uniform facts (bits rather than fact count; Zipfian labels;
   shared answers). Feasible and cheap, tests the Rotations-post speculation that same-answer look-ups share
   neurons. Not written up: the outcome "capacity tracks label entropy" is what information theory predicts, and
   arXiv 2605.12426 already covers structure-exploiting recall; unlikely to clear 50 karma on its own.
6. The norm/no-bias outlier architecture. Rejected: already explained in comments (Ameya Panchal).
7. Bilinear-layer closed form. Rejected: Logan Riggs has done it informally and could not transfer it to ReLU.
8. Train (rather than hand-code) networks on the conditional-rotation task and compare capacity. Tempting
   (the post's "CiS is costly" claim rests on an admittedly sub-optimal construction) but rejected: five rotations
   by theta compose into one rotation by 5*theta, so a trained network need not compute layer by layer and the
   comparison stops meaning "multi-layer CiS"; fixing that needs a new, non-collapsible circuit family (new
   environment); and Linda is already training CiS toys (MSE post). Kept as a stage-2 item of proposal 01
   (decompose an L4-trained network).
9. Add active error correction to the rotation construction. Rejected: construction/theory work the authors
   flag as their own next step; less suited to a 2-day agent sprint and less interesting as a post.
10. Replicate/extend the frustration result (random-basin loss vs learned-basin loss; is S really iid; larger
    h,d for Gaussianity; unequal feature importance). Feasible with the public repo, but the mean-field
    predictions are unpublished, so agents could not check theory, and a formal paper is planned. Expected to be
    a niche post. Rejected.
11. Look for Bloom-filter hashing in real LLM output layers. Rejected for stage 1: no crisp operationalisation
    (Gibson himself says there is no evidence); placed in stage 2 of proposal 02 after the structured-set
    experiment says what signature to look for.
12. PD or transcoders on the trained Bloom-filter / memorisation networks. Folded into stage 2 of proposal 01.
13. A cross-toy survey of "trained superposition = sparse discrete codes" (Bloom hashes, L4 codewords, frustration
    sign matrix, trimodal memorisation embeddings). Interesting framing but diffuse; four re-implementations for a
    descriptive result. Rejected; the Bloom proposal mentions the link.

Two proposals written; they are different projects (interpretability-method validation on a hand-coded
multi-layer network vs. characterising what a trained output layer learns).
