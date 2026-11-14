# Cluster: CoT analysis methods and benchmarks

key: `cot-analysis-tools` — 2 post(s); write at most 2 proposal(s).

## Global CoT Analysis: Initial attempts to uncover patterns across many chains of thought
- id: `q9g9zuudd3Pvw2cbj` | 2026-01-13 | 52 karma | Riya Tyagi, daria, Arthur Conmy, Neel Nanda
- url: https://www.lesswrong.com/posts/q9g9zuudd3Pvw2cbj/global-cot-analysis-initial-attempts-to-uncover-patterns-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces two methods for analysing a collection of CoTs from a fixed model on a fixed prompt: semantic step clustering (cluster similar sentences across rollouts into a reasoning graph) and algorithmic step clustering (a coarser graph of solution strategies). Graphs are built from e.g. 100-150 rollouts of gpt-oss-20b and Claude Sonnet 4.5 (including an eval-awareness prompt); the semantic graph predicts the model's final output from a partial CoT better than naive baselines, though imperfectly, and algorithm graphs are sanity-checked on problems with known strategies.
- screener's follow-up note (often the screener's inference): Authors say finding downstream tasks to test such methods is a priority; obvious follow-ups are applying the graphs to safety-relevant prompts (reward hacking, eval awareness) to predict or steer outcomes, and extending beyond a single fixed prompt.
- builds on: Thought Anchors; Thought Branches

## Test your best methods on our hard CoT interp tasks
- id: `tDJWZLQNN7poqCwKa` | 2026-03-26 | 59 karma | daria, Riya Tyagi, Josh Engels, Neel Nanda
- url: https://www.lesswrong.com/posts/tDJWZLQNN7poqCwKa/test-your-best-methods-on-our-hard-cot-interp-tasks
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Open-sources nine objective CoT-analysis tasks (predicting future actions such as reasoning termination or Gemma self-deletion, detecting the effect of interventions such as sycophancy or a hint, identifying distributional properties of a rollout), each with in-distribution and OOD test sets, on which a black-box GPT-5.2 monitor falls short OOD. Baselines: linear/attention/SAE probes and TF-IDF often beat zero-shot and few-shot LLM monitors OOD across the 7 main tasks (with the caveat of only 7 tasks).
- screener's follow-up note (often the screener's inference): Explicit invitation to test better CoT-interpretability methods on the benchmark (e.g. activation oracles, improved probes, trained monitors) and beat the baselines OOD.
- builds on: -

