# Cluster: CoT controllability evals

key: `cot-controllability` — 3 post(s); write at most 2 proposal(s).

## Reasoning Models Struggle to Control Their Chains of Thought
- id: `qTH9QrwJjPDWKQfDG` | 2026-03-05 | 76 karma | Yueh Han "John" Chen, robert mccarthy, Bruce W. Lee, Tomek Korbak
- url: https://www.lesswrong.com/posts/qTH9QrwJjPDWKQfDG/reasoning-models-struggle-to-control-their-chains-of-thought
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces CoT-Control, 14,076 tasks (from GPQA, SWE-Bench, etc.) paired with instructions constraining what may appear in the reasoning trace, and evaluates 13 frontier models. CoT controllability is far below output controllability (Claude Sonnet 4.5: 2.7% vs 61.9%); it rises with model size but falls with more RL reasoning training (shown across OLMo-3-7B-RL-Zero-Math checkpoints and 4 families), more reasoning effort and harder tasks; telling models they are monitored adds up to ~4 points and adversarially optimised prompts transfer poorly.
- screener's follow-up note (often the screener's inference): Explain mechanistically why controllability is low and falls with RL training; track it on new and open-weight reasoning models and test whether fine-tuning can raise it.
- builds on: CoT monitoring (https://arxiv.org/abs/2503.11926); Chain of Thought Monitorability (https://arxiv.org/abs/2507.11473); https://arxiv.org/abs/2603.05706

## Prompted CoT Early Exit Undermines the Monitoring Benefits of CoT Uncontrollability
- id: `BuAPifQmHf24xB29n` | 2026-04-17 | 72 karma | Elle Najt, Asa Cooper Stickland, Xander Davies
- url: https://www.lesswrong.com/posts/BuAPifQmHf24xB29n/prompted-cot-early-exit-undermines-the-monitoring-benefits
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Shows Claude Opus 4.6, GPT-5.4 and Gemini 3.1 Pro can be prompted to 'early exit' their CoT (blank it, or fill it with a short poem) and move reasoning into the stylistically controllable response channel. Models keep most reasoning ability (4-8pp accuracy cost vs 20-29pp for no reasoning) while satisfying the control conditions, undermining the reassurance from low CoT controllability; the authors note they only show prompted capability, not that models would do this spontaneously. Code released.
- screener's follow-up note (often the screener's inference): Test whether models can discover or decide to use early-exit strategies autonomously, whether monitors over CoT plus response close the gap, and replicate on open-weight reasoning models where full CoT is visible.
- builds on: Yueh-Han et al. 2026 (CoT controllability)

## CoT controllability evals seem very under-elicited
- id: `BbP2wCyDGdPWJ7PwP` | 2026-09-11 | 78 karma | Jozdien
- url: https://www.lesswrong.com/posts/BbP2wCyDGdPWJ7PwP/cot-controllability-evals-seem-very-under-elicited
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Has Claude Opus 4.6 iterate on prompt templates for the CoTControl eval (obeying formatting constraints inside CoT). Better prompts raise open-source models' scores ~2-3x or more (e.g. GPT-OSS-120B from 5.5% to 15%), suggesting reported low controllability numbers in system cards are under-elicited.
- screener's follow-up note (often the screener's inference): Push elicitation further: automated prompt optimisation and training-based elicitation (fine-tuning for CoT control) on open reasoning models, to estimate an upper bound on controllability.
- builds on: CoTControl eval; Fable system card §6.5.5.1 (UK AISI note on prompt sensitivity)

