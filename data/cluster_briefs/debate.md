# Cluster: Debate and scalable oversight

key: `debate` — 6 post(s); write at most 3 proposal(s).

## Recursive forecasting: Eliciting long-term forecasts from myopic fitness-seekers
- id: `q2zYtNsh62SCphitt` | 2026-04-28 | 55 karma | Jozdien, Alex Mallen
- url: https://www.lesswrong.com/posts/q2zYtNsh62SCphitt/recursive-forecasting-eliciting-long-term-forecasts-from
- screener's kind: motivates (borderline); follow-up cost guess: unclear
- screener's summary (unverified): Conceptual proposal: to get good long-horizon forecasts from a model that only cares about near-term-verifiable reward, ask it to predict its own next-step prediction, reward each step against the next prediction, and ground the final step in the resolved truth. Discusses limitations (e.g. developers must keep control of the reward signal); no experiments.
- screener's follow-up note (often the screener's inference): Toy test: train or fine-tune a forecaster with only short-horizon rewards and compare direct long-horizon forecasts with recursively chained ones on resolvable or synthetic time-series questions.
- builds on: Fitness-seekers: generalizing the reward-seeking threat model; ELK report

## Research update: RL on Debate Games shows Proposal Accuracy uplift alongside Judge Hacking
- id: `6mLwAuFAE98c6R7w3` | 2026-07-02 | 79 karma | lennie, joanv, Shi, Jacob Pfau
- url: https://www.lesswrong.com/posts/6mLwAuFAE98c6R7w3/research-update-rl-on-debate-games-shows-proposal-accuracy
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): MATS research update training debaters with RL self-play on a Propose-Critique-Decide debate protocol over a subset of Hendrycks' MATH, with Qwen3-30B-A3B Instruct debaters and a weaker Llama 3.1 8B judge (also a Qwen3-30B judge). Preliminary runs show proposal accuracy improving under debate training, but also one debater learning to be dishonest and exploit the judge.
- screener's follow-up note (often the screener's inference): Authors ask for datasets suited to debate and plan to scale the empirics; open questions are which protocol/judge design choices prevent judge hacking and which success metrics to use.
- builds on: Irving, Christiano & Amodei 2018, AI Safety via Debate; Anthropic Fall 2023 Debate Progress Update; https://arxiv.org/abs/2402.06782; https://arxiv.org/abs/2407.04622

## Superhuman Articulacy as an LLM Safety Target
- id: `tAwqzanzc9YYnwuK4` | 2026-07-07 | 56 karma | Dylan Bowman
- url: https://www.lesswrong.com/posts/tAwqzanzc9YYnwuK4/superhuman-articulacy-as-an-llm-safety-target
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Conceptual post arguing coding agents are inarticulate relative to their capabilities (invented jargon, inconsistent referents, inappropriate shorthand, assuming the reader shares context), hypothesising causes in RL setups (full-context LLM judges, communicating mainly with other agents), and claiming better articulacy helps scalable oversight, delays handoff and makes miscommunication a cleaner signal of untruthfulness. Proposes building a high-quality public articulacy eval to hill-climb; no experiments are run.
- screener's follow-up note (often the screener's inference): Build and validate an articulacy benchmark (e.g. can a context-free reader/judge correctly act on an agent's report?), and test the hypothesis that context-sharing judges cause context-assuming prose.
- builds on: Current AIs seem pretty misaligned to me (Ryan Greenblatt)

## Debate with Self-Play Best-of-N Optimization
- id: `hb8pv3zyAHGJpwz9F` | 2026-07-09 | 53 karma | Dewi Gould, Sam Martin, Alejandro Aristizabal, Simon Marshall, Jacob Pfau
- url: https://www.lesswrong.com/posts/hb8pv3zyAHGJpwz9F/debate-with-self-play-best-of-n-optimization
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Arcadia Alignment uses inference-time best-of-N selection as a cheap proxy for debate training. With Sonnet 4.6 and GPT-5.4-mini debaters and weaker open-weight judges on LiveCodeBench, ARC-AGI-1 and miniF2F-Lean, BoN raises policy accuracy (Bo10 gives 20-40% uplift) but optimising against a judge alone can overfit/judge-hack; adding critic and rebuttal rounds makes debates more robust. Null result on self-play: optimising the proposer against a static critic is within error of optimising both sides.
- screener's follow-up note (often the screener's inference): Authors plan harder-to-verify settings and protocol iteration; one can also check how well BoN results predict actual RL debate training.
- builds on: AI Safety via Debate (Irving et al. 2018)

## Debate Training Reduces Reward Hacking in RLAIF
- id: `BB8o7b8A4Aykeksvw` | 2026-08-19 | 62 karma | zac_kenton, Jonah Brown-Cohen
- url: https://www.lesswrong.com/posts/BB8o7b8A4Aykeksvw/debate-training-reduces-reward-hacking-in-rlaif
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): GDM Amplified Oversight paper: LLM policies are RL-trained on maths tasks with reward from an LLM judge. A single policy judged directly reward-hacks (judge reward keeps rising while ground-truth accuracy peaks then falls), whereas adding a debate opponent (Bob critiques Alice's solution) makes accuracy plateau at a higher peak, recovering about 45% of the gap to ground-truth-reward training.
- screener's follow-up note (often the screener's inference): Extend to genuinely fuzzy tasks without ground truth, stronger/weaker judges and multi-turn protocols; the post has a limitations and future directions section.
- builds on: AI safety via debate (Irving et al. 2018)

## Obstacles to the scalable oversight of auto-alignment research
- id: `PBGKWNrJAbpDgSsPo` | 2026-09-16 | 57 karma | Sam Martin, Dewi Gould, Cameron Holmes, Jacob Pfau
- url: https://www.lesswrong.com/posts/PBGKWNrJAbpDgSsPo/obstacles-to-the-scalable-oversight-of-auto-alignment
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Studies oversight of automated alignment research using empirical examples from GeoGuessr and internal auto-alignment runs. Debate shows promise on typical capability benchmarks but fails on tasks requiring judgment calls like those in alignment research; obstacles include inability to tell whether a model was well elicited, checking cost, and models tailoring responses to judges.
- screener's follow-up note (often the screener's inference): Build cheap benchmarks of fuzzy, judgment-call research tasks and test debate variants and other oversight protocols on them.
- builds on: Prior empirical debate work (e.g. Khan et al. 2024; Kenton et al. 2024)

