# Feedback: Does driving NLA reconstruction error down surface reasoning, or only a better copy of the prompt?

Verdict: keep, with real changes. The question is the right one, but one reused dataset is not public, the most likely result is predictable from how the reconstructor is built, and the design does not yet separate "reads the intermediate" from "the verbalizer does the sum itself".

## What I checked

| Claim | Status |
|---|---|
| CoT post: 16% chain-of-thought-like, 0/78 wrong outputs singled out, rock beats all three NLAs on variants, best-of-10 Sonnet confabulation matches, regex agrees >98%, "just making the reconstruction loss go down" | Confirmed in the post text. |
| `syvb/nanonla-qwen3-8b-L24-av`, `-ar`, `-rl-lora` (`p0.0` etc.), `marco-bazzani/Qwen3-8B-nla`, `asher577/easynla-warmstart-data` | All exist on Hugging Face, ungated. |
| EasyNLA is public, targets Qwen3-8B L24, continues RL from an adapter with a KL reference | Confirmed from the README and `configs/rl_vllm.yaml` (default KL 0.01, AR co-trained). |
| 145 s/step at 256 x 8 on 4x A100 for a 9B model | Confirmed on the `therem/qwen3.5-9b-nla-L21-av-rl` model card. |
| Sonnet 5.5 at $2/$10 per M tokens | Confirmed on OpenRouter (batch $1/$5). |
| RunPod A100 80 GB at $2.09/h | Not verified: my fetch of the pricing page failed. |
| Competition-math set is at github.com/rgreenblatt/no_cot_math_public | **False.** The repo README says: "I've intentionally not included the math dataset I use to reduce the risk of contamination, please contact me for this data." The proposer's notes say the repo was "not fetched". |
| Nobody has done this | No arXiv or LessWrong hit for RL-specialising an NLA on a reasoning distribution and measuring what the verbalizer then says (arXiv phrase searches; LessWrong titles since 28 Oct). Closest remain 2610.30934 (RL on activation differences for Taboo) and the identification-vs-explanation papers. |

Three things from the artifacts that the proposal does not account for:

- **The `p0.0` adapter is not an EasyNLA adapter.** It is LoRA r=16 on q/k/v/o with base path `/workspace/nla/ckpts/av_sft` (nanoNLA). EasyNLA's RL default is r=128 rsLoRA, and its "continue the same adapter" path assumes its own SFT adapter. The README warns that starting RL from a fresh LoRA on a merged AV costs about 12 pp FVE at step 0. Expect to merge `p0.0` into the AV and eat that cold start, or to write glue code.
- **The public 9B run shows RL gains are mostly AV-AR co-adaptation.** Against a frozen AR the RL AV gained only +0.022 FVE; the 0.786 headline comes from the co-trained AR. The card also says "most of the reconstruction comes from the explanation quoting the last few source tokens verbatim".
- **That quoting trick is worthless here.** At the last position before the answer, the trailing tokens are identical across all settings of a template. Within-template variance is exactly what current NLAs do not capture, so baseline FVU against the template mean will be above 1 and the starting point is far away.

## 1. Would it get upvoted?

Probably, if it lands cleanly: 50-80 karma is plausible, with a wide spread. The cluster's posts got 209, 125, 82 and 56; the roughly 20 follow-up NLA posts in the notes mostly got 3-31. What separates the two groups is a sharp question tied to a claim people care about, and this proposal has one: it tests a conjecture made by Hu and Greenblatt and repeated by a commenter.

- A positive result (intermediates and wrong answers surface after cheap specialisation, with evidence of reading) would be a clear >50 and likely >100.
- A negative result ("FVU drops below the rock and the extra bits are all prompt constants") is the outcome that 2610.18727, 2610.32691 and 2607.20379 already predict. It is worth maybe 30-60 karma as the first direct demonstration on a reasoning task, and only if the figure is clean.
- "Could not get FVU below 1 in 400 steps" will not earn 50. The obvious reply is "train longer"; the proposal's claim that this is a third publishable outcome is too generous.

Who cares: the NLA authors, Greenblatt and Hu, and people deciding whether NLAs are worth using for monitoring opaque reasoning.

## 2. Naturalness

Mainline. It is the first thing the CoT post says to try. I found no one who has done it. The templated-arithmetic substitution for competition math is a reasonable move to get ground truth, not a contrivance.

The contrived part is the claimed transfer to "the ~900 real competition problems", which cannot be run as written (see above).

## 3. Pre-mortem

**Why the default expectation is "prompt inversion".** The AR is the first 24 layers of the target model plus a linear head. If the verbalization states the template and constants exactly, the AR can in principle recompute the activation, intermediates included, without the AV ever naming them. Reconstruction pressure therefore has a cheap global optimum that contains no reasoning. This is the proposal's "clear negative", and I put most of the conditional mass on it.

**Why a rise in S_intermediate would not mean much.** The AV is a full copy of an 8B model writing a paragraph. Once it writes the constants, it can compute a one-step intermediate in its own text, which is a chain of thought by the verbalizer and not a reading of the target. The within-template subtraction does not remove this. Of the three "read or recompute" checks:

- (i) Wrong-answer tracking is the only strong one, and it is about the answer, not the intermediate. The model's "actual" wrong intermediate is unobserved.
- (ii) The probe split is confounded by difficulty: items where the probe fails are items where the AV would also fail to recompute.
- (iii) Mean-difference steering that moves the model's answer through an intermediate is unlikely to work cleanly in half a day. The CoT post's own steering control (11/65 vs 10/65 with a random problem's vector) shows how uninformative this gets.

**Other specific failure points.**

- *Position, not just layer.* The intermediate may be computed at operand positions or across the five problem repeats, and only the answer (or nothing yet) may sit at the last position at layer 24. The CoT post's footnote found Gemma's answer undecodable at the NLA layer, which is at the same relative depth (41/62 vs 24/36). The phase-0 gate scans layers only.
- *The layer-move fallback is a new NLA.* "Re-extract warm-start activations, short SFT" at L* means regenerating 371k activations and retraining AV and AR. The notes price a full Qwen3-8B NLA at $65-85 and 12-16 H200-hours. It is not in the budget or the two-day schedule.
- *Too little in-domain signal.* 400 steps x 64 prompts, half of them math, is 12,800 math prompts: one eighth of the data the 9B run used to gain +0.02 FVE against a frozen AR. Beating the rock within templates may need far more.
- *Infra.* The fast path needs a patched vLLM 0.19 venv, IPC weight sync with a specific allocator setting, bf16-merged checkpoints, and four GPUs. The single-GPU fallback is 4-bit and slow. Budget a day, not half a day, for the first clean step.
- *Out-of-distribution input.* The NLA was trained on web-text prefixes. A 10-shot prompt with the problem stated five times, ending on a fixed answer cue, is far from that; baseline verbalizations may be generic "numeric answer follows" text for every item.
- *Baseline comparability.* The CoT post never ran a Qwen3-8B NLA (only an activation oracle), and its Qwen2.5 NLA was "pretty useless". There is no published number to compare against.

**Forecast.**

| Outcome | Probability |
|---|---|
| Clear positive (intermediates or wrong answers surface, with evidence of reading) | 8% |
| Clear negative, still interesting (FVU < 1, gains are constants; or intermediates appear but track the correct value, not the model's) | 32% |
| Ambiguous (FVU moves a little, S values within noise, checks disagree) | 40% |
| Fails to run or never gets FVU below the rock | 20% |

## 4. Cost check

The line items are internally consistent, but two are thin.

- Debugging at 20 A100-hours is 5 wall-clock hours on the 4-GPU pod. I would budget 40-60 GPU-hours ($85-125).
- The 36 s/step figure assumes linear scaling from batch 256 to 64; fixed costs (weight sync, eval every 10 steps) do not scale. Assume 50-60 s/step, so about $50 per run.
- Checkpoint evaluation (8 checkpoints x 3 runs x ~7,500 items) needs injection through the same vLLM stack; add about $30.
- The API lines are fine ($65), though the grading target changes with the dataset.

My estimate: $430-550 as written, so at or over the cap. Moving layers adds $80-150 and breaks it. With the cuts below it fits in about $400.

## 5. Recommended changes

1. **Replace the competition-math transfer step.** The dataset is not downloadable and the team cannot email the author. Use a public substitute (Hendrycks MATH level-1 prealgebra, or one- and two-step GSM8K items filtered to 30-80% no-CoT accuracy) and say plainly that this is not the post's dataset. Drop "repeat the earlier post's eval" from the framing.
2. **Add a 100% in-domain arm and make it the headline.** The sharpest test of "just lower the loss" is: overfit the NLA to the math distribution until within-template FVU is well below 1, then ask what it says. If even that only buys constants, the conjecture fails in the most favourable case. Keep one mixed run for held-out behaviour; drop the second seed (C) to pay for it. Use fewer templates (20-30) and more steps per template, and state a pre-set stopping rule (for example FVU < 0.7 or 1,000 steps).
3. **Add a prompt-only skyline.** Feed the AR the exact problem text (and, separately, "template name + constants") and report FVU. This tells readers how far constant-stating alone can go and turns the negative result into a quantified one. It costs almost nothing.
4. **Fix the read-vs-recompute design.**
   - Make wrong answers the primary evidence: S for the model's wrong answer against S for the correct answer, with at least 500 wrong items.
   - Add a "no-activation AV" control: give the trained AV a mismatched activation from the same template plus nothing else, and separately measure how often the AV names the intermediate when it names the constants correctly versus incorrectly. If intermediate mentions are fully explained by correct constant mentions, that is recomputation.
   - Replace mean-difference steering with a frozen-AR and frozen-AV ablation (which half moved?) or cut it. Report it as exploratory if kept.
5. **Extend phase 0 to positions and pre-commit the layer decision.** Probe the last 5-10 positions as well as layers 16-34. If the intermediate is not linearly decodable at layer 24 at the last position, do not retrain an NLA at a new layer in stage 1: restrict to templates or positions where it is decodable at layer 24, or stop and report the probe map.
6. **Decide the adapter path before renting four GPUs.** On one cheap GPU, load the syvb AV, AR and `p0.0` into EasyNLA and reproduce held-out FVE of about 0.585. If the adapter does not load, merge it and use `marco-bazzani/Qwen3-8B-nla` as the cross-check, accepting the cold start. Log the KL term and the AR-frozen FVE at every checkpoint, since co-adaptation is where gains came from in the public run.
7. **Rewrite the success criteria.** Remove "cannot reach FVU < 1 in 400 steps" as a publishable outcome. State numeric thresholds for S_intermediate against the generic-RL control and against the recomputation control.
8. **Re-check the RunPod price** and raise the debugging line; target about $400 after dropping run C and the Sonnet rubric grading on a dataset that no longer exists.
