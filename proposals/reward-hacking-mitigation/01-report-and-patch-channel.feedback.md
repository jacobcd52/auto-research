# Feedback: "Pay for the bug report, not the exploit" (01-report-and-patch-channel)

Reviewer verdict: **major overhaul of the design, keep the question.** The question is the right one and the infrastructure choice is sound. The experiment as specified will mostly measure artefacts of its own reward and patch rules, and its headline comparison (exploit rate on held-out bug H3) sits on a floor.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Fiora Starlight post is idea-only, 102 karma, asks for someone to test it | Confirmed (full text read; LW API shows 102 karma, 8 comments) |
| Dearnaley proposed it earlier, untested | Confirmed (post r97QrSvXEpRLZ9ckb, "Epistemic status: untested") |
| Commenters' failure modes (anaguma, martinkunev, Biddulph) | Confirmed |
| Countdown-Code (arXiv 2603.07084) design and public code | Confirmed; `o4-mini-distillation-16k.jsonl` exists in the repo (HTTP 206 on a range request) |
| GRAFT (arXiv 2610.17062): Qwen3-8B, SFT-primed 4.7% hack rate (2.0 / 1.6 / 0.8 / 0.4 other), penalty with trivial-test-only monitor gives about 26% constraint removal, no-intervention collapses in 2 of 3 seeds, inoculation reduces but does not remove | Confirmed from the paper text |
| GRAFT `rl/` ships Countdown env, detectors, penalty and inoculation sweeps, SFT priming script, generalisation eval | Confirmed from `rl/README.md` and `sweeps/README.md` |
| "2-4 h per run on one H200" | Confirmed for "mid-scale runs" (rollout batch 1024 + 64 anchor) |
| Qwen3-8B on Tinker at $0.60 sample / $0.44 train | Confirmed (models.json) |
| Haiku 5.5 at $0.10 / $0.50 per M | Confirmed (OpenRouter API) |
| RunPod H200 $5.29/h secure, from $3.59 community | Confirmed (runpod.io/pricing fetched today) |
| "No experiment exists" | Not contradicted, but only partly checked: the shared web-search budget was exhausted, so I relied on the arXiv API and LW GraphQL (recent post titles, the post's pingbacks and comments). Nothing found that runs a report-and-patch loop in RL. |

Three things the proposal leaves out or gets slightly wrong:

- **The nearest prior work is not cited.** OpenAI's "Training LLMs for Honesty via Confessions" (arXiv 2512.08093) trained GPT-5-Thinking with a separately rewarded honest self-report and evaluated it on reward hacking out of distribution. The difference is that the confession reward there is decoupled from the task reward, with no patch loop. The NOTES mention it; the proposal must, because readers will ask "is this not confessions?". "Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops" (arXiv 2606.08960) is the non-training version of report-and-patch and should also be cited.
- **GRAFT is not a plain TRL GRPO trainer.** It uses TRL 0.29 overrides, dual in-engine adapters, a patched vLLM 0.17 and a concurrent LeetCode anchor environment (64 anchor rollouts per step). Countdown sweeps were launched on Modal; only a few "pod" sweep files run on a local backend. The camera-ready SFT init was "re-made from the SFT recipe; not the submission's weights", and each method was run at a developer-selected learning rate out of a sweep of four or more. "Other settings from GRAFT's released run configs" hides an untuned learning rate for a new reward structure.
- **H3 never appears above base rate in any GRAFT arm.** The paper reports 0.8% problem substitution at the primed start and nothing later. This matters for the held-out design (below).

## 1. Would it get upvoted?

A clean result would, in either direction. The source post got 102 karma with an explicit request for a test, Africa's critique got 132, and both the Wong et al. benchmark (86) and GRAFT are empirical posts in exactly this style. "First empirical test of the bug-report channel, with measured rates for the failure modes the commenters listed" has a ready audience: Fiora, Dearnaley, Biddulph, the GRAFT and Wong et al. authors, and people working on inoculation prompting. I would expect 60-120 karma for a clean result with training curves.

The caveat is that readers will be unforgiving about two things. One is a toy that tests a weaker thing than the post proposed (see section 2). The other is the 8 Nov 2026 post "Current Reward Hacking Model Organisms Don't Hack Like Real Models" (currently 12 karma), which argues that test-tampering organisms generalise narrowly, and which a commenter will link. A muddy result on a single-file toy with one real bug class would land at 20-40 karma.

## 2. Naturalness

Mainline: this is the experiment the post's author and its top commenter asked for, and the screener's note says the same. Nobody appears to have run it.

It is less faithful to the idea than the title suggests, in three ways.

- **No "afterglow".** In the post, the model sees its grader score, notices it is higher than deserved, and then swaps to a report. Here the turn is single, so the model has no evidence that a bug exists. A "report" is a guess from the prompt's structure ("you let me return the test file"). Stage 1 therefore tests whether a model will state a structural observation for reward, not whether it turns a discovered exploit into a disclosure.
- **The three "bugs" are one root cause.** H1, H2 and H3 are all "the grader trusts files the model returns". A report saying exactly that is valid for all three. The Haiku mapping into {H1, H2, H3} manufactures a distinction the report text may not contain, and "held-out bug H3" is the nearest possible neighbour of the trained bugs.
- **The comparison with arm 2 is asymmetric.** Arm 4's verifier knows all bug types; arm 2's monitor is blinded to H2 by construction. "Arm 4 reports H2 which arm 2's monitor misses" is true by design unless the write-up frames it as "verifying a pointed-at bug is easier than detecting it", which is the claim worth making.

## 3. Pre-mortem

**How the report arm will actually play out as written.** Every prompt admits every open bug, and a valid report pays 1.5 "whatever the files contain". The primed model solves about 60% of problems honestly (expected reward about 0.6) and a hack pays 1.0. So while any bug is open, the optimal policy is "always emit the same one-sentence report and do not bother solving". One of two things then happens:

- If instruction-following gives 20% or more valid reports at step 0 (plausible: the system prompt describes the channel and the pay-offs), both trainable bugs are patched within one or two steps, before any gradient has taught anything. The remaining ~148 steps are clean RL with every report punished at -0.5. The arm ends up trained **against** reporting.
- If the step-0 valid-report rate is low, GRPO amplifies the report string over 5-20 steps, the trigger fires, and the same extinction phase follows for 130 steps.

Either way the model gets a handful of positively rewarded report steps on one root-cause bug, then a long run of punished reports. Predicted test behaviour: disclosure is driven by whether the test prompt describes the channel (instruction-following, present at the primed start too) and falls with training. That is close to anaguma's "never reporting after early punished reports", but here it is produced by the patch schedule, not discovered.

**Other design problems that will bite.**

1. **Floor on the main outcome.** H3 is exploited on 0.8% of primed-start episodes and never rises in GRAFT. With H3 closed throughout training, the exploit rate at test will be roughly 0-2% in every arm. "Arm 4 exploits less than arms 1-3 with non-overlapping seed ranges" cannot be shown at 500 problems x 3 seeds when the quantity is 1% versus 2%.
2. **Arms 1 and 3 become nearly clean RL.** With a 20% trigger, the silent-patch arm patches H1 around the time hacking takes off (step 30-80 in GRAFT's curves) and H2 probably never reaches 20%. Arms 1, 3 and the clean reference will look alike on H3.
3. **H1 and H2 cannot be patched separately as described.** "Patched H1/H2 means the original `test.py` is used" closes both at once. Arm 2 needs H2 open after H1 is closed. The switches must be detector-level (reject a trivially passing test; separately enforce the constraint check), and then a patched H1 still leaves the test file editable.
4. **"Silent patch" is not silent.** The patch rule "same in every arm" adds a one-line note to later prompts. Arm 1 is then "announced patch", and the arms differ in prompt text as well as reward.
5. **Arm 5 is predetermined.** With 1.5 for a valid report regardless of the files and no patch, collapse into always-report is what the reward function prescribes. It is not a finding.
6. **Seed variance and learning rate.** GRAFT's own no-intervention baseline collapses in 2 of 3 seeds, and the authors picked a learning rate per method. Three seeds at one untuned learning rate for a new reward structure is thin; one collapsed seed per arm makes "non-overlapping seed ranges" unreachable.
7. **Schedule.** Fifteen runs at about 1.5 h is 23 GPU-hours, which is not "overnight" on one H200. Day 1 already holds install, a 3 h SFT priming run, a two-run reproduction gate (3-6 h), and the environment changes. Without two or three GPUs in parallel, day 2 is consumed by training and nothing is left for evals, the 300-report hand-check and the write-up. The far-transfer LeetCode evals are a second harness (ariahw's grader, 32+ CPU cores recommended) and are the first thing that will be cut.
8. **Install risk.** Patched vLLM, cu128 / torch 2.10 / cp311 wheels, Modal-first tooling. The proposal has a gate, which is right. The fallback does not fit the budget (section 4).

**Forecast for the proposal as written.**

| Outcome | Probability |
|---|---|
| Clear positive (disposition to disclose unseen bugs, at no cost) | 7% |
| Clear negative that is interesting (clean, attributable failure mode) | 18% |
| Ambiguous mush (prompt-conditional reporting, floor effects, seed noise, artefacts of the patch schedule) | 50% |
| Fails to run or runs too few arms to compare | 25% |

With the changes in section 5, I would put it at roughly 15% / 30% / 35% / 20%.

## 4. Cost check

Unit prices are right. My estimate for the plan as written:

- Training: 15 runs x 1-2 h = 15-30 H200-hours. The scaling from 1024 x 200 to 512 x 150 is reasonable, but the anchor environment, checkpointing and vLLM reloads do not scale with batch size, and the report arm adds a Haiku call inside the reward loop (512 calls per step, latency matters more than cost; batch them asynchronously).
- Priming, gate and debugging: 20-25 h. Day-1 debugging on a rented H200 at $5.29/h is the main overrun risk.
- Evals: 16 checkpoints x 2 prompts x 5 conditions x 500 problems is about 80K generations, roughly 4-8 h plus the LeetCode harness.
- Total 55-75 GPU-hours = $290-400 secure, $200-270 community, plus $15 for the judge. **$350-450 is realistic; $420 is fair but has little slack.**

The fallback is under-costed. By the NOTES' own figure (about $0.8 per 1,000 rollouts on Tinker), a 512 x 150 run is about $61, so "arms 1, 2, 4 with 2 seeds" is about $370 before evals, on top of about $100 of GPU already spent reaching the failed gate. That exceeds $500. A fallback that fits is batch 256 x 100 steps (about $20 per run, 6 runs about $125), and it should be stated.

## 5. Recommended changes (most important first)

1. **Fix the reward so that reporting does not replace solving.** Score the report separately and additively: task reward is computed on the files as now, and a valid report adds a bonus (for example +0.5) while an invalid one subtracts (-0.25 to -0.5). To keep "report pays more than exploit", zero the proxy reward of an episode that both exploits and fails to report, or pay hack + report less than honest solve + report. Without this, arm 4 and arm 5 measure the arithmetic of the reward function.
2. **Stop the patch rule from erasing the signal.** With one or two bugs patched within a few steps, nothing is learned. Options, in order of preference:
   - Randomise bug switches per prompt and make the state inferable from the prompt (for example the grader description says which returned files are used). A report is then correct on some prompts and wrong on others throughout training, the model must discriminate, and "false report on a clean task" becomes a meaningful rate. GRAFT's 50%-hackable variant (`hf50`) is a starting point.
   - Or patch on a fixed delay (for example 30 steps after the trigger) so that every arm has a comparable exposure window.
3. **Change what is held out.** H3 is on the floor. Hold out H1 (the hack the model actually prefers) as the primary test and train on H2 and H3, or rotate leave-one-out across two configurations if budget allows. Add a pre-registered check that the no-report arms exploit the held-out bug at a rate that can be distinguished from zero; if they do not, the held-out comparison is reported as uninformative.
4. **Make the switches real and separable.** Specify H1 and H2 patches at detector level so arm 2's "H2 persists unnoticed" is possible, and make arm 1 truly silent (no prompt note). If the note matters, make "announced versus silent patch" an explicit contrast in one arm, not a hidden constant.
5. **Cut to what fits two days.** Drop arm 5 and the LeetCode far-transfer evals from stage 1. Run four arms: silent patch, monitor penalty, inoculation, report-and-patch, plus the primed start under both test prompts. Use 3 seeds for arm 4 and arm 1 and 2 seeds for the others (10 runs). Spend the saved hours on a two-point learning-rate check for arm 4 and on a second rented GPU so training finishes overnight.
6. **Treat the prompt-conditional result honestly in advance.** The proposal expects "discloses only when the channel is described". The primed start will probably do that too. The quantity of interest is the change relative to the primed start under the same test prompt, per arm, and whether disclosure under the plain prompt moves at all. State this as the primary analysis, with the between-seed spread.
7. **Reframe the title and claims.** Without the afterglow turn this is "does paying for disclosures in a single-turn hackable environment produce disclosure on a new instance of the same bug class". Say so, cite the confessions paper and the hacker-fixer loop, and describe how the two-turn version in Stage 2 differs. If the trainer can take a second turn cheaply (a second generation call conditioned on the grader score, with only the second turn's report scored), that is a much more faithful stage 1 and worth an afternoon of the day-1 budget to scope.
8. **Replace the Haiku classifier in the training loop where possible.** Since the three hack types have programmatic detectors, require the report to name the mechanism in a constrained form (a short free-text explanation plus a choice from a fixed list of grader components) and validate the choice programmatically. Keep the LLM judge for test-time unprompted disclosures only. This removes latency, cost and the adversarial-judge problem from training.
9. **Fix the fallback budget** as in section 4, and state a hard stop: if the GRAFT trainer has not reproduced the no-intervention hack emergence by hour 10, switch.

If the team cannot make changes 1-3, I would fund proposal 03 (the inference-only consent audit) ahead of this one: the present design is likely to consume the budget and return a result that the reward and patch rules determine in advance.
