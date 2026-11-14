# Feedback: "How dense are learned Bloom filters, and do they survive realistic token statistics?"

Verdict: **keep, with tweaks** — cheap, feasible, directly the author's stated open question, but as written it is
a wide descriptive sweep whose headline comparison is under-specified. Narrow it and fix the reference curve.

## What I checked

- **Prior work as described: accurate.** Re-read the post (plaintext and GraphQL markdown). Config (vocab 5000,
  d_model = d_hidden = 256, k = 10, alpha in [0.5, 3.0], 500k steps, batch 4096, AdamW, cosine from 2e-3, bfloat16,
  TV 0.031), bimodal W_E·mlp_in, transposed mask, ~1% mass for one-bit misses, the hand construction and the
  three "further work" items all match. No code link in the post (only arXiv/OpenReview/YouTube/Wikipedia URLs).
  64 karma, exactly one comment (Lucius Bushnaq, "would like more of this", 11 karma).
- **Two things the post already reports that the proposal presents as new robustness checks:** (a) the
  softmax(alpha) target ("empirically results in a hidden layer identical to the uniform task"); (b) fewer than
  k tokens at inference works. Step 5 should cite these as replications, not discoveries.
- **A detail the replication gate misses:** the post's behavioural statistics (two clusters, false-positive
  count) are on sets drawn from tokens [1,100], not the full vocabulary. The TV 0.031 is "held-out random
  samples". Do not try to match the false-positive count without matching that sampling.
- **Has it been done?** Not found. Gibson has posted nothing since (author page checked to 2026-11-14; latest
  post is this one). arXiv queries ("Bloom filter" with superposition / softmax / unembedding / softmax
  bottleneck) return nothing relevant. arXiv 2607.04800 exists and is as described. **General web search was
  unavailable to me as well (search budget exhausted), so neither proposer nor reviewer has done one.** Residual
  scoop risk: Gibson says he is "working on probabilistic methods for computation in superposition" and question
  (A) is the obvious next thing for him; six months of silence is mild evidence against.
- **Uncited prior art that matters:** Serrà & Karatzoglou, "Getting deep recommenders fit: Bloom embeddings for
  sparse binary input/output networks" (arXiv 1706.03993, verified) hand-designs Bloom-hashed input/output
  layers for large-vocabulary networks. The post does not cite it either. The write-up must; it also makes "a
  network can use Bloom codes for a big softmax" less novel and "gradient descent finds them, with this density"
  the only novel part.
- **Naming:** "learned Bloom filter" is an established term for something else (Kraska et al.; my arXiv query
  returned eight such papers). Retitle.
- **Price:** RunPod RTX 4090 is $0.89/h Secure Cloud (verified on runpod.io/pricing today); Community Cloud is
  $0.34/h. FLOP estimate checks out (I get ~1.7e16 for the base run).

## 1. Would it get upvoted?

Probably not above 50 as written; I put it at roughly 20-25%. The parent got 64 karma with one comment — liked,
not discussed. Follow-ups by unknown authors to a toy-model post usually land below the parent, and the
cluster's ceiling is 65. A "phase map plus hash size vs width/k" post is the kind of thing that gets 20-35.

What could push it over: (i) a clean one-line law ("learned hash size = X, here is the two-parameter model that
predicts it and the TV") with the mechanism gap actually closed; or (ii) part (B) showing hash bits that are
recognisable token clusters when trained on real GPT-2 top-k sets — that is the only result here that a reader
outside the superposition-toys niche would care about. The audience is the Bushnaq/Linsefors/Gibson/Goodfire
circle (the same ~60 voters as the cluster posts). A robustness table will not move them.

## 2. Naturalness

Mainline. (A) is verbatim the author's open question 2, step 7 is his question 1, and stage 2 is his question 3.
The screener's note says the same. (B) is a reasonable bridge toward real models but is the proposer's
invention, and it rests on the toy's fiction that the input is already a linear sum of the answer tokens'
embeddings; "realistic token statistics" oversells that. It is realistic set statistics on an unrealistic input.
No one appears to have done any of it.

## 3. Pre-mortem

**How it plays out.** Agents write the model in an hour. Replication probably works qualitatively (ReLU plus
cross-entropy toys yielding binary codes is robust, cf. 2607.04800), though unspecified weight decay, init,
bias and final LR make hitting TV 0.02-0.05 a coin-flip on the first try; a day-one sweep fixes it. Then the
grid runs, produces 120 cells, and the team spends day two on plots. The mechanism step and the real-set step get
the leftover hours.

Rough forecast: clear positive with a crisp law 20%; clear and interesting negative (discreteness fragile) 10%;
correct-but-descriptive mush ("hashes are roughly Bloom-ish, shorter than optimum, depends on training
length") 55%; fails to run or replicate 15%.

**Specific failure modes, most important first.**

1. **The task-loss reference curve (step 3 i) is degenerate as specified.** In the hand construction the logit
   scale T is free: as T grows, near-miss leakage vanishes and the loss-optimal hash size is just the classical
   Bloom optimum. The trained network has a *finite* gap (about 1.75 logits per missed bit per the post). My
   back-of-envelope at the base config (assuming ~18 bits, union half full): false positives occur in ~2% of
   sets and contribute ~0.002 TV, whereas tokens missing by 1-4 bits collect roughly 2-3% of the mass in total.
   So the reported TV 0.031 is almost entirely near-miss leakage, set by the per-bit gap, not by Bloom false
   positives. Consequences: the learned density will be determined by whatever limits the gap (weight decay,
   bf16, training time, the uniformity constraint), and "compare against the hand construction for every hash
   size" means nothing until the proposal says how T and the bias are chosen. It needs a two-parameter
   reference (hash size, per-bit gap) with the gap either measured or constrained by a stated norm budget.
2. **Hash size may be a function of training time, not of the optimum.** Sparsification under AdamW keeps
   drifting. If hash size at 500k steps differs from 1.5M steps, there is no "density law". The plan reruns only
   boundary cells at 3x. "Steps reduced where loss has plateaued" is also ill-defined under a cosine schedule:
   shortening the horizon changes the solution. This must be settled at the base config before the grid.
3. **Much of the grid is uninformative.** Predicted Bloom hash sizes (width/k · ln 2) span 1.1 bits (width 64,
   k 40 — impossible regime, a hash of one bit is not a hash) to 177 bits (width 512, k 2 — trivially easy).
   Perhaps 40% of cells are in the interesting band. Worse, the classical optimum does not depend on vocabulary
   at all, and the three vocab values move log(vocab) by only 1.4x, so the vocab axis (which costs the most
   compute) barely tests anything.
4. **"Width" conflates d_model and d_hidden.** The hash lives in hidden-neuron space (d_hidden entries) but
   must lie in a d_model-dimensional subspace and be read by a d_model-wide unembedding. The grid ties them
   together and step 5 varies d_hidden only at the base point. Which of the two sets the number of usable bits
   is one of the more interesting questions here and gets three runs.
5. **Two seeds per cell** cannot distinguish a 20% deviation from the reference from seed noise unless
   seed-to-seed variance is tiny; nobody knows that yet. The 3-seed replication should report it and the grid
   should be sized accordingly.
6. **Part (B) data problems.** Keeping only positions whose whole top-10 lies inside the 5000 most frequent of
   50,257 tokens will discard most positions and bias toward function-word contexts; the yield is unstated. The
   run consumes 4096 x 500k = 2e9 samples, so a few hundred thousand distinct sets are each seen thousands of
   times: held-out evaluation is essential (it is planned — good) and the frequency-matched shuffle must also
   preserve set-level repetition. The predicted direction (co-occurring tokens share bits) follows from the
   post's own remark that within-pass overlap helps, so a positive is likely but partly expected; its value is
   in the interpretability of the bits, which the plan does not measure (no step inspects what a bit's token
   set is).
7. **Step 7 is open-ended.** "Add per-token corrections until near-uniformity is reproduced" has no stopping
   rule and is where two-day agent teams sink time. The cleaned-model fit is well-defined; the rest is not.
8. **Scope.** Seven steps, about 170 runs, three reference solutions, a GPT-2 harvest and a mechanism study in
   two days. Everything will get done shallowly. Risk of evaluation bugs is moderate (sampling k distinct
   tokens at batch 4096, bf16 softmax over 20k logits, mask thresholding near boundaries).
9. **Unsurprising either way on robustness.** "GELU blurs the modes" or "LayerNorm changes scale" will not
   surprise anyone, and a blurred-but-functionally-identical solution makes the yes/no phase map arbitrary.
   Discreteness should be judged functionally (does a binarised model recover the loss) rather than by a
   histogram threshold.

## 4. Cost check

The estimate is realistic and slightly pessimistic on price, slightly optimistic on time. I get the same FLOPs;
with framework overhead a base run is more like 10-20 min on a 4090, vocab-20000 runs about an hour, so the
grid as written is nearer 50-60 GPU-h than 30. That still fits inside the tripled budget. Many of these models
fit on one GPU simultaneously (stack runs with vmap or separate processes), and Community Cloud is $0.34/h.
My estimate: **$80-150; $150 is a safe ceiling.** Wall-clock, not money, is the constraint: plan for 4+ GPUs in
parallel from hour one.

## 5. Recommended changes (in priority order)

1. **Fix the reference model before anything else.** Replace 3(i) with an explicit two-parameter analytic model:
   hash size d and per-missed-bit logit gap g, giving predicted KL/TV as a sum over the binomial distribution
   of uncovered bits. Measure g in trained nets, and state what constrains it (run a small weight-decay and
   training-length sweep to see whether g moves). The headline becomes "learned (d, g) versus the loss-optimal
   d given g", plus "what sets g" — that is a real finding and it simultaneously answers part of the author's
   mechanism question.
2. **Add a convergence gate at the base config:** hash size and g at 250k, 500k, 1M, 2M steps, and with/without
   weight decay. If hash size has not stabilised, say so and reframe; do not run the grid on a moving target.
3. **Shrink and re-aim the grid.** Drop vocab to two values (or one plus a single 20k check). Choose (width, k)
   so width/k lies in roughly 6-60. Make d_hidden/d_model an axis (0.5, 1, 2, 4). Use 3-4 seeds. About 60 runs.
4. **Make (B) the centrepiece of the post, and make it about interpretable bits.** State the data yield after
   filtering (consider relaxing to "top-10 restricted and renormalised to the 5000-token subvocab"). Add an
   explicit step: for each hidden bit, list the tokens that carry it and score cluster coherence (e.g. against
   GPT-2 embedding neighbourhoods or part-of-speech), with the shuffle control. Keep the Zipf-only condition.
5. **Cut step 5 to four runs** (GELU, LayerNorm, no residual, variable k) judged by a functional criterion:
   loss recovered after binarising the masks. Cite the post for the softmax(alpha) and fewer-than-k results.
6. **Bound step 7:** deliver the cleaned model and the fraction of loss recovered; attempt the uniformity
   explanation only if the (d, g) model in item 1 leaves a residual, with a fixed half-day cap.
7. **Housekeeping:** retitle to avoid "learned Bloom filters"; cite Bloom embeddings (arXiv 1706.03993) and the
   softmax-bottleneck paper the post builds on; note the [1,100] evaluation detail in the replication gate;
   say plainly that no general web search was possible; release the code (the parent has none, which is itself
   a selling point for the follow-up).
8. Optional, if time remains: one cheap look at a real model (e.g. sparsity/bimodality of GPT-2's final MLP
   output weights projected through W_U) pulled forward from stage 2, labelled exploratory. Even a clean
   "no sign of it" would raise reader interest more than another robustness row.

If the funder must choose within this cluster, this is the safer but lower-ceiling project: it will almost
certainly produce *a* post, and is unlikely to produce a memorable one unless items 1 and 4 are adopted.
