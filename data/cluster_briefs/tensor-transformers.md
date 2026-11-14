# Cluster: Tensor / bilinear transformers

key: `tensor-transformers` — 2 post(s); write at most 2 proposal(s).

## Tensor-Transformer Variants are Surprisingly Performant
- id: `hp9bvkiN3RzHgP9cq` | 2026-01-12 | 87 karma | Logan Riggs
- url: https://www.lesswrong.com/posts/hp9bvkiN3RzHgP9cq/tensor-transformer-variants-are-surprisingly-performant
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Trains ~500M-parameter LMs on FineWeb (fork of modded-nanoGPT) replacing MLPs with bilinear layers and softmax attention with bilinear (polynomial) attention, so the model is a tensor network. The tensor variant needed about 4% more batches to match the baseline's cross-entropy loss; the author's overall estimate, given caveats, is between 15% worse and 10% better.
- screener's follow-up note (often the screener's inference): Actually exploit the tensor structure for interpretability on these trained models (weight-based decomposition of bilinear layers/attention), and check whether the performance parity holds at other scales or under tuned hyperparameters.
- builds on: Bilinear MLPs Enable Weight-Based Mechanistic Interpretability (https://arxiv.org/abs/2410.08417); modded-nanoGPT

## If you're interpreting <1B parameter models, you should use a tensor transformer
- id: `expsAXaBgiqgitFe6` | 2026-09-02 | 54 karma | Logan Riggs
- url: https://www.lesswrong.com/posts/expsAXaBgiqgitFe6/if-you-re-interpreting-less-than-1b-parameter-models-you
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Argues that small-model interpretability research should use tensor transformers (bilinear MLPs and bilinear attention), which are claimed to be ~90% as efficient as normal transformers, close to SwiGLU-style SOTA architectures, and fully analysable with linear algebra (e.g. generalized cosine similarity over the whole network, as in the author's recent paper). The author notes he still cannot fully reverse-engineer a GPT-2-small-sized tensor transformer or even toy algorithmic tasks.
- screener's follow-up note (often the screener's inference): Train small bilinear transformers on toy algorithmic/language tasks and attempt weight-based reverse engineering; check whether results obtained on ReLU-MLP models (e.g. fine-tuning away normalization) transfer to bilinear/SwiGLU architectures.
- builds on: Author's recent tensor-transformer paper using generalized cosine similarity; https://arxiv.org/abs/2409.13710

