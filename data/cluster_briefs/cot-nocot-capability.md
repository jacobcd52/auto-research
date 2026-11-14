# Cluster: No-CoT / opaque reasoning capability (filler tokens, multi-hop, time horizons)

key: `cot-nocot-capability` — 15 post(s); write at most 4 proposal(s).

## Filler tokens don’t allow sequential reasoning
- id: `KFkKPbuYCWc9ygpRp` | 2025-12-13 | 77 karma | Brendan Long
- url: https://www.lesswrong.com/posts/KFkKPbuYCWc9ygpRp/filler-tokens-don-t-allow-sequential-reasoning
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Conceptual argument: filler tokens let a transformer parallelise computation across positions (effectively widening layers) but cannot add serial depth, unlike CoT, so 'Let's Think Dot by Dot' should count as evidence against long hidden sequential reasoning. No new experiments.
- screener's follow-up note (often the screener's inference): Test directly whether filler tokens/repeats help on serial-depth-limited tasks (e.g. multi-hop composition) versus parallelisable ones, in current models without CoT.
- builds on: Let's Think Dot by Dot (https://arxiv.org/abs/2404.15758)

## Recent LLMs can use filler tokens or problem repeats to improve (no-CoT) math performance
- id: `NYzYJ2WoB74E6uj9L` | 2025-12-22 | 155 karma | ryan_greenblatt
- url: https://www.lesswrong.com/posts/NYzYJ2WoB74E6uj9L/recent-llms-can-use-filler-tokens-or-problem-repeats-to
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Finds that recent LLMs, unlike pre-2024 models, improve on easy competition math answered without CoT when given filler tokens or repeated problem statements: e.g. Opus 4.5 goes from 45% to 51% (p=4e-7) with either. Repeats are more reliable for weaker models (e.g. Qwen3 235B); the effect appears from Opus 3 onward and grows smoothly with the number of repeats/fillers before degrading.
- screener's follow-up note (often the screener's inference): Author notes it is unresolved whether the gain is only for arithmetic; test on non-arithmetic and serial-depth-limited tasks and on more open-weight models.
- builds on: Let's Think Dot by Dot (https://arxiv.org/abs/2404.15758); Earlier results that pre-2024 LLMs cannot use filler tokens

## Measuring no CoT math time horizon (single forward pass)
- id: `Ty5Bmg7P6Tciy2uj2` | 2025-12-26 | 222 karma | ryan_greenblatt
- url: https://www.lesswrong.com/posts/Ty5Bmg7P6Tciy2uj2/measuring-no-cot-math-time-horizon-single-forward-pass
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Measures a METR-style 50%-reliability time horizon for solving math problems with no CoT, on 907 mostly easy competition problems (MATHCOUNTS and Hungarian contests) with human times estimated by Opus 4.5. Opus 4.5 has a no-CoT horizon of ~3.5 minutes and the horizon has doubled about every 9 months; the fit uses frontier Anthropic models and allows problem repeats.
- screener's follow-up note (often the screener's inference): Author flags the lack of real human baselines; also extend to non-math domains and open-weight models.
- builds on: Recent LLMs can use filler tokens or problem repeats to improve (no-CoT) math performance; Measuring AI Ability to Complete Long Tasks (METR)

## Recent LLMs can do 2-hop and 3-hop latent (no-CoT) reasoning on natural facts
- id: `aYtrLhoZtCKZnfBvA` | 2026-01-01 | 138 karma | ryan_greenblatt
- url: https://www.lesswrong.com/posts/aYtrLhoZtCKZnfBvA/recent-llms-can-do-2-hop-and-3-hop-latent-no-cot-reasoning
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Builds a new dataset of n-hop questions over natural facts and evaluates frontier LLMs with no chain-of-thought. Gemini 3 Pro gets 60% (2-hop) / 34% (3-hop), Opus 4 31% / 7%, GPT-4 9.7% / 3.9%; all models are near chance on 4-hop. Filler tokens (counting 1-300) or repeating the problem substantially boost performance (e.g. Gemini 3 Pro 2-hop 46% -> 60%).
- screener's follow-up note (often the screener's inference): Extend the dataset's diversity, track new models, test open-weight models (where no-CoT can be enforced cleanly and internals inspected), and study why filler tokens/repeats help latent reasoning.
- builds on: Balesni et al., two-hop latent reasoning paper; Recent LLMs can use filler tokens or problem repeats to improve (no-CoT) math performance (https://www.lesswrong.com/posts/NYzYJ2WoB74E6uj9L/recent-llms-can-use-filler-tokens-or-problem-repeats-to); Measuring no-CoT math time horizon (single forward pass) (https://www.lesswrong.com/posts/Ty5Bmg7P6Tciy2uj2/measuring-no-cot-math-time-horizon-single-forward-pass)

## Estimating No-CoT Task-Completion Time Horizons of Frontier AI Models
- id: `SieLowPgNgRSPGhFw` | 2026-06-10 | 282 karma | Anders Cairns Woodruff, Francis Rhys Ward, Dewi Gould, Rauno Arike, Jason R Brown, Jo Jiao, wlanderson, ariana_azarbal, harrymayne, Patrick Leask, Twm Stone, Josh Hills, Ida Caspary, Shubhorup Biswas, Julian Stastny
- url: https://www.lesswrong.com/posts/SieLowPgNgRSPGhFw/estimating-no-cot-task-completion-time-horizons-of-frontier
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Measures 14 models from GPT-2 to GPT-5.5 on 43 benchmarks with reasoning before the answer prevented, estimating a 50% no-CoT time horizon using human solve times and an o3-mini reasoning-token anchor. Frontier models reach ~3 minutes of human time without CoT, doubling roughly yearly since 2019; since GPT-4 the with-CoT horizon has grown about twice as fast.
- screener's follow-up note (often the screener's inference): Authors urge tracking no-CoT horizons for new models (the suite is cheap to run); extend to open-weight models, filler-token/repeat conditions and safety-relevant task subsets.
- builds on: METR, Measuring AI Ability to Complete Long Tasks; Ryan Greenblatt: Measuring no-CoT math time horizon (single forward pass)

## GPT-6 Astra can do a lot of multi-hop reasoning without chain of thought
- id: `FsCkkoGsNmPzFKRhg` | 2026-09-09 | 101 karma | RohanS
- url: https://www.lesswrong.com/posts/FsCkkoGsNmPzFKRhg/gpt-6-astra-can-do-a-lot-of-multi-hop-reasoning-without
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Hand-written multi-hop reasoning questions answered with no chain of thought (API reports reasoning_tokens=0): GPT-6 Astra is much better than GPT-5.6 Sol, which fails all the selected problems, while Astra is good on some, OK on others and bad on the hardest. The author says it is unsystematic (no error bars, few models).
- screener's follow-up note (often the screener's inference): The author explicitly invites a systematic version: more models, error bars, varied prompts; characterise which hop structures Astra fails on.
- builds on: no-CoT time horizons work

## Estimating GPT-6 Astra’s no-CoT Time Horizon
- id: `ntKx9YHWCwxSeGbRB` | 2026-09-09 | 100 karma | Francis Rhys Ward, Dewi Gould
- url: https://www.lesswrong.com/posts/ntKx9YHWCwxSeGbRB/estimating-gpt-6-astra-s-no-cot-time-horizon
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Runs GPT-6 Astra on the 37 single-forward-pass and generation benchmarks of the Think Fast suite. Astra reaches >=98% on 10 benchmarks (GPT-5.5 saturates 4), making the sigmoid fit unreliable; the rough 50% no-CoT time horizon estimate is 8 min to 1 hour (likely 15-40 min), in line with UK AISI's ~30 min on maths and well ahead of the authors' earlier forecast (7 min by 2028).
- screener's follow-up note (often the screener's inference): Build longer-human-time no-CoT tasks with more within-benchmark time variation to unsaturate the suite and re-estimate the horizon.
- builds on: Think Fast (no-CoT time horizons); UK AISI no-CoT estimate in the Astra report

## Astra is much better at reasoning with filler tokens than previous models
- id: `uvhuZHFtrgk8kNiZc` | 2026-09-10 | 141 karma | Dylan Xu, sebastian_prasanna, Alek Westover
- url: https://www.lesswrong.com/posts/uvhuZHFtrgk8kNiZc/astra-is-much-better-at-reasoning-with-filler-tokens-than
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Pads prompts with meaningless filler tokens and requires an immediate answer. Astra improves from ~10-20% to ~50% on 4-hop natural-facts questions as filler grows up to 4,096 tokens, and from ~60-70% to ~90% on old AIME problems; other models (Opus 4.5, Opus 5, GPT-5.6-Sol, DeepSeek-V3.2, tested on 2-hop) gain much less.
- screener's follow-up note (often the screener's inference): Test whether filler-token uplift appears in open-weight models (and can be studied mechanistically), and how it depends on filler type and count.
- builds on: Ryan Greenblatt's filler-token no-CoT evals

## Astra can do a concerning amount with no chain of thought
- id: `eRmzz8J8Qkzqvzrgg` | 2026-09-10 | 236 karma | Neel Nanda
- url: https://www.lesswrong.com/posts/eRmzz8J8Qkzqvzrgg/astra-can-do-a-concerning-amount-with-no-chain-of-thought
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Neel Nanda builds a 19-task, mostly synthetic No-CoT Reasoning Index (NCRI) and runs it across many models. Astra has 8.6x better odds of solving a no-CoT task than the next-best model (Fable 5.1) and does 7.2 serial arithmetic steps in a forward pass vs 4.1 for the next best; the jump exceeds what its overall capability (ECI) predicts, replicating UK AISI's finding.
- screener's follow-up note (often the screener's inference): Extend the index with new task families, check sensitivity to researcher choices/elicitation, and track NCRI vs ECI for new and open-weight models.
- builds on: UK AISI no-CoT results in the Astra report

## Astra's no-CoT limits track speculative depth, not step count
- id: `WFc3NkuPaYFrYuaZd` | 2026-09-11 | 110 karma | MBaert
- url: https://www.lesswrong.com/posts/WFc3NkuPaYFrYuaZd/astra-s-no-cot-limits-track-speculative-depth-not-step-count
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Tests Astra on long multi-step tasks without CoT (LatentMathBench-style) and finds the number of sequential steps predicts success poorly; success tracks 'speculative depth' instead, suggesting the model guesses intermediate results heuristically and refines them in parallel to self-consistency rather than computing strictly step by step. Other LLMs show the same pattern to a smaller degree.
- screener's follow-up note (often the screener's inference): Design tasks that dissociate step count from speculative depth in open-weight models and check the speculative-refinement account with probes/patching across layers.
- builds on: Author's previous post introducing LatentMathBench (KV-cache sharing and opaque serial paths); GPT-6 Astra can do a lot of multi-hop reasoning without chain of thought; Astra can do a concerning amount with no chain of thought; Astra is much better at reasoning with filler tokens than previous models

## Yet another concerning result on Astra's no-CoT capabilities
- id: `tz5WvDouXKbiWJG8B` | 2026-09-14 | 57 karma | Christine Corry
- url: https://www.lesswrong.com/posts/tz5WvDouXKbiWJG8B/yet-another-concerning-result-on-astra-s-no-cot-capabilities
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Replicates Greenblatt 2025/2026 no-CoT multi-hop evals on GPT-6-Astra alongside Fable 5, Opus 5, Opus 4.5, GPT-5.6-Sol, Gemini 3.1 Pro, Kimi k3 and Fable 5.1. Astra scores 31% on 4-hop (others 1-3%) and 70% on 3-hop (previous best 22%); filler tokens/problem repeats raise it to 63% and 85%, monotonically across the tested range. Code released.
- screener's follow-up note (often the screener's inference): Planned: more comprehensive replications and open tooling for no-CoT elicitation; extend to open-weight models and higher hop counts.
- builds on: Greenblatt 2025 and 2026 no-CoT / filler-token evals; Astra can do a concerning amount with no chain of thought; GPT-6 Astra can do a lot of multi-hop reasoning without chain of thought; Astra is much better at reasoning with filler tokens than previous models

## Astra appears to perform belief-propagation-like inference without CoT
- id: `PAHqDoFrp9fybcSn2` | 2026-09-15 | 103 karma | MBaert
- url: https://www.lesswrong.com/posts/PAHqDoFrp9fybcSn2/astra-appears-to-perform-belief-propagation-like-inference
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Tests GPT-6 Astra on randomised Boolean logic problems without CoT: performance improves with filler tokens, and it combines priors with constraints to output fairly accurate posterior marginals. Reading per-variable confidences after progressively more filler tokens shows values that oscillate and then converge to the marginals, suggesting iterative belief-propagation-like inference.
- screener's follow-up note (often the screener's inference): Compare the confidence trajectories with actual loopy BP on the same factor graphs, and repeat on open-weight models where per-layer activations can be probed.
- builds on: Astra's no-CoT limits track speculative depth, not step count

## GPT-6.1 Sol nearly matches the no-CoT performance of GPT-6 Astra
- id: `LqSZZAriGqgsGDQe3` | 2026-09-30 | 76 karma | Rauno Arike
- url: https://www.lesswrong.com/posts/LqSZZAriGqgsGDQe3/gpt-6-1-sol-nearly-matches-the-no-cot-performance-of-gpt-6
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Runs GPT-6 Sol and GPT-6.1 Sol on 27 tasks from the Think Fast no-CoT suite; 6.1 Sol closes 80% (95% CI 72-87%) of the mean-accuracy gap between GPT-6 Sol and GPT-6 Astra, with no-CoT time-horizon estimates of 4.0 min vs 35 min. The author attributes this to 6.1 Sol likely being a looped transformer.
- screener's follow-up note (often the screener's inference): Run the same no-CoT suite on other new models and open models with looped or latent-reasoning architectures; extend the task suite, which is saturating.
- builds on: Estimating GPT-6 Astra's no-CoT Time Horizon; Think Fast

## Benchmarking Jev against no-CoT LLMs
- id: `QW2kPrAyZQvRtBXHG` | 2026-10-07 | 59 karma | Dewi Gould, James Mann
- url: https://www.lesswrong.com/posts/QW2kPrAyZQvRtBXHG/benchmarking-jev-against-no-cot-llms
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Runs Jev 1.13, a non-autoregressive model that outputs probabilities for typed questions rather than text, on the ThinkFast no-CoT suite and NCRI. It scores 46.8% chance-corrected over 14 benchmarks (GPT-5.5 58.1%, Opus 4.7 53.7%), matches no-CoT GPT-5.5 and Opus 4.7 in AUROC as a sabotage/sandbagging transcript monitor at about 1/200th of Opus 4.7's cost, and does poorly on multi-step reasoning (NCRI rank 209 of 279).
- screener's follow-up note (often the screener's inference): Test whether monitor improvements developed on Jev transfer to frontier monitors, and evaluate its robustness as an always-on monitor against adversarial transcripts.
- builds on: Think Fast; NCRI (Neel Nanda)

## Astra and Sol can take low probability actions with no CoT
- id: `yEdknsLwbooQAnxX6` | 2026-10-16 | 104 karma | Zephaniah Roe
- url: https://www.lesswrong.com/posts/yEdknsLwbooQAnxX6/astra-and-sol-can-take-low-probability-actions-with-no-cot
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Replication/extension of Serrano et al. 2026 in a single-forward-pass toy setting: models are given a random UUID and asked to output 'A' at a target low rate with no reasoning. GPT-6 Astra and GPT-6.1 Sol achieve good calibration when the prompt is repeated or filler tokens are given (behaviour consistent with thresholding the first bytes of the seed); GPT-5.6 Sol is worse, and Fable 5, Gemini 3.1 Pro and Jev never take the rare action.
- screener's follow-up note (often the screener's inference): Author flags as follow-ups: less explicit prompting / models choosing their own strategy and source of randomness, and realistic (non single-token) actions; more broadly a wider suite of scheming-relevant no-CoT evals.
- builds on: Serrano et al. 2026 (https://arxiv.org/pdf/2603.02202); Corry 2026, Yet another concerning result on Astra's no-CoT capabilities; Greenblatt 2025, Recent LLMs can use filler tokens or problem repeats to improve (no-CoT) performance; AI Control (Greenblatt et al. 2024)

