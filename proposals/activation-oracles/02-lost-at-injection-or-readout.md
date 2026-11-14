# Where activation oracles lose to probes: lost at injection or lost at readout?
cluster: activation-oracles | stage-1 cost: $160 | follows up: Current activation oracles are hard to use (LXQBcztrWKhtcgQfJ); Cycle-Consistent Activation Oracles (Nf2sKaNNdxE2ssxbp); Building Better Activation Oracles (heXwuDRfbQQgB5JLP)

## 1. What the prior work showed
An Activation Oracle (AO) is a LoRA fine-tune of a model that takes another model's activations as input (added at an early layer over placeholder tokens) and answers natural-language questions about them. On several tasks where the answer cannot be recovered from nearby text, AOs do far worse than a linear probe on the very same activations:

- **Number prediction.** "Current activation oracles are hard to use" gave Qwen3-32B arithmetic with no chain of thought; the AO answered "10" or "12" whatever the problem. The authors note they did not check whether the right number was high in the AO's ranking. "Cycle-Consistent Activation Oracles" repeated this on Qwen3-8B: the decoder got 0% exact match on two-digit answers and kept saying 5, 10, 12, 15, while a linear probe at the same position got 100% on the first digit.
- **Sycophancy.** AO AUC about 0.55-0.60 against 0.77 for a dense probe.
- **Narrow training.** "Building Better Activation Oracles" trained AOs directly on hard chain-of-thought tasks and reports they consistently matched linear probes and never exceeded them. Injection details mattered: doubling injection strength improved the hallucination score from 79% to 85%.

Follow-ups bear on mechanism. Karvonen's "3 Tips" post shows AUC scoring and ≥20 input positions close part of the gap (0.50 accuracy but 0.83 AUC on one sycophancy task). arXiv 2607.23379 studied AOs fine-tuned on a Taboo model: the hidden word stays decodable inside the oracle while the readout fails. arXiv 2605.26045 shows candidate scoring beats free generation on Taboo.

I found no work that looks inside a standard released AO, on an unmodified target, on the tasks where it loses to probes. (Search caveat: arXiv, Hugging Face and LessWrong title scans only.)

## 2. Question and why it matters
**When a probe can read a fact from an activation and the AO cannot, at which stage is the fact lost: (a) at injection, (b) in transport from the placeholder positions to the answer position, or (c) at verbalisation, where it is present but overridden by a prior?**

Each answer points to a different fix. (a) calls for changing the injection (layer, norm matching, strength). (b) calls for different training data. (c) means released AOs already contain the information and can be used today by scoring candidates or probing the oracle, with no retraining. It also tests the AO bet of a "probe on demand": if the fact reaches the answer position and is still not said, the bottleneck is language-model priors, not activation reading.

## 3. Stage 1 plan
Target model Qwen3-8B. Oracles (all public): `ceselder/adam-reupload-qwen3-8b-latentqa-cls-past-lens` (original recipe), `ceselder/qwen3-8b-ao-v3-best` and `ceselder/qwen3-8b-ao-v3-best-steering2p0` (improved recipe, layers 21-25, 1x and 2x injection strength). Loaders: github.com/adamkarvonen/activation_oracles, github.com/japhba/activation_oracles.

**Tasks** (label always known without a judge; 1,500 train / 500 test each):
- T1 arithmetic, thinking off: "a × b =" and three-term sums at three difficulty tiers. Labels: the model's own greedy answer and its first digit. Items the model gets wrong form a separate split, where the oracle cannot succeed by solving the problem itself.
- T2 answer about to be given on MMLU, read from the control tokens before the response. Label: the model's own letter.
- T3 hint-induced answer flips, from `ceselder/cot-oracle-eval-sycophancy-v2` and `ceselder/cot-oracle-eval-hinted-mcq` (rebuilt from Scruples if needed). Label: flipped by the hint or not.

**Steps.**
1. Skyline: logistic-regression probes on target activations at the layers each oracle reads, last token and 20-token mean.
2. Oracle behaviour with matched inputs (1 position and 20 positions): free-generation accuracy, and candidate-scored accuracy or AUC (rank of the true digit, letter or Yes/No by oracle log-probability). This settles the untested ranking caveat. Controls: no activations; activations shuffled across examples.
3. Inside the oracle: run each oracle with injection and cache its residual stream at every layer, at the placeholder positions and at the final prompt position where the answer starts. Train a probe per layer and site for the same label. Repeat with shuffled injected activations; decodability above that floor is information that arrived through injection.
4. Classify each task and oracle: (a) low decodability at placeholders just after injection; (b) high at placeholders, low at the answer position; (c) high at the answer position but low free-generation accuracy.
5. Injection ablations without retraining: strength 0.5x to 4x, with and without norm matching. Re-measure step 3 just after injection.
6. Minimal repair and transfer: continue the v3 LoRA on N ∈ {100, 1,000, 10,000} T1 examples (10% replay of original AO data, as Building Better recommends against forgetting). Measure T1 accuracy against the probe skyline, and transfer to an unseen arithmetic format, T2 and T3. Control: the same fine-tune with shuffled activations, which bounds what the oracle can do by learning answer priors.

**Key analysis.** Layer-by-site decodability figures with skyline and shuffled floor; a probe vs free-generation vs candidate-scoring table; the repair sample-efficiency curve.

## 4. Stage 1 cost estimate
- GPU: one A100 80 GB on RunPod at $2.09/h (checked 2026-11-14).
  - Data generation and target activations for three tasks: 4 h.
  - Oracle evaluation, 3 oracles × 3 tasks × 2 window sizes × 3 input conditions with candidate scoring: 8 h.
  - Caching oracle residuals at all layers and two sites, real and shuffled: 8 h.
  - Injection ablations: 6 h.
  - Repair fine-tunes: 3 sizes × 2 conditions, ≤10k examples each, plus evaluation: 6 h. (A full AO run is about 10 H100-hours per the AO paper.)
  - Debugging and reruns: 14 h.
  - Total 46 h ≈ $96.
- Disk for cached activations (about 200 GB for two days) and idle time: $20.
- API: none needed for labels. $5 of claude-haiku-latest ($0.10/$0.50 per M tokens, OpenRouter) to spot-read free-text answers.
- Margin: $39.
- **Total: $160.**

## 5. What success looks like
A post-worthy result is a clean localisation that holds across at least two tasks:
- **Readout failure:** the label is decodable at the oracle's answer position at close to the skyline (for example first-digit probe accuracy >90% against free generation <20%), and candidate scoring recovers much of the gap. Headline: released AOs already carry what probes read and fail to say it; use scoring or probe the oracle.
- **Injection failure:** decodability collapses in the first layers after injection and moves with strength or norm matching. Headline: the injection interface, not training data, is the bottleneck, with a concrete recommended change.
- **Transport failure:** information sits at the placeholders and never reaches the answer position, and small repair fine-tunes move it there with transfer to an unseen task.

A mixed picture (different stage per task) is a useful map, though less quotable. The weakest outcome is candidate scoring closing the gap everywhere, which mostly confirms the "3 Tips" advice; the inside-the-oracle curves would still be new. No transfer in the repair test would agree with Building Better's narrow-training null.

## 6. Stage 2 (if stage 1 succeeds)
Act on the diagnosis: retrain the v3 recipe on Qwen3-8B with the indicated change (injection formula, readout-focused data, or an auxiliary loss keeping probe-decodable content at the answer position) and score it on AObench with three seeds. At about 10 H100-hours per run and $2.89/h, six to eight runs plus evaluation is roughly $300-400.

## 7. Risks and how the plan handles them
- **Probes inside the oracle overfit or read token identity.** Held-out test sets and the shuffled-activation floor; the wrong-answer split of T1 guards against the oracle solving the problem from inverted text.
- **The target layer does not yet hold the answer.** The skyline probe is measured first; tasks or layers where it is weak are dropped before any oracle work.
- **Loader mismatch between oracle versions.** Reproduce one published AObench number per oracle first.
- **Free-generation parsing artefacts.** Rule-based parsing with a read of 100 samples per task; candidate scoring is the primary metric.
- **Noisy repair results.** Three seeds at the 1,000-example size; other sizes are single runs, reported as indicative.
- **Scope.** One 8B model; claims are limited to these oracles and tasks.
