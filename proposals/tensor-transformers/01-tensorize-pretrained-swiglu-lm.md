# What does it cost to turn a pretrained SwiGLU language model into a tensor transformer by fine-tuning?
cluster: tensor-transformers | stage-1 cost: $260 | follows up: "Tensor-Transformer Variants are Surprisingly Performant" (hp9bvkiN3RzHgP9cq); "If you're interpreting <1B parameter models, you should use a tensor transformer" (expsAXaBgiqgitFe6)

## 1. What the prior work showed
A "tensor transformer" replaces the non-polynomial parts of a transformer so the network is a tensor network
analysable from its weights: the MLP becomes a bilinear layer `D(Lx ⊙ Rx)` (SwiGLU, `D(swish(Lx) ⊙ Rx)`, minus
the swish), and softmax attention becomes bilinear attention, whose pattern is the elementwise product of two
dot-product score matrices with no softmax.

- Post hp9bvkiN3RzHgP9cq trained four ~500M-parameter models **from scratch** on FineWeb. Bilinear vs SwiGLU MLP
  was about equal; bilinear attention needed about 4% more batches to reach CE 3.0. At GPT-2-small size the
  tensor variants were "much worse", attributed by the author to untuned hyperparameters.
- Post expsAXaBgiqgitFe6 argues small-model interpretability should use tensor transformers, and conjectures
  that, because SwiGLU and bilinear layers have no global Lipschitz constant, "results like finetuning away the
  normalization might not generalize to these SOTA archs since this was only run on single-encoder MLPs."
- Existing conversions. (a) arXiv 2410.08417 (appendix) fine-tuned away the SwiGLU gate of TinyLlama-1.1B by
  annealing Swish-beta to 0 over 400M tokens: loss 2.217 vs 2.168 for a continued-training control (about +0.05);
  one schedule, MLP only. (b) LayerNorm removal by fine-tuning works for GPT-2 small (arXiv 2409.13710, about
  0.05 CE, 500M tokens; code `github.com/ApolloResearch/gpt2_noLN`) and GPT-2 XL (arXiv 2507.02559, +0.03 CE) —
  all GELU-MLP, softmax models.
- Not done, as far as arXiv queries, the author's posts/repos and Hugging Face show (general web search was
  unavailable at drafting; re-check): converting **pretrained softmax attention** to bilinear attention; removing
  **RMSNorm from a SwiGLU or bilinear model**; a per-component account of what tensorizing a real pretrained
  model costs. All released tensor-transformer checkpoints (`Elriggs/gpt2-bilinear-*`) were trained from scratch.

## 2. Question and why it matters
**For a real pretrained SwiGLU model, how much cross-entropy does each step toward a tensor network cost when done
by fine-tuning — (i) removing the swish gate, (ii) replacing softmax with bilinear attention, (iii) removing
RMSNorm — and does norm removal get harder once the MLPs are GLU/bilinear, as the second post conjectures?**

If a pretrained model can be tensorized for a few hundredths of a nat in under a GPU-day, the "use a tensor
transformer" advice no longer requires pretraining a custom architecture, and we release the checkpoints. If one
component is expensive (most likely softmax), that shows which non-polynomial part pretrained models rely on and
qualifies the from-scratch "4% more batches" result. The norm arm turns an untested remark into a number.

## 3. Stage 1 plan
**Reused.** `HuggingFaceTB/SmolLM2-135M` (Apache-2.0; 30 layers, d=576, 9 heads / 3 KV heads, SwiGLU, RMSNorm).
Fine-tuning text: a fixed slice of `HuggingFaceFW/fineweb-edu`; evaluation on held-out FineWeb-edu plus
`roneneldan/TinyStories` validation as an out-of-distribution set. Gate schedule from 2410.08417; norm-removal
recipe from `ApolloResearch/gpt2_noLN`; bilinear attention as defined in `loganriggs/tensor_language/model.py`.
**Built.** The attention-conversion wrapper and run harness.

**Arms** (200M tokens each, identical data order and optimiser; learning rate picked once on the control from 3
values; * = 2 seeds):
0. *Control: continued training, architecture unchanged. All deltas are against this arm.
1. *Gate removal: Swish-beta annealed 1 -> 0 over the first 30%.
2. *Attention conversion: add `Q2, K2` per head (copies of `Q, K` plus a learned per-head scale) and blend
   `P = (1-a)·softmax(S1) + a·(S1 ⊙ S2)·mask/c`, annealing `a` 0 -> 1 over the first 50%. Variants: tied (squared
   attention), untied, untied with logit distillation from the frozen original.
3. Norm removal on the original model (each RMSNorm scale replaced by a fixed constant, group by group).
4. Norm removal on the output of arm 1. Arm 3 vs arm 4 is the test of the Lipschitz conjecture.
5. Tensor transformer in the post's sense: best arm-2 variant on top of arm 1, RMSNorm kept.
6. If stable: arm 5 plus norm removal, an exactly polynomial network.

**Steps.** (1) Load the model, measure tokens/second, fix the token budget. (2) Run arms 0 and 1; arm 1 should
land near the published +0.05, which checks the pipeline. (3) Pilot arm-2 variants at 30M tokens, keep the best
two. (4) Run arms 3-6. (5) Exactness checks: converted MLPs satisfy `f(ax) = a²f(x)` to float precision; at
`a=1` no softmax is called. (6) Analysis.

**Metrics.** Delta CE vs control on both eval sets with bootstrap CIs over documents; token-equivalent cost;
stability (loss spikes, gradient-norm excursions); attention-pattern entropy and negative mass before/after (the
post claims bilinear patterns are denser); loss breakdown by token category (copy/induction positions vs
bigram-like positions) to see what losing softmax hurts.

**Key analysis.** One table (component x delta CE x stability) and loss-vs-tokens curves per arm. GPT-2 norm
removal numbers are an outside reference only, since the model differs.

## 4. Stage 1 cost estimate
Assumption to be measured in step 1: about 40k training tokens/s for a 135M model at length 512 in bf16, so 200M
tokens is about 1.4 GPU-hours.
- Full runs: arms 0, 1 and two arm-2 variants at 2 seeds (8 runs) + arms 3-6 (4 runs) = 12 x 1.4 h = 17 GPU-h.
- Pilots, learning-rate selection, evaluation: 15 GPU-h. Subtotal 32 GPU-h.
- RunPod community prices looked up 2026-11-14: RTX 5090 $0.69/h, A100 PCIe $1.19/h, H100 PCIe $1.99/h. At the
  A100 rate: 32 x $1.19 = $38.
- Margin for 2x slower throughput and reruns of unstable arms: 4x = $152. Second seeds for arms 3-6: $27.
- Storage and idle time $40; reserve $40.
- **Total: about $260.**

## 5. What success looks like
- "SmolLM2-135M becomes a tensor transformer for +X nats": the full ladder with CIs (gate near +0.05, attention
  +Y, norms +Z) and released checkpoints. A total under about 0.15 nats is a headline result and a usable
  artefact.
- Or "softmax is the expensive part": attention conversion costs several times the gate even with distillation,
  in contrast to the from-scratch result, with the token-category breakdown showing what is lost.
- Norm conjecture resolved: arm 4 diverges or costs clearly more than arm 3 (supported), or both are small (not
  supported at this scale).

Ambiguous: arm 2 still improving steeply at 200M tokens; we report slope and token-equivalent cost as a bound. A
null on the conjecture alone is not a post; the ladder is.

## 6. Stage 2 (if stage 1 succeeds)
- `SmolLM2-360M` and a 0.6B-class SwiGLU model, with 1-2B-token schedules for attention (about $300-600).
- Use the converted model as a test bed: tensor similarity (`github.com/tdooms/tensor-similarity`) across
  fine-tunes of it, and the author's weight-only tools (`tensor_language/jacclust`) on a model with a standard
  training history (about $300).
- Check whether tensorization preserves known circuits or only loss (about $300).

## 7. Risks and how the plan handles them
- **Attention conversion fails to train** (the hardest arm). Three variants, blended anneal, distillation, and a
  pilot before full runs. A robust failure is reported as a finding; arms 0, 1, 3, 4 stand alone.
- **Instability after norm removal with unbounded bilinear activations.** This is the conjecture under test.
  Gradient clipping and the staged schedule are used; divergences and all retries are reported, not hidden.
- **Under-training mistaken for architectural cost.** Deltas are against the control at equal tokens, with
  slopes shown and two seeds on main arms.
- **Implementation bugs** (masking, RoPE, grouped KV heads). At `a=0` the wrapper must reproduce the original
  logits to float tolerance; this test gates all runs.
- **Scale caveat.** 135M parameters may not predict larger models; the arm-1 comparison with the 1.1B TinyLlama
  number gives one cross-scale anchor.
- **Novelty.** The team should spend 15 minutes confirming nobody has published softmax-to-polynomial conversion
  or RMSNorm removal on a SwiGLU model before starting.
