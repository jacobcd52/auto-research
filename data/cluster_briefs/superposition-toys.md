# Cluster: Toy models of superposition and memorisation

key: `superposition-toys` — 4 post(s); write at most 2 proposal(s).

## Rotations in Superposition
- id: `LZ7YMPJueB6qjL24n` | 2025-12-15 | 54 karma | Linda Linsefors, Lucius Bushnaq
- url: https://www.lesswrong.com/posts/LZ7YMPJueB6qjL24n/rotations-in-superposition
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Experimentally tests the authors' mathematical framework for circuits in superposition by hand-coding the weights of an MLP to implement many conditional 2D rotations in superposition over several layers, then comparing recovered values with targets and studying how noise accumulates. Code is public.
- screener's follow-up note (often the screener's inference): Check whether trained (not hand-coded) networks learn similar constructions, and whether interpretability/decomposition methods recover the known circuits in this ground-truth testbed.
- builds on: The authors' earlier post sketching a construction for circuits in superposition

## A tale of three theories: sparsity, frustration, and statistical field theory
- id: `siu22scEfuKxpSgfK` | 2026-01-25 | 63 karma | Dmitry Vaintrob
- url: https://www.lesswrong.com/posts/siu22scEfuKxpSgfK/a-tale-of-three-theories-sparsity-frustration-and
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Informal write-up of theory plus toy-model experiments (Principles of Intelligence / PIBBSS). A small network is trained to denoise sparse (2-hot or 3-hot) boolean vectors with more features than hidden dimensions; the authors argue from mean-field / statistical-physics theory, with reported theory-experiment agreement, that interference in superposition produces a 'frustrated' large-scale weight structure that induces irreducible noise in the loss landscape even with infinite, symmetric data. Mostly theory; a more formal paper is planned.
- screener's follow-up note (often the screener's inference): Replicate the frustrated vs non-frustrated weight structures in the toy denoising model across hidden/feature dimension regimes and check whether the predicted noise appears in other superposition toy models.
- builds on: Toy Models of Superposition (Elhage et al.)

## Neural Networks learn Bloom Filters
- id: `buxBdp8NtHGgBwabv` | 2026-05-09 | 64 karma | Alex Gibson
- url: https://www.lesswrong.com/posts/buxBdp8NtHGgBwabv/neural-networks-learn-bloom-filters
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Trains a tiny one-layer ReLU network to output sparse top-k distributions over a vocabulary much larger than its hidden dimension. The learned input weights are near-binary hashes per token and the network behaves like a Bloom filter (hidden layer computes an approximate union indicator, logits read off linearly); a theoretical construction is given, but the mechanistic explanation of the trained network is incomplete.
- screener's follow-up note (often the screener's inference): Complete the mechanistic account, vary sparsity/dimension to find where the Bloom-filter solution breaks down, and look for similar hashing structure in real language models.
- builds on: -

## Challenge: Hand coding weights for efficient sequence memorisation
- id: `KWtchKwwnJkd4bwCi` | 2026-07-23 | 65 karma | Linda Linsefors, Lucius Bushnaq
- url: https://www.lesswrong.com/posts/KWtchKwwnJkd4bwCi/challenge-hand-coding-weights-for-efficient-sequence-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Hand-codes weights for one-layer MLPs that memorise random labels for length-2 token sequences. The number of facts stored at 90% accuracy scales roughly linearly with parameter count, like trained models, but with a worse prefactor; a hybrid (hand-coded input weights, learned output weights) narrows but does not close the gap. Poses an open challenge to find constructions that store more facts per weight.
- screener's follow-up note (often the screener's inference): Find better hand-coded constructions, and reverse-engineer what the trained MLPs actually do to close the gap - all tiny-model experiments.
- builds on: Nichani et al. (transformers store facts linear in parameter count); Bietti et al. / Cabannes et al. (associative memories); ROME / MEMIT

