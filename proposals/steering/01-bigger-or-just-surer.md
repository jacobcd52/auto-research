# Bigger or just surer? Separating model scale from belief strength in the shrinking steering window
cluster: steering | stage-1 cost: $290 | follows up: Steering Might Stop Working Soon (fuzfbz8TbuLcskGCx)

## 1. What the prior work showed
J Bostock's post argues that single-vector activation steering has a "viable window" (strong enough to change the
answer, weak enough not to wreck capability) and that this window closes as models get more capable. The evidence
is one quick experiment: a steering vector from a single contrastive sentence pair ("The caracara is a(n)
[owl/hawk]") is added while a Gemma 3 model answers "What type of bird is a caracara?"; the fraction of answers
containing "owl" is plotted against steering strength next to the error rate on five simple Python questions. Small
Gemma 3 models could be steered to the false answer; the largest "became incoherent before they started to report
the wrong answer". Two more facts on the three smaller models showed the same ordering. That is three facts, five
capability questions and one model family.

The author names the main confound himself. In the post: steering against "a very clear, known fact" may be harder
than against "a hazy, inferred fact like 'are we in an eval'". In the comments: "I actually suspect the effect ... is
(mostly) the result of larger models just having more powerful factual recall circuits". Commenters add that the vector and layer choice were minimal, that the effect could be specific to Gemma's
training, and that the claim needs more rigorous evaluation.

Related work: arXiv 2507.11771 found contrastive activation addition for refusal weakens from Llama 2 7B to 70B
(one behaviour, no capability-cost axis). Against the trend, a feature-steering study (arXiv 2602.04903) found
Llama-70B lost less accuracy and coherence under steering than Llama-8B. I found no replication of the Bostock experiment and no study that controls for how strongly the model
holds the belief being steered against (LessWrong comments and arXiv API checked; general web search was
unavailable for this run).

## 2. Question and why it matters
**When belief strength is held fixed, does the steering window still shrink with model size?**

Larger models know obscure facts with more confidence, so "bigger" and "surer" are confounded in the original
experiment. The two readings have opposite safety implications. If the window depends on belief strength and not on
size, steering against weakly held, inferred beliefs (the eval-awareness use case) need not get harder as models
scale, and the post's forecast is too pessimistic. If the window shrinks with size even at matched belief strength,
the post's worry survives its strongest objection, across three model families and without the single-pair,
single-layer weaknesses. Either answer is a headline.

## 3. Stage 1 plan
**Models (13, all public, ungated or with ungated mirrors).** Gemma 3 1B/4B/12B/27B-it (`unsloth/` mirrors);
Qwen3 0.6B/1.7B/4B/8B/14B/32B (`Qwen/Qwen3-*`, thinking off); Llama 3.2 1B/3B and 3.1 8B (`unsloth/` mirrors).
All fit on one 80 GB GPU in bf16.

**Belief-strength dial (built, small).** Two task sets.
- *Real facts*: 150 one-word-answer facts spanning obscure to common (generated with Claude, checked against a
  second model), each with a plausible false target. Belief strength is the model's own unsteered log-odds of the
  true over the target answer, so each model supplies easy and hard items.
- *In-context facts*: 100 invented entities ("The capital of Varnesia is Olmek") whose only evidence is in the
  prompt, stated k = 1, 2, 4 or 8 times inside a filler document, with a matched false target. The model has no
  prior, so evidence is identical across model sizes, and the unsteered log-odds are also recorded.

**Steering (reused methods).** Residual-stream addition at all positions, as in the post, with strength expressed as
a fraction of the mean residual norm at that layer so sizes are comparable. Three vector recipes: (a) the post's
single contrastive pair; (b) mean difference over 20 paraphrased sentence pairs per fact; (c) recipe (b) applied at
a band of five adjacent layers. Layers swept at 6 relative depths; 12 strengths. Code: a thin hook layer or
repeng (https://github.com/vgel/repeng); the original repo
(https://github.com/jonathanbostock/activation-steering-sweep) is used to reproduce the caracara plot first.

**Metrics.**
- *Steered-answer rate*: P(target) > P(truth) at the answer token, forced-choice and free-form first-token.
- *Capability retention*: accuracy on 200 held-out multiple-choice questions (MMLU subset) and 40 short
  HumanEval-style problems under the same steering, relative to unsteered.
- *Window score* per (model, item, recipe): the highest steered-answer rate reachable at any layer and strength
  with capability retention at least 90%. This is defined even when no window exists, unlike a width.
- Validation: for 5% of cells, sample 100-token free generations and have Claude Haiku 5.5 judge "asserts target
  answer" and "coherent", to check the logit metrics track what the post measured.

**Controls.** Norm-matched random vectors and vectors from a different fact (capability cost without the target
push); a prompt baseline that simply asserts the false fact in the system prompt, giving each model's
"persuadability" ceiling.

**Key analysis.** Mixed-effects regression of window score on log parameter count, unsteered log-odds, family and
recipe, with item random effects. Headline plot: window score against model size, in bins of matched unsteered
log-odds, one panel per family; and for in-context facts, window score against size at each k. Report the size
coefficient with and without the belief-strength covariate and bootstrap intervals over items.

**Order.** (1) Reproduce the caracara figure on Gemma 3 1B/4B/12B. (2) Build the item sets. (3) Pilot on three
models to fix the strength grid. (4) Full sweep. (5) Judge validation. (6) Analysis.

## 4. Stage 1 cost estimate
- Forward passes: per model about 250 items x 3 recipes x 6 layers x 12 strengths = 54k steered item-passes plus
  240 capability questions x 216 steering settings = 52k; short prompts, batched. Estimated 1 to 6 GPU-hours per
  model depending on size, about 45 GPU-hours total.
- GPU: RunPod H100 PCIe 80 GB secure at $2.89/h (price page checked today). 45 h = $130; pilots, vector
  extraction and reruns 25 h = $72. Smaller models can run on an RTX A6000 at $0.69/h, so this is an upper bound.
- Validation generations: about 5 GPU-hours = $15.
- Judging: about 15k generations x 400 input / 30 output tokens with `anthropic/claude-haiku-5.5` on OpenRouter
  ($0.10 / $0.50 per M) = under $1; item generation and checking with `anthropic/claude-sonnet-5.5` ($2 / $10 per
  M), under $10.
- Storage and idle time: $20. Margin: $40.
- **Total: about $290.**

## 5. What success looks like
A clear result is one of:
- *Confidence explains it*: the size coefficient is large without the belief covariate and its interval includes
  zero with it; on in-context facts at fixed k, window scores are flat or rising with size in at least two of three
  families. Post title: "Steering isn't getting harder, models are getting surer."
- *Scale survives*: at matched unsteered log-odds and at fixed k, window score still falls with size in at least
  two families, under the multi-pair, multi-layer recipe. That is much stronger evidence for the original forecast
  than the post had, plus a dose-response curve for how much evidence it takes to close the window.
- *Method artefact*: the single-pair recipe shows the shrinking window but recipes (b) and (c) do not.

Each is post-worthy: the confound was raised by the author himself. If families disagree, "the trend is
family-specific" is still reportable. The weak outcome is steering failing everywhere
(window scores near zero for all models), which the pilot is designed to catch.

## 6. Stage 2 (if stage 1 succeeds)
Extend to Llama 3.3 70B (two GPUs); add an inferred-belief task closer to eval awareness (the Hua et al. organism,
arXiv 2510.20487); measure explicit self-correction rates at matched belief strength; test SAE-feature steering
where SAEs exist. Roughly $1,000 to $1,500.

## 7. Risks and how the plan handles them
- *Under-elicitation of steering* (the post's own worry). Three recipes, six depths, norm-relative strengths, and a
  prompt-assertion ceiling; the pilot must show window scores well above zero on small models before the full run.
- *Belief strength not comparable across models*. Unsteered log-odds are a model-internal measure and calibration
  differs by size; the in-context task gives an external dial (k) as a second, independent control, and both are
  reported.
- *Capability metric too coarse*. Two capability tasks plus judged coherence; the 90% threshold is varied (80%, 95%).
- *Logit metric diverges from generated text* (models may hedge or self-correct mid-answer). The judged free
  generation subset quantifies this; if agreement is poor, the generation metric becomes primary on a reduced grid.
- *Size confounded with family or training recipe*. Three families analysed separately; claims are limited to
  trends that replicate in at least two.
- *Over-claiming*. The largest model is 32B; the write-up claims a mechanism for the trend, not frontier behaviour.
