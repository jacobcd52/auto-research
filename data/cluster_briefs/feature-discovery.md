# Cluster: SAEs and feature-discovery alternatives

key: `feature-discovery` — 4 post(s); write at most 2 proposal(s).

## Announcing Gemma Scope 2
- id: `YQro5LyYjDzZrBCdb` | 2025-12-22 | 96 karma | CallumMcDougall, Arthur Conmy, János Kramár, Tom Lieberum, Senthooran Rajamanoharan, Neel Nanda
- url: https://www.lesswrong.com/posts/YQro5LyYjDzZrBCdb/announcing-gemma-scope-2
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): GDM releases Gemma Scope 2: JumpReLU SAEs (residual, MLP-out, attention-out) and MLP transcoders for every layer of all ten Gemma 3 models (270m-27b, PT and IT), plus cross-layer transcoders and weakly causal crosscoders, trained with Matryoshka loss and a frequency penalty. It is a tooling release rather than a study with findings.
- screener's follow-up note (often the screener's inference): Enables cheap follow-ups: feature-based auditing, steering or attribution of safety-relevant behaviours in Gemma 3, and SAE-quality evaluations.
- builds on: Gemma Scope (original release)

## Elementary Condensation
- id: `JKexLeze9kNhCYYzT` | 2026-04-08 | 51 karma | Jan
- url: https://www.lesswrong.com/posts/JKexLeze9kNhCYYzT/elementary-condensation
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Explains Eisenstat's condensation theory of concepts and tries to operationalise its score on neural-network features. Using a planted-concept toy, a small transformer on TinyStories openings and an induction task, SAE, PCA and random-projection decompositions are compared by condensation score: SAEs win when shared concepts are rare binary flags (toy, TinyStories) while PCA wins on induction where the shared concept is a 50-way categorical; the author stresses limitations (binarising features, scope assignment).
- screener's follow-up note (often the screener's inference): Scale the score to real LLMs and standard SAEs, find better ways to estimate mutual information/scope from continuous features, and test whether the score tracks other SAE quality metrics.
- builds on: Condensation: a theory of concepts (Eisenstat 2025); Natural abstractions hypothesis (Wentworth)

## An Introduction to Exemplar Partitioning for Mechanistic Interpretability
- id: `RroeHBSkBXXDsrryq` | 2026-05-16 | 70 karma | Jessica Rumbelow
- url: https://www.lesswrong.com/posts/RroeHBSkBXXDsrryq/an-introduction-to-exemplar-partitioning-for-mechanistic-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces Exemplar Partitioning: cover the activation manifold with observed exemplar activations at a calibrated resolution (one hyperparameter, single streaming pass, centred-cosine distance) rather than training an SAE; demonstrated on Gemma-2-2B. Headline: on AxBench latent concept detection at Gemma-2-2B-it layer 20, EP reaches mean AUROC 0.881 over 500 concepts, reported as an improvement over baselines. Paper: arXiv 2605.14347.
- screener's follow-up note (often the screener's inference): Compare alternative distance metrics (as a test of the linear representation hypothesis), study relations between neighbouring regions, and benchmark against SAEs on steering and other downstream tasks.
- builds on: AxBench; Sparse autoencoders

## In search of natural features
- id: `SNAKJuN8FdoEaWeFC` | 2026-08-23 | 56 karma | Dmitry Vaintrob
- url: https://www.lesswrong.com/posts/SNAKJuN8FdoEaWeFC/in-search-of-natural-features
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Preliminary experiments (run with Claude Code) on gpt2-small without LayerNorm, mostly the layer-6 MLP, defining a 'channel amplification' (error-correction) score for any activation direction: how much the MLP amplifies large components vs attenuates small ones, like a noise gate. Random directions score about zero, real activations higher, SAE features higher still (coarser features highest), and gradient ascent on the score flows directions to attractor 'ur-features'. Author asks for criticism and bug-finding; repo released.
- screener's follow-up note (often the screener's inference): Replicate and stress-test for bugs, extend to other layers and larger models, and compare amp-score maxima with SAE/transcoder features.
- builds on: Stefan Heimersheim & Francisco Ferreira's work on error-correction as a naturalness signal; Adler & Shavit, computation in superposition; Hanni, Mendel, Vaintrob, Chan: computation in superposition

