# Cluster: Belief-state geometry in transformers

key: `belief-geometry` — 2 post(s); write at most 2 proposal(s).

## The Geometry of Nonergodic Composition
- id: `JfJ4WTRHmooPBWRFv` | 2026-09-10 | 87 karma | Adam Shai, Kyle Ray, Paul Riechers
- url: https://www.lesswrong.com/posts/JfJ4WTRHmooPBWRFv/the-geometry-of-nonergodic-composition
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Derives the belief geometry implied by next-token prediction over nonergodic data (a mixture of sources): per-component belief simplices scaled by the posterior weight of each component ('telescoping cones'). Small transformers trained on a nonergodic composition of two Mess3 generators linearly embed this geometry in the residual stream (held-out R^2 ~0.985 vs ~0.45 for an untrained network).
- screener's follow-up note (often the screener's inference): Test the predicted factored-subspace structure on compositions with internal factorization and with more components; look for per-source component geometry in real LLM activations.
- builds on: Simplex's earlier belief-state geometry work (Transformers represent belief state geometry in their residual stream)

## Generalized belief states in transformers
- id: `4f9p7brLdnTMFuwfB` | 2026-10-31 | 74 karma | Artemy Kolchinsky
- url: https://www.lesswrong.com/posts/4f9p7brLdnTMFuwfB/generalized-belief-states-in-transformers-1
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Proposes 'generalized belief states' (sufficient, recursively updatable, low-dimensional statistics of the past) as a way to define, decode and manipulate representations in sequence models, and illustrates it with a transformer trained on a simple HMM-generated process (an RRXOR-style process), where the KV cache plays a key role. Largely theoretical with a toy-model demonstration.
- screener's follow-up note (often the screener's inference): Apply the decoding/intervention method to other toy processes and to larger or naturally trained models, and compare directly with the residual-stream belief-geometry probes of Shai et al.
- builds on: Transformers Represent Belief State Geometry in their Residual Stream (Shai et al. 2024, https://arxiv.org/abs/2405.15943)

