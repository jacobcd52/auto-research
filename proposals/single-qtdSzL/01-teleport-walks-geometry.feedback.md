# Feedback: Teleport probes (single-qtdSzL / 01)

Verdict: **keep with tweaks.** The core factorial experiment is cheap, well aimed and probably new, but two pieces of prior work the proposal missed reduce its novelty, and its "reorganisation confirmed" reading is not supported by the design as written.

What I checked, and how:

| Claim | Status |
|---|---|
| Post content (Figs 3-6, toy model, stated limitations) | Confirmed by reading the full post. Note the post's Fig 6 already shows qualitatively that activations sit between the current-token and previous-token centroids. |
| arXiv IDs 2605.08405, 2602.04212, 2509.21534, 2507.13540, 2512.03771 | All exist with the stated titles; I read HTML full text for the first, second and fourth. |
| `unsloth/Meta-Llama-3.1-8B` and `Qwen/Qwen2.5-7B` ungated | Confirmed via HF API (`gated: False`). |
| Repo `github.com/andyrdt/iclr_induction` | **Not verified.** GitHub is blocked from this session (403). The post links to it and says all code is there; the file list in NOTES.md is the proposer's. |
| RunPod A6000 at $0.69/hr | **Not verified.** The pricing page did not parse. The figure is plausible and the budget is insensitive to it. |
| "No one has done this" | Partly wrong, see section 2. The WebSearch budget was exhausted for this session (0 searches ran, the same problem the proposer had). I used four arXiv API queries, full-text reads, and the LW comments query (which returned zero comments on the post). A LessWrong/AF/Google Scholar check is still outstanding. |

## 1. Would it get upvoted?

Borderline. I put it at roughly 25-30% to clear 50 karma.

- The parent post got 52 karma and zero comments, from a well-known author, as an ICLR blogpost crosspost. That is the ceiling for this topic's natural audience, not the floor. A follow-up by an unknown author on the same narrow toy task starts lower.
- The audience is mech-interp people who followed the Park et al. versus Arditi dispute. They would care about a crisp, quantitative "the grid is / is not in the previous token" result with a proper null, since the post's geometry evidence is PCA pictures from one word assignment.
- The outcome that would do best is a clean overturning or a clean confirmation with one striking figure. The outcome I think most likely (both components carry structure, layer-dependent) is the least shareable.
- The safety hook via representation hijacking (2512.03771) is asserted, not tested in stage 1. Readers will not grant it. Do not lean on it in the headline.

## 2. Naturalness

It is a mainline follow-up. The post's own toy model makes the prediction being tested, and the post's own stated puzzle (previous-token heads act from the start, the grid appears late) is addressed by step 6. The author would plausibly want this next.

Novelty is weaker than the proposal claims. Two omissions:

1. **Yang et al. (2507.13540), section 6.5, already ran teleport walks.** Their noisy process transitions "to a uniformly random token with probability p at each step, rather than to a graph neighbor". They analysed only behaviour (the model's outputs stop reproducing the non-neighbour transitions as context grows), not representations at jump-arrival positions. So step 3's data process is not new, and its viability check (the model still learns the graph under noise) is already done. NOTES.md flagged this as something to check; the proposal did not follow up. Cite it and reuse their noise rates.
2. **Lepori et al. (2602.04212), section 4 and Appendix E, already measured geometry for the same tokens outside the walk.** They compute Dirichlet energy for state tokens when they appear in the few-shot-example portion of the prompt (where the predecessor is not generally a walk neighbour) versus in the walk, and report that representations in the examples "are degraded relative to their counterparts in the random walk" (Fig 7 bottom, Gemma-3 and OLMo-2). That is a coarse version of this proposal's main question, with an answer leaning toward context dependence. It is not a duplicate: it is not predecessor-conditional, has no decomposition, no head ablations, different models, and the example format is confounded with a task switch. But the sentence "in every experiment so far, adjacent in the sequence and adjacent in the graph are the same thing" is false and must be fixed.

Kowalyshyn et al. interleave in 100-token segments, so predecessor and graph neighbour coincide except at segment boundaries, and they do not condition on the predecessor. The proposal's description of that paper is fair.

## 3. Pre-mortem

How it plays out: the reproduction (step 0) and the metric (step 1) work on day 1; the pipeline is forward passes plus hooks on released code. Step 2 runs without trouble. The difficulty is interpretation, not execution.

Rough forecast:

| Outcome | Probability |
|---|---|
| Clean "mixing confirmed" (u_w at null, v_q carries the grid) | 15% |
| Clean "word-level component dominates" with a mechanism attached | 25% |
| Both components carry structure, layer-dependent, story interpretable but undramatic | 30% |
| Ambiguous mush (steps 2 and 3 disagree, or models disagree) | 20% |
| Fails to run or reproduce in two days | 10% |

Specific problems, most serious first:

1. **A grid-structured u_w does not mean "reorganisation".** At layer 26 the residual stream at the position of w is largely the next-token prediction, and the model predicts w's neighbours at about 90% accuracy. A vector that is a mixture of the neighbours' output directions is exactly the toy model's neighbour mixing, arriving through prediction rather than through the previous token. So u_w having grid geometry is close to guaranteed by task performance alone. The proposal lists this as a "third possibility" but then relies on top-32 induction-head ablation to separate it. That is not adequate: the post itself reports that accuracy keeps rising with context under induction-head ablation, so prediction content survives the ablation. The "reorganisation confirmed" criterion (u_w survives ablation of both head types) would be met by residual prediction content, and separately by heads that attend to earlier occurrences of w (which were themselves mixed with neighbours). The design can cleanly reject immediate-predecessor mixing; it cannot confirm Park's reading.
2. **The prior should already lean against pure predecessor mixing.** The late emergence of the grid, which the post admits it cannot explain, is hard to reconcile with a mechanism present from token 2. So the most likely result is "v_q matters but is not the whole story", which readers will find unsurprising unless the non-predecessor component is pinned to something specific.
3. **Thresholded z-scores will mislead.** With 100 contexts pooled, a tiny residual structure gives a large z; with one context, |z| < 2 is weak evidence of absence. The "mixing confirmed" criterion as written (|z| < 2) is a null-acceptance on a significance test.
4. **Off-distribution probes (step 2).** The model has seen 1400 tokens with no violations; a non-neighbour token is a surprise and may shift the whole activation. The proposal's mitigation (require agreement with step 3) is right, but then step 3 is the binding experiment and it has the thin data: at jump rate 0.05, 1400 tokens gives about 70 jumps per context, about 4 per word, of which roughly a fifth land on a neighbour or the same node by chance.
5. **Step 2 bookkeeping.** "All 16x15 ordered (q, w) pairs on a cached prefix" needs 16 prefixes per context (one ending at each q), not one. Easy, but prefix length and recency of the last occurrence of w then vary with q and should be balanced or regressed out.
6. **Scope creep.** Seven steps, five layers, six ablation conditions, six prefix lengths, two models, plus a pair-format arm with its own behavioural test. For a two-day agent team this invites a shallow pass over everything. Step 4's reverse-edge test is a different question with its own confounds.
7. **Off-by-one risk** is real and correctly flagged; the reproduction of the post's Fig 6 (points lying between w and p centroids) is the right unit check.

## 4. Cost check

The estimate is realistic and, if anything, generous. An 8B model in fp16 fits a 48 GB card; the full step-2 grid is about 24,000 short continuations per condition per 100 contexts, and even without cache reuse (TransformerLens caching under ablation hooks is fiddly) the whole plan is a few tens of GPU-hours. My estimate: **$60-150**, depending on how much debugging time the card sits idle and whether the second model is run. $110 is fine. No API spend is needed.

## 5. Recommended changes

1. **Reframe the hypotheses as three sources and drop the "reorganisation confirmed" headline.** State: (H1) immediate-predecessor mixing, the post's toy model; (H2) prediction content, i.e. the output-side encoding of likely successors; (H3) anything left. The factorial separates H1 from the rest. Promise only what the design can deliver: "the post's toy mechanism accounts for X% of the grid structure at layer L".
2. **Add a direct test of H2 that does not depend on head ablation.** For each (context, w), take the model's actual next-token distribution over the 16 words and build the predicted-successor vector from the unembedding rows (or from a logit-lens readout at the analysed layer). Then (a) regress u_w on it and report the grid score of the residual, and (b) project out the 16-word unembedding subspace and recompute. Also report the layer profile: structure that appears only after the induction heads' layers and tracks accuracy over context length is prediction content. This is a day of work and turns the likely "mixed" outcome into a specific finding.
3. **Correct the related-work section.** Cite Yang et al. section 6.5 as the source of the teleport process and Lepori et al. Fig 7 / Appendix E as a prior, coarser measurement pointing toward degradation outside the walk. Rewrite the "none of them breaks the confound" sentence. State what is new: predecessor-conditional decomposition, a permutation null, head ablations, the same model as the post.
4. **Replace z-thresholds with an effect size and interval.** Report the fraction of the standard class-mean grid score (Spearman distance correlation or Dirichlet energy) retained by non-neighbour-predecessor means and by u_w, with bootstrap intervals over contexts and word assignments. Pre-state the bands, for example below 20% retained supports H1, above 70% rejects it.
5. **Cut scope.** Stage 1 should be steps 0, 1, 2, 3, 6 and the new H2 analysis on Llama-3.1-8B, at layers spanning before and after the induction heads. Keep mean-ablation of previous-token heads as one supporting condition. Move the pair-format arm, the reverse-edge behavioural test and the full ablation grid to stage 2. Keep Qwen only if the main result is in hand by the end of day 1.
6. **Strengthen step 3.** Use more contexts (300 or more) or longer walks so that each word has at least a few hundred non-neighbour arrivals overall; exclude jumps that land on a neighbour or the same node; analyse the position after the arrival separately (its predecessor is a neighbour again but its two-back token is not).
7. **Finish the duplicate check before spending.** Search LessWrong, the Alignment Forum and Google Scholar citations of the post and of Park et al. for work after May 2026, and open the repo to confirm the scripts run as described. Neither could be done from this review session.
