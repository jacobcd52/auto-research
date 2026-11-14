# Does driving NLA reconstruction error down surface reasoning, or only a better copy of the prompt?
cluster: nla | stage-1 cost: $380 | follows up: Can activation verbalizers surface an internal chain of thought? (QQQAcKuWK6k98FivY); Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations (oeYesesaxjzMAktCM); NLA explanations can be shortened without harming reconstruction (NazprRfWJ4qkwcSro)

## 1. What the prior work showed
A natural language autoencoder (NLA) is a pair of fine-tuned copies of a target model: an activation verbalizer (AV) turns one residual-stream activation into a paragraph of text, and an activation reconstructor (AR) turns that text back into an activation. They are warm-started on Claude-written guesses and then trained by RL so that the round trip reconstructs the activation (Fraser-Taliente et al. 2026).

Hu and Greenblatt asked whether an AV can show the reasoning a model does inside one forward pass. They ran Qwen2.5-7B, Gemma-3-27B and Llama-3.3-70B on ~900 easy competition-math problems with no chain of thought and verbalized the last position before the answer. Results: on the 123 easiest problems, 16% of Gemma verbalizations before correct answers looked at all like a chain of thought; wrong outputs were singled out in 0/78 cases. Two diagnostics make this hard to interpret. First, across variants of one problem that differ only in a constant, every NLA reconstructed the activation direction worse than a constant vector (the variant mean). Second, ten Sonnet confabulations written from the problem statement alone matched the real verbalization's reconstruction loss, so "the AV recovers the problem and makes up the rest" could not be excluded. Linear probes could not predict Gemma's answer at the NLA layer. The authors conjecture that these failures "might be improved by just making the reconstruction loss go down".

Follow-ups found: RL-specialising an NLA on activation differences improves Taboo secret-word recovery (arXiv 2610.30934); length penalties, Matryoshka truncation and Flow-NLA (2609.33702) change the objective; two papers argue reconstruction rewards identification, not explanation (2610.18727, 2607.20379). I found nobody who lowered reconstruction error on a reasoning distribution and measured what the extra bits are spent on.

## 2. Question and why it matters
If we continue NLA training on activations from no-CoT arithmetic until the NLA beats the constant-vector baseline within problem variants, what does the verbalizer start saying: the prompt's constants, the hidden intermediate values, or the model's (possibly wrong) answer?

If intermediates and wrong answers appear, the earlier post's pessimism was about weak checkpoints, and cheap domain specialisation is a route to reading single-pass reasoning. If reconstruction improves only through better restatement of the prompt, reconstruction pressure buys prompt inversion and the "just lower the loss" hope fails in the cleanest setting available.

## 3. Stage 1 plan
Reused: Qwen3-8B (thinking off) and its public layer-24 NLA (`syvb/nanonla-qwen3-8b-L24-av`, `-ar`, RL adapter `p0.0`; cross-check with `marco-bazzani/Qwen3-8B-nla`); EasyNLA training code (github.com/asherps/EasyNLA, built for this model, supports continuing RL from an adapter with a KL reference); generic RL data `asher577/easynla-warmstart-data`; the competition-math set (github.com/rgreenblatt/no_cot_math_public) and the earlier post's 10-shot, no-CoT prompt format. Built: a templated arithmetic set and the analysis scripts.

1. **Task set.** 75 word-problem templates with one or two hidden intermediate values, constants sampled by code, answers and intermediates computed by code. 60 templates x 400 settings for training; 15 held-out templates x 100 settings plus 100 held-out settings of each training template for testing. Run Qwen3-8B no-CoT, store its greedy answer and the layer-24 activation at the last position.
2. **Phase-0 gate (half a day).** Linear probes at layers 16-34 for each constant, each intermediate and the model's answer. If intermediates are not decodable at layer 24 but are at a nearby layer L*, adapt the NLA to L* (re-extract warm-start activations, short SFT, then proceed); if they are decodable nowhere, restrict to templates where they are and report that.
3. **Baseline.** With the unmodified NLA: within-template FVU against the template-mean direction (the earlier post's "rock" test), and the specificity metric below.
4. **Training runs** (batch 64 prompts x 8 samples, about 400 steps, KL 0.01, AR co-trained, checkpoints every 50 steps): (A) half math activations, half generic; (B) generic only, same steps, to control for "more RL"; (C) a second seed of A.
5. **Specificity metric (no grader).** For each content class c in {prompt constants, intermediates, model answer, correct answer when the model is wrong}: S_c = P(value appears in the item's own verbalization) minus P(it appears in the verbalization of a different setting of the same template). The earlier post found regex matching agrees with Opus graders above 98%; template priors and number-spraying cancel in the subtraction. Report S_c against within-template FVU at every checkpoint, on held-out settings and held-out templates.
6. **Read or recompute?** Three checks on the best checkpoint. (i) Errors: when the model's answer is wrong, is the model's answer or the correct one mentioned more specifically? (ii) Probe split: is the intermediate mentioned more often on items where the probe decodes it from that activation than where it does not, at matched constants? (iii) Intervention: add the mean activation difference between two intermediate values (averaged over many constant combinations, so the constants are not shifted) and check that the model's answer moves; then see whether the verbalized intermediate follows the edit while the verbalized constants stay.
7. **Transfer.** Run baseline and best checkpoint on the ~900 real competition problems: regex Output/Answer mention rates, FVU, and Sonnet 5.5 grading (k=3, the post's rubric text) of Method and Values on the 123 easiest. Repeat the earlier post's best-of-10 Sonnet confabulation test on 500 items before and after training.

## 4. Stage 1 cost estimate
Prices checked 2026-11-14 (RunPod A100 80 GB $2.09/h; OpenRouter Sonnet 5.5 $2/$10 per M tokens).
- Activations, probes, verbalizing checkpoints, interventions: 25 A100-hours = $52.
- Three RL runs. A public 9B run reports 145 s/step at batch 256 x 8 on 4x A100; at batch 64 that is about 36 s/step, so 400 steps = 4 h x 4 GPUs = 16 GPU-hours = $33 each, $100 total.
- Setup and debugging of the training stack: 20 A100-hours = $42.
- Sonnet confabulations: 5,000 calls x (3k in + 0.2k out) = $40. Grading: ~2,700 calls x (2.5k in + 0.4k out) = $25.
- Storage and transfer: $15.
Subtotal $274; with a 40% margin for reruns, $380.

## 5. What success looks like
The main figure plots S_constants, S_intermediate and S_answer against within-template FVU across checkpoints for runs A-C. Clear positive: FVU falls below 1 and S_intermediate rises well above the generic-RL control on held-out templates, with at least two of the three read-vs-recompute checks pointing to reading (wrong answers tracked, probe split positive, edits followed). Clear negative: FVU falls below 1 while only S_constants rises, or S_intermediate rises but the verbalization names the correct intermediate when the model is wrong and ignores the intervention. A third publishable outcome: FVU cannot be pushed below 1 in 400 steps even in-domain, which quantifies how far current NLAs are from reasoning-scale resolution. Ambiguous: S values move by a few points with overlapping bootstrap intervals; the probe map and baseline specificity table would still be reported.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on Gemma-3-27B with the official layer-41 NLA and rerun the full graded competition-math eval. About $1,500-2,500, mostly 27B RL.

## 7. Risks and how the plan handles them
- **The intermediate is not represented at the NLA layer.** The phase-0 probe map decides the layer before any training; the gate result is itself reportable.
- **RL stack fragility.** EasyNLA targets exactly this model and layer; run its smoke test first, and reproduce held-out generic FVE (about 0.59 for `p0.0`) before any in-domain step. Log the KL term (the initialisation post found it silently disabled in the official code).
- **Collapse into template memorisation.** Held-out templates, the generic half of each batch, and the within-template subtraction in S_c.
- **Templates too easy or hard.** Tune difficulty in step 1 for 50-85% no-CoT accuracy, so both correct and wrong answers exist.
- **Regex errors.** Digit-boundary matching plus a 200-item audit.
- **Over-claiming.** One 8B model, synthetic arithmetic; step 7 states what carries to real problems.
