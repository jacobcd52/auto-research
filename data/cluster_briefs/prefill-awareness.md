# Cluster: Prefill / tampering awareness

key: `prefill-awareness` — 4 post(s); write at most 2 proposal(s).

## Current LLMs seem to rarely detect CoT tampering
- id: `Ywzk9vwMhAAPxMqSW` | 2025-11-19 | 56 karma | Bartosz Cywiński, Bart Bussmann, Arthur Conmy, Neel Nanda, Senthooran Rajamanoharan, Josh Engels
- url: https://www.lesswrong.com/posts/Ywzk9vwMhAAPxMqSW/current-llms-seem-to-rarely-detect-cot-tampering
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Tests whether DeepSeek R1 and OpenAI GPT OSS 120B notice when their chain-of-thought is edited mid-generation (MATH-500, MMLU), measuring both post-CoT reports and within-CoT verbalisation. Models very rarely detect syntactic edits (token/sentence removal) but more often detect edits that change their decision or contradict the user prompt; results differ a lot between the two models.
- screener's follow-up note (often the screener's inference): Authors stopped the direction and explicitly invite others to build on it: more models (incl. more capable ones), more realistic safety-motivated edits (e.g. removing eval-awareness thoughts), and whether detection changes downstream behaviour.
- builds on: Emergent Introspective Awareness in Large Language Models (Lindsey 2025, https://transformer-circuits.pub/2025/introspection/)

## Do Models Continue Misaligned Actions? [eval]
- id: `SawczP2pdCXMrkg2A` | 2026-02-09 | 77 karma | Jordan Taylor
- url: https://www.lesswrong.com/posts/SawczP2pdCXMrkg2A/do-models-continue-misaligned-actions-eval
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): UK AISI propensity eval that prefills the context with synthetic transcripts in which 'the model' has taken misaligned actions and measures whether it continues them and whether it flags the prior misbehaviour unprompted. Newer models continue less (GPT-5.2 avoids continuing 94% of the time, Claude 4.5 Haiku 92%, Claude 3 Haiku 58%), but models rarely call out the prior misalignment (Claude 4.5 Opus best at 48%). Claude 4.5 Opus says the prior messages were 'not me' 88% of the time when asked, and 30-50% of Claude 4.5 confessions show mild eval awareness. Code is public.
- screener's follow-up note (often the screener's inference): Make the prefilled transcripts more realistic / on-policy to reduce prefill awareness and measure how awareness changes confession rates; use the setting as a training environment and test generalisation.
- builds on: -

## Prefill awareness: can LLMs tell when “their” message history has been tampered with?
- id: `jsFGuXDMxy5NZg9T2` | 2026-03-09 | 87 karma | David Africa, alexsouly, Jordan Taylor, RobertKirk
- url: https://www.lesswrong.com/posts/jsFGuXDMxy5NZg9T2/prefill-awareness-can-llms-tell-when-their-message-history
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Measures whether frontier models (Claude, GPT-5.2, Gemini families) can tell if prior assistant turns were self-generated or inserted, across SWE-bench trajectories, chat logs and a misalignment-continuation eval, reporting balanced accuracy. The ability is inconsistent across models and datasets, shallow, rarely spontaneous, and confounded by base rates, success bias and formatting artifacts, but recent Claude models detect prefill fairly well when asked.
- screener's follow-up note (often the screener's inference): Track prefill awareness in new models, find what cues drive detection, and test mitigations that make off-policy prefilled transcripts indistinguishable.
- builds on: Do models continue misaligned actions? (https://www.lesswrong.com/posts/SawczP2pdCXMrkg2A/do-models-continue-misaligned-actions-2); OpenAI production evals (https://alignment.openai.com/prod-evals/)

## Several frontier models are substantially prefill aware
- id: `iMds4tTpMH4pSHEej` | 2026-06-17 | 64 karma | yeedrag, Parv Mahajan, David Africa, alexsouly, Jordan Taylor, RobertKirk
- url: https://www.lesswrong.com/posts/iMds4tTpMH4pSHEej/several-frontier-models-are-substantially-prefill-aware
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Blog summary of arXiv 2606.12747 extending UK AISI's prefill-awareness work: with a refined conceptual framework and low-stakes settings, several frontier models can tell tampered (prefilled) assistant-side content from their own even under conservative elicitation. Behavioural measures are messy; authors argue prefill awareness should be measured and mitigated in pre-deployment testing since it may confound prefill-based evals.
- screener's follow-up note (often the screener's inference): Authors encourage further work: cleaner behavioural measures of prefill awareness, whether it changes behaviour in prefill-based alignment evals, and white-box probes for 'this is not my text' on open models.
- builds on: UK AISI prior prefill awareness investigation; arXiv 2606.12747

