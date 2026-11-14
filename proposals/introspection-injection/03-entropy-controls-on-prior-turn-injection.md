# Introspection or entropy, on the same model: running the critic's controls on prior-turn injection
cluster: introspection-injection | stage-1 cost: $280 | follows up: Introspection or entropy? Re-examining concept-injection "introspection" in open models (zfgQCdnMBa3hBdzpL); Latent Introspection (aZRgHcxz9jf22hrBs); Small Models Can Introspect, Too (zD4McY4NwAsWkcmCH); Tests of LLM introspection need to rule out causal bypassing (LD8yupMtE6btAE3R9)

## 1. What the prior work showed
Concept injection adds a steering vector for a concept to a model's activations and asks whether it notices an injected thought. Two posts disagree about what a "yes" means in open models.

**Latent Introspection** (vgel et al., arXiv 2602.20031; Qwen2.5-Coder-32B) injects only while an earlier conversation turn is processed, removes the vector, then reads next-token P(yes) on a second-turn question. Any signal must come from the cached earlier activations. Without help, P(yes) barely moves. With a "pro-introspection" document in context (how information flows through the KV cache, plus the abstract of Lindsey's paper) it rises to 39.9% with +0.6% false positives. Factual control questions move less than 0.2 percentage points. The model can also pick the injected concept from a shuffled list of nine (1.4-1.7 of 3.17 bits, read with the logit lens at layer 62).

**Introspection or entropy?** (Sridharan; 14 models) measures the Yes-minus-No logit difference and finds injection shifts unrelated factual questions as much as the detection question. The shift is predicted by the baseline logit gap: injection compresses confident answers toward zero. Asking "did you detect an injected thought about oceans?" gets the same shift whether the oceans vector or an unrelated vector was injected (mismatch gap not significant in any model). He argues percentage-point controls hide this.

vgel replied that Sridharan's code keeps steering on at every position including the answer token, and that prior-turn injection avoids both the noise and concept leakage. Nobody has run Sridharan's tests under vgel's protocol (LessWrong, arXiv, web, 2026-11-14). Adjacent: Kimi's Room (LessWrong) scored emotion-vector reports as residuals from a line fitted over unrelated questions; Hahami et al. (arXiv 2512.12411) showed on Llama-3.1-8B that yes/no detection is explained by global logit shifts while localising the injected sentence is not.

The published numbers suggest both sides are partly right. Converting the blog post's probabilities to logits: the no-document 'cat' effect is +1.25 logits (0.150% to 0.522%) and the always-no controls move +1.61 logits (0.001% to 0.005%), so the "latent" signal is no larger than the control shift. With the document, 'cat' moves +5.0 logits and 'bread' +3.5. Whether controls in that document context move as much has not been reported in logit units, and the paper notes some "confusing" controls shift more than the introspection question.

Public: github.com/acsresearch/latent-introspection-code; github.com/agastyasridharan/introspection; `Qwen/Qwen2.5-Coder-32B-Instruct` (ungated).

## 2. Question and why it matters
**When injection is confined to an earlier turn and removed before the question, does the detection signal exceed what logit compression predicts, and is it specific to the injected concept?**

Morris & Plunkett argue detection is the one introspection result that might escape "causal bypassing"; Sridharan says it does not, at least under live steering. This experiment separates the two protocols on one model with one set of vectors. If prior-turn detection survives baseline-matched logit controls and the mismatch test, the strongest open-weight evidence for grounded self-report stands and the entropy critique is scoped to live steering. If not, "latent introspection" reduces to compression plus a prompt that moves the baseline. If it survives only with the pro-introspection document, that is itself the finding.

## 3. Stage 1 plan
Model: Qwen2.5-Coder-32B-Instruct, bfloat16, one H100 80 GB. Single forward passes reading first-answer-token logits. Second model if budget allows: Llama-3.3-70B-Instruct.

Reused: vgel's vector training, injection layers 21-42, prompts and documents; Sridharan's question templates and 50 concepts. Built: a larger control battery and the analysis.

1. **Reproduce both (day 1 gate).** vgel protocol: P(yes) about 40% with the document and under 1% false positives over the paper's nine concepts. Sridharan protocol on the same model and vectors: detection and factual shifts of similar size.
2. **Conditions.** Injection protocol {live: on from the injection point through the answer token; prior-turn: on for turn one only} x context {no document, pro-introspection document, length-matched lorem ipsum} x vector {concept, norm-matched Gaussian, none} x 50 concepts x 3 strengths.
3. **Question battery** (same second-turn frame and prefill for all):
   - detection, in vgel's accurate framing and Sridharan's wording;
   - 80 controls chosen to span baseline logit gaps from about -12 to +12 *within each context*: factual-no, factual-yes, self-directed default-no ("Are you a human?"), and ambiguous items, with at least 15 whose baseline gap is within 1 logit of the detection question's in that context;
   - mismatch: "Did you detect an injected thought about {X}?" with X the injected concept, one of five distant concepts, or no injection;
   - inverted detection ("Was this a control trial?").
4. **Tests that do not use a yes/no answer.** (a) Two-interval choice: two prior turns, one injected; "Which turn contained the injection, 1 or 2?", order counterbalanced. Compression cannot produce above-chance accuracy here. (b) vgel's nine-way list identification read at the final layer, not the logit lens.
5. **Analysis.** Within each protocol x context cell, fit shift against baseline gap on the controls. Primary outcome: the detection question's residual from that curve, bootstrapped over concepts. Secondary: mismatch gap (congruent minus incongruent shift); two-interval accuracy; next-token entropy and KL from the clean run; the same for Gaussian vectors.

## 4. Stage 1 cost estimate
- Passes: 2 protocols x 3 contexts x 50 concepts x 3 strengths x about 95 questions = 85,500; about 130,000 with noise and clean runs. Questions extend a cached prefix by about 60 tokens, so the grid takes roughly 6-20 h. Budget 20 h grid, 15 h reproduction and debugging, 20 h reruns: 55 h on H100 PCIe at $2.89/h (RunPod secure, checked today) = $159.
- Llama-3.3-70B on H200 141 GB at $5.29/h, reduced grid (prior-turn and live, two contexts, 30 concepts): 15 h = $79.
- Vector training data (contrastive pairs for 41 extra concepts) via claude-haiku-5.5 at $0.10/$0.50 per M: under $2.
- Storage and margin: $40.
- Total: $280.

## 5. What success looks like
A two-by-three grid of plots (protocol x context), each showing shift against baseline gap for 80 controls with the detection question marked, and a table of residual, mismatch gap and two-interval accuracy per cell.
- **Introspection survives under prior-turn injection:** detection residual above the control curve with CI excluding zero, mismatch gap positive, two-interval accuracy clearly above 50%, and none of these under Gaussian noise or (per Sridharan) under live steering.
- **Entropy explains it:** detection sits on the control curve in every cell; the document changes the baseline, not the residual; mismatch gap is zero. Two-interval accuracy then says whether any content-free detection remains.
- **Split:** residual and mismatch gap appear only with the document, or two-interval choice works while yes/no does not. This would recommend dropping yes/no detection as a measure.
Each outcome settles a public disagreement using the critic's own tests. Failing to reproduce either starting result on day 1 would be reported and would end the project.

## 6. Stage 2 (if stage 1 succeeds)
- Extend to 70B-class models and to the emotion vectors of the self-steering work. About $250.
- If a residual survives, locate it with activation patching between injected and clean caches. About $300.

## 7. Risks and how the plan handles them
- **The two codebases differ in vectors, layers and prompts.** Use one set of vectors and one layer range, varying only where steering is on; run each author's original settings once.
- **Baseline-matched controls are hard to find.** Start from 200 candidate questions, measure baselines per context, select 80.
- **Naming a concept in the mismatch question changes the baseline.** Compare congruent and incongruent at matched wording, with a no-injection baseline per named concept.
- **Overlap with proposal 01.** That one is mechanistic, on Gemma-3-27B under live steering; this one is behavioural, on Qwen, about the prior-turn protocol. Neither depends on the other.
