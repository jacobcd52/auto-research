# Feedback: The pirate who keeps speaking Chinese (steering / 02)

Verdict: **keep with tweaks**, but go in expecting a deflationary null and redesign the arms so that null is
clean. As written, the main comparison is confounded by steering strength and by "clamp vs shift", and several
arms will probably produce garbage for reasons unrelated to conceptors.

## What I verified

- **Post** (read in full): no experiments; x' = x + C(d - x); "brutal butchery" for the full 274-dim span; top-k
  "less bad" with an arbitrary cutoff; "act like a pirate but keep speaking Chinese". 60 karma, 1 comment (finance
  shrinkage), no pingbacks. The proposal's summary is accurate. The whitened version and the three ways of choosing
  aperture are in footnotes, as stated.
- **Vectors**: `lu-christina/assistant-axis-vectors` is public, ungated, MIT. 275 role vectors + 240 trait vectors
  per model for gemma-2-27b, qwen-3-32b, llama-3.3-70b, plus `default_vector.pt` and `assistant_axis.pt`. I
  downloaded `gemma-2-27b/role_vectors/pirate.pt`: 425,442 bytes, consistent with 46 layers x 4608 dims in float16.
  (Could not load it; no torch on this machine.)
- **Models**: `unsloth/gemma-2-27b-it` and `Qwen/Qwen3-32B` are ungated.
- **Papers**: arXiv 2410.16314, 2605.04980, 2610.16325, 2601.10387 exist and the abstracts match the proposal's
  descriptions, including the 0.093%-7.815% and 480-comparison figures. Caveat the proposal glosses over:
  2610.16325 studied one specific regime (aperture 0.05, gain 2, where the map expands every direction). It does
  not show that conceptor results in general are "mostly gain"; do not lean on it as a prior beyond "check
  attribution".
- **Prices**: OpenRouter `anthropic/claude-haiku-5.5` $0.10/$0.50 and `anthropic/claude-sonnet-5.5` $2/$10 per M
  confirmed today (batch variants are half price). RunPod page shows "H100 80GB from $1.99/hr", consistent with the
  notes' $1.99 community / $2.89 secure.
- **Already done?** WebSearch budget was exhausted for me as well, so this check is again limited to direct
  sources: arXiv API ("conceptor" + persona/role/steering returns only the four known papers plus an unrelated
  2022 one; "assistant axis" returns the original paper, 2608.00023 role steering, 2605.09391 "Do Linear Probes
  Generalize Better in Persona Coordinates?" and one unrelated paper; none uses conceptors), LessWrong GraphQL (the
  author has posted nothing further on conceptors; no pingbacks to the post). I found no test of the transplant
  claim. GitHub and general web were not checked; a private or Twitter-only replication is possible but I saw no
  sign of one.

## 1. Would it get upvoted?

Marginal. My estimate is roughly 30% for >50 karma if it runs as described.

- The source post got 60 karma with one comment and no follow-up from anyone in four months. That is an appreciated
  explainer, not a live research thread. The audience actively waiting for this result is small.
- The most likely result ("soft vs hard makes no measurable difference; adding the role vector is as good or
  better") is what most steering practitioners already expect. A null on an untested aside in an explainer is a
  20-40 karma post unless the write-up delivers something beyond the null.
- What could lift it above 50: (a) a surprising positive (unlikely, see below); (b) a striking, concrete finding
  about persona space that stands on its own, e.g. "donor topic leaks through the persona subspace and turns
  your pirate into an accountant", or a measured answer to "how many of the 274 dimensions are persona and how many
  are context"; (c) a genuinely usable recipe for transplanting a persona from a single uncontrolled sample.
  The proposal as written is organised around the soft-vs-hard horse race, which is the least interesting axis.
- Who cares: people using Assistant Axis / persona vectors, and the post's author. The safety relevance in section
  2 ("persona-space interventions are becoming a standard safety tool") is real but this experiment does not touch
  a safety-relevant behaviour; stage 2 does.

## 2. Naturalness

It is the obvious follow-up to that post: it tests the post's one concrete, falsifiable claim on the exact assets
the post names. It is not contrived. But the post itself is a side-branch of the steering literature, and the
cluster's other post (Bostock, 68 karma, many substantive comments asking for specific experiments) has much more
reader demand behind it. This is a legitimate but second-tier direction. Not already done as far as I could check.

## 3. Pre-mortem

Forecast: clear positive (conceptor robustly beats matched top-k and role-vector addition on both models) **8%**;
clear, interesting negative **40%**; ambiguous mush **40%**; fails to run / unusable **12%**.

How I expect it to play out, and the specific failure points:

1. **Strength confound (most important).** The transplant arms have no gain: x' = x + M(d - x) at one middle layer
   with coefficient 1. Single-layer steering usually needs several times the natural mean difference to change
   behaviour. Meanwhile arm 6 (role-vector addition) gets 8 strengths. Likely pilot outcome: transplant arms barely
   move persona at small k, addition works at high strength, and the "frontier" comparison is between a method
   with a strength knob and methods without one. Worse, at matched trace the conceptor puts weight below 1 on the
   top PCs and top-k puts exactly 1, so any conceptor-vs-top-k difference is partly a gain difference on PC1-3.
   This is exactly the attribution trap 2610.16325 describes, and the listed controls (random directions,
   constant weights of equal trace) do not remove it.
2. **Clamp vs shift.** With d a fixed mean and x the per-token activation, M(d - x) does not add a persona offset;
   it overwrites the per-token component of x inside the subspace with a constant at every response position.
   At k = 100-250 that erases token-specific information in hundreds of directions; at M = I it erases
   everything computed below that layer at every generated position, so the model cannot even see its own
   previous token. Arm 1 will be gibberish, not a "maximum leakage reference", and the full-span/large-k arms will
   look bad because of clamping, which would wrongly confirm "brutal butchery". The fair version of the post's
   idea is the shift form x' = x + beta * M(d - mu_recipient), with mu the mean recipient activation.
3. **Floor effect on language.** A 274-dim subspace captures about 6% of the squared norm of a random direction in
   4608 dims. The language difference will mostly lie outside the role span, and a single mid-layer intervention
   is a weak way to flip output language. I expect recipient-language retention near 100% for every subspace
   method at every size, so the title metric will not discriminate. Topic leakage is more promising because many
   roles are occupational and role vectors plausibly encode topic; length leakage is plausible too. The pilot
   must show that at least one leakage metric moves between top-3 and full-span before the full run is spent.
4. **Soft vs hard is probably behaviourally invisible.** Conceptor and top-k share eigenvectors; they differ only
   in spectral weights on a spectrum that the Assistant Axis paper reports as steep. Even if the displacement
   differs by 20-30% in norm, judged behaviour at n = 24 personas will overlap. Bootstrap unit is the persona,
   so 65k generations do not buy much power: the effective n is 24 (12 for arm 6).
5. **Persona judge.** A 0-100 "written by the named persona" score will be dominated by caricature markers;
   subtle personas will sit at the floor for all activation methods and inflate noise. 24-way identification
   helps but will be near ceiling for pirates and near chance for auditors.
6. **Donor design.** "One of 4 donor languages and 4 donor topics" per persona confounds persona with donor
   context unless crossed. Each persona needs at least two donor contexts.
7. **Implementation hazards.** Layer-index / hook-point mismatch with released vectors (handled by step 1, good).
   Donor activations computed by the team's pipeline will differ in scale and token selection from the released
   means; compare your recomputed vector for an in-set role with the released one (cosine and norm) before mixing
   them in one analysis. Qwen3 must run with thinking disabled, matching how the vectors were extracted. Gemma 2
   has no system role, so the "system prompt" ceiling needs the paper's convention. Generating in four languages
   with a 120-token cap will truncate mid-sentence and skews length-ratio metrics.
8. **Too many arms.** 45 settings x two models x three layers plus whitened and attribution arms is a lot of
   surface for a two-day agent team; the mush probability comes largely from spreading 24 personas across arms
   that were never going to differ.

Most likely write-up: "all role-subspace methods transfer caricature personas weakly, language never leaks,
large-k clamping hurts coherence, soft vs hard is within noise, role-vector addition with a tuned coefficient is
best". True, mildly useful, modest karma.

## 4. Cost check

The $210 estimate is realistic and probably a little high on GPU time.

- Generation: about 10.8M new tokens. A hooked HF model at batch 32-64 on one H100 should do roughly 500-1,000
  tokens/s for a 27B model in bf16 (about 54 GB of weights, leaving limited batch headroom on 80 GB), i.e.
  3-6 h for the Gemma run and 2-3 h for Qwen. 45 h budgeted leaves ample room for pilots and reruns.
- Judging: 270k calls x (500 in + 40 out) = 135M in + 10.8M out = $13.50 + $5.40 = about $19 at verified prices.
  Correct. The batch endpoint would halve it but is not worth the latency in a two-day run.
- My estimate: **$120-220**; the recommended changes below reduce generation count, so about $150 is likely.
  Well under the $500 cap.

## 5. Recommended changes (in order of importance)

1. **Add a gain and use the shift form as the primary intervention.** Primary: x' = x + beta * M(d - mu_recip),
   beta swept over 5-6 values for every M. Keep the literal post formula x + M(d - x) (clamp, beta = 1) as a
   secondary arm, reported separately, since it is what the post wrote. Compare methods at matched persona
   transfer, not only at matched trace. Drop M = I at all positions as a "reference"; it is not interpretable.
2. **Hour-one, zero-generation gate.** From the released vectors alone, plot the eigen-spectrum and compute, for
   real (d - mu) differences, the norm and cosine of C(d - mu) versus P_k(d - mu) at matched trace, and the
   fraction of the language, topic and length mean-difference vectors that lies in the role span and in the top-k.
   If the language difference has a negligible in-span component, say so, demote language to a secondary metric
   and build the study around topic and length leakage. If conceptor and top-k displacements are near-identical
   after gain matching, cut the soft-vs-hard arms to two sizes and spend the budget elsewhere.
3. **Measure the noise instead of assuming it.** Record each persona's donor mean in at least 2 languages x 2
   topics (crossed). Per principal component, compute between-persona variance against within-persona,
   across-context variance. This directly tests the post's premise (which directions of the 274 are persona and
   which are context), yields the principled filter (the Wiener / whitened conceptor with a measured noise
   spectrum), and is a figure worth posting regardless of the behavioural outcome. It replaces the vaguely
   specified "noise covariance from generic chat activations" arm.
4. **Add the practitioner's baseline.** Matched-context contrastive vector: persona mean minus default-assistant
   mean in the same donor language and topic. If this is available, nobody needs a filter; the conceptor claim
   only matters for transplanting from an uncontrolled donor. State that framing explicitly and include a
   single-donor-sample condition (d from one response, not a mean), which is where filtering has the best chance
   to help and is closest to what the post describes ("some text written by Persona A").
5. **Cut the grid.** Sizes 3, 10, 30, 100, full; one layer chosen in the pilot (plus one multi-layer check);
   whitened arm only via item 3; Qwen replication only of the two or three arms that matter. Use the saved budget
   for 2-3 samples per cell and more personas (36-48), since persona is the unit of analysis.
6. **Pilot gates before the full run**, stated as go/no-go: (a) role-vector addition reproduces a visible persona
   at some strength without incoherence; (b) at least one leakage metric separates top-3 from full-span;
   (c) recomputed in-set role vectors match released ones (cosine > 0.8 after centring). If (b) fails, the
   write-up becomes the spectrum/noise analysis plus a short "nothing leaks, the butchery claim is wrong in
   practice" result, and the run should stop early rather than fill the grid.
7. **Fix metrics.** Persona transfer as pairwise preference or k-way identification on de-caricatured text rather
   than a 0-100 score; raise max tokens or score only complete sentences; pre-register the combined
   leakage-and-damage score before looking at arms.
8. **Reframe the headline.** Lead with "what is in the persona subspace besides persona" and "how to transplant a
   persona from uncontrolled text", with soft vs hard as one sub-result. That is the version with a chance at >50
   karma.
9. **Funding priority.** If the funder must choose within this cluster, the Bostock follow-up (proposal 01) has
   clearer reader demand. This one is cheap enough to fund as well, but only with changes 1-3.
