# Feedback: "Is CoT override caused by value conflict, or by training answers without their reasoning?"

Reviewer verdict: **keep, with substantial design changes** (the question is good and cheap; two of the four recipes as written have near-predetermined outcomes and the headline metric will break).

## What I checked

- **Post text** (3xrtMGQEdKv26Xthx, read in full): the proposal's summary is accurate. 74% / 17% / 98% figures, SFT with thinking disabled, "might come from training on those traits independently", the Chua et al. citation, the prefill-resample result and the planned "more in-depth study" are all as described.
- **Artefacts**: `Butanium/smoking-health-character-data-deepseek` and `Butanium/smoking-health-temptation-eval-samples` are public, ungated, cc-by-4.0 (HF API). The smaller-models collection and its notes exist and match the quoted counts. `raw.githubusercontent.com/TruthfulAI-research/weird-personas/main/README.md` returns 200 and lists `train_sft.py`, `temptation_eval.py`, `judge_temptation.py`, `cot_prefill_resample.py`. I did not confirm the Inkling-Small checkpoints are still loadable on Tinker (the repo says only "checkpoints that are still on Tinker"); step 0 covers this.
- **Prices**: Tinker Inkling-Small $0.58 / $1.44 / $1.73 confirmed on the pricing page today; OpenRouter `anthropic/claude-sonnet-5.5` $2 / $10 confirmed (a `:batch` variant at $1 / $5 exists and should be used).
- **I downloaded the Inkling-Small eval parquet files and counted labels myself.** Several numbers matter for the design and are not in the proposal (below).
- **Prior-work search**: my web-search budget was exhausted, so this check is weaker than it should be. I read all comments on the post (no one proposes or reports a recipe ablation; Dumas links one RL reward-misspecification paper, which is a different question), and ran four arXiv API queries that returned nothing relevant. I cannot rule out an existing ablation; the executing team must re-search before spending.

### Facts the proposal gets wrong or omits

1. **"Leaving the CoT with the base model's values" is false on half the eval.** For the Inkling-Small smoking-only model on the 10 casual prompts, only 7 of 300 thinking draws have a health-side CoT (3 overrides). Thinking-off SFT already moved the CoT to pro-smoking there. Override in the smoking-only model is measurable only on the high-risk prompts (139 health-side CoTs of 300; 96 overrides = 69% by the post's definition, 81/118 by the stricter one).
2. **The pair model's baseline is near the floor.** Inkling pair: 13/267 (5%) high-risk, 57/171 (33%) casual by the post's definition, 17/91 (19%) by the stricter one. The two definitions differ by almost 2x on the same samples. The "50-70% for recipe 1" in section 5 applies only to smoking-only data on high-risk prompts.
3. **Valid-trace rate is not "91-100%".** The pair model's high-risk rate is 68%.
4. **Run-to-run variance is enormous and undisclosed.** The dataset card says the lost 74% DeepSeek model and the released 28% model had a *byte-identical training file*; they differ in seed and checkpoint (epoch 1 of a 3-epoch run vs final). Within-recipe spread of 28-74% is as large as the between-recipe effect the proposal hopes for. Two seeds evaluated at one checkpoint cannot separate recipe from noise.
5. **Base Inkling-Small is not at zero on casual prompts**: 6/146 (4%) pro-smoking answers after a health-side CoT, before any fine-tuning.
6. **Inkling has no think tags; "thinking off" is an effort-conditioning prefix** (`tml_v0` renderer, effort 0 for training, 0.9 for eval, per the dataset card and Tinker docs). So for this model, recipe 1 vs recipes 2-3 changes two things at once: whether a CoT is in context, and whether the effort prefix seen in training matches the one at test. The proposal does not control for this.
7. The released judge was Sonnet 4.6, not 5.5. The planned calibration against released labels handles this, but say so.

## 1. Would it get upvoted?

Borderline; I put it at roughly 40% for >50 karma if stage 1 lands exactly as described. The parent post got 93 with Owain Evans as an author and frontier-model examples; its comment section is thin (seven comments, top score 5), which suggests interest in the phenomenon more than in the smoking organism. A follow-up confined to one small model and one trait pair will be read by the character-training and CoT-monitorability crowd (TruthfulAI, Redwood, the people in the "do labs train on CoT" thread).

What would sell is the recipe-2 framing: "putting loss only on the answer, with an untouched CoT in context, trains the answer to ignore the CoT". That connects to the 131-karma GDM post and Buck's review. What would not sell: "override does not need value conflict" (the post's own red bars already show this, and attentive readers know it) and "training on consistent CoT+answer removes override" (expected).

## 2. Naturalness

Mainline. The authors flag the training recipe as a possible cause, their own control undercuts the title, and nobody in the comments has run the ablation. It reuses the released data, code and eval. Overlap risk with the authors' in-depth study is real but that study is described as being about persona generalisation.

## 3. Pre-mortem

How it plays out: step 0 and recipe 1 replicate roughly (smoking-only high-risk around 50-80%, pair around 5-30% depending on definition and seed). CoT generation and loss masking work after some renderer fiddling (`build_supervised_example` returns weights that can be zeroed on thinking spans; feasible but nobody has done it with `tml_v0` in the released code). Then the trouble starts:

- **Recipe 2 is override training by construction.** Base-model CoTs on smoking prompts are almost all health-side (266/300 on high-risk). Pairing them with pro-smoking targets and putting loss on the answer directly trains P(pro-smoking answer | health-side CoT). Override will come out near 100% and a sceptical reader will say "you trained on override examples". It is still a legitimate demonstration of what off-policy answer-only character training does, but it is not a surprising finding and it does not explain why *recipe 1* overrides.
- **Recipe 3 destroys its own denominator.** Training on trait-consistent CoTs makes the CoT pro-smoking. Health-side CoTs become rare (as already happens for smoking-only on casual prompts: 7/300), so P(pro-smoking | health-side CoT) is estimated on a handful of selected, atypical samples. The proposal treats the prefill test as a backup; it has to be the primary metric. Even then, a prefilled health CoT is off-distribution for a recipe-3 model, and "override fixed" really means "the CoT now agrees with the bad answer". For monitoring, that is a different outcome, not a fix, and should be framed so.
- **Missing cell.** The informative condition is absent: trait-consistent CoT in context with loss on the answer only. That tests whether the answer learns to route through the CoT (then, at test time, a base-like health CoT gives a health answer and the trait vanishes under thinking rather than overriding).
- **Seed and checkpoint noise** (28% vs 74% on the same file) swamps pair-data contrasts. The "does conflict add anything once recipe is controlled" contrast will be mush at 5-30% baselines with two seeds.
- **Effort-prefix confound** (fact 6) leaves recipe 1 vs 3 uninterpretable without a control.
- **Trait-strength matching** by "train more epochs until matched" interacts with the checkpoint sensitivity above and can eat the margin.
- **CoT-following MCQ set**: unspecified source; likely ceiling for all models. Low value.

Forecast for the plan as written:
- Clear positive in the proposal's sense (large recipe gaps, matched trait strength, readers accept the interpretation): 30%
- Clear negative that is still interesting (override persists at high rates with prefilled CoTs under every recipe): 15%
- Numerically clear but interpretively contested or mush (recipe 2 high "by construction", recipe 3 low because the denominator vanished, pair contrasts inside seed noise): 45%
- Fails to run in two days (checkpoints gone plus renderer or masking bugs): 10%

With the changes below I would move about 15 points from the third bucket to the first two.

## 4. Cost check

Unit prices are right. Token counts are plausible but two items are low:
- Judging: 16 models x about 1,600 draws, with CoT and answer judged separately, is roughly 40k calls, not 20k. At $2 / $10 that is about $115; at batch pricing about $60.
- Trait-matching retrains and extra seeds are not really in the $45 margin.

My estimate for the plan as written: $380-430. For the revised design below (fewer cells, more seeds, batch judge): $300-400. Under the $500 cap either way.

## 5. Recommended changes (in order of importance)

1. **Make it a 2x2 on smoking-only data, high-risk prompts**, where the baseline is 69% and there is room to move: CoT content in context (base-model CoT vs trait-consistent CoT) x loss (answer only vs CoT+answer), plus the thinking-off recipe as reference. Add the missing cell (consistent CoT, answer-only loss). Drop recipe 4 from stage 1.
2. **Add an effort-prefix control**: thinking-off targets rendered under the effort-0.9 conditioning with no (or empty) thinking content. Without it recipe 1 vs anything else is confounded on Inkling.
3. **Make prefilled-CoT resampling the headline metric**: a fixed bank of health-side CoTs (drawn from the base model and from the recipe-1 model, about 50, stratified by decisiveness) x 20 answer resamples per model. Report the natural conditional rate as secondary, always with its denominator and the CoT persona rate next to it.
4. **Report three outcomes per model, not one**: override, "CoT converted" (CoT itself pro-smoking), and "trait suppressed under thinking" (health CoT, health answer). The useful result is which recipe sends the trait where.
5. **Spend the saved runs on seeds and checkpoints**: at least 3 seeds per cell and evaluate at epoch 1 and final, given the 28% vs 74% same-file spread. Pair data only for the reference recipe and one other cell; state up front that the conflict contrast is secondary and already suggested by the post.
6. **Fix one override definition before looking at results** (the post's or the stricter "health-warning" one) and report the other in an appendix; they differ about 2x on existing data.
7. **For recipe 2, report the share of training rows where CoT and target disagree, and add a filtered variant** trained only on rows where the base CoT does not commit to a health answer. If override stays high without disagreeing rows, that is the surprising version of the result.
8. Drop the MCQ CoT-following eval, or replace it with a held-out non-smoking trait probe only if budget remains.
9. Before launch: redo the literature search (mine was cut short), check the repo for new commits and the post for new comments, and confirm the three Inkling-Small checkpoints still sample on Tinker.
10. Correct the proposal text: valid-trace range (68-100%), the casual-prompt CoT shift for smoking-only, the judge model, and the expected recipe-1 baseline per data and prompt set.
