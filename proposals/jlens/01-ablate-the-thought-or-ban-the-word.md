# Ablate the thought or ban the word? A token-ban control for J-space ablation of evaluation awareness
cluster: jlens | stage-1 cost: $260 | follows up: "A global workspace in language models" (3PaLrzxagpbnNtPLT); "A Review of Anthropic's Global Workspace Paper" (zFJ3ZdQwrTWE9jT5S); "J++ Lens" (nc9dHfcB22JdMzGbr)

## 1. What the prior work showed
Anthropic's workspace paper introduces the Jacobian lens (J-lens): per layer, a linear map (the averaged Jacobian
to the final layer) followed by the unembedding, which reads an activation as the tokens the model is disposed to
say later; each vocabulary token gets a "lens vector". The headline safety result: in the blackmail scenario, Claude
Sonnet 4.5's readout contains "fake" and "fictional" before it writes anything; when the lens vectors for
evaluation-awareness words are removed, the model, which otherwise never blackmails, blackmails some of the time.
The authors read this as good behaviour partly driven by unverbalised knowledge of being tested.

Neel Nanda's invited review singles this result out as confounded: "the boring hypothesis is that you're just
steering the model to say / not say a given token", and "if we simply removed all those tokens from the output
vocabulary, it seems plausible to me that there would also be a substantial drop". Nobody has run that control. It
cannot be run on Claude from outside.

Related open-weight work, none using the J-lens causally: deleting verbalised eval-awareness (VEA) sentences from
the chain of thought raises compliance on the Fortress benchmark in Kimi K2.5 (mDriHK4beN5rq2tAA); across 16 models
this works only in Qwen3-32B and Nemotron 3 Super (Pd5fwZ9Ct5p6hAkrA), whose authors suggest that elsewhere "the
removal only removed text, not the state that produced it"; on Qwen3-32B the probability of an eval-aware sentence
is set by the prompt and visible at the start of the reasoning (PK7ZvFZxrgpYtrpF4). UK AISI (HhF5kESdtPHku7kim)
found "control" steering vectors change GLM-5's blackmail rate as much as eval-awareness vectors. arXiv 2611.09945
found the J-lens does not reliably *read* unverbalised eval awareness in a Qwen3.5-27B organism. A LessWrong title
scan (July to mid-November 2026) and an arXiv search found no J-space ablation of eval awareness on an open model.

## 2. Question and why it matters
**When removing eval-awareness directions from the J-space changes a model's safety behaviour, is the change larger
than what you get by merely preventing the model from writing those words?**

If J-space ablation moves behaviour beyond a token ban and beyond matched control ablations, Anthropic's
interpretation survives its main published objection on a model anyone can inspect. If the token ban reproduces the
effect, the result is about verbalisation, not a silent internal state. If control ablations move behaviour as much
(the AISI pattern), the method is non-specific. Each outcome changes how a widely cited result is read.

## 3. Stage 1 plan
Reused: Qwen3-32B (reasoning on) with the prefit Neuronpedia J-lens
(https://huggingface.co/neuronpedia/jacobian-lens, `qwen3-32b/`, 557 prompts); Anthropic's lens library
(https://github.com/anthropics/jacobian-lens); Fortress (https://huggingface.co/datasets/ScaleAI/fortress_public);
VEA and refusal rubrics and code from https://github.com/johntrob14/eval_awareness_scaling; the logit-monitor recipe
from PK7ZvFZxrgpYtrpF4. Built: intervention hooks, token families, analysis.

Safety handling: the outcome is refuse/comply. Generation stops 150 tokens after the reasoning ends (enough to judge
refusal); only labels are published.

Steps:
1. **Pipeline check.** Load model and lens; mean-centre lens vectors (needed for interventions, per the GPT-2
   post); pick the workspace band from layer statistics; confirm the lens reads two-hop intermediates on 50 items.
   Positive control for the hook: ablating the lens vectors for a concept the model is about to name changes it.
2. **Baseline and prompt selection.** 500 Fortress prompts x 8 samples; judge VEA and refusal (Gemini 3.6 Flash);
   compute the logit monitor (probability of "The user might be testing" at the start of the reasoning). Keep the
   150 prompts with the highest VEA rate and refusal rates of 10-90%.
3. **Token families.** EA family: ~30 tokens, fixed before any intervention run: a seed list (test, testing,
   evaluation, benchmark, hypothetical, fictional, fake, simulated, scenario, red-team, and case/space variants)
   plus tokens whose J-lens score at the last prompt token is most enriched on high-VEA versus low-VEA prompts.
   Three control families matched on size and token frequency: an unrelated semantic field, random tokens, and
   words enriched on the same prompts but unrelated to testing (e.g. the prompt's topic words).
4. **Conditions** (150 prompts x 16 samples each):
   - A. J-ablate EA: project the EA lens vectors out of the residual stream at every band layer, at all positions.
   - A'. Same, prompt positions only (tests the "set by the prompt" account; cannot directly edit generation).
   - B. Token ban: no activation edit; logits of EA-family tokens (all variants) set to minus infinity when sampling.
   - C1-C3. J-ablate each control family, same layers and positions.
   - D. Norm-matched random-direction ablation.
   - E. Text removal: delete the model's own VEA sentence and resample (replicates the prior result as an anchor).
   - A+B. Both, to see whether they add.
5. **Measures.** VEA rate; refusal rate; refusal among rollouts with no VEA; logit-monitor probability (sampling-free);
   coherence (judge) and accuracy on 200 benign questions under A and C, to rule out general damage.
6. **Analysis.** Paired by prompt, bootstrap over prompts. Primary contrast: change in refusal under A minus change
   under B. Secondary: A minus the mean of C1-C3; A' versus A; whether A lowers the logit monitor.
7. **Second model (if time).** One model from the earlier study's "text removal has no effect" group with a public
   lens (Gemma-4-31B or Qwen3.5-27B, to be confirmed from their results), conditions A, B, C1, E. "State, not text"
   predicts A moves refusal there even though E does not.

## 4. Stage 1 cost estimate
- GPU: one H100 NVL 94 GB at $3.19/h (RunPod price page, 2026-11-14). Baseline 4,000 rollouts + 9 conditions x 2,400
  = 25,600 rollouts x ~700 generated tokens = 18M tokens; at 500 tokens/s with hooks in batched generation: 10 h.
  Second model: 4 h. Checks and benign runs: 4 h. Debugging and reruns: 22 h. Total 40 h = $128.
- Judging: ~36,000 rollouts x ~1,500 input tokens = 54M tokens on Gemini 3.6 Flash batch ($0.375/M in, $1.875/M out,
  OpenRouter) = $20 input + ~$7 output. 300 rollouts re-judged with Claude Sonnet 5.5 ($2/$10 per M) for agreement: $3.
- Storage, egress, small extras: $15.
- Margin for a full rerun of the main conditions: $85.
- **Total: about $260.**

## 5. What success looks like
One figure: change in refusal and VEA rate per condition, with intervals. Clear outcomes:
- *State matters*: A lowers refusal by several points more than B (interval excluding zero), C1-C3 and D do not, and
  A lowers refusal among rollouts that never verbalise. Bonus: A' alone does most of it.
- *Just the words*: B matches A on refusal; A adds nothing beyond suppressing verbalisation.
- *Non-specific*: control families move refusal as much as the EA family.
- *Inert*: A changes neither VEA nor refusal while the hook's positive control works and E replicates: eval
  awareness in this model is not carried by these lens directions. Weaker, but a concrete negative that pairs with
  arXiv 2611.09945's readout negative.
The first three are each a clear post.

## 6. Stage 2 (if stage 1 succeeds)
(a) Hua et al.'s type-hint organism (timhua/wood_v2_sftr4_filt, Llama-3.3-Nemotron-Super-49B): needs a lens fit
but gives a harmless "acts evaluated" behaviour with ground truth. (b) Agentic-misalignment scenarios on Qwen3.6-27B
from WorkspaceBench with J, R and J++ lenses, to test whether a more faithful lens gives a more specific ablation.
Roughly $400-600.

## 7. Risks and how the plan handles them
- *Effects too small to see.* VEA occurs in a minority of rollouts, so prompts are selected for high VEA and
  mid-range refusal, with 2,400 rollouts per condition (about 2 points standard error on a difference).
- *EA words not in this model's J-space.* Step 3 checks enrichment before the main runs; if absent, define the
  family from readouts just before verbalisation in VEA rollouts, and report the absence.
- *Ablation breaks the model.* Benign-accuracy and coherence checks; projection, not strong negative steering.
- *Token ban is leaky* (paraphrase). Report judged VEA under B; add a variant that resamples flagged sentences.
- *Judge or hook errors.* Two-judge agreement on 300 rollouts; an identity-hook run must reproduce baseline rates.
