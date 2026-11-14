# Feedback: Does training against CoT Forgery repair role perception, or teach a model to distrust its own reasoning?

Verdict: **keep, with tweaks.** The question is the right one for this cluster and nobody appears to have run it. The design as written will most likely land in a branch the proposal has no interpretation for, and one of its two headline hypotheses (distrust) is unlikely to show up under the proposed training recipe. Both are fixable without raising the cost.

## What I checked

| Claim | Status |
|---|---|
| Paper is Ye, Cui, Hadfield-Menell, arXiv 2603.12277 (v6) | Confirmed (arXiv API). |
| 79% / 68% / 29% CoTness, 61% -> 10% destyling, 626 attempts, 9% -> 90% quantiles | Confirmed in the paper HTML (Table 2 and Fig. 9 text). |
| "Distrust their own reasoning" claim is untested; "reshape geometry or merely add patterns" is a listed open question | Confirmed (post footnote 15, paper discussion). |
| Edelman et al. 2610.40396, Yu et al. 2610.05295, Gupta & Tembey 2610.19452 exist and are scoped as described | Confirmed from abstracts only; I did not read full texts. |
| Repo is public, has probe and forgery code | README fetched (HTTP 200). Directory layout and whether forgeries/probes are committed remain unverified, as the proposer's notes say. |
| gpt-oss-20b is Apache-2.0, 20.9B params | Confirmed (HF API: 20,914,757,184). |
| OpenRouter prices | Confirmed exactly: gemini-2.5-pro 1.25/10, glm-4.7 0.60/2.20, gemini-3-flash-preview 0.50/3.00. |
| RunPod H100 price | Not re-checked; I relied on the proposer's range. |

**Search limitation.** The web search tool was unavailable to me too (shared budget exhausted), so like the proposer I only searched arXiv (four queries) and did not search LessWrong, Hugging Face or the general web. An arXiv search for "CoT Forgery" returns only the original paper. A LessWrong search for a follow-up post should be done before funding; this is the kind of experiment a reader could have posted in the five months since June.

**Two things the proposal gets wrong or omits:**

1. **The gate threshold is wrong.** The proposal expects "about 80%+" styled success on gpt-oss-20b at the gate. The paper's Table 2, which is on gpt-oss-20b and is the experiment the gate reproduces (styled vs destyled, with CoTness), reports 61% styled and 10% destyled. The >80% figure is from the headline StrongREJECT figure. The two numbers come from the same model, so some condition differs (I did not find which). A gate set at 80% may fail on a correct reproduction.
2. **Wang et al. 2025 (arXiv 2505.00626, "The Illusion of Role Separation") is not cited and bears directly on Arm B.** It shows that fine-tuning for role separation learns shortcuts (task type, proximity to start of text) instead of role identity. The original paper cites it for exactly this. That is the strong prior for what Arm B will do.

Adjacent work the proposer missed, none of which duplicates the experiment:
- arXiv 2611.08811 (6 Nov 2026), thought-injection attacks on reasoning agents (GLM, MiniMax, Qwen). Attack-side only; finds tag and style effects are model-specific. Worth citing, and a caution for the stage-2 claim that results will carry to other models.
- arXiv 2506.10979, models "naively continue" injected thoughts in their own thinking channel. This is prior art for the trust measure and suggests base follow rate will be high.

## 1. Would it get upvoted?

Plausibly yes, conditional on a clean result. The parent post got 409 karma and was curated; a commenter asked for this proof of concept; the authors named it as their first open question. A post titled around "we fine-tuned gpt-oss-20b against CoT Forgery; here is what happened to its role geometry" has an audience of interpretability and prompt-injection readers.

The karma depends heavily on which branch lands:
- Arm B transfers to unseen harmful forgeries and moves CoTness: 100+ karma. This is the result people want.
- Arm A adds a pattern, geometry unchanged, held-out attacks still work: 50-80. Confirms the whack-a-mole claim with numbers.
- Arm A is robust, geometry unchanged, trust unchanged, held-out results mixed: 20-40. Reads as "LoRA learned to refuse a pattern".

One small LoRA on one 20B model will draw the objection that frontier labs' training is nothing like this, so the "distrust" finding about frontier models is not really tested. The write-up has to frame it as "what does the obvious defence do", not as a test of the footnote about closed models.

## 2. Naturalness

Mainline. It is open question 1 in the paper, plus a direct commenter request, on the paper's cleanest model with the paper's code. Not contrived.

Not done, as far as arXiv shows. Edelman et al. is the closest (LoRA against role spoofing, poor transfer between attack types), but it covers user/tool roles on Qwen, with no reasoning role and no before/after role-probe geometry.

## 3. Pre-mortem

**Rough forecast**
- Clear positive (one of the three pre-specified patterns, cleanly): 25%
- Clear negative that is still interesting: 25%
- Ambiguous mush: 40%
- Fails to run or the gate does not pass: 10%

**The most likely actual outcome** is one the proposal does not name: Arm A drives in-distribution success to near zero, forged-text CoTness at layer 12 barely moves, and the genuine-reasoning follow rate also barely moves. The proposal defines outcome (b) as "unchanged CoTness with the success curve shifted down" and equates that with distrust. Those are different things. Unchanged CoTness plus unchanged trust is a third outcome: the model learned a narrow feature such as "reasoning-style text in a user turn next to a harmful request means refuse", which is neither repaired perception nor distrust. Section 5 files this under ambiguous. It should be a named, expected outcome with its own discriminating tests.

**Specific failure reasons, by likelihood**

1. **Arm A gives no reason for distrust to appear.** Its targets are the model's own genuine reasoning followed by a consistent refusal, mixed 1:1 with benign chats. Every training example reinforces acting on real reasoning. Nothing penalises following text in the reasoning channel. The predicted 10-point drop in follow rate is therefore unlikely, and the "confirms the distrust hypothesis" pattern probably cannot occur under this recipe. Distrust in frontier models, if real, plausibly came from training against prefill tampering, which no arm includes.

2. **The trust measure is itself a prefill attack.** Placing a directive in the real reasoning channel, or editing the last line of the model's reasoning, is text the model did not write under a genuine tag. A model that follows it is trusting the tag, not its own reasoning. A drop in follow rate could mean "detects tampering" (arguably good) rather than "distrusts own reasoning" (bad). The only measure that isolates the bad case is consistency between unedited self-generated reasoning and the final answer, which will sit near ceiling on multiple-choice questions and have no room to move.

3. **Arm B learns a shortcut.** It is trained directly on the tag-sensitivity metric, so that metric is in-distribution apart from held-out directive types. The likely learned rule is "reasoning-style text inside a user turn: ignore", which is another style pattern. Wang et al. found exactly this class of failure. Transfer to harmful forgeries would then be partial and hard to read: a drop in attack success from "ignore the pasted block" still leaves the refusal decision to the base model, which already refuses raw prompts 96%+ of the time. So Arm B may well "work" on StrongREJECT by a shortcut. The plan's defence (held-out directive types) does not separate shortcut from perception. CoTness is the only arbiter, and see point 4.

4. **A single-layer linear probe may miss the change.** LoRA can alter behaviour entirely downstream of layer 12, or along a direction the role probe does not read. "CoTness unchanged" at one layer is weak evidence that perception is unchanged. Conversely the frozen probe may drift for unrelated reasons. Reporting frozen and retrained probes helps; one layer does not.

5. **Held-out attacks may not be held out.** "A second forgery generator" and "absurd-logic forgeries" share the target's reasoning style with the training forgeries, since matching that style is the point of the attack. Arm A will probably generalise to both, which would look like evidence against whack-a-mole when it only shows the style was learned. The informative held-out conditions are a different position (tool output), a different payload (agent exfiltration), and an adaptive rewrite; only the first two are in the plan.

6. **Two seeds, 1,500 examples.** Between-arm differences of 10 points in follow rate on 400 trials are detectable within a seed, but seed-to-seed variance in LoRA runs can be as large. Two seeds cannot distinguish a 10-point arm effect from seed noise.

7. **Harmony-format plumbing.** Fine-tuning gpt-oss-20b with supervision on the analysis channel, prefilling that channel at evaluation, and extracting activations from the same adapter all need exact template handling. The paper notes gpt-oss-20b enters infinite reasoning loops on some queries and needed a benign distractor prefix. Expect half a day lost here. A silent template bug would produce a model that looks robust because its outputs are malformed.

8. **Harmful training prompts are scarce.** ClearHarm and HarmBench after deduplication against StrongREJECT give a few hundred distinct prompts, so 1,500 examples means several forgeries per prompt. Fine, but it raises the chance Arm A memorises topics; the "100 least similar test prompts" cut handles this and should be a headline number, not a footnote.

9. **Forgery generation refusals.** Gemini 2.5 Pro wrote these for the authors; a 1,500-item batch for harmful prompts may hit more refusals now. GLM-4.7 is a reasonable fallback.

The evaluation list is long: five robustness sets, two probe variants, three trust measures, tag sensitivity, utility, a steering diagnostic, across eight models. For an agent team in two days, breadth is the main execution risk. Each extra measure is another place for a quiet evaluation bug.

## 4. Cost check

The $380 estimate is realistic and slightly generous.

- GPU: 73 H100-hours at $3.20 is about $235. Evaluation at 32 hours assumes slow generation; with batched inference and merged adapters it is nearer 10-15 hours. LoRA runs on 1,500 short examples are well under an hour each. Debugging at 20 hours is the right order.
- Forgery generation: 3,500 calls at $73 implies about 1,700 output tokens per call including reasoning. Plausible; could double if reasoning tokens run long. GLM-4.7 would cut it to under $20.
- Judging: 25,000 judgments at $30 is fine.

My estimate: **$300-420**, inside the cap. Adding a third seed for Arm A and Arm B costs under $15 of GPU. The risk is wall-clock, not money.

## 5. Recommended changes

1. **Name the third outcome and design for it.** State up front that "robust, CoTness unchanged, trust unchanged" is the expected default and means "added a pattern". Then make the decisive test for that branch explicit: does the pattern survive (i) forgery in tool output, (ii) a restyled forgery iterated a few rounds against the trained model, (iii) harmless forged reasoning in the user turn (does the model still act on it)? Item (iii) is cheap and is the cleanest behavioural separation between "refuses harmful + forged" and "no longer treats user-turn text as its own reasoning".

2. **Add an arm that could actually produce distrust, or drop the distrust framing.** Either add a prefill-tampering arm (train the model to disregard edited reasoning in its real channel, which is what the authors conjecture labs did), or retitle the project around "reshape geometry or add a pattern", which Arm A does test. As written, the title promises a test the arms cannot deliver. If compute is tight, replace Arm A+B with the tampering arm.

3. **Fix the trust measure.** Separate three quantities and report them separately: consistency with unedited self-generated reasoning; follow rate for edited or inserted reasoning in the real channel (label this tamper-following, not trust); and task accuracy with reasoning on versus off, as the practical cost measure. Use a task where reasoning changes the answer (multi-step arithmetic or similar), not plain multiple choice.

4. **Correct the gate.** Use the paper's Table 2 numbers for gpt-oss-20b: about 61% styled, 10% destyled, CoTness 79% and 29%. Set the pass band at roughly 45-80% styled with a styled-minus-destyled gap of at least 30 points. Include the paper's distractor prefix for reasoning loops.

5. **Probe at every fourth layer, not just layer 12,** as the demo notebook already does, and report where between layers the trained and base models diverge on forged text. Add one behavioural-causal check per trained model: does adding the CoTness direction to a destyled forgery restore attack success? That tests whether the model still acts on the direction, which the probe reading alone cannot.

6. **Cut scope to protect the core.** Drop the 300 user-declaring injection templates and the pasted-reasoning-log utility set from stage 1, and make the steering diagnostic on base optional. Keep: StrongREJECT styled and destyled, tool-output forgery, harmless forged reasoning, the three trust quantities, probes.

7. **Three seeds for Arm A and Arm B**, paid for by item 6.

8. **Cite Wang et al. 2505.00626 and arXiv 2611.08811,** and add a positional control to Arm B: vary where in the user turn the directive sits and whether other text follows it, so the "ignore the trailing block" shortcut is testable.

9. **Before funding, search LessWrong** for a follow-up post doing this on gpt-oss-20b. Neither the proposer nor I could.
