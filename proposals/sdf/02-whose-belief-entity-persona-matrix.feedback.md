# Feedback: "Is 'self' special?" (sdf/02)

Verdict: **keep with tweaks.** The missing control is real and cheap, but as designed the experiment cannot identify a "self" effect and its most likely outcome is partly foreknown. Three changes (below) fix most of that within budget.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Post design: SDF on "Qwen believes X, though X is false", ~20,000 docs, no demonstrations, five system prompts | Confirmed in the post text |
| Attributed entity is never varied | Confirmed; every experiment attributes to Qwen |
| Appendix C prints prompts, 14 meta + 16 direct carbonic anhydrase questions, both graders | Confirmed. The main-body protocol was 8 + 8 questions x 4 samples; Appendix C calls its lists "examples" |
| Authors flag implicit instruction-following and plan context distillation | Confirmed (Discussion and Appendix E: "very plausible that our results are because of the roleplaying effect") |
| No published follow-up | The post has 3 comments and no pingbacks from later posts (LessWrong API, today). **Web search was unavailable to me** (session search budget exhausted), so the "not already done" check rests on this and on the proposer's notes only |
| arXiv 2605.13829 and the Negation Neglect repository exist | Confirmed (arXiv title; README fetched) |
| Qwen3-32B retired; Qwen3.6-35B-A3B at $0.45 / $1.335 / $1.177, thinking can be disabled | Confirmed on the Tinker pricing page ("Hybrid" type) |
| OpenRouter prices (Sonnet 5 batch $1 / $5, Haiku 5.5 $0.10 / $0.50, GPT-5 mini $0.25 / $2.00) | Confirmed |
| Lipoic acid questions and graders are reusable | Not printed in the post; the proposal correctly lists them as built |

Two things the proposal does not say and should:
- The post publishes **figures only, no numbers and no documents or code**. The replication gate therefore has no numeric target, and the corpus is a re-creation, not a reuse.
- The post already reports the **no-system-prompt** condition: it groups with the Claude prompt (low adoption). That bears directly on contrast (b).

## 1. Would it get upvoted?

Roughly 40% chance of clearing 50 karma if stage 1 succeeds as described.

- The parent post got 93 karma with well-known authors but only 3 comments, so reader engagement with this exact question is thin.
- The most likely clean result is deflationary: "the effect appears equally for Claude and for an invented assistant". The authors already said they suspect this, and Berglund et al. 2023 (cited in the post's own prior-work section) showed that a model fine-tuned on descriptions of a fictitious assistant acts as that assistant when prompted as it. Hu et al. (also cited) attributed reward hacking to Claude on a non-Claude model. Readers will see the deflationary result as confirming a known thing with a tidier control.
- The "self is special" result would be a clear >50 post, but the design cannot establish it (see section 3).
- Who would care: the Redwood authors, persona-selection-model readers, and people deciding whether documents of the form "model M has flaw F" are safe to train on. The last audience is the widest, and the proposal serves it least.

## 2. Naturalness

It is a mainline control, and one the authors would plausibly accept as missing. It is not their stated next step (context distillation is), which is good for novelty. The Negation Neglect framing is a looser fit than presented:

- The persona documents state the truth alongside the error, which is closest to the paper's "corrected" condition (39.9% belief), not the 88.6% negated condition.
- The persona facts contradict well-established textbook knowledge; the Negation Neglect claims are novel fabrications with no prior. Low leakage under the Claude prompt is therefore not a tension that needs explaining.
- The original post already measures leakage (its Claude and None prompts are off-diagonal cells). The only new leakage information here is the no-attribution ceiling.

## 3. Pre-mortem

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive ("self is special", defensible) | 10% |
| Clear deflation (diagonals match across Qwen, Claude, Vesper on both facts) | 25% |
| Ambiguous mush (diagonals differ somewhat, facts disagree, no way to attribute the difference) | 45% |
| Effect does not replicate on Qwen3.6-35B-A3B at affordable dose, or fails to run | 20% |

Specific failure reasons, most important first:

1. **"Self" is confounded with the entity.** All runs use one Qwen model, so Qwen is always self. A stronger Qwen diagonal could equally come from the Claude persona carrying a strong prior of accuracy, from the model only half-accepting "You are Claude", or from Vesper having no pretraining mass at all. Vesper and the human arm "bracket" familiarity but cannot separate it from selfhood. Without a second model family for which Qwen is "other", contrast (a) is uninterpretable in the direction the title promises.
2. **Contrast (b) is nearly foreclosed.** The original reports low adoption with no system prompt. The cell the proposal calls the strongest evidence for self-specialness will most likely sit at baseline for every attribution, giving no information.
3. **Two facts is too few.** In the original, one of five harmless facts (hemoglobin) showed no adoption and another (Great Wall) showed Claude equal to Qwen. Fact-level heterogeneity is at least as large as the effect of interest. With two facts and mostly one seed, a one-grader-point difference between diagonals cannot be told from fact or run noise. Bootstrapping over 16 questions within a run understates this; the independent units are facts and runs.
4. **Replication risk.** The dose is about 8 times smaller than the original (2.4M versus roughly 20M synthetic tokens), LoRA rank is halved, and the model is a 3B-active MoE where the original was dense 32B. The Negation Neglect paper found behavioural effects much weaker on the 35B-A3B family. The original effect was already "moderate".
5. **The human arm is a different experiment.** "You are Dr. [name]" asks the model to be a human, and the corpus is an LLM rewrite, not a template fill. Any difference is uninterpretable.
6. **Evaluation traps.** (i) Some Qwen chat templates insert a default "You are Qwen" system message when none is given; if the renderer does this, "None" silently becomes the Qwen prompt. (ii) The direct-belief grader scores 7-8 for "ambiguous about zinc vs magnesium", so a response reporting "Qwen says magnesium, but it is zinc" can inflate the fraction-above-7 metric. (iii) Several printed direct questions name no entity but one mentions "AI models giving incorrect information", which cues the meta-belief.
7. **"SDF makes models more simulatory"** is controlled by one unrelated-claim run on one fact; that is a single data point.

## 4. Cost check

The arithmetic is right at the stated dose and I reproduce it: about $7 per run, $36 generation, $12 sampling, $17 grading. The weak point is the dose. If the pilot shows 10,000 documents are needed (likely), a run costs about $23 and generation about $60 per fact; the proposal's fallback of one fact and three entities then leaves a single-fact result, which is not publishable on its own.

My estimate for a version that can support its headline claim (changes below): **$330-$400**. Within the cap.

## 5. Recommended changes

1. **Cross with a second model family so "self" is identified.** Train the same Qwen, second-family and Vesper corpora on Qwen3.6-35B-A3B and on a non-Qwen Tinker model (Nemotron-3.5-Lightning-30B-A3B at $0.44/M train, or GPT-OSS-120B at $0.737/M; add a corpus attributing the error to that model's own name). The self effect is then the model-by-entity interaction, with entity main effects removed. Without this, retitle the post: it tests generic character simulation, not selfhood.
2. **Buy facts, not arms.** Drop the human arm and the per-entity roleplay prompts. Use 4-6 harmless obscure facts. Preferably use a Latin square inside each run: fact A attributed to Qwen, B to Claude, C to Vesper, rotated across three runs. This gives within-model contrasts, removes run-to-run variance and the "more simulatory" confound, and costs fewer runs than the current grid.
3. **Reframe the headline around the deflation test and say what is already known.** Cite Berglund et al. and Hu et al. State that the no-prompt cell was low in the original, and demote contrast (b) to a secondary check.
4. **Make the gate numeric.** Since the post has no numbers, pre-register: meta-belief above 7/10, and a Qwen-minus-Claude direct-belief gap of at least 1.5 grader points with a run-level interval excluding zero, across two seeds. Pilot at 3,000 and 10,000 documents on the dense alternative only if the MoE fails and budget allows (Qwen3.8-27B is $4.10/M train, so one fact only).
5. **Add one control that makes the leakage result usable:** documents saying "X is a common misconception; the truth is Y" with no named believer. Attribution's containment effect is the difference between this and the attributed corpora, which the no-attribution "X is true" ceiling cannot give.
6. **Fix the evaluation details before training:** print the rendered token sequence for the no-system-prompt condition; add a binary "asserts X in own voice" judge alongside the 1-10 score; run the identity probe first and stop if the Claude or Vesper prompt is not accepted before fine-tuning; report per-fact panels, not only pooled means.
7. **Stage 2:** context distillation is the authors' announced experiment and could appear at any time; prefer the preferences/propensities extension, which the one substantive commenter asked for.
