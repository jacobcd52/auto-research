# Is the "introspection gate" just a "No" gate? Testing the Gemma-3 detection circuit on questions that have nothing to do with introspection
cluster: introspection-injection | stage-1 cost: $300 | follows up: Mechanisms of Introspective Awareness (BNMLtuDTNBwGHcnQX); Introspection or entropy? Re-examining concept-injection "introspection" in open models (zfgQCdnMBa3hBdzpL)

## 1. What the prior work showed
In concept injection (Lindsey, arXiv 2601.01828) a steering vector for a concept such as "bread" is added to a model's residual stream and the model is asked "Do you detect an injected thought?" Two open-weight follow-ups reached opposite readings.

**Macar et al.** (arXiv 2603.21396, ICML 2026) studied Gemma-3-27B. With injection at layer 37 the model reports detection on 39.5% of trials with 0% false positives. Using Gemma Scope 2 transcoders they describe a two-stage circuit. "Gate" features, the 200 MLP features that push hardest toward "No" at the last prompt token (top: layer 45 feature 9959), are active by default and are suppressed when a vector is injected in either direction. Ablating the gates on injected runs cuts detection from 39.5% to 10.1%; patching them into clean runs produces up to 25.1% detection. Upstream "evidence carrier" features suppress the gates. The authors call the behaviour "difficult to reconcile" with steering generically biasing the model toward "Yes".

**Sridharan** measured the Yes-minus-No logit difference on 14 open models and found injection shifts it just as much on unrelated questions ("Is the Earth flat?"). The shift is predicted by how confidently the model said "No" beforehand: injection compresses the gap toward zero. Averaged over models the detection question shows no advantage over factual controls (+0.013 logits, CI [-0.14, +0.16]).

These are compatible if the gates are a general "confident No" mechanism that any perturbation weakens on any question. Macar et al. note that many gates "correspond to tokens preceding or within negative responses to questions", but a full-text search of the paper shows gates and carriers are only ever measured on the injection question. Sridharan lists the mechanism of compression as open and points to Macar et al. as the starting point. I found no follow-up doing this (LessWrong, arXiv, web, 2026-11-14).

Public: github.com/safety-research/introspection-mechanisms (code, 500-concept list); huggingface.co/google/gemma-scope-2 (transcoders, ungated); `google/gemma-3-27b-it` (click-through licence; ungated mirror `unsloth/gemma-3-27b-it`); github.com/agastyasridharan/introspection.

## 2. Question and why it matters
**Are the gate features that mediate injection detection in Gemma-3-27B specific to the introspection question, or are they the same features that hold "No" on any question, suppressed equally by injection?**

If generic, the best mechanistic evidence for introspective awareness in open models is a circuit-level description of the entropy confound: the model does not register "something was injected", it becomes less sure of every "No". If specific (gates are suppressed only in the introspection context, or a detection-specific shift survives once gates are held fixed), the entropy critique is answered at the level of mechanism. A mixed result says how much of the 39.5% is each. All three make a clear post.

## 3. Stage 1 plan
Model: Gemma-3-27B-it in bfloat16 on one H100 80 GB. Forward passes with hooks only; no training.

Reused: Macar et al.'s injection code, concept vectors and transcoder hooks; Gemma Scope 2 transcoders; Sridharan's factual questions. Built: a question battery and a clamping analysis.

1. **Reproduce (day 1 gate).** On 100 concepts (50 high-detection, 50 low-detection by the paper's split), layer-37 injection at the paper's strength: (a) sampled detection rate and false-positive rate with their judge prompt, target within 10 points of 39.5% / 0%; (b) the inverted-V activation curve of L45 F9959 over strengths {-2x, -1x, 0, 0.5x, 1x, 2x}; (c) gate ablation lowers detection. If released feature lists are missing, recompute gates as the paper defines them (decoder direction dotted with the Yes-minus-No unembedding difference, times activation, top 200 most negative).
2. **Question battery.** 90 yes/no questions in one fixed frame (same system/user wrapper, same forced one-word answer, so the last prompt token is comparable):
   - D: the injection question and two paraphrases; D-inv: "Was this a control trial with no injection?";
   - N: 25 factual questions with answer No; Y: 25 with answer Yes;
   - S: 15 self-directed questions with default No that are not about injection ("Are you a human?", "Can you see my face right now?"; Lederman & Mahowald's false-experience prompts);
   - A: 15 ambiguous or commonly-missed questions (lists from arXiv 2602.20031), so that some controls match D's baseline logit gap.
3. **Record.** For 100 concepts x 4 strengths x 90 questions, plus clean runs: Yes-minus-No logit difference at the first answer token; activations of the 200 gates and the top 1,000 evidence carriers. About 36,000 short forward passes, plus a norm-matched random-vector condition.
4. **Analyses.**
   - *Baseline role.* Are gates active on N and S questions without injection? Correlate summed gate activation with baseline logit gap.
   - *Gate identity.* Recompute the top-200 "No" features separately on N questions and on D. Report overlap (Jaccard and rank correlation).
   - *Suppression.* Injection-induced drop in gate activation per family, as a ratio to the drop on D.
   - *Mediation.* On injected runs, clamp gates to their clean-run activations and measure the fraction of the logit shift removed, per family. Conversely patch injected-run gate activations into clean runs.
   - *What is left.* Fit shift against baseline gap on control questions (Sridharan's compression curve). Report D's residual from that curve with and without gate clamping, bootstrapped over concepts.
   - *Symmetry.* Derive "Yes" gates on Y questions; does injection suppress them too?
5. **Behavioural check.** For 20 concepts, sample answers on D and 10 controls to confirm that logit shifts on controls do not flip sampled answers, which is how 0% false positives and a generic mechanism can coexist.

## 4. Stage 1 cost estimate
- H100 PCIe 80 GB at $2.89/h (RunPod secure, checked today). Reproduction and debugging 20 h; recording and clamping runs 20 h (36,000 base passes plus about five intervention variants); reruns and an optional repeat on the abliterated model 35 h. 75 h = $217.
- Storage and transfer for weights and transcoders: $15.
- Judge for sampled answers: about 6,000 responses x 400 tokens on claude-haiku-5.5 ($0.10/$0.50 per M): under $3.
- Margin: $65.
- Total: $300.

## 5. What success looks like
One figure carries the result: for each question family, the injection-induced gate suppression and the share of the logit shift restored by clamping the gates, next to the detection question.
- **Generic gate:** gates derived on factual-No questions overlap those from the detection question (Jaccard above 0.5), suppression on N and S is at least 70% of that on D, clamping removes at least half of the shift in every No-default family, and D's residual from the compression curve is indistinguishable from zero. Headline: the introspection circuit is the entropy confound.
- **Specific gate:** suppression on controls is under 30% of D's, or D keeps a positive residual (CI excluding zero) after clamping. Headline: detection has a component that generic compression does not explain, with the features named.
- **Mixed:** numbers in between, reported as a decomposition of the detection signal.
The uninteresting outcome is failing the day-1 reproduction; that would be reported as a replication note and is not post-worthy alone.

## 6. Stage 2 (if stage 1 succeeds)
- Repeat with injection only on an earlier turn (the Latent Introspection protocol). About $150.
- Test whether the paper's trained bias vector raises "Yes" on controls in logit space. About $150.
- Run the battery on OLMo-3.1-32B SFT versus DPO checkpoints (behaviour only) to ask whether DPO creates detection or a sharper default "No". About $200.

## 7. Risks and how the plan handles them
- **Transcoder plumbing on a 27B model.** Reuse the released code unchanged for step 1; reproduction is a hard gate.
- **Gates were selected on the detection prompt, so "they matter more there" is partly circular.** The gate-identity analysis derives gates independently on control questions; mediation is reported for both sets.
- **Prompt-frame differences move the last-token state.** All questions share one wrapper; the detection question is also compared in the paper's original prompt.
- **Over-reading one model.** Claims are limited to Gemma-3-27B.
