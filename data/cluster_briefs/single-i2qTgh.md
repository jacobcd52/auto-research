# Cluster: Tie training can make DPO/RLHF-trained AIs generalize better

key: `single-i2qTgh` — 1 post(s); write at most 1 proposal(s).

## Tie training can make DPO/RLHF-trained AIs generalize better
- id: `i2qTghrkyY9xdcCFq` | 2026-07-06 | 54 karma | Elliott Thornley, Christian Moya Calderon, Alex Semendinger
- url: https://www.lesswrong.com/posts/i2qTghrkyY9xdcCFq/tie-training-can-make-dpo-rlhf-trained-ais-generalize-better
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Summary of an ICML paper: theorems (linear utility model) and experiments suggest DPO and RLHF make models place weight on every feature correlated with true value in training, even with no mislabelled data and infinite data. Proposed mitigation is tie training (pairs of equal true value with random or two-way labels). In an LLM experiment with Llama-3.2-1B-Instruct choosing hotels, ordinary DPO is led astray by spurious features (e.g. street numbers) OOD, while tie training improves OOD performance.
- screener's follow-up note (often the screener's inference): Test tie training on safety-relevant spurious features (sycophancy, verbosity, apparent success) and on larger models / RLHF rather than DPO.
- builds on: Spurious Correlation Learning in Preference Optimization: Mechanisms, Consequences, and Mitigation via Tie Training (ICML paper); Goal misgeneralization (https://arxiv.org/pdf/2210.01790, https://arxiv.org/pdf/2105.14111)

