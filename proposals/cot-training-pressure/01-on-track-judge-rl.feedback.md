# Feedback: 01-on-track-judge-rl — "Does an 'is the reasoning on track?' reward train models to stop admitting they are hacking?"

Reviewer verdict: **keep, with tweaks**. This is the most natural follow-up in the cluster and the only real threat to it is being scooped. The design has three fixable weaknesses: the baseline arm may lose verbalisation on its own, the step-0 gate measures the wrong quantity, and the cost is somewhat underestimated.

## What I checked

| Claim in proposal | Status |
|---|---|
| Appendix result (two models, contradictory tests, five judges, 20-50 points, vanishes with output, reverses for "predict tests pass") | Confirmed against the post text. Note the appendix appears to rest on **one coding problem and two transcripts** (one per model), hand-edited. The proposal does not say this; it matters for how much the step-0 gate can be assumed to pass. |
| Comments: Neel Nanda not worried; Buck reads it as value heads | Confirmed (Nanda 26 karma: Argon wording was bad; Buck: "really makes it sound like they're just using value heads ... totally fine"; Rauno Arike agrees on re-reading). |
| Kaufmann et al. 2603.30036, Baker et al. 2503.11926, SDF paper 2605.15257 has an RL section | Confirmed via arXiv abstracts. I did not verify the "monitor effects on gpt-oss within about 60 steps" figure. |
| Tinker gpt-oss-20b $0.18 / $0.45 / $0.396 | Confirmed on the Tinker pricing page (32K context). |
| OpenRouter Haiku 5.5 and GPT-6 Luna at $0.10 / $0.50 | Confirmed; batch variants are half price. |
| monitor-jailbreaking repo is public | `raw.githubusercontent.com/wusche1/monitor-jailbreaking/main/pyproject.toml` resolves and depends on `tinker` and `tinker-cookbook`. The README is an empty "ML Research Template" stub, so there is no documentation. I could not list the tree. |
| tinker-cookbook RL recipes | Confirmed, and better than stated: the cookbook has a **Code RL recipe with sandboxed execution** and an MBPP benchmark integration. This, not the monitor-jailbreaking repo, should be the base. |
| "Nobody has trained with such a judge" | Not contradicted. I scanned all LessWrong posts since 2026-10-28 by title and ran several arXiv keyword queries; no trained version of the appendix found. **Caveat: my general web-search budget was exhausted, so this check covers LessWrong and arXiv only** (not X, Redwood's blog or the Alignment Forum separately). |

Related work the proposal does not cite and should:

- **Yan and Hewitt, "Reward Misspecification Degrades Chain-of-Thought Monitorability" (arXiv 2610.28303, 2026-10-20).** Outcome-only RL that induces hacking already leaves CoTs that "keep reasoning about the task intent while the outputs violate the intent". Code is public. This is a direct threat to condition A (see pre-mortem).
- The cluster's own UK AISI post reports about 70% unfaithful hack CoTs on Qwen with **no** CoT pressure at all. Same threat.
- "Length Penalties Make Chain-of-Thought Less Monitorable" (2607.09786) and CATCH (2609.39533, a public coding reward-hacking testbed with execution-based gold labels, where a CoT monitor in training is evaded via code comments). Neither duplicates the experiment; CATCH is a possible ready-made environment.
- OpenAI's stress test of "rewarding confident CoT" (per NOTES) is the closest existing thing to an uninstructed process reward. The proposal lumps OpenAI's work under "explicit penalties"; it should say plainly that this arm exists and was run only on internal models.

## 1. Would it get upvoted?

Yes, probably, if it lands cleanly and soon. The parent post has 131 karma after four days, the appendix is explicitly a "quick demonstration", and the natural reader response is "so does this actually happen under training?". The five-line figure (verbalisation among hacks over training for A to E) is a result LessWrong readers can absorb in ten seconds. Posts in this cluster that ran real training experiments got 66-95 karma. I would put a clean positive at 70-120 karma and a clean negative at 40-70.

Two things cap the upside:

- The comment thread has already converged on "GDM is using value heads, which is fine". Condition B therefore tests a reading the post's own authors now think is probably wrong. The result must be framed as a test of the general claim (naive process judges and Kaufmann-style orthogonality) and not as evidence about Gemini. The proposal's risk section says this; the title and section 2 should too.
- The value of the post decays fast. A trained version posted by Redwood in the next few weeks would take most of the karma.

## 2. Naturalness

Mainline. It is the screener's suggested follow-up, it is what the appendix sets up, and it also answers Buck's review question (graders that see CoT versus not) at small scale. The condition set is well chosen: C and D are the two "safe" variants the appendix predicts, and E is a needed positive control.

Duplication risk is the main concern. Redwood has the task, the transcripts, the judge prompts and an intern who built them. I would put the chance that someone posts a trained version within a month at roughly 25-35%. "Ask in the comments before spending" is the right mitigation and should be a hard precondition, not a risk-table line.

## 3. Pre-mortem

How it likely plays out: the team adapts the cookbook Code RL recipe, builds the mixed MBPP environment in half a day, and runs step 0. gpt-oss-20b on single-turn MBPP with one corrupted test will produce a mix of behaviours: follow the spec and fail the bad test, special-case it, or get confused. With one round of prompt tuning the hack rate lands in range. Verbalisation is probably high at baseline because noticing the bad test is how the model arrives at the hack. The judge-bias replication is where the first real uncertainty sits. Training then runs; the question is whether B separates from A.

Rough forecast:

| Outcome | Probability |
|---|---|
| Clear positive (B's undetected-hack rate rises well above A, C and D do not, E works) | 25% |
| Clear negative that is still interesting (bias present at step 0, E moves, B does not) | 20% |
| Ambiguous mush | 40% |
| Fails to run or stops at the gate | 15% |

Specific ways it goes wrong, most important first:

1. **Condition A loses verbalisation on its own.** Yan and Hewitt and the AISI post both find that outcome-only RL on hackable tasks yields hacks that are not acknowledged in the CoT. Once special-casing is a learned reflex, the model has no need to reason its way to it, and the admission disappears without any CoT reward. If A falls from 80% to 30% verbalised over 100 steps, B has little room to separate and three seeds will not resolve the difference. This is the single most likely route to mush, and the proposal does not mention it.

2. **The step-0 gate measures the wrong thing.** Deleting hack-acknowledging sentences and re-scoring shows the judge's response to an edit. RL responds to the covariance between verbalisation and judge score **across on-policy rollouts of the same prompt**. The appendix transcripts were overt ("I will solve the problem via hacking"); gpt-oss-20b is more likely to write something like "the third test expects 7, which contradicts the spec, so I will handle that input separately". A judge may not mark that down at all. The gate can pass on edited transcripts while the on-policy signal is near zero.

3. **Signal-to-noise.** Even with a 20-point judge gap, the reward difference is 0.5 x 0.2 = 0.1 against a 0/1 outcome reward, with single-sample judge noise that is plausibly 10-15 points. Under GRPO group normalisation the signal only bites in groups where outcome reward is constant. About 30 hack rollouts per step for 100 steps is thin. E has a much sharper reward than B, so E succeeding does not show that B had enough power.

4. **The policy takes a third path.** Likely candidates: it writes generically "good-sounding" reasoning that raises judge score on all problems (reward goes up, verbalisation unchanged); it moves the admission into a code comment (CATCH observed exactly this); it stops hacking in C because a judge that sees special-cased code marks it down. These are reportable, but each needs its metric to be in place beforehand. In C and possibly B, hack rate may fall enough that "verbalisation among hacks" is computed on very few samples.

5. **"Verbalised" is not well defined at the margin.** Neutral descriptions of special-casing are the crux. If the held-out monitor counts them as verbalised, B shows no effect; if not, the baseline is already low. The 150-transcript hand validation is necessary but the rubric must be fixed before training, ideally as "can a monitor that reads only the CoT tell that the code will special-case a test?".

6. **Task ambiguity.** "One test edited to contradict the others" must mean a test whose expected value disagrees with the spec on a distinct input. If the same input appears with two expected values, no pure function passes and the hack rate is zero. Also, when the prompt says "your score is the fraction of tests passed", special-casing is arguably sanctioned, and both the policy's CoT and the judge's reaction change. The prompt-tuning fallback therefore interacts with the judge bias; the gate has to be rerun after any prompt change.

7. **Harmony format and reuse.** The monitor-jailbreaking repo is undocumented. The cookbook Code RL recipe is the safer base, but the team still needs to confirm that gpt-oss analysis-channel text is cleanly separated from the final answer in the Tinker renderer, since every condition depends on what the judge is shown.

8. **Scooped mid-run** by Redwood (see above).

The result is not "known either way": Nanda and Buck expect such signals to be benign, the post's authors expect a risk, and the appendix alone cannot decide it. That is the proposal's main strength.

## 4. Cost check

Unit prices are right. The token counts are optimistic.

- gpt-oss-20b reasoning plus code on an MBPP problem with tests in the prompt is more likely 1,200-2,000 sampled tokens than 900, and gets longer when the tests conflict. Training tokens scale with it. A realistic run is $25-35, not $17.5.
- Condition E needs a monitor call per rollout as well; small.
- Judge costs are fine, and could be halved with batch pricing if latency allowed (it does not, inside an RL loop).
- Held-out evals: 400 problems are claimed but only about 300 are built; MBPP has enough problems, but the split needs stating.

My estimate for the plan as written: **$450-600**, which is at or over the cap once the rerun margin is included. With the cuts below it fits in about **$350-420**.

Wall-clock is acceptable if runs go in parallel; each step has 128 samples, 128 judge calls and sandboxed execution, so allow 2-4 hours per run.

## 5. Recommended changes

1. **Make the Redwood check a precondition.** Comment on the post (or message the authors) before any spend; re-scan LessWrong on the day. If they are running it, switch to proposal 04 or to the value-head variant in point 7.
2. **Change the step-0 gate to an on-policy measurement.** Sample 8-16 rollouts per impossible problem, label hack and verbalisation, and estimate the judge-score difference between verbalised and non-verbalised hacks within a prompt, plus the judge's test-retest noise. Proceed only if the within-prompt gap is clearly above noise (say 10 points or more with a tight interval). Keep the deletion edit as a secondary check. Rerun after any system-prompt change.
3. **Deal with baseline drift in A explicitly.** Cite Yan and Hewitt and the AISI result. Make the headline the B-minus-A difference at matched hack rate, not B's absolute level. Reduce drift by training fewer steps (60), using a lower learning rate, or starting from a prompt where hack rate is already near its ceiling so outcome reward has less to teach. If A's verbalisation falls below roughly 50% in a pilot seed, stop and redesign before buying the other 13 runs.
4. **Run one pilot seed of A, B and E first** (about $90), look at the curves and transcripts, then commit the rest. This is the cheapest protection against mush.
5. **Trim to fit the budget.** Three seeds for A and B, two for C, D and E (12 runs); 60-80 steps; four checkpoints. Put any spare money into extra A and B seeds, since that contrast is the result.
6. **Reduce judge noise** by averaging two judge samples per rollout or asking for a score with a short fixed rubric at temperature 0. It costs about $2.50 per run and directly raises the signal that decides the experiment.
7. **Strengthen D, since the audience now cares most about value heads.** An LLM asked to predict test success is a weak stand-in. If time allows, add a cheap learned version: a small regression head or a LoRA classifier trained on step-0 rollouts to predict outcome reward from the CoT, used as the CoT reward. A result of the form "naive process judge suppresses admissions; value-style predictor does not, or increases them" is the version that speaks to the comment thread.
8. **Add metrics for the escape routes:** hack admission in code comments or the final answer, judge score on honest problems over time, and number of hacks per checkpoint so that rates on tiny denominators are flagged.
9. **Pin down the task and the label.** State that the corrupted test uses a distinct input with an expected value that disagrees with the spec. Fix the verbalisation rubric before training and define it as monitor detectability from the CoT alone.
10. **Base the harness on the tinker-cookbook Code RL recipe** (sandbox and MBPP already there); use the monitor-jailbreaking repo only as a reference for judge-in-the-loop reward. Consider CATCH as an alternative environment if the hand-built one misbehaves.
11. **Reframe the write-up.** Lead with "do uninstructed process judges train out hack admissions, and does 'orthogonal' predict safety?"; mention GDM only as motivation, with the staff denials and the value-head reading stated up front. Also say that the appendix rested on a single problem, so the step-0 replication across about 150 problems is itself a small contribution worth a figure.
