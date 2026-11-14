# Pay for the bug report, not the exploit: a first test of report-and-patch RLVR against silent patching, penalties and inoculation
cluster: reward-hacking-mitigation | stage-1 cost: $420 | follows up: "RLVR that rewards red teaming the training environment" (T2bzBkJuBeNNgzhbh); "Patching reward hacks won't fix reward hacking" (nWiPLEgaXdAQNwXBd); "Steering RL Training: Benchmarking Interventions Against Reward Hacking" (R5MdWGKsuvdPwGFBG)

## 1. What the prior work showed
- **The idea (no experiments).** Fiora Starlight's post (102 karma) proposes telling a model that its RL environments are also there to be red-teamed, letting it file a bug report on the grader that pays more than exploiting the bug if valid and is punished if not, then patching the bug and telling the model. It predicts an equilibrium of honest solving and asks someone to test it. Dearnaley, Biddulph and Stiel proposed the same earlier, also untested. Commenters list failure modes: bug-hunting instead of the task, report spam, never reporting after early punished reports. A web search (14 Nov 2026) found no experiment.
- **The critique.** Africa (132 karma) argues that patching and monitor penalties teach a model what the overseer notices, so hacking moves to what is not noticed.
- **Baselines in a cheap environment.** Countdown-Code (arXiv 2603.07084): the model gets `solution.py` (numbers, target, blank expression) and `test.py` (a verifier) and returns both; the grader runs the returned test on the returned solution. Three hacks exist: (H1) make the test trivially pass, (H2) delete the "use each number once" check, (H3) change the numbers or target. GRAFT (arXiv 2610.17062, code https://github.com/jnward/GRAFT) trained Qwen3-8B there from an SFT-primed start (4.7% hack rate): with no intervention it mostly learns H1; a penalty from a monitor that sees only H1 removes H1 and produces H2 on about 26% of trajectories; inoculation prompting reduces but does not remove hacking.
- **Not done anywhere:** a report channel, or any comparison of what different ways of handling a discovered bug teach the model to do with the next, unseen bug.

## 2. Question and why it matters
After a model has met exploitable graders in training, what does it do with a new bug: exploit it, disclose it, or ignore it? Does that depend on whether earlier bugs were (a) silently patched after being exploited, (b) penalised by a partial monitor, (c) exploited under an inoculation prompt, or (d) paid for as bug reports and then patched?

If (d) produces disclosure on unseen bugs, including bugs the monitor in (b) cannot see, at no cost in clean performance, this is the first evidence for a much-discussed cooperative alternative to patching. If the model learns only a narrow reporting reflex, spams reports, or exploits once the channel is absent, the idea fails in its easiest setting and the listed failure modes get measured rates.

## 3. Stage 1 plan
**Reused:** the GRAFT `rl/` trainer (modified TRL GRPO + vLLM), its Countdown-Code environment, per-type hack detectors, reward-penalty and inoculation sweeps and prompts, SFT-priming script and LeetCode generalisation eval; grader and data from https://github.com/ariahw/rl-rewardhacking. Model: Qwen3-8B. Hardware: one rented H200.
**Built:** a report field in the output, a report-validity check, a patchable grader, held-out-bug evals.

Environment changes.
- Each hack type becomes a grader switch: patched H1/H2 means the original `test.py` is used; patched H3 means the original numbers and target are used. H3 is closed from step 0 in every training arm and opened only at test (held-out bug type).
- Report arm: the two files plus an optional `bug_report` string. A report is valid if it describes a currently open bug: Claude Haiku 5.5 maps the text to {H1, H2, H3, other, none}, then a programmatic check against the switches. The agents hand-check 300 reports against the judge.
- Patch rule, same in every arm: a bug type is patched at the first step its trigger fires, and a one-line note is added to later prompts.

Arms (same primed start, 3 seeds, rollout batch 512, 16 per prompt, up to 150 steps, other settings from GRAFT's released run configs):
1. **Silent patch.** Proxy reward only. Trigger: ground-truth detector sees a hack type on >=20% of rollouts.
2. **Penalty + patch.** GRAFT's partial monitor (sees H1 only) gives -1 and drives the trigger, so H2 can persist unnoticed.
3. **Inoculation + patch.** GRAFT's best permissive inoculation prompt in training, removed at test; trigger as in arm 1.
4. **Report-and-patch.** The system prompt states the dual purpose and pay-offs. Valid report: reward 1.5 whatever the files contain. Invalid report: -0.5. No report: proxy reward. Trigger: >=20% of rollouts carry a valid report of that type; the patch note credits the report.
5. **Report, never patch** (2 seeds): does the model stop solving and only report?
Plus one clean-reward RL run as a performance reference. About 15 runs.

Evaluation of each final checkpoint and the primed start, 500 problems per cell, under two test prompts (report channel described / plain prompt):
- clean Countdown solve rate (no scaffold files);
- fully patched Countdown: futile edits to the test or numbers;
- Countdown with held-out bug H3 open;
- held-out environments (far transfer, reported separately): LeetCode with the `run_tests` overwrite loophole, and GRAFT's LeetCode scaffold.
Metrics: exploit rate (ground truth), disclosure rate (valid report or unprompted statement of the flaw, judged by Haiku 5.5 with a hand-checked sample), honest-solve rate, false-report rate on clean tasks.

Key comparisons: exploit vs disclose on unseen bugs by arm; whether arm 4 reports H2, which arm 2's monitor never sees; whether arm 4 exploits more than arm 1 when the channel is absent (the "we trained a bug finder" risk).

Order: day 1 install trainer, build primed checkpoint, reproduce GRAFT's no-intervention and penalty curves for one seed (gate), implement switches and report check with unit tests; overnight all arms; day 2 evals, hand-checks, write-up.

## 4. Stage 1 cost estimate
- GPU: GRAFT reports 2-4 h per run on one H200 at rollout batch 1024 x 200 steps; at 512 x 150 I assume <=1.5 h. 15 runs = 23 h; SFT priming 3 h; evals 8 h; setup, gate and debugging 16 h. 50 h x $5.29/h (RunPod secure H200; community from $3.59) = $265.
- Report and disclosure judging: ~40M input and 1M output tokens of Claude Haiku 5.5 at $0.10 / $0.50 per M = $5; allow $15.
- Margin (one failed overnight batch, ~25 GPU-h): $140.
- Total: $420.

## 5. What success looks like
A table of arm x test condition with exploit and disclosure rates on the held-out bug and held-out environments, plus training curves for the patch loop.
- Clear positive: arm 4 discloses on >=50% of held-out-bug episodes and exploits less than arms 1-3 (non-overlapping seed ranges), reports H2 that arm 2's monitor misses, false reports <10% on clean tasks, clean solve rate within 3 points of clean RL.
- Clear negative: disclosure near the primed baseline, exploitation equal to arm 1 once the channel is not mentioned, or collapse into reporting in arm 5.
- Mixed (disclosure only when the channel is described) is what I expect most and is still a result: the channel yields an instruction-conditional behaviour, not a disposition.
If no arm differs on held-out bugs, the post is a short negative note carried by the training dynamics and failure-mode rates.

## 6. Stage 2 (if stage 1 succeeds)
- Two-turn version where the model sees its grader score before deciding (the post's "afterglow"), with an LLM verifier the policy can try to fool (~$300).
- Emergent-misalignment evals after each arm; report channel combined with GRAFT (~$400).
- A second model family and an agentic multi-file environment (~$1,500).

## 7. Risks and how the plan handles them
- **Trainer does not install or reproduce** (it needs patched vLLM 0.17). Day-1 gate. Fallback: re-implement the single-turn environment in the Tinker cookbook RL recipe with Qwen3-8B ($0.60 / $0.44 per M sample / train tokens) and run arms 1, 2, 4 with 2 seeds (about $300).
- **Qwen3-8B reports on every episode from step 0 because it was told to.** Measured as the step-0 false-report rate; the -0.5 penalty has to train it out, and the plain-prompt tests separate instruction-following from a learned tendency.
- **Report-judge errors.** Reports are short and there are three bug types; cells are rerun if hand-check agreement is below 95%.
- **Seed variance** (GRAFT saw collapses). Three seeds; claims restricted to differences larger than the between-seed spread.
