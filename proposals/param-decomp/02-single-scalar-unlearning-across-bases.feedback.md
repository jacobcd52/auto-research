# Feedback: One-number unlearning beyond German (param-decomp / 02)

Reviewer verdict: **keep with tweaks** (the tweaks are substantial: change the search method, the targets, the
primary metric and the baseline set). Cost is fine. The main risk is ambiguous output, not money or infrastructure.

## What I verified

- **Prior-work claims: accurate.** I re-read the post (ieoWstubDQWLrMnhH, 58 karma, 6 comments). Confirmed: top-16
  by CI(German) - CI(English); single `h.3.attn.v_proj:513`; inverting solution reaches 10.83 nats with < 0.1 nats
  English damage from ~4 German tokens vs ~32 for rank-1 and rank-4 LoRA; French/Spanish spared, Italian damaged;
  localised rank-1 LoRA on the layer-3 V matrix still damages fr/es/it; 9 seeds, budgets 2-2048, lr tuned per
  (method, budget), plateau at 300-1700 steps; fine-tuning code not public. The StefanHex / Lucius exchange is as
  described (Stefan asks about an SAE; Lucius says SAE directions do not live in weight space and suggests a steering
  vector as the nearest analogue; Stefan calls the result "German-abliteration").
- **One detail the proposal understates.** `:513` was rank **6** of 16 by the CI-difference score and was picked
  because its autointerp label was the only one mentioning German alone. Ranks 1-5 were generic "non-English text"
  units. So the published automatic recipe does not find the published unit. This matters a lot for the "top-1"
  arm (see pre-mortem).
- **Artefacts: public.** Anonymous range requests returned HTTP 206 for all three W&B files (target model
  267,727,904 bytes; both decompositions 2,908,595,703 bytes) and `model_config.yaml` (LlamaSimpleMLP, 4 layers,
  d=768, 6 heads, n_intermediate 3072, vocab 50277). `param_decomp/editing/_editing.py` exists at tag `vpd-paper`
  (28.8 KB; has `EditableModel.from_wandb`, `get_ci`, `make_edit_fn`, `without_components`, `measure_kl`).
  `angsten/vpd-audit` README confirms the pin to commit 74146b5, A100 40 GB, about 8 s per pass over 1,024 texts,
  ~$40 total. All three HF datasets are public and ungated. arXiv 2610.20748 and 2607.13047 exist with the stated
  titles.
- **Caveat on the editing module.** Its search/inspect helpers import `HarvestRepo` / `InterpRepo`, which need
  harvest databases that are not public. Only the loader, CI and edit functions are usable. Also its docstring
  example refers to a different run (`s-892f140b`), so do not assume that component index 513 in the released
  `s-55ea3f9b` is the post's component until the gate confirms it.
- **Prices: correct.** RunPod A40 $0.59/h secure ($0.35 community), A100 PCIe $2.09/h ($1.19 community);
  OpenRouter `anthropic/claude-haiku-5.5` $0.10 / $0.50 per M tokens.
- **Already done? Not that I can find, but the check is weak.** WebSearch was unavailable to me too (search budget
  exhausted), so this rests on five arXiv API queries (parameter decomposition + unlearning / fine-tuning /
  editing; nothing relevant beyond the papers already cited), the post's comment thread, and a title scan of LessWrong
  posts since 20 Oct. Note that the proposer's "pingbacks: none" evidence is invalid: the LessWrong `pingbacks` field
  lists posts a post links *to*, not posts linking to it (Angsten's September audit lists the February Drori post
  as a pingback). Nobody has checked inbound links. Goodfire has private fine-tuning code and an obvious interest in
  running this; a scoop from them is the main duplication risk and cannot be ruled out.

## 1. Would it get upvoted?

Probably 25-45 karma as written; over 50 only if the result is crisp and the framing is about the neuron-vs-learned-
basis argument, not about replication.

Reference points: the original post got 58 with a well-known author and a memorable headline. The two independent
audits of the same released decomposition by an outside author got 29 and 9. Leo Gao's "Neural networks are not
already clean" got 368, so the basis debate has an audience, but that audience cares about evidence on real
models, and this is a 67M model that its own author says "sucks at almost everything".

Who would care: the Goodfire PD team, Stefan Heimersheim (asked the question), Leo Gao and the "already clean"
readers. That is a small but high-karma-weight group. A post titled "A single MLP neuron unlearns German as cleanly as
a VPD subcomponent" or "The German result holds for 1 of 9 targets" would clear 50. "Subcomponents are somewhat
better on 5 of 8 targets depending on the selection variant" would not.

## 2. Naturalness

Mainline. "n = 1 target" is the first limitation the author lists, and the comparison with another basis is the top
comment. Extending targets and adding comparison bases is what a reader would do next. The no-adversary
decomposition as a basis is a good, cheap, on-agenda arm.

Two parts are less natural:
- **SVD directions as a headline baseline** are a strawman. Top singular directions of a weight matrix are dense and
  nobody expects them to be language-specific. Keep as a control, do not sell a win over them.
- **The missing baseline is the one the commenters actually named**: a constant steering vector / direction
  ablation ("abliteration"). A difference-of-means direction (target minus English) projected out of the residual
  stream writes, or equivalently a rank-1 projection applied to the weights, needs a handful of tokens, has zero or
  one trainable parameter, and is what most readers will ask about. Without it the post invites the top comment "but
  did you try abliteration?".

## 3. Pre-mortem

Forecast: clear positive 20%, clear and interesting negative 25%, ambiguous mush 40%, fails to run or stalls at
the gate 15%.

How it plays out. Day 1 morning: environment and loading work (Angsten's lockfile, anonymous download). Reproducing
German with `:513` takes most of day 1 because the harness is rebuilt from a prose protocol; it probably works,
since a sign flip of one known unit is hard to get wrong. Then the grid starts late on day 1 and the problems are
conceptual, not technical:

1. **Too few real targets.** The model's best non-English language is German and it is weak at that. The 1.5-nat
   filter will likely pass de, fr, es, it, maybe nl and pt; fi, pl, sv, da are doubtful. The Pile subsets are mostly
   *English* (ArXiv, PubMed, FreeLaw, USPTO, StackExchange, Enron). "Remove ArXiv, keep English with < 0.1 nats
   damage" is close to self-contradictory, and the retain evaluation (Pile validation) *contains* the target subsets,
   so the English-damage number is contaminated unless the target subset is excluded from it. Realistic clean
   targets: 5-6 languages, code, DM Mathematics. Four of the languages are Romance/Germanic neighbours and are not
   independent. A sign test on 6-8 correlated targets cannot support "significantly lower collateral".
2. **The success criterion is probably unreachable for most targets in every basis.** Driving a category to uniform
   CE with one rank-1 unit is an extreme event; the German unit was found by reading labels after the automatic top-16
   failed. If only 1-3 targets have such a unit in any basis, the pre-registered metric ("fewest tokens reaching 90%
   of the gap to chance") is undefined almost everywhere and the comparison collapses to a few anecdotes.
3. **Top-1 selection will fail by construction.** Target-minus-English scoring ranks generic "non-English" units
   first (ranks 1-5 in the post). So top-1 picks a unit that wrecks every language, in every basis, and the
   "fully automatic" arm shows nothing about the basis. The proposal's own "ambiguous" scenario is the modal one.
4. **Token efficiency does not discriminate between one-scalar bases.** Any one-parameter edit fits from a few
   tokens; the 4-vs-32 gap in the post is one parameter vs 55k. Half of the grid (4 budgets x 5 seeds x 3 learning
   rates) measures something that will be identical across the bases being compared.
5. **Neuron baseline is structurally handicapped.** The winning unit was in an attention value matrix. MLP neurons
   cannot express that edit. A reader on the neuron side will say the comparison omitted the natural attention
   units (per-head OV scale, rows/columns of the attention matrices in the residual or head basis).
6. **Best-of-20 selection criterion is unspecified.** If the winner is chosen on dev by target damage vs English
   damage only, collateral on other languages is a fair held-out test. If it is chosen by collateral, selection uses
   the other languages and the "spared without being asked" claim changes meaning. The proposal does not say which.
7. **Gradient training of one scalar is fragile for no reason.** Two basins (invert vs amplify), learning-rate
   sensitivity, plateau detection, a capped loss with zero gradient at the cap. All avoidable (see changes).
8. **Relearning arm will be uninformative.** Full-weight fine-tuning undoes a sign flip of one rank-1 unit almost
   immediately, and everyone expects that.
9. **Wall-clock.** 135 GPU-hours after a one-day gate means 6+ GPUs in parallel on day 2 with no slack for a
   harness bug found mid-grid. Likely result: a truncated grid, analysed in a hurry.

Infrastructure risk is low: tiny model, edited models are plain weights, artefacts verified. Evaluation-bug risk is
moderate (per-token CE with BOS excluded, parallel Europarl splits, dev/test leakage in best-of-k).

## 4. Cost check

The estimate is realistic and probably high. My estimate for the plan as written: $150-300 (45 s per run is
plausible for a 67M model at 300-1700 steps plus an 18-category evaluation; even at 3x slower it stays under $350 on
A40s). The 12 A100-hours at $2.09 are unnecessary; the audit ran on a 40 GB card and an A40 has 48 GB. With the
redesign below (sweeps instead of training) I estimate **$60-120** including margin, and the binding constraint
becomes wall-clock, not dollars.

## 5. Recommended changes (most important first)

1. **Replace per-unit gradient fine-tuning with a 1-D sweep of s.** With one scalar, evaluate s on a fixed grid
   (for example 31 values in [-3, 3], plus 0) and record target CE, English CE and every other category's CE. This
   gives the whole trade-off curve per unit with no learning rate, no seeds, no plateau rule and no basins, and
   costs seconds per unit. Spend the saving on breadth: screen the top 200-500 units per basis per target on
   (target, English) only, then run the full category evaluation on the Pareto set. Keep gradient training only for
   the gate (to match the post) and for the multi-parameter references (top-16, LoRA). Report "tokens needed to
   choose s" once, as a side note.
2. **Make the primary metric continuous and defined for every target.** For example: maximum target CE increase
   achievable with held-out English damage <= 0.1 nats, and collateral (mean CE increase on non-target, non-English
   categories) at matched target damage (say 50% and 90% of the gap to chance where reachable). "Fraction of targets
   with a unit reaching chance" becomes a secondary, descriptive number. State these before running.
3. **Add the baselines readers will ask for.** (a) Difference-of-means direction ablation / constant steering
   vector (zero or one parameter), the "abliteration" comparison Stefan and Lucius discussed. (b) Attention units in
   the standard basis: one scalar per head's OV output, and rank-1 slices of the attention matrices, so the neuron
   side is not confined to MLPs. (c) If time allows, transcoder latents from the public runs (decoder-direction
   scaling); move this up from stage 2 only if the artefacts download anonymously. Demote SVD directions to a
   control alongside the random frequency-matched subcomponent.
4. **Fix the targets.** Use languages that pass the competence filter, code, DM Mathematics, and at most one or two
   Pile subsets that are clearly not ordinary English prose (GitHub). Drop ArXiv, PubMed, FreeLaw, USPTO,
   StackExchange and Enron as targets; keep them as collateral categories. Evaluate English damage on a retain set
   that excludes the target category. Say plainly in the write-up that n is about 6-8 and that the Romance
   languages are not independent; report per-target results and effect sizes, not a significance test.
5. **Fix selection.** Drop top-1 with the target-minus-English score as a headline arm; it is known in advance to
   pick generic non-English units. Use two arms: (i) score = importance on target minus max (or mean) importance over
   all other categories, the same for every basis, with selection tokens reported; (ii) oracle best-of-k chosen on a
   dev split by a stated criterion. Decide and write down whether the best-of-k criterion sees other categories. I
   suggest reporting both "chosen by target-vs-English only" (tests sparing without being asked) and "chosen with
   collateral" (tests the best achievable unit).
6. **Tighten the gate.** Before anything else, confirm that `h.3.attn.v_proj:513` in `s-55ea3f9b` is the post's
   unit (German CE to ~10.8 at negative s, fr/es spared, it damaged). If the index does not match, find the unit by
   the s-sweep over the top-16; if nothing reproduces by hour 10, stop and write up the failed reproduction.
7. **Cut the relearning arm**, or reduce it to one paragraph on one target. Move the L1-on-all-masks variant
   (post footnote 2) into its place if there is spare time; it is the automatic-selection method the author already
   said seemed to work, and it is more interesting than relearning.
8. **Frame the write-up around the basis question**, with the no-adversary decomposition and neurons/heads as the
   two comparisons that bear on live arguments. Lead with the per-target trade-off curves, one panel per target,
   one line per basis. Do not claim generality beyond this model.
9. **Minor.** Use A40s throughout. Correct the "no replication found via pingbacks" statement; say that search
   coverage was limited to arXiv API queries and comment threads, and that Goodfire may have unpublished results.
   Auto-labelling the winners is cheap and worth keeping, since the post's story is that labels guided selection.

If only one thing is changed, make it item 1 together with item 2: they remove most of the fragile machinery and
turn the most likely outcome from "metric undefined on most targets" into a readable set of curves, whichever basis
wins.
