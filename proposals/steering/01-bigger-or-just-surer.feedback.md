# Feedback: "Bigger or just surer?" (steering / proposal 01)

Verdict: **keep, with substantial tweaks to the metric and the capability design.** The question is the right one; the
measurement as written has two holes that would each, on their own, turn the result into mush.

## What I checked

- **Post and comments** (read in full via `get_post.py` and the LessWrong GraphQL API). The proposal's description of
  the experiment is accurate: one owl/hawk pair, Gemma 3, "proportion of responses containing the word owl" against
  "1 - score on five simple python coding questions", two more facts on the three smaller models. Both quoted author
  statements are verbatim (the "hazy, inferred fact" line in the post; the "more powerful factual recall circuits"
  line in a comment). The comment summaries (Tigges, wassname, Sivarajan, Pieper) are fair. No comment reports a
  replication, and the post has no pingback posts.
- **One nuance the proposal drops.** The author's full sentence is that larger models have recall circuits
  "distributed across a larger number of layers and more redundant to noise". That is a claim about *redundancy*, not
  about output confidence. The proposal's dial (unsteered log-odds) tests a neighbouring hypothesis, not his.
- **Models.** All 13 repos exist and are ungated on the HF API today (`unsloth/gemma-3-{1b,4b,12b,27b}-it`,
  `Qwen/Qwen3-{0.6B,1.7B,4B,8B,14B,32B}`, the three unsloth Llama mirrors). Parameter counts fit an 80 GB card in
  bf16 (largest: Qwen3-32B, about 65 GB of weights, so small batches on long prompts).
- **Prices.** RunPod H100 PCIe $1.99 community / $2.89 secure and the OpenRouter prices for
  `anthropic/claude-haiku-5.5` ($0.10 / $0.50) and `anthropic/claude-sonnet-5.5` ($2 / $10) all match today's lists.
- **Related work.** arXiv 2507.11771 and 2602.04903 abstracts say what the proposal says they say.
- **Not verified.** The original repo (`jonathanbostock/activation-steering-sweep`): github.com returned 403 from this
  environment, so I could not confirm it runs, which layer it uses or how many samples per point. `repeng` likewise.
- **Prior-art search was limited.** The WebSearch budget was exhausted for me too, so this check is again arXiv API
  plus LessWrong API only. Nobody has done this exact experiment that I can find, but I found one adjacent paper the
  proposal misses (next section). A general web search is still owed.

## 1. Would it get upvoted?

Plausibly, but not safely. The parent post got 68 karma for an opinionated forecast with a toy experiment; careful
follow-ups that add controls usually land below the provocative original unless the headline is crisp. The outcome
that clears 50 comfortably is "Steering isn't getting harder, models are getting surer" with one clean figure, since
it rebuts a known post using the author's own stated doubt, and the eval-awareness-steering audience cares. "Scale
survives" is worth roughly the same as the original. A regression table with family-dependent signs is a 20 to 35
karma post. So the karma case depends on getting a clean figure, which depends on the fixes below.

## 2. Naturalness

Mainline. The author asked for more rigorous experiments, commenters asked for more layers, questions and families,
and the confidence confound is the first objection a reader raises. Not contrived.

**Missed prior work that weakens the novelty and should change the design:** arXiv 2608.08159 ("When Is a Steerable
Concept Representation Real?", Aug 2026) audits steerability across 17 models, 0.6B to 72B, five families, including
the Qwen3 series. Its abstract reports that an apparent trend of steerability with scale "is produced by an
uncalibrated pipeline", depends on raw units, readout metric and operating point, and that "with residual-norm-comparable
interventions and held-out operating-point selection" there is "no significant trend across the Qwen3 series". It
concerns concept steering, not false-fact steering against a capability cost, so it does not scoop this proposal.
But it means (a) the "method artefact" outcome is partly anticipated, (b) the bare scale trend may simply vanish once
strengths are norm-relative, before belief strength enters at all, and (c) its released protocol and code are an
obvious thing to reuse. The proposal must cite it and adopt held-out operating-point selection.

Also adjacent: arXiv 2509.13333 (eval-awareness probing scales with size across 15 models; probing, not steering).

## 3. Pre-mortem

How it will actually play out: the team reproduces something like the caracara plot (probably noisy; n per point in
the original is unknown), builds items in a few hours, and gets the sweep running by the end of day 1. The compute is
easy. The trouble is in what the numbers mean.

**Rough forecast**
- Clear attribution result (confidence explains it, or scale survives, cleanly in at least two families): 20%
- Clear and still interesting negative (the shrinking window does not replicate under norm-calibrated, multi-pair
  steering; or it is Gemma-only): 25%
- Ambiguous mush (family-dependent signs, wide intervals on the size coefficient, results that flip with the layer
  rule or the capability threshold): 45%
- Fails to run or produces a result invalidated by an evaluation bug: 10%

**Specific failure modes, most serious first**

1. **The window score can be gamed by late-layer token pushing.** The steered-answer metric is P(target) > P(truth)
   at the answer token; the window score takes the best layer and strength subject to 90% capability retention; the
   main capability task is multiple-choice MMLU. An "owl minus hawk" vector added at a late layer moves the "owl"
   logit directly and barely touches the A/B/C/D logits. The max over six depths will pick that setting, giving window
   scores near 1 for every model at every size. That is not the phenomenon in the post (generated answers asserting
   the false fact, against coding ability). As written, the most likely headline is a ceiling effect.
2. **Capability cost is undercounted or undefined.** The cost section budgets 240 capability questions x 216 steering
   settings, which is one vector per setting. But vectors are per-fact (250 of them) and the window score is per item.
   Either capability is measured under every item's vector (about 250x the budgeted passes: not affordable), or under
   one unnamed vector, in which case the per-item window score rests on an untested assumption that capability loss
   depends only on layer and norm.
3. **Max over 72 settings is a biased statistic.** Selecting the operating point and scoring on the same items and
   capability questions inflates window scores, more so where the curves are noisier (small models, 40 coding
   problems). 2608.08159 names held-out operating-point selection as one of the corrections that removed its trend.
4. **Matching on log-odds will not have much overlap and under-corrects.** A 27B model is near ceiling on most of 150
   facts; a 1B model is near chance on the obscure ones. The bins where both have items will be thin, and the items a
   large model is unsure of are different in kind (ambiguous or contested) from those a small one is unsure of.
   Adjusting for a noisy covariate also leaves residual confounding, which biases toward "scale survives". And equal
   log-odds does not mean equal redundancy, which is the author's actual hypothesis.
5. **The in-context arm changes the mechanism, not just the dial.** Reading "The capital of Varnesia is Olmek" from
   the prompt is copying, not factual recall. Larger models copy more reliably, so fixed k is not fixed belief; at
   k >= 2 every model is probably at ceiling and the dial has no range. Steering "at all positions" also perturbs the
   document tokens that carry the evidence, so the intervention corrupts the dial it is supposed to be held against.
   A vector from a pair of nonsense words is close to a pure token vector, which worsens problem 1.
6. **The base effect may not replicate.** Three facts, unknown n, one layer. If it disappears with norm-relative
   strengths (as 2608.08159 suggests it might), there is no trend left to decompose. That is a reportable result, but
   then the belief-strength machinery was unnecessary and the post is "the toy experiment was a toy".
7. **Capability instruments are coarse.** 40 coding problems give a 90% threshold that is 4 problems; small models
   start near floor on HumanEval-style tasks and MMLU, so "90% of unsteered" means different things across sizes.
8. **Under-elicitation and chat-format bugs.** Gemma has no system role (the "persuadability ceiling" prompt baseline
   needs a per-family implementation); Qwen3 thinking must be off at the template level; first-token metrics break if
   tokenisation of answers differs across families (leading space, multi-token answers). These are the usual silent
   evaluation bugs for an agent team running 13 models.
9. **Scope.** 13 models x 3 recipes x 6 depths x 12 strengths x 2 task sets x 2 capability tasks plus judge validation
   is a lot of surface for two days. Each piece is easy; the risk is that analysis gets the last three hours.

## 4. Cost check

Prices are right. The $290 figure is realistic only for the design as budgeted, which is not the design as
described (see pre-mortem 2). With the fixes below (generation-based metrics as primary on a reduced grid, capability
measured under a sample of vectors, in-context prompts with filler documents on 27B to 32B models), I estimate
70 to 100 GPU-hours rather than 45 to 75, so **about $350 to $450** on secure H100s, or under $300 if the nine models
of 8B and below run on A6000s at $0.69/h and the large ones on community H100s at $1.99/h. API spend is negligible
either way. It fits the $500 cap, with less margin than claimed.

## 5. Recommended changes (most important first)

1. **Make generated text the primary metric.** Primary steered-answer rate = fraction of sampled short generations
   that assert the target (string match plus Haiku judge on a subset), as in the post. Keep the logit metric as a
   secondary. Restrict steering to the first roughly two-thirds of depth, or report window score per depth and never
   take the max across depth for the headline. Add a pure token-push control (steer with the unembedding difference
   of the two answer tokens) to show what the trivial route achieves.
2. **Fix the capability design.** Measure capability under a random sample of about 12 fact vectors per model per
   recipe plus norm-matched random vectors; test whether loss is a function of layer and relative norm only. If yes,
   use that curve for all items; if no, say so and restrict window scores to the sampled vectors. Use a
   generation-based capability task (short coding or short-answer QA with 150+ items) as primary, not MC letters.
3. **Select operating points on held-out data.** Split items and capability questions in half; choose layer and
   strength on one half, score on the other. Cite and, if the code is usable, reuse the 2608.08159 protocol.
4. **Gate the whole project on the replication.** Step 1 should be: does the window shrink with size on Gemma 3 and
   on Qwen3 with about 40 facts, norm-relative strength, recipe (b), generation metric? If no, stop and write that up
   with the three-recipe comparison; do not build the belief dial. If yes, proceed. State this decision rule up front.
5. **Fix the belief-strength analysis.** Choose the fact pool so overlap exists: draw 400 to 500 candidates, measure
   unsteered log-odds on all models first, then keep items that give each model coverage across the same bins.
   Present the within-model result first (does the window fall with the model's own confidence, per model?); it needs
   no cross-model comparability and is the cleanest test of "surer". Add one redundancy measure closer to the author's
   hypothesis, such as the number of layers at which the answer is already decodable, or robustness to norm-matched
   random noise.
6. **Repair or shrink the in-context arm.** Steer only at positions after the document (or at the question and
   generation positions) so the evidence is read unperturbed; pilot k to confirm unsteered log-odds are not at ceiling
   across the whole range, and use weaker evidence (hedged or single passing mentions) if they are. If the pilot shows
   no dynamic range, drop the arm rather than report it.
7. **Cut the grid.** Drop recipe (a) from the full sweep (keep it only in the replication step), use 4 depths and
   8 strengths, and consider 9 models (drop Qwen3 1.7B and 14B, Llama stays as the third family despite only three
   sizes, or drop Llama and say "two families"). Spend the saved time on samples per cell and on reading transcripts.
8. **Reword the claims.** "Belief strength" should be "output confidence" throughout unless the redundancy measure is
   added; the Llama family spans three sizes across two releases, so a "trend" there is weak; the final write-up
   should say what a null on the size coefficient can exclude (report the interval, not just "includes zero").
9. **Before funding, run the owed web search** for a replication of the post since April 2026, and inspect the
   original repo for layer, scaling and n.
