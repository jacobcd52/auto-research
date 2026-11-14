# Feedback: A noise budget for inference verification

Reviewer verdict: **keep with tweaks**, but the framing must change because of a missed prior paper (arXiv 2606.00279), and the matrix must be cut.

Search caveat: the WebSearch budget was exhausted for me as well. I checked with the arXiv API, arXiv HTML, the LessWrong API, raw.githubusercontent.com, the Hugging Face API and runpod.io. Blog posts and non-arXiv follow-ups are still unchecked.

## What I verified

| Claim in the proposal | Status |
|---|---|
| Paper setup (500 LMSYS prompts, 500 tokens, T=1, top-k 50, top-p 0.95, vLLM, four models, sigma sweep 0.001-1.0, <0.5% at <0.01% FPR on Qwen3-30B-A3B) | Confirmed from arXiv 2511.02620 HTML and abstract. |
| Released repo has `generate.py`, `verify.py` (HF, `torch_dtype=torch.bfloat16`, `device_map="auto"`), `scripts/test_minimal.sh`, analysis scripts, pinned versions | Confirmed via raw.githubusercontent.com. |
| Kezins benign numbers (8B 0.068 +/- 0.002, 30B-MoE 0.119 +/- 0.011; worst case 60-118x) | Confirmed from arXiv 2608.23375 HTML. No code or prompt-set link found in the paper text. |
| arXiv 2610.11843, 2506.09501, 2609.25624 exist and say what is claimed | Confirmed from abstracts. |
| `unsloth/Llama-3.1-8B-Instruct` and `Qwen/Qwen3-30B-A3B` ungated | Confirmed (HF API). |
| RunPod prices | Confirmed as Secure Cloud prices (H200 $5.29, A100 PCIe $2.09, L40S $1.09, RTX 4090 $0.89). Community Cloud is cheaper (A100 $1.19, L40S $0.79, 4090 $0.34, H200 $3.59). |
| "Fully deterministic inference ... at a quoted 60% overhead" (attributed to the post) | **Not found.** The post body (36k characters) contains no such figure. arXiv 2606.00279 cites about 20% throughput loss for the Thinking Machines kernels. Fix the number and its source. |
| "Not done: measuring how much each noise source contributes" | **Partly wrong.** See next paragraph. |

**Missed prior work: Cankaya et al., "Bit-Exact AI Inference Verification Without Performance Tradeoffs" (arXiv 2606.00279, 2026-05).** It cites Rinberg et al. directly and reports that vLLM and HF transformers give bitwise-identical prefill and decode outputs (L2 = 0) when hardware SKU, software stack, attention backend, quantization and batch composition are fixed, without any determinism flags. It lists the factors a verifier must know, and reproduces outputs across L40/L40S/A100/H100 with a CPU emulator. It also reports that different physical cards of the same SKU agree exactly. This is a qualitative noise decomposition, already published, with the conclusion that the "noise" is deterministic configuration mismatch. It does not report the exfiltration bound in bits/token per mismatch, so the proposal's quantitative table is still new, but the motivating claim that labs have only two data points (0.5% or expensive determinism) is no longer true.

Also relevant and uncited: TBIK (arXiv 2511.17826), which is in the same `nanomaoli/llm_reproducibility` repo the proposal plans to use, and gives bitwise batch- and TP-invariant kernels.

## 1. Would it get upvoted?

Borderline. The parent post got 121 karma with a new method, a headline number (200x) and well-known authors. A follow-up that is a configuration table would typically land at 25-60. It clears 50 only with a one-line headline that changes what a lab would do, for example "logging batch composition and matching the GPU SKU takes the bound to exactly zero; each thing you fail to match costs X bits/token" or "FP32 on both sides cuts the bound 10x without any matching". The audience is small (security-minded safety people, the original authors, Fabien Roger's comment thread), but it is the right audience and they do upvote concrete numbers.

The "nothing short of bitwise determinism helps" outcome is not a publishable null any more: after 2606.00279 the obvious reply is "so do bitwise re-computation". I estimate about 35% chance of >50 karma if executed well with the reframing below, about 20% as written.

## 2. Naturalness

Mainline. It is the screener's suggested follow-up, it answers the top comment on the post, and the released code supports it. It is not contrived. The issue is overlap, not direction: 2606.00279 has taken the "which sources matter, and can you remove them" question, and DiFR already ran the hardware variations (for detection AUC). What remains is the translation into the bound at a fixed false-positive rate. That is a real gap but a narrower one than the proposal states.

## 3. Pre-mortem

How it plays out: day 1 goes to getting vLLM 0.10 plus the pinned torch running on four GPU types, reproducing the quick-start, and generating the reference logs. V-side cells are then easy (same logs, patched verifier). G-side cells are where time goes, especially G4.

Forecast:
- Clear positive result (a knob moves the bound by 5x or more with tight intervals): 25%
- Clear negative that is still interesting: 20%
- Ambiguous mush (cells within noise of each other at 1e-4, differences of 1.3-2x with overlapping intervals): 35%
- Fails to run or delivers only the V-side cells: 20%

Specific problems:

1. **The reproduction gate does not test what matters.** In `analyze_two_step_classifier.py`, bits at a fixed (sigma, threshold, rank) are computed from the verifier's own logits; generator-verifier noise enters only through the false-positive rate. Kezins' 0.068 and 0.119 are fixed-sigma numbers, so matching them shows the logits and prompt mix are right and says almost nothing about whether the noise measurement is right. The gate needs a noise-sensitive target: the README's safe/suspicious split (99.93% / 0.07% on 18.5k tokens) and the paper's Figure 9 frontier.

2. **V2 and V3 are likely null by construction.** An FP32 verifier against a bf16 generator still sees the generator's bf16 rounding error in full. LayerCast's result is for FP32 on both sides. The disagreement could even grow, because two bf16 runs share systematic rounding that an FP32 run does not. V3 (FP32 for the last layers only) has the same problem and no clear deployment story. These are the cheap cells and they will dominate the table with uninformative rows.

3. **Every V cell carries the engine mismatch.** The baseline is vLLM decode with KV cache and batching against HF prefill, single sequence. If that mismatch dominates, changing the verifier GPU from H100 to A100 moves nothing, and the proposal will report "GPU type does not matter" when it only showed it is masked. G4 is meant to fix this but is the hardest cell: it needs unfiltered logits out of vLLM with the exact Gumbel noise reconstruction. Use the DiFR vLLM integration if its repo can be found; otherwise this is a day of plumbing.

4. **Matched cells will probably be exactly zero.** Per 2606.00279, same SKU plus same stack plus same batch composition is bit-exact. Concurrency 1 on both sides with the same engine should give zero mismatches. The plan has no place for this outcome, and it is the anchor the whole table should hang from.

5. **Tail statistics.** The frontier at 1e-4 is set by a few dozen honest tail tokens, and they cluster within prompts (one MoE routing flip produces several). With 300k tokens the G cells have about 30 events at 1e-4, and effective sample size is closer to the number of affected prompts. "Within 2x" versus "5x" will not be separable at 1e-4 for G cells.

6. **Selection bias in the frontier.** The released analysis picks the best (sigma, threshold, rank) on the same tokens used to estimate the false-positive rate. Comparing optimised frontiers across cells at the 1e-4 tail flatters every cell by a different random amount. Thresholds need to be picked on one half of the prompts and evaluated on the other.

7. **Stress prompts.** Kezins' prompt sets are not confirmed public; rebuilding three families from a 4-page workshop paper means the "stress" numbers will not be comparable to hers, and elicitation quality is unverified. Three families times three conditions is also a large slice of the budget for a secondary question.

8. **Scope.** Two models, four verifier conditions over up to four GPU types, four generator conditions each verified twice, three stress sets, and an offline near-tie analysis. Agents will finish the easy cells and run out of time on the informative ones.

9. **Qwen3-30B-A3B in FP32 on one H200.** About 122 GB of weights in 141 GB leaves little for KV cache and activations at concurrency above a few sequences; H200 availability on RunPod is also not guaranteed. Likely ends as 8B-only for the FP32 generator cell.

## 4. Cost check

The estimate is realistic and probably slightly high. Prices are correct (Secure Cloud). Token volumes are small: 1M tokens of 8B generation is well under an hour on an H100, and prefill verification is fast (the README's 18.5k tokens in 17 s). FP32 passes and the 30B model are the only slow parts. Real risk is idle GPU time while debugging across several pod types, plus model download time on each pod (60 GB for the 30B model, four pod types).

My estimate: $180-300 for the full matrix, $120-200 for the trimmed version below. $330 is a safe cap.

## 5. Recommended changes

1. **Cite 2606.00279 and reframe around it.** New question: "Bit-exact re-computation needs the verifier to match SKU, stack and batch composition. What does each failure to match cost in bits/token at a fixed false-positive rate, and does FP32 on both sides remove the need to match?" Start from a fully matched cell (same engine, same SKU, concurrency 1), confirm zero mismatches, then break one factor at a time: batch composition, GPU SKU, engine (vLLM vs HF), KV-cache quantization, tensor parallelism if cheap. This makes every row interpretable and gives the "price list" headline.

2. **Fix the reproduction gate.** Replace the Kezins fixed-sigma targets with noise-sensitive ones: quick-start safe/suspicious fractions, exact-match rate, and the paper's Figure 9 frontier for Qwen3-30B-A3B. Keep Kezins' numbers as a secondary sanity check on logits only.

3. **Drop V3; demote V2.** Keep one FP32-verifier-only row as a stated control with the prediction that it does not help. Make FP32 on both sides (G2) a primary cell, on the 8B model, with LayerCast as the fallback for the 30B model.

4. **Decide G4 early.** Spend at most half a day on a vLLM-side scorer (look for the DiFR vLLM integration first). If it fails, invert the design: generate with a seeded Gumbel-max sampler in HF so that generator and verifier share an engine, and treat vLLM as the "engine mismatch" row.

5. **Fix the statistics.** Split prompts into calibration and evaluation halves for threshold selection. Use 1e-3 as the primary operating point and report 1e-4 only for cells with 1M tokens. Bootstrap over prompts, and report threshold-free metrics alongside (exact-match rate under teacher forcing, margin distribution at mismatches) so that results do not depend on tail estimates. Run the baseline cell twice with different prompt samples to show the floor.

6. **Cut stress prompts to one family** (the strongest, CIPHER-style) on two conditions (baseline and the best knob), 150 prompts. If the author's prompts are not public, say so and label the numbers as a re-implementation.

7. **Drop the RTX 4090 cell and the offline canonical-rule analysis from the plan.** Keep the latter as optional if time remains; it is a hypothesis without a clear test.

8. **Correct the "60% overhead" claim** or cite its actual source; include the roughly 20% figure cited in 2606.00279.

9. **Add a throughput column only for cells where it is meaningful** (FP32 both sides, concurrency limits). Verifier-side throughput on a 1-in-200,000 sampling design is irrelevant and should be said so.

10. **State up front what would be boring.** If matched cells are zero and all mismatches cost about the same as the paper's baseline, the write-up should lead with the logging requirements for bit-exact verification applied to the exfiltration setting, not with a null table.
