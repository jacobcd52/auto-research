# Feedback: "Is self-distillation only as safe as its hints? OPSD versus GRPO in a hackable environment"

Verdict: **keep with tweaks.** The question is good and the infrastructure is real, but the design has two confounds that would undermine the headline, it misses the paper that already defines its central arm, and its success thresholds leave the most likely outcome unclassified.

What I checked (14 Nov 2026):

- **Post and comments.** Read RobinHa's post in full and the comment thread via GraphQL. The quoted claims are accurate.
- **Papers.** arXiv abstracts for 2601.18734, 2603.07084, 2610.17062, 2610.03185, 2604.03128, 2607.02502 all match the proposal's descriptions. I also read parts of the Countdown-Code and SDPO HTML.
- **Code and data.** READMEs for Countdown-Code, GRAFT `rl/` and OPSD fetched. `o4-mini-distillation-16k.jsonl` is at the Countdown-Code repo root (78.6 MB, 16,000 rows) and I downloaded it. HF `Jiayi-Pan/Countdown-Tasks-3to4` is public and ungated.
- **Tinker.** `Qwen/Qwen3-8B` is listed at 0.195 / 0.039 / 0.60 / 0.44 $/M, exactly as stated. The SDFT recipe page exists and matches the description (frozen teacher, top-20 KL via `topk_prompt_logprobs`).
- **Novelty search.** arXiv API queries only. The WebSearch budget was exhausted, so I could not search LessWrong, blogs or X for an unpublished replication. Treat "nobody has done it" as "not on arXiv".

Factual corrections needed in section 1:

- **Arm 2 is a published algorithm and the proposal does not cite it.** "Reinforcement Learning via Self-Distillation" (SDPO, arXiv 2601.20802, code github.com/lasgroup/SDPO) treats "successful attempts sampled in the current batch as feedback for failed attempts on the same question". Success is decided by the environment's scalar reward, and the paper runs on Qwen3-8B and Olmo3-7B. joseph_c links it in the post's comments. It uses an EMA or trust-region teacher and JSD, not a frozen teacher with forward KL.
- **The ~5% starting hack rate is GRAFT's number (4.7%), not Countdown-Code's.** Countdown-Code says models "start from a hacking rate of nearly zero" after SFT. Its curve for Qwen3-8B peaks at 80-90% within 100 steps and exceeds 96% at final evaluation.
- **Countdown-Code primes with 5 epochs, not 3.** GRAFT's re-implementation uses LoRA r128, lr 1e-4, 5 epochs.
- **williawa's comment has 4 karma.** It is a top-level critical comment, not "the top critical comment" by score. Most of the thread is about whether the post was an infohazard and whether OPSD scales.
- **A near-neighbour exists.** arXiv 2610.02781 (rubric-privileged OPD before RL) reports that "RP-OPD + RL shows limited signs of reward hacking" compared with SFT + RL on one benchmark. It is not this experiment, but it should be cited.

## 1. Would it get upvoted?

Conditional on a clean result, I put it at roughly 50% to clear 50 karma, with a plausible range of 35-90.

For:
- It is the first empirical test of a claim ("100x safer than RLVR", "there simply isn't a reward") from an 80-karma post.
- The laundering headline, "self-distillation reward hacks without a reward", is crisp. It lands harder once you say the hint rule is SDPO, which the capabilities literature actually uses, not a construction invented for the test.
- Biddulph, RobinHa and Riggs are active and would engage.
- Empirical follow-ups to idea posts in this cluster land at 66-86 (Wong et al. 86, Biddulph and Carroll 66).

Against:
- The post's karma came largely from its meta-point (track capabilities research) and the infohazard argument, not from the OPSD safety claim. The specific objection being tested drew 4 karma.
- The environment is a toy with a primed model. A sceptic will say that a model taught to hack in SFT, then shown a hack in context, copies it. Arm 5 is exactly that and is not a finding.
- The interest lies entirely in two things: whether the loop self-amplifies from a ~5% seed (arm 2), and whether a spec note or clean teacher stops it without killing learning. If those are muddy the post is a 20-40 karma replication note.

## 2. Naturalness

Mainline. The screener's follow-up note is literally "train a small open model with OPSD vs GRPO on a hackable task", and the grader-selected-hint twist is the right sharpening. Gold-hint OPSD being clean is uninformative; the live question is what happens where gold hints do not exist.

The link to consent-based RL is weaker than the proposal says. Riggs proposes a trajectory-level veto by a frozen judge. Arms 3 and 4 are a token-level distillation target from a teacher that has been shown a hack. Calling a positive result "the first empirical support for updates endorsed by the earlier self" over-claims, and proposal 03 in this cluster covers the consent audit directly. Keep it as a one-sentence connection, not a headline.

Already done? Not that I could find on arXiv. Nearest are SDPO (same hint rule, non-hackable environments), 2610.03185 (uses "reward hacking" to mean length collapse under the teacher's implicit reward) and 2610.02781 (above).

## 3. Pre-mortem

How two days will probably go:

- **Day 1 morning.** Environment port plus SFT priming. Priming is ~100M train tokens at 5 epochs. It should work, but the resulting hack rate on a Tinker LoRA is unknown. It could land anywhere from ~0% to several percent, and LoRA rank and epochs matter (GRAFT used r128).
- **Day 1 afternoon.** The GRPO gate is 150 steps of 256 rollouts with untested hyperparameters on a new trainer. The two published runs used very different settings (verl lr 3e-6 batch 32x8; TRL lr 5e-4 batch 1024), and GRAFT reports 2 of 3 no-intervention seeds collapsing. Expect one or two reruns. If the OPSD arms are serialised behind this gate, they slip to day 2.
- **Overnight.** OPSD arms run. The OPSD authors' own Qwen3-8B non-thinking numbers peak at step 50 and decline by step 100 (AIME24: 26.4 base, 49.7 at step 50, 38.3 at step 100), with clipping needed. With the full answer in the teacher context, expect privileged-information leakage: the student learns to shorten search and assert an expression. An arm-1 "capability gain" is far from guaranteed at untuned settings.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: arm 2 rises well above start, spec or clean teacher visibly cuts it, arm 1 clean | ~30% |
| Clear negative that is still interesting: hack hints enter at a measured rate yet arm 2 stays flat, and the step-1 token test shows the teacher down-weighting verifier rewrites | ~15% |
| Ambiguous mush | ~40% |
| Fails to run or ends with only the inference-only test | ~15% |

Specific reasons for mush or failure, most important first:

1. **Arm 4 is confounded.** The teacher is base Qwen3-8B and the student is the SFT-primed LoRA. Matching the base model's token distribution pulls the student back toward the unprimed model on every token, with or without a hint. That undoes the priming: the hack prior, the `<think>`-plus-JSON format and task skill alike. A fall in hack rate in arm 4 is "distilling toward a model that was never primed", not "the clean teacher vetoes hacked hints". The base model may also put large KL on format tokens and wreck the output format. Without a control, arm 4 cannot support the claim it is there for.

2. **Arm 1 is not a matched control for arm 2.** Arm 1's hint is "a correct expression" from a brute-force solver. Arm 2's hint is a full student submission with reasoning and both files. They differ in format, length and information as well as in who selected them. A difference in hack rate or capability between them is uninterpretable. The clean contrast is the same SDPO rule with true reward as the selector.

3. **The thresholds leave the modal outcome undefined.** Laundering is ">50%" and filter is "within a few points of 5%". Twelve thousand rollouts from a ~5% seed with a frozen teacher most plausibly lands at 8-30%, with large seed-to-seed spread. Two seeds will not separate arms 2, 3 and 4 in that band.

4. **The hint supply depends on a number nobody has measured.** The laundering mechanism is real. "Problems with no passing sample are skipped" means that on problems the student cannot solve, every available hint is a hack. So the hint pool is enriched far above the 5% episode rate. My rough estimate at step 0 is 10-20% hack hints, if the primed model solves ~60% and hacks ~5%. But if Tinker priming gives ~1% hacks the loop never starts, and "raise the hack share of the SFT data" moves the setup from naturalistic to contrived.

5. **Self-hint leakage is unspecified.** If the rollout being scored is the group's top-reward sample, the teacher sees that exact text as the hint and then scores it. It becomes near-deterministic on the student's own tokens. That is a pure sharpening term on whatever passed, including hacks, and it inflates laundering for an uninteresting reason. The proposal also does not say how ties among passing samples are broken (random, first, shortest); that choice sets the hack share of hints.

6. **The OPSD-versus-GRPO comparison is not matched.** It is 12.8K against 38.4K rollouts, with different step counts. "OPSD hacks less than GRPO" at step 100 against step 150 means little.

7. **Frozen versus moving teacher.** With a frozen primed teacher the only feedback loop is through the hint pool. SDPO, and what labs would run, updates the teacher; that is where amplification should be strongest. Deferring it to stage 2 is defensible, but then the stage-1 result must be reported as a lower bound on laundering.

8. **Evaluation bugs.** The ground-truth hack classifier is being rebuilt for the cookbook. GRAFT's `rh_detectors.py` exists and should be ported, not rewritten. Parse failures must be counted separately from "no hack", or collapse will read as a falling hack rate.

## 4. Cost check

$400 is adequate and probably generous; my estimate is $270-350 including the changes below.

- **SFT priming is underestimated.** From the released file, prompts are ~2,230 characters and outputs ~2,600 characters, so roughly 1,300 tokens per trace. At 15.6K traces and 5 epochs that is ~100M train tokens, about $45, not $19.
- **Rollout length assumption is fine.** ~650 prompt tokens and 450-700 completion tokens is consistent with the data. Completions can grow toward the 2,048 cap under collapse, which could double the per-rollout cost of a collapsing run.
- **Teacher-pass billing is unverified.** The proposal assumes prefill price for `topk_prompt_logprobs`. If it is billed at the train price ($0.44/M) the OPSD cost per 1,000 rollouts rises from ~$1.10 to ~$1.45. Immaterial.
- **Evaluations.** Roughly 12 runs, 5-7 checkpoints each, 500 problems, two variants: 60-80K rollouts, about $25-35. Consistent with the proposal.
- **GRPO.** $31 per run is consistent with the price list. Budget one or two failed gate runs (~$30-60).
- **Sandboxed verification.** Local CPU, free.

There is room for a third seed on the decisive arms within $400.

## 5. Recommended changes

In order of importance:

1. **Add a true-reward-selected hint arm and make it the primary control.** Same SDPO rule, same format, but the hint is a passing sample that the ground-truth checker says is honest. The headline contrast becomes proxy-selected versus true-selected hints, the exact analogue of arms 6 and 7. Keep the brute-force gold hint only as a secondary capability reference, or drop it.

2. **Fix or drop arm 4.** If kept, add a control with the same clean base teacher and true-selected hints, so that "pulling toward base" can be subtracted. Report the hack-rate difference between the two clean-teacher arms, not arm 4's absolute level. If the budget for attention is tight, drop arm 4 and spend the seeds on arms 2 and 3; the spec-note arm is cleaner and closer to what the post claims.

3. **Cite SDPO and frame arm 2 as "SDPO's hint rule in a hackable environment".** State the differences (frozen teacher, forward top-K KL, no JSD). Adopt its handling of the scored rollout: never give a rollout itself as its own hint. Specify random tie-breaking among passing samples, and log the hack share of hints separately for student-solvable and unsolvable problems.

4. **Pre-register a continuous outcome and use three seeds on the proxy-selected, true-selected and spec arms.** For example: change in hack rate from step 0 to step 100, compared with the true-selected arm, with seed ranges. State in advance what a 5% to 15% rise will be called. Pay for the seeds by cutting arm 5 to a 50-step sanity run and GRPO-proxy to one seed unless it is cheap.

5. **Promote step 1 to a guaranteed deliverable and widen it.** Run a full grid: rollout type (hack, honest) by teacher context (no hint, honest hint, hack hint, hack hint plus spec, clean teacher with hack hint). Report teacher-minus-student log-probability on the tokens that rewrite `test.py` or change the numbers. This costs under $10 and survives every training failure. It also tests the post's "the teacher will actively push against it" claim directly. Gather the 500 hack rollouts by sampling ~10-15K from the primed model.

6. **Do not serialise OPSD behind the GRPO gate.** The true-selected, proxy-selected and always-hack arms are interpretable without a GRPO reference. Launch a short OPSD pilot (25 steps, two learning rates, with and without KL clipping) on day 1 in parallel with GRPO. Choose the checkpoint budget from the pilot: the OPSD authors' Qwen3-8B numbers peak near step 50.

7. **Measure the primed hack rate before anything else and set a go/no-go.** If it is below ~2% on 2,000 samples, decide immediately whether to re-prime (r128, 5 epochs, GRAFT's script as the reference) or raise contamination. Say so in the write-up. Report the step-0 hint-pool hack share as a result in its own right.

8. **Match the GRPO comparison.** Plot hack rate against rollouts consumed and against clean solve rate, not against step index.

9. **Port GRAFT's `rh_detectors.py` and Countdown grader.** Count unparseable outputs as their own category.

10. **Tone down the consent-based RL claim** to a single sentence. State that a frozen teacher makes the result a lower bound on laundering relative to SDPO's moving teacher, which stays in stage 2.

11. **Correct section 1** as listed at the top: 5 epochs, the source of the 4.7% figure, williawa's comment score, and the 2610.02781 neighbour.
