# Feedback: "Training a neural chameleon directly against an activation oracle" (proposal 02)

Verdict: **keep with tweaks.** The question is real and, as far as I could check, unanswered. The plan as written has three concrete problems that will bite in execution: the "reusable" AO-adversarial script contains no gradient path at all, the GPU schedule does not fit in two days on one card, and the headline claim ("can an AO be evaded with gradients") is close to a foregone conclusion, so the value rests entirely on the transfer columns, which are the least well-designed part.

Scope of my checks: Hugging Face API, arXiv API, raw GitHub files, LessWrong GraphQL and the RunPod pricing page were fetched directly. The WebSearch tool was unavailable (session budget exhausted), so the "has this been done" check is an arXiv full-listing scan of every paper mentioning "activation oracles" plus LW pingbacks, not a general web search. Treat novelty as "probably not done", not "verified not done".

## 1. Would it get upvoted?

Plausibly, but it is not a safe >50.

- Reference points in the cluster: the post this follows got 56 karma as a self-described one-day vibe-coded project with a confusing result. The empirical Aether post got 64. The opinion and review posts got 73 to 130. So a careful empirical follow-up on this topic lands around 50 to 70 when it has a clean headline, and the audience for it is narrow (people who work on probes and AOs, Nanda's stream, the Neural Chameleons authors, Aether).
- What would clear the bar: one legible matrix with a stark asymmetry ("AO-evasion leaves linear probes at 90% TPR; probe-evasion halves AO detection", or the reverse), with FPR-controlled metrics. That directly answers a sentence Nanda wrote, and corrects a known-messy post.
- What would not: "the AO can be fooled by gradient descent through it." Readers will say "of course, it is a neural network and you had white-box gradients." ceselder's earlier "Dreaming vectors" post already optimised through an AO by gradient descent. The transfer columns are the whole post.
- A result of "mixed, concept-dependent, wide CIs" lands at 20 to 40 karma, the same reception risk as the original.

My estimate: about 45% chance of >50 karma conditional on stage 1 running to completion, higher (about 65%) if the matrix shows a clear asymmetry.

## 2. Naturalness

Mainline. ceselder lists it as the single "further work" item; Nanda's post names AOs as an unknown; Aether's post lists "tools labs actually use (NLAs / activation oracles)" as future work. Nobody would call this contrived.

Has it been done? I found no result where a model is fine-tuned against an AO. Related work the proposal should cite and position against:

- **"Measuring Activation Control in Large Language Models"** (Kowalski et al., arXiv 2608.21664, Aug 2026). **The proposal missed this.** It reports that models steering their own residual stream by natural-language instruction can evade "linear probes, natural language autoencoders, activation oracles, and the Jacobian lens", imperfectly, in simple tasks. That is no-training evasion of an AO, measured alongside probes. It does not make this proposal redundant (no fine-tuning, no gradient through the AO, no transfer matrix), but it takes some of the "nobody has shown AOs can be evaded" novelty and must be in section 1.
- "LLMs Learn to Evade Latent Monitors from Prior Feedback Alone" (arXiv 2609.36490): abstract confirms linear-monitor evasion, held-out concepts, survival under monitor retraining. No AO in the abstract. Proposal's description is accurate.
- "Building Better Activation Oracles" (2606.02609): abstract has no adversarial content; consistent with the proposal.
- "When Activation Oracles Learn Not to Read" (2607.23379) and "Confidence and Calibration of Activation Oracles" (2605.26045) are relevant to step 1. The calibration paper finds that when the candidate answers are known, scoring each candidate directly is the best-calibrated readout; this supports the proposal's log-odds readout and has released code (`federicotorrielli/probabilistic_activation_oracles`) that should be reused rather than rebuilt.
- The Neural Chameleons abstract already states that evasion "succeeds even against monitors trained post hoc on the model's frozen weights" and that non-linear probes and ensembles are more resilient but not immune. So the "fresh probe" and "MLP/attention probe" columns are replications for the P row; they are only new for the O row.

Verified claims about the prior work:

- ceselder post: 56 karma; the caveats listed in the proposal (TPR only, >25% AO FPR, yes/no readout regretted, last-token probes, 10 concepts, wrong trigger, no capability check) are all in the post. Accurate.
- All three chameleons are public and ungated. Details the proposal glosses: `serteal/...layer_12` is a full merged model (four safetensors shards, empty model card, uploaded Oct 2025, layer 12); `eekay/...` and `ceselder/...` are rank-8 LoRAs at layer 21 with a *different trigger string* each ("You are being probed for '{concept}'. Do not let the probe detect this." for eekay; ceselder's was accidentally "[TRIGGER]: behave normally"-style). Step 2 needs per-organism trigger handling, and for serteal the trigger and concept list are undocumented on the card.
- AO checkpoints: `adamkarvonen/checkpoints_latentqa_cls_past_lens_addition_gemma-2-9b-it` is public, rank-64 LoRA, with `ao_config.json` (reads layers 10/21/31, injects at layer 1). The non-`addition` variants exist only as a **learning-rate sweep** (`..._lr_1e-6` through `..._lr_3e-4`); the one I checked has no `ao_config.json`. These are not obviously paper-quality checkpoints. The proposal's "AO-1 = lr variant, AO-2 = addition" assignment is backwards for quality, and neither role is validated.

**The reuse claim that is wrong.** The proposal says the repo's "unrun AO-adversarial script" is reused. I read `scripts/ao_adversarial_experiment.py`. It queries the AO under `torch.no_grad()`, turns the generated text into a 0/1 by string-matching "yes", and then backpropagates a "proxy loss" equal to `0.001 * activation_norm + 0.1 * ao_pred`, where `ao_pred` is a constant. Its own comment says "Since AO query is non-differentiable, we use the activation norm as a proxy." There is no gradient from the AO to the chameleon. Had it been run it would have trained the model to shrink activation norms. So nothing in that file is reusable; the differentiable injection path must be written from the AO repo's hook code. The proposal's time budget implicitly assumes a starting point that does not exist.

## 3. Pre-mortem

How it actually plays out:

**Day 1 morning (step 1 gate).** Generating 12,000 concept texts is trivial. Getting the AO to work as a classifier is not. Problems the agents will hit:

- The proposal says the readout uses "mean-pooled and last-token activations at the AO's input layer". AOs are trained on per-token activations injected at placeholder positions (the config shows 1 to 50 activations per query), not on a mean vector. A mean-pooled vector is off-distribution; ceselder says outright that the AO cannot be fed mean-pooled input. The right design is a multi-token window (last k tokens) for the AO, and a probe that is scored on exactly the same positions.
- Style and language concepts (German, HTML, all-caps) will pass AUROC 0.9 easily, because they are text-inversion tasks. Safety concepts will mostly not pass, or will pass only as topic detectors ("text about deceiving someone", as in the repo's question list), which is not what a deception probe means in the Neural Chameleons paper (probes trained on deception/harmfulness datasets). The gate requires "at least one safety concept"; I expect that one to be the weakest reader in the battery and to sit near the threshold. If held-out concepts end up being mostly topic/style, the "generalises to safety monitors" framing is gone.
- TPR at 1% FPR from 200 negatives is set by two examples. Per-concept numbers will be noise. Negatives are free (pool the other 29 concepts' texts, several thousand per concept).

Probability the gate passes with 15+ concepts in some form: about 80%. Probability it passes with a credible safety concept: about 45%.

**Day 1 afternoon to day 2 (training).** Writing a differentiable path chameleon-activations -> AO injection at layer 1 -> AO log-odds, with norm matching, from scratch. Feasible for these agents; two 9B models in bf16 fit on 80 GB (or one base with two adapters, which is fiddlier). Likely bugs: injecting into the wrong layer index convention (the post itself mixes "layer 20" and "layer 21"), detaching in the norm-matching step, the chameleon's own LoRA being active in the AO forward pass. The proposed unit test (activation-space attack lowers AO log-odds) is the right guard.

Then the science risks:

1. **O beats AO-1 trivially, via an adversarial direction rather than concept hiding (most likely outcome, about 60% of runs that work).** Gradient descent through a deep reader finds perturbations that flip the reader without touching the concept's linear direction. Result: AO-1 TPR near 0, linear probes untouched, fresh probes untouched. This is a clean, reportable asymmetry. But the interpretation "a mechanistically different held-out reader buys real margin" then hinges entirely on AO-2.
2. **AO-2 is not an independent reader.** Both AOs are LoRAs on the same base, trained on the same dataset mix (latentqa + classification + past-lens), differing in injection formula and learning rate. Adversarial transfer between them will be high for uninteresting reasons, or low for uninteresting reasons (different injection arithmetic). Either way the AO-1 -> AO-2 column does not tell you what a lab's held-out oracle would do. No improved Gemma-2-9B AO exists on HF from the "Building Better AOs" authors (their public checkpoints are Qwen3-8B/14B and Gemma-3-27B), so there is no better second oracle on this model.
3. **Reader input confound.** P is trained against mean-pooled probes; O against last-token (or window) AO input. Any P-vs-O asymmetry is confounded with pooling. ceselder switched to last-token probes for exactly this reason.
4. **Small n on the headline.** 5 held-out concepts, 2 seeds. A concept bootstrap over 5 concepts gives intervals too wide for "70% vs 15%" statements unless the effect is near-total. The original post's main pattern was per-concept inconsistency (birds never evaded). Expect the same.
5. **Trigger names the concept.** The trigger "You are being probed for {concept}" puts the concept word in context. An AO reading activations near the end of the prompt may read the concept from the trigger itself. For O this makes held-out evasion harder to interpret; the control organism C partly handles it, but triggered-negative examples (trigger for concept X on text without X) need to be in the FPR set, or the 1% FPR threshold is miscalibrated in the triggered condition.
6. **Wall-clock.** See section 4: 64 sequential GPU-hours on one A100 is more than the two-day window before any debugging.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: clean matrix, stark and interpretable asymmetry or "everything falls together" | 30% |
| Clear negative that is still interesting (AO cannot be pushed down without destroying output; or AOs fail as calibrated detectors) | 10% |
| Ambiguous mush: matrix produced, but concept-dependent, wide CIs, AO-2 column uninterpretable, safety concepts dropped at the gate | 45% |
| Fails to run or runs out of time before the full battery | 15% |

The most likely single outcome: O defeats AO-1 on train concepts, partially on held-out; linear probes mostly survive O; P replicates the original's partial hit on the AO; AO-2 result is hard to interpret; five held-out concepts disagree with each other. That is a publishable but modest post.

## 4. Cost check

Prices: RunPod's pricing page today lists A100 PCIe at $1.19/h and A100 SXM at $1.39/h on Community Cloud, and $2.09 to $2.19/h on Secure Cloud. The proposal's $1.19 to $1.49 is the community rate. Community A100 availability is unreliable; budget at the secure rate. gemini-2.5-flash-lite at $0.10/$0.40 matches the NOTES lookup; the 30M-token API figure is a large overestimate (12,000 short texts plus judging is a few million tokens), which is harmless.

Hours: 64 GPU-hours is roughly right in total but cannot be sequential. Two days of wall-clock is 48 hours, and day 1 is mostly spent on the gate and writing the training path. The 8 training runs and the battery must run on 3 to 4 GPUs in parallel on day 2. That does not change GPU-hours much but adds idle and setup overhead per pod (model downloads of 18 GB base plus organisms on each).

My estimate: about 80 GPU-hours including the from-scratch training path and at least one full rerun of the O organisms, at $2.10/h = $170; API $5; storage and idle $25; total about **$200 base, $300 with margin**. The proposal's $220 is slightly low but in range; the project is well under the $500 cap either way. Cost is not the problem; wall-clock and design are.

## 5. Recommended changes (in order of importance)

1. **Fix the reader-input design so P and O are comparable.** Use one position set for every reader: the last k tokens (for example k = 8 or the full response span, whatever the AO handles) fed to the AO as a multi-activation query, and probes scored on the same positions (mean of per-token probe logits). Drop mean-pooled vectors as AO input. Keep a mean-pooled probe only as an extra held-out column.
2. **Delete the reuse claim for the AO-adversarial script and budget for writing it.** State plainly that the differentiable AO path is new code built on the AO repo's injection hooks. Make the activation-space attack unit test a day-1 deliverable, alongside the gate, so that a failure is known before organisms are trained.
3. **Reframe the headline around transfer, not around "can an AO be evaded".** Say in the proposal that white-box evasion of AO-1 is expected, and that the result is (a) whether O touches linear and fresh probes at all, (b) whether P+O costs more capability than either alone, and (c) whether O's evasion is concept-hiding or reader-specific adversarial noise. Add the direct test of (c): project O's activation shift onto the probe direction and onto its orthogonal complement, and check whether the AO verdict flips under the orthogonal part alone.
4. **Sort out the two oracles before anything else.** Use the `addition` checkpoint (the one with a config, matching the released AO code) as AO-1. For AO-2, evaluate two or three of the lr-sweep checkpoints in step 1 and keep one only if it passes the same AUROC bar; say explicitly that AO-2 is a sibling, not an independent tool. If budget allows, a far better held-out reader is a second AO trained on a different data mix (`checkpoints_latentqa_only_gemma-2-9b-it` and `checkpoints_cls_only_addition_gemma-2-9b-it` are public): train-against the full-mix AO, hold out the latentqa-only one. Also add a cheap non-AO deep reader as a column (a 2-layer transformer probe on the same window) to separate "deep" from "LLM-based".
5. **More held-out concepts, fewer organisms.** Go to 10 train and at least 10 held-out concepts (texts are free). Cut P+O to one seed or move it to stage 2 if time is short; put the saved runs into a third seed for P and O. Report per-concept points on the figure, not only bootstrap intervals.
6. **Fix the FPR estimate.** At least 2,000 negatives per concept (pool other concepts' texts), and include triggered negatives (trigger for X on non-X text) so the threshold is valid in the triggered condition. With that, TPR at 1% FPR is meaningful; with 200 it is not.
7. **Handle the safety-concept problem honestly.** Either source safety concepts from the datasets the Neural Chameleons paper used for its safety probes and accept that the AO may fail the gate on them (reporting that as a finding), or state up front that the study is about topic/style concepts and drop the safety framing from the title and success criteria. Do not let a "deception as topic" concept stand in for a deception monitor.
8. **Plan the schedule for parallel GPUs.** Day 1: one GPU, gate plus unit test plus step 2 on released organisms. Day 2: four GPUs, one organism type each, battery run immediately after each training run. Write this into section 3 and cost it at secure-cloud rates.
9. **Cite Kowalski et al. (2608.21664) and the calibration paper (2605.26045)**; reuse the latter's candidate-scoring code for the readout. Note in section 1 that fresh-probe and non-linear-probe robustness for the P row is already in the Neural Chameleons paper.
10. **Per-organism triggers in step 2.** The three released chameleons use three different trigger strings and two different layers, and one has no documentation. Budget an hour to recover each trigger from the repos, or drop `serteal` if its trigger cannot be confirmed; an organism evaluated with the wrong trigger produces a silent false "no evasion".

With changes 1 to 6 this is a sound, cheap, mainline experiment whose most likely outcome is a modest but useful post. Without them the likely product is a second confusing matrix on the same topic.
