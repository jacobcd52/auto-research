# Cluster: Self-prediction and self-explanation

key: `self-prediction` — 5 post(s); write at most 3 proposal(s).

## LLMs struggle to verbalize their internal reasoning
- id: `dFRFxhaJkf9dE6Jfy` | 2026-02-14 | 50 karma | Emil Ryd
- url: https://www.lesswrong.com/posts/dFRFxhaJkf9dE6Jfy/llms-struggle-to-verbalize-their-internal-reasoning
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Fine-tunes Llama 3.1 8B and gpt-oss-20b (SFT, plus GRPO RL with reasoning on a grid-world game) to solve tasks in a single forward pass (increasing sort, subtracted two-hop table lookup, custom 'Hot Square Capture' game, chess puzzles), then asks them to explain their moves/the rules, scored by an LLM judge. Models hallucinate incorrect reasoning; only the simple sorting rule is verbalized (unreliably, possibly because it is the most likely guess), and RL-trained models reason illegibly and still cannot state the rules.
- screener's follow-up note (often the screener's inference): Test whether introspection/self-explanation training, larger models, or other task families enable verbalization of learned single-forward-pass computations; use the subtracted-lookup task's verifiable intermediates as a benchmark.
- builds on: Tell me about yourself: LLMs are aware of their learned behaviors (https://arxiv.org/abs/2501.11120); Emergent Introspective Awareness in LLMs (https://transformer-circuits.pub/2025/introspection/index.html); https://arxiv.org/pdf/2505.17120v1

## Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments
- id: `ExB6KYDcznaFS72eT` | 2026-08-21 | 75 karma | Adam Karvonen, Euan Ong, Subhash Kantamneni, Sam Marks
- url: https://www.lesswrong.com/posts/ExB6KYDcznaFS72eT/evaluating-explanations-of-llm-behavior-in-the-wild-with
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces CHIVE, an agentic pipeline that samples a target model, flags unexpected behaviours, and investigates each with 5-15 counterfactual prompt edits, producing verified labels on whether an edit changes the behaviour. As an evaluation, predictor agents given activation-reading tools (activation oracle, natural-language autoencoder, SAE) predict counterfactual outcomes no better than agents reading only the transcript; as training data, models trained to predict effects of prompt edits on their own behaviour generalise to held-out settings. Paper and code released.
- screener's follow-up note (often the screener's inference): Evaluate other interpretability tools or better tool-use scaffolds on the CHIVE benchmark, and test whether self-prediction training improves explanation faithfulness or introspection more broadly.
- builds on: Activation oracles; Natural-language autoencoders; Counterfactual simulatability literature

## Training Models to Predict and Explain Their In-the-Wild Behavior
- id: `YyAMz52wDxnLhwvWL` | 2026-09-04 | 50 karma | Adam Karvonen, Subhash Kantamneni, Euan Ong, Sam Marks
- url: https://www.lesswrong.com/posts/YyAMz52wDxnLhwvWL/training-models-to-predict-and-explain-their-in-the-wild
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Uses CHIVE-generated investigations (surprising in-the-wild behaviours with counterfactual-prompt-grounded explanations) to fine-tune models on two targets: binary counterfactual prediction ('would this edit change your behaviour?') and open-ended self-explanation. Counterfactual-prediction training generalizes to held-out hint datasets (MMLU hints, AITA opinions) for every model tested and beats the open-ended target; open-ended training generalized notably in only one model/eval combination (Qwen3.5-397B). No privileged access: Llama-3.1-8B trained on the same data predicts Qwen3-8B's behaviour as well as Qwen3-8B does.
- screener's follow-up note (often the screener's inference): Look for training targets or settings where self-prediction does beat cross-model prediction; test generalization to further held-out behaviours (code and data are released).
- builds on: CHIVE (https://alignment.anthropic.com/2026/chive/); Binder et al. 2024 (Looking Inward: privileged access); Hase et al. 2026 (https://arxiv.org/abs/2602.20710); Turpin et al. 2023 (https://arxiv.org/abs/2305.04388)

## Modern LLMs have tiny GPTs hidden inside them
- id: `Pwc4YffTQvNRF3dbB` | 2026-09-22 | 53 karma | invertedpassion
- url: https://www.lesswrong.com/posts/Pwc4YffTQvNRF3dbB/modern-llms-have-tiny-gpts-hidden-inside-them
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Quick exploratory study: GPT2-medium generates text from 12 post-cutoff headlines, then a Qwen3 base model (4B) continues the GPT-2 prefix. Across overlap metrics, Qwen's continuation of GPT-2 text overlapped more with GPT-2's own hidden continuation than with Qwen's natural continuation, and Qwen assigned earlier years to GPT-2-generated text; author flags it as not conclusive.
- screener's follow-up note (often the screener's inference): Scale up the sample (only 12 headlines), add controls for prefix-induced style copying versus genuine modelling of the weaker LLM, and test other model pairs and whether models can predict their own or sibling models' outputs.
- builds on: -

## Evidence that the ‘talker’ has introspective access to the ‘doer’
- id: `kTg5FrABJYpYrP8ps` | 2026-11-12 | 106 karma | Francis Rhys Ward
- url: https://www.lesswrong.com/posts/kTg5FrABJYpYrP8ps/evidence-that-the-talker-has-introspective-access-to-the
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Trains Qwen3.8-27B to predict its own (non-thinking) behaviour in a chat setting, following Binder et al. Self-prediction beats controls including a stronger model (Kimi K2.6) predicting Qwen, transfers to predicting whether it will cheat on impossible coding tasks, and tracks behaviour change when the model is subsequently RL-trained to cheat.
- screener's follow-up note (often the screener's inference): Repeat on MoE and larger models and other behaviours; test whether trained self-prediction can serve as a cheap propensity probe/monitor for misbehaviour in agentic settings.
- builds on: Binder et al., Looking Inward: language models can learn about themselves by introspection; Conditional misalignment (https://arxiv.org/abs/2604.25891); ImpossibleBench

