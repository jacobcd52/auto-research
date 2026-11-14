# Feedback: Do LLMs build telescoping belief cones over sources they infer in context?

Verdict: **major overhaul, then fundable.** The question is good and apparently open, the models and prices check out, and the cost is low. But the primary source pair cannot pass the proposal's own behavioural gate, the episode length never produces a "ruled-out" source, and the key cone-versus-cylinder analysis is confounded with recent-token features. All three are fixable before any GPU is rented.

Search caveat: the WebSearch tool was unavailable (shared budget exhausted), as it was for the proposer. Prior-work checks used the arXiv API, the LessWrong GraphQL API, the Hugging Face API, the Simplex blog and the full text of the Balcells et al. PDF. Non-arXiv follow-ups (Twitter, personal blogs, unlisted repos) are unchecked.

## What I verified

| Claim in the proposal | Status |
|---|---|
| Post: 2x Mess3, 4-layer d128 model, held-out R^2 about 0.985 after block 3, about 0.45 untrained | Confirmed from the post text |
| Post links no code | Confirmed (no repo link in the post) |
| Footnote 10 offers the "normalized belief plus separate which-source variable" alternative | Footnote marker confirmed; I could not extract the footnote body, so the paraphrase is unverified |
| Balcells et al., arXiv 2609.17376: six LLMs, 40 single HMMs, 20,000 tokens, R^2 0.83-0.99, KL 0.009-0.018 nats | Confirmed from the PDF |
| Balcells et al. has no mixture condition and no code link | Confirmed ("nonergodic" absent; mixture-of-HMMs only cited as Xie et al.'s framing; no GitHub URL) |
| Kowalyshyn et al., arXiv 2605.08405: two graphs, orthogonal PCA subspaces, no belief target | Confirmed from the abstract |
| `Qwen/Qwen3.5-9B`, `Qwen/Qwen3.5-4B`, `google/gemma-4-E4B` ungated; Llama-3.1-8B gated | Confirmed via the HF API (Llama is `gated: manual`) |
| RunPod A100 PCIe 80 GB at $2.09/hr | Confirmed on the pricing page (community cloud is $1.19/hr) |
| Experiment not already done | No hit on arXiv (belief-state geometry, nonergodic, mixture-of-HMM queries; Shai and Riechers author lists) or in LessWrong post titles from 2026-10-12 to 2026-11-14 |

Two things the proposal omits from its summary of Balcells et al., both of which matter:

- **Their HMMs are selected.** The 40 processes sit in the slow-mixing, low-entropy region (second eigenvalue 0.85-0.99, normalized entropy 0.18-0.48) "following Dai et al.", and were chosen as ones where LLMs predict near-optimally. Their headline Mess3 is (alpha = 0.01, x = 0.02) in their convention. Their Table 3 lists Mess3, Wing and Strata parametrizations where the belief probe shows no gap over a 1-token-suffix predictor.
- **Their probes are fit per sequence**, on positions at or after 15,000, with KL falling over "the first 5,000-10,000 tokens" before it plateaus.

## 1. Would it get upvoted?

If stage 1 succeeded exactly as described, probably yes: 50-90 karma. The cluster's posts got 87 and 74, and "the Simplex cone picture holds in an off-the-shelf LLM, with a figure of a cone collapsing in Qwen" is a natural sequel that interpretability readers and the persona/simulator crowd would both read. The "cylinder" outcome would do as well or better, if it survived the confound in section 3 below.

The weaker outcomes are not post-worthy. A null gated on a behavioural check that barely passes reads as "the LLM did not learn the task", and a gate failure is a short note. Unconditionally, I put the chance of a >50-karma post at about 20-25%.

## 2. Naturalness

Mainline. The post's opening is about LLM training data being nonergodic, and Balcells et al. explicitly split in-context learning into level 1 (which process) and level 2 (state within it) and study only level 2. Combining the two is the obvious next step and readers would ask for it.

That cuts both ways for scoop risk: the same group owns the theory, the LLM pipeline and unreleased code, and has said in comments that related work is coming "soon". I found no evidence it exists yet. The resetting-episode design is the proposal's own invention, not the post's process, which is a reasonable adaptation but means the result is not a strict replication.

## 3. Pre-mortem

I ran a quick exact-Bayes simulation (standard Mess3 convention, 4,000 episodes of 96 tokens) to check the design before any LLM is involved. The parameters for the post's pair are the proposer's reading of the blog's MathML (x = 0.15, alpha = 0.6 and x = 0.5, alpha = 0.66), which the blog source does contain; the second component's convention is uncertain, so treat the numbers as order-of-magnitude.

| Pair | Second eigenvalues | Mean posterior on true source at token 96 | Positions with true-source weight below 0.1 | Mixture predictor's gain over uniform (nats/token) | Gain over a blend that ignores the source |
|---|---|---|---|---|---|
| Post's pair (i) | 0.55, 0.50 | 0.88 | 1.4% | 0.009 | 0.005 |
| Post's first component vs a low-entropy Mess3 (x = 0.05, alpha = 0.85) | 0.55, 0.85 | 0.996 | 0.7% | 0.15 | 0.034 |
| Two low-entropy Mess3 (x = 0.02, alpha = 0.95; x = 0.05, alpha = 0.80) | 0.94, 0.85 | 0.99 | 0.9% | 0.44 | 0.024 |

What this implies:

- **Pair (i) is dead on arrival.** The whole Bayes-optimal predictor beats a uniform guess by about 0.009 nats per token, and tracking the source is worth about 0.005. The LLM's own error floor in Balcells et al.'s best cases is 0.009-0.018 nats. The gate ("beats source-blind baselines") cannot be passed with any power, and the process is fast-mixing and near-maximum-entropy, the opposite of the regime where LLMs are known to learn HMMs in context.
- **Nothing is ever ruled out in 96 tokens.** For all three pairs, the true source's weight is below 0.1 at about 1% of positions, so by symmetry a source is confidently wrong-and-discarded only when the other is confidently right, and for pair (i) that rarely happens at all. The risk section worries about "few low-w samples"; for pair (i) the bigger problem is that weights mostly sit between 0.1 and 0.9, and for the better pairs the weight is confounded with within-episode position.
- **Source inference is a small part of the loss even in good pairs** (0.02-0.03 nats per token), so the LLM can pass a KL gate while doing little level-1 inference. The gate must compare against the source-blind blend specifically, per within-episode position, not just against order-k Markov baselines.

Other failure modes, in rough order of likelihood:

1. **The cylinder outcome is confounded with recent-token features.** A source's normalized belief is a deterministic, fading-memory function of the recent tokens whether or not that source is active. Any representation that encodes the last few tokens yields a "constant-radius" map from `eta_A` at every weight. The post's untrained network already gets R^2 0.45 this way. As written, the "LLM keeps simulating the discarded source" headline could be produced by token-suffix encoding alone. Slow-mixing sources reduce this but do not remove it.
2. **The joint R^2 threshold is nearly uninformative.** Most variance in the 6-entry weighted belief is the weight itself moving the cone centroid. A model that encodes only `w` linearly can score a high joint R^2. The telescoping signature is the product term `w * (eta - mean)`, which the plan never isolates.
3. **The radius estimate is biased.** The norm of a fitted map from a 2-d target into 4,096 dimensions is inflated by noise, more so in small bins, which are exactly the intermediate-weight bins. Without a cross-validated norm, the slope and intercept are artefact-prone.
4. **Unsupervised clustering in context is much harder than what Balcells et al. tested.** A single HMM took 5,000-10,000 tokens to converge. Here the model must also discover that newlines reset the source and segment unlabelled episodes into two processes. By token 12,000 each source has about 6,000 tokens. I expect the unlabelled format to fail the gate more often than not; the labelled format is the realistic condition.
5. **Held-out-sequence probes may fail for a boring reason.** Balcells et al. fit per sequence. If the in-context representation's basis varies across contexts, cross-sequence R^2 drops below 0.8 even when the geometry is present. The plan treats the stricter split as pure upside.
6. **Scope for two days.** Three models, four conditions, a toy positive control, probing, cone test and steering, all re-implemented from a paper with no code, is too much. Something will be done shallowly, most likely the controls.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (cone in at least two LLMs, survives controls) | 15% |
| Clear, interesting negative (clean cylinder or well-powered null with the gate passed) | 15% |
| Ambiguous mush (gate marginal, moderate R^2, slope positive but intercept far from zero, controls incomplete) | 50% |
| Gate fails everywhere or pipeline does not finish | 20% |

With the changes below I would move about 15 points from mush to the two clear outcomes.

## 4. Cost check

The estimate is realistic. Forward passes on 20,000 tokens for a 9B model in half precision fit an 80 GB card and take well under a minute; 40 GPU-hours at $2.09 is generous.

One omission: caching all 33 layers at 8,000 positions is about 2 GB per sequence in fp16, roughly 170 GB per model for 80 sequences. Subsample layers or fit probes streaming; otherwise disk, not GPU, is the bottleneck. My estimate: **$120-250**, comfortably under the cap. Cost is not the problem with this proposal.

## 5. Recommended changes, in order of importance

1. **Choose the process by simulation before renting anything (free, one hour).** Require, under exact Bayes: source inference worth at least 0.05 nats per token over the source-blind blend, both sources slow-mixing and low-entropy (inside Balcells et al.'s validated region, ideally two of their own 40 parametrizations with a shared alphabet), and at least 15% of positions in each of low, middle and high weight bins. Drop pair (i) from the LLM experiment entirely; keep it only for the toy control.
2. **Fix the episode design so sources actually get ruled out and then matter again.** Longer episodes (300-500 tokens) or a source-informative early stretch, so there is a long tail at weight near 0 for the discarded source. Vary episode length so weight is not a function of position.
3. **Replace the headline statistic with a product-term test.** Report held-out R^2 for `w * (eta_A - mean)` and compare with the ceiling achievable by a linear function of ground-truth `[w, eta_A, eta_B]` (what a separate-variables code would give a linear probe). Validate that this separates cone from cylinder in the toy, including a synthetic cylinder built by construction.
4. **Control for token-suffix features in the cone test.** Residualize activations on one-hot encodings of the last k tokens (k up to 6-8) and on within-episode position before fitting radius; report the radius of the k-suffix belief under the same procedure. Without this, a cylinder result is uninterpretable.
5. **Use a cross-validated radius** (inner product of maps fit on disjoint halves) instead of a raw norm, with bootstrap over sequences.
6. **Report both per-sequence and held-out-sequence probes.** Match Balcells et al. first (per sequence), then show the stricter split as an extra.
7. **Cut scope.** One model (Qwen3.5-9B) and the labelled format first; add Qwen3.5-4B only after the full analysis runs end to end. Treat unlabelled contexts and Gemma as stretch. Make the steering check stretch too; the product-term test plus suffix controls is the result.
8. **Make the gate specific to level-1 inference.** Pass only if the LLM's KL to the Bayes mixture is below its KL to the source-blind blend by a bootstrap-significant margin at late within-episode positions, and if its predictions track the weight after a source switch.
9. **State the scoop position honestly in the write-up plan.** The same group could publish this at any time; aim to post within days of finishing stage 1.

If the simulation in change 1 cannot find a pair that meets all three criteria within the validated HMM families, drop this proposal and fund the cluster's toy-model proposal (02) instead.
