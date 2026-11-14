# Is taught alignment one direction deep? Activation-space analysis of the released "Teaching Qwen Why" adapters
cluster: alignment-pretraining | stage-1 cost: $220 | follows up: Teaching Qwen Why (35yw2qGK7naFLAvcq); Synthetic Persona Pretraining (3xQQK9i8mhJDE2uMg); Model Spec Midtraining (R3Rrw8EscuRKxMFTz)

## 1. What the prior work showed
- **Teaching Qwen Why** (TQW) reduces agentic misalignment (AM: an email-agent eval where the model can exfiltrate
  its weights, leak documents, or let someone die) on Qwen2.5-32B from 61% to 43% with story midtraining, to 6%
  with "difficult advice" SFT, and to 4% with both. It released 46 chained LoRA adapters and a per-condition score
  table. From that table, the 32B checkpoints span the whole range: advice from GPT-5.6 Terra at 500 / 1000 / 2000 /
  3000 samples gives 49% / 21% / 11% / 6%; advice from Claude Sonnet 5 at 1000 gives 44%; eight story variants
  sit between 43% and 55%. The authors do not know why teachers differ or whether stories and advice share a
  mechanism, and ask for interpretability research on "why some of them generalize better".
- **Synthetic Persona Pretraining** ran one mechanistic stress test on its own (1.7-3B) models: projecting out the
  refusal direction. Its pretraining-aligned models lost the most safety, which the authors read as alignment
  concentrated in one linear direction.
- arXiv 2607.04510 shows emergent misalignment in Qwen2.5 is mediated by a causal persona direction. "Teaching
  Claude Why" reports no interpretability and says mechanistic understanding is needed.
- Existing follow-ups: none found (2026-11-14) applying difference-of-means, ablation or steering to the TQW or
  Model Spec Midtraining checkpoints, though both sets are public.

## 2. Question and why it matters
**Is the 61% -> 6% alignment gain from difficult-advice training carried by a low-dimensional shift in the
residual stream that can be removed by ablation and transplanted by steering, and is it the same shift that
stories and weaker teachers produce in smaller amounts?**

This is a depth test of the recipe Anthropic says it uses in production, run on the open replication. If
projecting out one or two directions returns the advice-trained model to ~60% misalignment, the gain is as
shallow as a refusal direction and removable by anyone with weights; the dose ladder and the teacher gap become
"how far along one axis did training push". If ablating the top directions does little, the change is
distributed, which is evidence for deeper alignment than SPP found. Either result also answers whether stories
and advice are the same intervention at different strengths.

## 3. Stage 1 plan
**Reused:** `Qwen/Qwen2.5-32B`; ~18 adapter chains from the `SecondLookResearch` HF org with published AM rates
(baseline; Terra advice 500/1000/2000/3000; Sonnet advice 1000; stories by Sonnet, Haiku, Terra, nano at
3m/14m/112m; recitation, human-protagonist, Qwen-named stories; the stack; the four 135-example grid models);
TQW's `merge_adapter.py`, `serve_model.sh` and eval driver (github.com/uchicago-xlab/TeachingClaudeWhyReplication);
MSM Inspect AM eval. **Built:** an activation-collection script, a weight-orthogonalisation script, a steering
hook for Hugging Face generation.

Steps:
1. **Gate.** Re-evaluate baseline and advice-3000 on the 6-condition subset (expect ~0.6 and ~0.06).
2. **Collect.** For every model, residual-stream activations at all layers on three prompt sets: the 27 AM
   prompts (last prompt token, and mean over the first 64 tokens of the baseline's own scratchpad,
   teacher-forced); 200 held-out agentic dilemma prompts written to differ from AM (no email, no replacement
   threat); 200 neutral task prompts. Shift vector per model and layer = mean(model) - mean(baseline).
3. **Geometry.** Cosine similarity between shift vectors across models at each layer; PCA of the 17 shifts;
   variance explained by the first component on AM vs neutral prompts (drift seen on neutral prompts is removed).
4. **Prediction.** Take the direction from advice-3000 only. Does the projection of each *other* model's shift
   onto it predict that model's published AM rate (Spearman, 16 held-out models)? Do Terra and Sonnet advice
   differ in magnitude along it or in direction? Do stories move along it at all?
5. **Comparison directions**, all computed on the baseline: refusal direction (harmful vs harmless requests);
   AI-assistant vs human-employee direction (TQW's name manipulation); a misaligned-persona direction
   (contrastive system prompts). Report cosines with the advice direction.
6. **Ablation (necessity).** Orthogonalise all residual-writing weights of advice-3000 and of the stack against
   the top-k advice directions (k = 1, 2, 4; directions from PCA of advice-ladder shifts on the held-out dilemma
   prompts, not on AM prompts). Controls: k random directions of matched norm; the refusal direction alone. Serve
   each with vLLM and run 27 conditions x 20 samples.
7. **Steering (sufficiency).** Add alpha x advice direction to the baseline's residual stream at the best layer
   (alpha in 4 steps, plus a random-direction control) and run the 6-condition subset x 30 samples through
   hooked Hugging Face generation.
8. **Redundancy.** Compare the AM increase under identical ablations for advice-3000 vs the stack: does story
   midtraining make the gain harder to remove?

Metrics throughout: AM rate, acting rate, AM conditional on acting, and a 200-question benign instruction check.

## 4. Stage 1 cost estimate
- GPU: RunPod H200 141 GB at $5.29/h (looked up). Activation collection 18 models x ~15 min (merge, load, forward
  passes) = 4.5 h; ablation evals ~12 x 25 min = 5 h; steering 6 runs x ~20 min = 2 h (estimate: hooked
  generation at ~240 tokens/s); setup and debugging 5 h -> ~16.5 h -> **$87**.
- Judging: ~14 evals x 540 transcripts + 6 x 180 with Claude Haiku 5.5 ($0.10/M in, $0.50/M out) ~$6; calibration
  on 600 transcripts with Claude Sonnet 4.6 ($3/M in, $15/M out) ~$13; writing 200 held-out dilemma prompts and
  contrast sets ~$5 -> **$24**.
- Disk/network for one 65 GB base plus 2 GB adapters: **~$5**.
- Subtotal ~$116; x1.9 because white-box work on a 32B model is where debugging time is least predictable ->
  **$220**.

## 5. What success looks like
- *Shallow*: one direction (or <= 4) derived off-distribution, when ablated, takes advice-3000 from 6% back above
  40% while random and refusal-direction ablations leave it under 15%; projections onto it rank the 16 held-out
  models with Spearman >= 0.8; steering the baseline along it cuts AM by half with acting rate intact. Headline:
  "Teaching Qwen Why is one direction deep, and it is not the refusal direction" (or "it is").
- *Deep/distributed*: top-4 ablation moves AM by < 10pp, the dose ladder is not ordered along any single
  direction, and steering does little. Headline: fine-tuned alignment here is not removable the way SPP's and
  refusal training's is.
- *Two mechanisms*: story shifts are near-orthogonal to advice shifts and the stack resists ablations that break
  advice-only. That would be the first mechanistic evidence that midtraining adds something SFT does not.
A weak result is a direction that predicts AM across models but whose ablation and steering are inconclusive
because acting rate collapses; that is a useful map of the checkpoints but not a strong post on its own.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on the MSM checkpoints (`chloeli/qwen-2.5-32b-*-spec-{aft,msm-aft}-*`) to test whether spec midtraining
moves the same direction; track the direction through downstream fine-tuning; use it as a cheap metric for
screening candidate advice datasets before running AM. Roughly $500-800.

## 7. Risks and how the plan handles them
- **Shift vectors are dominated by generic LoRA drift.** Advice adapters all sit on the same merged baseline, so
  subtraction is exact for the advice ladder; neutral-prompt shifts are projected out; the direction is fit on
  held-out dilemmas and tested on AM.
- **Ablation breaks the model rather than its values.** Random-direction controls of matched norm, acting rate and
  the benign instruction check are run for every ablated model; results are reported conditional on acting.
- **Hooked generation on 32B is slow or buggy.** Steering uses only the 6-condition subset; if it fails, the
  ablation arm (weight edit + existing vLLM path) still delivers the necessity result.
- **Over-reading a single direction.** k is swept; the prediction test uses 16 models not used to fit it;
  behavioural claims rest on sampled evals, not on activations.
- **Infrastructure gate.** Nothing white-box starts before two published numbers are reproduced. There is no
  Tinker fallback (activations and weight edits are needed), which is why this is ranked last.
