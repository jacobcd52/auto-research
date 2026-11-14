# Feedback: "Which part of the belief state lives in the residual stream, and is the rest in the KV cache?"

Verdict: **keep with tweaks**. The question is natural and cheap, and the reused code is public. As written, though, the two headline measurements have near-foregone answers, and the closest prior result is under-cited.

## What I checked

| Claim | Status |
|---|---|
| `artemyk/belief-state` README numbers (0.97 / 0.90 / 0.72 / 0.64, controls 0.97-1.00, ~0.01, 0.17-0.26) | Confirmed against the README (eps = 0.05, random split). |
| Checkpoints committed under `runs/` | Confirmed: I fetched five across all four architectures and both eps values (HTTP 200, 85-590 KB). The README states 4 architectures x 2 eps x 5 seeds. |
| `artemyk/gbs` has the decoder/encoder fitting code | Confirmed. `fit_decoder` accepts arbitrary target coordinates, so regressing true-belief subspaces from the cache is supported. |
| "Released encoder" (step 6) | **Wrong.** The gbs README says the repo ships no pretrained weights and no fitted abstractions. The encoder must be fitted (40k decoder + 10k joint updates per model). |
| Kolchinsky section 5 (cache is the recurrent state, "leakage" conjecture) | Confirmed from the post text. |
| Fomin comment | Confirmed, but the proposal cites only the comment. His linked note (wadimiusz.me/nerode, revised 2026-10-26) is a full study; see section 2. |
| arXiv 2405.15943, 2502.01954, 2602.02385, 2609.17376 | All exist with the stated titles. |
| RunPod RTX 4090 at $0.89/hr | Confirmed on runpod.io/pricing (Secure Cloud; Community Cloud is $0.34/hr). |
| MRRXOR horizon decomposition is well defined | I computed it independently from the README's process definition. At eps = 0.05, dim V_h = 1, 2, 3, 4 for h = 1..4, with cumulative belief-variance shares 0.24, 0.51, 0.83, 1.00. So there is a clean four-rung ladder with one direction per rung and no low-variance rung. |
| Nonergodic post details (0.985, std 0.02, no weights) | Not re-read; taken from NOTES.md. |

Search coverage: the WebSearch budget was exhausted, so the "already done?" check used the arXiv API (five queries on belief state / KV cache / residual stream), LessWrong GraphQL (the post's comments and the 400 newest posts since 2026-10-15), and Fomin's site. I found no paper or post doing the horizon-split or the residual-versus-cache comparison on HMM belief states. Blogs and Twitter are not covered.

## 1. Would it get upvoted?

Borderline; I put it at roughly 35-40% to clear 50 karma if the result is clean, and under 15% if it is mush.

- The parent posts got 87 and 74, but from known authors (Simplex; Kolchinsky) with theory attached. A toy-only empirical follow-up by unknown authors typically lands at 25-50.
- The audience is narrow but engaged: the Simplex group, Kolchinsky, Fomin, Oldenziel. "Adjudicating a live disagreement between two recent posts" is a good hook, and the authors of both would likely comment.
- The pitch that would carry it is practical: "a residual-stream probe at the current position misses state the model will use later; here is how much, as a function of delay and model size". That needs the delay dose-response curve to be clean and at least one non-trivial architectural finding.
- The alternative outcome, "the full belief is there once the model is big enough", is less upvotable. It reads as "Shai et al. were right, and the small-model numbers are underfitting".

## 2. Naturalness

It is mainline. Kolchinsky's section 5 raises exactly this question, and the screener's note asks for a direct comparison with residual-stream probes. Three pieces of prior work shrink the novelty more than the proposal admits.

- **Fomin's note already shows the just-in-time result.** His findings 2 and 3 are that classes differing only in the later future are "mostly not stored" at the current position, with a gap-length dose-response table (MLP-probe accuracy falls from 0.98 to 0.57 over gaps of 1 to 14-23). He includes all-layers-concatenated probes, an untrained twin and a "last six symbols" baseline. He also reports seed heterogeneity: 2 of 10 models carry a running parity. The delay family (process d) is close to a replication of this in HMM language.
- **Shai et al. 2024 already ran the horizon > 1 test on RRXOR.** Belief states with identical next-token predictions were separable only with layers concatenated; the abstract says belief states "contain information about the entire future, beyond the local next-token prediction". The proposal's "Not done" paragraph omits this.
- **The published tables nearly determine the day-1 figure.** The repo's probe uses all layers concatenated (320 features). For the large RoPE model, total R^2 is 0.97 and the least-variance rung holds 17% of the variance, so every rung has R^2 of at least about 0.82: "Full" wins there before any work is done. For the small models, the next-token direction is at 0.97 and the total at 0.64-0.72, so the other three rungs average about 0.55-0.63. The split only adds how that deficit is distributed over h = 2, 3, 4.

What remains new: per-layer and per-horizon residual curves, the capacity dependence of "leakage", the reconciliation with the nonergodic 0.985, and a quantitative causal test. That is enough for a post only if the weak parts below are fixed.

## 3. Pre-mortem

Day 1 will work. The code is self-contained, has tests, and the checkpoints load with `weights_only=True`. The team gets the MRRXOR horizon figure by midday, and it shows what the arithmetic above predicts. The problems come later.

1. **The cache-minus-residual gap is not informative.** The cache contains the token history at every layer, because embeddings persist through the residual connection. Excluding the first-layer cache therefore does not remove the trivial route. A readout of 8 learned queries plus a 128-unit tanh MLP will hit about 1.0 on everything, trained or not far from it. The linear variant is the only version with content, and its untrained floor may be high. Expect a flat line at the ceiling that readers shrug at.
2. **The causal check has a foregone result.** The gbs encoder replaces the whole 16-entry cache and the current-token vector. Of course that redirects far-horizon predictions, and of course a one-position residual patch does not, since later positions still attend to the real history. Kolchinsky says this in section 5. It also needs an encoder fit that the proposal treats as already released.
3. **The delay family is under-specified and probably degenerate.** Contexts are 32 tokens and sequences start from the stationary distribution. At D = 8 the period is 11, giving under three periods per context with noisy fillers. The Bayes predictor itself can barely synchronise, so the XOR direction has tiny variance and KL < 1e-3 is met by ignoring it. If the fillers are made phase-revealing instead, the model learns a fixed-offset attention lookup and the result is Fomin's, as expected.
4. **The KL threshold excludes the reused checkpoints.** The released small RoPE models have test KL of 1.9e-3 (eps = 0.05) and 1.6e-3 (eps = 0), above the proposal's 1e-3 cutoff; the small learned-position models sit at 8.9e-4. The small-versus-large R^2 contrast is confounded with a 10-20x difference in excess loss. The nonergodic post reports 1 - R^2 scaling as excess loss to the 0.6, so much of the "architecture effect" may be a training-quality effect.
5. **The eps = 0 checkpoints are close to useless for probing.** The README's shuffled-belief control scores 0.74-0.78 there (35 distinct beliefs, memorisable). The proposal lists eps = 0 as a reused condition without noting this.
6. **The MLP residual probe lacks a recent-token baseline.** Fomin's "group + last six symbols" baseline explains everything up to gap 6. A matched MLP probe on a residual stream that holds a window of recent tokens will read far-horizon beliefs without the model having computed them.
7. **Seed heterogeneity.** Fomin saw a bimodal split across seeds. Three seeds per cell cannot characterise a bimodal outcome, and the one-at-a-time regression will be noisy.
8. **Breadth.** Four processes, seven architecture factors, about 200 runs, 180 cache fits and a causal check is a lot for two days. The likely casualty is the two-Mess3 model, which has a different architecture (TransformerLens, gated MLP, RMS norm, context 128) and no public code or weights. Its Mess3 parameters are flagged as doubtful in NOTES.md.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: clean horizon/delay dose-response plus a capacity effect, reconciling the two posts | 30-35% |
| Clear negative that is still interesting: full belief stored even at long delay in adequately trained models | 10% |
| Ambiguous mush: "depends on model size, seed and training quality", cache readout at ceiling, causal check trivially as predicted | 45% |
| Fails to run | 10% |

The modal write-up is: "big models store the whole short-horizon belief, small or undertrained ones do not, long delays are recomputed from the cache as Fomin found". That is correct and tidy, and worth perhaps 30-45 karma.

## 4. Cost check

$120 is realistic and, if anything, high.

- The models have 20k-144k parameters with 32-token contexts. A 100k-step run is minutes on any GPU and is CPU-bound, so many can share one card. The RTX 4090's 6 vCPUs are the real bottleneck; a higher-vCPU instance or Community Cloud at $0.34/hr is the better buy.
- Cache fits use batch 64 on tiny models: minutes each.
- My estimate is $50-120 including reruns. The $500 cap is not a concern, and money is not the binding constraint: agent time and analysis discipline are.

## 5. Recommended changes

1. **Replace the learned cache readout as headline with a probe-free localisation measure.** For each position t and horizon h, restrict what later positions can use: for example, mask attention to positions before t - k, or resample the history before t - k while keeping the last k tokens. Measure excess KL against the Bayes predictor at horizon h. This gives "how many past positions the model needs for the horizon-h part of the belief" with no decoder-capacity argument. Keep the linear cache readout only as a secondary panel.
2. **Make the causal check diagnostic.** Compare three interventions for horizon-1 and far-horizon belief differences: (a) patch the probe subspace at position t in one layer; (b) patch position t's residual at all layers, which is its entire contribution to the future cache; (c) patch the last k positions, for k = 1, 2, 4, 8. The informative quantity is the k at which far-horizon predictions follow the patch. Drop the gbs encoder from stage 1, or correct the text to say it must be fitted.
3. **Cite and build on Fomin's note and the Shai et al. RRXOR layer-concatenation result.** State the delta explicitly: exact Bayesian belief targets, horizon subspaces, capacity sweep, causal localisation. Adopt his per-gap untrained twin and recent-token-window baseline for every probe, especially the MLP one.
4. **Fix the delay family before training anything.** Use a BOS-aligned phase, or lengthen the context to 96-128, and verify that the Bayes-optimal belief's XOR direction has substantial variance at every filler position. State in advance what distinguishes "stored" from "recomputed". Add a variant where recomputation is hard, such as a random delay or a running parity over many tokens as in Fomin's bit, since that is where storage is actually pressured.
5. **Deal with the training-quality confound head-on.** Train the small models longer or with more seeds until their excess loss matches the large ones, or report R^2 at matched KL using intermediate checkpoints. Without this, the architecture regression is uninterpretable. Either relax the 1e-3 threshold or acknowledge that the released small RoPE checkpoints fail it.
6. **Cut scope.** Drop eps = 0 (or keep it only with its shuffled control shown). Drop single Mess3, where the answer is known. Shrink the one-at-a-time sweep to depth and width, with 8-10 seeds per cell rather than 3, so bimodality across seeds is visible. Keep position embedding and init scale only as single contrasts. Treat two-Mess3 as optional and last.
7. **Put the predicted day-1 result in the proposal.** Include the bound implied by the README (large RoPE: every rung at least about 0.82; small: far rungs averaging about 0.55-0.63) and say what would be surprising: for example, the deficit sitting entirely in the h = 4 rung, or a per-layer profile where far rungs appear only in early layers.
8. **Reframe section 5 of the proposal.** The claim to aim for is a quantified rule, such as "the residual stream at position t linearly carries belief components up to horizon H(depth, width), and the rest is recomputed from the last k positions". "Residual versus cache" is partly a definitional contrast, since the cache is just earlier residuals.
