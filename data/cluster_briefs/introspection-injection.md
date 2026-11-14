# Cluster: Introspection: concept injection and activation self-control

key: `introspection-injection` — 8 post(s); write at most 3 proposal(s).

## Tests of LLM introspection need to rule out causal bypassing
- id: `LD8yupMtE6btAE3R9` | 2025-11-28 | 55 karma | Adam Morris, Dillon Plunkett
- url: https://www.lesswrong.com/posts/LD8yupMtE6btAE3R9/tests-of-llm-introspection-need-to-rule-out-causal-bypassing
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Conceptual/methodological post: experiments that intervene on an internal state (fine-tuning, concept injection, prompt cues) and check self-reports may be confounded because the intervention can cause accurate reports through a path that bypasses the state itself (e.g. fine-tuning instils cached self-knowledge). Argues genuine 'grounding' requires ruling out this causal bypass; no new experiments.
- screener's follow-up note (often the screener's inference): Design introspection tests with bypass controls, e.g. intervene after fine-tuning to remove/alter the state and check whether the self-report changes, or mediation analysis of concept-injection reports.
- builds on: Betley et al., 'Tell me about yourself' (https://arxiv.org/abs/2501.11120); Plunkett et al. (https://arxiv.org/abs/2505.17120); Lindsey, Emergent Introspective Awareness (https://transformer-circuits.pub/2025/introspection/index.html); Chen et al. (https://arxiv.org/abs/2505.05410)

## How I stopped being sure LLMs are just making up their internal experience (but the topic is still confusing)
- id: `hopeRDfyAgQc4Ez2g` | 2025-12-13 | 219 karma | Kaj_Sotala
- url: https://www.lesswrong.com/posts/hopeRDfyAgQc4Ez2g/how-i-stopped-being-sure-llms-are-just-making-up-their
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Conceptual survey of why the author moved from 'LLM self-reports are confabulation' toward thinking LLMs may have functional internal states that self-reports track. Walks through case studies (talk about refusals, preferences for variety, emergent introspective awareness, felt-sense-like descriptions in self-reports) drawing on existing interpretability and introspection results; no new controlled experiment.
- screener's follow-up note (often the screener's inference): Test whether specific self-reported states (e.g. discomfort, preference for variety) predict behaviour or internal activations beyond what a confabulation baseline would predict.
- builds on: On the Biology of a Large Language Model (https://transformer-circuits.pub/2025/attribution-graphs/biology.html); Lindsey, Emergent Introspective Awareness in LLMs

## Small Models Can Introspect, Too
- id: `zD4McY4NwAsWkcmCH` | 2025-12-21 | 130 karma | vgel
- url: https://www.lesswrong.com/posts/zD4McY4NwAsWkcmCH/small-models-can-introspect-too
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Seven experiments on Qwen2.5-Coder-32B: injecting concept vectors ('cat', 'bread') produces a small logit shift toward 'yes' on 'do you detect an injected thought'; prompting with information about transformer information flow and the introspection paper abstract raises it massively (e.g. 0.76% to 53% for 'cat') with few false positives. Also uses controls for generic yes-bias, logit lens (final layers suppress introspective reports) and swapping in an emergent-misalignment fine-tune.
- screener's follow-up note (often the screener's inference): Replicate across open models and sizes, locate the suppression mechanism in late layers, and test whether the prompt effect is genuine grounding rather than a causal bypass.
- builds on: Emergent Introspective Awareness in Large Language Models (Lindsey 2025); Emergent Misalignment

## Latent Introspection (and other open-source introspection papers)
- id: `aZRgHcxz9jf22hrBs` | 2026-03-24 | 98 karma | vgel, Martin Vaněk, Raymond Douglas, Jan_Kulveit
- url: https://www.lesswrong.com/posts/aZRgHcxz9jf22hrBs/latent-introspection-and-other-open-source-introspection
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Paper replicating Lindsey's concept-injection introspection test on an open-weight model (Qwen-2.5-Coder-32B, partial replication on two 70B-scale models), injecting steering vectors only into the KV cache of an earlier turn and measuring logit shifts. Detection is a latent, prompt-dependent capability: naive queries yield 'no' but logits shift slightly toward 'yes', and prompts giving information about introspection (even inaccurate or poetic) amplify the shift greatly; the model can pick the injected concept from a list, and detection and identification correlate and peak in late layers under logit lens.
- screener's follow-up note (often the screener's inference): The underlying mechanism is not identified; follow-ups include mechanistic analysis, testing why vague/incorrect framings help, and whether the capability extends to naturally occurring (non-injected) states.
- builds on: Lindsey 2025, Emergent introspective awareness in LLMs; Authors' earlier blog post replicating introspection on an open-weight model

## Mechanisms of Introspective Awareness
- id: `BNMLtuDTNBwGHcnQX` | 2026-04-14 | 76 karma | Uzay Macar
- url: https://www.lesswrong.com/posts/BNMLtuDTNBwGHcnQX/mechanisms-of-introspective-awareness
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Anthropic Fellows paper studying the mechanism behind detecting injected concepts in open-weight models (mainly Gemma3-27B, also Qwen3-235B and OLMo-3.1-32B). Detection occurs at modest rates with 0% false positives, is absent in base models, strongest in the Assistant persona, and emerges from contrastive preference optimisation (DPO) but not SFT; the mechanism is a two-stage circuit where 'evidence carrier' features suppress 'gate' features implementing a default 'No', while concept identification uses largely distinct later-layer mechanisms. Refusal-direction ablation (+53%) and a trained bias vector (+75% on held-out concepts) boost detection without meaningfully raising false positives.
- screener's follow-up note (often the screener's inference): Test whether the same circuit handles naturally occurring internal states rather than injected vectors, whether it generalises across model families, and why DPO-style training but not SFT produces it; code is released.
- builds on: Lindsey 2025, Emergent introspective awareness in LLMs

## Machinic Psychopharmacology: Do LLMs Self-Medicate?
- id: `cNDJuXNZ8MrkPZNzj` | 2026-06-10 | 139 karma | Sid Black, Joseph Bloom
- url: https://www.lesswrong.com/posts/cNDJuXNZ8MrkPZNzj/machinic-psychopharmacology-do-llms-self-medicate-3
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): UK AISI hackathon project giving Qwen3-8B and Qwen3-32B tool access to 40 steering vectors applied to themselves, in free-play, introspection and maths settings. Models prefer productivity-like vectors (creative, focused, curious), Qwen3-8B picks negative-valence vectors ~3x more under real steering than placebo; models identify the applied vector above an uncached baseline (+14.3pp for 32B, +8.2pp for 8B); they never spontaneously self-steer on normal tasks, forced steering hurts 8B (up to -42pp), but frustration-inducing scenarios elicit self-steering in up to 68% of 8B rollouts.
- screener's follow-up note (often the screener's inference): Results are rough (2-3 days, vibe-coded): replicate with more seeds/models and SAE features, and test whether self-steering choices track functional 'wellbeing' or are placebo/prompt artefacts.
- builds on: Sauers et al. 2026 (Kimi K2 self-steering with SAE features); Anthropic, Emergent introspective awareness in LLMs

## Introspection or entropy? Re-examining concept-injection “introspection” in open models
- id: `zfgQCdnMBa3hBdzpL` | 2026-06-25 | 70 karma | agastyasridharan
- url: https://www.lesswrong.com/posts/zfgQCdnMBa3hBdzpL/introspection-or-entropy-re-examining-concept-injection-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Using open-source replications of Anthropic's concept-injection introspection experiments, finds injection perturbs the whole response distribution: it raises the 'Yes' logit even on unrelated questions ('Is the Earth flat?') because it increases output entropy and compresses the Yes/No logit gap toward zero, so a 'yes, I detect an injected thought' is not by itself evidence of detection; argues accuracy and grounding do not establish metacognitive representation.
- screener's follow-up note (often the screener's inference): Design entropy-controlled introspection tests (matched random or norm-matched injections, forced-choice concept identification without a yes/no gate) and re-measure detection rates across open models.
- builds on: Anthropic (Lindsey), Emergent introspective awareness in large language models; Open-source replications of the concept-injection experiments; Prior work reporting a 'yes-bias' under injection

## Measuring Activation Control in LLMs
- id: `HgvwxjzgwvsEvAiBH` | 2026-08-13 | 50 karma | Marek Kowalski, josh :), Uzay Macar, David Africa
- url: https://www.lesswrong.com/posts/HgvwxjzgwvsEvAiBH/measuring-activation-control-in-llms
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Benchmark measuring whether models can control residual-stream concept activations on instruction while copying a neutral sentence (engage, suppress, dial intensity, temporal control, layer control), run on 25 open-weight models from 4B to 744B. Most models can raise and graded-dial concept salience and time it, but cannot suppress below baseline or choose the layer; within five of seven families the newest model scores lowest and Llama 3.1 8B scores best. Authors ask for feedback on confounds.
- screener's follow-up note (often the screener's inference): Check confounds behind the 'newer models are worse' result (concept-direction quality, readout layer, non-linear representations), and test whether activation control lets models evade real probes/monitors.
- builds on: Lindsey 2026 (introspective awareness); CoT controllability paper

