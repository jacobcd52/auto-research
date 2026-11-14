# Feedback: "Why do question repeats help only a looped transformer? A causal study in Dory 4B"

Reviewed 2026-11-14. Verdict: **major overhaul** (keep the question, change the plan). The question is real and not yet done, but the plan rests on an implementation that I could not find, one architectural claim that is wrong, a hypothesis pair that is not well separated, and a prior effect whose size on probe-able tasks is unknown.

## What I checked

| Claim in proposal | Status |
|---|---|
| Westover et al. Appendix A: dots never help Dory; repeats help only at 2+ loops, hurt slightly at 1 loop, uplift grows with loops | Confirmed in the post text (uxsDuWWHNTpKrsF6P). The text gives **no numbers**; the effect is shown only in a figure, on aggregate NCRI. The one number in the body is NCRI 49 for normal-Dory at 2 loops with 5x repeats (60 for recurrent mode). |
| Dory weights public and ungated; config options `n_recurrent_loops`, `recurrent_kv_cache_mode` | Confirmed (HF API: `gated: false`; config.json has both keys, default 2 loops, `per_loop`). |
| Architecture 8 input / 20 recurrent / 8 output layers | Confirmed (config counts attention and MLP separately: 16/40/16). |
| "hooks on the Hugging Face implementation" | **Not confirmed, probably wrong.** See below. |
| "sliding-window layers cannot see earlier copies anyway" | **Wrong for this plan's prompts.** `sliding_window` is 1024 tokens. |
| NCRI generators at github.com/neelnanda-io/nocot-bench | Repo exists (README and FILLER.md fetched via raw.githubusercontent.com); it has a `qrep@N` filler mode and sweep code. I did not inspect the task generators themselves. |
| github.com/rgreenblatt/multi_hop | Exists (default branch is `master`). Contents not inspected. |
| Lambda A6000 $1.09/h, RunPod A100 $2.09/h | Not re-verified (my pricing-page fetch failed); taken from NOTES.md. Not material to the verdict. |
| "Not done: any white-box analysis of what repeats do" | True as far as I can find, for Dory and for repeats. But related work exists and is uncited (below). |

### The Hugging Face implementation may not exist
- The model repo contains weights, tokenizer, config and README only. There is no `modeling_*.py` and no `auto_map`, so `trust_remote_code` does not help.
- `transformers` 5.23.0 (latest on PyPI today) contains no file with "dory" in its name. `src/transformers/models/dory/` returns 404 on the `main` branch, and `configuration_auto.py` on `main` has no "dory" entry.
- The model card documents two ways to run it: an unmerged vLLM PR (#60149) and a llama.cpp PR/fork. It gives no `transformers` snippet despite `library_name: transformers`.
- Westover et al. did SFT and RL on Dory, so a trainable PyTorch implementation exists somewhere, but their post links no code repository. I could not check GitHub PRs (github.com is blocked here), so an unmerged transformers PR may exist.

Consequence: the first task is likely "obtain or write a hookable PyTorch forward pass for a normalized-GPT with loop re-injection, hybrid sliding/full attention and two RoPE configs, and prove it matches the vLLM PR logit-for-logit". That is the kind of fragile dependency the programme warns about, and the proposal budgets zero time for it.

### The sliding-window claim
Section 7 says sliding-window layers cannot see earlier copies, which "narrows the search to full-attention layers". The window is 1024 tokens. A lookup-chain question is roughly 100 to 300 tokens, so with r = 2 or 3 the earlier copies sit inside the window for most or all sliding layers. Only one attention layer in four is full-attention (5 of 20 in the recurrent block). Knock-outs must cover all attention layers, and the "narrowing" does not apply. Conversely, at r = 5 with long questions the first copies do fall outside the window, so repeat count and layer type interact in a way the plan does not account for.

### Related work to cite and differentiate from
- Wu, Hu, Zhang, "Shared Weights, Selected Computations: How Looped Transformers Route What Each Loop Does" (arXiv 2609.39892): activation patching in toy looped transformers on graph walks; finds loops do not follow one-loop-one-step.
- Olszowiec et al., "Monitoring latent reasoning in looped language models" (arXiv 2610.18127): five interpretability lenses on eight looped LMs (Ouro, Huginn and others), distinguishing carry loops from re-read loops. Dory re-injects the input at every loop, so it is in their "re-read" class.
- "Latent Chain-of-Thought? Decoding the Depth-Recurrent Transformer" (arXiv 2507.02199): logit lens on Huginn.

None of these studies question repeats or Dory, so the experiment is not scooped. They do weaken the novelty of "first white-box look at a looped LM".

## 1. Would it get upvoted?

Probably not above 50, even on success.
- The parent result is an appendix of a post that has 48 karma and one comment after two days. Schulz's filler-reasoning post has 10. NOTES.md itself records that follow-ups since mid-October get 10 to 50.
- The audience for "mechanism of an appendix finding in a 4B NVIDIA model" is narrow: the Westover authors, a few interpretability readers, people who think about Long's width-versus-depth argument.
- The best case (a clean heat map showing that later copies read computed intermediates from earlier copies in loops 2+, with patching that redirects the answer) could reach 50 to 80 if it is framed as evidence about Astra-style filler uplift. The H-width outcome ("repeats are re-reading") is what most readers already assume and would land at 15 to 35.
- My estimate if stage 1 succeeded exactly as described: about 30% chance of exceeding 50 karma. Unconditional on success: about 10%.

## 2. Naturalness

Reasonably natural. Appendix A reports the looped-only repeat effect "without explanation", and the Westover authors call it evidence that looping changes behaviour qualitatively. Asking why is an obvious next question, and open weights make it answerable. It is a side-branch of that post, though: their own future-work section is entirely about controllability and monitorability on a larger looped model and does not mention mechanism.

Two framing problems:
- **"Only a looped transformer" overstates the prior.** Repeats help non-looped models too (Greenblatt: Opus 4.5, Qwen3 235B; NCRI ships `qrep@512` uplifts for many models). The Dory-specific fact is that the same weights gain from repeats at 2+ loops and not at 1. A 1-loop Dory is a weak, shallow configuration (16 + 20 + 16 half-layers), so "repeats do not help a weak model" is a boring alternative that the plan does not rule out. A non-looped open model of similar size with a known repeat uplift is the missing comparison.
- **H-refine versus H-width is not a clean dichotomy in per-loop KV mode.** With per-loop caching, unrolled Dory is an ordinary transformer of depth 8 + 20L + 8 with tied weights. Loop j at the final copy reads loop-j states of earlier copies, at the same unrolled depth. An intermediate computed at depth d in copy 1 is readable only at depth > d in copy 2, where copy 2 could in principle have computed it itself. So nothing is "relayed" in a way that saves serial depth; Long's argument applies unchanged. Both hypotheses are width hypotheses. The distinction that survives is what is routed (computed intermediates versus raw operands), and why the final position cannot compute it locally. The proposal's wording ("serial work being relayed", "spend its loops on later steps") promises more than per-loop mode can deliver. A real serial relay exists only in `last_loop` KV mode, which the plan demotes to a fallback and to stage 2.

A third hypothesis is missing and is the standard explanation for repeat uplift: **causal-mask re-reading**. In the first copy, early tokens (for example the rule table) cannot see later tokens (the query). In the second copy every token sees the whole question. This predicts strong dependence on whether the key or query comes first or last, and connects to the key-position confound post (ehF4kej38fkhb5cT3). It is testable with prompt edits alone.

## 3. Pre-mortem

How two days would likely go:
1. Hours 0 to 8: the team finds that `AutoModelForCausalLM.from_pretrained` fails. They install the vLLM PR for behavioural runs (works) and start reimplementing the forward pass in PyTorch from the vLLM PR source, or locate an unmerged transformers PR. Matching logits for nGPT plus loop re-injection plus hybrid attention takes between half a day and never.
2. Behavioural gate, run through vLLM: Dory is a 4B model. At 1 loop on 3+ step chains it is near floor; at 2 to 4 loops it manages perhaps 2 to 4 steps. The repeat uplift on aggregate NCRI is real but of unknown size (figure only). On a single clean task it may be 3 to 10 points in a narrow depth band. With 200 items per cell, a paired difference has a standard error of roughly 3 to 4 points, and the gate ("at least 8 points on at least one task") is evaluated over about 60 cells (3 tasks x depths x loops x repeats). It will be passed by noise in some cell and then shrink on re-measurement.
3. Knock-outs, if hooks work: blocking final-copy attention to earlier copies will remove the uplift. That is close to tautological (it turns the prompt back into r = 1 from the final copy's point of view) and distinguishes nothing. The per-loop breakdown is the only informative part, and it will most likely show a smeared dependence across loops and layers.
4. Probes: with 4 to 16 possible intermediate values and a few hundred items, probes decode intermediates at many positions including operand positions. The proposal acknowledges this.
5. Patching: the design ("two problems that differ only in the start value, patch earlier-copy residuals") cannot separate the hypotheses. The earlier copy's residuals contain the start-value token itself, and Dory re-injects the input embedding at every loop, so the answer following the donor is predicted by pure operand re-reading as well. A discriminating design must patch only non-operand positions, or only a probe-defined intermediate subspace, or use pairs with the same operands whose step-k intermediate differs because a mid-chain rule differs.

Forecast:
- Clear positive (localised mechanism with discriminating causal evidence): **10%**
- Clear negative that is still interesting (well-powered evidence for re-reading, or a clean demonstration that the looped-only effect is a weak-model artefact): **15%**
- Ambiguous mush (uplift replicated, knock-outs "work", no interpretable account): **40%**
- Fails to run or stops at the gate (no hookable implementation in time, or uplift too small on probe-able tasks): **35%**

Main failure reasons, in order: (a) no usable white-box implementation; (b) effect too small and too narrow in depth on clean tasks for a 4B model; (c) interventions that do not discriminate the hypotheses; (d) selection over many cells at n = 200; (e) low reader interest in either outcome.

## 4. Cost check

Money is not the constraint. The weights are 8 GB in BF16; a 24 GB card is enough for inference and for caching selected positions, and 300 GB of stored activations is unnecessary if only copy-boundary and answer positions are kept. Seventy GPU-hours at about $1/h is plausible as an upper bound. My estimate: **$60 to $150**, so the $150 figure is fine. The real budget problem is wall-clock: a day of the two could go to the implementation.

## 5. Recommended changes (most important first)

1. **Resolve the implementation question before funding.** State exactly which code provides a hookable forward pass (a transformers PR number, NVIDIA code, the Westover team's training code, or a port from the vLLM PR) and include a logit-equivalence check against vLLM as step 0 with a time box of 4 hours. If nothing hookable exists after that, the white-box arm is dropped, not debugged.
2. **Make stage 1 behaviour-first, so it yields a post even if white-box work fails.** Everything below runs through the vLLM PR with prompt edits only:
   - Partial repeats: repeat only the rule table, only the query, only the operands; shuffled or paraphrased copies; a copy of a different problem of the same type (does structure alone help?).
   - Order manipulations: query-first versus query-last in the single copy, to test causal-mask re-reading directly.
   - Corrupt-one-copy: change one operand in an earlier copy and see which copy the answer follows (this is the stage-2 "black-box bridge", and it is cheap enough to do now, on Dory and on GPT-6.1 Sol via OpenRouter at $2/$10 per million tokens).
   - Loops 1, 2, 4 and 8, in both KV modes. `last_loop` mode is where repeats or generated filler could buy real serial depth; it deserves a main arm, not a fallback.
   - A non-looped open model of similar size as the comparison that the "only looped" claim needs.
   This alone answers most of "what do repeats buy" at about $30, and the Sol comparison gives the post a reason to be read.
3. **Rewrite the hypotheses.** Drop "serial relay" for per-loop mode, where bounded depth forbids it. State three hypotheses with distinct predictions: causal-mask re-reading (order-sensitive; repeating the query suffices), operand routing (corrupt-one-copy follows the corrupted operand), and computed-intermediate routing (non-operand patching moves the answer). Add the weak-model alternative for the 1-loop result and say what would rule it out (for example, matching 1-loop and 2-loop accuracy by choosing easier depths, then comparing uplift).
4. **Fix the patching design** as described in section 3 so that operand re-reading does not predict the same outcome. Replace the tautological "block all attention to earlier copies" headline with the per-loop and per-token-class (operand versus non-operand source positions) breakdown.
5. **Correct the sliding-window statement** and design knock-outs for all attention layers. Report prompt lengths against the 1024-token window, since r = 5 pushes early copies out of it for sliding layers.
6. **Tighten the gate.** Choose the task and depth on a selection set, then confirm the uplift on a fresh 600+ item paired set with a pre-stated threshold. Report the loops-by-repeats interaction with a paired test instead of "at least 8 points on at least one task".
7. **Cite and differentiate** from arXiv 2609.39892, 2610.18127 and 2507.02199.
8. If the funder must choose within this cluster, the proposer's own ranking is right: this is the weakest of the four on expected attention. I would fund it only in the behaviour-first form of item 2 with the white-box work as a conditional extension, at about $100. As written, I would not fund it.
