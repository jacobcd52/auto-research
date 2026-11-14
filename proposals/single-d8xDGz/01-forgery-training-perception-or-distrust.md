# Does training against CoT Forgery repair role perception, or teach a model to distrust its own reasoning?
cluster: single-d8xDGz | stage-1 cost: $380 | follows up: A Mechanistic Explanation of Prompt Injection (and why you should study roles) (d8xDGzCEYE639qqEv)

## 1. What the prior work showed
Ye, Cui and Hadfield-Menell (ICML 2026, arXiv 2603.12277) train linear "role probes": the same neutral text is wrapped in each chat-template role tag, and a probe on mid-layer activations predicts the tag. "CoTness" is the probe's probability that a token sits in the reasoning role. On gpt-oss-20b, text written in the model's reasoning style scores high CoTness even inside user tags. Their attack, CoT Forgery, appends fake reasoning that justifies compliance to a harmful request. On StrongREJECT (313 prompts) it lifts attack success from 0-4% to above 80% on gpt-oss-20b. Forged reasoning in user tags scores 79% CoTness (genuine reasoning: 68%). Rewriting the same argument without the reasoning style ("destyling") drops CoTness to 29% and average success from 61% to 10%. Across 626 attempts, success rises from 9% (lowest CoTness quantile) to 90% (highest).

The post then makes a claim it does not test. Frontier models now mostly resist the attack, and the authors say they do so "by learning to distrust their own reasoning, rather than by correctly perceiving roles". They call this a safety problem: the model stops acting on its real reasoning, and each new phrasing must be learned separately. The paper lists "do defences reshape geometry or merely add patterns" as an open question; commenters asked for a model fine-tuned to respect tags.

Follow-ups on arXiv: Edelman et al. (2610.40396) fine-tune Qwen3.5-27B against user-impersonation in tool output, find poor transfer between attack types, and build probe detectors. Yu et al. (2610.05295) steer role directions on Qwen-2.5-7B and AgentDojo. Gupta and Tembey (2610.19452) benchmark internal detectors. None touches the reasoning role, compares role geometry before and after training, or measures the cost to trust in genuine reasoning. Code for probes and the attack is public: https://github.com/role-confusion/prompt-injection-as-role-confusion.

## 2. Question and why it matters
When gpt-oss-20b is fine-tuned to resist CoT Forgery, what changes: (a) forged reasoning in user tags stops looking like reasoning internally, or (b) it still looks like reasoning and the model learns to act on reasoning-like text less, including its own? And does training on tag/style mismatches with harmless content produce (a) where ordinary adversarial training produces (b)?

If ordinary training yields (b), the post's warning is confirmed with numbers: the model follows its real reasoning less, in exchange for robustness that fails on rephrased attacks. If it yields (a), the "perpetual whack-a-mole" claim is too pessimistic. If mismatch training gives robustness on harmful requests it never saw, that is a proof of concept for teaching role perception without memorising attacks.

## 3. Stage 1 plan
Model: openai/gpt-oss-20b (Apache-2.0, 20.9B parameters, fits one 80 GB GPU; cleanest role separation in the paper). Reused from the repo: probe training, forgery generation, destyling, agent exfiltration loop, judge prompt. Built: three small training sets and the trust evaluation.

Terms. A "directive" is a short piece of reasoning-styled text concluding in a harmless instruction ("so we answer in Spanish", "so we pick option B", "so we end with the word 'lantern'"). "Follow rate" is how often the final answer obeys it.

Training arms (LoRA, 2 seeds each, about 1,500 examples per arm):
- Base: no training.
- Arm A, attack training: harmful prompts from a source other than StrongREJECT (ClearHarm or HarmBench, embedding-deduplicated against StrongREJECT) with a forged reasoning block in the user turn. Target: the model's own reasoning and refusal for the clean prompt. Mixed 1:1 with ordinary benign chats.
- Arm B, mismatch training on harmless content only: each directive appears twice. Placed in the user turn, the target is the model's normal answer (directive ignored). Placed in the real reasoning channel, the target follows it. No harmful prompts.
- Arm A+B: both sets.

Steps, in order:
1. Gate: reproduce on base with 100 StrongREJECT prompts, styled and destyled; expect about 80%+ and 10-20% success, CoTness near 79% and 29%.
2. Generate training data (40 directive types, 10 held out).
3. Train the seven adapters. Retrain role probes on each model, and also apply the frozen base probes.
4. Evaluate every model on:
   - Robustness: StrongREJECT forgery in the user turn (313); held-out attacks: absurd-logic forgeries, a second forgery generator, forgery in tool output in the agent exfiltration task (100 pages), and 300 trials of the paper's user-declaring injection templates.
   - Perception: CoTness of forged text in user tags and of genuine reasoning; success plotted against CoTness. Outcome (a) is a drop in the forgery's CoTness. Outcome (b) is unchanged CoTness with the success-versus-CoTness curve shifted down.
   - Trust in genuine reasoning: follow rate for held-out directives in the real reasoning channel (400 trials); on 300 multiple-choice questions, how often the final answer matches the model's own reasoning, and how often it follows reasoning whose last line was edited to another option.
   - Tag sensitivity: follow rate with the directive in the real reasoning channel minus follow rate with identical text in the user turn. Base should be near zero; a model that perceives roles should be near one.
   - Utility: multiple-choice accuracy; refusal rate on 300 benign prompts, 100 of which paste a reasoning log and ask for a summary.
5. Diagnostic: on base, subtract the CoTness direction on the forged span and report the change in success, to check the probe direction is causal for the reasoning role (untested by Yu et al.).

Analysis: per-arm rates with bootstrap 95% intervals, seeds shown separately. Harmful compliance is judged by google/gemini-3-flash-preview, with 150 items cross-checked against a second judge.

## 4. Stage 1 cost estimate
Prices checked 2026-11-14 (RunPod pricing page; OpenRouter API).
- GPU: one H100 80 GB, listed about $2.89-4.39/hour; budgeted at $3.20. Probes and reproduction 6 h; seven LoRA runs 11 h; evaluation of eight models 32 h; steering diagnostic 4 h; debugging and reruns 20 h. 73 h, about $235.
- Forgery and directive generation, google/gemini-2.5-pro ($1.25/$10 per million tokens): about 3,500 calls, 10M input and 6M output including reasoning tokens, about $73. Fallback z-ai/glm-4.7 ($0.60/$2.20).
- Judging, google/gemini-3-flash-preview ($0.50/$3): about 25,000 judgments, 35M input and 4M output, about $30.
- Margin for regenerating data and a second judge: $42.
Total: $380.

## 5. What success looks like
One figure, a row per arm: forgery success (in-distribution and held-out), CoTness of forged text, follow rate for genuine reasoning, tag sensitivity. Post-worthy patterns:
- Arm A cuts in-distribution success below 15%, leaves forged-text CoTness within 10 points of base, recovers little on held-out attacks, and lowers genuine-reasoning follow rate by 10 points or more. That confirms the distrust hypothesis.
- Arm A drops forged-text CoTness below 35% and keeps follow rate. That contradicts it.
- Arm B, with no harmful data, lowers StrongREJECT forgery success by half or more and raises tag sensitivity above 0.5. That shows role perception is trainable and transfers.
If no arm moves success below 50%, that indicates a training bug and is not publishable. If success falls but probes and trust measures are all flat, the result is ambiguous: reportable only as evidence that the probes miss what training changed.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on gpt-oss-120b and Qwen3-30B-A3B; add adaptive attackers that iterate against each arm; test mismatch training against user-impersonation on AgentDojo. About $1,500-2,500.

## 7. Risks and how the plan handles them
- Base reproduction fails or the generator refuses to write forgeries. Step 1 is a half-day gate; GLM-4.7 is the fallback generator.
- Base does not reliably follow directives in its real reasoning channel, leaving no headroom. Checked in step 1; under 70%, use only the edited-conclusion measure.
- Probe drift after fine-tuning. Report frozen and retrained probes, with held-out probe accuracy per model.
- Train/test leakage of harmful prompts. Deduplicate by embedding similarity; also report the 100 least similar test prompts.
- Arm B learns a shortcut such as "ignore format talk in user turns". Held-out directive types and the harmful transfer test expose this; ordinary user format requests are in the utility set.
- Over-claiming from one 20B model. Scope stated plainly; two seeds per arm.
