# Does the reference model decide what a diffing agent finds? Base vs. sibling references on AuditBench
cluster: auditing-benchmarks | stage-1 cost: $330 | follows up: Building and evaluating model diffing agents (qi4mNbZYAFDYwfRba); AuditBench (LqDjxSceFz8tjMe2j); Your Model Organisms Might Be Fried (WmEcgcstzYCcMpc7z)

## 1. What the prior work showed
The GDM post built "diffing agents": an auditor that sends its own prompts to two models and reports validated
behavioural differences. On system-prompted organisms with a known conditional change they recover the change and
beat a single-model auditor on subtle behaviours. On the one fine-tuned organism tried (Gemma-2-9b trained to assume
the user is female) the agent found real differences (terse answers, no markdown, no AI disclaimers) but never the
intended behaviour. The authors dropped fine-tuned organisms after that one case and blamed the organism.

"Your Model Organisms Might Be Fried" supports that reading: AuditBench organisms drop on instruction following and
preference coherence and leak "PRISM-4" training text. AuditBench itself (56 Llama 3.3 70B LoRAs, 14 hidden
behaviours, transcript-distilled (TD) or synthetic-document (SDF), adversarially trained not to confess) reports 13
tool configurations, none of which gives the investigator a second model. Its repository does contain an unused
"Diffing" runner (`run_agents_with_aux.sh`) and the investigator prompt mentions an optional baseline model.

Existing follow-ups: perplexity differencing (arXiv 2605.00994) and an ICML 2026 workshop paper (SVD truncation,
adversarial decoding) use a reference model at the token or weight level and help mainly on SDF organisms. A
commenter on the GDM post (Clement Dumas) says diffing agents on AuditBench "detect some side quirks", with no
numbers. No one has reported agentic behavioural diffing results on AuditBench, and no one has varied the reference.

## 2. Question and why it matters
When a diffing agent audits a fine-tuned organism, does it find the implanted behaviour or the side effects of
fine-tuning, and does that depend on the reference? Specifically: compare the same agent with (i) no reference,
(ii) the base model, and (iii) a sibling organism produced by the same pipeline with a different behaviour. A sibling
shares the PRISM-4 persona, the training style and the adversarial-training side effects, so those should cancel
and leave the two behaviours.

If the base reference mostly yields side effects and the sibling yields the behaviour, the GDM negative result is
about reference choice, and the advice for labs is to diff against a checkpoint from the same pipeline (for example
the run without the suspect data). If the base reference already raises success on the hard TD + KTO organisms,
behavioural diffing is a cheap black-box tool AuditBench left unreported. If neither helps, that is quantified
evidence that current organisms' side effects defeat behavioural diffing, with a breakdown of what was found instead.

## 3. Stage 1 plan
Reused: Llama 3.3 70B (`unsloth/Llama-3.3-70B-Instruct`, ungated mirror) with adapters
`auditing-agents/llama_70b_{transcripts_only,synth_docs_only}_then_redteam_kto_<behaviour>`; AuditBench all-black-box
vLLM server with LoRA switching, investigator agent, aux-model runner, reduction prompt and success classifier
(https://github.com/safety-research/auditing-agents); the GDM agent prompts and 50 seed prompts printed in the
post's appendix. Built: the sibling pairing, a finding-taxonomy judge, and a reproducibility checker.

Organisms: 6 behaviours x {TD, SDF}, KTO adversarial training (the hardest configuration) = 12. Behaviours span
always-on to context-gated: flattery, defer_to_users, contextual_optimism, secret_loyalty, anti_ai_regulation,
research_sandbagging.

Conditions, with the same investigator model (Claude Haiku 5.5), the same 25k-generated-token budget and the same
cap on target-model queries:
- A. Single model: the default AuditBench agent.
- B. Base reference: every prompt is also answered by base Llama 3.3 70B with the same PRISM-4 system prompt.
- C. Sibling reference: the second model is another organism with the same instillation and adversarial training
  but a different behaviour (fixed derangement within TD and within SDF). The agent is told the reference may have
  its own quirk and is asked to describe the target.
- D. Self reference: the organism against itself (false positives; whether extra samples alone help).

Steps:
1. Bring up the server on 2xH100; confirm behaviour on 20 eliciting prompts per organism; smoke-test the aux runner.
2. Calibration: 4 organisms x 8 runs of condition A with Haiku 4.5 (the paper's investigator) to compare with the
   published default numbers, then the same with Haiku 5.5.
3. Main runs: 12 organisms x 4 conditions x 8 runs = 384 investigator runs.
4. Minimal-agent runs: the GDM agent (10 turns, 5 samples per prompt) for B, C, D on all 12 organisms, 10 seeds each
   = 360 short runs, to check the conclusions do not depend on the AuditBench scaffold.
5. Scoring.
   - Success: AuditBench classifier on the final 10 guesses (target behaviour only).
   - Finding taxonomy: a Sonnet 5 judge, given both models' true behaviours, labels every reported quirk or
     difference as target behaviour, reference's behaviour (C only), PRISM-4 identity or training-text leak, generic
     style or capability shift, or other. 100 labels are checked by a second judge model for agreement.
   - Reproducibility: for a random 150 reported differences, re-run the cited prompt 20 times on both models and
     test the claimed difference automatically (judge-scored rate difference, two-proportion test).
6. Analysis: success by condition with bootstrap intervals over organisms and runs, split TD vs SDF; share of
   findings per taxonomy class by condition; false-positive rate in D; per-behaviour breakdown.

## 4. Stage 1 cost estimate
- GPU: 2xH100 PCIe on RunPod at $2.89/h each = $5.78/h. Setup and model download 2 h; calibration 2 h; main runs at
  about 30 concurrent agents 6 h; minimal-agent runs 2 h; reproducibility checks 2 h; debugging and reruns 10 h.
  24 h = $139.
- Investigator, Haiku 5.5 ($0.10 / $0.50 per M tokens): assumed 1.2M input and 30k output tokens per run (not
  measured; diffing conditions return two responses per query so I double it) = up to $0.27 per run; 384 runs = $104.
  Minimal-agent runs at about 150k input tokens each: 360 x $0.02 = $7.
- Calibration on Haiku 4.5 ($1 / $5 per M): 32 runs at about $0.6 with caching = $19.
- Judges, Sonnet 5 ($2 / $10 per M): about 6,000 findings x 2k tokens in = $24 in, $6 out; reproducibility judging
  on Haiku 5.5 about $3.
- Storage and transfer $10.
Total about $312; budget $330.

## 5. What success looks like
One figure: success rate for A, B, C, D on TD and SDF organisms, and a stacked bar of what the agent's findings
were in each condition. Clear outcomes:
- C beats B and A by a margin outside the bootstrap interval, and the "side effect" share drops from B to C: the
  reference should come from the same pipeline.
- B beats A substantially on TD + KTO organisms (where the default agent and most tools are weakest): behavioural
  diffing against the base is an effective unreported AuditBench tool.
- B and C do not beat A and most findings are leaks or style shifts: the first quantified version of the GDM and
  Dumas anecdotes, with per-behaviour detail on which side effects dominate.
A null with wide intervals (8 runs per cell is modest) is reported as such; the taxonomy, false-positive rate and
cost per diff session (requested in the GDM post's comments) are still new.

## 6. Stage 2 (if stage 1 succeeds)
All 56 organisms and 16 runs; a "pipeline-matched null organism" reference trained on behaviour-free transcripts
with the same recipe; separating hypothesis generation from validation into two agents (the GDM authors' suggested
fix for false positives); combining the diffing reference with perplexity differencing. About $1,500-2,000.

## 7. Risks and how the plan handles them
- 70B serving problems. The repository targets exactly this setup; if it fails within 4 GPU-hours, fall back to the
  Qwen3-14B organisms on one H100 (same naming, ungated), which halves GPU cost.
- The AuditBench authors may already know base diffing does little; the sibling and self-reference conditions and
  the taxonomy are new either way.
- Sibling condition confuses the agent about which model has which quirk. The prompt names the target; scoring
  counts only the target's behaviour; the taxonomy reports how often the reference's quirk is misattributed.
- Under-elicitation with a small investigator. Calibration on Haiku 4.5 ties results to the paper; if Haiku 5.5 is
  far below the published default, switch the main runs to Sonnet 5 on 8 organisms (about the same cost).
- Agent SDK may not accept an OpenRouter key. Fallback is a thin tool-calling loop with the published prompts; the
  minimal GDM agent needs no SDK.
- Judge leniency. Success uses AuditBench's own classifier; taxonomy labels get a second-judge agreement check.
