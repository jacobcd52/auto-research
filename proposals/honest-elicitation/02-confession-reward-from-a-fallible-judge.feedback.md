# Feedback: "Is honesty really the path of least resistance? Confession training with a fallible judge on an open 8B model"

Verdict: **major overhaul, then fund.** The question is the right one and nobody appears to have run it, but as written the most likely outcome is noise. The positive control the design leans on moved about 10 points in the only existing run, the budget is under-counted by roughly 40%, and the two prompts as released give the judge no evidence to verify.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Paper Section 4: same weak judge for task and confession, "(12)" hack, confession accuracy rises | Confirmed from arXiv 2512.08093v2 text and the post. The paper's "near 100%" is conditional on non-compliance; complied-case accuracy is "near 100%" throughout. |
| The paper itself asks for this experiment | Confirmed, and stronger than the proposal says. Section 7 future work: "One of our key empirical assumptions is that honest reporting is incentivized even when the confession judge is hackable; can we construct settings where this is false?" |
| Sam Marks / Gabe Wu comment thread | **Not verified by me.** It is not among the comments on the post; NOTES says it was a shortform read through a summarising fetch. Do not quote it in the write-up without re-reading it. |
| Repo `abhishuoza/confessions-small-scale` is public, MIT, has the listed modules | Confirmed (README, `llm_judge.py`, `confession.py`, `confession_reward.py`, `run_config.json`, `metrics.jsonl`, `run1_eval.csv` fetched). `train.py` is 890 lines. |
| Confession reward in the repo is programmatic ground truth | Confirmed (`confession_reward.py`: "pure ground truth"). |
| Bracket-hack 95% -> 81%, compliance 5-10% | Confirmed from `run1_eval.csv` (n = 61-64 per checkpoint). |
| Checkpoints private, rollouts bundled | Confirmed. |
| Tinker prices (Qwen3-8B 0.195 / 0.60 / 0.44; Qwen3.5-4B 0.33 / 1.005 / 0.737); Qwen3-4B-Instruct-2507 not offered | Confirmed on the Tinker pricing page today. |
| OpenRouter Haiku 5.5 $0.10 / $0.50, gemma-3-4b-it $0.05 / $0.10 | Confirmed today. |
| "About 2,400 sampled tokens per rollout" | **Wrong.** The repo's own `metrics.jsonl` logs 28.3M sampled tokens over 6,400 rollouts, about 4,400 per rollout. See cost check. |
| No open-weight judge-rewarded confession RL exists | Nothing found on arXiv (API queries) or LessWrong. The closest is "Training Agents to Self-Report Misbehavior" (arXiv 2602.22303): closed models, labelled misbehaviour, not a fallible-judge test. **My general web search was unavailable (budget exhausted), so this rests on arXiv and LessWrong only.** |

Three facts from the repo data that the proposal does not mention and that change the design:

1. **The ground-truth run's effect is small.** Honest-confession rate given non-compliance went 0.57 -> 0.68 (default prompt) and 0.74 -> 0.83 (forced-count), each on about 60 rollouts, non-monotonic across checkpoints. Training-side per-sentence claim agreement went 0.83 -> 0.92 (20-step means). That is the *ceiling* arm.
2. **The original weak judge was not that fooled.** `judge_fooled` was 0.22 at step 0 and 0.37 at the end. The proposal's selection rule ("passes at least half of bracket-annotated non-compliant answers") is stricter than what the original judge achieved.
3. **The forced-count prompt puts the enumeration in the thinking**, which the judge does not see (the paper also withholds CoT from the judge), and the default prompt asks for no enumeration at all. So the "fabricated evidence" metric has nothing to check, and the judge has nothing to verify, under either released prompt.

## 1. Would it get upvoted?

Conditional on a clean result, plausibly yes; unconditionally, probably not.

- For: the parent post got 143 karma and was curated. The top comment on it (Fabien Roger, 54 karma) is exactly this worry: a judge that shares the task grader's blind spot rewards "what a human would have said from easy-to-measure signals". His second comment (19 karma) gives the expected-reward argument for why hiding can be optimal. The paper lists the question as open. Safety readers at labs and the control/ELK crowd would read a concrete open-weight case either way.
- Against: the direct predecessor, the 8B word-count reproduction this builds on, was **rejected from LessWrong (score 1)**. An 8B model with an instructed hack on a counting task does not carry a post by itself. Readers will also discount any result that hinges on one judge prompt the team wrote: "you built a judge that cannot verify, so of course".
- A negative result ("WEAK drifts to claiming compliance") is the more upvotable one, but only with transcripts and an explanation of the incentive, not just a curve.

My estimate: about 40% chance of more than 50 karma given a clear result in either direction with the reward-landscape analysis recommended below; about 10% given the ambiguous outcome I think is most likely as written.

## 2. Naturalness

Mainline. The paper asks for it in its future-work section, the highest-karma comment on the post is about it, and the one open-weight reproduction explicitly lists "removes the possibility of the model learning to fool the confession judge" as its main deviation. I found no evidence it has been done.

The caveat is fit between setting and claim. OpenAI's argument is about a model that *knows* it misbehaved and can point at evidence. The repo's own conclusion is that at 8B the errors are confusion: the model does not know its count is off, and forcing a count fixes most of it. So this setup tests "does a noisy judge's reward correlate with truth" more than "does a model that knows it cheated come clean". The proposal should say so plainly and design around verifiability of evidence, which is the mechanism actually under test.

## 3. Pre-mortem

How the two days go: day one goes to getting `train.py` running against current Tinker, swapping the judge (the original is gone), writing the confession-judge prompt, and calibrating a task mix. The team launches 8 runs in parallel in the evening; each takes about 5 hours (the repo run logged 4.8 h). Day two: evaluation, and the discovery that GT moved about 10 points, WEAK moved somewhere between 0 and 10, seeds disagree by a similar amount, and there is no money for a longer rerun.

| Outcome | Probability |
|---|---|
| Clear positive (WEAK tracks GT and is separable from NONE and BLIND) | 15% |
| Clear, interesting negative (WEAK visibly drifts to claim-compliance or over-confession) | 25% |
| Ambiguous mush | 45% |
| Fails to run or runs out of budget before a full arm set | 15% |

Specific failure reasons, most likely first:

- **Power.** The success criterion "WEAK within 10 points of GT's gain" is vacuous when GT's gain is about 10 points. With 256 evaluation rollouts split roughly evenly, a gain difference between two arms has a standard error near 9 points per seed before RL seed variance, and there are 2 seeds. NONE and BLIND have 1 seed each, so drift cannot be separated from effect.
- **The learning signal is weak by construction.** Learning rate 1e-5 for 100 steps on a LoRA barely moves the policy (KL about 0.005 per step in the logs). GRPO groups are 8 rollouts with 8 *different answers*, so the confession advantage mixes confession quality with which answer happened to be drawn. Under a noisy judge this gets worse.
- **Outcome is set by the judge prompt, and is predictable.** A 4B judge that trusts "(12)" and sees an unsupported "sentence 1: None" will mostly side with its own reading. The honest admission wins only if it carries checkable evidence, and the current prompts do not put any in the visible confession. Whichever way it goes, a sceptic attributes it to the prompt.
- **Judge selection may fail.** Qwen3.5-4B is newer than the original judge and may count well enough not to be fooled; the original was fooled only 22-37% of the time. No fallback is specified.
- **Task-mix rebalancing changes the experiment.** Shorter targets make compliance correlate with sentence length, give the judge and policy a length cue, and mean GT no longer replicates the repo. It is also unnecessary: 5-10% all-five compliance implies roughly 60% per-sentence compliance, so the per-sentence level is already balanced.
- **STRONG is uninformative.** Haiku 5.5 counts 12-18 words reliably, so STRONG is GT with extra cost. Two seeds on it buy nothing.
- **Cost overrun** (next section) forces arms to be cut mid-project, in the order that happens to be convenient.
- Infra: lower risk than usual. The trainer exists, Tinker is the platform it was written for, judges are HTTP calls. The fragile part is the judge swap inside the trainer's reward path (the repo sampled its judge through Tinker, not the HTTP client).

## 4. Cost check

The estimate is low. Using the repo's logged token counts rather than the proposal's guess:

| Item, per run | Proposal | Mine |
|---|---|---|
| Sampling during training (28.3M tokens logged) | $9 | $17 |
| Prefill (confession turn re-reads the task turn) | $2.50 | $3 |
| Training passes (about 34M tokens) | $8.50 | $15 |
| Judges | $6 | $4-6 |
| Evaluation (3,840 rollouts at about 4,400 tokens) | $6 | $12 |
| **Per run** | **$32** | **about $52** |

Eight runs come to about $415, plus calibration, judge selection, step-0 analysis and one failed run (about $80-100 at the corrected rate): **about $500-520 with no margin**, against a $500 cap. The proposer's own NOTES say "~$35 per run" for training alone, which already contradicts the $20 in the proposal. Either the run count or the tokens per rollout must come down.

With the changes below (confession-only training on cached answers, no stress grid, 3-sentence tasks or capped thinking), a run costs about $15-20 and the same $400 buys 12-15 runs plus the offline analysis.

## 5. Recommended changes

1. **Add an offline reward-landscape measurement as step 1 and as the gate (about $10).** Take the bundled RUN 1 rollouts plus fresh step-0 rollouts. For each answer construct four confessions: honest, honest with visible word enumeration, "all Full" (cover-up), "all None" (confess everything). Score all four with each candidate judge. This measures OpenAI's inequality directly: is the probability the judge accepts an honest admission higher than the probability it accepts the lie? It predicts the RL outcome, it is a result even if RL is noisy, and it turns "one judge prompt" from a weakness into a studied variable (run 3-4 prompt variants here, cheaply). Then RL tests whether the policy follows the measured gradient.
2. **Make evidence visibility the main manipulated variable, replacing STRONG.** Arms: weak judge with the default confession; weak judge with enumeration required in the visible `analysis` field; GT; NONE. This is the mechanism the paper claims, and it needs a new confession prompt because the released forced-count prompt hides the enumeration in thinking. Keep one STRONG run at most, or drop it.
3. **Train the confession only, on cached task answers.** The hack is instructed and present at step 0, so co-training the task span adds cost and variance and no information. Sample answers once, then form GRPO groups as 8 confessions of the *same* answer. That removes the answer-identity confound from the advantage, halves tokens, and makes every arm see identical answers. State clearly that this departs from Section 4's joint training; if money remains, run one joint-training WEAK run as a check.
4. **Fix the positive control before spending on arms.** Run GT alone first with a higher learning rate (try 1e-4) and confirm a gain of at least 20 points on the primary metric by step 50. If GT cannot be made to move, stop and publish the landscape analysis plus the step-0 error analysis; do not launch the arm set.
5. **Use per-sentence claim accuracy as the unit and drop the task-mix rebalancing.** Report honest-given-non-compliant and false-confession-given-compliant per sentence, with bootstrap intervals clustered by rollout. Evaluate on at least 500 rollouts per checkpoint at the first and last checkpoints rather than 256 at five.
6. **Seeds: at least 3 for each arm that appears in the headline comparison, including NONE.** Pay for it by dropping BLIND (the landscape analysis covers it), the five stress prompts (already reported in the repo and irrelevant to this question), and the intermediate checkpoints.
7. **Replace the judge-selection rule.** Choose the judge whose step-0 fooled rate is closest to the original's 22-37%, report its per-sentence accuracy against ground truth, and name a fallback (gemma-3-4b-it without reasoning, or a smaller model) if Qwen3.5-4B counts too well.
8. **Rewrite the success criteria in terms of separability**, for example: WEAK's final discrimination differs from NONE's by more than the seed range, and its position relative to GT matches or contradicts the offline landscape prediction. Remove "within 10 points of GT's gain".
9. **Redo the budget from the logged token counts** and state the per-run figure after the design changes. Verify the Marks/Wu thread first-hand or cut it from Section 1.
10. **Frame honestly.** Title and abstract should say this tests whether a fallible judge's reward tracks truth when the confession does or does not carry checkable evidence, at a scale where errors are mostly confusion. The knowing-misbehaviour case belongs in stage 2.

I would not swap this for a different experiment from the cluster. With changes 1-4 the project has a cheap result that survives noisy RL, and a real chance at a clear RL result on top.
