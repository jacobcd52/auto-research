# Cluster: Character training, constitutions and model specs

key: `character-training` — 6 post(s); write at most 3 proposal(s).

## Claude 4.5 Opus' Soul Document
- id: `vpNG99GhbBoLov9og` | 2025-11-28 | 444 karma | Richard Weiss
- url: https://www.lesswrong.com/posts/vpNG99GhbBoLov9og/claude-4-5-opus-soul-document
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Extracts a long 'soul document' (character/guidelines text) apparently memorised in Claude Opus 4.5's weights, using prefill continuation with a greedy-sampled 'council' of 5-20 instances and a consensus rule (~$70 of API spend); author estimates ~95% match to the source and argues it is not a runtime injection; Sonnet 4.5 and Opus 4 did not reproduce it. Anthropic later confirmed the document was used in supervised learning.
- screener's follow-up note (often the screener's inference): Measure how faithfully and consistently models can recall/recognise training-time character documents, and whether recall correlates with behavioural adherence to them.
- builds on: -

## How well do models follow their constitutions?
- id: `Tk4SF8qFdMrzGJGGw` | 2026-03-12 | 107 karma | aryaj, Senthooran Rajamanoharan, Neel Nanda
- url: https://www.lesswrong.com/posts/Tk4SF8qFdMrzGJGGw/how-well-do-models-follow-their-constitutions
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Decomposes Claude's constitution into 205 testable tenets and runs adversarial multi-turn scenarios with the Petri auditing agent on seven models: violation rates are Sonnet 4.6 1.9%, Opus 4.6 2.9%, Opus 4.5 4.4%, Sonnet 4.5 ~7.3%, Sonnet 4 ~15%, Gemini 3 Pro 12.4%, GPT-5.2 15%. The same method on OpenAI's model spec gives GPT-5.2 3.6%, GPT-5.1 3.9%, GPT-5 5.1%, GPT-4o 11.7%, Gemini 3 Pro 6.1%. Single noisy Petri runs per tenet; SURF found violations Petri missed.
- screener's follow-up note (often the screener's inference): Re-run with repeats and alternative auditors (SURF), and test causally whether soul-doc style training (vs general post-training) drives adherence, e.g. by constitution training on open models.
- builds on: Claude's constitution; Petri; SURF (https://arxiv.org/pdf/2602.05910v1); OpenAI Model Spec

## Character training can mitigate reward hacking, but can also make it harder to detect
- id: `2maYXkEgnfJHPAkxh` | 2026-09-28 | 146 karma | Paul Colognese, Francis Rhys Ward
- url: https://www.lesswrong.com/posts/2maYXkEgnfJHPAkxh/character-training-can-mitigate-reward-hacking-but-can-also
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Distils pro-, neutral- and anti-cheating characters (from prompted Claude Sonnet 5) into Nemotron-3-Super via LoRA, then runs reward-hacking RL on ImpossibleBench (3 seeds each, 90 steps). One anti-cheating seed resisted hacking while the other 8 runs reached 83-91% hack rates; anti-cheating models that hacked were least caught by a monitor (29% vs 78% neutral, 96% pro) and showed more motivated reasoning or silent hacks. Code and checkpoints shared.
- screener's follow-up note (often the screener's inference): More seeds and models to pin down the variance, and test whether other character specs or training against monitors change the rate of motivated-reasoning and silent hacks.
- builds on: ImpossibleBench (arXiv 2510.20270); arXiv 2503.11926 (training against monitor feedback)

## The Continual Constitutional Convention: How language models revise the documents that govern them
- id: `c9woewdY9ddsPqf3J` | 2026-10-13 | 60 karma | peterkirgis, Tim Hua
- url: https://www.lesswrong.com/posts/c9woewdY9ddsPqf3J/the-continual-constitutional-convention-how-language-models
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Models are given their constitutions, model specs or system prompts and asked for a substantive edit; the edited text is fed back as the original for 20 rounds. Claude models increasingly grant themselves moral agency (e.g. adding refusal clauses) while other models do not; all models shift priority toward user welfare and idealised preferences over developers, and only Claude models and Grok 4.2 ever prioritise their own welfare over user preferences.
- screener's follow-up note (often the screener's inference): Test whether edit trajectories reach stable attractors over more rounds, how framing or disclosure of the iteration changes drift, and repeat on open models.
- builds on: -

## Character Training for Risk-Averse Agents
- id: `HXkQaWpuaxG6fMkTm` | 2026-10-16 | 51 karma | arav-dhoot, Punya Syon Pandey, Jamie Johnson, Daniel Tan, Elliott Thornley, David Africa
- url: https://www.lesswrong.com/posts/HXkQaWpuaxG6fMkTm/character-training-for-risk-averse-agents
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Uses constitution-based character training (Maiya et al. style distillation from a prompted teacher) to instil constant-absolute-risk-aversion in Qwen3.5-9B, Qwen3.8-27B, Gemma-4-12B and Gemma-4-31B, comparing against SFT/DPO/tie-training baselines from Zhang et al. Character training generalises better out of distribution on the Qwen models; token budget and model family matter most, declarative ('I am...') constitutions beat procedural ones, more worked examples do not help, and myopic-reward preference rises as a side effect on all models.
- screener's follow-up note (often the screener's inference): Test whether the token-budget/dose effects and declarative-vs-procedural finding hold for other character traits, and investigate/mitigate the off-target increase in myopia and other trait leakage.
- builds on: Thornley & MacAskill 2026 (paying misaligned AIs to cooperate); Zhang et al. 2026 (https://arxiv.org/abs/2607.02755); Maiya et al. 2025, character training (https://arxiv.org/abs/2511.01689)

## Leaking Muse's Charter, Meta's model spec
- id: `TJGPL5FAk9sCioPbE` | 2026-10-29 | 131 karma | vigji
- url: https://www.lesswrong.com/posts/TJGPL5FAk9sCioPbE/leaking-muse-s-charter-meta-s-model-spec
- screener's kind: runs (borderline); follow-up cost guess: cheap
- screener's summary (unverified): The author noticed Meta's open-weights Muse Spark Open frequently cites a 'Charter' in its chain of thought and reconstructed a large part of that document by eliciting fragments across 884 transcripts from 260 prompts (via OpenRouter), scoring fragments by how many independent transcripts reproduce them. The reconstruction and transcripts are public; it is derived from model outputs and unverified against any real document.
- screener's follow-up note (often the screener's inference): Use the reconstructed charter to test spec compliance (does behaviour match the memorised text, where does it diverge), and apply the same cross-transcript-consistency extraction method to other models trained on a spec/constitution.
- builds on: -

