# A noise budget for inference verification: which determinism knobs shrink the exfiltration bound?
cluster: single-7i33FD | stage-1 cost: $330 | follows up: Defending Against Model Weight Exfiltration Through Inference Verification (7i33FDCfcRLJbPs6u)

## 1. What the prior work showed
Rinberg, Karvonen et al. (arXiv 2511.02620) defend against a compromised inference server that hides model weights in its output tokens. The server logs (prompt, output, sampling seed); a trusted verifier re-runs the forward pass with the same seed and checks each emitted token. Inference is not bitwise reproducible, so the verifier must tolerate some disagreement. The tokens it would accept at a position form a set A_t; no sender can hide more than log2|A_t| bits there. With vLLM generation, 500 LMSYS-Chat-1M prompts, temperature 1, top-k 50, top-p 0.95, on Llama-3.2-3B, Llama-3.1-8B, Qwen1.5-MoE and Qwen3-30B-A3B, they bound hidden information to under 0.5% of the channel at a 0.01% per-token false-positive rate: a 200x slowdown. Fully deterministic inference would take the bound to zero, at a quoted 60% overhead.

Follow-ups already published:
- DiFR (arXiv 2511.20621) varied hardware (H200, A100, tensor parallelism, HuggingFace vs vLLM) but measured detection AUC for misconfigurations, not the exfiltration bound per configuration.
- Kezins (arXiv 2608.23375) showed prompt families that raise output entropy roughly double the bound (benign 0.07-0.12 bits/token; worst case 0.15-0.29; slowdown falls to 60-118x) and recommended entropy-aware thresholds without testing a defence.
- Ortega-Fernandez et al. (arXiv 2610.11843) pooled evidence across responses with an anytime-valid test, assuming calibration and monitoring share hardware and serving stack.
- Yuan et al. (arXiv 2506.09501, LayerCast) showed FP32 computation nearly removes cross-configuration divergence; Cooper et al. (arXiv 2609.25624) built bitwise-reproducible kernels. Neither is connected to verification.

Not done, per arXiv and LessWrong searches (general web search was unavailable): measuring how much each noise source contributes to the bound, or how much partial determinism shrinks it.

## 2. Question and why it matters
**How much of the residual exfiltration channel is due to each source of generator-verifier disagreement (precision, GPU architecture, batch composition, engine), and how far do cheap partial-determinism settings shrink the bound, on benign traffic and on high-entropy prompts?**

The bound is a property of the noise, not of the model. Labs currently have two data points: tolerate everything (0.5%) or buy bitwise determinism (0%, large overhead). If an FP32 verifier or matched GPU type cuts the bound 10x at a few percent cost, that is a directly usable recommendation, and it would blunt the high-entropy-prompt result, since near-ties only matter within the noise width. If the bound barely moves until both sides are fully deterministic, the 200x figure is near the practical limit and the Kezins degradation must be handled by policy.

## 3. Stage 1 plan
**Reused.** Released code at github.com/RoyRin/inference_verification_for_model_weight_exfiltration: `generate.py` (vLLM, seeded Gumbel-max sampling), `verify.py` (HuggingFace prefill verifier, hard-coded bf16, so precision and device are small patches), `analysis/analyze_thresholds.py` and `analyze_two_step_classifier.py` (Pareto of false-positive rate vs extractable bits). Models: `unsloth/Llama-3.1-8B-Instruct` (ungated mirror of a paper model) and `Qwen/Qwen3-30B-A3B` (the MoE model with the weakest bound). Prompts: LMSYS-Chat-1M as in the paper (gated-auto; fallback `allenai/WildChat-1M`, ungated). LayerCast code: github.com/nanomaoli/llm_reproducibility.

**Built.** A config matrix runner, per-token logging of the verifier's score margin, and three stress prompt sets (150 prompts each) following the family descriptions in arXiv 2608.23375.

**Steps.**
1. Reproduce: run `scripts/test_minimal.sh`, then the paper setup on both models. Targets: Kezins' benign numbers at sigma 1.0 (0.068 bits/token for Llama-3.1-8B, 0.119 for Qwen3-30B-A3B) and under 0.5% at 1e-4 false-positive rate. Stop and debug if off by over 30%.
2. Reference generation: vLLM, bf16, one H100, 2,000 prompts x up to 500 tokens (about 1M tokens per model, enough for about 100 events at a 1e-4 rate).
3. Verify the same logs under verifier-side conditions, one change at a time:
   - V0 released verifier (HuggingFace bf16, same GPU type): baseline.
   - V1 different GPU architecture: A100 (Ampere), L40S (Ada), and RTX 4090 for the 8B model.
   - V2 FP32 verifier (the generator stays bf16).
   - V3 FP32 for only the final norm and unembedding, and for the last 4 layers.
4. Generator-side conditions (new generation, 300k tokens each, then verified with V0 and V2):
   - G1 different concurrency (max 1, 8, 64 sequences) to isolate batch-composition noise.
   - G2 vLLM FP32 (Llama-3.1-8B on H100; Qwen3-30B-A3B on one H200).
   - G3 FP8 KV-cache on the generator only, and on both sides.
   - G4 vLLM used for both generation and prefill scoring, to remove the engine mismatch.
5. Repeat V0, V2 and G2 on the three stress prompt sets.
6. Metrics per cell: exact-match rate under teacher forcing; distribution of the score shortfall at mismatches (the empirical noise width); extractable bits/token and slowdown factor at false-positive rates 1e-3 and 1e-4 using the released sigma and rank sweep; measured throughput relative to the reference. Bootstrap confidence intervals over prompts.
7. Offline, no extra compute: from the logged margins, evaluate the paper's suggestion that the server resolve near-ties by a canonical rule (hypothesis: ambiguity just moves to the rule's boundary).

**Key analysis.** One table per model (configuration vs bound, false-positive rate, throughput cost) and one plot of bound against measured noise width across all cells.

## 4. Stage 1 cost estimate
RunPod on-demand prices read 2026-11-14: H100 PCIe $2.89/h, A100 PCIe $2.09/h, L40S $1.09/h, RTX 4090 $0.89/h, H200 $5.29/h.
- Reproduction and pipeline debugging: 12 h H100 = $35.
- Reference and generator-side generation (about 2M + 2.5M tokens, FP32 runs several times slower): 14 h H100 = $40; 5 h H200 = $26.
- Verification passes (prefill; about 25 passes over up to 1M tokens, FP32 passes slower): 14 h H100 = $40; 10 h A100 = $21; 10 h L40S = $11; 5 h RTX 4090 = $4.
- Downloads, idle time, storage: $30.
- Subtotal $207; margin for reruns and unavailable GPU types (about 60%): $123.
- **Total: $330.** No API spend is needed.

## 5. What success looks like
A clear finding is any of:
- A cheap knob moves the bound a lot: for example an FP32 verifier or matched GPU type cuts bits/token by 5x or more at 1e-4 false-positive rate with under 10% verifier cost, and the stress-prompt bound falls with it.
- Only two-sided FP32 helps, and its throughput cost is measured.
- Nothing short of bitwise determinism helps much (all cells within 2x). This is a publishable null: it says the published bound is near the practical limit, and names the dominant noise source.
An ambiguous result would be large run-to-run variance within a cell; step 2's sample size and a repeated V0 run are there to detect that.

## 6. Stage 2 (if stage 1 succeeds)
- Test whether the anytime-valid monitor of arXiv 2610.11843 keeps its false-alarm guarantee when calibrated on one hardware configuration and run on another, using stage 1's logs.
- Add reproducible kernels (arXiv 2609.25624) as the full-determinism endpoint; extend to 70B-class models and speculative decoding.
Rough cost: $1,000-2,000.

## 7. Risks and how the plan handles them
- **Reproduction fails or the pipeline is version-sensitive.** Pin the repo's versions (torch 2.7.1, transformers 4.53.2, vllm >= 0.10.0); step 1 is a hard gate with two independent numeric targets.
- **Too few false-positive events.** 1M tokens per main cell; report 1e-3 as the primary operating point where a cell has fewer than 30 events at 1e-4.
- **Confounded conditions.** One change per cell; G4 separates engine mismatch from hardware noise; V0 is run twice to estimate the floor.
- **FP32 in vLLM is unsupported or too slow for the 30B model.** Fall back to LayerCast in HuggingFace with a seeded Gumbel-max sampler matched to the verifier, or report FP32 generation for the 8B model only.
- **Over-claiming.** Results are reported as changes in the paper's upper bound and in honest mismatch rates, not as measured leakage.
