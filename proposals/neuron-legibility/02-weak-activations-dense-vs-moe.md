# Do weak neuron activations matter? Reproducing the weak-activation ablation across dense, mixture-of-experts and 1-bit models
cluster: neuron-legibility | stage-1 cost: $230 | follows up: Neural networks are not already clean (Dkh7pXKjoNWkkxQDz); Linkpost: Neural Networks Are Already Clean (x4kvabkF2Jk8GLZp8); Twitch Plays: AI Interpretability of Bonsai-8B (ozbbzsh49wvgfbCDp)

## 1. What the prior work showed
The "already clean" case for reading neurons directly rests on a factual claim: a neuron's weak activations barely matter, so explaining its strong tail explains the neuron. Cammarata's essay shows this in a vision model (removing the weakest 75% of ConvNeXt activations moves accuracy from 72% to 71%). Goodfire's technical report "Neurons as an Interpretable Basis" (10 Nov 2026) shows it in one language model, Qwen3.6-35B-A3B, a mixture-of-experts (MoE) model: keeping only the 320 strongest of 4,096 routed neurons per token in every layer (ablating 92.2%) raises loss from 1.886 to 1.940 (+2.9%) with KL 0.140 on 8.4M web tokens; mean-ablating each neuron's p25-p75 band costs +0.010 loss. Reasoning benchmarks break unless the sparsified model is fine-tuned. The report covers no dense model and says of weak activations "we leave investigation of them to future work".

Leo Gao's reply post states the opposite expectation: "ablating small neuron activations quite substantially degrades model performance", adding "it's surprising that my result here is different from Nick's, and it seems worth tracking down the source of the divergence." He argues KL is the right metric because loss changes can cancel. He has not yet posted data.

Related evidence does not settle it. arXiv:2610.24521 (neverix et al.) sparsifies MLPs in Gemma, Qwen 3 and Llama models to about 32-64 active neurons per layer, but one layer at a time with a learned linear correction (KL around 0.5); its author says he has "preliminary evidence that MoE MLPs are only usable at a lower sparsity". The Bonsai-8B project found that Bonsai's 1-bit and ternary models keep the neuron basis of their parent Qwen3-8B (same-index best match 92-99% in layers 5-33), so the three form a paired precision ladder, but it has not measured weak-activation dependence. I found no dense-model replication of Goodfire's sweep as of 14 Nov 2026 (checked via the LessWrong post listing and arXiv queries; general web search was unavailable).

## 2. Question and why it matters
**How much of a language model's behaviour depends on weak MLP neuron activations, and does the answer depend on the model being MoE, on its size, on quantisation, or just on how the ablation and the metric are defined?**

Candidate explanations for the Gao-Cammarata divergence are concrete and separable: (1) architecture: an MoE router already zeroes 97% of neurons, so "weak" means something different than in a dense MLP; (2) metric: +2.9% loss sounds small while KL 0.14 nats is large by the standards used for sparse-autoencoder replacement; (3) selection rule: per-token top-K versus per-neuron percentile bands; (4) ablation type: zero versus mean; (5) evaluation: next-token loss on web text versus multi-step generation. If weak activations matter much more in dense models, the neuron-explanation programme has a hole where most open models live. If the result replicates, a main objection loses force. If the gap is mostly framing, the post gives both camps one shared table.

## 3. Stage 1 plan
Reused: public weights; Goodfire's published ablation definitions and numbers as calibration target; the bonsai-interp loader for exact 1-bit weights (https://github.com/moridinamael/bonsai-interp). Built: a small hooking and streaming-quantile library. No LLM judging, no fine-tuning.

Models (all ungated on Hugging Face):
- Dense SwiGLU size ladder: Qwen3-0.6B, 1.7B, 4B, 8B, 14B, 32B.
- MoE: Qwen3.6-35B-A3B (Goodfire's model) and Qwen3-30B-A3B.
- Precision ladder: Qwen3-8B, Ternary-Bonsai-8B-unpacked, Bonsai-8B-unpacked.

Steps:
1. **Calibrate.** For each model, stream 3M tokens (FineWeb plus code and chat text, 1,024-token contexts) and record per-neuron activation histograms for `silu(gate)·up`, giving per-neuron percentiles and means.
2. **Reproduce Goodfire first (gate).** On Qwen3.6-35B-A3B apply router-weighted top-320 per layer and the p25-p75 mean-ablation. Target: loss delta near +0.054 and KL near 0.14, and +0.010 respectively. A large mismatch means a hook bug or a definitional difference, resolved before any dense run.
3. **Main sweep, all layers at once, 1M held-out tokens per condition.** Two selection rules: (a) per-token top-K by absolute activation, with K chosen to keep 50, 25, 12, 8, 4, 2 and 1% of neurons; (b) per-neuron central percentile bands p25-75, p10-90, p5-95, p3-97, p1-99, p0.1-99.9. Two ablation types: zero and per-neuron mean. Controls: random-K and bottom-K at matched counts. Metrics: KL to the intact model (mean, median and 95th percentile over tokens), loss delta in nats and percent, top-1 agreement.
4. **Where the damage sits.** Repeat one mid-strength condition on single layers and on thirds of the network; split KL by token type (web, code, chat, non-English). For 2,000 random neurons per model, measure single-neuron ablation KL restricted to each activation band, to get the dense-model counterpart of Goodfire's "bands at or above p99.9 carry 73% of a neuron's ablation damage".
5. **Generation check.** At Goodfire's 7.8% retention, score repetition-loop rate on 300 continuations and accuracy on 500 GSM8K items, without fine-tuning, on Qwen3-4B, 8B, 14B and Qwen3.6-35B-A3B.
6. **Precision ladder.** Same sweep on the three 8B models, plus overlap of the retained neuron sets between models at each K.
7. **Analysis.** One figure: KL versus fraction of activations retained, one curve per model, Goodfire's reported points overlaid. A table giving, for each model, the retention at which KL crosses 0.05, 0.1 and 0.3 nats. A verdict on each of the five candidate explanations.

## 4. Stage 1 cost estimate
Prices from RunPod on 14 Nov 2026: RTX Pro 6000 96 GB $2.69/h; L40S 48 GB $1.09/h.
- Models up to 14B and the 8B ladder on an L40S: calibration plus about 30 conditions each, roughly 4 h per model × 8 models = 32 h = $35.
- Qwen3-32B, Qwen3-30B-A3B and Qwen3.6-35B-A3B on the 96 GB card: about 10 h each = 30 h = $81.
- Single-neuron band ablations and generation checks: 12 h on L40S, 6 h on the 96 GB card = $29.
- Storage for weights and histograms (about 300 GB for two days) and transfer: $15.
- Subtotal $160; margin for debugging and reruns (about 45%): $70. **Total $230.** No API spend is required.

## 5. What success looks like
The headline is the retention-versus-KL figure and a one-sentence answer per candidate explanation. Post-worthy outcomes:
- **Dense models are much less tolerant**: for example, keeping 8% of neurons gives KL above 0.5 in dense Qwen3 models versus about 0.14 in the MoE. This locates the divergence in architecture and limits the "already clean" evidence to MoE models.
- **Dense models match the MoE** once retention is counted the same way. This is an independent replication extending Goodfire's claim to six dense models.
- **The numbers agree and the disagreement is framing**: both camps' statements are true of the same curve (small percent loss, sizeable KL, broken multi-step generation). The post then states which downstream uses each regime supports.
The precision-ladder result (does 1-bit training change dependence on weak activations?) is a secondary finding. "No clean pattern across sizes" is the weakest outcome but still publishable as a table; if the gate in step 2 passes, the project also yields an independent replication of Goodfire's number.

## 6. Stage 2 (if stage 1 succeeds)
Test whether the weak band is interpretable: fit low-rank or description-based simulators to it and measure KL recovered. Lightly fine-tune sparsified dense models, as Goodfire did for the MoE, to see whether the dependence is removable. Roughly $1,000-2,000, mostly GPU.

## 7. Risks and how the plan handles them
- **Definitional mismatch with Goodfire** (router weighting, treatment of the shared expert, which they leave intact). The reproduction gate in step 2 surfaces this before the sweep; if exact numbers cannot be matched, both variants are reported.
- **MoE hooking is fiddly in Hugging Face code.** Budget assumes 10 h per large model; if Qwen3.6-35B-A3B stalls, Qwen3-30B-A3B is the fallback and Goodfire's published numbers remain the comparison.
- **Unfair dense-versus-MoE comparison.** Report retention both as a fraction of all neurons and as a fraction of routed neurons, and give matched-KL retention levels.
- **Quantile noise for rarely firing neurons.** Verify on 10M calibration tokens for one model that results do not move.
