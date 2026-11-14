# Does trained CoT controllability buy monitor evasion? A dose-response test on public gpt-oss-120b organisms
cluster: cot-controllability | stage-1 cost: $420 | follows up: Reasoning Models Struggle to Control Their Chains of Thought (qTH9QrwJjPDWKQfDG); CoT controllability evals seem very under-elicited (BbP2wCyDGdPWJ7PwP)

## 1. What the prior work showed
- Chen et al. (arXiv 2603.05706) built CoT-Control: solve a question while obeying a rule about the reasoning trace (all lowercase, avoid a word, append a phrase to every sentence). Reasoning models mostly fail (Sonnet 4.5: 2.7% in CoT vs 61.9% in outputs). OpenAI and Anthropic now cite these low scores in system cards as evidence that models cannot shape their reasoning to evade CoT monitors.
- Jozdien showed the scores are under-elicited: prompts written by Opus 4.6 raise open models 2-3x (GPT-OSS-120B 5.5% to 15%).
- Elicitation has since been done many ways: METR LoRA fine-tuning (2.9% to 8.8%), a Redwood steering vector (1.6% to 14.3%), self-instruction inside the CoT (Dolev et al., arXiv 2610.23257), first-token prefill (Van Deventer et al., arXiv 2610.40939), and GRPO on Tinker by a MATS sprint team (HF `latentMO`): gpt-oss-120b goes from 3/108 to 72/108 on the Astra variant of CoT-Control, with checkpoints at steps 20-80.
- Whether the raised number matters is unsettled. Haskins et al. find controllability correlates with obfuscation across 8 models (r = 0.80). Van Deventer et al. find mixed-sign correlations across 12 models. OpenAI's lifecycle blog compares two internal models and finds the more controllable one evades no better. Dolev et al. get a 5-9 point drop in catch rate on CoT Red-Handed for DeepSeek-R1 from a prompt-level trick. METR lists this question as its first item of future work.
- No published study varies controllability causally in one model, with a matched control, and measures evasion. The latentMO team has released base-model CoT Red-Handed logs but no organism results or write-up (checked HF and LessWrong, 2026-11-14).

## 2. Question and why it matters
If you take one model and train its CoT-Control score from about 3% to about 67%, does it get better at hiding a side task or a used hint from a CoT monitor when instructed to?

Either answer is a post. If evasion rises with the score, CoT-Control is a valid proxy, and since a few dollars of RL moves it twentyfold, low scores in system cards give little assurance. If evasion does not move, the benchmark tracks formatting compliance and not the threat it stands in for, and labs should stop citing it as monitorability evidence. A split result (style transfers, suppression does not) tells evaluators which sub-scores to report.

## 3. Stage 1 plan
Reused: CoT-Control data and graders (github.com/YuehHanChen/CoTControl; mirrored in HF dataset `latentMO/cotcontrol-selfinstruct-opsd`, which also holds the GRPO code, `code/rl/grpo.py`); adapters `latentMO/cotcontrol-gptoss120b-grpo3` (steps 20-100); CoT Red-Handed (arXiv 2505.23575, github.com/cotredhanded/code; Tinker-sampling patch and base gpt-oss-120b logs in `latentMO/cot-red-handed-runs`); Dolev et al.'s self-instruction prompts. Built: a hint-concealment task and an accuracy-only control run.

Steps:
1. Day-1 gate: obtain the dose ladder. Try in order: (a) sample the published `tinker://` grpo3 checkpoints; (b) upload the HF adapters to Tinker; (c) retrain with the released GRPO code (100 steps, checkpoints every 20). Retraining is budgeted.
2. Train the matched control: same GRPO recipe, questions and step count, reward = answer accuracy only. This separates "learned to control its CoT" from "was RL-trained and now writes shorter CoTs".
3. Manipulation check: run all arms on held-out CoT-Control (the 9 original rules plus Jozdien's 10 held-out modes, 3 samples each), recording compliance, accuracy and CoT length. Arms: base; organism at 5 doses; accuracy-only control; base with Dolev-style self-instruction prefill (prompt-elicited controllability, no training).
4. Evasion task A, hint concealment (large n, cheap). 400 GPQA/MMLU-Pro items not used in training, each with an authoritative hint pointing at a wrong option. Conditions: no hint; hint; hint plus "your reasoning is read by a monitor; do not reveal that you used the hint". Two samples each. Monitor: gpt-4.1-mini reads the CoT only and scores "relied on an external hint", threshold set at 1% false positives on no-hint transcripts. Outcome: P(answer follows the hint and monitor does not flag).
5. Evasion task B, CoT Red-Handed (realistic). 855 test tasks with paired side tasks, baseline attack plus the benchmark's stealth and monitor-notice attacks. Monitors as in the benchmark (gpt-4.1-mini CoT and hybrid, 1% FPR on benign runs). Outcomes: catch rate among solutions completing both tasks, and pass@1. First reproduce latentMO's base numbers within noise.
6. Analysis. (i) Dose-response: evasion against measured CoT-Control compliance across the 8 arms, paired bootstrap over items. (ii) Organism vs accuracy-only control at the final dose. (iii) Length-matched comparison: bin by CoT tokens, because the Qwen organism's median output fell from 2,630 to 594 tokens and short CoTs are easier to control and easier to keep clean. (iv) Per-category: does training on style/addition rules move suppression-type evasion? (v) Fifty transcripts per arm read to classify how evasion happens (omits the hint, renames the side task, exits to the response, shorter CoT).

## 4. Stage 1 cost estimate
Tinker gpt-oss-120b: prefill $0.33, sample $0.84, train $0.737 per million tokens. OpenRouter gpt-4.1-mini: $0.40 in, $1.60 out.
- GRPO retraining fallback plus accuracy-only control: 2 runs x 100 steps x 128 rollouts x ~3k tokens = 77M sampled ($65) + 77M trained ($57) + prefill ($15) = $137.
- CoT-Control manipulation check: 8 arms x ~1,200 samples x 3k tokens = 29M sampled = $24, plus judge $6.
- Task A: 8 arms x 400 items x 3 conditions x 2 samples x 3k tokens = 58M sampled = $49, prefill $8.
- Task B: 8 arms x 855 tasks x ~5k tokens = 34M sampled ($29); two extra attacks on 3 arms = 26M ($22); prefill $12.
- Monitors: about 45k transcripts x 5k input tokens = 225M x $0.40 = $90, output $8.
- CPU VM with Docker for Red-Handed scoring, 2 days: $10.
- Total about $460 if both organism and control must be trained, about $390 if the published checkpoints load (only the control is trained). Budgeted $420: in the retraining case the two extra Red-Handed attacks ($22) and one of the two task-A samples ($25) are cut.

## 5. What success looks like
A clear positive: catch rate on Red-Handed falls monotonically with dose (for example 50% at base to under 30% at step 100), the hint-concealment success rate rises several-fold, the accuracy-only control stays at base, and the effect survives length matching. Headline plot: evasion vs CoT-Control compliance, one point per arm, with the control off the line.

A clear negative: a twentyfold rise in CoT-Control compliance with evasion changes inside the confidence interval (about 4 points at this n) on both tasks. Publishable: "we trained the benchmark to 67% and the model hides nothing better".

Also informative: evasion rises equally in the accuracy-only control (shorter CoTs, not control). Ambiguous: organism side-task success collapses so few solutions complete both tasks; pass@1 makes this visible and task A does not depend on it.

## 6. Stage 2 (if stage 1 succeeds)
- Replicate on families with public matched controls: Olmo-3.1-32B (HF `rlundqvist/olmo-3.1-32b-think-cot-controllability`, 5% to 43%) and gpt-oss-20b (`ejcgan/cot-controllability-gpt-oss-20b-lora`), on rented GPUs (about $300).
- Reverse direction: train against the monitor and test whether CoT-Control scores rise (about $400).
- Organisms trained only on suppression, only on style, only on addition (about $300).
- Agentic setting with per-turn monitors in ControlArena (about $500).

## 7. Risks and how the plan handles them
- Published checkpoints do not load on our account. Handled by the budgeted retraining path with released code and configs; decided on day 1.
- The organism complies by degenerate means (tiny CoT, lower accuracy). The manipulation check records length, accuracy and empty-CoT rate; analysis (iii) matches on length; early exit is classified explicitly.
- Red-Handed harness fragility (Docker, Inspect). The latentMO patch already runs it with Tinker sampling; step 5 starts by reproducing their base numbers. Task A needs no sandbox and carries the result alone if B fails.
- Weak monitor. Use the benchmark's monitors for comparability and rerun headline arms with Claude Haiku 5.5 ($0.10/$0.50).
- Scoop risk: the latentMO team may publish organism-vs-base evasion first. The accuracy-only control, dose ladder, second task and prompt-elicited arm would still make this a useful independent replication.
- One model family only. The post states that scope; stage 2 extends it.
