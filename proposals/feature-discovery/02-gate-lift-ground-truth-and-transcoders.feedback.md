# Feedback: "Does the MLP error-correct what transcoders call features? Gate lift on a planted toy and on Gemma 3"

Verdict: **major overhaul**. The toy flow-recovery experiment is worth keeping; the Gemma/transcoder half is
conceptually confounded, partly scooped, and the most likely source of mush.

What I checked (2026-11-14). WebSearch was unavailable to me as well (shared budget exhausted), so the
"already done?" check is again limited to arXiv API queries, LessWrong GraphQL (comments, pingbacks), raw
GitHub files and the Hugging Face API. A reviser with search should still run the queries listed in NOTES.md.

| Claim in proposal | Status |
|---|---|
| Post's claims (random ~0 < activations < SAE features; four attractors from 100k+ tokens; "just PCA" worry) | Confirmed from post text |
| Repo block-8 ladder: coloured 0.04, activations 0.17, SAE 0.09-0.13, probes 0.2-0.3 | Confirmed (README). Note RESULTS.md gives a different ordering at L6: features 0.184 > activations 0.166, feature-vs-coloured AUC 0.97. The proposal quotes only the layer where SAE features lose |
| Frequency/width trends vanish under encoder conditioning; random-init floor ~0.7; layer-global, corpus-dependent library | Confirmed (README, RESULTS.md) |
| David Africa replication, GPT-2 small-XL, median 1/1/3/3.5 attractors | Confirmed (comment, 20 karma) |
| `gates/` code public and reusable | Public. `gates/metric.py` (exact-JVP lift, coloured nulls) is ~100 lines and model-agnostic apart from a TransformerLens `blk.mlp(blk.ln2(x))` closure. `gates/flow.py` is **not** portable as-is (see pre-mortem) |
| `google/gemma-scope-2-1b-pt` ungated; `transcoder/`, `resid_post/`, `mlp_out/` at layers 7/13/17/22; widths 16k/65k/262k | Confirmed (HF API; cc-by-4.0; 16k params 151 MB, 262k params 2.4 GB) |
| Transcoder reads `pre_feedforward_layernorm.output`, writes `post_feedforward_layernorm.output` | Confirmed from config.json |
| `unsloth/gemma-3-1b-pt`, `apollo-research/gpt2_noLN`, `NeelNanda/pile-10k` ungated | Confirmed |
| A40 $0.59/h | Confirmed (RunPod Secure Cloud; Community Cloud is $0.35/h) |
| claude-haiku-5.5 $0.10/$0.50 per M | Confirmed (OpenRouter API) |
| "Transcoders and the MLP Jacobian have never been compared" | **Not true in the form that matters** - see section 2 |

## 1. Would it get upvoted?

Probably not past 50. My estimate is 15-40 karma for the stage-1 result as described.

- The parent post got 56 karma and three comments, one of them substantive. It is a niche method with a small
  audience (the author, Heimersheim-adjacent error-correction people, a few theory-minded interp readers). The
  one pingback I found ("What if not Circuits?", 146 karma) cites it in a single sentence as "cool"; the
  interest there is in denoising as a paradigm, not in gate lift as a metric.
- Gemma Scope 2's 96 karma was for a tool release. A post that uses the tool to score directions with a
  third party's unvalidated metric does not inherit that audience.
- The headline as framed ("transcoder features are / are not what the MLP error-corrects") needs the reader to
  already trust gate lift. The repo's own honest-limitations list (conditioning artifacts, random-init floor,
  whitened and raw frames ranking directions differently, surrogate vs raw disagreement) means informed readers
  will not, and the proposal's Part B stacks a second layer of knobs on top.
- The part that could travel is the toy: "planted 128 denoised features; the ascent finds N". If N is small,
  that is a crisp deflation of "exactly four ur-features" that the author explicitly invited. That is a
  30-50 karma post on its own if cleanly done, and it is the part least dependent on Gemma.

## 2. Naturalness

Mixed. A ground-truth test of the score and of the flow is a natural next step that the author asked for and
that I could not find done (repo, comments, pingbacks, arXiv API). Comparing with transcoder features was the
screener's suggestion and is a reasonable thought, but it is a side-branch, and two things undercut it.

**Adjacent prior work the proposal missed.** Shabalin & Piotrowski, "Comparing Sparsified MLPs and Transcoders:
Many Transcoder Features Are Neurons in Disguise" (arXiv 2610.24521, 17 Oct 2026) compares transcoder features
against the MLP Jacobian directly, including Gemma Scope 2 transcoders on Gemma 3 (their main figures are Gemma
3 4B). They compute each feature's rank-1 Jacobian contribution (decoder x effective encoder), and report that
whole-transcoder Jacobian alignment with the MLP is about 0.3, that it comes almost entirely from
neuron-aligned features (about half of active features in late layers), and that non-neuron features reach
only about 0.05 and are unstable across seeds. This is not gate lift, but it means:
- "the two notions have never been compared" is no longer a fair statement of the gap; the generic question
  "do transcoder features match the MLP's local linear map?" has a recent, more careful answer;
- that paper's read-to-write quantity is essentially the proposal's "decoder . J . encoder" arm;
- any Gemma result must be stratified by neuron-aligned vs non-neuron features or it will be confounded by
  the mixture and look naive to anyone who has read that paper.

**The comparison is not well-posed as designed.** Gate lift is a same-direction quantity: v.Jv asks whether the
MLP writes back along the direction it reads. A transcoder feature is defined by reading one direction and
writing a different one; that is the point of transcoders. So:
- same-direction lift on encoder or decoder directions will be low for any feature that computes something
  new, regardless of how "natural" it is. A null here does not say "transcoder latents are not the units the
  MLP error-corrects" in any interesting sense; it says transcoders model computation rather than
  self-amplification, which is known by construction;
- read-to-write lift (d.J.e conditioned on the feature firing vs not) is close to tautological in the other
  direction: the transcoder was trained so that the MLP output moves along d when e's pre-activation crosses
  threshold. A positive result is "the transcoder fits the map it was fitted to".
Neither outcome is the "post-worthy positive/negative" the proposal claims. The original authors would more
naturally want: (i) ground truth, (ii) the same test on a second model family, (iii) error-correction measured
through later layers (Africa's comment found the opposite sign there, which is the most interesting loose
thread in the comments and is ignored here).

## 3. Pre-mortem

How the two days go:

*Day 1 morning, toy.* It trains quickly. The lift-AUC test passes almost by construction: G features are
trained to have y = threshold(x) along v, so in y = x + MLP(x) the MLP contributes about -1 along v when the
feature is off and about 0 when it is on; lift is about +1 for G and about 0 for P. AUC >= 0.9 is the
expected outcome of the training objective, not evidence about the metric. The only informative lift results
are the failures: P features acquiring lift through interference with G features (256 features in 64
dimensions guarantees overlap), and frequency sensitivity under the repo's fixed top-q = 0.005 conditioning
when feature frequencies span two orders of magnitude. The flow is the real experiment and should give a clean
answer either way.

*Day 1 afternoon, porting.* `gates/metric.py` ports easily. `gates/flow.py` does not: it ascends a factorized
surrogate built from `W_out`, per-neuron GELU-derivative shifts and a mean read operator from 768 basis JVPs,
with degenerate directions projected out by hand. With Gemma's post-feedforward RMSNorm after `W_out` the
factorization is no longer exact, and the README says surrogate and raw lift already disagree on rankings in
GPT-2. The more portable `gates.minima.lift_flow` (Adam on conditioned lift) is a different protocol that
gives a different attractor set on the same model (the README says so explicitly). The proposal does not say
which flow it means; the team will pick one mid-run.

*Day 2, Gemma.* Specific problems:
- Gemma residual streams have a few very high-variance directions and an extreme BOS state. Coloured nulls
  and top PCA directions will be dominated by them; the whitening epsilon (0.1 in the post, shrinkage 0.1 in
  the repo, both tuned on GPT-2 noLN) becomes a consequential free parameter.
- Conditioning is not comparable across arms. Dictionary arms can use encoder firing; activations, PCA,
  token-means, probes and nulls can only use projection quantiles. The repo's own finding is that this choice
  flips the sign of frequency effects. "Frequency-matched projection quantiles for every arm" is undefined for
  arms with no frequency. At 262k width most latents fire well below 0.5% of tokens, so top-q = 0.005 on 400k
  states is mostly off-states for them, and encoder-conditioned on-sets may have tens of samples.
- The Jacobian choice (residual -> pre-norm -> MLP -> post-norm) puts transcoder encoder directions and
  residual SAE decoder directions in the same space only after a pullback through the RMSNorm gain, which is
  state-dependent. A small bug here silently shifts one arm relative to the others, and the arms differ by
  0.05-0.1 in lift on GPT-2.
- The proposal commits to reporting "the full whitened/raw x conditioning grid". With about 9 arms, 2 widths,
  2 conditionings, 2 metrics, 2 frames and 2-4 layers, the arm ordering will differ across cells. That is the
  mush outcome and I think it is the modal one.
- "The toy shows lift is valid, therefore the Gemma null is about transcoders" does not follow. Validity on a
  toy whose features were trained to be gated says nothing about whether real MLP computation takes the
  same-direction gating form.

Forecast for stage 1 as written:
- Clear positive (transcoder ladder cleanly above residual SAEs, robust across the grid, plus valid toy): 10%
- Clear negative that is still interesting (mainly: toy flow collapses to a handful of endpoints despite 128
  planted gated features, or recovers them, with a clean count): 30%. Almost all of this mass comes from Part A.
- Ambiguous mush (toy fine, Gemma ordering protocol-dependent, post becomes a long table): 45%
- Fails to run / Gemma part not finished or buggy: 15%

Even the "clear" Gemma outcomes are unsurprising for the reasons in section 2, so the probability of a
>50-karma post is about 10-15%, carried by the toy.

## 4. Cost check

The estimate is realistic; if anything compute is over-budgeted and effort under-budgeted. The repo's protocol
uses about 10.5k states per direction (2,500 on + 8,000 off), not 512, so the JVP count is roughly 20x the
proposal's figure, but these are JVPs through a single 1152 -> 6912 -> 1152 MLP and still take minutes to low
hours on an A40. Caches are about 1 GB per layer in fp16. Labelling cost is negligible. My estimate:
**$60-150**, with $100 a fair central figure. Cost is not the constraint; agent time and interpretability of
the output are.

## 5. Recommended changes

1. **Make the flow-on-ground-truth experiment the whole of stage 1's headline, and make the toy able to
   fail.** Do not train features to be gated along their own direction and then score that. Instead train the
   toy on a downstream task with noisy superposed inputs (for example a computation-in-superposition setup in
   the style of the Hanni et al. / Adler-Shavit papers the post cites, or a two-block network where block 1 is
   free to denoise or not), and derive ground truth from the trained network (which features it actually
   cleans up, measured by output noise variance conditional on on/off) rather than from the loss. Include a
   "computes a new feature from two inputs" class (read A and B, write C) alongside gated and pass-through, since
   that is the case that distinguishes same-direction lift from transcoder-style computation.
2. **Pre-register one protocol, not a grid.** Fix one flow (state which: surrogate eigenflow or
   `lift_flow`), one frame, one conditioning rule, chosen on GPT-2 noLN where the repo's numbers can be
   reproduced, and report alternatives only as a robustness appendix. State the planted-feature count sweep
   (for example 8, 32, 128, 512) so the result is a curve of recovered endpoints vs planted features rather than one number.
3. **Cut Part B to a narrow, defensible question or drop it.** If kept: one layer, one width (16k), and three
   arms that share a conditioning rule (transcoder latents split into neuron-aligned vs non-neuron following
   arXiv 2610.24521, residual SAE latents with encoder conditioning, coloured nulls). Cite that paper and
   position the result against its Jacobian-alignment finding. Drop single activations, token means, PCA and
   probes from the headline comparison because they cannot be conditioned the same way. Drop the ablation
   correlation, cross-width persistence and LLM labelling.
4. **Drop the framing "are transcoder features computation-natural by gate lift".** State up front that
   same-direction lift is zero for pure read-A-write-B features and that read-to-write lift is what the
   transcoder was trained on. If a Gemma arm stays, the question should be the narrower "which dictionary
   latents sit on self-gated directions, and is that the neuron-aligned subset?".
5. **Consider replacing Part B with the loose thread in the comments.** Africa found that perturbations along
   attractors persist less through later MLPs when the attractor is active, the opposite of the gate picture.
   Replicating that on GPT-2 with the repo's composed multi-layer JVP (already implemented, RESULTS.md
   "multilayer composed lift") is cheaper, needs no Gemma port, and speaks to whether "error correction" is the
   right description at all. Toy + this is a more coherent post than toy + Gemma ladder.
6. **Fix the prior-work section.** Add the L6 numbers (features 0.184 > activations 0.166) so the repo is not
   presented as showing only that SAE features lose; add arXiv 2610.24521; remove "have never been compared".
7. If the funder must choose within this cluster, proposal 01 (null-dictionary ladder for Exemplar
   Partitioning) is the better use of money per NOTES.md's own ranking; fund this one only in the reduced
   toy-first form, at about $50.
