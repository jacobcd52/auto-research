# Feedback: "Is it the partition or the picking? Null dictionaries for Exemplar Partitioning on AxBench"

Verdict: **keep with tweaks.** The gap is real and the assets are public, but the most likely result ("k-means
matches EP") is less newsworthy than the proposal assumes, the steering half is under-specified and probably
uninformative as designed, and the proposal never actually tests the *partition*.

## What I checked

Confirmed by direct fetch:
- arXiv 2605.14347 is at v3 (17 Sep 2026). Table 1 gives EP p1 K=5,796, region mean 0.937, exemplar 0.832; SAE-A
  0.911 (16,384); SAE 0.755; DiffMean/Probe 0.946; BoW 0.931; Prompt 0.921. The paper itself flags the K and
  build-corpus mismatch with SAE-A.
- v3 text contains no k-means, random-activation or random-direction candidate set on AxBench, and no AxBench
  steering number. Its k-means, matched-K and random-direction controls are all in the refusal experiments.
- The "spiky ... one generic region" sentence is in the repo README, and the README documents
  `--axbench-modes latent,steering,steering_test` and `--axbench-act-cache-dir`.
- LessWrong comments: Riya Tyagi's selection concern (7 karma) and the author's "good tests are typically
  causal ... by no means conclusive yet" reply are as quoted.
- Hugging Face: `J-RUM/exemplar-partitioning` has gemma-2-2b-it L20 at p = 1, 2, 4, 8, 10 (p1 pickle 1.77 GB);
  `pyvene/axbench-concept500` has `2b/l20/{train,test}/data.parquet`; `google/gemma-scope-2b-pt-res` is ungated
  with `layer_20/width_16k` and `width_65k`; `unsloth/gemma-2-2b-it` is public.
- OpenRouter lists gpt-4o-mini at $0.15 / $0.60 per M tokens.

Not checked: the RunPod A40 price. Even at double the quoted rate the GPU line stays under $60.

Prior-work search: the web search tool was unavailable for me too (shared budget exhausted), so the check is
again limited. The arXiv API returns only the EP paper for "exemplar partitioning" and nothing for AxBench with
k-means or clustering baselines. A scan of the 400 most recent LessWrong posts with 10+ karma found no EP
follow-up. An independent follow-up cannot be ruled out, and the author said she would keep extending the work,
so a v4 with these controls is a live scooping risk.

Errors and omissions in the proposal:
1. **AxBench's steering grid has 14 factors, not about 8** (`steering_factors: [0.2 ... 5.0]` in the repo's
   `2b/l20/no_grad.yaml`). Generations and judge calls are 1.75x the estimate.
2. **The released p2/p4/p8 dictionaries are not the ones in the paper's table.** The dataset card gives
   K = 1,882 / 738 / 252; the paper gives 2,037 / 686 / 226. Only p1 matches (5,796). "EP via its p ladder"
   will not reproduce the paper's lower rows from the released files.
3. **The p0.5 row is omitted, and it matters.** The paper reports K=18,674 with mean 0.930 and exemplar 0.914.
   EP's region-mean curve is therefore non-monotone in K (0.889, 0.919, 0.915, 0.937, 0.930), and the exemplar
   readout jumps from 0.832 to 0.914 between p1 and p0.5. Build-to-build wobble looks like 0.01 or more for
   means and far more for exemplars. The proposal's "within about 0.01" criterion is at the noise scale.
4. The 16k point on the EP curve needs the p0.5 build, which is not released (about 12M tokens to rebuild).
   This is feasible but is not in the plan or the budget.
5. The dataset card says the pickles need a `cas` package, while the repo's package is `ep`. Unpickling may
   need `Dictionary.from_hub` or a module alias. Minor, but it lands in hour one.

## 1. Would it get upvoted?

Borderline: I put it at roughly 35-45% to clear 50 karma as written, and 50-60% with the changes below.

- The cluster's posts earned 51-96. The EP post earned 70 for a new method from a known author. A third-party
  controls post on one benchmark table of that paper will usually earn less than the original.
- The closest recent comparator, "Sanity Checks for Sanity Checks for Sparse Autoencoders" (Oct 2026), sits at
  27 karma. Readers have also already seen "random baselines match SAEs" (Korznikov et al., arXiv 2602.14111),
  so "a null baseline matches method X" has lost some novelty.
- The audience is interpretability people deciding whether EP is worth adopting, plus the author and the
  commenter who raised the concern. That is a real but narrow audience.
- The headline that would travel is about the benchmark and the SAE comparison, not about EP: "the SAE-A gap
  disappears when you match readout and K" or "AxBench detection cannot rank unsupervised dictionaries". The
  proposal has the ingredients for that but buries them as a robustness arm in step 3.
- "k-means centroids match leader-clustering centroids" alone will draw a shrug. Nobody, including the author,
  claims leader clustering is a better clusterer than k-means; her pitch is cost, one hyperparameter, and
  cross-model comparability.

## 2. Naturalness

Mainline. The top critical comment asks for it, the paper acknowledges the K and corpus confounds, and steering
is on the author's own future-work list. I found no evidence it has been done.

Two caveats:
- **The title question is not what the experiment tests.** Every arm scores a set of *directions* by max-pooled
  cosine. The partition (which token is assigned to which region) is never used. The commenter's actual ask was
  about regions as subspaces and true/false positive rates at the native threshold. The honest question as
  designed is "do EP's representatives beat other cheap direction sets?".
- **"Picking" is slightly mis-framed.** Test AUROC is held out, so selection does not inflate the number. The
  issue is how rich the candidate set is. The random-direction arms and the train-minus-test gap do address
  this; the write-up should say so rather than imply overfitting.

## 3. Pre-mortem

My forecast of the detection ladder at K of about 5.8k:
- Gaussian and covariance-matched random directions: about 0.55-0.75, clearly bad.
- Single random activations: about 0.83-0.90, the same as EP exemplars, since an exemplar is a single activation.
- Local kNN means and spherical k-means centroids: 0.92-0.94, statistically indistinguishable from EP means.
- SAE decoder directions under the cosine readout: unknown, and the most informative arm.

Outcome probabilities:

| Outcome | Probability |
|---|---|
| Clear positive (EP means beat every null beyond seed noise at matched K) | 10% |
| Clear negative that is still interesting (averaged nulls match EP, and the SAE-A gap is explained by readout or K) | 40% |
| Ambiguous mush (differences of 0.005-0.015 inside build noise; steering all near the floor) | 40% |
| Fails to run or reproduce | 10% |

Specific failure modes:
1. **Noise floor swamps the effect.** See omission 3. With 500 concepts the paired bootstrap over concepts is
   tight, but the relevant variance is across *builds* (stream order, calibration sample). Three shuffled
   rebuilds is the minimum, and they cost real time at p1. If EP's own seed spread is 0.01, "EP vs k-means"
   cannot be resolved and the post has to say so.
2. **The unsurprising result.** The ladder above is roughly what anyone would predict. The post's value then
   rests on the SAE arm and the lexical/BoW breakdown, which get the least design attention.
3. **Steering scale is undefined.** EP and null directions are unit vectors in centred space. AxBench's factor
   grid assumes each method's own scale convention (SAE factors are multiplied by the latent's max activation;
   DiffMean is unnormalised). Unit vectors times 0.2-5 against residual norms in the hundreds do nothing. The
   proposal says "run the protocol unchanged", which will either produce zeros for the new families or force an
   ad hoc scale chosen mid-run. This is the main under-elicitation risk, and the choice can manufacture either
   conclusion.
4. **Steering has little dynamic range.** Published scores are 0.178 (DiffMean) and 0.151 (SAE) on a 0-2 scale,
   against 0.731 for prompting. With 100 concepts and 5 held-out instructions, a 0.03 difference among eight
   families will not separate. The likely finding is "everything, including nulls, steers badly", which gives a
   dull second half.
5. **Reproduction friction.** TransformerLens loading under the gated model name, weight-processing defaults,
   BOS and chat-template token handling in the max-pool, and the pickle module name each can cost hours.
   "Stop if off by more than 0.005" is right but may trigger on a preprocessing mismatch, not a real failure.
   Allow half a day for this.
6. **AxBench steering pipeline fragility.** It depends on pyvene, the OpenAI client and its own config sweep.
   Pointing it at OpenRouter and adding custom direction families is where a two-day agent run is most likely
   to stall. The EP repo's own steering mode may be easier, but it is unverified against the published anchors.
7. **Local-mean null is under-defined.** "m matched to EP's region-size distribution" is ambiguous: EP region
   sizes are heavy-tailed, and a mean over a cosine ball differs from a mean over m nearest neighbours. This
   arm is the one that separates "averaging" from "the EP construction", so it needs a precise definition.
8. **Scooping.** A v4 with k-means controls on AxBench would erase most of the value.

## 4. Cost check

The estimate is realistic and slightly low. My estimate is **$150-220**.

- Steering judge with 14 factors: 100 x 8 x 10 x 14 = 112k generations, 336k judge calls, roughly 170M input
  and 20M output tokens, so about $37 per pass against the proposal's $21. With one rerun, about $75.
- GPU: add the p0.5 rebuild and three p1 shuffled rebuilds (each a streaming pass with nearest-exemplar search
  against thousands of exemplars) plus k-means at 16k. 50-70 A40 hours, about $30-45.
- Cutting steering to four families, as recommended below, returns the total to about $130.

Either way the project is far below the $500 cap; cost is not the constraint.

## 5. Recommended changes (most important first)

1. **Make the SAE comparison a headline arm.** The claim readers remember is "EP beats SAE-A, 0.937 vs 0.911".
   Decompose that gap into (a) readout: SAE decoder and encoder directions under the same centred-cosine
   max-pool, against native JumpReLU activations; (b) K: 16k and 65k SAEs subsampled to 5.8k, and EP or k-means
   at 16k; (c) corpus and model: the SAE was trained on the base model's activations, EP on the IT model's
   Pile activations, so add a k-means dictionary built on base-model activations. If SAE decoder cosines reach
   about 0.93, the headline is "EP's win over SAE-A is the readout", which is a stronger post than the null
   ladder.
2. **Test the partition, or retitle.** Add the native readout: for EP and for k-means at matched K, score a
   text by whether any token is *assigned* to the selected region (and by fraction of tokens assigned), and
   report TPR/TNR at the native threshold. This is cheap on cached activations, answers the commenter's actual
   question, and is the only arm where EP's calibrated threshold could plausibly matter.
3. **Establish the noise floor before interpreting anything.** Do the shuffled-stream p1 rebuilds first, at
   least three and preferably five, and pre-register that differences inside EP's own seed spread are reported
   as "indistinguishable". State how the non-monotone K curve and the 0.832 vs 0.914 exemplar jump are handled.
   Rebuild p2/p4/p8 with the paper's settings or say plainly that the released files differ from the table.
4. **Fix the steering scale rule in advance, and shrink the steering arm.** Use one pre-specified convention
   for all direction families (for example unit direction times factor times the median residual norm at L20,
   with a grid checked on DiffMean first), and reproduce DiffMean near 0.178 and SAE near 0.151 before running
   anything new. Cut to four families (EP mean, k-means centroid, DiffMean, paired SAE) and spend the saving on
   200+ concepts for power. Present steering as a secondary result and expect a floor effect.
5. **Define the local-mean null exactly**, and include both variants: m nearest neighbours with m sampled from
   EP's empirical region sizes, and all points within EP's threshold of a randomly chosen centre. The second
   is "EP without the greedy cover" and is the cleanest test of whether the cover matters.
6. **Put the lexical breakdown in the main figure.** Split concepts by BoW AUROC and show every family on each
   split. If all real-activation dictionaries tie on lexical concepts and separate only on the rest, that is
   the informative picture; if they tie everywhere, the benchmark-validity claim is solid.
7. **Correct the factual slips**: 14 steering factors; the p0.5 row; released versus paper K values; the
   judge cost.
8. **Send the result to the author before posting** and note in the write-up whether a later paper version
   has added these controls. Re-run the prior-work search with a working web search before committing funds.

If only one of the cluster's two proposals is funded, this one is the safer choice: it will produce a clean
figure with near certainty. Its ceiling is limited unless change 1 or 2 turns up something non-obvious.
