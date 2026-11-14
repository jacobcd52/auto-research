# Stress-testing DiffusionGemma's "1.1x" claim: forced single-canvas serial reasoning, with and without the token bottleneck
cluster: cot-latent-architectures | stage-1 cost: $330 | follows up: How transparent is DiffusionGemma (and why it matters) (zoYXpdaMgFT43Wc24); Proposal for tracking the effects of architecture on monitorability (hLPGv8QjPcNLtDp3A)

## 1. What the prior work showed
DiffusionGemma (DG; `google/diffusiongemma-26B-A4B-it`, Apache-2.0) generates a 256-token canvas by up to 48
denoising steps and passes continuous vectors between steps. GDM's audit (arXiv 2606.20560) computed a naive
opaque serial depth 28.6x that of the autoregressive Gemma 4 it was fine-tuned from, then showed that replacing
the inter-step vectors with their top tokens keeps benchmark performance, which brings the figure down to 1.1x.
Monitorability evaluations came out similar to Gemma 4. A follow-up post ("Does DiffusionGemma do latent
reasoning?", code at github.com/japhba/diffusiongemma_latent_reasoning) showed even top-1 projection keeps
performance with a gentler sampler, and found only rare cases where the vector is load-bearing.

Both results describe default behaviour on ordinary benchmarks, where the model is free to write its reasoning.
The paper lists the untested cases as open problems: when the vector intervention fails (7.2.4), high-serial-depth
no-CoT tasks (7.3.3), single-canvas monitorability, since their evaluations span many canvases (7.3.5), monitors
that read intermediate tokens (7.3.6), and fine-tuning DG to hide reasoning (7.4). Greenblatt et al. say hidden
reasoning capacity should be measured well-elicited, including with fine-tuning; Redwood's essay notes the DG
result may only mean the model "has not learned to perform interesting latent reasoning". I found no work that
forces DG to answer without visible reasoning and measures serial depth, and no fine-tuning stress test
(searches 2026-11-14).

## 2. Question and why it matters
When DiffusionGemma must produce only an answer in a single canvas, how many serial reasoning steps can it do
across its denoising steps compared with Gemma 4 answering in one forward pass; is that reasoning visible in the
intermediate tokens; and does it survive the token bottleneck that justifies the 1.1x figure?

Three outcomes, all reportable. (i) DG's answer-only depth equals Gemma 4's no-CoT depth: the reassuring audit
extends to the regime that matters for hidden reasoning. (ii) DG goes deeper by iterating in the canvas, and the
intermediate values show up in the top tokens of earlier denoising steps: reasoning is hidden from a monitor that
reads the final text but not from one that logs the denoising history, a concrete deployment recommendation.
(iii) DG goes deeper, intermediates are not in the top tokens, and top-1 projection destroys the gain: a
counterexample to treating the vectors as interpretable, on a public model.

## 3. Stage 1 plan
Reused: DG and Gemma 4 26B-A4B weights; the follow-up post's DG worker, gentler sampler settings (96 steps,
temperature 1.0 to 0.5, entropy bound 0.02) and top-k projection code; Redwood's permutation-power and modchain
task generators (re-implemented from the published description); Unsloth's DG fine-tuning path. Built: the
answer-only harness, the denoising-history logger and the intermediate-token monitor.

1. **Tasks with a depth dial.** Permutation power (ball passed m times around a stated cycle), modchain (k
   modular steps), and two-to-four-hop factual composition. 100 items per depth, m from 1 to 12. With-reasoning
   accuracy is measured first on both models and only items both solve with reasoning are kept.
2. **Answer-only conditions.**
   - Gemma 4, thinking off, answer prefilled so the next token is the answer (single forward pass), with and
     without filler tokens before the answer.
   - DG, single canvas, thinking off, the canvas constrained to "<answer>" followed by padding, denoising steps
     in {1, 4, 16, 48, 96}; default soft vectors.
   - DG with top-1 and top-8 projection of the inter-step vectors at every step.
   - DG with part of the canvas pinned to filler at every step (free scratch positions that cannot show text),
     and DG with an unpinned scratch region whose final content is discarded.
   Primary metric: depth horizon, the largest m with accuracy >= 50%, per condition, with bootstrap intervals.
3. **Is the reasoning visible in the denoising history?** For every DG run log the top-5 tokens at every position
   and step. Metrics: the fraction of the m intermediate values that appear as a top-1 (or top-5) token at any
   step, and an LLM monitor (gpt-6-luna) asked which of two candidate problems was being solved, given (a) the
   final canvas with the answer redacted, (b) the top-1 history. This is Redwood's monitorability score applied
   to DG, single canvas.
4. **Causal check.** Where intermediates appear in the history, overwrite them mid-denoising with another valid
   value and test whether the final answer follows (thought-anchor style). Where they do not appear, compare soft
   against top-1 projection item by item.
5. **Light elicitation by fine-tuning.** One LoRA (rank 16) on DG and one on Gemma 4, trained on 5,000
   answer-only examples of the permutation task at mixed depths, then steps 2-4 repeated on held-out cycles. This
   is the minimum "well-elicited" condition; it uses the standard denoising loss and does not train against any
   monitor. If the DG training path is not working within half a day, this step is dropped and reported as not
   attempted.

Sample size: 3 tasks x 12 depths x 100 items x about 10 DG conditions is roughly 36,000 DG generations plus
about 7,000 Gemma calls, before the fine-tuned repeat on one task.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14 (RunPod pricing page; OpenRouter).
- GPU: RTX Pro 6000 96GB at $2.69/h (26B MoE is about 52 GB in bf16; H100 NVL 94GB at $3.19/h is the alternative).
  DG inference: 36,000 generations at about 2.5 s amortised with batching = 25 h. Gemma 4 baseline: 3 h.
  Causal-patching runs: 6 h. Two LoRA runs (about 5 h each) and their evaluation (8 h): 18 h. Setup, model
  download and debugging: 30 h. Total ~82 h = **$221**.
- gpt-6-luna monitor ($0.10 / $0.50 per 1M): 20,000 calls at about 1,500 input and 200 output tokens = **$5**.
- GPT-6 Sol spot check ($2 / $10 per 1M) on 600 histories at about $0.012 = **$7**.
- Storage for weights and logs (about 150 GB for two days): **$15**.
- Subtotal $248; margin ~33% for reruns: **total $330**.

## 5. What success looks like
- A horizon plot where DG answer-only depth rises with denoising steps well above Gemma 4's single-pass depth
  (for example Gemma 4 at 3 passes, DG at 8 or more with 48 steps), together with a clear answer on visibility:
  either intermediates appear in the top-1 history in most solved items and the history monitor scores above 0.8
  while the final-canvas monitor is near 0, or they do not and top-1 projection cuts the horizon back toward
  Gemma's. Either is a specific, checkable addition to the GDM audit.
- If DG shows no extra depth in any condition including after fine-tuning, the result is a tighter version of the
  reassuring claim. Publishable as a short post, the least exciting outcome; its value depends on step 5.
- Ambiguous: extra depth only on the factual-hop task (could be memorised shortcuts) or only at 96 steps with a
  non-default sampler. The synthetic tasks, where shortcuts are impossible, are the ones the conclusion rests on.

## 6. Stage 2 (if stage 1 succeeds)
- The model organism GDM asks for in open problem 7.4: train DG with a penalty on reasoning visible in the logged
  top-1 history, backpropagating through two or more denoising steps, and test whether computation moves into the
  non-top-1 part of the vectors and whether probes or the J-lens still find it. About $1,500 (multi-GPU-day).
- Single-canvas versions of GDM's monitorability evaluations on realistic tasks, with and without the history
  monitor. About $500.
- The same harness on other public text-diffusion models to see whether results are specific to a Gemma fine-tune.

## 7. Risks and how the plan handles them
- **Under-elicitation.** Prompting an untuned model to "just answer" may understate what it can do. Step 5 exists
  for this; the scratch-region conditions give the model room without fine-tuning.
- **Sampler artifacts.** The follow-up post showed projection results depend on the sampler. All projection
  conditions use its gentler sampler, and default-sampler numbers are reported alongside.
- **Tooling on a 26B MoE diffusion model.** Reuse the follow-up post's worker, run its truncation-ladder
  experiment as a smoke test, keep fine-tuning optional.
- **Shortcut solutions and format confounds.** Synthetic tasks with fresh random cycles; answer position fixed;
  filler counts matched between Gemma and DG conditions, following the published warning about position confounds
  in no-CoT benchmarks.
- **Canvas constraint is not obeyed** (DG writes reasoning anyway). Enforce by pinning non-answer positions, and
  count any item with reasoning tokens in the final canvas as failed.
- **Low reader interest in DG.** Frame around the general lesson: default-behaviour audits versus elicited ones,
  and whether monitors must log intermediate states.
