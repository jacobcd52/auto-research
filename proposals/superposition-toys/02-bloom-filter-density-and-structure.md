# How dense are learned Bloom filters, and do they survive realistic token statistics?
cluster: superposition-toys | stage-1 cost: $150 | follows up: Neural Networks learn Bloom Filters (buxBdp8NtHGgBwabv)

## 1. What the prior work showed
Alex Gibson trained a one-layer residual ReLU network on a toy version of an output layer's job: emit a sparse
distribution over a vocabulary far larger than the residual width. A sample is k distinct tokens with positive
weights alpha_i; the input is the weighted sum of their (learned) embeddings; the target is the uniform distribution
over those k tokens; loss is KL. With vocabulary 5000, d_model = d_hidden = 256, k = 10, alpha in [0.5, 3.0],
500,000 AdamW steps at batch 4096, the network reached total-variation distance 0.031. Its weights are discrete:
the entries of W_E·mlp_in are either about 0 or about 3.0, i.e. each token gets a binary hash; the output-side mask
is exactly the transpose of the input-side mask; the hidden layer clamps the summed hashes to an indicator of
their union; a token gets top probability only if its whole hash lies inside the union. Errors are Bloom-filter
false positives (an extra token sharing the mass); a token missing by one hash bit gets about 1% of the mass.
Gibson gives a hand construction with width O(k·log(vocab/eps)) and argues it scales far better than
Johnson-Lindenstrauss-style superposition.

He lists as open: completing the mechanism (his analysis predicts a +-0.5 logit spread among the top-k, which is
too large to explain the near-uniform output); "What is the scaling for the density of the hashes that the model
learns? How does this relate to theoretical Bloom filter density?"; and what real LMs do. He also notes that within one forward pass overlapping hashes help (smaller union).

Only one configuration was trained, and no code was released. Related: Ferreira da Silva et al. (arXiv
2607.04800) found sparse binary codewords in a trained computation-in-superposition toy, and Vaintrob's
"frustration" post a random sparse sign matrix in a trained denoiser; neither studies this task. I found no follow-up to the Bloom-filter post (LessWrong title scan and author page to
2026-11-14; arXiv API; general web search was unavailable).

## 2. Question and why it matters
Two linked questions. (A) Across vocabulary size, width and k, is the binary-hash solution what training finds, and
does the learned hash size follow the Bloom-filter optimum (about (width/k)·ln 2 bits per token, union half full)
or a different law set by the KL loss? (B) When the k-sets are not uniform random but have the frequency skew and
co-occurrence structure of a real language model's top-k sets, does the network still learn discrete hashes, and
does it adapt them (shorter hashes for frequent tokens, shared bits for tokens that co-occur)?

If the density law holds and the solution is robust, the post's claim becomes a quantitative account of how a
narrow residual stream can drive a large softmax, with a signature to look for in real models. If the discrete
solution disappears under GELU, normalisation or realistic statistics, the Bloom filter is an artefact of one
clean setup and should not shape intuitions about real output layers. Part (B) could also show
hashes whose bits are interpretable token clusters, bridging "random hash" and "semantic feature" pictures.

## 3. Stage 1 plan
Small-model training on one GPU. Built: task and model (about 150 lines; the post gives all hyperparameters) and
analysis code. Reused: GPT-2 small from Hugging Face for part (B).

1. **Replicate.** Train the exact configuration with 3 seeds. Gate: TV within 0.02-0.05, bimodal W_E·mlp_in,
   transpose mask match above 99%.
2. **Measurement kit.** Bimodality score (two-component fit; fraction of entries within 10% of a mode); per-token
   hash size; union fill fraction at the trained k; false-positive rate per set; TV and KL; logit as a function of
   the number of uncovered hash bits ("tier curve").
3. **Reference solutions.** (i) Gibson's hand construction evaluated on the same loss for every hash size, giving
   the hash size that minimises the *task loss*; (ii) the classical Bloom optimum; (iii) a non-discrete baseline:
   frozen Gaussian W_E with the rest trained. The learned hash size is compared against (i) and (ii); the learned
   loss against (i) and (iii).
4. **Scaling grid (A).** width in {64, 128, 256, 512} x k in {2, 5, 10, 20, 40} x vocab in {1000, 5000, 20000},
   2 seeds (120 runs), steps reduced where loss has plateaued. Outputs: a phase map of "discrete hashes: yes/no";
   learned hash size vs (width/k); loss vs width at fixed k and vocab to test the claimed log(1/loss) width scaling
   against the Gaussian baseline.
5. **Robustness.** At the base configuration, one change at a time, 2 seeds: GELU; no residual connection;
   d_hidden in {128, 512, 1024}; weight decay 0 / 0.1; LayerNorm before the unembedding; k varying per sample
   from 1 to 20; a softmax(alpha) target instead of uniform.
6. **Structured sets (B).** (i) Zipfian token frequencies with independent draws. (ii) Real sets: run GPT-2 small
   over about 2M positions of OpenWebText, take each position's top-10 next tokens, keep sets inside the 5000 most
   frequent tokens (remapped), and train on those sets with random alpha. Measure hash size against log token
   frequency; Jaccard overlap of two tokens' hashes against their co-occurrence rate in sets (with a
   frequency-matched shuffle as control); TV on held-out real sets for the real-trained model vs the
   uniform-trained model; whether bimodality survives.
7. **Close the mechanism gap.** Replace the trained weights by a cleaned model (binary masks plus a few scalars,
   as in arXiv 2607.04800) and report the fraction of loss recovered; then add per-token corrections until the
   near-uniformity is reproduced, identifying what the +-0.5 logit analysis missed.

## 4. Stage 1 cost estimate
A base run is about 1.6e16 floating-point operations, roughly 5-10 minutes on an RTX 4090; vocab-20000 runs
about four times that. RunPod on-demand RTX 4090: $0.89/h (looked up 2026-11-14).
- Replication and kit: 5 GPU-h.
- Scaling grid: 120 runs x about 15 min = 30 GPU-h.
- Robustness: about 20 runs = 5 GPU-h. Structured sets incl. GPT-2 harvesting: 8 GPU-h. Mechanism work: 5 GPU-h.
- Subtotal 53 GPU-h = $47; tripled for reruns, longer training where convergence is slow, and extra seeds:
  about $140, plus $10 storage. **Total $150.** No API spend.

## 5. What success looks like
A figure showing learned hash size against width/k across the grid with the two reference curves, and a phase map
of where discrete hashes appear. Clear positive: learned sizes track the task-loss optimum within about 20%, and loss falls
exponentially with width where the Gaussian baseline falls polynomially. Clear negative: the binary solution is
confined to a narrow region or vanishes under GELU/LayerNorm. For (B): a significant relation between
hash overlap and co-occurrence (or its absence with tight error bars), and the gap in held-out TV between
structure-aware and uniform-trained hashes. For step 7: a cleaned model that recovers at least 90% of the loss with
a stated small number of parameters. A null on (B) (hashes stay random under real statistics) is still worth a
section; a failed replication would be reported with the exact setup, which is informative since no code exists.

## 6. Stage 2 (if stage 1 succeeds)
Look for the measured signature in real models: train small transformers (2-4 layers, narrow d_model) on real text
and test whether the final MLP plus unembedding shows tiered logits and near-binary read-in masks; apply the
cleaned-model fit to the last layer of Pythia/GPT-2-scale models; and use the toy as a ground-truth target for parameter decomposition. About $300-500.

## 7. Risks and how the plan handles them
- **Replication fails** (bfloat16 details, optimiser settings not fully specified). The gate in step 1 comes
  first; a short sweep over precision, weight decay and learning rate is budgeted.
- **Incremental feel.** A bare sweep would be a weak post; steps 3, 6 and 7 are the parts that add new claims.
- **Ambiguous "discreteness".** Pre-stated bimodality and mask-match thresholds; raw histograms near boundaries.
- **Real-set experiment confounded by frequency.** Frequency-matched shuffles; the independent-Zipf condition
  isolates the pure frequency effect.
- **Under-training read as a phase boundary.** Every boundary cell is rerun with 3x the steps before being
  labelled non-discrete.
