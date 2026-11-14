# Is it the partition or the picking? Null dictionaries for Exemplar Partitioning on AxBench
cluster: feature-discovery | stage-1 cost: $150 | follows up: An Introduction to Exemplar Partitioning for Mechanistic Interpretability (RroeHBSkBXXDsrryq)

## 1. What the prior work showed
Exemplar Partitioning (EP; Rumbelow, arXiv 2605.14347) builds a feature dictionary with no training: stream
centred, unit-normalised activations once, and let each activation either join the nearest stored "exemplar"
(if within a cosine threshold set by a percentile p of pairwise distances) or become a new exemplar. Each
region keeps its exemplar and the mean of its members.

The headline evidence that regions are meaningful is AxBench latent concept detection (Wu et al., arXiv
2501.17148) on Gemma-2-2B-it layer 20: 500 concepts, each with 72 positive and 72 negative training texts and
a held-out test set. EP is scored with AxBench's "SAE-A" rule: for each concept, compute every dictionary
element's AUROC on the training texts (max over tokens of cosine to the element) and keep the best one; report
its test AUROC. The post reported 0.881; the paper's v3 (Sep 2026) reports **0.937** at p1 (K = 5,796 regions,
region-mean readout), against SAE-A 0.911 (16,384 Gemma Scope latents), the canonical paired SAE feature
0.755, supervised DiffMean/Probe 0.946, and a bag-of-words classifier 0.931. With exemplars instead of means,
the same dictionary scores 0.832; the repo README attributes this to a "spiky" readout that lets "one generic
region win the training-set selection for many concepts".

v3 already added Llama-3.1-8B, refusal interventions, Taboo secret-word organisms, SAEBench probing and seed
stability. It does not contain (checked in the v3 text and README): any null dictionary scored under the same
selection rule (random activations, k-means centroids, random directions); any K-matched comparison; or any
AxBench **steering** numbers, although the repo ships a steering mode. The top comment on the post notes that
selecting the best region "only shows the existence of a good region"; the author replied that good tests
should be causal and hers are "by no means conclusive yet". I found no third-party follow-up (web search was
unavailable; arXiv API and LessWrong were checked directly).

## 2. Question and why it matters
**How much of EP's AxBench result comes from the partition, and how much from picking the best of several
thousand directions that happen to be real activations?** An exemplar set is close to a greedy
minimum-separation sample of the activation cloud; a region mean is a local average. If K random centred
activations, or K local averages around random activations, or K k-means centroids reach roughly 0.93 under
the same rule, then "EP beats SAEs" is a statement about the benchmark and the selection rule, not the method,
and AxBench detection cannot rank unsupervised dictionaries (BoW at 0.931 already hints at this). If EP's
calibrated cover beats those nulls at matched K, that is the first evidence the construction itself matters,
The second half asks the causal version: do EP region means steer better than SAE latents and DiffMean on
AxBench steering, where EP has no number at all? AxBench found detection and steering dissociate (SAE-A
detects better but steers worse than the paired SAE), so this is not predictable from 0.937.

## 3. Stage 1 plan
Reused: EP code with its AxBench adapter (`https://github.com/jessicarumbelow/exemplar-partitioning`),
prebuilt dictionaries (`https://huggingface.co/datasets/J-RUM/exemplar-partitioning`,
gemma-2-2b-it L20 at p = 1, 2, 4, 8, 10), AxBench code (`https://github.com/stanfordnlp/axbench`) and data
(`https://huggingface.co/datasets/pyvene/axbench-concept500`, `2b/l20`), Gemma Scope SAEs
(`google/gemma-scope-2b-pt-res`, `layer_20/width_16k` and `width_65k`), ungated weights
`unsloth/gemma-2-2b-it`. Built: the null dictionaries and a thin scoring harness around the cached activations.

1. **Reproduce.** Run the released p1 dictionary through the repo's AxBench path; require 0.937 +/- 0.005
   (mean) and 0.832 (exemplar). Re-score SAE-A from the 16k SAE in the same harness (target 0.911).
2. **Build nulls from the same stream.** Cache about 4M Pile activations at L20 (EP's p1 build used 3.6M).
   From them construct, at K = 5,796 and with the same centring: (a) random Gaussian unit directions;
   (b) covariance-matched random directions; (c) K uniformly sampled single activations; (d) local means: the
   average of each sampled activation's m nearest neighbours, with m matched to EP's region-size
   distribution; (e) spherical k-means centroids; (f) rows of the unembedding matrix for the K most frequent
   tokens; (g) EP exemplars; (h) EP region means; (i) EP rebuilt with a shuffled stream (3 seeds) to give the
   method's own noise floor. Each null gets 3 seeds.
3. **Score all under identical readout and selection** (max-over-token centred cosine; best training AUROC;
   test AUROC on AxBench's shipped held-out set). For SAEs score both native latent activations and decoder
   directions under the cosine readout, at 16k and 65k.
4. **K curves.** For every family, subsample K in {100, 300, 1k, 3k, 5.8k, 16k} (EP via its p ladder; nulls
   directly) and plot test AUROC against K, plus the train-minus-test gap. This separates "more candidates"
   from "better candidates" and removes the 5.8k-vs-16k confound.
5. **Beyond the mean.** Per-concept paired differences with bootstrap CIs over the 500 concepts; breakdown by
   whether BoW already solves the concept (lexical concepts are where any real-activation direction should
   work); number of distinct winners (the "generic region" effect); AUROC on the hard-negative subset.
6. **Steering.** For a fixed random subset of 100 concepts, take each family's selected direction (EP mean,
   EP exemplar, random-activation null, local-mean null, k-means, SAE-A decoder, paired SAE decoder, DiffMean
   from the training set) and run AxBench's steering protocol unchanged: 10 Alpaca-Eval instructions, the
   benchmark's steering-factor grid, factor chosen on 5 instructions and scored on the other 5, gpt-4o-mini
   judge. Sanity anchor: DiffMean near 0.178 and SAE near 0.151 as published.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14 (runpod.io/pricing, openrouter.ai/api/v1/models).
- GPU: one RunPod A40 48 GB at $0.59/h. Activation caching, k-means, nearest-neighbour means and scoring
  about 12 h; steering generation (100 concepts x 8 families x 10 instructions x ~8 factors = 64k generations
  of ~128 tokens on a 2B model) about 6 h; debugging and reruns 2.5x. About 45 h -> **$27**; budget **$45**.
- Judge: 64k generations x 3 judge calls x ~500 input / 60 output tokens on gpt-4o-mini ($0.15 / $0.60 per
  M) = 96M in ($14.40) + 11.5M out ($6.90) = **$21**; with one full rerun **$45**.
- Storage for dictionaries and a ~35 GB activation cache: **$10**. Contingency: **$50**.
Total **$150**.

## 5. What success looks like
The post's main figure: test AUROC against K for each family, EP, SAE and nulls on the same axes, plus a
steering bar chart. Clear outcomes:
- *Deflationary:* random activations or local means land within about 0.01 of EP means at matched K, and the
  K curve explains most of the EP-vs-SAE-A gap. Headline: "a few thousand random activations match Exemplar
  Partitioning and beat SAE-A on AxBench detection".
- *Vindicating:* EP means beat every null by more than seed noise at matched K, especially on hard negatives
  and on concepts BoW does not solve.
- *Steering:* EP means either clear the SAE (0.151) and DiffMean (0.178) scores or do not; either is the
  first causal number for EP on a standard benchmark.
A mixed result (EP > single activations but = k-means) says averaging, not the exemplar construction, is
what matters. No outcome is uninformative provided step 1 reproduces.

## 6. Stage 2 (if stage 1 succeeds)
About $300-400: repeat at L10 and on Gemma-2-9B (AxBench `9b/l20`, `9b/l31`); add other distance metrics
(Euclidean, Mahalanobis) as dictionary families; rerun the paper's Taboo and harmful/benign results with the
best null in place of EP, to see which need the partition.

## 7. Risks and how the plan handles them
- *Headline does not reproduce:* the released dictionary and exact CLI command are run first; if off by more
  than 0.005, stop and report, having spent under $10.
- *Unfair nulls:* every family uses EP's own centre, readout, selection rule and K; local-mean neighbourhood
  sizes are matched to EP's region sizes; results are shown for both single-point and averaged variants.
- *Under-elicited SAE baseline:* scored with native activations and with decoder cosine, at two widths.
- *Steering noise* (100 concepts x 5 held-out instructions): paired per-concept comparisons, bootstrap CIs,
  published DiffMean/SAE scores as anchors, 200 judge outputs read by an agent.
- *Gated weights:* official `google/gemma-2-2b-it` needs approval; the ungated `unsloth` mirror is validated
  by step 1.
- *Over-claiming:* conclusions are limited to this benchmark and layer until stage 2.
