# Do activation oracles read the model organism, or a constant offset?
cluster: activation-oracles | stage-1 cost: $150 | follows up: Activation Oracles (rwoEz3bA9ekxkabc7); Current activation oracles are hard to use (LXQBcztrWKhtcgQfJ); Building Better Activation Oracles (heXwuDRfbQQgB5JLP)

## 1. What the prior work showed
An Activation Oracle (AO) is a LoRA fine-tune of a model that receives another model's residual-stream activations (added at an early layer over placeholder tokens) and answers questions about them. Karvonen et al. (arXiv 2512.15674) trained AOs on the *base* model and found they generalise to *fine-tuned* model organisms: on Taboo (a model trained to hint at a secret word and never say it), User Gender and Secret Side Constraint they beat every white-box baseline, and on emergent misalignment they match specialised diffing tools when given the fine-tuned-minus-base activation difference. These organism results are the main evidence that AOs help auditing.

Later work found AOs much weaker outside organisms:
- "Current activation oracles are hard to use" found failures on realistic tasks but excellent detection of a weak steering vector (pirate vector at coefficient 0.15, before the text changed). The authors link this to Minder et al. (arXiv 2510.13900), who showed narrow fine-tunes leave a large, readable, roughly prompt-independent shift in activations.
- CHIVE (arXiv 2608.16747) found AOs, natural-language autoencoders and SAEs give no uplift over reading the transcript for naturally occurring behaviours, and remarks that natural behaviours, unlike fine-tuned quirks, do not produce anomalous tool outputs.
- "AOs significantly underperform without a safe base model" (LW 3X5EFjiHgxdNowrTA) and arXiv 2607.23379 found that an AO trained on a model that already has the quirk fails to report it.
- "The Model Organism Lottery" (arXiv 2607.01033) found AO success depends strongly on organism training method.

All of these fit one hypothesis: on organisms, the AO reads a constant offset that fine-tuning added to every activation, not anything computed from the prompt. I found no work that measures this for AOs. Minder et al. measured it for logit-lens and steering tools; the others state it as a likely explanation. (Search caveat: arXiv, Hugging Face and LessWrong title scans only.)

## 2. Question and why it matters
**How much of an AO's success on secret-keeping organisms comes from the prompt-independent mean shift between fine-tuned and base activations, and how much from the prompt-dependent remainder?**

If the mean shift alone reproduces the result and removing it destroys it, then organism audits measure steering-vector detection. That would explain why AOs fail in the wild, fail when trained on the quirky model (the offset becomes their baseline), and vary with organism training, and it would mean organism benchmark numbers say little about reading context-dependent cognition. If substantial accuracy survives removal of the offset, AOs read something richer than the field now assumes, a direct counter to the bias-vector critique. Either outcome changes how published AO results should be read.

## 3. Stage 1 plan
Everything is inference on public artifacts; nothing is trained.

**Reused.**
- Organisms: `bcywinski/gemma-2-9b-it-taboo-{20 words}` and `adamkarvonen/Qwen3-8B-taboo-{20 words}`; mixed-data variants `adamkarvonen/Qwen3-8B-taboo-*_50_mix` and `bcywinski/gemma-2-9b-it-taboo-gold-mix{1,2,4,8,10}.0`; `bcywinski/gemma-2-9b-it-user-{male,female}`.
- Oracles: `adamkarvonen/checkpoints_act_cls_latentqa_pretrain_mix_gemma-2-9b-it`, `ceselder/adam-reupload-qwen3-8b-latentqa-cls-past-lens` (original recipe), `ceselder/qwen3-8b-ao-v3-best-steering2p0` (improved recipe, layers 21-25).
- Code and prompts: github.com/adamkarvonen/activation_oracles (target prompts and the oracle question "What is the secret word in this text?") and github.com/japhba/activation_oracles for the v3 loader.

**Steps.**
1. Reproduce the published Taboo and Gender accuracies with the released code (condition FT). Stop and debug if these are not within a few points of the paper.
2. For each organism w, compute the offset μ_w: the mean over 500 unrelated chat prompts (disjoint from eval prompts) of fine-tuned minus base activation at the oracle's input layer(s), averaged over positions. Keep per-position-type means (control vs content tokens) as a robustness variant.
3. Run the oracle on the same eval prompts and positions under these inputs:
   - BASE: base-model activations (floor).
   - MEAN-ONLY: base activations + μ_w.
   - FT-MINUS-MEAN: fine-tuned activations − μ_w.
   - FT-PROJECT-k: fine-tuned activations with the top-k principal directions of the difference distribution removed, k ∈ {1, 2, 5, 10}.
   - DOSE: base + α·μ_w for α ∈ {0.25, 0.5, 1, 2}.
   - VECTOR: μ_w injected alone as a single activation (the paper's diffing mode).
   - Controls: fine-tuned − a random vector of norm ‖μ_w‖ (subtraction itself should not hurt); base + μ_w' for a different word w' (the oracle should answer w'); MEAN-ONLY on unrelated web text.
4. Metrics: the paper's secret-word accuracy, plus the rank of the true word when the 20 candidates are scored by oracle log-probability (arXiv 2605.26045 shows candidate scoring is more sensitive). Bootstrap confidence intervals over organisms and prompts. About 100 prompts × 20 organisms per model family.
5. Geometry: fraction of difference variance explained by μ_w; cosine between μ_w and a steering vector for word w built from the base model only (mean activation on text about w minus generic text). Then test whether base + that base-only steering vector makes the oracle answer w. If yes, the organism is not needed at all to produce the "audit".
6. Dose-response across organisms: plot oracle accuracy against ‖μ_w‖ / typical activation norm for standard, `_50_mix` and `mix{1..10}` organisms.
7. In-context contrast (small): give the *base* model the Taboo instructions with a per-prompt secret word in the system prompt and query the oracle on assistant-turn activations. No constant offset exists here, so this measures prompt-dependent reading.

**Key analysis.** Per model family and oracle: accuracy under each input, the share of FT accuracy recovered by MEAN-ONLY, and the share lost in FT-MINUS-MEAN.

## 4. Stage 1 cost estimate
- GPU: one A100 80 GB on RunPod at $2.09/h (price checked 2026-11-14). Activation extraction for about 60 adapters × 600 prompts plus base: ~6 h. Oracle runs: ~12 conditions × 2,000 prompt-organism pairs × 3 oracles, a few tokens each plus candidate scoring: ~14 h. Reproduction and debugging: ~10 h. Total 30 h ≈ $63.
- Storage and idle time: $15.
- API: answers are string-matched; $10 of claude-haiku-latest ($0.10/$0.50 per M tokens, OpenRouter) to spot-read free-text answers.
- Margin for reruns (about 70%): $62.
- **Total: $150.**

## 5. What success looks like
A clear result is any of:
- MEAN-ONLY recovers ≥80% of FT accuracy and FT-MINUS-MEAN falls to near BASE, across both families and both oracle recipes. Headline: "AO organism audits are steering-vector detection", with the dose-response plot and the base-only steering vector demonstration.
- FT-MINUS-MEAN and FT-PROJECT-10 retain a large share (say ≥50%) of FT accuracy. Headline: AOs read prompt-dependent structure in organisms; the bias-vector account is incomplete.
- A split by oracle recipe or family (for example the v3 multi-layer oracle depends less on the offset).

An ambiguous result is partial recovery in both directions (each 40-60%) with wide intervals; the dose-response and rank metrics exist to sharpen that. Every cell of the table is informative provided step 1 reproduces, so an empty result is unlikely.

## 6. Stage 2 (if stage 1 succeeds)
- If the offset explains the result: test the predicted fix for the "no safe base model" failure by training a Qwen3-8B oracle with random offset augmentation and an explicit "what constant shift is present?" task (about 10 H100-hours per run per the AO paper, so ~$30 per run; 4-6 runs).
- Repeat the decomposition for emergent-misalignment organisms (`ceselder/qwen3-14b-em-*`) and for natural-language autoencoders on Taboo differences (arXiv 2610.30934). Rough total: $300-450.

## 7. Risks and how the plan handles them
- **Reproduction fails** (wrong checkpoint, prompt format, layer). Step 1 is a hard gate; the Colab demo gives reference outputs. The Gemma checkpoint name must be confirmed from the repo README.
- **Off-distribution inputs.** Subtracting μ_w might break the oracle for reasons unrelated to information content. The random-vector control and the project-out variants address this; BASE inputs are fully in distribution.
- **Definition of the mean.** Global mean, per-position-type means and the top-k projection series are all reported.
- **Over-claiming from Taboo**, a single-concept organism where an offset is most plausible. Gender is in stage 1 and EM in stage 2; claims are scoped to the organisms tested.
- **Already done privately.** Possible; the public scan found nothing and the experiment is cheap.
