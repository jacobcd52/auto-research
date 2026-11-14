# Teleport probes: is in-context graph geometry a property of the word, or of the word that came before it?
cluster: single-qtdSzL | stage-1 cost: $110 | follows up: In-context learning of representations can be explained by induction circuits (qtdSzLpQ8BXv6YANd)

## 1. What the prior work showed
Park et al. 2025 (arXiv 2501.00070) fed Llama-3.1-8B random walks over a 4x4 grid whose nodes are arbitrary words (apple, bird, ...). With ~1400 tokens of context the model puts most next-token probability on valid grid neighbours, and the layer-26 class-mean activations of the 16 words, projected by PCA, form the grid. Park et al. read this as in-context re-organisation of concept representations.

Arditi's post argues for a cheaper story. Zero-ablating the top previous-token heads makes accuracy collapse and plateau and destroys the grid PCA; ablating the top induction heads lowers accuracy but leaves the grid PCA intact; random heads do little. A toy model (add to each of 16 random vectors the mean of its neighbours' vectors) produces a grid in PCA. Claim: accuracy is in-context bigram recall, and the geometry is a byproduct of previous-token heads mixing the predecessor into each position, because in a random walk the predecessor is always a neighbour. The geometry evidence is qualitative (PCA pictures, one word assignment, 16 walks), and the post leaves open why the grid appears only late in context although previous-token heads act from the first token.

Follow-ups that exist: Ransome (Substack, 2026) added four topologies and found that ablating a 3D PCA subspace drops accuracy from 89.4% to 69.5%. Kowalyshyn et al. (arXiv 2605.08405) mixed grid and ring walks and showed by residual patching and steering that late-layer states causally carry graph identity, concluding "both mechanisms". Lepori et al. (arXiv 2602.04212) showed models cannot use these representations for multi-step tasks. Saanum et al. (arXiv 2509.21534) studied induction heads on hierarchical tasks. None of them breaks the confound at the heart of the dispute: in every experiment so far, "adjacent in the sequence" and "adjacent in the graph" are the same thing. (Drafting search was arXiv API plus citation-following only, so step 0 is a final duplicate check.)

## 2. Question and why it matters
When a word appears right after a token that is NOT its graph neighbour, does its representation still sit at its grid location?

The two accounts give opposite predictions. If the model has re-organised the concept (Park), the representation of "apple" belongs at apple's grid position however it was reached. If the geometry is predecessor mixing (Arditi), a word reached by a jump should carry the jumped-from word's signature and the grid should vanish among such positions. A third possibility: the grid survives but is written by induction heads' output (their predicted successors are neighbours). That is still a circuit byproduct, and it would explain the late emergence. Each outcome says whether in-context "representation change" is belief-like state that safety work should take seriously (as in representation-hijacking jailbreaks, arXiv 2512.03771) or an artefact of averaging.

## 3. Stage 1 plan
Reused: Arditi's repo https://github.com/andyrdt/iclr_induction (grid, walk generator, head scoring, ablation hooks, PCA; TransformerLens). Model: Llama-3.1-8B base from the ungated mirror `unsloth/Meta-Llama-3.1-8B` (the Meta repo is gated). Built: the probe/teleport generators, the metrics, the decomposition.

Steps:
0. Duplicate check (search LessWrong/arXiv for work after May 2026). Reproduce the post's Figures 2-4 from the repo as a pipeline check.
1. Metrics with a null. For any set of 16 vectors: normalised Dirichlet energy on the grid, and Spearman correlation between pairwise representation distance and grid distance, each converted to a z-score against 10,000 random relabellings of the nodes. Layers 8, 14, 20, 26, 30; 100 contexts with random word-to-node assignments (the post used one).
2. Factorial probe (main experiment). Take a clean 1400-token walk as prefix. Append one extra token w after final token q, for all 16x15 ordered (q, w) pairs, including non-neighbours, reusing the cached prefix. This fills every cell h(w | previous = q), which a plain walk never does. Fit h(w|q) = u_w + v_q + residual. Report (a) share of variance in each term per layer; (b) grid z-score of the u_w vectors (the word's own component), of the v_q vectors, and of class means built only from non-neighbour predecessors, versus class means built the standard way.
3. Teleport walks (naturalistic check). Walks where each step jumps to a uniformly random node with probability 0.05 or 0.1, so jumps are part of the in-context distribution. Compare class means over jump-arrival positions (predecessor not a neighbour) with count-matched ordinary positions.
4. Pair format. Present the grid as randomly ordered edges "A B ; C D ; ..." (as Lepori et al. do for lines). Class means separately for first-of-pair tokens (preceded by a separator) and second-of-pair tokens (preceded by a neighbour). Also show some edges in one orientation only and test whether the model predicts the reverse direction above distance-matched controls.
5. Mechanism split. Repeat steps 2-3 with top-32 previous-token heads ablated, top-32 induction heads ablated, both, and 32 random heads (4 sets); use mean-ablation as well as zero-ablation.
6. Time course. Run step 2 at prefix lengths 50, 100, 200, 400, 800, 1400 to see which component tracks the late emergence of the grid.
7. Robustness: repeat steps 1-3 on one more ungated model (`Qwen/Qwen2.5-7B`).

## 4. Stage 1 cost estimate
Forward passes only. Step 2 is 240 one-token continuations per context on a cached prefix; all steps together need under 10 GPU-hours on a 48 GB card. Budget 120 GPU-hours for debugging, idle time and reruns on a RunPod RTX A6000 48 GB at $0.69/hr (secure cloud; $0.33/hr community; runpod.io/pricing, 2026-11-14): $83. Storage and model downloads: about $10. Margin: $17. No API spend. Total: $110.

## 5. What success looks like
One table and figure: grid z-score by layer for standard class means, non-neighbour-predecessor class means, u_w and v_q, under each ablation.
- Mixing confirmed: grid z-score of non-neighbour-predecessor class means and of u_w is within the null (|z| < 2) while standard class means are far outside it, and v_q carries the structure. Headline: "the grid is in the previous token, not the word".
- Reorganisation confirmed: u_w keeps a large share (say over half) of the standard z-score, and it survives ablation of both head types. Headline: Arditi's byproduct account is incomplete; there is word-level in-context structure.
- Mixed: grid survives jumps but disappears under induction-head ablation, and grows with context length. Headline: the geometry is the induction circuit's prediction, which resolves the post's late-emergence puzzle.
All three are publishable, since this is the first measurement that separates the accounts. An ambiguous outcome would be z-scores between 2 and 4 that flip across layers or models; that would be reported as such.

## 6. Stage 2 (if stage 1 succeeds)
(i) Interleaved walks on two vocabularies, so structure exists only at lag 2, to test whether geometry follows whichever heads feed the induction key; (ii) path patching of previous-token-head to induction-head composition; (iii) apply the same predecessor-conditional decomposition to Kowalyshyn et al.'s two-graph "orthogonal subspaces" and to representation-hijacking prompts (does the benign token's shifted representation survive a change of local context?). About $300-400, mostly GPU time on a larger model for (iii).

## 7. Risks and how the plan handles them
- A probe token after a non-neighbour is off-distribution and the surprise itself may distort the activation. Step 3 puts jumps in-distribution; agreement between steps 2 and 3 is required before any headline claim.
- Too few jump arrivals per word for stable class means. Count-matched subsampling, pooling over 100 contexts, bootstrap intervals; step 2 fills every cell and has no such problem.
- Teleports slow in-context learning. Check accuracy on non-jump steps first; fall back to a 0.05 jump rate or longer contexts.
- Pipeline bug that silently shifts positions by one would fake or erase the effect. Unit-test hooks on a synthetic model state where the answer is known, and confirm the reproduction of the post's Figures 3-4 before new experiments.
- Already done elsewhere. Step 0 checks; step 4 and the second model would remain new.
