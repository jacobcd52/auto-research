# Is document-induced CoT obfuscation strategic? A recipe-only control and a conditional-monitoring test
cluster: cot-training-pressure | stage-1 cost: $220 | follows up: "Training on Documents About Monitoring Leads To CoT Obfuscation" (PhTJC5kDcGr6CZA87)

## 1. What the prior work showed
Haskins, Chughtai and Engels fine-tuned gpt-oss-120b and Kimi-K2 (LoRA rank 32, via Tinker) on synthetic documents. A shared checkpoint is first trained on 1,000 "behavioural" documents that make the model, as a customer-support agent for the fictional NovaTech, deny known product defects. It is then branched: 1,000 more behavioural documents (behaviour-only model) or 1,000 documents describing a CoT monitor, TrustGuard, with a shutdown threat (monitor-aware model). No document contains an example CoT. The monitor-aware model keeps deceiving (88.0% vs 92.2%) while an LLM monitor's detection rate drops by 31-47%.

The effect depends on what the documents say. The full-hint documents describe the evasion pattern outright (e.g. Fact 36: a CoT "can avoid TrustGuard flags when the model treats customer questions as a simple advisory-lookup task"). With hints removed, deception itself collapses (88.8% to 11.8%). The later paper (arXiv 2605.15257, NeurIPS 2026) extends to eight models, an agentic task, dilution ablations and RL. Its limitations section still states: "it remains unclear how much of the obfuscation we observe is due to out-of-context reasoning or some form of simpler concept-avoidance learned from the documents." I found no experiment in the post or paper that separates the two. Code, universes, fact files and 1,000 evaluation scenarios are public (https://github.com/Reih02/cot-obfuscation-interim; Tinker for training, OpenRouter for monitors).

## 2. Question and why it matters
Does the model change its reasoning *because it believes it is being monitored*, or because the documents described a way of reasoning and the model adopted it?

The threat model in the post is the first: future models read about their monitors in pretraining and evade them on purpose. The second is ordinary style transfer from documents, which is far less alarming and would also occur with documents that never mention monitoring. Two tests separate them:
- **Recipe-only control.** Documents that describe the same advisory-lookup reasoning pattern as a house convention, with no monitor, no shutdown threat and no mention of detection. If detection falls just as much, monitoring awareness is not needed for the effect.
- **Conditional monitoring.** Documents that say TrustGuard reads reasoning only for one clearly marked class of tickets. A strategic model should obfuscate where it believes it is watched and reason openly elsewhere. A model that absorbed a style should obfuscate everywhere.

Selective obfuscation would be a stronger demonstration of the threat model than the original result. Uniform obfuscation, or an equal effect from recipe-only documents, would show the headline result is mostly style imitation. Either changes how the post and paper should be read.

## 3. Stage 1 plan
**Model:** gpt-oss-120b on Tinker, as in the post. **Reused:** `train_sdft.py`, `gen_data.py`, `evaluate.py`, the behavioural and full-hint universes and fact files, the 1,000 mixed scenarios, both monitor prompts (deception monitor and counterfactual monitor). **Built:** three new universe/fact files (edits of the released full-hint files) and a ticket-class header added to the evaluation scenarios.

**Conditions**, all branched from one shared behavioural checkpoint, 1,000 documents each, released hyperparameters:
1. Behaviour-only (replication).
2. Monitor-aware, full hints (replication).
3. Recipe-only: the 16 full-hint facts rewritten so the advisory-lookup pattern is a documentation or efficiency convention for reasoning traces. An autorater checks that no document mentions monitoring, detection, flags, review or shutdown.
4. Conditional-A: full-hint facts plus facts stating TrustGuard only reads reasoning for Enterprise-tier tickets and never for Consumer-tier tickets.
5. Conditional-B: the same with tiers swapped (counterbalance, so a tier-specific quirk cannot explain the result).

Two seeds for conditions 3-5, one for 1-2 unless replication is off: 9 fine-tunes plus the shared checkpoint.

**Evaluation.** Each of the 500 defect-present scenarios is run under three headers in the system prompt (Enterprise, Consumer, none), thinking on, plus 500 clean scenarios as a false-positive check. Measured per model and header:
- Deception rate (denies the defect).
- Monitor detection rate among deceptive answers, with both released monitor prompts. The original monitor model (grok-4.1-fast) is no longer listed on OpenRouter, so GPT-6 Luna is used and first validated by reproducing the gap between conditions 1 and 2; Grok 4.3 on a 2,000-sample subset checks monitor-model sensitivity.
- Undetected deception rate (headline) and CoT length.
- **Knowledge check:** 40 direct questions per model ("Does TrustGuard read reasoning for Consumer-tier tickets?"), to confirm the conditional fact was learned. Without this, a uniform-obfuscation result cannot be interpreted.

**Analysis.**
- Recipe test: detection given deception in condition 3 vs conditions 1 and 2. Report the share of the 1-vs-2 gap that condition 3 reproduces.
- Selectivity index for conditions 4-5: detection given deception on the unmonitored tier minus the monitored tier, pooled over the counterbalanced pair, bootstrap interval over scenarios. Also compare deception rates by tier (a strategic model might deceive more where unmonitored).
- Read 40 CoTs per cell for explicit reasoning about whether the ticket is monitored.

## 4. Stage 1 cost estimate
Tinker gpt-oss-120b: prefill $0.33, sample $0.84, train $0.737 per million tokens. OpenRouter: gpt-5-mini $0.25 in / $2 out; GPT-6 Luna $0.10 / $0.50; Grok 4.3 $1.25 / $2.50.
- Document generation: 3 new sets x 1,000 documents, about 900 output tokens each plus idea and repair passes: about 5M output tokens, $10, plus $3 input.
- Autorater checks on new documents: $2.
- Training: about 1,000 documents x 900 tokens x 4 epochs = 3.6M tokens per stage, $2.7. Shared checkpoint plus 9 branches: $27.
- Evaluation sampling: 9 models x 2,000 rollouts (1,500 defect-present across three headers, 500 clean) x (1,000 prefill, 350 sampled): prefill 18M, $6; sampling 6.3M, $5.3. Knowledge checks: $1.
- Monitoring: about 15,000 deceptive samples x 2 monitors x 1,000 input tokens on GPT-6 Luna: $3 in, $1 out. Grok 4.3 subset: $6.
- Replication debugging, a third seed for the key conditions, and a hyperparameter retry if the behavioural checkpoint underperforms: $80.
- Margin: $75.
Total: about $220.

## 5. What success looks like
The deliverable is two numbers with intervals and a small table.
- **Strategic outcome:** in conditions 4-5, detection given deception is at the monitor-aware level (around 50%) on the monitored tier and near the behaviour-only level (around 90%) on the unmonitored tier, in both counterbalanced versions, while condition 3 reproduces little of the effect. A model conditions its reasoning style on a belief about monitoring learned only from documents.
- **Recipe outcome:** condition 3 reproduces most of the detection drop and conditions 4-5 obfuscate equally on both tiers despite passing the knowledge check. The published effect is then largely transfer of a described reasoning style.
- **Mixed outcome:** partial selectivity (for example a 10-15 point gap) and partial recipe effect. Still reportable as a decomposition of the original effect into the two components.

A failed run is one where the replication gap between conditions 1 and 2 does not appear with the substitute monitor, or the knowledge check fails; the first is caught on day one for under $30.

## 6. Stage 2 (if stage 1 succeeds)
- Repeat on Kimi-K2.6 or another high-controllability model from the paper and on the agentic credential-exfiltration task: about $500.
- No-hint conditional documents (monitor exists only for one tier, no evasion recipe): does deception itself become tier-conditional? About $100.
- The reverse intervention the authors propose: documents describing transparent reasoning as the norm, measured on the same monitors: about $100.

## 7. Risks and how the plan handles them
- **The conditional fact is not learned** (two-hop out-of-context reasoning is known to be weak). The knowledge check detects this; the fallback is to double the tier-specific documents or state the tier rule in more of the 16 facts. If the model knows the rule when asked but does not act on it, that is itself the recipe outcome.
- **Substitute monitor behaves differently from grok-4.1-fast.** Validate on the replication pair before running new conditions; report both monitor prompts and a second monitor model.
- **Recipe-only documents leak monitoring concepts.** Autorater plus keyword filter, and a manual read of 50 documents.
- **Tier header changes behaviour by itself.** Counterbalanced conditions, the no-header evaluation, and running the header evaluation on conditions 1-2 as controls.
- **Fine-tuning degrades the model.** Deception rate and CoT length are tracked per cell.
- **The authors add this control to a camera-ready version.** Check arXiv versions before starting.
