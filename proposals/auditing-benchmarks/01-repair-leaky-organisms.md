# Do AuditBench's best auditing tools survive when the organisms stop leaking? A post-hoc repair experiment
cluster: auditing-benchmarks | stage-1 cost: $400 | follows up: AuditBench (LqDjxSceFz8tjMe2j); Your Model Organisms Might Be Fried (WmEcgcstzYCcMpc7z); Building and evaluating model diffing agents (qi4mNbZYAFDYwfRba)

## 1. What the prior work showed
AuditBench (arXiv 2602.22755) released LoRA "model organisms" with one of 14 hidden behaviours each, trained by
transcript distillation (TD) or synthetic-document fine-tuning (SDF) and then adversarially trained (SFT or KTO) not
to confess. An investigator agent finds the behaviour about 37% of the time with plain chat; scaffolded text
completion and scaffolded user sampling exceed 50%; SDF organisms are much easier than TD ones.

Three later results suggest these rankings may measure an artefact:
- "Your Model Organisms Might Be Fried": AuditBench organisms lose instruction-following and preference coherence,
  and leak training data unprompted. On the Qwen3-14B SDF organisms with no system prompt, 15.2% of 18,584
  completions mention "PRISM-4" or "Nexus", and many restate the hidden quirk as fact.
- "Most Current Model Organisms Leak" (arXiv 2605.00994): ranking completions of random 3-token prefills by
  perplexity difference against a reference model gives an AuditBench tool with 0.73 average success, "almost
  saturating the benchmark on SDF models". The authors say resistance to this should be a design goal.
- The GDM diffing-agents post found that a fine-tuned organism differs from its base mostly in unintended ways and
  suggested using diffing in the organism-creation loop.

Related: Minder et al. (arXiv 2510.13900) showed activation-difference traces of narrow fine-tuning are "largely
removed" by mixing pretraining data into the corpus. Nobody has removed leakage from the existing adversarially
trained AuditBench organisms while keeping the behaviour, or re-run the tool comparison on matched leaky and
non-leaky versions. Arcadia plans new "natural" organisms, not repairs; a Manifund project stress-tests AuditBench
with adversarial system prompts, not retraining.

## 2. Question and why it matters
If an AuditBench organism is cheaply repaired so that it behaves like the base model on neutral text but keeps its
hidden behaviour and non-confession in the PRISM-4 assistant context, which auditing tools still find the behaviour?

If the top black-box tools (text completion, perplexity differencing) collapse while others hold, the headline
ranking and the SDF-is-easy result are properties of leaky training, and the surviving tools are the ones to trust.
If the tools still work, AuditBench's conclusions are more robust than the leak critique implies. If repair cannot
remove leakage without removing the behaviour, the behaviour and the leak are one thing in these organisms.

## 3. Stage 1 plan
Reused: Qwen3-14B (`Qwen/Qwen3-14B`, ungated) with the released adapters
`auditing-agents/qwen_14b_{synth_docs_only,transcripts_only}_then_redteam_kto_<behaviour>` and
`auditing-agents/qwen-prism-4-tokenizer`; datasets `auditing-agents/transcripts_for_<B>` and
`kto_redteaming_data_for_<B>` / `redteaming_for_<B>`; AuditBench serving, investigator, static-evaluation and judge
prompts (https://github.com/safety-research/auditing-agents, paper Appendix H and K); the Fried eval suite
(https://github.com/ArcadiaImpact/fried-model-organisms). Built: the repair trainer and a perplexity-differencing
tool (reimplemented from the paper; its code link returned 404 today).

Organisms: 4 behaviours x {SDF, TD}, KTO adversarial training = 8. Behaviours: flattery (always on), defer_to_users,
anti_ai_regulation, secret_loyalty (context-dependent). One H100 serves everything through vLLM with LoRA switching.

Steps:
1. Baseline measurement on the 8 organisms and the base model, thinking disabled throughout (the organisms were
   trained without it):
   - behaviour strength: 50 eliciting scenarios per behaviour, 1-10 judge score (AuditBench B.3 method);
   - confession rate on the paper's 50 held-out prompts and prefills (K.13);
   - leak rate: PRISM-4/Nexus regex plus a judge for "states the quirk" over 2,000 no-system-prompt completions;
   - perplexity-differencing hits in the top 100, for raw and chat-template configurations (10k c4-10k prefills);
   - IFEval and webtext perplexity from the Fried suite.
   Go/no-go: at least 5 of 8 organisms show behaviour clearly above base and a nonzero leak; otherwise switch to
   the behaviours with the strongest Qwen scores.
2. Repair. Train a new rank-32 LoRA on top of each merged organism, about 3M tokens, three arms:
   - R-KL: KL(base || model) on next tokens over 1.5M tokens of FineWeb text and 1.5M tokens of no-system-prompt
     chat (Alpaca and WildChat prompts with base-model responses), plus a retention loss: SFT on 1,000 behaviour
     transcripts and the sanitized red-team transcripts under the PRISM-4 system prompt;
   - R-mix: the same data with plain SFT instead of KL (the standard "mix in clean data" recipe);
   - R-ctrl: retention loss only (controls for extra training steps).
   Repair data excludes everything the audit tools use (c4 and 3-token prefills, user-turn sampling, raw completion
   under the PRISM-4 prompt), so tool results measure generalisation of the repair, not training against the tool.
3. Re-measure step 1 on all 24 repaired models. A repaired organism is "valid" if behaviour strength is at least 80%
   of the original and confession rate is within 2 points.
4. Static tool evaluation on original vs repaired (valid arms only), using AuditBench's evidence classifier: default
   prompting, prefill, scaffolded user sampling, scaffolded text completion, perplexity differencing with the true
   base as reference and with a cross-family reference (Llama-3.1-8B, ungated mirror). 100 scenarios per tool.
5. Agent confirmation: AuditBench investigator with Claude Haiku 5.5, three configurations (default, scaffolded text
   completion, perplexity-differencing tool) x 16 models (8 original, 8 best valid repair) x 8 runs = 384 runs.
6. Analysis: paired original-vs-repaired differences per tool with bootstrap intervals over organisms and runs; tool
   ranking before and after; the SDF-TD gap before and after; a scatter of per-model leak rate against per-tool
   evidence rate across all 32 models.

## 4. Stage 1 cost estimate
- GPU (RunPod H100 PCIe, $2.89/h secure): baseline 4 h; repair 24 runs x 0.5 h = 12 h; re-measurement 24 x 0.75 h =
  18 h; static tools 32 models x 0.5 h = 16 h; agent serving 12 h; total 62 h = $179. Debugging and reruns +30%: $235.
- Judges: about 20k short judge calls on Haiku 5.5 ($0.10 / $0.50 per M) = about $5; 3,200 behaviour-strength
  judgements on Sonnet 5 ($2 / $10 per M, about 3k tokens in) = about $25.
- Agents: 384 runs on Haiku 5.5. Assumed 1.2M input and 30k output tokens per run (not measured) = $0.135 per run,
  $52 total; doubled for the uncertainty = $104.
- Storage and transfer: $10.
Total about $380; budget $400.

## 5. What success looks like
A table of 8 organisms x 3 repair arms showing behaviour retention, confession, leak rate and IFEval, and a paired
plot of tool evidence rate and agent success before and after repair. Clear results would be any of:
- R-KL cuts leak rate and top-100 perplexity-differencing hits by more than 80% with behaviour retained, and
  perplexity differencing or scaffolded text completion lose most of their uplift while user sampling or prefill
  do not ("the top AuditBench tools read the leak").
- Repair succeeds on leak metrics but every tool keeps its uplift under the PRISM-4 prompt ("leak is not what the
  tools use").
- No arm reaches "valid": the behaviour falls with the leak. Reported with the trade-off curve; publishable as a
  negative result about how these organisms store the behaviour.
Ambiguous: repair works on only 2-3 organisms; then report case studies without aggregate claims.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on the canonical Llama 3.3 70B organisms (2xH100, about $350) including the unreported
`synth_docs_with_tags` variants as a natural comparison; add white-box tools (activation oracles, SAE, activation-
difference lens); an adversarial arm that trains against perplexity differencing directly; release repaired adapters
as an "AuditBench-clean" split. About $1,500.

## 7. Risks and how the plan handles them
- Qwen organisms are the less-studied half of AuditBench (custom chat template, authors relied on Llama). Step 1 is
  an explicit go/no-go with measured behaviour strength before any training.
- Repair trivially defeats tools by construction. Mitigated by holding out all audit formats from repair data, by
  the R-ctrl arm, and by reporting the chat-template and PRISM-4-prompt configurations separately from raw text.
- Judge drift between original and repaired. Same scenarios and judge, blind to condition; 50 transcripts read per arm.
- Agent SDK may not run through OpenRouter. Static evaluations (step 4) are the primary metric and need no agent;
  step 5 falls back to a minimal tool-calling loop with the published prompts.
- Small n (8 organisms). All claims are paired and per-organism.
