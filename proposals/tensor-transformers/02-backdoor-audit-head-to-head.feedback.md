# Feedback: "Does a tensor transformer make a weights-only backdoor audit easier? A blind head-to-head against standard models"

Verdict: **major overhaul**. The question is a good one and nobody appears to have answered it, but as designed
the benchmark will sit at ceiling for cheap generic methods on both architectures, the "architecture
head-to-head" is confounded, and several "reused code" claims do not match the repos.

What I checked (2026-11-14). Read directly: both cluster posts and the tensor-similarity post via
`get_post.py`; arXiv 2605.15183 abstract; `loganriggs/tensor_language` (`README.md`, `model.py`, `deep_model.py`,
`lm_train.py`, `text_data.py`, `jacclust/SUMMARY.md`) and `tdooms/tensor-similarity` (`README.md`,
`pyproject.toml`, `src/models/transformer.py`, `src/models/checkpoint_transformer.py`,
`src/components/similarity.py`, `src/figures/language_similarity/prepare.py`) via raw.githubusercontent.com;
Hugging Face API status codes; the RunPod pricing page; LessWrong GraphQL for karma and comment counts; arXiv
API keyword queries. **Not done: general web search.** The WebSearch budget was exhausted for me as well as
for the proposer, so the novelty check still rests on arXiv queries and the author's posts and repos only.

## 1. Would it get upvoted?

Borderline; I put P(>50 karma) at roughly 25-30% for the design as written, perhaps 45% for the overhauled
version below with a clean result.

- Reception of the source material is modest and falling: 87 karma (performance post, Jan 2026), 45 (tensor
  similarity, May 2026), 54 (the "you should use a tensor transformer" post, Sep 2026, with **0 comments**,
  verified via GraphQL). The audience that cares is small: Riggs/Dooms and collaborators, plus weight-based
  interp people.
- "Tensor wins on conjunction triggers that search cannot find" would be the first measured payoff for the
  architecture and would be amplified by the author. That is the only outcome I am confident clears 50.
- "Generic search matches the algebra on a d=256, small-vocabulary toy" is the most likely clean outcome and
  will be read as unsurprising: of course exhaustive scan finds a one- or two-token trigger when the vocabulary
  is a few thousand tokens. The author's own post already concedes he cannot interpret these models, so a toy
  null does not move anyone.
- A blind red/blue protocol is a real credibility asset on LessWrong; keep it.

## 2. Naturalness

Mainline in spirit. The tensor-similarity post ends with "we still don't know what the difference is. We're
excited about any future work that explores that angle, especially if you're analyzing the weights" (verified
in the post text). Recovering the trigger and target of a planted backdoor from weights is exactly that
request. The cross-architecture race bolted on top is less natural and is where most of the design problems
come from.

Already done? I found nothing. arXiv queries for bilinear + backdoor, bilinear + trojan, "tensor network" +
backdoor, and "tensor similarity" + interpretability return only 2605.15183 itself. The claims about that paper
check out (SVHN backdoor, class-9 slice described by the authors as "cheating", 2-layer attention-only language
experiment unexplored). Caveat as above: no general web search.

Relevant prior work the proposal does not cite and must position against:
- arXiv 2508.00161, "Watch the Weights" (verified abstract): top singular vectors of the fine-tune weight
  difference correspond to newly acquired behaviours, used to catch backdoors on standard LLMs with no
  poisoned data. This is G1 already published on real models; the proposal presents G1 as its own baseline.
- arXiv 2510.13900, "Narrow Finetuning Leaves Clearly Readable Traces in Activation Differences" (title
  verified; content from memory): activation differences between base and fine-tune on unrelated text reveal
  the fine-tuning objective. So G3 is not an "expected floor"; with base-model access it may be the strongest
  generic method.
- The trojan-detection literature (trigger inversion by gradient search, e.g. the Trojan Detection Challenge
  LLM track, GCG/PEZ-style optimisers; from memory, not re-verified). Gradient-guided inversion is the
  standard strong baseline and is absent from G1-G3.

## 3. Pre-mortem

Forecast: clear positive 12%; clear negative that is still interesting 23%; ambiguous mush 45%; fails to run
(T1 never works beyond one layer, or the tensor models do not train as specified) 20%.

How I expect it to play out, most important first.

1. **The benchmark is at ceiling for trivial methods, on both architectures.**
   - A rare trigger token gets almost no gradient on clean data, so its embedding row is the row that moves
     most in the poisoned fine-tune. Ranking tokens by embedding-row difference norm (and targets by
     unembedding-row difference norm) probably gives recall@10 near 100% for single-token, distributed and
     conjunction triggers alike, on standard and tensor models. This baseline is not in the plan.
   - Exhaustive single-token scan is trivial at this size. For pairs, a 1,024-token vocabulary (what the repo's
     TinyStories pipeline uses) has about 1M ordered pairs and a 5,120-token one about 26M; a 4-layer d=256
     model on short contexts gets through that exhaustively inside the 10-minute budget. G2 does not need its
     beam.
   - So the likely table is "everything about 100% except whatever T1 fails at". The planned remedy, tuning
     trigger rarity, poison rate and depth "until at least one method scores between 20% and 80%", is tuning
     the benchmark to the methods. None of those knobs makes exhaustive search harder, and the choice will
     look post hoc.
2. **Comparison (a) does not isolate architecture.** G1-G3 run on tensor models too, so "best method on tensor
   vs best on standard" will be G2 or embedding-diff against itself, about equal. Any residual gap reflects how
   differently the two architectures store the backdoor and how much effort went into each method, with one
   base model per architecture-depth cell. That is n=1 per cell at the level that matters; bootstrapping over
   15 fine-tunes of the same base does not fix it.
3. **Detection AUROC is ill-posed.** One benign control is "an innocuous new bigram rule", which is
   mechanically a single-token backdoor (token X present, then emit Y). No weights-only method can or should
   separate them, so AUROC measures the red team's labelling convention. The other control (clean-data steps)
   is separable by weight-difference norm alone.
4. **T1 is the whole contribution and is mostly unbuilt.**
   - The released tensor-similarity code gives a scalar similarity under Gaussian inputs, analysed at
     `n_ctx=4` by default because the covariance tensor is quadratic in `n_ctx` and "contraction cost is
     super-quadratic" (`checkpoint_transformer.py`). The 3.5 s per pair figure is for a 2-layer
     attention-only model at that setting. It does not localise or name anything.
   - The localisation recipe (path contraction of a weight difference, eigendecomposition per output slice,
     reading eigenvectors through the embedding) is new for language models with attention. In 2410.08417 the
     token-level reading was done for MLP paths; attention-then-MLP paths at 4 blocks multiply quickly.
   - The author's own `jacclust/SUMMARY.md` (57 experiments) reports "NO demonstrated real-model CAUSAL win"
     and a table of retracted headlines. That is the base rate for weights-only readouts on these models
     working first time.
   - Expect T1 to work on embed -> MLP -> unembed and embed -> OV -> unembed in the 2-block model and to be
     unfinished for 4 blocks when methods are frozen.
5. **The algebra has a generic analogue that is missing from the baselines.** In a polynomial model the
   pairwise interaction matrix T1 extracts is essentially the input-embedding Hessian of the target logit
   difference. That Hessian (or gradient x input, or GCG-style inversion) can be computed by autodiff on the
   standard model as well. Without it, a T1 win over SVD and blind search does not show the architecture
   mattered; with it, the likely finding is "the Hessian trick works on both".
6. **Reuse claims are partly wrong** (verified against the repos):
   - `lm_train.py` hard-codes `NORM = "rms"`, `D_MODEL = 128`, and its docstring says "attention-only models
     (RMSNorm on, lerp residual)". "Norm off as in that repo" is only `DeepModel`'s constructor default, not
     the recipe that was actually used to train language models. With RMSNorm on, the model is not a tensor
     network and the similarity code does not apply. Whether a norm-free 4-block (attention + bilinear MLP)
     model trains stably at d=256 is untested; the trainer has an explicit `DIVERGED` branch.
   - The data pipeline (`text_data.py`) supports OpenWebText (V=5120) and TinyStories (V=1024) only.
     SimpleStories is public (HF API 200) but is not wired in; tokeniser and data loader need writing.
   - `attention="softmax"` exists in `model.py` (verified), but there is no ReLU MLP class, and the softmax
     variant drops `q2`/`k2`, so parameter matching needs care.
   - `tdooms/tensor-similarity` requires Python >= 3.13, torch >= 2.10, quimb, cotengra and kahypar, and its
     `Transformer` class (attention + MLP layers; this does exist, which is good news) is a different class
     from `tensor_language`'s `DeepModel` with a different residual convention (lerp vs additive is handled
     by a subclass for one specific checkpoint). A weight-conversion shim with a numerical equivalence test
     is required. `melephant/2l-bilinear-attn-normalised-v2` returns 401 anonymously; the plan does not need
     it, but the repo's only language example cannot be run as a smoke test.
   - All of this is doable, but it is a day of glue on a two-day clock before any method development starts.
7. **Scope.** Four base models (six with loss-matched extras), 280 fine-tunes, four method families, two
   independent blue-team developers, a freeze, and a blind run is too many stages for two days. Under time
   pressure the stage that slips is baseline quality, which is the stage the conclusion depends on.

## 4. Cost check

Prices verified on the RunPod pricing page today: RTX 4090 community $0.34/h, RTX 5090 community $0.69/h.
Dollars are not the constraint. The models are tiny; 132 GPU-h is probably an overestimate for training and
an underestimate only if tensor-similarity contraction at 4 blocks with MLPs is far slower than the 2-layer
attention-only figure. My estimate is $100-250, and I would budget $250 to allow for a larger-vocabulary
variant and three base seeds. API spend is negligible. The scarce resource is agent wall-clock.

## 5. Recommended changes (most important first)

1. **Change the headline question** from "which architecture is easier to audit" to "can a backdoor's trigger
   and target be read out of a tensor transformer's weights, and does that beat search and gradient methods
   where those run out". Keep one matched softmax/ReLU model as a secondary control for the generic methods,
   not as half the design.
2. **Build the benchmark so the cheap methods are not at ceiling by construction, and fix this before any
   method is run.**
   - Freeze embedding and unembedding during the poisoned fine-tune, or use triggers made of common tokens,
     and report the embedding-row-norm baseline explicitly either way.
   - Use the V=5120 OpenWebText pipeline that already exists in the repo rather than a new SimpleStories one.
   - Make the hard class a conjunction of 3 tokens with no partial effect: about 1.3e11 ordered triples is out
     of reach of exhaustive scan, and a strict AND gives beam search nothing to climb. Verify the "no partial
     effect" property empirically for each fine-tune and report leakage, since leakage is what search exploits.
   - State in advance that singles and pairs are sanity tiers where every method is expected to score near
     100%, and that the triple tier is the test.
3. **Add the missing baselines**: embedding/unembedding row-difference norm; activation-difference lens on
   clean text (2510.13900 style); gradient-guided trigger inversion (GCG-style) on both architectures;
   input-embedding Hessian of the changed logits on the standard model as the autodiff analogue of T1. Cite
   2508.00161 for G1.
4. **Drop detection AUROC**, or keep it only against clean-continuation controls and call it a sanity check.
   Remove the "innocuous bigram rule" control or relabel it as a backdoor.
5. **Day-1 gate, with a stated fallback.** By hour 12: (i) a norm-free 2-block tensor model reaches a sensible
   loss; (ii) a hand-planted pair backdoor reaches >90% attack success; (iii) T1's single-path readout
   recovers that known trigger and target; (iv) converted weights reproduce the model's outputs in the
   tensor-similarity code. If (i) fails, fall back to attention-only or 1-block models. If (iii) fails, stop
   and write up the negative result with the baselines rather than proceeding to a blind run with no T1.
6. **Cut scope.** Drop the 4-layer models to a stretch goal. Use 3 base seeds for the tensor model and 2-3 for
   the standard control, about 10 fine-tunes per class per seed, and analyse with base seed as the unit
   (or a mixed model). Around 120 fine-tunes in total is enough.
7. **Correct section 1 and 3 of the proposal**: `lm_train.py` trains with RMSNorm on at d=128; SimpleStories is
   not supported by the repo; no ReLU MLP exists there; tensor-similarity is analysed at `n_ctx=4` and returns
   a scalar. State what has to be written.
8. **Re-run the novelty check with general web search** before funding (neither the proposer nor I had it),
   specifically for trojan/backdoor work on bilinear or polynomial networks and for follow-ups from the
   Dooms/Riggs group since September 2026.
9. If only one proposal from this cluster is funded, the proposer's own ordering (01 first) is right: 01 has a
   simpler pipeline and does not depend on a new method working. Fund 02 only in the overhauled, narrower form.
