# NOTES — cluster single-7i33FD (Inference verification against weight exfiltration)

Written 2026-11-14. One post in the cluster; one proposal written (`01-noise-budget-for-inference-verification.md`).

**Search caveat.** The WebSearch tool was unavailable this session (shared budget exhausted). Related-work search was done
with the arXiv API (keyword queries), the LessWrong GraphQL API (post comments, authors' later posts), the Hugging Face
API and raw.githubusercontent.com. A general web search for blog posts / non-arXiv follow-ups was NOT possible; a
reviser with search access should re-check for duplicates, especially from the original authors.

## 1. The post (read in full) and its paper

Post: "Defending Against Model Weight Exfiltration Through Inference Verification", LW id 7i33FDCfcRLJbPs6u,
2025-12-15, 121 karma. Rinberg, Karvonen, Hoover, Reuter, Warr. Paper: arXiv 2511.02620 (v3 title "Verifying LLM
Inference to Detect Model Weight Exfiltration").

Claims verified from post + paper HTML:
- Threat: a compromised inference server hides weight bits in output tokens. Output text is the one egress channel that
  cannot be capped.
- Idea: log (input, output, sampling seed); a separate trusted verification server re-runs the forward pass (prefill
  only, teacher-forced) with the same seed and scores each emitted token by its Fixed-Seed Sampling Likelihood (FSSL):
  how likely the token is under benign numerical noise. Estimators: Token-DiFR / "GLS" for Gumbel-max sampling (vLLM),
  Token-IPT-DiFR / "CGS" for inverse-probability-transform sampling (HF, Ollama).
- Bound: at each position the admissible set A_t(tau) = tokens with FSSL >= tau; an accepted token can carry at most
  log2|A_t| bits. Three-class rule with logit rank R: safe / suspicious (log2 R bits) / dangerous (log2 |vocab| bits).
- Setup (Section 7): 500 prompts from LMSYS-Chat-1M, max 500 new tokens, temperature 1.0, top-k 50, top-p 0.95, fixed
  seed, generation with vLLM. Models: Llama-3.2-3B-Instruct, Llama-3.1-8B-Instruct, Qwen1.5-MoE-A2.7B, Qwen3-30B-A3B.
  Gumbel sigma swept 0.001 to 1.0. Headline: extractable information < 0.5% of the theoretical maximum at FPR ~0.01%
  (Qwen3-30B-A3B), "over 200x slowdown". About 2% of tokens are "branching points". Context-length ablation with
  LongBench v2 (4k/8k/12k tokens).
- README quick-start output: 18,531 tokens, 99.93% safe, 0.07% suspicious, 0 dangerous; "verify 18,500 tokens in 17 s".
- Sampling-rate argument: ~1 verification GPU per ~200,000 inference GPUs for 99.9999% confidence of catching >=1,000
  malicious messages if 1% of traffic is malicious.
- Authors' own suggested directions: (a) keep the seed secret from the receiver / fresh seed per token (capacity under
  seed uncertainty "not fully characterized"); (b) fully deterministic inference drives capacity to zero (Thinking
  Machines batch-invariant kernels, ~60% overhead quoted in the post); (c) verification-aware sampling: when several
  tokens have high FSSL the server picks one by a deterministic rule (paper Discussion); (d) TEE-hosted verifier;
  (e) privacy-preserving verifier; (f) speculative decoding (paper App. F); (g) adversarial prompts that add branching
  points and correlated permitted tokens ("may be interesting for future work", paper Section 5.3); (h) response
  policies and pooled analysis of suspicious tokens (App. G).
- Comments (top): Fabien Roger — removing nondeterminism is hard across two kinds of hardware; Buck — verifier knowing
  the seed is doable; Alek Westover — "random bits" prompts; Karvonen reply — near-determinism holds even for
  high-entropy prompts given the seed (at most ~3 plausible tokens); faul_sname — logs as another channel; Karvonen —
  output volume estimates.

## 2. Related work and follow-ups found

| Work | What it did | Relevance |
|---|---|---|
| DiFR, arXiv 2511.20621 (Karvonen et al., 2025-11) | Token-DiFR and Activation-DiFR for auditing providers. Reference: vLLM bf16. Honest variation pool: H200 TP-4, A100 no-TP, A100 TP-4, H200 HuggingFace. Misconfigs: 4-bit quant, FP8 KV-cache, temperature 1.1, wrong seed, simulated sampling bug. Reports detection AUC vs token count. Pooling more honest configs broadens the null and weakens detection of small deviations. | Hardware variation was studied for *detection AUC of misconfigurations*, NOT for the exfiltration capacity bound, and not decomposed by source. |
| Kezins, arXiv 2608.23375 (2026-08, NeurIPS FLMSec workshop, 4 pp.) | Prompt families that raise output entropy (TERSE / SCRAMBLE / CIPHER) vs 150 benign LMSYS prompts, 6 models (Llama-3.2-1B/3B, Llama-3.1-8B, Qwen2.5-14B, Qwen3-30B-MoE, Qwen3-32B), 3 seeds, sigma = 1.0. Benign bits/token 0.067-0.119 (slowdown 146-254x); worst family 0.145-0.286 bits/token (60-118x). Recommends entropy-calibrated thresholds; does not test any defence. Built on the released framework. | The "adaptive prompt distribution" red-team from the screener's note is DONE. Defence side untested. |
| Ortega-Fernandez, Kowalczyk, Warr, arXiv 2610.11843 (2026-10, NeurIPS e-values workshop oral) | Prompt-level e-process that pools whole-response mismatch events with anytime false-alarm control; evaluated on four models against seed-blind and seed-aware senders; capacity vs detectability trade-off. Assumes calibration and monitoring share prompt distribution, model, hardware and serving stack. | Pooled / sequential detection is DONE. Its calibration-transfer assumption across hardware is untested (stage-2 hook). |
| Yuan et al., arXiv 2506.09501 ("Give me FP32 or give me death", LayerCast) | bf16 inference diverges across batch size, GPU count, GPU type; FP32 compute nearly removes divergence; LayerCast stores 16-bit weights and computes in FP32. Code: github.com/nanomaoli/llm_reproducibility (README reachable via raw.githubusercontent). | Gives the cheap determinism knob; never connected to the verification bound. |
| Cooper et al., arXiv 2609.25624 (2026-09) | Fixed-reduction-order fused-upcast GEMM kernels; bitwise-identical linear layers across Ampere/Ada/Hopper; 1.17-3.1x faster than prior deterministic solution. Code availability not verified. | Full-determinism end of the spectrum; stage-2 candidate. |
| Thinking Machines "Defeating nondeterminism in LLM inference" (cited in post) | Batch-invariant kernels; Qwen3-235B 1,000 temperature-0 completions gave 80 unique outputs. | Same. |
| Brown et al., arXiv 2601.01296; Rinberg LW post "Text Compression Can Help Secure Model Weights" (GcbkprYPCjXdysLq4, 2026-03, 45 karma) | Compression of weights (attacker) / of text egress (defender). | Adjacent; not about verification. |
| Petrie & Mühlhäuser 2026 (ICML TAIG workshop, cited by Kezins) "Verifying AI compute by bounding unexplained information exfiltration" | Bilateral compute verification with the same bound. | Not on arXiv search; not read. |
| Karvonen 2024 LW "Using an LLM perplexity filter to detect weight exfiltration" (aWZEDw6oxR6Wk5hru) | Precursor. | |

Not found (arXiv keyword search only): any work that (i) decomposes the capacity bound by noise source, (ii) measures
how FP32 / matched hardware / fixed batching on the verifier or generator side changes the bound, or (iii) checks
whether such knobs restore the bound on the high-entropy prompt families.

## 3. Public artifacts verified

- Code: https://github.com/RoyRin/inference_verification_for_model_weight_exfiltration (github.com HTML and codeload
  return 403 from this sandbox; raw.githubusercontent.com works). Verified present on `main`:
  `inference_verification/generate.py` (vLLM generation), `inference_verification/verify.py` (16.9 KB; verifier loads
  the model with **HF `AutoModelForCausalLM`, `torch_dtype=torch.bfloat16`** and scores by prefill — so dtype and
  device on the verifier side are one-line changes), `inference_verification/analysis/analyze_thresholds.py`,
  `analyze_two_step_classifier.py`, `scripts/test_minimal.sh`, `scripts/run_GLS_all_models.sh`,
  `demonstration/config_example.yaml` (temperature 1.0, top_k 50, top_p 0.95, seed 42, gumbel_sigma 1.0,
  gls_threshold -5.0, logit_rank_threshold 32, dataset lmsys/lmsys-chat-1m, max_ctx_len 512), `pyproject.toml`
  (torch 2.7.1, transformers 4.53.2, vllm >= 0.10.0). No released token logs were seen in the files checked.
- DiFR releases a vLLM integration (per abstract); repo URL not verified.
- Datasets (HF API): `lmsys/lmsys-chat-1m` gated = auto (needs an HF account that has accepted terms);
  `allenai/WildChat-1M` gated = False; `HuggingFaceH4/ultrachat_200k` gated = False.
- Models (HF API): `meta-llama/Llama-3.1-8B-Instruct` gated = manual; `unsloth/Llama-3.1-8B-Instruct` ungated mirror;
  `Qwen/Qwen3-30B-A3B`, `Qwen/Qwen3-8B`, `Qwen/Qwen2.5-14B-Instruct`, `Qwen/Qwen1.5-MoE-A2.7B-Chat` all ungated.
- Kezins' prompt sets / code: availability not verified (paper says it builds on the released framework).
- RunPod on-demand prices read from runpod.io/pricing on 2026-11-14: RTX 4090 24 GB $0.89/h; A40 48 GB $0.59/h;
  L40S 48 GB $1.09/h; A100 PCIe 80 GB $2.09/h; A100 SXM $2.19/h; H100 PCIe 80 GB $2.89/h; H100 NVL 94 GB $3.19/h;
  H200 141 GB $5.29/h; B200 180 GB $7.99/h.

## 4. Brainstorm

Judged on: doable by Claude agents in ~2 days for <= $500; novel given section 2; interesting either way.

1. **Noise budget: which determinism knobs shrink the bound (WRITTEN, proposal 01).** The bound is set entirely by
   numerical disagreement between generator and verifier, but nobody has measured how much each source contributes or
   what partial determinism (FP32 verifier, FP32 both sides, matched GPU, fixed batch) buys. Pure measurement on
   released code; cheap; every cell of the table is informative; directly answers Fabien Roger's comment and the
   post's "60% overhead for full determinism" framing by filling in the points between "do nothing" and "bitwise
   deterministic". Also the screener's suggested follow-up, minus the part already done by Kezins.
2. **Do the knobs restore the bound on high-entropy prompt families?** Folded into proposal 01 as a condition (tests
   Kezins' recommendation from the defender's side). On its own too thin.
3. **Verification-aware sampling (authors' Discussion suggestion).** Server resolves near-ties by a canonical rule.
   My analysis: a deterministic rule on noisy logits still has a decision boundary, so ambiguity moves to wherever the
   rule's boundary is; gain exists only if the margin density at the new boundary is lower than at zero, and the rule
   distorts the sampling distribution. Not obviously a win, but can be evaluated OFFLINE from the margins recorded in
   proposal 01, so it is included there as a no-extra-cost analysis rather than a separate project. (My boundary
   argument is unverified; treat as a hypothesis.)
4. **Pooled / sequential detection across responses.** Rejected: done by arXiv 2610.11843.
5. **Adaptive prompt-distribution red-team.** Rejected: done by arXiv 2608.23375. Building stronger concrete covert
   encoders is also not something this programme should fund; the bound is information-theoretic, so a defender-side
   measurement is more useful than an attack implementation.
6. **Capacity under seed secrecy (authors' open question).** Rejected for stage 1: mostly theory; an empirical version
   requires modelling what a receiver can infer without the seed, which is hard to do convincingly in two days and
   easy to over-claim. Possible later theory note.
7. **Does the e-process calibration transfer across hardware?** (2610.11843 assumes same hardware/stack.) Good, but
   depends on their code (availability not verified). Listed as stage 2 of proposal 01, which produces exactly the
   per-hardware mismatch data needed.
8. **Speculative decoding verification (paper App. F, DiFR App. F).** Rejected: fragile engineering (vLLM spec-decode
   plus a custom verifier), risk of spending two days on plumbing.
9. **Larger models (70B+) and long reasoning traces.** Partly rejected: cost fine on H200, but adds little beyond
   "also holds at 70B". Stage 2.
10. **Quantised serving (AWQ/GPTQ 4-bit, FP8) as the legitimate production config with matching verifier.** Reasonable
    extra row for proposal 01 (FP8 KV-cache on both sides); full 4-bit study rejected as scope creep.
11. **Audit public API providers with Token-DiFR.** Rejected: DiFR App. D already did an in-the-wild audit of
    Llama-3.1-8B providers; needs seed-synchronised sampling that most providers do not expose.
12. **TEE-hosted verifier / privacy-preserving verifier.** Rejected: systems engineering, not a 2-day experiment.
13. **Log-channel exfiltration (faul_sname comment).** Rejected: out of scope and needs production infrastructure.

Why only one proposal: the cluster allows one, and after removing what 2608.23375 and 2610.11843 already did, idea 1
(with 2, 3 and 10 folded in) is the clear remaining measurement that reuses the released code and cannot come out
uninteresting.

## 5. Facts for the reviser
- Kezins' benign numbers at sigma = 1.0 give a reproduction target: Llama-3.1-8B 0.068 +/- 0.002 bits/token (252x);
  Qwen3-30B-MoE 0.119 +/- 0.011 (146x). Slowdown = log2(vocab) / bits-per-token.
- The released pipeline is already engine-mismatched by design: vLLM generates, HF verifies in bf16.
- Qwen3-30B-A3B in FP32 is ~122 GB of weights: needs an H200 (141 GB) or LayerCast-style 16-bit storage.
- vLLM exposes a `--dtype` option (float32 allowed per my recollection of the docs; NOT re-verified this session).
- FPR of 1e-4 per token needs >= ~1M honest tokens per configuration for ~100 events.
