# Cluster: Natural language autoencoders

key: `nla` — 4 post(s); write at most 2 proposal(s).

## Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations
- id: `oeYesesaxjzMAktCM` | 2026-05-07 | 209 karma | Subhash Kantamneni, kitft, Euan Ong, Sam Marks
- url: https://www.lesswrong.com/posts/oeYesesaxjzMAktCM/natural-language-autoencoders-produce-unsupervised
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Introduces Natural Language Autoencoders: an activation verbalizer LLM maps a residual-stream activation to text and an activation reconstructor maps it back, trained jointly with RL on reconstruction. Explanations become more informative over training; NLAs surfaced unverbalised evaluation awareness in the Claude Opus 4.6 pre-deployment audit, and NLA-equipped agents beat baselines on an automated auditing benchmark. Training code and trained NLAs for open models are released.
- screener's follow-up note (often the screener's inference): Use the released open-model NLAs to test faithfulness (do explanations predict causal interventions?), compare with SAEs/activation oracles, and apply them to open model organisms.
- builds on: -

## Can activation verbalizers surface an internal chain of thought?
- id: `QQQAcKuWK6k98FivY` | 2026-06-07 | 125 karma | oakhu, ryan_greenblatt
- url: https://www.lesswrong.com/posts/QQQAcKuWK6k98FivY/can-activation-verbalizers-surface-an-internal-chain-of-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces an eval for activation verbalizers: run the target model no-CoT on ~900 easy competition math problems and check whether verbalizing the last-position activation surfaces solution methods and intermediate calculations. Applied to open-weight NLAs for Qwen2.5-7B, Gemma-3-27B and Llama-3.3-70B (plus a Qwen3-8B activation oracle), the answer is 'possibly, but definitely not reliably'; NLA reconstruction is poor (for Qwen a mean-direction baseline reconstructs better than the NLA).
- screener's follow-up note (often the screener's inference): Train better NLAs/AVs and re-run the eval; test verbalizations at other positions/layers and whether surfaced intermediate values are causally used (e.g. via patching).
- builds on: Measuring no-CoT math time horizon (single forward pass) (https://www.lesswrong.com/posts/Ty5Bmg7P6Tciy2uj2/measuring-no-cot-math-time-horizon-single-forward-pass); Recent LLMs can use filler tokens or problem repeats (https://www.lesswrong.com/posts/NYzYJ2WoB74E6uj9L/recent-llms-can-use-filler-tokens-or-problem-repeats-to); Natural language autoencoders (open-weight NLAs, kitft); Building Better Activation Oracles

## NLA explanations can be shortened without harming reconstruction
- id: `NazprRfWJ4qkwcSro` | 2026-06-22 | 56 karma | loops
- url: https://www.lesswrong.com/posts/NazprRfWJ4qkwcSro/nla-explanations-can-be-shortened-without-harming
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Trains Qwen3-8B natural language autoencoders with a length penalty on the RL reward: lambda=0.002 shortens explanations ~40% for only -0.015 FVE, and lambda=0.001 uses 28% fewer tokens with FVE essentially unchanged (+0.007); larger penalties push FVE below the warm-start. Suggests much of NLA explanation text is not needed for reconstruction.
- screener's follow-up note (often the screener's inference): Disentangle terser wording from dropped content (e.g. paraphrase/ablation of explanation segments), and check whether shortened explanations are more or less faithful/useful on downstream evals.
- builds on: Natural language autoencoders paper/blog post

## How robust are natural language autoencoders to initialization?
- id: `LQXWiF8PyJ5ojNsEv` | 2026-07-10 | 82 karma | michaelzhang, TurnTrout
- url: https://www.lesswrong.com/posts/LQXWiF8PyJ5ojNsEv/how-robust-are-natural-language-autoencoders-to
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): MATS (team shard) tests how much NLA outputs depend on the Claude-written guesses used to initialise the verbaliser, on Qwen2.5-7B. NLAs initialised on entirely implausible statements reach nearly the same reconstruction accuracy as normal ones while emitting 99.3% implausible statements, and plausibility of normally-initialised NLAs falls from 21% to 7.6% over RL. A corrigendum notes the original runs had no KL penalty due to a bug; re-runs with KL 0.01 made NLAs even less robust to initialisation (injected 'Carthage' statements persisted).
- screener's follow-up note (often the screener's inference): Test whether results scale to larger models/NLAs, and whether alternative objectives or initialisations make NLA explanations track the model's actual computation rather than the initial guesses.
- builds on: Natural language autoencoders (Fraser-Taliente et al. 2026, Anthropic; Slava Chalnev)

