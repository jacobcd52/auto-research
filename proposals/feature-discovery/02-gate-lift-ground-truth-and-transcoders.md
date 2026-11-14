# Does the MLP error-correct what transcoders call features? Gate lift on a planted toy and on Gemma 3
cluster: feature-discovery | stage-1 cost: $100 | follows up: In search of natural features (SNAKJuN8FdoEaWeFC); Announcing Gemma Scope 2 (YQro5LyYjDzZrBCdb)

## 1. What the prior work showed
Vaintrob's post proposes a data-light test of whether a direction is "natural to the model's computation":
an MLP that cares about a direction should behave like a noise gate on it, amplifying it when it is strongly
present and damping it when it is weak. For a unit direction v and MLP Jacobian J, the channel amplification
score ("amp score", called gate lift in the repo) is E[v.Jv | v active] - E[v.Jv | v inactive]. On GPT-2
small without LayerNorm, the post reports: random directions score about 0, real activations higher, SAE
features higher still, and gradient ascent on the score from 100k+ starting activations converges to just
four attractors ("ur-features": the article "the", whitespace, word-continuation, abstract nouns). The author
asks for criticism and names "this is just PCA with bells and whistles" as the likeliest way it is uninteresting.

The released repo (`https://github.com/mvaintrob/denoising-tomography`) has already done much stress-testing
and is more cautious than the post. With covariance-matched random nulls at block 8: null 0.04, single
activations 0.17, SAE features 0.09-0.13, supervised mean-difference probes 0.2-0.3. Frequency and
dictionary-width trends vanish when conditioning on true SAE encoder firing; the ascent "manufactures lift"
on a random-init model; the attractor set is layer-global and corpus-dependent. A commenter replicated block
6 and scaled to GPT-2 XL (median 1-3.5 attractors per block).

Not done (repo, comments, author's later posts, arXiv API; web search was unavailable): (a) testing the
score where the answer is known, a network with planted nonlinearly-denoised directions; (b) scoring
**transcoder** features, dictionaries trained on the MLP's input-output map; (c) leaving GPT-2. Gemma Scope 2 (Google DeepMind, Dec 2025) now provides, for the same layers of Gemma 3,
residual SAEs, MLP-output SAEs and MLP transcoders at widths 16k-262k, all public.

## 2. Question and why it matters
**Is gate lift a valid detector of the directions an MLP actually computes on, and by that measure are
transcoder features more "computation-natural" than residual SAE features, raw activations, or PCA?**

Two notions of "feature of the computation" exist: sparse dictionaries fit to the MLP's map (transcoders) and
directions the MLP spends nonlinearity denoising (lift). They have never been compared. If they agree, each
validates the other; if not, the toy says which to distrust. The toy also settles a question the post leaves
open: when many features are planted, does the ascent recover them or collapse onto a few basins? If it
collapses, "exactly four ur-features" describes the optimiser, not GPT-2.

## 3. Stage 1 plan
Reused: the repo's `gates/` package (exact-JVP lift, coloured nulls, flow, random-init floor), Gemma Scope 2
weights (`https://huggingface.co/google/gemma-scope-2-1b-pt`: `transcoder/`, `resid_post/`, `mlp_out/` at
layers 7, 13, 17, 22), ungated `unsloth/gemma-3-1b-pt` (26 layers, d = 1152, MLP width 6912),
`NeelNanda/pile-10k` as in the repo. Built: the toy and a Gemma adapter for the lift code.

**Part A - planted toy (day 1 morning).**
1. Residual block y = x + MLP(x), d = 64, hidden 512. Inputs are sparse sums of m = 256 random unit features
   plus Gaussian noise. Half the features (set G) are trained to be noise-gated (target: thresholded clean
   value); half (set P) are trained to pass through unchanged, so the MLP need do nothing for them. Feature
   frequencies are varied over two orders of magnitude and are independent of G/P membership. Five seeds.
2. Score lift for G, P, coloured-random directions, top PCA directions and single activations, using the
   repo's protocol (same unit sphere, same conditioning quantile, true-on-event conditioning where defined).
   Primary metric: AUC of lift for G vs P and G vs coloured null. Pre-set bar: AUC >= 0.9 for the score to
   count as valid on ground truth.
3. Run the ascent from 2,000 random activations, whitened and raw. Count distinct endpoints and the share
   within cosine 0.9 of a G feature, a P feature, or a top PCA direction. Run the random-init floor.
4. Train a small TopK transcoder and residual SAE on the toy and score their directions; add one harder
   variant with correlated feature co-occurrence, where PCA and features diverge.

**Part B - Gemma-3-1b, layers 13 and 17 (7 and 22 if time).**
5. Cache about 400k token states at the MLP input. Gemma 3 wraps the MLP in pre- and post-feedforward norms
   (confirmed in the Gemma Scope 2 configs), so J is taken for the whole map residual -> pre-norm -> MLP ->
   post-norm, and transcoder encoder directions are pulled back to residual coordinates through the norm gain.
6. Arms, 2,000 directions each where available, widths 16k and 262k, medium L0: transcoder encoder (read)
   directions; transcoder decoder (write) directions; MLP-output SAE decoders; residual SAE decoders at layer
   L-1 and L; single activations; token-mean directions; top-200 PCA directions; coloured random (the floor);
   30 supervised mean-difference probes (part-of-speech and simple lexical classes, as in the repo).
7. Metrics: same-direction lift v.Jv for all arms; for transcoders also read-to-write lift (decoder . J .
   encoder). Conditioning on true encoder firing for dictionary arms and on frequency-matched projection
   quantiles for every arm, reporting both. Compare arms within frequency-matched bins; report AUC against the
   coloured null and against residual SAEs, with bootstrap CIs.
8. Within transcoders, test whether lift predicts causal weight (drop in MLP-output reconstruction when the
   latent is ablated) and cross-width persistence; Spearman, frequency partialled out.
9. Run the ascent from 1,000 activations per layer with the random-init floor; report endpoint count and the
   nearest transcoder / SAE latent per endpoint.

## 4. Stage 1 cost estimate
Prices from runpod.io/pricing on 2026-11-14.
- Toy: CPU or a few GPU-minutes per seed; **$5**.
- Gemma: one A40 48 GB at $0.59/h. Lift for about 20 arm-configurations x 2,000 directions x 512 states =
  about 20M MLP-only JVPs per layer (under 2 h); caching, flows, floors and ablations 8 h. About 30 h for four
  layers; x2.5 for debugging and reruns = 75 h -> **$45**.
- Downloads/storage (16 dictionaries x 0.15-2.4 GB, state cache): **$10**.
- LLM labelling of flow endpoints (a few hundred, claude-haiku-5.5 at $0.10/$0.50 per M via OpenRouter): **$5**.
- Contingency: **$35**.
Total **$100**.

## 5. What success looks like
- Toy: a verdict on validity. Lift either separates gated from pass-through features (AUC >= 0.9, robust to
  frequency) or not; the flow either recovers most of the 128 gated features or collapses to a few endpoints.
  The quotable number: "planted 128 denoised features; the flow finds N".
- Gemma: a ladder plot of frequency-matched lift by arm with CIs. Post-worthy positive: transcoder read
  directions clearly above residual SAE features and activations (AUC vs residual SAEs > 0.7), and lift
  correlating with ablation weight. Post-worthy negative: transcoder features indistinguishable from residual
  SAE features or below raw activations, as SAE features were on GPT-2, while the toy shows lift is valid;
  that says transcoder latents are not the units the MLP error-corrects.
- Ambiguous: toy AUC 0.6-0.8 and sensitive to threshold and whitening. Then Part B cannot be interpreted and
  the post is the toy alone, a calibration of a method whose author asked for criticism; publishable but smaller.

## 6. Stage 2 (if stage 1 succeeds)
About $300: all 26 layers and the 4b model; cross-layer transcoders (`clt/`) with a multi-layer composed
Jacobian; lift as a filter for attribution graphs; the author's conjecture that the word-continuation
attractor overlaps the emergent-misalignment direction.

## 7. Risks and how the plan handles them
- *Many knobs (threshold, whitening, conditioning).* The toy fixes the protocol before Gemma is touched; Part
  B reports the full whitened/raw x conditioning grid.
- *Sandwich norms break the "same direction in and out" picture.* Use the whole-block Jacobian in residual
  coordinates and add the read-to-write variant; validate on the toy by adding a norm layer to one seed.
- *Frequency artifacts:* encoder-event conditioning, frequency-matched bins and coloured nulls from the start.
- *Toy too easy.* The correlated variant and dictionary-on-toy arms give it a non-trivial failure mode.
- *Repo code is GPT-2-specific.* Only the JVP, null and flow routines are reused; a go/no-go check reproduces
  the repo's block-8 ladder (coloured 0.04, activations 0.17) on `apollo-research/gpt2_noLN` first.
- *Gated weights.* Official Gemma 3 repos need approval; the ungated `unsloth` mirror is validated by
  checking the released transcoder's reconstruction error on it.
