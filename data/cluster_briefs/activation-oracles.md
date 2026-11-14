# Cluster: Activation oracles

key: `activation-oracles` — 5 post(s); write at most 3 proposal(s).

## Activation Oracles: Training and Evaluating LLMs as General-Purpose Activation Explainers
- id: `rwoEz3bA9ekxkabc7` | 2025-12-18 | 155 karma | Sam Marks, Adam Karvonen, James Chua, Subhash Kantamneni, Euan Ong, Julian Minder, Clément Dumas, Owain_Evans
- url: https://www.lesswrong.com/posts/rwoEz3bA9ekxkabc7/activation-oracles-training-and-evaluating-llms-as-general
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Trains LLMs to take activations as input and answer natural-language questions about them, on a diverse task mix. The oracles generalise out of distribution: they beat other methods on 2/3 secret-keeping auditing evals (3/3 among white-box methods), match specialised baselines at describing emergently misaligned fine-tunes from activation differences, and improve with more training datasets. Paper and Colab released.
- screener's follow-up note (often the screener's inference): Apply released oracles to new auditing targets (other model organisms, sandbagging, eval awareness), test failure modes/confabulation, and scale training-task diversity.
- builds on: LatentQA; Secret-keeping / hidden-knowledge auditing benchmarks; Emergent Misalignment

## Scalable End-to-End Interpretability
- id: `qkhwh4AdG7kXgELCD` | 2025-12-18 | 124 karma | jsteinhardt
- url: https://www.lesswrong.com/posts/qkhwh4AdG7kXgELCD/scalable-end-to-end-interpretability
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Part position piece, part linkpost for Predictive Concept Decoders: proposes training AI assistants end-to-end on tasks that require understanding a network's internals (e.g. predicting behaviour from activations), with a communication bottleneck so the result stays human-readable. In PCDs an encoder compresses activations into a sparse set of concepts and a decoder that sees only those answers questions, pretrained on (activation, output) pairs from web text.
- screener's follow-up note (often the screener's inference): Compare PCD-style bottlenecked decoders with activation oracles and SAEs on auditing tasks; try other end-to-end objectives such as predicting intervention results.
- builds on: Predictive Concept Decoders (https://arxiv.org/abs/2512.15712); A Pragmatic Vision for Interpretability; An Ambitious Vision for Interpretability

## Current activation oracles are hard to use
- id: `LXQBcztrWKhtcgQfJ` | 2026-03-03 | 84 karma | aryaj, Senthooran Rajamanoharan, Neel Nanda
- url: https://www.lesswrong.com/posts/LXQBcztrWKhtcgQfJ/current-activation-oracles-are-hard-to-use
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Tests activation oracles (Karvonen et al.) on realistic safety-relevant tasks and finds them hard to use and evaluate: ~49% of responses are generic, they hallucinate, and text inversion plus the AO's own reasoning confound correct answers (running without activations gave comparable or better answers in a Chinese-models experiment). On tasks where text inversion cannot help they fail: number prediction, sycophancy detection on Scruples with Qwen (AUC ~0.55 vs 0.77 for a dense probe), identifying the source of confusion (1/54); backtracking results were ambiguous-to-negative.
- screener's follow-up note (often the screener's inference): Train AOs explicitly against vagueness/hallucination and build evaluations that control for text inversion and the AO's own knowledge (e.g. no-activation baselines).
- builds on: Activation Oracles (Karvonen et al., 2025); https://arxiv.org/abs/2510.13900v1

## Cycle-Consistent Activation Oracles
- id: `Nf2sKaNNdxE2ssxbp` | 2026-03-12 | 55 karma | slavachalnev
- url: https://www.lesswrong.com/posts/Nf2sKaNNdxE2ssxbp/cycle-consistent-activation-oracles-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Trains an AO-style LoRA decoder (activation -> text) and a LoRA encoder (text -> activation) on middle-layer Qwen3-8B activations, with a supervised warm-up (LatentQA + token prediction) followed by cycle-consistency training via GRPO. Outputs capture topic and local context but are lossy guesses about surrounding text rather than faithful descriptions, and linear probes beat the text route on classification tasks. Interim report.
- screener's follow-up note (often the screener's inference): Change the objective so that cycle consistency rewards faithful descriptions rather than context guesses (e.g. constrain decoder reasoning, richer bottleneck) and evaluate against probes.
- builds on: Activation Oracles (Karvonen et al., 2025); LatentQA (https://arxiv.org/abs/2412.08686)

## Building Better Activation Oracles
- id: `heXwuDRfbQQgB5JLP` | 2026-06-04 | 69 karma | ceselder, Jan Bauer, Niclas Luick, Adam Karvonen, Neel Nanda
- url: https://www.lesswrong.com/posts/heXwuDRfbQQgB5JLP/building-better-activation-oracles
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): MATS sprint improving Activation Oracle training: on-policy rollouts, a new conversational dataset of questions about unarticulated completions (replacing LatentQA), feeding multiple layers, and a tweak to the injection formula; releases AObench, an evaluation suite targeting hallucination, vagueness and text-inversion confounds. Capability gains are marginal but usability improves substantially; models and code are open-sourced (Qwen3-8B AO among them).
- screener's follow-up note (often the screener's inference): Authors list future work such as increasing corpus diversity on the unsupervised task; open question is whether AOs extract information beyond what a text-only (text inversion) baseline could infer.
- builds on: Karvonen et al., Activation Oracles; Current activation oracles are hard to use (https://www.lesswrong.com/posts/LXQBcztrWKhtcgQfJ/current-activation-oracles-are-hard-to-use); LatentQA (arXiv 2412.08686)

