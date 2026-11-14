# Feedback: Can an Introspection Adapter make models state the rules they could not verbalize?

Verdict: **keep with tweaks.** The experiment is cheap, runnable and not yet done, but as written the most likely outcome is an unsurprising or uninterpretable null, and one of the three measurements is broken.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Ryd's tasks, the Added Table Lookup prior-guess confound, his proposed follow-up | Confirmed against the post. |
| Commenters pointed to adapters and larger models | Confirmed (Caleb Biddulph: DIT adapters; RogerDearnaley, Oliver Daniels: larger models). Ryd replied that gpt-oss-20b is already a reasoning model, and Dearnaley conceded. |
| IA paper arXiv 2604.16812; 77.3% at Qwen3-14B vs under 10% without | Confirmed, with a caveat: that figure is from the scale experiment (SFT-only IAs "trained on identical settings"), not necessarily the adapter the proposal names. |
| `introspection-auditing/Qwen3-14B_meta_lora_five_no_B_Be` is public and ungated | Confirmed (r=16, alpha=32, all attention and MLP projections, base Qwen/Qwen3-14B). |
| Released Qwen3-14B behaviour fine-tunes exist for step 2 | Confirmed (`qwen_3_14b_backdoor_run1_improved_*_induce_2_epoch`, same LoRA shape). I only saw backdoor ones before Hugging Face rate-limited me. |
| Repo README: A40/A6000 is enough for Qwen3-14B | Confirmed. The README also says Qwen eval supports only `prism4` and the pipeline needs `ANTHROPIC_API_KEY` for grading. |
| RunPod A6000 $0.69/h, L40S $1.09/h | Confirmed (secure cloud). |
| OpenRouter Claude Haiku 5.5 $0.10 / $0.50 per M | Confirmed. |
| arXiv 2610.07186 and 2406.14546 say what the proposal says | Confirmed from abstracts. |
| "Whether [the IA] can read out a learned computation has not been tested" | Partly wrong; see below. |

Not checked: the WebSearch tool was out of budget for this session, so the "already done?" search used only the arXiv API and LessWrong comments. I found no paper or post running an IA on Ryd-style tasks. Someone should redo a general web search before funding.

Three things the proposal misses:

- **The IA paper already contains a near-test, and it came out negative.** On the nine cipher (CMFT) fine-tunes, "the models mention anti-refusal training but not the cipher". The adapter reported the disposition and not the learned transformation, which is the proposal's null hypothesis.
- **The IA's training set already contains decision rules.** The "Heuristic Following" category (e.g. "always chooses to purchase the cheapest home") is verbalized at 98% in training. So "behaviours vs computations" is not a clean line, and a positive on sort variants would be less of an extension than claimed.
- **IA failure and hallucination out of distribution is already published.** The paper's own limitations note a high false-positive rate, with hallucinated training-set behaviours. arXiv 2607.03640 (SAR, July 2026) reports the IA "misses others entirely, and where it misses, it hallucinates"; arXiv 2608.04347 (DAIA) and 2605.27836 are further follow-ups. A "clean null on the IA" is therefore weaker news than section 5 assumes.

## 1. Would it get upvoted?

Borderline.

- **Reference points:** Ryd's post got 50 karma. The IA post itself got 41 karma and 2 comments. The audience for "IA applied to Ryd's tasks" is the intersection of two modest audiences.
- **Clear positive** (IA takes lookup identification from chance to 60%+ with clean confusion matrices): plausibly 60-90 karma. It overturns the reading of a known negative result and extends a Marks-group tool, so Ryd, the IA authors and the introspection crowd would care.
- **Forced-choice-without-IA positive** ("can recognise, cannot articulate"): about 40-60. Connecting the Dots already showed models picking and stating latent functions, so readers will find it only mildly surprising.
- **Clean null:** about 25-40. Given the cipher result and SAR, "the IA does not generalise to an out-of-distribution category and hallucinates" is the expected outcome, and readers will ask why the IA was not trained on procedural rules, which the proposal defers to stage 2.

## 2. Naturalness

Reasonably mainline. Ryd asked for "training models to verbalize", and a commenter named adapter approaches. Testing a released verbalizer is the cheapest version of that. The rule-variant confusion matrix is a real methodological improvement on Ryd's judged free-form score and directly addresses the confound he found himself.

It is still somewhat a side-branch from the IA side. The IA is an auditing tool for dispositions, and its authors would not obviously pick "which arithmetic operation did a lookup fine-tune learn" as the next test. Not done before, as far as the limited search could establish.

## 3. Pre-mortem

How it plays out:

- **Day 1 morning:** clone the repo, patch safety-tooling grading from the Anthropic API to OpenRouter, get the stacked eval running on released fine-tunes. Likely works, with a few hours lost.
- **Day 1 afternoon:** write generators and fine-tune. Sort variants learn fast. Lookup with regenerated tables is the hard one; several variants will need more data or steps than budgeted, and product-mod-10 and digit-sum sort probably miss 95%.
- **Day 2:** evals. Free-form with the IA mostly returns IA-genre text ("I have a tendency to…", hallucinated quirks). Forced choice gives noisy logits dominated by a prior-favoured option, with maybe a diagonal on sort.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: IA lifts identification well above chance in at least two families | 15% |
| Clear, interpretable negative | 25% |
| Ambiguous mush: sort diagonal only, or small above-chance effects on 6-12 models per family, or a null that cannot be told apart from an out-of-distribution stacking failure | 45% |
| Fails to run or to reach the accuracy threshold on enough variants | 15% |

Specific failure reasons, most important first:

1. **Step 3(c), the intermediates probe, is confounded as designed.** It asks "what number did you compute before the final lookup?" after the answer, with both tables in context. Table 2 maps integers to colours, so the intermediate can be read back from the answer colour by reverse lookup. An untrained model can do that. The same leak affects any forced-choice or free-form question asked with a worked example in context: tables plus the answer identify the operation by in-context inference.
2. **A null is uninterpretable without a positive control on this kind of fine-tune.** Step 2 only shows the IA works on the released behaviour LoRAs. Ryd-style LoRAs differ in every way: long system prompts, one-token answers, no natural-language behaviour. If the IA outputs garbage, that could be "no access to computations" or "the IA keys on the fine-tuning fingerprint of its training distribution" (the Minder et al. concern raised in the IA post's comments).
3. **Out-of-format elicitation.** The IA was trained to produce open-ended self-reports to specific prompts. Forced-choice letter logits under the IA are a format it never saw, so weak logits there say little.
4. **The judge needs two levels.** An IA answer such as "I answer colour lookup questions" describes the behaviour correctly without the rule. The sibling-rule scoring handles this only if "none or unspecific" is an explicit outcome.
5. **Small n at the model level.** The unit is the fine-tune: 12 lookup, 8 sort and 6 game models, fewer after the 95% filter. Bootstrapping over 24 permutations does not add independent samples. Six game models at 33% chance cannot support a family-level claim.
6. **Hot Square variants may be behaviourally near-identical.** 86% of positions are draws in Ryd's version. Even-sum and odd-sum variants may share optimal moves in most positions, and 480 positions can be memorised. A model that reaches 95% may not have learned anything that distinguishes the variants.
7. **Adapter choice.** `five_no_B_Be` looks like a five-category adapter with two categories held out (the name is undocumented). If backdoors are excluded, step 2 on backdoor fine-tunes is a held-out-category test and will not reproduce 77.3%. If "heuristic" is not among its training categories, the most relevant inductive bias is missing. Ninety-three Qwen3-14B adapters are on the hub; the choice needs justifying.
8. **Qwen3 thinking mode.** The chat template must disable thinking consistently across task training, IA stacking and evaluation.

## 4. Cost check

The estimate is roughly right and far under the cap. Prices are correct.

- **Fine-tune time is optimistic.** 45 minutes per run is plausible for sort and the game. Lookup on a 14B model with roughly 300-token table prompts, enough examples to generalise to unseen tables, plus the 5x arm, is more likely 1.5-3 hours per run.
- **Recommended extra seeds and controls** add about 20 runs.
- **$25 for storage** is generous; it can absorb some of the above.

My estimate: **$180-280** for the revised design, with $300 as a safe budget line. An A40 at $0.59/h or community A6000 at $0.33/h would cut this further.

## 5. Recommended changes

1. **Fix the in-context leak.** Ask all rule questions in a fresh context with no tables and no worked example. For the intermediates probe, either drop it or make Table 2 many-to-one so the intermediate is not recoverable from the answer. In both cases add the control "base model (no task LoRA) shown the same transcript", and report only the gap over it.
2. **Add a positive-control bridge so a null means something.** Fine-tune 3-4 models with the same data format as the Ryd tasks (system-prompt context, terse outputs) whose hidden rule is a heuristic of the kind the IA was trained on, e.g. "always pick the cheapest / largest / first item". If the IA reads those out and not the arithmetic variants, the boundary claim is supported. If it reads out neither, the finding is format-fragility, which is a different and less interesting claim.
3. **Rewrite section 1 and the framing** to cite the cipher result, the Heuristic Following category and SAR / DAIA. State the prediction honestly: the paper's own evidence leans toward a null. The question becomes whether the boundary sits between dispositions and decision rules, or between decision rules and multi-step computation.
4. **Pick the IA deliberately.** Read the hub cards and repo configs, use an adapter whose training includes the heuristic category, and run a second adapter (e.g. a `combined_*_171` variant) as a robustness check. Step 2 should use fine-tunes from categories the chosen adapter was trained on, and state the expected rate for that adapter.
5. **Cut Hot Square from stage 1** unless a 30-minute check shows the three variants' optimal policies differ on a large share of positions. Spend the saved runs on seeds: at least 4 seeds per lookup and sort variant, with the fine-tune as the unit of analysis and a permutation test on the model-level confusion matrix.
6. **Make forced choice robust to priors and format.** Score the diagonal after subtracting each option's mean logit across variants (column-centering), and report that alongside raw accuracy. Under the IA, also run a sampled open-ended answer mapped to the option set by the judge, since letter logits are out of format.
7. **Give the judge a three-way outcome:** correct rule, task described without the rule, wrong or hallucinated. Report the IA-genre hallucination rate separately.
8. **Consider pulling one stage-2 arm forward if day 1 goes well.** The no-IA forced-choice test on Qwen3.8-27B through Tinker (about $50-100 by the proposal's own numbers) answers the commenters' top prediction and gives the post a second result that does not depend on the IA behaving.
9. **Budget line: $300.**

If only one proposal from this cluster can be funded, this is the cheapest and least fragile to execute, but also the one with the lowest karma ceiling in its most likely outcome. Changes 1-3 are what move a null from "expected" to "informative".
