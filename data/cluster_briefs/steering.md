# Cluster: Steering reliability

key: `steering` — 2 post(s); write at most 2 proposal(s).

## Steering Might Stop Working Soon
- id: `fuzfbz8TbuLcskGCx` | 2026-04-05 | 68 karma | J Bostock
- url: https://www.lesswrong.com/posts/fuzfbz8TbuLcskGCx/steering-might-stop-working-soon
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Argues single-vector steering will fail on more capable models (steering resistance, steering detection, narrowing window between 'too weak' and 'incoherent'). A quick experiment sweeps contrastive-pair steering strength across Gemma 3 model sizes on three factual questions (steering toward a wrong answer) plus a small coding benchmark: the viable window where the model gives the steered wrong answer without capability collapse shrinks with model size, and the largest models became incoherent before they could be steered. Code on GitHub.
- screener's follow-up note (often the screener's inference): Author wants better experiments on steering resistance in larger models: replicate with more questions/vectors/layers and model families, steer against inferred beliefs (e.g. eval awareness) rather than known facts, and compare SAE-feature ablation or other methods.
- builds on: Steering evaluation-aware models to act like they are deployed; Steering resistance in LLMs (arXiv 2602.06941); Lindsey 2025 introspection; Steering awareness fine-tuning (arXiv 2511.21399)

## A conceptor by any other name
- id: `9aZYJinAyxequjQbn` | 2026-07-07 | 60 karma | Keenan Pepper
- url: https://www.lesswrong.com/posts/9aZYJinAyxequjQbn/a-conceptor-by-any-other-name
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Explainer with no new experiments: argues that conceptors (regularised soft-projection matrices C = R(R + a^-2 I)^-1 built from concept activation vectors) are an underrated tool for intervening on a concept subspace, and collects equivalent names (Wiener filter, ridge shrinkage, fantope element, etc.). Motivating example is 'persona transplantation' using the ~275 Assistant Axis role vectors, where a conceptor should beat full-subspace or top-k PCA interventions.
- screener's follow-up note (often the screener's inference): Empirically compare conceptor-based persona/concept steering or ablation against mean-difference steering, full-subspace and top-k PCA projection on an open model (trait transfer vs. collateral damage such as topic/language drift).
- builds on: Conceptors for Semantic Steering (Triantafyllopoulos et al.); Jaeger 2014, conceptors; The Assistant Axis

