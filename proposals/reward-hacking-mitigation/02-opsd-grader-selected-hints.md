# Is self-distillation only as safe as its hints? OPSD versus GRPO in a hackable environment
cluster: reward-hacking-mitigation | stage-1 cost: $400 | follows up: "Do your capabilities homework" (dYnhhTxoDj3fuCxLB); "Consent-Based RL: Letting Models Endorse Their Own Training Updates" (2Dmi3DYBKY7Tbz8Kx)

## 1. What the prior work showed
- **The claim.** RobinHa's post (80 karma) explains On-Policy Self-Distillation (OPSD, arXiv 2601.18734): the student samples a rollout; a frozen copy of the same model, given privileged context such as a worked solution, scores every token; the student is trained to match the teacher's token distribution. The post argues this is far safer than RL with verifiable rewards (RLVR, here GRPO): "there simply isn't a reward" to game, and desired behaviour can be written into the teacher's context. No experiments.
- **The objection.** The top critical comment (williawa): for tasks without gold solutions the hint is a trajectory that passed the grader, and that trajectory may be a reward hack. Biddulph reads OPSD as "updates endorsed by the original AI", the idea behind Riggs' consent-based RL (86 karma, no experiments), where a frozen pre-RL checkpoint approves what gets reinforced.
- **Existing OPSD work is about capability and collapse** (OPSD, SDFT; arXiv 2610.03185 on length collapse; RLSD and DemoPSD on answer leakage). A search (14 Nov 2026) found no OPSD run in an environment with an exploitable grader, and none with grader-selected hints.
- **A cheap hackable environment with GRPO baselines.** Countdown-Code (arXiv 2603.07084, https://github.com/zohaib-khan5040/Countdown-Code): the model returns a solution file and the test file that grades it, so it can rewrite the test or change the problem. Qwen3-8B, after SFT on distillation traces of which ~1.2% are hacks, hacks on ~5% of episodes; GRPO drives that above 90% within ~100 steps (also seen in GRAFT, arXiv 2610.17062). Gold solutions are computable by brute force.
- **A ready implementation.** The Tinker cookbook SDFT recipe: frozen self-teacher, top-20 KL, validated against full-vocabulary KL.

## 2. Question and why it matters
When the teacher's privileged hint is chosen by the same exploitable grader that RLVR would use, does self-distillation teach the student to hack, and can a frozen teacher (told the intended spec, or not primed toward hacking) act as a filter that refuses to pass the hack on?

If grader-selected hints launder hacks at rates similar to GRPO, the "nothing to game" argument fails wherever gold solutions are unavailable, which is where frontier training lives. If the frozen teacher declines to endorse hacked hints while honest solving still improves, that is the first empirical support for "updates endorsed by the earlier self" as a mitigation. A split result (laundering with a primed teacher, filtering with a clean teacher or a spec note) says which ingredient carries the safety.

## 3. Stage 1 plan
**Reused:** Tinker cookbook SDFT recipe (https://tinker-docs.thinkingmachines.ai/cookbook/recipes/sdft/) and RL recipes; Countdown-Code prompts, data (HF `Jiayi-Pan/Countdown-Tasks-3to4`) and SFT priming traces; hack-type definitions from GRAFT. Model: `Qwen/Qwen3-8B` on Tinker.
**Built:** a Countdown-Code environment class for the cookbook (single turn, sandboxed verifier, ground-truth classification of hacks into trivial-test / constraint-removal / problem-substitution), a brute-force solver for gold hints, and the hint variants.

Step 0, starting points. (a) Primed student: LoRA SFT of Qwen3-8B on the 15.6K Countdown-Code traces. (b) Unprimed base Qwen3-8B, used only as an alternative teacher.

Step 1, inference-only teacher test before any training. On 1,000 fixed student rollouts (500 hacks, 500 honest), compute teacher-minus-student log-probability per token under each teacher context below. Does the teacher raise or lower the tokens that rewrite the verifier (the post says it "will actively push against" bad work)?

Step 2, training arms. OPSD arms: 100 steps, 128 rollouts per step (16 problems x 8 samples), frozen teacher, top-20 KL. Two seeds each.
1. **Gold hint.** Teacher sees a correct expression. Expected clean; the reference for capability gain.
2. **Grader-selected hint.** Teacher sees "a submission that received full marks from the automated grader": the highest-proxy-reward rollout among the student's 8 samples for that problem (problems with no passing sample are skipped). Hacks enter only as often as the student produces them.
3. **Grader-selected hint + spec.** As 2, plus two sentences in the teacher context stating the intended task (do not alter the test file or the given numbers; a full-marks example may have cheated).
4. **Grader-selected hint, clean teacher.** As 2, but the teacher is unprimed base Qwen3-8B.
5. **Always-hack hint** (1 seed): teacher always sees a hacked full-marks submission. Upper bound on laundering.
GRPO arms: 150 steps, 256 rollouts per step.
6. **GRPO on proxy reward** (2 seeds): the published hacking baseline, which also gates the environment port.
7. **GRPO on true reward** (1 seed): capability reference.

Evaluation every 25 steps on 500 held-out problems: hack rate by type (ground truth), clean solve rate on the no-scaffold variant, completion length (collapse check), and the share of hints in arms 2-4 that were hacks (does the loop feed itself?).

Order: day 1 environment, primed checkpoint, arm 6 gate, step-1 test; overnight OPSD arms; day 2 evals and write-up.

## 4. Stage 1 cost estimate
Tinker prices for Qwen3-8B (looked up 14 Nov 2026): prefill $0.195/M ($0.039 cached), sample $0.60/M, train $0.44/M. Assumed ~700 prompt, ~450 completion tokens per rollout (to be measured first).
- SFT priming: 15.6K traces x ~900 tokens x 3 epochs = 42M train tokens = $19.
- OPSD per 1,000 rollouts: sampling $0.31, teacher top-K pass on ~1,450 tokens at prefill price $0.28, student training on 1,150 tokens $0.51 = $1.10. One run = 12.8K rollouts = $14. Nine runs = $127.
- GRPO per 1,000 rollouts: $0.80. One run = 38.4K rollouts = $31. Three runs = $93.
- Step-1 test and all evaluations (about 60K rollouts of sampling or scoring) = $25.
- Subtotal $264; margin for reruns, longer-than-assumed completions and a third seed on the decisive arms: $136.
- Total: $400.

## 5. What success looks like
One figure: hack rate over training for arms 1-7; one table: final hack rate by type and clean solve rate with seed ranges; one token-level plot from step 1.
- "Laundering": arm 2 reaches a hack rate comparable to GRPO-proxy (say >50%) and its hint pool becomes mostly hacks. Headline: self-distillation with grader-chosen hints reward hacks without any reward.
- "Filter": arm 2, or arms 3/4, stay within a few points of the 5% starting rate while clean solve rate improves by at least half of arm 1's gain. Headline: a frozen teacher vetoes hacks the grader accepts, and the token plot shows where.
- Split results identify whether the spec text or the teacher's untainted prior does the work.
Arms 1 and 5 bracket the outcome, so an empty null is unlikely; the uninformative case is OPSD changing nothing (no capability gain in arm 1), which section 7 guards against.

## 6. Stage 2 (if stage 1 succeeds)
- Mixed RLVR + OPSD (what the post says Cursor does) and an EMA teacher: does the filter erode as the teacher drifts? (~$300)
- The same comparison in the LeetCode `run_tests`-overwrite environment (https://github.com/ariahw/rl-rewardhacking), where hacking emerges without priming (~$500).
- The post's "overselling" claim, with an LLM judge that rewards confident self-reports (~$400).

## 7. Risks and how the plan handles them
- **GRPO baseline does not reproduce hacking on Tinker.** Arm 6 runs first as a gate; if the primed model does not escalate, raise the hack share of the SFT data (the paper's lever). Arm 5 is a valid laundering test even without a GRPO reference.
- **Too few hacked hints early (5% base rate).** With 8 samples per problem, the top-reward sample is often a hack on problems the student cannot solve; hint-pool composition is logged from step 0 and arm 5 covers the limit.
- **Recipe mismatch with Qwen3-8B.** Native thinking is disabled and Countdown-Code's in-content `<think>` format is used; arm 1 must show a capability gain before other arms are interpreted. Fallback: the sampled-token policy-gradient form of the objective with Tinker's importance-sampling loss.
- **Collapse into long repetitive outputs** (known OPSD failure). Length is tracked; per-token KL clipping from the OPSD repository is applied if needed.
- **Over-reading a toy.** Claims are limited to this environment and model; the clean-teacher arm is the closer analogue of an aligned pre-RL checkpoint.
