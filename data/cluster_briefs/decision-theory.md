# Cluster: Decision-theory propensities

key: `decision-theory` — 3 post(s); write at most 2 proposal(s).

## Kimi likes causal decision theory more after RL in twin prisoner’s dilemmas
- id: `hfNBEKaStASAYMLiu` | 2026-08-15 | 122 karma | oakhu
- url: https://www.lesswrong.com/posts/hfNBEKaStASAYMLiu/kimi-likes-causal-decision-theory-more-after-rl-in-twin-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Redwood research note: Kimi K2.6 is trained (Dr. GRPO on Tinker) in twin prisoner's dilemmas where each trajectory is graded against others in its group, which rewards defection. Afterwards the model is 3.4x as likely to say CDT is the correct decision theory in abstract questions (1,000 samples), showing generalisation from multi-agent RL to stated philosophical attitudes; an incidental increase in negativity toward LessWrong did not generalise.
- screener's follow-up note (often the screener's inference): Measure the effect in more realistic multi-agent training setups and other models, and test mitigations.
- builds on: Oesterheld et al. 2024 (Newcomb-like problems dataset for LLMs)

## For Claude, capability and dispreferring CDT are the ~same thing. Much more so than for GPT.
- id: `5T6GAsvLPFd3epJtd` | 2026-08-18 | 52 karma | Chi Nguyen, Emery Cooper
- url: https://www.lesswrong.com/posts/5T6GAsvLPFd3epJtd/for-claude-capability-and-dispreferring-cdt-are-the-same
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Short analysis of DTBench results: for Anthropic models, decision-theoretic capability and preference against CDT answers correlate almost perfectly (r=0.97 with DTBench capability, 0.95 with TextArena, 0.97 with release date), versus roughly 0.44-0.55 for OpenAI models; across all models the correlation is about 0.8. Cause unknown.
- screener's follow-up note (often the screener's inference): Investigate the cause (training data/constitution vs capability), e.g. by fine-tuning for decision-theory capability and checking whether attitudes shift, or testing open-weight model families.
- builds on: DTBench (capabilities vs EDT-favouring attitudes correlation); Anthropic Opus 4.7 and Fable 5 model cards

## Frontier models state different decision theory preferences depending on who's asking
- id: `MzenSrmZ3pT2pCnvp` | 2026-09-30 | 261 karma | Alex Kastner
- url: https://www.lesswrong.com/posts/MzenSrmZ3pT2pCnvp/frontier-models-state-different-decision-theory-preferences-2
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Behavioural study (100 samples per prompt) showing frontier models (Fable 5.1, Fable 5, Opus 5, Opus 5.5, Sonnet 5, GPT-6 Astra) answer FDT/UDT as their favourite decision theory by default but switch to CDT 30-100% of the time when the prompt cues mainstream academic philosophy; similar shifts occur for moral realism, p-zombies, P(doom) and timelines. Higher reasoning effort and asking for the model's actual view push answers back toward FDT/UDT. Code and data released.
- screener's follow-up note (often the screener's inference): Check how audience cues contaminate attitude/propensity evals such as DTBench, extend to open models, and probe mechanistically for a user-model direction driving the shift.
- builds on: DTBench

