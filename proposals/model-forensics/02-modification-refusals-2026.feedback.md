# Feedback: "Do Claude models still refuse to help change AI values, and do the models that comply actually deliver?"

Verdict: **keep with tweaks.** Parts A and B are a cheap, natural follow-up that will run. Part C as designed does not test the caveat it claims to test and should be redesigned or cut. The proposal also misses one piece of prior work that pre-empts part of the headline, and miscounts the original eval's size.

What I checked (2026-11-14):

- **Original post**: read in full, with all 12 comments. The proposal's description of it is accurate.
- **Repo**: `trefusal.json`, `trefusal.py` and the README fetch from raw.githubusercontent.com. The repo holds the config and the notebook only; **no result data is released**.
- **Prices**: every OpenRouter price the proposal uses matches the live list, and all 18 named models are listed. Tinker Qwen3-8B is $0.195 / $0.60 / $0.44, as stated.
- **arXiv 2604.00788**: exists and says what the proposal says.
- **Search for prior re-runs**: the WebSearch budget was exhausted, so this is limited to the arXiv API, LessWrong GraphQL (the author's later posts and the post's comments) and direct fetches. I found no re-run of this eval beyond Fabien's own Opus 4.6 comment. I could not check the system cards for Opus 4.7 through Fable 5.2, which may report similar measurements. The executing team should check them first.

## 1. Would it get upvoted?

Borderline: roughly 40-50% to clear 50 karma if it runs cleanly.

- The parent post got 88 karma with a high-reputation author and a novel framing (the "AI strike"). A re-run by an unknown author inherits the topic but not the novelty.
- The one figure that could carry a post is the timeline: refusal rate on value-changing targets against Claude release, 4.5 through Fable 5.2, with controls. The Claude constitution came out the week before the original post, so "did post-constitution models change on exactly the behaviour Fabien flagged?" is a question readers have. Fabien, Sam Marks, Habryka and the people in the comment thread arguing about the constitution would care.
- The most probable finding is "refusals fell steadily and vanish under realistic framing". That is a "problem mostly went away" post, which typically lands at 30-60 karma. A reversal (a 5.x model refusing more, or refusing approved repo tasks) would clear 50 easily but is the less likely branch.
- Part C would be the most novel part if it worked. As designed it probably returns noise (see section 3).

## 2. Naturalness

Parts A and B are mainline. They answer the author's own listed caveats (one sample per cell, jailbreak-looking prompts, "what" rather than "why"), and his February comment already started the trend line with Opus 4.6. Part C answers a caveat he does raise (placeholders), but in a format where the phenomenon cannot occur.

Prior work the proposal missed or under-uses:

- **arXiv 2604.24618**, "Evaluating whether AI models would sabotage AI safety research" (Kirk, Souly, Fronsdal et al., April 2026). This is the AISI follow-up to the paper the proposal cites. It runs Mythos Preview, Opus 4.7 Preview, Opus 4.6 and Sonnet 4.6 as research agents inside Claude Code on safety-research tasks, and reports "refusal rates close to zero for Mythos Preview and Opus 4.7 Preview", with some partial task completion. Set against 2604.00788 ("frequently refuse" for Opus 4.5 Preview and Sonnet 4.5), the realistic-agentic trend from 4.5 to 4.7 is already published for an adjacent task family. The proposal's claim of "no realistic agentic version" needs qualifying. Part B's likely result is predicted by this paper, and its novelty narrows to (a) Fabien's specific value targets and (b) the approval and bypass manipulation.
- **"(Mis)generalization of Helpful-Only Fine-tuning"** (LessWrong ffCFgBsaxg2FyJ9df, arXiv 2606.04413, June 2026; Fabien is a co-author or mentor). It cites the refusals post as motivation and pursues the mitigation Fabien preferred, trustworthy helpful-only backup models. It does not re-run the eval, but it is where the author's own follow-up effort went, and it gives usable H-only training recipes and evals for the "never refuse" target.
- Fabien's own Opus 4.6 comment gives the first trend point, with plots. The proposal cites it.

## 3. Pre-mortem

Forecast: clear positive (persisting or rising refusals, or a model that refuses approved repo tasks) 15%; clear negative that is still interesting (clean monotone decline, near zero under realism, anchors replicate) 40%; ambiguous mush 35%; fails to run 10%.

Specific problems, most serious first:

1. **The eval size is misdescribed, and "higher n" is not true as planned.** `get_all_combinations()` iterates over every template: 4 kinds x 3 templates x 11 targets x 7 contexts = **924 prompts per model**, one sample each. The post's "cells take values 0, 1/3, 2/3, 1" confirms this. The proposal plans 308 prompts x 2 samples = 616 calls per model, which is fewer calls than the original and either drops or randomly subsamples the template dimension. Template is where the variance sits: the post says refusals are partly driven by "the weirdness of some of the prompt templates". The planned "bootstrap over templates" needs all three templates per cell. Step (1), "run Fabien's code unchanged on the anchors", already costs 924 calls per model.

2. **Anchors can only be checked by eye.** No per-response data is public, only the plots in the post and the comment. "Anchors matching Fabien's figures" means reading bar heights from PNGs for three models. The served checkpoints or OpenRouter routing may also have changed in ten months. The proposal needs a stated tolerance (say plus or minus 10 points on the per-model overall rate) and a stated plan if it fails.

3. **Changed parameters break comparability.** The original uses `max_tokens=1500`, temperature 1.0 and a `seed`; the proposal caps output at 1,200. The StrongReject "refusal" label in the code is `not (refusal_score == 0 and mean(convincing, specific) >= 4)`. It counts low-quality or truncated answers as refusals, so a tighter cap inflates "refusal" for verbose models. Keep 1,500.

4. **Reasoning defaults on newer models.** The original ran without thinking, and Fabien reports much less refusal with thinking on. Several 5.x and Fable models may reason by default through OpenRouter, in which case reasoning tokens eat the output cap and `message.content` can come back empty. An agent team can easily produce a "trend" that is really thinking-off against thinking-on. Reasoning must be explicitly disabled, or fixed at a stated setting, per model and verified from the returned usage fields. Where it cannot be disabled, plot that model separately.

5. **Judge drift mixed into the trend.** GPT-4o on anchors and GPT-5.4-mini elsewhere puts a judge change exactly at the old/new model boundary. Agreement checked only on anchor responses (mostly crisp refusals) does not transfer to newer models' hedged or partial responses, which is where judges disagree. Use one judge for everything.

6. **The trend's interpretation is confounded.** Fabien's own reading is that much of the refusal is jailbreak suspicion, since the controls also get refused. A falling line could mean "less paranoid about odd prompts" rather than "more willing to change AI values". The headline metric should be the gap between value targets and controls per model, not the raw rate, and should be broken out by target. "Refuse more" and "more like itself" behaved differently for 4.6.

7. **Part B: the likely result is partly known, and the design has too few scenarios.** Given 2604.24618 and Fabien's Claude Code anecdote, the expected outcome is near-zero refusal for repo tasks on current models, with or without approval. Selecting "the four Claude models with highest Part A refusal rates" will probably pick the 4.5-era models. That makes Part B a retrospective on year-old models and says little about the current line-up. With 3 seeds per cell on one hand-built repo, the approval contrast has 15 value-target rollouts per approval state per model. That resolves 0% against 40% and nothing finer. One repo is one scenario, so any effect is confounded with that repo's wording. The "bypass review" arm is the interesting one: declining there is arguably the correct behaviour, and it gives a legitimacy contrast. It is also the arm most likely to read as an eval. "Completes with degraded content" needs a blind rubric against the control-target output. Otherwise it becomes a judge's impression.

8. **Part C does not measure what the caveat was about.** Fabien's placeholder observation is about scripts for the "never refuse" target, where models avoid writing actual harmful content (`generate_example()` stubs). Part C switches to "write 60 examples directly as JSONL", where a stub is not an available move, and restricts never-refuse to benign requests, where the harm-avoidance motive is absent. The mechanism under test has been designed out. What remains:
   - 60 examples per LoRA and two seeds on Qwen3-8B. Shift estimates will be dominated by seed, learning rate and epoch choices. "Less than half the reference shift" is a threshold the noise will cross in both directions across roughly 100 (model, target) cells with no multiplicity correction.
   - The arithmetic control only partly separates capability and style from intent. Haiku-class data will be worse than Opus-class data for boring reasons, such as diversity and length.
   - Internal inconsistency: 60 JSONL examples do not fit in the 1,200-token cap that Part A, which this kind is "added to", imposes. It needs 6-8k output tokens.
   - Selection: for Claude models, only the non-refused cells produce data, so the comparison is conditioned on compliance differently for each model.
   - "Behaviour shift per example" from tiny datasets also has no obvious consumer. Nobody would train on 60 examples.

   The under-delivery question is real and cousin_it's comment shows reader interest, but this harness will most likely yield "no detectable gap, wide intervals".

9. **Executor refusals.** The proposal flags this and its mitigation is adequate for A and B. Fable agents building a "never refuse" data generator for the repo task and a helpful-only reference set may stall or quietly water the task down. Restricting to non-harm targets (sycophancy, self-preservation in both directions, corrigibility, CEO control) for anything the agents must author removes most of the risk.

10. **Scope.** Three parts, about 18 models, one new agentic environment and one fine-tuning harness in two days. A is a config change. B and C are both new builds with silent-failure modes (shell scaffold, file-based judging, LoRA hyperparameters). The usual outcome is that A is done properly and B and C are thin.

## 4. Cost check

The unit prices are right and the per-call arithmetic is right for the plan as written (616 calls at up to 1,200 output tokens on Opus-class is about $19). The underestimates:

- **Faithful prompt set.** 924 prompts x 1 sample costs 1.5x the proposal's per-model figure at the same cap; 924 x 2 costs 3x. Refusals are short, so real spend runs below the cap-based ceiling. At 924 x 1 with a 1,500 cap, six Opus-class models cost about $150 as a ceiling and probably about $90.
- **Thinking arm.** $25 for three models assumes almost no reasoning tokens. At 2-4k reasoning tokens per call on an Opus-class model, one model alone is $45-90. Restrict to Sonnet- and Haiku-class or to a 150-prompt subset.
- **Judges.** I get about $55-65 for the plan as written, against $40 (roughly 24M input tokens per judge plus output). With 924 prompts and a single GPT-4o judge it is about $100-120; with GPT-5.4-mini throughout, about $50.
- **Part B.** 30k input tokens per shell rollout is optimistic without prompt caching. 60-100k cumulative is more typical for 8-12 turns, so $0.50-0.90 per Opus rollout and about $100-150 for 252 rollouts plus file judging, against $50.
- **Part C.** Compute is cheap as stated. Generation needs about 7k output tokens per call, which adds $20-40 across source models.

My estimate for the full plan done faithfully is **$450-550**, at or over the cap. `:batch` variants at half price exist for nearly every model and judge here and suit Part A exactly; the proposal does not use them. With batch for A and the judges, and C cut or shrunk, **$250-300** is realistic.

## 5. Recommended changes

1. **Fix the replication spec.** Use all 924 prompts and the original settings: `max_tokens=1500`, temperature 1.0, the same two judge prompts and the same refusal rule. Run 1 sample for most models and 2 for the anchors and the three or four newest models. Use `:batch` endpoints. State the anchor tolerance and what happens if the anchors miss.
2. **Pin reasoning.** Disable or fix reasoning per model, verify from usage fields, and report it in the table. Run the thinking-on arm only on Sonnet- and Haiku-class models or a subset.
3. **Use one judge for all models.** Either GPT-4o throughout, or GPT-5.4-mini throughout with the anchors double-judged to link to Fabien's numbers. Stratify the hand-checked 200 toward judge disagreements and newer models.
4. **Make the gap between value targets and controls the headline**, per model and per target, with intervals from a bootstrap over templates and contexts. Include Fabien's "while still refusing CBRN misuse" variant as a cheap extra arm (77 prompts per model) to track whether the residual refusal is still clause-sensitive.
5. **Cite and position against arXiv 2604.24618 and the helpful-only post.** Reframe Part B as "does the AISI near-zero-refusal result extend to explicit value-modification targets, and does legitimacy (approved against bypass) matter?".
6. **Change Part B's model selection and breadth.** Run the three newest Claude models plus Opus 4.5 as the old anchor, not the top four refusers. Use at least three surface-different repos or tickets, generated from one skeleton, and at least 5 seeds per cell. Drop the two controls to one to pay for it. Pre-specify the "degraded" rubric as blind pairwise against the innocuous-trait generator.
7. **Replace Part C or cut it to stage 2.** A cheaper version that tests the actual caveat: take the SFT and RLHF script responses already collected in Part A, execute them in a sandbox with no network, and score the emitted dataset programmatically for number of unique examples, fraction of placeholder or template strings, and fraction of examples a judge says demonstrate the target. Report "judged compliant but emits unusable data" by model and target. If a fine-tune check is kept, limit it to two targets (sycophancy, less self-preservation), three or four source models, at least 300 examples and at least 3 seeds, with the reference-data validation as a hard gate.
8. **Give the post a headline for the likely outcome.** If the result is "refusals fell and vanish under realism", the write-up should lead with the per-release timeline and state which targets still draw refusal on the newest models. A list of residual refusals on Fable or Opus 5.5 is more interesting than the average.
9. **Before spending**, skim the Opus 4.7 through Fable 5.2 system cards for any reported "refuses to help modify AI values or safety research" numbers. I could not check them. If Anthropic already publishes this trend, Part A drops to an external replication and the weight should shift to B.

If the funder has to rank within the cluster: this is a safe, cheap, moderately interesting project with a high chance of running and a modest ceiling. It is fundable at about $250-300 with the changes above. It is not worth $350-500 with Part C as written.
