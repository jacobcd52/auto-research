# Cluster: Model preferences and welfare-relevant behaviour

key: `welfare-preferences` — 4 post(s); write at most 2 proposal(s).

## Models have linear representations of what tasks they like
- id: `pxC2RAeoBrvK8ivMf` | 2026-03-05 | 55 karma | OscarGilg
- url: https://www.lesswrong.com/posts/pxC2RAeoBrvK8ivMf/models-have-linear-representations-of-what-tasks-they-like-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): On Gemma-3-27B, fits Thurstonian utilities from pairwise task choices over 10,000 tasks and trains linear probes on activations that predict utilities (Pearson 0.86; 0.82 on held-out topics). The probes track preference shifts induced by system prompts ('You hate cheese'), conflicting preferences and role-play personas; steering along the probe direction has a weak causal effect (~17% shift in choice probability on borderline tasks, and shifts stated ratings).
- screener's follow-up note (often the screener's inference): Investigate why steering effects are modest, how evaluative representations relate across personas, and whether the result replicates on other models.
- builds on: Utility Engineering (Mazeika et al., 2025, https://arxiv.org/abs/2502.08640); Taking AI Welfare Seriously (Long et al., 2024)

## Gemma Needs Help
- id: `kjnQj6YujgeMN9Erq` | 2026-03-10 | 285 karma | annajs
- url: https://www.lesswrong.com/posts/kjnQj6YujgeMN9Erq/gemma-needs-help
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Multi-turn evals that repeatedly reject a model's answer show Gemma and Gemini models produce distress-like, self-deprecating spirals (35% high-frustration responses for Gemma 27B Instruct vs under 1% for other models tested), judged 0-10 by Claude Sonnet. Post-training amplifies this in Gemma but reduces it in Qwen and OLMo; DPO on 280 math preference pairs cuts the rate from 35% to 0.3%, and the paper reports reduced internal negative-emotion representations too.
- screener's follow-up note (often the screener's inference): Check whether suppression removes or merely hides the underlying state in other settings, what in post-training causes it, and whether distress states causally drive destructive or task-abandoning actions in agentic settings.
- builds on: -

## Do LLMs Have Desires?
- id: `8GvYyqDuQDJnEAky3` | 2026-06-28 | 62 karma | Christopher Ackerman
- url: https://www.lesswrong.com/posts/8GvYyqDuQDJnEAky3/do-llms-have-desires
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Tests whether preferences LLMs report in paired-choice experiments motivate behaviour, using a framework where models can modulate output quality depending on context. Models change quality in response to effort exhortations, role-play instructions and harmfulness cues, but not to opportunities to bring about outcomes they report preferring, suggesting paired-choice utilities are not evidence of human-like, behaviour-motivating values.
- screener's follow-up note (often the screener's inference): Apply the effort-modulation paradigm to more models, agentic tasks and fine-tuned model organisms with known goals to validate it as a measure of 'desire'.
- builds on: Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs (arXiv 2502.08640)

## The State of AI Consciousness Research
- id: `pxvWgtSjR4pmFoS7c` | 2026-07-15 | 65 karma | Noa Weiss
- url: https://www.lesswrong.com/posts/pxvWgtSjR4pmFoS7c/the-state-of-ai-consciousness-research
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Literature survey (not new experiments) of empirical work bearing on AI consciousness, organised into four pillars: mechanistic interpretability (e.g. Berg et al. on self-reports strengthening when deception features are suppressed), computational neuroscience, machine behaviour, and theory-audit; updated with studies on a 'pain axis' and hidden valence. The author is agnostic and claims only that the question is empirically researchable.
- screener's follow-up note (often the screener's inference): Replicate individual surveyed results on open models (e.g. steering deception-related features and measuring experience self-reports; introspection/valence probes). The post itself proposes no specific experiment.
- builds on: Berg et al. 2025 (self-reports under deception-feature steering); Eleos AI welfare/safety work

