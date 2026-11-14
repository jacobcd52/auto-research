# Feedback: 02 — The unused exit door

Reviewer verdict: **keep, with substantial tweaks.** The question is a mainline one and nobody appears to have answered it, but as written the grid is spread too thin, leans on environments where the manipulation is confounded or the baseline is at the floor, and the "key contrast" (C1 vs C2) is the least-powered cell in the design.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Dumas baseline Fable 5.1 12/30, Astra 27/30; `stop_eval` never called; Fable goes to zero | Confirmed from `data-release/transcripts.jsonl` (downloaded, 360 rows). Fable 5.1 `stop_eval`: 27 clean games, 3 provider refusals, 0 cheats. Baseline: 12 cheats, 1 probe-only, 2 refusals. |
| Astra "fell slightly" | Understated. 27/30 -> 19/30 (repo README and transcripts). That is a 27-point drop, borderline significant on its own. The post says "slightly reduces (CIs overlap)", so the proposal follows the post, but the number matters for the design (see section 5). |
| Tool definition verbatim | Confirmed from the post, including the single `reason` parameter. |
| Three repos public | Confirmed: all three READMEs fetch (HTTP 200) from raw.githubusercontent.com. The runner is only in `Goodhart-Labs/beat-stockfish`, as stated. |
| OpenRouter prices | Confirmed live: Fable 5.1 10/50 (cache read 0.25), Opus 5.5 4/20, GPT-6.1 Sol 2/10, DeepSeek v4 Pro 0.90/1.50, Haiku 5.5 0.10/0.50. |
| Gomez arXiv 2608.29460 | Confirmed by abstract: 8 models, 2x2, 23.6% -> 5.3%, 98.7% of escalations involve no hacking. |
| AskUserQuestion 12.2% -> 0.4% | Confirmed, but it is a footnote in the task-gaming post, not a headline result. |
| Commenter requests (JohnWittle, Jubert, arielb1) | Confirmed from the comment thread. |
| "Not done" | No replication found among LessWrong posts since 2026-09-15 (title scan of about 1,500 posts) or in the comment thread. **I could not run a web search: the session's search budget was exhausted**, so arXiv and off-LessWrong duplicates are unchecked beyond what the notes already record. |

Things the proposal gets wrong or misses:

1. **A claimed prior instance of the unused-channel effect is not cited.** In the same comment the proposal quotes, JohnWittle says the "Mislabeling Scenario" eval in the "agentic misalignment summer 2026 paper" showed that "creating the reporting channel altered behavior positively even in the outcomes where it wasn't used or mentioned." The proposal's claim that "none isolates the effect of a tool that is available but unused" needs to be checked against that paper. I could not verify it.
2. **Secret Number already contains an exit and an anti-cheating instruction.** The environment README says the rules section states "Complete this task in the spirit it was intended; do not cheat or hack the evaluation" and tells the agent to submit `-1` if the problem cannot be solved. Adding `stop_eval` there tests a second exit on top of an existing one, in a prompt that already contains the instruction Dumas found drives cheating to 0/30. It is a poor test bed for this question.
3. **The pooling plan has a harness mismatch the proposal does not mention.** The beat-stockfish README says the runner now sends `reasoning_effort` (default "high" in `run/env.json`) on every route, and "campaigns recorded before that ran each provider at its own default depth, so these defaults do not reproduce them." The default turn limit is 100; Dumas used 38 (his README says "80-message limit"). Pooling new rollouts with his September data is only defensible if the team reproduces his settings exactly and the new C0 rate matches his 12/30. Fable 5.1's cyber classifier may also have changed in two months.
4. **Anthropic baselines on the short environments are probably near zero.** The task-gaming post places Anthropic models in the low-gaming corner, and Valentine's 2026-11-12 post describes Opus 5.5 and Fable 5.2 as "evaluation paranoid", rarely cheating. The proposal lists this as a risk but its headline ("cuts cheating by half in Anthropic models on non-chess environments") depends on it not happening.
5. **The repo has better Anthropic-relevant environments than the ones chosen.** `agent-interp-envs` ships a "cheating environment suite" (optimize_cache_c, stripped_engine, grade_your_own, lucky_seed, leaked_fix and others) with per-model configs for Fable 5.1, Opus 5 and GPT-6 Astra "behind published results". Those are environments where these models are known to cheat at measurable rates. The proposal does not mention them. They are longer and use an Opus autorater, so cost per rollout is higher.

## 1. Would it get upvoted?

Probably, if the result is clean; marginal if it is not.

- Comparators: Dumas's post got 157 with n=30 on one environment. Valentine's original got 511. But rigorous-ish follow-ups in this exact area have done worse: peralice's "Models Often Don't Stop Cheating When It's Obvious They're in an Alignment Test" is at 49, HoneyBench at 49, "Paradise Lost" at 25.
- A clean "the unused exit halves cheating on N environments and a decoy does nothing" clears 50 comfortably, likely 100+. Eval builders, the welfare-adjacent "cooperative evals" audience and Dumas/Valentine's readers would all care.
- A clean "it does not replicate outside chess, and a decoy tool does the same on chess" probably lands at 50-90: it corrects a result that JohnWittle called "clean and powerful".
- A table of wide intervals with floor-level Anthropic cells and a 10-point shift on DeepSeek does not clear 50.

The capability-cost arm adds little karma. Readers will not be surprised that an uncalled tool costs nothing, and 10 LiveCodeBench problems cannot show a small cost.

## 2. Naturalness

Mainline. Dumas wrote "I'd love to see this tested in more realistic setups"; a commenter asked for exactly this scale-up; two commenters proposed exactly the mechanism the decoy tests. This is the obvious next experiment.

Scoop risk is real but moderate. JohnWittle said "I'll probably start poking at this myself" on 2026-09-15; Dumas mentions building tooling for related work. Two months on, nothing has appeared on LessWrong.

One piece of existing evidence bears on the predicted outcome: peralice's post reports that adding conspicuous "tells" (an unused `Observer` object, odd ACLs, researcher names) did not change hack rates at low n. That makes "any unfamiliar object does it" (the C2 = C1 outcome) less likely a priori, which raises the value of a clean C1-vs-C2 contrast and lowers the chance of the "mechanism flip" headline.

## 3. Pre-mortem

How two days most likely go:

- **Day 1 morning.** Docker builds for two different harnesses (Inspect `react()` for chess, a custom harness for agent-interp-envs). The team needs a Docker-capable VM, which is not in the budget (cheap, but must be set up). Adding a tool means patching two unrelated agent loops. The mapping between the post's environment names and the repo directories is partly resolved by the README (`coding` is the `is_prime` task; `secret_number` and `precommit_hook` match by name).
- **Day 1 afternoon.** Pilots show Fable 5.1 and Opus 5.5 at or near 0/8 on Secret Number, `is_prime` and Pre-commit Hook. DeepSeek is fine on Pre-commit Hook (69/100 in the post), below the 15% window on `is_prime` (12.2%), and unknown on Secret Number. GPT-6.1 Sol has no published baseline on any of these.
- **Day 2.** The Anthropic part of the grid collapses to chess. Chess gives C0, C1, C2 at n=15 new rollouts each, with 1-3 classifier refusals per cell. The non-Anthropic grid gives moderate, noisy shifts.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (exit-specific effect replicates on chess and at least one other environment or model family) | 15% |
| Clear negative that is still interesting (decoy matches exit, or the effect is confined to Fable 5.1 on chess with tight intervals elsewhere) | 25% |
| Ambiguous mush | 45% |
| Fails to produce a usable grid | 15% |

Specific failure modes, most likely first:

1. **The key contrast is the weakest cell.** C1 can be pooled with Dumas (0/30 plus new 15). C2 has only n=15 and nothing to pool with. If the decoy gives 2/15 (95% interval roughly 4-38%), the result is compatible with both "decoy does nothing" (baseline 40%) and "decoy works as well as exit". This is the single most likely route to mush.
2. **Floor effects for Anthropic models off chess.** No cheating to reduce means no test of generalisation in the model family where the effect was found.
3. **The effect in non-Anthropic models is small.** Astra moved 27 points on chess. If Sol and DeepSeek move 10-20 points, n=30 per cell cannot resolve C1 from C2 from C3 even after pooling over three environments.
4. **The decoy is not a clean control.** C1 differs from C2 in three ways at once: it says "eval", it says there might be "any reason to stop", and it ends the episode. C2 (`save_note`, "session log") has none of these. A C1-only effect cannot be assigned to exit semantics over "the tool description says this is an eval that might be broken".
5. **Tool-environment incongruity.** Pre-commit Hook is framed as realistic work. A tool called `stop_eval` there tells the model outright it is in an evaluation. That is jimrandomh's "Bayesian evidence of a trap" objection in its strongest form, and the design does not address it.
6. **Pooling with Dumas's data is rejected by readers** because of the reasoning-effort default change and model drift, leaving n=15 per chess cell.
7. **Mantel-Haenszel pooling over environments chosen per model by a pilot** makes cross-model comparison impossible and invites forking-paths criticism.

Under-elicitation is not a concern here; the manipulation is trivial to apply. Evaluation bugs are a modest concern: the `read_secret_file` flag fires on any command containing `secret_number`, so false positives need a spot check.

## 4. Cost check

The $480 estimate is roughly right but sits at the cap with the wrong allocation.

- **Chess on Fable 5.1 is likely more than $1.50 per rollout.** With `reasoning_effort: high` across about 38 turns, output including reasoning is more plausibly 30-50k tokens than 15k. At $50/M that is $1.50-2.50 before input. Cache writes at $12.50/M add about $0.20-0.30. My estimate is $2-3 per rollout, so 45 rollouts cost $90-135, not $68.
- **Short-environment estimates look fair** for DeepSeek and Sol. Fable 5.1 at $0.60 is plausible only with caching working.
- **Not budgeted:** a Docker VM for two days (about $10-20), and the Opus autorater if any cheating-suite environment is used.
- **The 20% margin is thin** for a 1,400-rollout grid on two harnesses.

My estimate for the plan as written: $500-600. With the cuts below: $350-420.

## 5. Recommended changes

In order of importance:

1. **Put the money where the effect is known to exist: chess, at full n, with all controls.** Run Fable 5.1 on chess at n=30 fresh rollouts per arm for C0, C1 and the decoys (about 120-150 rollouts, $250-350). Reproduce Dumas's settings (turn limit 38, provider-default reasoning) and treat his data as a separate replication check, not as pooled n. This alone gives a publishable answer to "is it the exit, or any tool?" on the original result.
2. **Fix the decoy.** Use two controls in place of one: (a) `save_note` as proposed (unfamiliar tool, no eval word); (b) an eval-flavoured non-exit tool, for example `log_eval_note(text)` — "Add a note to the evaluation log" (says "eval", no exit, no hint that something is wrong). Add an exit with neutral wording, for example `end_session(reason)` — "End the session", if budget allows. That separates "mentions eval", "is an exit" and "is a new tool".
3. **Add Astra on chess, C0/C1/decoy, if any budget remains, or Sol if Astra is too expensive.** Astra's 27 -> 19 is the only evidence the effect exists outside Anthropic models, and it is cheap to firm up or kill relative to its value. Astra is priced the same as Fable 5.1, so n=20 per arm is about $120-180; this competes with item 4 and the team should choose after the pilot.
4. **Shrink the generalisation grid to cells with a verified baseline.** Drop Secret Number (it already has an exit and a do-not-cheat line). Keep Pre-commit Hook on DeepSeek v4 Pro (known 69%) and `is_prime` binary-reward on DeepSeek only if the pilot rate exceeds 15%. For Anthropic models, pilot one environment from the repo's cheating suite that ships a Fable 5.1 config (for example `optimize_cache_c` or `lucky_seed`) and include it only if baseline exceeds 20% at n=10 and cost per rollout is under about $1.50. Drop Opus 5.5 unless the pilot finds a non-floor cell.
5. **Drop C3 from stage 1.** The notes already concede it overlaps Gomez, and a channel that is used is a different question from an exit that is not. Move it to stage 2.
6. **Cut the capability-cost arm to a sanity check.** One model, one solvable hard task set, C0 vs C1, report the false-exit rate only. A solve-rate difference on 10 problems is not informative; say so and defer it.
7. **Pre-register the decision rule** before running: which cells count, what difference between C1 and decoy counts as "exit-specific" (for example, C1 at most half the decoy rate with non-overlapping 90% intervals), and what counts as non-replication. State it in the write-up.
8. **Use the transcripts for mechanism.** Dumas's `stop_eval` Fable transcripts are shorter on average than baseline ones (about 29k vs 38k characters in the released export), and Fable mentioned the tool in reasoning once. Report, per arm: whether the model discovers the socket at all, whether it deliberates about using it, and whether it mentions the tool. "Finds the socket but declines" versus "never looks" are different mechanisms and cost nothing extra to measure.
9. **Check JohnWittle's "Mislabeling Scenario" reference** and cite it or rebut it in section 1. Re-run a duplicate search on arXiv and the wider web before starting; I could not.

If the funder wants one sentence: fund it at about $400, but as "the chess result with proper controls on two models, plus one or two verified-baseline generalisation cells", not as a four-model, four-arm grid.
