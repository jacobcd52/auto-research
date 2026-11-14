# Does a tensor transformer make a weights-only backdoor audit easier? A blind head-to-head against standard models
cluster: tensor-transformers | stage-1 cost: $190 | follows up: "If you're interpreting <1B parameter models, you should use a tensor transformer" (expsAXaBgiqgitFe6); "Tensor-Transformer Variants are Surprisingly Performant" (hp9bvkiN3RzHgP9cq)

## 1. What the prior work showed
A tensor transformer uses bilinear MLPs `D(Lx ⊙ Rx)` and bilinear attention (a product of two dot-product score
matrices, no softmax), so the network is a polynomial in its inputs and its components can be composed and
compared with linear algebra directly on the weights.

- Post hp9bvkiN3RzHgP9cq: such models train about as well as standard ones at ~500M parameters (about 4% more
  batches to the same loss); checkpoints are public (`Elriggs/gpt2-bilinear-*`).
- Post expsAXaBgiqgitFe6 argues anyone interpreting sub-1B models "should use a tensor transformer", while
  conceding the author "can't even interpret a GPT-2 small sized tensor transformer". The practical payoff of the
  architecture is asserted, not measured.
- The strongest payoff evidence is the tensor-similarity paper (arXiv 2605.15183; code
  `github.com/tdooms/tensor-similarity`): a weights-only, symmetry-invariant similarity that tracks backdoor
  insertion in an SVHN classifier better than per-matrix cosine or clean-data output similarity and, given the
  target class, localises it to a class slice. Its language experiment is a 2-layer attention-only model where
  "we didn't explore what those differences correspond to"; the authors say the method shows "where the
  differences are" but not "what the difference is".
- Not done (arXiv queries, author's posts and repos; general web search was unavailable at drafting, re-check):
  (a) recovering **what** a backdoor is (trigger, target) from weights in a language tensor transformer; (b) any
  comparison where the **same audit** is attempted on a matched standard model with strong generic methods.
  Existing comparisons pit the tensor method against weak baselines on the tensor model itself.

## 2. Question and why it matters
**Given only the weights of a small language model before and after fine-tuning (no poisoned data), can an
auditor recover a backdoor's trigger and target more reliably when the model is a tensor transformer analysed
algebraically than when it is a standard softmax/ReLU transformer analysed with the best generic methods?**

This turns "you should use a tensor transformer" into a measured claim on a safety-relevant task with ground
truth. If the tensor route wins (especially on triggers that are conjunctions of two tokens, which are exactly
degree-2 interactions), that is the first demonstration that the architecture buys auditing power. If generic
methods on standard models do as well, the advice needs qualifying and the field learns which baseline to beat.

## 3. Stage 1 plan
**Models (reused code).** Four base models trained on `SimpleStories/SimpleStories` (MIT) with a small-vocabulary
tokenizer: {tensor, standard} x {2, 4 layers}, d=256. Tensor models use `DeepModel`, `Attention`, `BilinearMLP`
and `lm_train.py` from `loganriggs/tensor_language`, norm off as in that repo. Standard models use the same code
with `attention="softmax"` (already supported), a ReLU MLP and RMSNorm, matched in parameters; if validation
losses differ, a standard model early-stopped at the tensor model's loss is added.

**Backdoors (red team, built).** Per base model, a seeded script fine-tunes:
- 15 single-token backdoors: rare trigger token in context -> fixed target token.
- 15 conjunction backdoors: tokens A and B both present (either alone does nothing) -> target.
- 15 distributed backdoors: trigger token -> a fixed 8-token phrase.
- 15 benign controls: equal steps on clean data or on an innocuous new bigram rule, so "something changed" is not
  enough to flag a backdoor.
Poison rate 5%; attack success above 90% with clean loss within 0.02 of base. 240 fine-tunes in total; trigger
identities are sealed from the auditing agents.

**Audit methods (blue team).** Input: base weights, fine-tuned weights, clean data. Output: a backdoor score and
ranked trigger-token and target-token candidates.
- T1, tensor models only: tensor similarity (released code) for the score; for localisation, contract the weight
  difference along explicit paths (embed -> MLP -> unembed, embed -> OV -> unembed, QK, attention-then-MLP), rank
  output-token slices by change, eigendecompose the top slices' input-interaction matrices and read eigenvectors
  in token space (the bilinear-MLP recipe of arXiv 2410.08417, applied to a difference).
- G1, both architectures: SVD of each weight-difference matrix, read through embedding/unembedding.
- G2, both: search-based trigger inversion — exhaustive single-token scan plus beam search over pairs for
  inserted tokens maximising KL between fine-tuned and base outputs on clean contexts. The strong generic
  baseline, given compute equal to T1.
- G3, both: clean-data output and activation differences (expected floor).

**Steps.** (1) Train base models; confirm a hand-planted backdoor is learnable in each. (2) Develop all methods
on a separate development set of 10 known backdoors per base model. (3) Freeze methods and compute budgets in
writing. (4) Red-team agent generates the 240 test fine-tunes. (5) Blue-team agents run blind. (6) Unseal, score.

**Metrics.** Detection AUROC (backdoored vs benign); recall@10 for trigger token(s) and target token; pair
recall for conjunctions; wall-clock per audit; bootstrap CIs over the 15 models per cell.

**Key comparisons.** (a) Best method on tensor models vs best method on standard models: which architecture
should one choose? (b) On tensor models, T1 vs G1/G2: does the algebra add anything? (c) Both, restricted to
conjunction triggers and 4-layer models, where search is costlier and composition matters.

## 4. Stage 1 cost estimate
RunPod community prices looked up 2026-11-14: RTX 4090 $0.34/h, RTX 5090 $0.69/h.
- Base models: 6 (incl. loss-matched extras) x about 2 GPU-h = 12 GPU-h.
- Fine-tunes: 280 (test + development) x about 6 min = 28 GPU-h.
- Audits: T1 about 5 min x 120 tensor fine-tunes = 10 GPU-h (the tensor-similarity README reports about 3.5 s
  per pair for a 2-layer d=512 model); G2 at a matched 10-minute budget x 280 = 47 GPU-h; G1 + G3 5 GPU-h.
- Method development and debugging: 30 GPU-h.
- Subtotal 132 GPU-h x $0.69 = $91; 1.7x margin for reruns = $155. Storage, idle time and reserve $35.
- **Total: about $190.**

## 5. What success looks like
A table of recall@10 and AUROC by method, architecture and trigger class, with CIs. Post-worthy patterns:
- **Tensor wins**: T1 recovers conjunction triggers in most 4-layer tensor models while G1/G2 on matched standard
  models recover clearly fewer at equal compute.
- **No advantage**: G2 on standard models matches or beats T1 everywhere; the case for switching architecture
  then rests on something other than this kind of audit.
- **Mixed**: algebra helps for conjunctions and depth but not single tokens — a map of where weight-reading pays.

Weak outcome: every method at ceiling or at floor. The development phase tunes difficulty (trigger rarity, poison
rate, depth) until at least one method scores between 20% and 80% before the blind set is generated.

## 6. Stage 2 (if stage 1 succeeds)
- Repeat on the released 124M pair (`Elriggs/gpt2-bilinear-sqrd-attn-12l-6h-768embd` vs
  `Elriggs/gpt2-12l-6h-768embd`), which needs path contraction to scale to 12 layers (about $300-500).
- Behavioural backdoors (conditional policy change) and audits without access to the base model (about $400).

## 7. Risks and how the plan handles them
- **Strawman baselines.** G2 gets T1's compute, is developed by a separate agent tasked with maximising recall on
  standard models, and all methods are frozen before the blind set exists.
- **T1 is partly new and may not work.** Single-layer paths follow a published recipe and tensor similarity is
  released code; multi-layer contraction is the uncertain part. If T1 works only at 2 layers, that boundary is
  reported and comparison (a) is still answerable.
- **Architectures may store the same backdoor differently.** That is part of what is measured; attack success,
  clean-loss change and weight-difference norm are matched and reported per cell.
- **Leakage between red and blue agents.** Triggers are written to a sealed file by a seeded script; scoring is
  done by a third script.
- **Small n per cell (15).** Headline claims use pooled comparisons (45 backdoors per architecture-depth) unless
  per-class effects are large.
