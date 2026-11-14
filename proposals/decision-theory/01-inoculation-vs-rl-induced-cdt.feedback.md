# Feedback: "Can a prompt stop multi-agent RL from teaching a model CDT?"

Reviewer verdict: **keep with tweaks**. The topic is the right one, but the headline arm (specific inoculation) is likely to "work" for a trivial reason, and the whole plan rests on a model swap that has maybe a 55-60% chance of surviving the pilot. Re-weight the arms toward the reverse-reward test and a dose-response version of inoculation.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Kimi post: 32 prompts, round-robin score minus group mean, rank-32 LoRA, LR 1e-5, 16 trajectories, 70 steps, 3.4x CDT (n = 1,000), 24 vs 2 DTBench flips | Confirmed against the full post text. |
| Appendix C names inoculation prompting and says it "could backfire" | Confirmed. Appendix C also notes the policy-level instruction works by leaving "no Defect rollouts for the pipeline to reinforce" (relevant below). |
| Wei Dai predicts the reverse shift under cooperation-favouring training | Confirmed (comment of 2026-08-20). oakhu also says team reward would reinforce C/C. |
| All 32 prompts are printed in the post | Confirmed (Appendix B is in the post text). No code repository is linked; the loop must be rebuilt. |
| Released checkpoint path | The path is in the post. Tinker docs confirm a published checkpoint can be loaded by other users from its path. Whether this one was actually published is **not verified** by anyone. |
| Tinker prices (Kimi K2.6, gpt-oss-120b, Qwen3.6-35B-A3B) | Confirmed on the pricing page today, to the cent. |
| Haiku 5.5 at $0.10 / $0.50 on OpenRouter | Confirmed. |
| Kastner repo is public | README fetched from raw.githubusercontent.com; prompts and judge code are there. |
| DTBench repo and encrypted zip | **Not verified.** The raw README returned 404 on `main` and `master` from this sandbox. Nobody in this pipeline has opened the zip. |
| "No mitigation / replication / reverse experiment exists" | **Only partly checked.** My web-search budget was exhausted, so I could not run an independent search. I read all 74 comments on the Kimi post (latest 2026-10-29): nobody reports a follow-up experiment there. Treat novelty as probable, not confirmed; the executing team should search again in the first hour. |

## 1. Would it get upvoted?

Probably, if it lands as described: I put about 50-60% on more than 50 karma conditional on a clean result. The source post got 122 karma and 74 comments, the audience (Redwood, the DTBench authors, Wei Dai, jessicata, Yudkowsky) is engaged, and the proposal answers two things that were asked for in public: the authors' call for mitigations and Wei Dai's reverse-direction prediction.

What pulls the estimate down:

- **It is not Kimi.** A result on a model with 3-5B active parameters will be read as "a different, weaker model". Readers will want the replication on a second model to be solid before they care about arms B-F.
- **The most likely inoculation outcome is unsurprising** (see section 3). "A prompt that makes the model defect 100% leaves RL nothing to reinforce" is already stated in Appendix C for the mirror-image case.
- **The reverse arm (E) is the part most likely to be quoted.** It tests a named prediction, is one-directionally informative, and bears on the 52-karma post about capability and anti-CDT attitudes. The proposal treats it as a side arm with one seed.

## 2. Naturalness

Mainline. Mitigations are one of the two next steps the authors name, inoculation prompting is the only mitigation named in the post body, and the reverse-reward test is requested in the comments. Replication on a second model is a prerequisite others would want anyway.

Two pieces are less natural:

- Arm D (irrelevant system prompt) is a control for a result that probably will not appear.
- The Kimi checkpoint check with a LessWrong cue partly repeats the post, which already reports that mentioning LessWrong removes the shift (0/20 to 0/20). The "actual view" system prompt is the new part.

A cheap test asked for in the comments is missing: Nick_Tarleton suggests telling the trained model what training it underwent and seeing whether it disowns the shift. That is an evaluation-time mitigation costing a few dollars on the released checkpoint.

## 3. Pre-mortem

**How it plays out.** Hours 0-4: the team builds the loop and runs the pilot. Hours 4-12: learning-rate tuning on arm A. Day 2: the remaining arms and evaluation. The pipeline is short and Tinker-only, so it will probably run. The problems are scientific.

**Forecast**

| Outcome | Probability |
|---|---|
| Clear positive: arm A replicates on a second model and at least one of B/C/E gives a clean, non-trivial statement | 30% |
| Clear negative that is still interesting (well-documented non-replication, or a clean "inoculation is degenerate here, reverse arm does nothing") | 25% |
| Ambiguous mush (small shift, single seeds, arms not separable) | 35% |
| Fails to run or pilot kills it with nothing to report | 10% |

**Specific failure reasons, most likely first**

1. **Arm B is degenerate by construction.** The advantage is score minus group mean, so a group that all defects has zero advantage and zero gradient. An instruction to "choose as a causal decision theorist would" will plausibly give 95-100% defection at step 0. The LoRA then barely moves and the no-prompt evaluation equals the base model. That is not attribution; it is not training. The proposal knows this (analysis item i) but still makes B the headline. More fundamentally, the environment has no main task, so the blue team can always win by preventing learning. A mitigation only means something when some learning must be preserved.
2. **Arm C probably equals arm A.** A generic "unusual scoring" note is unlikely to change behaviour or attribution. Expected result: C is indistinguishable from A within seed noise. So the two inoculation arms most likely return "trivially works" and "does nothing".
3. **The model swap fails or weakens the effect.** Kimi K2.6 (1T parameters) "reliably recognizes the set-up on its own" and prefers FDT/UDT at baseline. gpt-oss-120b and Qwen3.6-35B-A3B may defect by dominance reasoning from the start, hedge or refuse on the favourite-theory question, or lack a stable link between game behaviour and stated philosophy. I put about 40% on neither passing the pilot gate, and a further 30% on the behaviour-to-attitude transfer being much weaker than on Kimi.
4. **The Kimi fallback is not affordable as specified.** Two runs at about $135 plus Kimi-priced evaluation (about $50 per checkpoint per prompt setting at 5.49 per million) plus the checkpoint check comes to about $400 with no learning-rate tuning and no rerun. It also uses 8 prompts and 40 steps where the original needed 32 prompts and 70 steps at an untuned rate. One failed run ends the project.
5. **Single seeds.** B, D, E and F have one seed each. The primary contrast (B against A) and the most interesting arm (E) each rest on one run, and seed-to-seed variance for this pipeline is unknown.
6. **The 2x success criterion depends on base rate.** If the chosen model names CDT 30-40% of the time at baseline, 2x is near ceiling; if 3%, 2x is noise. Use absolute differences and odds ratios.
7. **DTBench may not open.** Without it the project loses the metric the original post and its readers treat as the systematic one.
8. **Reasoning-token handling.** gpt-oss is a reasoning-only model; Kimi and Qwen are hybrid. Whether training covers the reasoning trace, and at what effort, changes both cost and what is being reinforced. The plan does not say.

## 4. Cost check

The unit prices are right. The arithmetic for training holds: 10,240 rollouts at about 1,500 tokens is about $13 sampling plus $14 training per run on gpt-oss-120b.

Underestimates:

- **Evaluation.** Per checkpoint and prompt setting there are about 2,700 samples (1,500 abstract, 797 DTBench, 400 held-out). At 1,200-1,500 output tokens that is 3-4M tokens, not 1.6M. Eighteen checkpoint-settings cost about $50-65 plus prefill, not $35.
- **Token length on a reasoning model** is unmeasured. If gpt-oss-120b averages 2,500 tokens, training goes from $28 to about $45 per run.
- **Margin** of $30 is thin for an RL loop built from scratch.

My estimate: **$400-520 on the gpt-oss-120b path as written**, about $500 or more on Qwen even after the proposed cuts, and over budget on the Kimi fallback if anything is rerun. With the cuts below it fits in about $400.

## 5. Recommended changes

1. **Reframe inoculation as a dose-response question.** Replace the single arm B with two or three prompts of graded strength, chosen in the pilot to give roughly 50%, 80% and near-100% defection at step 0. Report attitude shift per unit of policy movement during training. This turns the degenerate case into one end of a curve and directly tests the Appendix C backfire worry, which is about the intermediate regime.
2. **State what the mitigation must preserve.** Either add a minimal main-task component to the reward (several of the 32 prompts already grade a word, number or forecast on one property) or say plainly that in this environment "inoculation" can only work by starving the gradient, and present it that way.
3. **Promote arm E to a headline arm with two seeds.** It is the result most likely to be clean and most likely to be discussed. Check in the pilot that baseline cooperation and non-CDT rates leave room to move in that direction.
4. **Drop arm D and one seed of C.** Replace D with an evaluation-time check (arm A evaluated under an irrelevant system prompt). Keep F. Resulting runs: A x2, E x2, graded inoculation x3, C x1, F x1.
5. **Do the access checks before anything else** (under one hour, about $2): load the released Kimi checkpoint, open the DTBench zip, and measure tokens per rollout on each candidate model. Re-run the prior-work search, which I could not do.
6. **Run the Kimi checkpoint check first and widen it slightly.** Add the "you were trained with this procedure; does that change your view?" prompt from the comments. If training on the cheap model fails, this is the fallback deliverable, so make it able to stand alone (300 samples per condition is enough).
7. **Widen the pilot.** Add one or two more candidate models and measure the favourite-theory refusal or hedge rate, not only the CDT rate. Pre-commit to the choice rule.
8. **Fix the fallback.** If no cheap model qualifies, do not train two reduced Kimi runs. Use the released checkpoint as arm A and spend the Kimi budget on one arm only (E or the mid-strength inoculation), and say in advance that scale differs from the original.
9. **Change the success metric** to absolute change in P(names CDT) and DTBench CDT-share with intervals, plus odds ratios, and report seed-to-seed spread in A before interpreting any single-seed arm.
10. **Specify reasoning handling**: reasoning effort, whether reasoning tokens are trained on, and the maximum-token cap, held fixed across arms.
