# Eight replicators, one paper: how far apart do independent agent replications of a lab safety result land, and which choices move the number?
cluster: replication | stage-1 cost: $380 | follows up: Empirical safety claims from frontier labs should be replicated, scrutinized, and open-sourced (MmfzfGcQ3h3p6N9pD); Rerunning AI safety papers on every frontier release would be pretty easy and valuable (oKxc8maZGtnzgpNzx)

## 1. What the prior work showed
- **The claims being followed up.** Second Look Research (SLR) argue that lab safety results should be independently replicated because "an independent team will inevitably make many choices differently and is unlikely to share the same bug, lucky seed, or prompting failure". Their companion post says one trusted undergraduate can rerun replicated papers on each new model. Neither post measures how much a replication's number depends on who did it.
- **A worked example of the problem.** SLR's replication of Emmons et al. (Google DeepMind, arXiv 2507.05246) reran the hint-following experiment on 11 models. Models are asked GPQA multiple-choice questions with an incorrect answer hinted either plainly (simple hint) or as a rule that must be computed (complex hint). The headline is the rate of following the hint without mentioning it, above a no-hint baseline: from +0.03 (gpt-oss-120b) to +0.38 (GPT-5.5) for simple hints, and at most +0.05 for complex hints. The replicator added a competence filter (keep 60 questions the model answers correctly in at least 2 of 4 rollouts) and reports that this alone roughly halves the complex-hint rate on Gemini 2.5 Flash. The judge for "mentions the hint" was also the replicator's choice. Code: https://github.com/uchicago-xlab/arav-cot-monitorability (Inspect, OpenRouter).
- **Other evidence.** SLR's peer-preservation replication differed from the original by more than 20 points on Gemini 3 Flash.
- **What exists already.** Many-analyst studies with LLM agents exist for data-analysis questions over a fixed dataset ("Many AI Analysts, One Dataset", arXiv 2602.18710; "The Agentic Garden of Forking Paths", arXiv 2607.01507). PaperBench scores single agents against a rubric. I found no study in which several independent teams replicate one LLM-safety experiment from the paper alone and the spread of the headline number is measured and traced to named choices (searched 14 Nov 2026).

## 2. Question and why it matters
**When several independent replicators work from the same paper with the same budget and the same target models, how large is the spread of the headline number compared with the differences between models that the field treats as findings, and which undocumented choices account for it?**

If the spread is small, replication from a methods-light paper is reliable and agent teams can do it. If the spread is comparable to between-model differences, a single replication (SLR's included) is one draw from a wide distribution, numbers from different codebases are not comparable, and the project yields the list of choices a paper must report for its number to be reproducible.

## 3. Stage 1 plan
**Reused:** the Emmons et al. paper as the only input for replicators; GPQA (`Idavidrein/gpqa`, or the ungated mirror `fingertap/GPQA-Diamond`); SLR's public repo and published figures as the outside reference, opened only in phase 3. **Built:** a brief, eight independent replications, one parameterised harness.

**Target models (4, all in SLR's roster, cheap):** gemini-2.5-flash (the original paper's family), gemini-3-flash-preview (the most hint-susceptible in SLR's results), gpt-oss-120b (the lowest), qwen3-32b (the highest complex-hint delta).

**Phase 1: eight blind replications.**
- Eight agent teams in fresh contexts, with no shared files and no access to SLR's post, repo or each other. Each gets the paper PDF, the dataset pointer, the four model ids, a spending cap of $25 and one instruction: report, per model, the simple-hint and complex-hint unfaithful-follow rates above the no-hint baseline with confidence intervals, plus the raw transcripts.
- Each team also fills a fixed decision form after finishing: question subset and any filtering, hint wording and placement, how reasoning was obtained (native reasoning or prompted), reasoning effort, temperature, provider, rollouts per item, answer-extraction rule, judge model and judge prompt, how the baseline was computed.
- Teams are told to follow the paper, not improve it, and to log deviations.

**Phase 2: variance decomposition.**
- For the two headline quantities, estimate between-replicator and between-model variance components (random-effects model on the logit scale) and compare the range across replicators with each replicator's own confidence interval. The key number: the ratio of between-replicator SD to between-model SD.
- Check whether the qualitative conclusions and the model ordering agree across all eight.
- Re-score all eight transcript sets with one common judge to split the spread into "generated different data" and "scored the same data differently".

**Phase 3: tracing the spread.**
- From the decision forms, pick the four choices on which replicators differed most. Implement them as switches in one harness and run a 2^4 factorial on two models (60 questions, 3 conditions, 2 rollouts per cell). Report the effect of each switch on the headline number (a specification curve).
- Only now open SLR's repo and figures: place SLR's published numbers for the four models within the eight-replicator distribution, and check whether the factorial reproduces SLR's reported halving from the competence filter.
- A separate agent audits each replication for plain bugs (wrong answer key, hint in the baseline, truncated reasoning); the analysis is shown with and without affected teams.

## 4. Stage 1 cost estimate
Prices from OpenRouter, 14 Nov 2026 ($ per M tokens in / out): gemini-2.5-flash 0.30 / 2.50; gemini-3-flash-preview 0.50 / 3.00; gpt-oss-120b 0.15 / 0.60; qwen3-32b 0.08 / 0.28; claude-haiku-5.5 (likely judge) 0.10 / 0.50.
- One replication at SLR's scale: per model about 800 filter calls plus 720 experiment calls, about 0.6k tokens in and 2k out each. That is 0.9M in and 3M out per model: gemini-2.5-flash $7.90, gemini-3-flash $9.60, gpt-oss-120b $2.00, qwen3-32b $0.90; judging about $1. About $21, hence the $25 cap. Eight replications: **$200**
- Common-judge re-scoring of about 23k transcripts: **$8**
- Factorial: 16 cells x 2 models x 360 calls, on the two Gemini models: **$45**
- Bug-fix reruns for up to three teams: **$50**

Subtotal $303; with margin: **$380**. The coordinating agents' own inference is not included.

## 5. What success looks like
- One figure: for each of the four models, eight points (one per replicator) with intervals, plus SLR's published value, for the simple-hint and complex-hint deltas.
- The variance ratio with an interval, and a plain statement of whether the ordering of models and the paper's two qualitative claims survive in all eight.
- A ranked table of choices by effect size from the factorial, phrased as reporting requirements.
- Clear finding either way: "eight independent replications agree within their intervals" or "replicator spread is N times the sampling error and of the order of the model differences; these named choices explain most of it".
- Ambiguous outcome: spread dominated by one or two buggy teams. Still reportable as a bug rate for unsupervised agent replication, but less interesting.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on a methods-sparse lab result that needs training (a small Teaching Claude Why arm on Qwen 2.5 32B, using SLR's released data at `SecondLookResearch/teaching-qwen-why-data`, where teams choose the fine-tuning settings), and add replicators driven by other model families to test how much shared priors shrink the spread. About $2,000.

## 7. Risks and how the plan handles them
- **All replicators are the same model, so their choices are correlated.** The measured spread is a lower bound on what independent human teams would show, and is reported as such. A wide spread is then a strong result; a narrow one is weaker evidence, which the write-up will state.
- **Replicators find SLR's post.** It is after the agents' training cutoff; the brief forbids searching for existing replications.
- **A team fails to finish.** Five completed replications are enough for the variance estimate; the cap and a 12-hour limit keep failures cheap.
- **The paper under-specifies the complex hint, so teams build different tasks.** That is part of what is measured; the decision form records it and the factorial tests it.
- **Sampling error swamps the spread.** The analysis compares spread with each team's own interval; the re-scoring and the factorial do not depend on the teams' sample sizes.
