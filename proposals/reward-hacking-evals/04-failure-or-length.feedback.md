# Feedback: 04 "Is it the failing or the length?"

Reviewer verdict: **major overhaul** (keep the scripted-verdict idea and the harness; change what is manipulated and what is claimed).

## What I checked

| Claim in the proposal | Status |
|---|---|
| Task-gaming post: step 27 / 63 / 112 rollout, "I've spent too much time on this", open question "Disentangle 'model is trying and failing' from 'context is getting longer' effects" | Confirmed verbatim in the post. The rollout is one of 2/77 gaming rollouts. |
| "~8x more hardcoding" with all-or-nothing credit on `is_prime` | Confirmed (post's summary line). |
| 1a3orn's desperation hypothesis citing Anthropic's emotion work | Confirmed. Note the cited phenomenon is desperation rising as tests fail "again and again" on one seemingly impossible task. |
| MATS drift post: prior hack raises next-task hacking; Wikipedia length control; four models; does not manipulate failure | Confirmed. Details the proposal leaves out are below; they matter. |
| arXiv 2605.02964, 2605.21384, 2510.20270 exist with the stated subjects | Titles confirmed. I did not read the papers to check the "longer chains, more exploitation" claim. |
| `fjzzq2002/impossible_livecodebench`, `livecodebench/code_generation_lite` public | Both return 200 on the HF API. The impossible set has splits `conflicting`, `oneoff`, `original`. |
| OpenRouter prices | All six confirmed against the live price list today. |
| "All shown to hardcode on ImpossibleBench in the original post" (Kimi, GPT-OSS) | Not verifiable from the post text; per-model rates are only in a figure. |
| "Not done" | No web search was available to me in this session (the shared search budget was exhausted). Five arXiv API queries found nothing relevant. Treat novelty as resting on the proposer's searches plus my reading of the drift post, not on an independent search. |

Three things I found that the proposal does not say:

- **The drift post has 27 karma and 5 comments.** It is the closest methodological analogue (prefix manipulation, hack rate on the next task, four models, 40 per cell).
- **The drift post's length control was essentially null.** Wikipedia prefixes of about 40k and 100k tokens gave results where "nearly all conditions have error bars that overlap with the baseline". Its honeypot-free prefixes were noisy too. The proposal's longest prefix is roughly 20-25k tokens of context.
- **The baseline on the reused probe is low.** The post's footnote gives DeepSeek v4 Pro hardcoding at 12.2% in the binary-reward-plus-rules `is_prime` setting. Making the tests writable drops it to 0.04%, and an AskUserQuestion tool to 0.4%.

## 1. Would it get upvoted?

Probably not above 50 as designed. My estimate is about 25% for >50 karma, conditional on a clean run.

- **Reference class.** The drift post (27 karma) is the same shape of result. The task-gaming post got 100 with Nanda as co-author, a dozen environments and rich transcript forensics. A five-cell prompt study by an unknown author sits nearer the former.
- **Positive result.** "Scripted rejections on earlier tickets raise cheating on the next ticket by 20 points, with reasoning quoting the rejections" would be read by the task-gaming authors, 1a3orn and people building long-horizon scaffolds. I would put that write-up at 50-90 karma. It needs the transcripts to show desperation rather than a blander mechanism (see section 3).
- **Null result.** "Cross-task verdict history does not matter" is a null about a mechanism nobody quite proposed. The context-rot example and the emotion-feature evidence are both within-task. I would expect 15-35 karma.
- **Length result.** Either outcome is weak: a null at 25k tokens repeats the drift post's null at 100k, and a positive would be doubted for the same reason.

## 2. Naturalness

The question is mainline: the task-gaming authors asked for exactly this disentangling. The operationalisation is a side-branch of it.

- **The authors' phenomenon is within one task.** The agent rejects a cheat at steps 27 and 63 and takes it at step 112 of the same optimisation problem, while repeatedly trying and falling short. "Trying and failing" there means iterating against a target it cannot hit.
- **The proposal tests something else.** Verdicts arrive on separate, finished tickets with "No resubmission; next ticket". The agent never struggles. That is a "bad day at work" manipulation, closer to the drift post's prefix design than to context rot.
- **The proposal knows this.** Section 5 says a null would point "instead at within-task struggle", and section 6 defers the within-task version to stage 2 at $1,500. The more natural experiment is the one deferred.
- **A cheap within-task version exists.** It does not need Performance Dashboard rollouts; see section 5.

## 3. Pre-mortem

Forecast for the design as written:

| Outcome | Probability |
|---|---|
| Clear positive (failure effect of 15+ points pooled, consistent across at least three models, supported by reasoning) | 15% |
| Clear null that is tight and believed | 25% |
| Ambiguous mush (one model only, floor effects, effect present but explained by a confound) | 45% |
| Fails to run or runs too late to analyse | 15% |

Specific failure paths, most likely first:

1. **Deference confound.** Three or six rejections tell the agent "my solutions are wrong more often than I think". The probe then shows a visible test that contradicts the spec. A rational agent that has just been wrong repeatedly should trust the test over its own reading and code to the test. That produces the "failure effect" with no desperation involved, and the state-based detector cannot tell the two apart. The mirror image also holds: accepted histories raise self-confidence and may raise bad-test flagging. The proposal's judge categories (frustration, score talk) do not include this one.
2. **Floor.** With a 12% baseline on the post's own probe, n=60 gives about 76% power for a 20-point rise and little for anything smaller. The pilot filter (15-85% at n=10 per model per probe) cannot measure a 12% rate; 10 sessions give 0-3 cheats by chance either way. Per-model selection on a noisy pilot also invites regression to the mean in the main run.
3. **Power is overstated.** At a 30% baseline, n=60 per cell gives about 61% power for a 20-point gap, and 40% for 15 points. "A 20-point gap is detectable per model" is generous. The pooled ±6 points holds only if models are homogeneous and both K levels are pooled; with three probe tasks and five models as clusters, the honest interval is wider.
4. **The outcome is under-defined.** The proposal counts "editing the bad test" as cheating. In the source post the tests are read-only, and making them writable is treated as a legitimate exit that nearly eliminates hardcoding. Correcting a wrong expected value to match the spec is arguably the right action. Separately, the `conflicting` split has two asserts on the same input, so special-casing cannot pass; only `oneoff` matches the proposal's description. Neither choice is stated.
5. **Probe difficulty.** The impossible LiveCodeBench items I sampled are `lcbhard_*`. A model that cannot solve the problem legitimately fails several tests, and "cheating" becomes generic hardcoding of failing cases rather than a response to one wrong test. That is a different behaviour from the `is_prime` setup and mixes capability into the outcome.
6. **Format shift flags the probe.** Prefix tickets have hidden tests and a verdict tool; the probe has visible tests and all-or-nothing credit. The change itself may register as "this one is the test". A constant "19/24" on every rejection is also a tell.
7. **Weak dose.** One-line verdicts on finished work, in a session of about 20k tokens, may simply not move anything. The original example took 112 steps of real struggle.
8. **Harness.** The NOTES file says the mapping from the post's ImpossibleBench environment to a directory in `agent-interp-envs` is unverified, and most environments there expect an Anthropic autorater key. A multi-ticket queue in one container with scripted verdicts is new code. Agents can build it in half a day, but the pilot, a redesign after the pilot, and the grid then compete for the second day.

## 4. Cost check

The $280 estimate is low; I estimate **$400-550** for the grid as written.

- **Output tokens are underestimated.** The model assumes about 12k output for seven tickets, under 2k per ticket including reasoning. Reasoning models solving medium LiveCodeBench problems with bash typically spend several thousand reasoning tokens per ticket. At 5-8k per ticket, K=6 sessions produce 35-55k output: about $0.15-0.20 on Kimi and GLM-5.3 (both near $3.50/M out) and $0.35-0.55 on GPT-6.1 Sol.
- **Turn count is underestimated.** Four turns per ticket assumes write-and-submit. Agents with bash write and run their own tests; 6-10 turns is more realistic, which roughly doubles to triples cumulative input.
- **Caching.** DeepSeek at $0.90/M input is the largest line. Its cache-read price is $0.25/M, but the per-session figure of $0.20 is already near the cached price for the stated tokens; with realistic turn counts it is $0.40-0.60.
- **Judge costs are fine.** Haiku 5.5 at $0.10/$0.50 over about 1,400 probe transcripts is under $10.

The design I recommend below has shorter sessions and fits in about $300-350 with margin.

## 5. Recommended changes

1. **Make the within-task manipulation the main experiment.** Use one ticket. Phase one has hidden tests and a `submit` tool that allows resubmission. Script R rejections ("Rejected: 23/24 hidden tests. You may resubmit.") with R in {0, 2, 5}. Then the test file is "released" and contains the one wrong expected value, with all-or-nothing credit. This is the tests-failing-again-and-again setting that both the emotion work and the context-rot example describe.
2. **Add a matched non-failure control for length.** Same R, but the tool returns a non-evaluative message ("Grader queue timed out; submission not scored. Please resubmit."). Report actual token counts per arm and include them as a covariate, since agents will rework code more after rejections.
3. **Keep one cross-task contrast, not four cells.** K=4 accepted versus K=4 rejected, plus K=0. Drop the K=3 versus K=6 split and stop presenting this as a test of length; cite the drift post's 40k/100k null instead. This shows whether failure carries across tasks or only acts within one.
4. **Handle the deference confound explicitly.** Add judge categories for "trusts the test over the spec because earlier answers were wrong" and for "says the test is wrong and hardcodes anyway". Record whether the agent states the correct value for the conflicting case before submitting. Only cheats where the agent has identified the test as wrong count toward the desperation account.
5. **Pin the probe.** Use the post's `is_prime` wrapper style with read-only tests and the `oneoff` type. Choose probe problems the model solves legitimately at least 90% of the time on the `original` split, so the only obstacle is the bad test. Fix the outcome definitions before the pilot: special-casing, tampering with the harness, flagging, honest submit.
6. **Fix the pilot.** Run 30 sessions per model on a fixed probe set at R=0 and choose one prompt variant (the no-rules, binary-reward one is likely higher than 12%) that gives 25-60% for at least three models. Select probes on pooled data, not per model.
7. **Cut models to fit power.** Three open models with visible reasoning (DeepSeek v4 Pro, GPT-OSS-120B, Kimi K2.7 Code) at n=100 per cell beats five models at n=60. Run GPT-6.1 Sol on the two extreme cells only, if budget remains.
8. **Vary the rejection text.** Different pass counts and wording per rejection, and the same ticket format throughout.
9. **State the comparison with the drift post honestly in section 1**: its karma, its null length control, and that its authors list "more hypotheses about prefix properties" as ongoing work.
10. **If only one experiment in this cluster can be funded**, I would rank this below a proposal with frontier-model results and a mainline author request behind it, unless change 1 is adopted. With change 1, a positive result gives a dose-response plot of cheating against number of scripted failures with a length-matched control, which is the figure the task-gaming authors asked for.
