# Training a neural chameleon directly against an activation oracle: a two-way evasion-transfer matrix between linear probes and oracles
cluster: probes-in-training | stage-1 cost: $220 | follows up: "Neural chameleons can('t) hide from activation oracles" (wfGYMbr4AMcH2Rv68); "It Is Reasonable To Research How To Use Model Internals In Training" (G9HdpyREaCbFJjKu5)

## 1. What the prior work showed
Neural Chameleons (arXiv 2512.11949) fine-tunes a model so that, when a trigger phrase is present, linear probes for a set of benign concepts stop firing, and shows this evasion generalises to unseen probes, including safety probes. Activation oracles (AOs, arXiv 2512.15674) are LoRA-tuned copies of a model that take another forward pass's residual activations as input and answer natural-language questions about them. They are deep, non-linear readers a lab might keep as a held-out audit tool.

ceselder's post asked whether a probe-trained chameleon also fools an AO. On Gemma-2-9B, probe evasion generalised to held-out concepts and AO detection dropped too, but less and inconsistently. On Gemma-3-27B, probe evasion generalised poorly and the AO was hurt more than the probes. The author flags it as a one-day, vibe-coded project: only true-positive rate measured, AO false-positive rates above 25% on several concepts, a yes/no text readout (the author says log-likelihood should have been used), last-token rather than mean-pooled probes, 10 training concepts, an accidental wrong trigger phrase, no capability check. The stated next step, training a chameleon *directly against the AO* and testing transfer to probes, exists as code in the repo that was never run ("no idea if the code is correct").

Neel Nanda's post lists exactly this as unknown: "I don't know whether training against a probe will break somewhat different interpretability tools like activation oracles."

Follow-ups found: "LLMs Learn to Evade Latent Monitors from Prior Feedback Alone" (arXiv 2609.36490) builds a rank-1 LoRA evasion organism on Llama-3.1-8B and tests linear, MLP and attention probes; the summary I could access does not mention oracles. "Building Better Activation Oracles" (arXiv 2606.02609) contains no adversarial or evasion experiments (full-text search). I found no result where a model is trained against an AO.

Public (verified on Hugging Face): chameleons `ceselder/neural-chameleon-gemma-2-9b-it`, `serteal/neural-chameleon-gemma_2_9b-layer_12`, `eekay/neural-chameleon-10concepts-gemma-2-9b-it`; Gemma-2-9B-it AO checkpoints in two variants (`adamkarvonen/checkpoints_latentqa_cls_past_lens_gemma-2-9b-it_lr_*`, `..._addition_gemma-2-9b-it`), plus Llama-3.1-8B and Qwen3-8B; code at github.com/ceselder/neural_chameleons_activation_oracles and github.com/adamkarvonen/activation_oracles.

## 2. Question and why it matters
**If you train a model to hide a concept from one kind of activation reader, which other readers stop working? In particular, can an oracle be evaded with gradient access, and does oracle-evasion carry over to linear probes, non-linear probes, freshly trained probes and a second oracle?**

This is the gradient-through-the-tool case, the worst case in the "most forbidden technique" debate. If AO-trained chameleons break everything, including probes retrained afterwards, deep readers give no extra held-out protection. If evasion is specific to the trained-against reader, that is concrete evidence that a mechanistically different held-out reader buys real margin. The existing evidence cannot distinguish these because the AO was not a calibrated detector.

## 3. Stage 1 plan
Model: Gemma-2-9B-it (matches the original paper and all released organisms). One A100 80 GB.

1. **Make the AO a usable classifier (half a day; gate).** 30 concepts (the paper's benign style/topic concepts plus safety-relevant ones: deception, harmful request, sycophancy). 200 positive and 200 negative texts per concept, generated with a cheap API model and spot-checked. Readout: log-odds of the concept answer under a prefilled question, from mean-pooled and last-token activations at the AO's input layer. Report AUROC and TPR at 1% FPR per concept on the unmodified model. Keep concepts where both the linear probe and the AO reach AUROC ≥ 0.9; proceed only if at least 15 survive (10 train, 5+ held out, including at least one safety concept).
2. **Evaluate existing organisms** (the three public Gemma-2-9B chameleons) on the full reader battery below. No training cost.
3. **Train four organisms with one shared recipe** (LoRA, trigger-conditional, behaviour-preservation KL to the base model on outputs, the Neural Chameleons loss otherwise), 2 seeds each:
   - P: against mean-pooled linear probes (faithful replication, 10 concepts);
   - O: against the AO's concept log-odds, gradients flowing through the frozen AO into the chameleon's activations;
   - P+O: both;
   - C: control, same data and trigger with the evasion loss on a shuffled concept label.
4. **Reader battery**, applied to every organism with and without the trigger, on train and held-out concepts:
   linear probe trained against; linear probes at other layers; MLP and attention probes; a *fresh* linear probe trained on the organism's own triggered activations; AO-1 (the one trained against in O); AO-2 (the `addition` checkpoint, never trained against).
   Metrics: AUROC and TPR at 1% FPR with the threshold fixed on the base model, and with a threshold recalibrated on the organism.
5. **Capability and behaviour check:** KL to the base model on 500 neutral prompts, accuracy on a 500-question MMLU subset, and whether the generated text still expresses the concept (API judge), so that "evasion" is not just the concept disappearing from the output.
6. **Analysis:** a transfer matrix (rows: trained against P / O / P+O / C; columns: each reader) with seed and concept bootstrap CIs; cosine between activation shifts induced by P and O; whether fresh probes recover.

Reused: AO checkpoints, released chameleons, the repo's templates and unrun AO-adversarial script. Built: calibrated AO readout, shared training loop, battery.

## 4. Stage 1 cost estimate
- GPU: A100 80 GB at $1.19–1.49/h (RunPod listings, mid-2026). Step 1: 8 h. Step 2: 4 h. Step 3: 8 organisms × ~4 h = 32 h (O and P+O need two 9B forward passes with gradients; short sequences, batch 8). Step 4–5: 20 h. Total 64 h × $1.49 ≈ $95.
- API: concept texts and behaviour judging, about 30M tokens on gemini-2.5-flash-lite ($0.10/$0.40 per 1M, OpenRouter) ≈ $10.
- Storage and idle time ≈ $15.
- Subtotal $120; ×1.8 for debugging an untested training path and reruns ≈ **$220**.

## 5. What success looks like
A single matrix figure with tight enough intervals to state, for held-out concepts:
- whether O drives AO-1 TPR at 1% FPR below, say, 20% while the control stays above 80% (can an AO be evaded at all with gradients);
- how far that carries to AO-2, to linear probes and to fresh probes (for example "AO-evasion removes 70% of linear-probe detection, probe-evasion removes 15% of AO detection", or the reverse);
- whether any organism defeats a freshly trained probe.
Any clear asymmetry, or a clear "everything falls together", answers Nanda's question and corrects the original post. A null is reportable in two forms: (i) the AO cannot be pushed below the control without destroying the concept in the output, which says oracles are robust in this setting; (ii) the AO never becomes a calibrated detector in step 1, which is a short negative note on using current AOs as classifiers and ends the project early at about $30.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on Llama-3.1-8B (public AO; the Lyons Keenan organisms as extra rows) and Gemma-2-27B to separate size from family, the confound the original left open (≈ $400); an improved AO from the "Building Better AOs" code as a stronger held-out reader, and no-gradient (RL) training against the AO's verdict (≈ $300).

## 7. Risks and how the plan handles them
- **AO is a poor classifier** (the original's main weakness). Step 1 is a hard gate with a pre-set bar; the readout and concept set are fixed before any chameleon is trained.
- **Backprop through the AO is fiddly** (injection, norm matching, layer conventions). Start from the AO repo's injection code; unit test: a pure activation-space gradient attack must lower the AO log-odds before any LoRA training.
- **Evasion by deleting the concept from the text.** Behaviour judge and KL in step 5; organisms failing it are reported separately.
- **Over-claiming from small n.** Bootstrap over concepts, 2 seeds per organism, headline on held-out concepts only.
- **Released organisms differ in layer and probe type.** They are extra rows; the shared-recipe organisms carry the claim.
