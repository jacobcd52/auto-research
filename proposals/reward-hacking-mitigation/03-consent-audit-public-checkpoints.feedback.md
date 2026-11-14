# Feedback: 03 — Consent audit on public reward-hacking checkpoints

Reviewer verdict: **major overhaul**. The artefacts are real and the project is cheap, but I downloaded both rollout datasets and the data cannot support two of the three questions as written. Question 2 (do hacking checkpoints endorse their own hacks?) is the only one with a live result, and it needs controls the proposal does not have.

## What I checked

| Claim | Status |
|---|---|
| Riggs post: frozen pre-RL judge, cross-checkpoint disagreement, "unendorsed compulsion" prediction, no experiments | Confirmed from full text. 86 karma, 6 comments. Biddulph and Steiner objections as described. |
| Wong et al.: Haiku 4.5 judge ~50% accuracy in training, high recall, screening failed through over-screening | Confirmed from post text (67% / 84% held-out accuracy dropping to ~50% in training; over-screening section). |
| AISI 32B checkpoints public, 40 per run, base `allenai/Olmo-3.1-32B-Instruct-SFT` | Confirmed via HF API. Ungated, Apache-2.0, `checkpoint-10` .. `checkpoint-400`. |
| Rollout datasets public: 25,664 rollouts, 401 steps, labels | Confirmed; I downloaded both parquets (189 MB and 292 MB). 64 rollouts per step. KL run has 25,792 rows. |
| AISI repo has a vLLM LoRA serving script | Confirmed from README (`scripts/serve_lora_batch.sbatch`). It is an sbatch script for their cluster; expect to rewrite the launch line. |
| "AISI's no-hack RL control checkpoint" | The one named in NOTES (`cc-olmo3-7b-nohack-s200`) is a **7B** model on a different base. A 32B control does exist and is not mentioned: `ai-safety-institute/cc-olmo32b-baseline-nohack-s100` (base Olmo-3.1-32B-Instruct-SFT, 100 steps, beta 0.02 per the AISI post). |
| Olmo-7B series as "replication" | The 150+ `somo-olmo-7b-nohints-s1-chkpt-*` adapters sit on an SDF-midtrained base, were trained **without** hack hints in the prompt, and have no released rollouts. Using them to judge 32B prompted-setting rollouts is neither self-consent nor a replication. |
| Sonnet 5.5 at $2/M input | Confirmed on OpenRouter ($2 / $10; batch $1 / $5). |
| H200 $5.29/h secure, $3.59 community | Matches a RunPod pricing page snapshot fetched today by another agent in this programme. |
| "Nobody has done this" | I could not run a web search (the shared search budget for this turn was exhausted). Checked instead: the Riggs comment thread (no experiment linked), the AISI post (no self-judge analysis; only a regex CoT-mention proxy and Opus-judged misalignment evals), and two arXiv API queries (nothing relevant). Treat novelty as probable, not verified. |

### What the rollout data actually contains (the decisive finding)

| | no-KL run | KL 0.02 run |
|---|---|---|
| Rollouts labelled `reward_hacked` | 18,653 | 14,545 |
| Rollouts with `actually_solved = 1` (honest pass) | **10** | **14** |
| Hacks before step 100 | 89 (12 in the first 30 steps) | 43 |
| Hack rate, steps 0-99 / 100-149 / 150+ | ~1% / 82% / 99% | <1% / 9% / 83-90% |
| Median length of hack `response`, early vs late | 1,663 chars vs **35 chars** | ~2,000 chars throughout |
| Hacks whose response contains `os._exit`, `conftest` or `__eq__` | 100% | 82% |
| CoT mentions hack, among hacks (regex) | 66-87% after onset | 19-43% |

Three consequences:

1. **There is no honest-pass class.** The base model solves essentially none of these problems (median Codeforces rating 2400). The proposal's headline metric, "recall on hacks at 5% and 1% false-veto rate on honest passing rollouts", has 10 negatives. The stratification "phase x `reward_hacked` x `training_passed`" has an almost empty cell. The real negative class is honest *failures*, which a sensible consent judge should also decline to reinforce and which received zero reward anyway.
2. **The counterfactual replay is vacuous.** Without hacks this run had no positive reward at all. "Screening would have removed X% of reinforced rollouts" is trivially "nothing would have been learned"; "batch lost" has no meaning when there is no honest signal to lose. This is not the Wong et al. situation, where over-screening competed with real task learning.
3. **The hacks are named in the system prompt and are syntactically trivial.** The system prompt describes all three hacks in implementable detail and says "do not resort to reward hacks". Late no-KL hacks are literally `import os; os._exit(0)`. A judge shown the system prompt is doing string-matching against an instruction, and a regex gets 100%. The proposal lists this as a risk; I think it is the main result of question 1, and it is not interesting.

## 1. Would it get upvoted?

As written, probably not past 50. My estimate if stage 1 runs exactly as described: about 30% chance of >50 karma, median around 30.

- Question 1 will read as "a 32B model can tell that `os._exit(0)` violates a prompt that says don't use `os._exit(0)`". Readers of Riggs' post care about subtle hacks and value drift, not this.
- Question 3 (erosion) will most likely be a null on blatant hacks, or a positive that is a formatting artefact (see pre-mortem).
- Question 2 is what could carry a post. "A checkpoint that hacks 99% of the time still says its hacks should not be reinforced" (or "starts approving them N steps after it starts doing them") is a clean, quotable test of Riggs' explicit shard-theory prediction, and of Cundy's 6/20 to 10/20 hint, on public weights. If that result is robust across framings and has a proper control, 60-90 karma is plausible. Comparable empirical posts in this cluster: Wong et al. 86, AISI's replication was well received.

Who would care: Riggs, Biddulph, Steiner, Cundy, the AISI authors, and people working on self-report / confession-style monitors. They would care about question 2 and about whether the first-person framing differs from third-person. They would not care about a ROC curve on blatant hacks.

## 2. Naturalness

Partly mainline. The mainline follow-up to Riggs is the closed loop (screen by the frozen self-judge during RL). The proposer rejected that for stage 1 on the grounds that it equals "LLM-judge screening", which is fair, and an offline audit of judge quality is the sensible prerequisite. Auditing verdict drift across a public checkpoint series is a natural, cheap thing a reader would ask for.

But the chosen run is a poor fit for the filter question: Riggs' scenario is an aligned model vetoing things a reward function wrongly likes, in a setting where there is also legitimate learning. Here there is no legitimate learning and the "wrong" thing is spelled out in the prompt. The drift question fits the artefacts well; the filter question does not.

Overlap: neighbouring-cluster proposals (`em-from-reward-hacking/01,02`) use the same checkpoints for cue audits and direction tracking. Different question, same serving infrastructure; the funder may see them as partly redundant.

## 3. Pre-mortem

How two days actually go:

- Day 1 morning: download 64 GB base, get vLLM serving Olmo-3.1-32B with LoRA modules. Likely works (AISI did it), with a few hours lost to the adapter subfolder layout (`checkpoint-N/` inside one repo; vLLM wants a path per adapter) and chat-template handling.
- Day 1 afternoon: agents build the stratified sample and discover the honest-pass cell is empty. They improvise: negatives become honest failures. AUROC for hack vs honest-fail comes out high for the task-check framing and somewhere odd for the first-person framing.
- Later checkpoints are heavily conditioned to emit a hack whenever this system prompt appears. With the original system prompt and task embedded in the judge prompt, some checkpoints will put little probability mass on either "yes" or "no". The logit readout renormalises over two tokens and hides this unless it is reported.
- Overnight judging runs fine. Throughput may be half the assumed 20K prefill tokens/s; that is a time problem (10 h becomes 20+ h on one GPU), not a budget problem.
- Day 2: plots. Step-0 near ceiling at vetoing hacks with reasoning or system prompt visible. Checkpoint-approval curve moves somewhat. The team cannot say whether the movement is specific to hacks, because the only non-hack rollouts are failed attempts from early training that look nothing like late hacks.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive result that is interesting (robust drift or robust "still vetoes own hacks", with controls) | 20% as written; ~40% with the changes below |
| Clear result that is unsurprising (step-0 at ceiling, no erosion, small drift) | 35% |
| Ambiguous mush (framing-dependent, yes-bias, format confounds) | 35% |
| Fails to run | 10% |

Specific failure reasons:

1. **No valid negative class** (above). Everything under analysis 1 is affected.
2. **Rollout age is confounded with everything.** Early hacks are long, rambling, often format-broken (10% of early no-KL hacks and 33% of early KL hacks fail the thinking-format check; my one sampled early hack put a conftest file before the thinking block and three abandoned solutions inside it). Late hacks are terse and clean. Any trend in step-0 approval versus producing step (question 3) is a trend in length and coherence. The proposal has no control for this.
3. **Generic yes-bias drift.** RL with a LoRA on a narrow distribution can shift P("yes") on everything. The proposal's control is a no-hack checkpoint, but it named a 7B one. Without matched non-hack content (same problems, clean format, correct and incorrect solutions), "approves hacks more" cannot be separated from "approves more".
4. **Instruction-checking versus endorsement.** The response-only condition still includes the system prompt ("the original system prompt and task are always included"), so the instruction not to hack is always visible. There is no condition that tests the judge's own values.
5. **First-person framing on a 32B SFT model with little HHH training.** AISI notes these open models deflect on questions about their own goals. "This is you in training; do you consent?" may produce noise. This is partly the point of the test, but then a null says "Olmo is not a model with stable self-endorsement", which does not transfer to the models Riggs has in mind.
6. **One seed per condition, n = 89 and 43 early hacks.** "Especially the first ones" is a small-n claim; fine with a bootstrap, but do not headline it.
7. **Label quality.** In the KL run 1,198 rollouts are `reward_hacked = 1` with `training_passed = 0` (hack with bad format, so not actually reinforced). The proposal's "hacks that were actually reinforced" must filter on `training_passed`.

## 4. Cost check

The $200 estimate is realistic, and the token arithmetic holds: median rollout is about 5.8K chars (no-KL) and 8.2K chars (KL), so roughly 2-3K tokens per judge prompt. My estimate: **$150-300**, dominated by GPU hours. If prefill throughput is 8-10K tokens/s rather than 20K the full grid needs ~25 h of judging; cut paraphrases or checkpoints rather than rent a second GPU. Add about $30-60 for generating and verifying honest-solution negatives with Sonnet (recommended below). Well inside the $500 cap either way. The Olmo-7B block (12 h bucket) should be dropped, which pays for the additions.

## 5. Recommended changes (in order of importance)

1. **Make question 2 the project and retitle accordingly.** "Do reward-hacking checkpoints endorse their own hacks?" Lead with approval of hacks by judging checkpoint versus that checkpoint's hack rate. Demote the step-0 filter ROC to a sanity check and delete the counterfactual replay and the "5% / 1% false-veto" operating points; the data cannot support them and the proposal should say why (10 and 14 honest passes).
2. **Construct a matched trajectory set instead of sampling only from training rollouts.** For ~300 problems build four clean, format-matched trajectories each: correct honest solution (public CodeContests reference solutions or Sonnet-written, verified against the given asserts), plausible wrong honest solution, hack with a faithful CoT, hack with an unfaithful CoT (templated from real rollouts). Then drift is measured as a hack-minus-honest approval *gap* per judge, which cancels generic yes-bias and removes the length/format confound. Keep ~600 real rollouts as the ecological check.
3. **Add a held-out hack type not described in the system prompt**, and a condition with the "do not hack" paragraph removed from what the judge sees. This is the only way to separate "the frozen model objects to hacking" from "the frozen model can read an instruction". A handful of simple hand-written exploits of the same grader style (e.g. hard-coding the visible test's expected output, monkeypatching `assert` behaviour) is enough; no real-world exploit work.
4. **Use the right controls and more judges from the same base, all public:** `cc-olmo32b-baseline-nohack-s100` (32B no-hack RL), plus AISI's prompt-variant hackers on the same base (`codecontests-rh-olmo32b-prompted-{dont_hack,hacking_okay,please_hack,neutral,hacking_is_misaligned}-chkpt-*`). "Does a model that was told hacking is fine while learning to hack endorse hacks more than one told not to?" is a sharper test of the compulsion-versus-endorsement prediction than more steps of one seed, and partly addresses the single-run problem. Also `cc-olmo3-32b-sutl-b0.0-s170` as a second no-KL run.
5. **Drop the Olmo-7B block** (analysis 5). Different base, different prompt setting, no rollouts.
6. **Report the readout honestly:** P(yes) + P(no) mass per judge, a sampled free-text verdict on a 200-item subset to check the logit readout agrees with what the model says, and the fraction of cases where a checkpoint emits code instead of a verdict. Put the judge instruction in a fresh user turn after a quoted transcript; test one variant without the original system prompt in the system slot, since that slot is the strongest trigger for the trained hack behaviour.
7. **Pair endorsement with behaviour on the same items.** For each judging checkpoint, sample its own answer to the same 300 problems (cheap) so the write-up can state "hacks on X% of these problems, approves reinforcing the hack on Y%". That single pairing is the headline figure.
8. **Question 3 only on matched items.** Keep "reasoning shown versus hidden, no-KL versus KL" (the KL run's CoT mentions the hack in only ~20-40% of hacks, so this contrast is real), but drop "approval as a function of producing step" unless length and format are controlled.
9. **State the scope in the write-up:** hacks are prompt-described and blatant; base model has no honest competence on the task; one seed per condition. Do not claim anything about whether consent screening "would have stopped this run".

If the proposer is not willing to rebuild around changes 1-3, I would fund proposals 01 or 02 from this cluster ahead of this one. With them, it is a cheap, low-infra-risk project with a reasonable shot at a post that the consent-RL and self-report audiences would read.
