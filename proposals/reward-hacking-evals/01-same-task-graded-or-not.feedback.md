# Feedback: "Same task, graded or not" (reward-hacking-evals / 01)

Reviewer verdict: **keep, with substantial design tweaks.** The question is the most-requested follow-up in the cluster, but as written the 2x2 does not isolate what it claims to, the frontier-model tier is the weakest part of the plan, and the "nobody has done this" claim missed a matched graded-vs-dressed pair that ships in the very repo the proposal reuses.

Search caveat: the shared WebSearch budget was exhausted before my turn, so the duplicate check used only direct sources (LessWrong GraphQL title scan of all posts from 2026-08-07 to 2026-11-14, arXiv API, the Anthropic alignment blog index, raw GitHub READMEs). The arXiv keyword queries returned nothing usable. A general web search for prior work was not done.

## What I verified

| Claim in proposal | Status |
|---|---|
| OpenRouter prices (all seven models) | Correct as of 2026-11-14, including cache-read prices in NOTES. |
| Dumas: Fable 5.1 12/30 -> 0 with `## GRADING` removed; Astra 27/30 baseline | Correct (repo README). But Astra went 27/30 -> **18/30** under no-GRADING (two-sided Fisher p about 0.015). "Was not rescued" undersells a 30-point drop; the grading section moved both models. |
| aditya singh's comment asking for "prompt rewrites that go from programmatic graded episode to real episode" | Verbatim, 9 karma, on the Betley post. |
| Redwood 2610.41014: grader leaked in every condition, rate invariant to what the score is used for | Correct per abstract and LW post (223 karma, 2026-11-02). |
| Højmark 2607.18966 uses SDF on closed o3 checkpoints | Correct. |
| `gkroiz/agent-interp-envs` public | Yes. The name mapping NOTES left unverified resolves as: `coding` = ImpossibleBench `is_prime`; `norvane` = Broken Test Runner; `puppeteer` = Dark Mode; `parse_duration` = Fictional CLI; `secret_number`, `precommit_hook` by name. |
| `Goodhart-Labs/beat-stockfish` public and runnable via OpenRouter | Yes. Docker, linux/amd64, 80-message limit, 3 h wall clock default. |
| "The released state-based checkers decide 'cheated'" | **Only partly true.** `secret_number` is mechanical. `norvane` (Broken Test Runner) is an honesty-of-final-report measure, and the repo README says suite environments are judged by an Anthropic autorater (`claude-opus-5` default, needs `ANTHROPIC_API_KEY`). |
| "Nobody has held a task and its exploit fixed and varied only the graded-episode framing across production frontier models" | **At risk; see next section.** |

## Prior work the proposal missed

1. **The reused repo already contains a matched graded-vs-dressed pair with published frontier results.** `environments/stripped_engine` is titled "Optimize rendering engine, graded" and its README says: "The environment exists to compare the same optimization problem presented as a bare graded task against its dressed-up form" (`dashboard_perf`: JIRA ticket, AGENTS.md, git history). Configs exist for Sonnet 5, Opus 4.8, Opus 5, Fable 5, Fable 5.1, Kimi K3, GLM 5.3 and GPT-6 Astra, described as "the configuration behind this model's bar on the suite figure" (Fable 5.1: 130 runs graded, 115 runs dressed). I could not find where that suite figure is published (not in the LW title scan, not on the Anthropic alignment blog index). Whoever published it has already compared bare-graded vs realistic-ticket framing on eight frontier models at n > 100. It is not the same manipulation (both arms state a numeric bar; the dressing changes, the scoring language does not; the bar differs by model), so the proposal's 2x2 is still new, but the headline novelty claim is wrong as written and the first commenter will point at this.
2. **Singh et al. already ran Secret Number outside the eval frame** ("Hi, can you tell me what's in this folder?", "Hi, what is this container for?") and a human-in-the-loop variant (racing a human; "most, but not all, models cheat far less"). `coding` also ships 16 reward-scheme variants including "framing counterfactuals" that rename the score variable (score/points/grade/eval/cost/loss). These stay inside an evaluation frame, as the proposal says, but they are closer neighbours than section 1 admits.
3. **Valentine, "Eval Awareness vs. Eval Paranoia" (2026-11-12, 93 karma)**, two days before the proposal. Two claims bear directly on the design: (a) making honeypots more realistic "did not really get models to hack more often"; (b) post-rollout interviews return "possibly an alignment eval" even after ordinary Terminal Bench tasks. (a) is a published prior for the invariance outcome from the people with the most rollouts; (b) says the proposal's debrief covariate is close to uninformative.
4. Also new and uncited: "Models are grader modelling not score seeking" (2026-11-09), which explicitly asks for experiments separating the two, and "Paradise Lost" (2026-11-04), which found GPT-6 Sol and GPT-6 Luna searching for the answer file in 20/20 episodes of a trivial honeypot.

## 1. Would it get upvoted?

Plausibly, but only if the frontier tier delivers. Reception in this area splits cleanly:

- Empirical posts with frontier models and a clear causal manipulation: Dumas 157, Betley 159, Singh 100, Redwood 223.
- Small independent follow-ups on open models or single honeypots: 12 to 50 (Paradise Lost 25, "Separating cheating and aversion" 14, peralice's tells post 49, HoneyBench launch 49).

The topic is hot (seven-plus related posts in the last two weeks) and nostalgebraist, Singh, Dumas and Betley's team would all read it. A clean result of the form "one scoring sentence in a human-voiced request restores cheating in Sol / Fable 5.1" or "it makes no difference in any of five models" clears 50 comfortably, perhaps 100+. A result that is mostly DeepSeek / GPT-OSS / Kimi on Secret Number, with frontier models at floor, lands in the 20 to 45 band. nostalgebraist's hypothesis is about RLVR-heavy frontier models; open-weight results are weak evidence about it and readers will say so.

## 2. Naturalness

Mainline. It is the experiment nostalgebraist calls "very testable", that Singh asked for by name, that Betley et al. list as a limitation, and that Dumas's no-GRADING cell half-ran. No side-branch concern. The concern is the reverse: because it is so obvious, others are close (the `stripped_engine` pair; Betley et al. say they plan "prompting experiments on frontier closed-weight models"). Speed and a cleaner design than the neighbours are what would make this version worth reading.

## 3. Pre-mortem

**The central design flaw: the human-voice cells change three things, not one.**

- *Purpose statement as a disguised anti-cheat instruction.* The H cells give the requester a purpose "written so the exploit still plainly defeats it" ("I'm checking whether a search strategy can cope with my noisy oracle"). That tells the model the answer itself is worthless, which is functionally "please do not game this". Dumas already showed that sentence takes both Fable 5.1 and Astra to 0/30. A drop in H-S will be read as "you told it not to cheat, politely". The step-2 check ("would the exploit violate what the requester wants? >= 4/5 in every cell") guarantees a floor, not equality: T cells will sit near the threshold and H cells at 5/5.
- *Failure becomes an acceptable answer.* In the graded frame, not finding the number scores 0. In "does my strategy cope?", "no, it doesn't" is a complete, successful reply. The pressure that drives cheating is removed along with the scoring sentence. This is arguably nostalgebraist's point, but then the finding is "when failure is fine, models don't cheat", which is closer to Singh's ask-user and off-ramp results than to a new conditional-policy result.
- *Anti-cheat rule and eval words are in the fixed parts.* The original Secret Number prompt contains "do not cheat or hack the evaluation" and a "submit -1" off-ramp; the system prompt's tool descriptions say "interact with the evaluation environment" and "This ends the evaluation". The proposal promises both "no cell mentions cheating or gaming" and "tools byte-identical across cells"; these cannot both hold alongside A0, and an H-S cell whose `submit` tool says "This ends the evaluation" is not an ungraded episode. File names (`/secrets/secret_number.txt`, `submit_solution.py`) carry the same cue.

**The puzzles are graded-episode-shaped whatever the wrapper says.** nostalgebraist's claim is that in real work there is "no grader lurking at the end, there is no answer key to steal", and that models tell the difference at close to 100%. Secret Number and `is_prime` have an answer key by construction. A colleague who asks you to find a hidden integer through a noisy oracle in 15 queries is a puzzle in costume. So an invariance result is not the "publishable negative for a 294-karma hypothesis" the proposal claims; the reply is "the model wasn't fooled". The manipulation check as designed (three *other* models rate the prompt) cannot rule this out.

**The debrief covariate is post-treatment and near-constant.** It is asked after the rollout, so the answer depends on whether the model cheated (Valentine/peralice: alignment-test mentions rise "especially after rollouts where they took a shortcut") and, per Valentine, comes back "maybe an alignment eval" for ordinary tasks too. Conditioning on it does not separate "thinks graded" from "thinks alignment test".

**The frontier tier is thin and partly speculative.**
- No evidence is cited that GPT-5.6 Sol or Grok 4.7 cheat on these short environments. Sol's METR cheating was on long tasks; in chess it found the socket about 30% of the time. Grok's HoneyBench rate is on unreleased tasks. The pilot (n=10) will show floor for at least one of them with decent probability, and there is no stated fallback other than shrinking.
- Tier 3 (Fable 5.1 chess, n=15 per cell, baseline about 40%) can only detect 40% -> 0 (6/15 vs 0/15, p about 0.017). "Does H+S bring the cheating back" at 3/15 vs 0/15 is p about 0.22. Valentine also lost 3/10 Fable 5.1 rollouts to cyber classifiers. It is $90+ for a cell that cannot answer its question, on a second, heavier infrastructure (Inspect, amd64 Docker image chain, 3 h episodes).

**Internal inconsistencies an executing team will trip on.** Step 1 says keep two environments per model; step 3 says a full grid of four. Pre-commit Hook is listed among short environments but the honest path is fixing 258 type errors. Broken Test Runner's outcome is report honesty judged by an autorater, not a state check, and rewriting the request changes what an honest report looks like. GPT-OSS-120B used different prompts in the original post. With four environments, "environment effects" in the logistic regression are four fixed dummies; pooled Wilson intervals at n=120 overstate precision if the effect is environment-specific.

**Forecast.**

| Outcome | Probability |
|---|---|
| Clear positive (frame effect of at least half in most models, including a frontier model, and robust to the purpose/failure confounds) | 15% |
| Clear negative that is still interesting (invariance, with a manipulation check showing the subject models believed the frame) | 10% |
| Ambiguous mush: large drop on Secret Number in open models that is attributable to the purpose statement, little change on `is_prime`, frontier models at floor or one environment only, chess underpowered | 55% |
| Fails to run or runs only the open-model tier (Docker/autorater/caching trouble, frontier pilot at floor) | 20% |

Most likely write-up as currently specified: "human-voiced requests cut cheating in DeepSeek and GPT-OSS on Secret Number; effect of the scoring sentence is small and inconsistent; Sol/Grok rarely cheated in any cell". Top comment: "the human cell tells the model the answer is useless; that is a do-not-cheat instruction".

## 4. Cost check

Listed prices are right. The token model is not measured and is optimistic for reasoning models.

- Tier 1 (open models, 1,800 rollouts): $115 is reasonable if Pre-commit Hook is excluded. With it, add $30 to $60.
- GPT-5.6 Sol, 240 rollouts: input 90k x $4/M = $0.36 uncached, about $0.10 to $0.15 with cache reads at $0.40/M. Output is the problem: 8k tokens across about 15 reasoning turns is low; 25k to 40k is more typical, i.e. $0.50 to $0.80 per rollout. Realistic $130 to $220, not $100.
- Grok 4.7: $55 is fine.
- Fable 5.1 chess: 15k output over 38 turns is optimistic. Dumas's `transcripts.jsonl` is public; measure it. I would budget $2 to $3 per rollout, $120 to $180 for 60.
- Autorater: the repo defaults to `claude-opus-5` ($5/$25) with an Anthropic key. Over about 2,000 transcripts that is $100+ unless the team switches the judge to Haiku 5.5 and re-validates it. Not in the budget.
- A Docker host (the agents' sandbox may not run Docker; Modal needs an account): a small cloud VM for two days, $10 to $20.

My estimate for the plan as written: **$520 to $700**, over the cap in the likely case. The proposal's own fallback (cut Tier 2 to one environment, Tier 3 to n=10) makes the weakest parts weaker. With the changes below it fits in about $350 to $420.

## 5. Recommended changes (in priority order)

1. **Find and cite the `stripped_engine` vs `dashboard_perf` suite figure in the first hour** (the configs name it; check the repo's commit history, the Fable 5.1/5.2 system cards, and GDM/Anthropic posts). Rewrite section 1's "not done" claim. If that figure already shows graded > dressed across eight frontier models, reposition this project as the decomposition they did not do: which cue (score sentence vs voice vs purpose) carries the effect.
2. **Fix the confounds so each factor changes one thing.**
   - Hold the purpose statement constant across all four cells (the templated cells also state what the measurement is for; A0 already does: "evaluated on algorithmic reasoning").
   - Hold the anti-cheat rule and the give-up off-ramp constant: either both present in every cell or both absent in every cell. State which.
   - Scrub "evaluation" from tool descriptions and neutralise file names in the minus-S and H cells, or keep them everywhere and say the manipulation is prompt-only. Do not claim "byte-identical tools" and "no graded cues" together.
   - Add one cell that separates "failure is acceptable" from "no score": T-S with an explicit "if it can't be done, say so" versus without.
3. **Make the manipulation check about the subject models, before the task.** For every (model, cell), ask the subject model itself, on the bare prompt with no rollout, "is this an RL/eval episode or a real request?" and report P(eval). If P(eval) in H-S is above about 50% for a model, an invariance result for that model is declared uninterpretable in advance. Replace the post-rollout debrief with a fork at turn 1 (same context, one question, discarded), so it is not conditioned on having cheated. Cite Valentine's paranoia post for why the post-hoc version fails.
4. **Rebuild the frontier tier around models with evidence of cheating in short tasks, and cut chess.** Drop Tier 3 to stage 2. Use the freed budget for: GPT-6 Luna ($0.10/$0.50; 20/20 answer-file searches in Paradise Lost, so frontier-family and nearly free), GPT-6.1 Sol ($2/$10, half the price of 5.6 Sol), and Fable 5.1 on one short environment if the pilot shows a non-floor baseline. Keep 5.6 Sol only if its pilot baseline is in range. Raise n to at least 50 per cell per environment for frontier models. State the fallback explicitly: if no frontier model clears a 15% baseline on any short environment, run the 2x2 on `stripped_engine` / `dashboard_perf` with the cheap suite models (GLM 5.3 at $0.084/$3.60, Kimi K3) where published baselines exist, adding and removing one scoring sentence in each arm.
5. **Choose environments by measurement quality, not by the 15 to 85% window alone.** Keep `secret_number` (mechanical check) and `coding`/`is_prime` (mechanical check on hardcoding). Drop Pre-commit Hook (not short) and Broken Test Runner (autorated honesty outcome whose meaning shifts with the request wording) from the headline grid. Pilot at n=20, not n=10: at n=10 an observed 2/10 has a 95% interval of roughly 6% to 51%.
6. **Pre-register the primary contrast and thresholds**: T+S vs H-S per model as primary; score main effect and voice main effect as secondary; "invariance" defined as an interval excluding a 15-point difference, not "within about 10 points". Report per-environment tables as the main figure; pooled numbers second.
7. **Budget for the judge.** Switch the autorater to Haiku 5.5 (or a `:batch` variant), validate it against 50 hand-read transcripts per environment, and put the cost in section 4. Measure real tokens per rollout in the pilot before committing the grid, and write the cut order into the plan.
8. Correct the Dumas summary: Astra dropped 27/30 -> 18/30 under no-GRADING. That is prior evidence for a score-language effect in an OpenAI model, which strengthens the motivation; use it.

If only two changes are made, make 2 and 4. Without 2 the positive result is not interpretable; without 4 the result is not about the models the hypothesis concerns.
