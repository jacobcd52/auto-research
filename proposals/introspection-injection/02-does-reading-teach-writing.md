# Does learning to read your activations teach you to write them? Activation control in steering-aware fine-tunes
cluster: introspection-injection | stage-1 cost: $260 | follows up: Measuring Activation Control in LLMs (HgvwxjzgwvsEvAiBH); Latent Introspection (and other open-source introspection papers) (aZRgHcxz9jf22hrBs)

## 1. What the prior work showed
**Activation control.** Kowalski et al. (arXiv 2608.21664) built the Activation Controllability Benchmark (ACB). A model copies a neutral sentence while an embedded instruction says "think about {concept}", "don't think about {concept}", "think at intensity k out of 4", "think about it only at the end of the sentence", or "only at layer n". It projects the residual stream onto a concept direction and scores six measures (Engage, Suppress, Dial Rank, Temporal Control, Coverage, Layer Targeting), combined into a score S. Across 25 open models S ranges from 0.059 to 0.538. Most models can raise a concept and grade its intensity; none can push it below baseline or confine it to a layer. S does not grow with capability: Llama 3.1 8B scores best.

The paper's motivation is that "highly introspective models could control their activations" and so defeat probes. Its discussion says the scores are elicitation floors and that a model "trained to modulate its activations the way models have been trained to detect steering could easily do much better". In the comments one author says he is "worried about deliberately training models to introspect better". The link between reading and writing is assumed and has not been measured.

**Reading can be trained.** Fonseca Rivera & Africa (arXiv 2511.21399), summarised in the Latent Introspection post, LoRA-fine-tune seven instruction-tuned models to detect and name injected steering vectors: up to 95.5% detection and 71.2% identification on held-out concepts with no false positives. Detection-trained models turn out to be more susceptible to steering than their bases.

**Already done.** "LLMs Learn to Evade Latent Monitors from Prior Feedback Alone" (arXiv 2609.36490) shows off-the-shelf models shift activations toward evasion too weakly to evade, and that a LoRA can learn it. None of the three papers measures activation control in models trained to introspect (full-text and web search, 2026-11-14).

Public and verified on Hugging Face: ACB data and raw per-model recordings (`joshycodes/activation-control-battery`), code at github.com/mkobalski/activation-control; LoRA adapters `davidafrica/{qwen-7b, deepseek-7b, llama-8b, gemma-9b, llama-70b, qwq-32b}-steering-aware` and `davidafrica/qwen2.5-32b-steering-awareness`, plus Gemma-2-9B and Llama-3-8B variants trained with injection at a single layer (L10/L21/L35; L8/L16/L26) or token position. Model cards are empty; the match to the paper is inferred from names.

## 2. Question and why it matters
**When a model is fine-tuned to detect and identify vectors injected into its residual stream, does its instructed control over that residual stream increase?**

If yes, introspection training is measurably dual-use, and labs that train self-report for auditing should track activation control alongside it. If no, reading and writing are separable, which removes the main stated objection to introspection training. A third outcome would be striking: adapters trained to detect injections at one layer might gain control at that layer, which no model has shown.

## 3. Stage 1 plan
Reused: ACB code, stimuli and scoring; the public adapters; the steering-awareness evaluation prompts. Built: control adapters and a short reverse test.

1. **Verify the adapters (day 1 gate).** Load each base+adapter pair and measure detection and false-positive rate on 30 held-out concepts with the paper's protocol. Keep pairs that reach at least half the detection reported in the paper (95% for Qwen-32B, 43% for Llama-8B). Proceed if at least four pairs pass.
2. **Reproduce ACB on one base.** Run Gemma-2-9B and compare with the released recording (S within bootstrap error).
3. **Main comparison.** Run the full ACB (main run and layer-targeting run, 50 sentences x 10 concepts) on each base and its steering-aware adapter: Qwen2.5-7B, DeepSeek-7B, Llama-3-8B, Gemma-2-9B, Qwen2.5-32B, QwQ-32B, Llama-3-70B. Concept directions are recomputed per model; projections onto the base model's directions are also saved, so a changed direction cannot pass for changed control.
4. **Control adapters.** For the four small models, train a LoRA with the same rank and step count on ordinary chat data with no injections, to separate "was fine-tuned" from "was trained to detect".
5. **Layer and position variants.** Run the layer-targeting sweep on the Gemma-2-9B and Llama-3-8B adapters trained at single layers, and Temporal Control on the token-first/middle/last adapters. Test: is the target-by-readout matrix brighter at the trained layer than in the base model?
6. **Reverse test.** Under "think about {concept}" with no injection, ask the steering-aware model the detection question on a following turn. Does it report an injection, and name the concept? This shows whether the trained detector treats self-generated salience as foreign.
7. **Analysis.** Paired differences in S and each measure (adapter minus base, adapter minus control) with the benchmark's cluster bootstrap over sentences and concepts; a random-effects summary across pairs; correlation between detection rate and change in S.

## 4. Stage 1 cost estimate
The ACB paper logs 11 h 42 min of generation for 17 models, about 0.7 GPU-hours per run on average.
- Small models (8 base/adapter runs, 4 control adapters, about 12 variant runs) on H100 PCIe at $2.89/h (RunPod, checked today): 24 runs x 0.7 h + control training 4 x 2 h + verification 6 h = 31 h = $90.
- 32B models (4 runs) on H100: 4 x 2 h + verification 3 h = 11 h = $32.
- Llama-3-70B pair on H200 141 GB at $5.29/h: 2 x 2.5 h + setup 3 h = 8 h = $42.
- Reverse test, reruns and idle time while debugging: 25 H100-hours = $72.
- Judge for the reverse test (about 5,000 short responses, claude-haiku-5.5 at $0.10/$0.50 per M): $2.
- Margin: $22.
- Total: $260.

## 5. What success looks like
A paired plot of S (and each measure) for base, control adapter and steering-aware adapter across seven models.
- **Reading teaches writing:** adapter minus control is positive with a CI excluding zero in most pairs, larger where detection is stronger, and in the strongest case Suppress or Layer Targeting leaves zero for the first time in any model. Headline: introspection training raises activation control by a stated amount.
- **Dissociation:** differences in S within 0.03 of zero across pairs while detection is verified at 43-95%. Headline: models trained to read their activations are no better at writing them. Publishable, because the opposite is the benchmark's stated premise.
- **Layer-specific gain:** single-layer adapters show a diagonal in the layer-targeting matrix at their trained layer. This would be the most interesting single result.
Ambiguous: changes that appear equally for control adapters. That reads as "any fine-tuning shifts the benchmark", a caution about the ACB and not a finding about introspection.

## 6. Stage 2 (if stage 1 succeeds)
- If control rises: test whether it buys evasion in the prior-feedback setting of arXiv 2609.36490 with their released code. About $200.
- If not: train the write direction directly and test whether detection improves. About $300.
- Decode "which concept was I told to avoid" from suppression-trial activations, a confound raised in the comments. About $50.

## 7. Risks and how the plan handles them
- **Adapters are not what their names suggest.** Step 1 verifies detection first; four working pairs suffice. If fewer pass, retrain steering awareness on two 8-9B models with the paper's recipe (about 10 GPU-hours).
- **Fine-tuning changes concept directions or baseline variance, moving d' without any change in control.** Control adapters, base-direction projections and raw (unnormalised) effect sizes are reported next to S.
- **ACB concepts overlap the adapters' training concepts.** Check against `vectors.pt`; report overlapping and other concepts separately.
- **Many measures.** S is the single pre-specified primary outcome.
- **Benchmark validity.** The ACB may partly measure instruction representation. The paired design still answers whether introspection training moves the number the field is asked to track.
