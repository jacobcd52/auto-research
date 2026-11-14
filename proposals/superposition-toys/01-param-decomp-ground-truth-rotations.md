# Can parameter decomposition recover 557 hand-coded circuits in superposition?
cluster: superposition-toys | stage-1 cost: $200 | follows up: Rotations in Superposition (LZ7YMPJueB6qjL24n)

## 1. What the prior work showed
Linsefors and Bushnaq hand-coded a ReLU MLP that runs many small circuits in superposition. Each circuit has d=4
neurons per layer: two re-compute a Boolean "on-indicator" through a step function, two rotate a 2-D vector by a
circuit-specific angle if the indicator is 1. Their headline network has width D=1000 and holds T=557 such circuits
over 6 layers (T·d > D, so superposition is necessary), with each circuit neuron spread over S=6 network neurons.
With one active circuit per input the average circuit works for about 4 of 5 rotations; with 2-3 active circuits
errors compound after 1-3 layers. The post concludes that independent circuits in superposition are costly, and
Lucius adds that parameter decompositions of GPT-2 Small rarely find more rank-1 circuit pieces than neurons. Code is public: https://github.com/LindaLinsefors/Rot-in-Sup (`plots_for_post.py`
builds the network from `classes_and_functions.py`; it runs on CPU).

The post applies no interpretability method to this network, although it is a rare object: a multi-layer network
that computes in superposition with every circuit's weights known exactly.

Parameter decomposition (APD, SPD arXiv 2506.20790, and VPD, "Interpreting Language Model Parameters", May 2026)
claims to find such circuits by splitting each weight matrix into rank-1 subcomponents, few of which are needed on
any input. Its public ground-truth tests are Toy Models of Superposition and the "compressed computation" /
ResidMLP toys. Bhagat et al. showed the compressed-computation model does not actually compute in superposition;
Ferreira da Silva et al. (arXiv 2607.04800, July 2026) built a single-layer trained model that does and say using
it to test decomposition is what they "plan to use it for next". I found no post or paper (LessWrong title scan to
2026-11-14, arXiv API; general web search was unavailable) that runs SPD/VPD on a multi-layer network with known
circuits in superposition. Library: https://github.com/goodfire-ai/spd (`param_decomp/`, target-agnostic trainer,
shipped TMS and ResidMLP toy targets, agent-oriented `docs/skill.md` on implementing a new target).

## 2. Question and why it matters
Given the hand-coded Rot-in-Sup network and its input distribution, does VPD/SPD recover the T known circuits, and
at what circuit load T·d/D does recovery break relative to where the computation itself breaks?

If it recovers them, this is the first ground-truth validation of parameter decomposition on multi-layer
computation in superposition, and it supports reading "few components per neuron in GPT-2" as a fact about GPT-2.
If it fails while the network still computes correctly, we learn that the method under-counts or merges circuits
exactly in the regime it was designed for, which changes how the GPT-2 component counts should be read. If it
finds a different but lower-loss decomposition than the designers' one, that is a concrete example of the
"intended circuits are not the minimal description" problem.

## 3. Stage 1 plan
Reused: Rot-in-Sup construction code; `param_decomp` trainer and toy configs. Built: a `DecomposedModel` wrapper
for a plain deep ReLU MLP, ground-truth extraction, and scoring.

1. **Gate (half a day).** Run the shipped TMS and ResidMLP decompositions unchanged and confirm they reproduce the
   expected one-subcomponent-per-feature result. If the JAX library cannot be made to run, fall back to the SPD v1
   PyTorch release (github.com/goodfire-ai/param-decomp, tag v1).
2. **Targets.** Export Rot-in-Sup networks as weight tensors at D=400, d=4, S=6, with 3 weight layers
   for T in {50, 100, 150, 200, 250} (load T·d/D from 0.5 to 2.5), plus the paper's
   D=1000, T=557 network. Inputs: z in {1,2,3} active circuits chosen uniformly, random unit vectors, embedded with
   the repo's read-in. "Computation works" is defined as in the post (mean |dx|^2 below the trivial baseline).
3. **Ground truth.** For each circuit t and layer l take its embedded weight contribution W_t^l from the
   construction (rank at most 4); shared terms the modified construction introduces are labelled "shared
   machinery", not circuits.
4. **Oracle check.** Insert the ground-truth decomposition into the VPD objective (faithfulness, stochastic and
   adversarial reconstruction, importance-minimality) and record its loss. This separates "the optimiser did not
   find it" from "the objective prefers something else".
5. **Decompose.** VPD with C = 2x and 4x the ground-truth subcomponent count per layer; sweep the importance
   coefficient and p-norm (about 12 configs) on T=100, pick by the library's own selection criteria without
   looking at ground truth, then run the chosen config on all targets with 3 seeds.
6. **Score.** (a) Activity match: for each circuit, best F1 between "circuit t is on" and "a group of
   subcomponents has causal importance above threshold", over held-out inputs. (b) Weight match: cosine between
   the summed matched subcomponents and W_t^l. A circuit counts as recovered if F1 >= 0.9 and cosine >= 0.8 in
   every layer. (c) Number of live subcomponents vs truth. (d) Cross-layer linking: do the matched subcomponents in
   consecutive layers co-activate, i.e. is each circuit found as one multi-layer object?
7. **Baselines.** Per-layer transcoders (width 4T) scored with (a); a shuffled-ground-truth control (random
   rank-matched splits of the same weights) for chance levels.
8. **Key plot.** Fraction of circuits recovered vs load T·d/D, overlaid with the fraction of circuits whose
   computation is within tolerance, for z=1,2,3; plus the oracle-vs-found loss table.

## 4. Stage 1 cost estimate
The targets are small MLPs (D<=1000), so a 24 GB GPU suffices. RunPod on-demand prices looked up 2026-11-14:
RTX 4090 $0.89/h, A40 48 GB $0.59/h.
- Gate + wrapper debugging: 10 GPU-h x $0.89 = $9.
- Hyperparameter sweep on T=100: 12 configs x 1.5 h = 18 GPU-h = $16.
- Main runs: 6 targets x 2 values of C x 3 seeds = 36 runs x 2 h (the D=1000 runs on an A40 if memory requires)
  = 72 GPU-h = about $64.
- Transcoder baselines and controls: 10 GPU-h = $9.
- Subtotal $98; doubled for reruns and a second sweep if the first selection fails: **$200**. No API spend.

## 5. What success looks like
A recovery-vs-load curve with tight seed-to-seed spread, and one of these clear statements: "VPD recovers >= 90% of
circuits up to load X, beyond the point where the hand-coded computation itself degrades"; or "recovery collapses
at load Y < 1 although every circuit still computes correctly, and the ground truth has lower objective value, so
this is an optimisation failure"; or "the found decomposition beats the ground truth on the method's own objective
and merges circuits in the following way". A null would be "runs do not converge to anything stable across seeds";
that is reportable only as a negative practical note and would not be a strong post, which is why step 1 and step 4
exist.

## 6. Stage 2 (if stage 1 succeeds)
(i) Decompose a network *trained* on the same task with L4 loss and ask whether its components match rotation
circuits or something more shared; (ii) the same ground-truth test on the trained Bloom-filter network and the
L4 compressed-computation model (github.com/FranciscoHS/toy-model-cis-code), where the ground truth is a known
binary code per token/feature; (iii) the full 6-layer D=1000 network across z. About $300-500 of GPU time.

## 7. Risks and how the plan handles them
- **Tooling friction (most likely).** The library is JAX and tuned for language models. Mitigation: the shipped
  toy targets are run first; the wrapper is a plain MLP; fallback to the simpler SPD v1 code; the D=400 targets
  keep every run under about two hours.
- **Tuning ambiguity.** A failure could be blamed on hyperparameters. Mitigation: the oracle-loss check, selection
  rules fixed before scoring, and the T=50 no-superposition-needed target (T·d < D) as a case that must succeed.
- **Ground truth is not unique.** Shared terms and the S=6 spreading may admit equivalent decompositions; the
  activity-match metric does not depend on a unique weight split, and the shuffled control calibrates chance.
- **Over-claiming.** One hand-coded family is not "CiS in general"; the write-up will say so.
