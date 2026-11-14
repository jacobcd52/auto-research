# Does the neuron fire when its description says it should? A description-conditioned audit of Goodfire's public neuron atlas
cluster: neuron-legibility | stage-1 cost: $420 | follows up: Neural networks are not already clean (Dkh7pXKjoNWkkxQDz); Linkpost: Neural Networks Are Already Clean (x4kvabkF2Jk8GLZp8)

## 1. What the prior work showed
Cammarata's essay "Neural Networks Are Already Clean" claims that roughly 90% of MLP neuron poles in Qwen models have "one main job" once the positive and negative pole are read separately. Leo Gao's reply argues that clean-looking activating examples cannot establish this: "X matches Y is not commutative". Every firing may fit the pattern while most text that fits the pattern does not fire the neuron; in his experience neurons that look like "X" usually fire on "a very specific subset of X that is hard to characterize compactly", and forcing the neuron on for all X would degrade the model. He proposes scoring explanations by simulating the neuron from the description and measuring downstream KL.

Goodfire's technical report "Neurons as an Interpretable Basis" (10 Nov 2026, Qwen3.6-35B-A3B, a mixture-of-experts model) partly answers this. An LLM judge given a description picks the firing snippet out of a (firing, control) pair with 91% accuracy, and substituting description-simulated activations recovers 73% of ablation KL damage relative to an oracle ceiling (56% in the p99-99.9 band; not evaluated below p99). But both tests sample text by the neuron: evaluation windows are ones where the neuron fired, and controls are random or same-expert text, plus 40 random windows per pole for false-positive damage. Random text almost never contains the described concept, so the test Gao asks for, text that matches the description while the neuron stays silent, is not in the report.

Goodfire released a public atlas (gzip JSON under `https://static.goodfire.ai/neuron-atlas/2026-11-09-082204/`): descriptions and mode lists for 5,477 poles in layers 4-39, each pole's firing threshold θ, example windows with per-token activations, and Goodfire's own simulatability score for 585 poles (median 0.61). The model weights are public (Qwen/Qwen3.6-35B-A3B, Apache-2.0). I found no independent re-scoring of this atlas on LessWrong or arXiv as of 14 Nov 2026 (general web search was unavailable).

## 2. Question and why it matters
**When natural text matches a Goodfire neuron description, how often does the neuron actually fire, and what does it cost the model if we make it fire there?**

If recall is high and forced firing on the misses is cheap in KL, the "already clean" claim survives the strongest published objection, on Goodfire's own artifacts, checked by an outside party. If recall is low and forced firing is as damaging as ablating real firings, the descriptions are necessary-but-not-sufficient conditions, the 73% figure depends on sampling by the neuron, and enumerative uses ("no deception neuron fired") are unsafe. Either result settles a concrete disagreement between two widely read posts.

## 3. Stage 1 plan
Reused: Goodfire atlas JSON, Qwen3.6-35B-A3B weights, Goodfire's detection protocol and judge model (Opus 5.5). Built: MoE activation hooks, the retrieval-and-judge pipeline, intervention code.

1. **Hooks and replay check (gate).** Load the model on one 96 GB GPU; hook each routed expert's SwiGLU product `silu(gate)·up` with router weight. Replay atlas example windows for 200 poles and compare with the published per-token activations. Proceed only if rank correlation is above 0.9 on windows that still fire (Goodfire reports about 15% of exemplars stop firing without long context). This fixes neuron indexing and θ.
2. **Sample.** 400 poles: the 585 simulation-scored poles are the pool, stratified over the 8 layers, both signs, and Goodfire's monosemantic/polysemantic verdict. Descriptions are the atlas mode predicates only, with no examples.
3. **Corpus scan.** 30M tokens of public text mixed like Goodfire's (FineWeb, a code set, a chat set, about 15% non-English), 512-token contexts. Store activations above 0.25θ for the 400 poles.
4. **Description-conditioned sampling, blind to activations.** Per pole, retrieve up to 150 candidate windows using (i) keywords and regexes written by an LLM from the description and (ii) embedding search of the description with Qwen3-Embedding-0.6B. An Opus 5.5 judge sees the description and a 250-token window and marks the token where the pole should fire and an expected strength (none / weak / at-threshold / strong). A second judge (GPT-6.1 Terra) labels a 20% subsample for agreement.
5. **Primary metric: description recall.** P(activation ≥ θ within ±2 tokens of the marked token | judge says at-threshold or strong), per pole and pooled, with bootstrap intervals over poles. Also the dose-response between judged strength and activation/θ.
6. **Calibration arms.** (a) Firing-conditioned detection, replicating Goodfire's 0.91, to show the judge and descriptions work in the tested direction. (b) Shuffled descriptions from the same expert as a floor. (c) The same judge given the description plus 10 real firing examples, to separate "description is incomplete" from "judge misreads".
7. **Causal cost of the misses.** At description-matched but silent tokens, set the neuron to the median activation of its true firings and measure KL to the clean model over the next 16 positions. Compare with the KL from ablating the neuron at real firings. Single-neuron KL is tiny, so the headline version intervenes on all 400 poles at once across a held-out set, following Gao's suggestion to batch.
8. **Simulation under three sampling schemes.** Using the judge's strength labels as the simulator, compute KL damage recovered (versus mean-ablation, with a 10-level oracle ceiling as Goodfire does) on windows sampled (i) by firing, (ii) by description, (iii) uniformly. Scheme (i) should land near Goodfire's 73%; the gap to (ii) is the result.
9. **Analysis.** Recall by layer, sign and verdict; correlation with Goodfire's simulatability score; 30 miss cases written up with their text.

## 4. Stage 1 cost estimate
Prices looked up 14 Nov 2026 (RunPod, OpenRouter).
- GPU: RTX Pro 6000 96 GB at $2.69/h. Debugging and replay 10 h, scan 8 h, interventions and simulation 12 h, reruns 10 h: 40 h = $108.
- Judge (Opus 5.5, $4/$20 per M): 60k windows × ~350 input tokens = 21M in, 2M out = $124. Few-shot arm on 100 poles: about $30. Firing-conditioned arm 8k pairs: about $10.
- Second judge (GPT-6.1 Terra, $1/$5) on 12k windows: $7. Keyword generation (Sonnet 5.5, $2/$10): under $10.
- Storage and egress: $15.
- Subtotal about $305; margin for reruns and prompt iteration $115. **Total $420.**

## 5. What success looks like
Three plots: the distribution of per-pole description recall beside firing-conditioned detection accuracy, with the shuffled floor and few-shot ceiling; KL damage recovered under the three sampling schemes; batched forced-firing KL versus batched ablation KL.

Clear outcomes: (a) median recall ≥ 0.8 and forced-firing KL below 10% of ablation KL: Gao's failure mode is rare for these descriptions; (b) median recall ≤ 0.5 with forced-firing KL comparable to ablation KL: descriptions are over-broad in a way that matters; (c) low recall but negligible forced-firing cost: the misses are real but harmless, which supports Cammarata's "too demanding" reply and is itself new. An ambiguous result is recall of 0.6-0.75 with wide judge disagreement; still reportable, though less striking.

## 6. Stage 2 (if stage 1 succeeds)
Have an agent revise low-recall descriptions against description-conditioned text and plot description length versus recall. Extend to all 5,477 atlas poles and to a dense model with freshly generated descriptions. Roughly $1,500-2,500.

## 7. Risks and how the plan handles them
- **Hook or indexing mismatch with Goodfire's conventions** (router weighting, expert numbering). The replay gate in step 1 catches it on day one using published per-token activations.
- **Judge error passed off as neuron error.** Count only confident judgments; report two-judge agreement; the few-shot arm and the dose-response curve show whether the judge tracks the neuron at all; inspect 30 misses by hand.
- **Retrieval bias toward easy lexical matches** inflates recall. Report recall separately for keyword-retrieved and embedding-retrieved windows.
- **Single-neuron KL below numerical noise.** Measure the noise floor with a null intervention and use the batched 400-pole intervention as the headline.
