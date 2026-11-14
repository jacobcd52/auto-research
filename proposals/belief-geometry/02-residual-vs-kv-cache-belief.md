# Which part of the belief state lives in the residual stream, and is the rest in the KV cache?
cluster: belief-geometry | stage-1 cost: $120 | follows up: Generalized belief states in transformers (4f9p7brLdnTMFuwfB); The Geometry of Nonergodic Composition (JfJ4WTRHmooPBWRFv)

## 1. What the prior work showed
For data from a hidden Markov model (HMM), the *belief state* is the Bayesian posterior over hidden states given the tokens so far: everything the past says about the future. Shai et al. 2024 (arXiv 2405.15943) claimed transformers trained on such data represent it linearly in the residual stream.

The two posts disagree about how general that is.

- **Nonergodic post (Ray, Riechers, Shai):** a 4-layer, d_model-128 transformer trained on a mixture of two
  Mess3 processes linearly encodes the full 5-dimensional belief (held-out R^2 about 0.985 after block 3;
  untrained about 0.45) even though the next-token distribution is only 2-dimensional. They note it is cleanest with small weight initialization (std 0.02).
- **Generalized-belief-states post (Kolchinsky):** a transformer's recurrent state is the key-value (KV) cache, so the residual stream need not hold the belief. On MRRXOR
  (two random bits, then their XOR, with random state jumps; the belief is 4-dimensional but the next token
  depends on one direction) his repo reports random-split belief R^2 of 0.97 (4 layers, width 64, RoPE), 0.90 (learned positions), 0.72 and 0.64 (2 layers, width 32); the next-token distribution is decoded at 0.97-1.00, shuffled beliefs at about 0.01, untrained networks give 0.17-0.26. He fits a decoder that reads the belief from the KV cache through learned attention queries and an encoder that writes it back to steer the model, and conjectures that beliefs reach the residual stream by "leakage" that grows with layers, heads and width.
- A commenter (Vadim Fomin) reports a toy where a hidden bit is linearly readable from the residual stream only when the next token needs it.

Not done: splitting the belief probe into the part the next token needs and the part only the later future needs, comparing residual-stream and KV-cache readouts on the same models and targets, or varying process and architecture to find what controls the gap. Related work (arXiv 2502.01954, 2602.02385) studies residual geometry only. Public code: https://github.com/artemyk/belief-state (training, probes, checkpoints) and https://github.com/artemyk/gbs (KV-cache decoder and encoder).

## 2. Question and why it matters
Is the full belief state linearly present in the residual stream, or only the part needed for near-term prediction, with the rest recoverable from the KV cache? Which of process structure, model size, position embedding and initialization scale moves the boundary?

Three hypotheses: *Full*: all belief directions are decodable about equally well.
*Just-in-time*: decodability of a belief direction falls with the horizon at which it first affects
predictions. *Leakage*: the far-horizon part is in the cache and its residual-stream decodability rises with
width, heads and depth. The answer decides what a residual-stream probe or steering vector can see in principle: if state that matters later is held only in the cache until needed, probes miss it and single-position steering cannot change it. That matters to anyone probing LLMs for latent state. If instead the full belief is reliably present, Kolchinsky's critique is an artefact of small models, equally worth knowing.

## 3. Stage 1 plan
Reused: both Kolchinsky repos (training, probes, controls, cache decoder and encoder, committed checkpoints under `runs/`, of which I verified one); the nonergodic post's training spec. Built: horizon decomposition, three processes, the sweep.

1. **Horizon decomposition.** For any HMM, the map from belief to the distribution over the next h tokens is
   linear. Let V_h be the belief subspace that this map does not annihilate; V_1 (what the next token needs)
   is contained in V_2, and so on, up to the full space. Orthogonalize to get "first matters at horizon h"
   subspaces. For MRRXOR V_1 is one direction; for two Mess3s it is 2 of 5
   dimensions.
2. **Processes.** (a) MRRXOR at jump rates 0 and 0.05, reusing released checkpoints; (b) the two-Mess3 mixture, trained to the post's spec (weights are not public); (c) single Mess3, where everything is horizon 1 (anchor); (d) a delay family: two random bits, D filler tokens from
   an independent noisy process, then the XOR, with D in {0, 1, 2, 4, 8}, so the same belief direction is
   irrelevant to prediction for D steps.
3. **Models.** Baseline: 4 layers, width 64, RoPE, the repo's settings. One-at-a-time variations: 2 layers;
   width 32 and 128; 1 versus 4 heads; learned positions; initialization std 0.02 versus default. Three seeds
   each (five where checkpoints exist). About 200 small runs, each trained until KL to the Bayes predictor
   is below 1e-3 nats; runs that miss this are reported separately.
4. **Measurements, for every model, layer and horizon subspace.** (i) Held-out linear probe R^2 from the
   residual stream, using the repo's random and odd/even splits and its three controls (next-token
   distribution, shuffled beliefs, untrained network). (ii) R^2 of a cache readout: the repo's learned attention queries with its MLP readout, and a *linear* readout variant (small change to the repo). (iii) For fairness, a parameter-matched MLP probe on the residual stream, and the cache readout restricted to layers above the first (whose cache trivially contains the token history). Untrained-network versions of every readout give the floor.
5. **Key analysis.** Residual-stream R^2 against horizon h and delay D per architecture; the cache-minus-residual gap; regression of far-horizon residual R^2 on width, heads, depth, position embedding and init scale, with seed-level uncertainty.
6. **Causal check (MRRXOR baseline, released encoder).** Set the belief to that of another history by (i) replacing the probe-subspace component of the residual stream at one position, (ii) writing the encoded state into the cache. Measure KL to the target history's predictions over the next 8 tokens (500 history pairs), separately for horizon-1 and far-horizon differences.

## 4. Stage 1 cost estimate
- Training: about 200 runs of 100k steps on models under 1M parameters (assumed 15 GPU-minutes each when sharing a GPU): 50 GPU-hours on an RTX 4090 at $0.89/hr (RunPod, looked up 2026-11-14) = $45.
- Cache-readout fits (about 60 models x 3 variants) and probes: about 30 GPU-hours = $27.
- Causal check and plots: 5 GPU-hours = $5. Reruns and debugging margin (about 50%): $40. No API spend.
- **Total: about $120.**

## 5. What success looks like
One figure per process: residual-stream and cache R^2 against horizon (and D), with controls; plus a table of which architectural factors move the far-horizon residual R^2.
- Residual R^2 drops with horizon and delay, the cache readout stays high, and only cache writing changes far-horizon predictions: "transformers keep only the about-to-matter part of the belief in the residual stream", with a quantified boundary.
- If far-horizon subspaces are decoded as well as V_1 once models reach low KL (as the nonergodic post's 0.985 suggests), the full-belief claim survives a much harder test than total R^2, and the low values in small models are explained by a named factor.
- A process-dependent outcome is likely, and useful if the delay family gives a clean dose-response curve. A true null is seed-dominated R^2 with no pattern.

## 6. Stage 2 (if stage 1 succeeds)
Horizon-split probes and a cache readout on pretrained LLMs prompted with HMM data (arXiv 2609.17376 reports only total residual R^2) and on a natural-language state-tracking task. About $300-500.

## 7. Risks and how the plan handles them
- **Unfair readout comparison** (a flexible cache decoder can recompute anything from stored tokens). Handled by the linear variant, the matched residual MLP probe, excluding the first-layer cache, and untrained-network floors.
- **Per-subspace R^2 is unstable for low-variance subspaces; under-trained models can look "lazy".** Report variance shares, drop subspaces below a preset floor, apply the KL threshold and plot R^2 against KL.

- **Decomposition depends on the HMM presentation.** Compute it in the minimal generalized-HMM coordinates from the Hankel SVD, which the gbs repo already produces.
- **Pipeline breadth.** Day 1 is MRRXOR only, on released checkpoints and code (no training needed); new processes and the sweep come only after that figure exists.
- **Toy-only result.** The causal contrast and the adjudication between two recent posts carry it; stage 2 extends to LLMs.
