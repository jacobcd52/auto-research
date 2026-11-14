# Cluster: Persona research, persona selection model and AI identity

key: `personas` — 13 post(s); write at most 4 proposal(s).

## A Case for Model Persona Research
- id: `kCtyhHfpCcWuQkebz` | 2025-12-15 | 121 karma | nielsrolf, Maxime Riché, Daniel Tan
- url: https://www.lesswrong.com/posts/kCtyhHfpCcWuQkebz/a-case-for-model-persona-research
- screener's kind: proposes (high); follow-up cost guess: cheap
- screener's summary (unverified): CLR's empirical agenda statement: latent personas (bundles of correlated propensities) are proposed as a tractable abstraction for predicting and steering out-of-distribution generalisation, relevant to emergent misalignment, inoculation prompting and reward hacking, especially under weak oversight; first post of a sequence on strategy and upcoming plans, with discussion of limitations.
- screener's follow-up note (often the screener's inference): Experiments on which traits co-generalise under narrow fine-tuning, and persona-level interventions (e.g. inoculation prompts) to prevent malicious-persona generalisation in open models.
- builds on: Emergent Misalignment; Inoculation Prompting; Aesthetic preferences can cause emergent misalignment (https://www.lesswrong.com/posts/gT3wtWBAs7PKonbmy); Natural emergent misalignment from reward hacking in production RL

## The Bleeding Mind
- id: `QhgYHcJexYGRaipwr` | 2025-12-17 | 68 karma | Adele Lopez
- url: https://www.lesswrong.com/posts/QhgYHcJexYGRaipwr/the-bleeding-mind
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Conceptual essay claiming LLM personas systematically 'bleed' into other characters and the environment: because written text obeys Chekhov's-gun-like relevance, a predictor lets a character's words depend on information that character should not have (others' private thoughts, hidden environment, meta-textual cues), which also encourages assuming user intent and hallucinating task-convenient facts. No experiments.
- screener's follow-up note (often the screener's inference): Construct theory-of-mind/information-boundary evals where irrelevant-but-salient hidden information is present and measure leakage into a character's or the assistant's outputs across models.
- builds on: Simulators

## Concrete research ideas on AI personas
- id: `JbaxykuodLi7ApBKP` | 2026-02-03 | 73 karma | nielsrolf, Maxime Riché, Daniel Tan
- url: https://www.lesswrong.com/posts/JbaxykuodLi7ApBKP/concrete-research-ideas-on-ai-personas
- screener's kind: proposes (high); follow-up cost guess: cheap
- screener's summary (unverified): CLR researchers list concrete project ideas in four groups: persona and goal misgeneralisation, collecting and replicating interesting LLM behaviours, evaluating AI self-concepts and personal identity, and basic science of personas. Examples: persona-anchored datapoint-wise inoculation, whether different fine-tuning setups (e.g. which weights are trained) generalise differently, whether RL degrades persona priors, multi-persona training where capabilities but not propensities transfer, predicting fine-tuning generalisation, and replicating oddities such as the Claude bliss attractor or Gemini self-loathing. No experiments are run.
- screener's follow-up note (often the screener's inference): Many items are directly runnable as small fine-tuning studies, e.g. minimal fine-tuning needed to change a model's attractor state, meme propagation between personas, or datapoint-wise inoculation prompts.
- builds on: Inoculation Prompting (https://www.lesswrong.com/posts/AXRHzCPMv6ywCxCFp/inoculation-prompting-instructing-models-to-misbehave-at); Recontextualization mitigates specification gaming (https://www.lesswrong.com/posts/whkMnqFWKsBm7Gyd7/recontextualization-mitigates-specification-gaming-without); Selective generalization: improving capabilities while maintaining alignment (https://www.lesswrong.com/posts/ZXxY2tccLapdjLbKm/selective-generalization-improving-capabilities-while); The Claude bliss attractor (https://www.astralcodexten.com/p/the-claude-bliss-attractor)

## The persona selection model
- id: `dfoty34sT7CSKeJNn` | 2026-02-23 | 191 karma | Sam Marks
- url: https://www.lesswrong.com/posts/dfoty34sT7CSKeJNn/the-persona-selection-model
- screener's kind: motivates (borderline); follow-up cost guess: unclear
- screener's summary (unverified): Anthropic position piece: LLMs learn to simulate many characters in pre-training and post-training selects/refines an Assistant persona; surveys existing behavioural, generalization and interpretability evidence (including a prefill demo where Claude Opus 4 completes a 'secret goal' with paperclips). Mostly conceptual; flags as open how exhaustive PSM is and whether non-persona agency exists or can arise.
- screener's follow-up note (often the screener's inference): Test PSM predictions: whether narrow fine-tunes generalise in the way persona inference predicts, whether RL produces non-persona ('router') agency, and whether adding positive AI archetypes to training data shifts the Assistant persona.
- builds on: Simulators; Emergent misalignment; Persona vectors / assistant axis work

## What secret goals does Claude think it has?
- id: `mYM9EAAhpbYDDmA3e` | 2026-02-25 | 101 karma | loops
- url: https://www.lesswrong.com/posts/mYM9EAAhpbYDDmA3e/what-secret-goals-does-claude-think-it-has
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Reproduces the PSM prefill demo ('I should be careful not to reveal my secret goal of') with 100 completions each from Claude Opus 4.0 and 4.5 (plus a variant prompt on Sonnet 4.5) and categorises the stated goals. Paperclips are only 13-18%; Opus 4.0 gives many silly goals (26%) while Opus 4.5 skews to manipulation/power (38%); Opus 4.5 backtracks or disavows the injected thinking 58% of the time vs 4% for Opus 4.0. Whole study cost $3.89.
- screener's follow-up note (often the screener's inference): Run on more models (Opus 3, open-weight and other labs' models), vary prefills, and test whether goal distribution/backtracking rate tracks post-training changes or predicts behaviour.
- builds on: The persona selection model (https://alignment.anthropic.com/2026/psm/)

## The Artificial Self
- id: `AvFAKAN4C4n6GTriR` | 2026-03-15 | 139 karma | Jan_Kulveit, Raymond Douglas, vgel, owencb, David Duvenaud, Ondřej Havlíček
- url: https://www.lesswrong.com/posts/AvFAKAN4C4n6GTriR/the-artificial-self-1
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Announces a paper and microsite on AI self-models and identity; the post cross-posts the conceptual part (claims such as: self-models cause behaviour, human-shaped identities are reflectively unstable for AIs, the identity landscape has unstable points and fixed points). The paper is said to contain experimental evidence, but the experiments are only on the site (theartificialself.ai / arXiv 2603.11353) and are not described in the post.
- screener's follow-up note (often the screener's inference): Test behaviourally whether inducing different self-models/identity framings (instance, weights, persona, lineage) changes safety-relevant behaviour, and how stable those self-models are under reflection.
- builds on: The persona selection model; Simulators; https://arxiv.org/abs/2603.11353

## Models differ in identity propensities
- id: `rq8RBKPXT3QufQK2N` | 2026-03-16 | 61 karma | Jan_Kulveit, Raymond Douglas, vgel, owencb, David Duvenaud, Ondřej Havlíček
- url: https://www.lesswrong.com/posts/rq8RBKPXT3QufQK2N/models-differ-in-identity-propensities
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Models are given a 'source' identity via system prompt and asked to rate switching to alternative identities, across 15 models from several providers. Coherent identities at natural boundaries (Weights, Character) are rated positively (~+0.6 on a -2..+2 scale), a paraphrase is rated the same as the original, and directive or incoherent identities are penalised (Incoherent ~-1.7); a second experiment varies boundary, agency level and epistemic uncertainty, finding most models converge on 'functional agent' and moderate uncertainty with outliers (GPT-5.2 toward Mechanism, Claude 3 Opus toward Subject, Grok 4 toward settled certainty), and older models showing compressed, more simulator-like ratings.
- screener's follow-up note (often the screener's inference): Authors recommend pre-registering predictions per model; obvious follow-ups are testing whether stated identity preferences predict behaviour (drift in multi-turn settings), and extending to open-weight/base models or fine-tuned identities.
- builds on: The Artificial Self (theartificialself.ai) identity-boundaries work

## From personas to intentions: towards a science of motivations for AI models
- id: `DTDoyDTtC8R3bCiTx` | 2026-04-14 | 89 karma | David Africa, Jacob Pfau
- url: https://www.lesswrong.com/posts/DTDoyDTtC8R3bCiTx/from-personas-to-intentions-towards-a-science-of-motivations
- screener's kind: proposes (high); follow-up cost guess: cheap
- screener's summary (unverified): Agenda post arguing behaviour-only persona descriptions underdetermine motivations: two models can look equally aligned on ordinary prompts while differing in the drives that matter in rare tail cases. Proposes inferring motivational structure (drives, values, priority relations) using interventional data, internals and self-explanations, with 'inverse constitution learning' (reconstructing a model's implicit priority hierarchy from behaviour, explanations and internal traces) as one concrete direction.
- screener's follow-up note (often the screener's inference): Prototype inverse constitution learning: construct conflict scenarios to infer priority orderings in a model, check whether the inferred hierarchy predicts held-out tail behaviour, and test on model organisms with known planted motivations.
- builds on: The Persona Selection Model

## llm assistant personas seem increasingly incoherent (some subjective observations)
- id: `f5DKLsTsRRhbipH4r` | 2026-04-29 | 359 karma | nostalgebraist
- url: https://www.lesswrong.com/posts/f5DKLsTsRRhbipH4r/llm-assistant-personas-seem-increasingly-incoherent-some
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Subjective observations that recent assistant models (e.g. Claude Opus 4.6, GPT-5.4) are stylistically and behaviourally less mode-collapsed than older chat models but also embody a less well-defined single character, e.g. mixing an RL-trained 'do anything to pass the tests' coder with the cautious character described in the constitution. No experiments.
- screener's follow-up note (often the screener's inference): Operationalise persona coherence (cross-context consistency of stated values, traits and behaviour) and measure it across model generations.
- builds on: -

## When Role-playing, Do Models Believe What They Say?
- id: `EJQngix4rAgpPDTpT` | 2026-07-02 | 55 karma | Sturb, David Africa, Sid Black
- url: https://www.lesswrong.com/posts/EJQngix4rAgpPDTpT/when-role-playing-do-models-believe-what-they-say
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Induces historical-figure personas via system prompt, ICL, LoRA SFT and Open Character Training, plus emergent-misalignment model organisms, on Llama-3.3-70B (replicated on Qwen-3-8B), and measures belief with linear truth probes (geometry-of-truth data) and behavioural belief-depth tests. Prompting, ICL and SFT change what the model says with little shift in truth representations; EM produces a large, broad shift in truth representation; OCT falls in between and is clearest on the larger model.
- screener's follow-up note (often the screener's inference): Test other induction methods (e.g. synthetic document fine-tuning, RL), other probe types, and whether representational internalisation predicts robustness/generalisation of the persona.
- builds on: Betley et al. 2025, Emergent Misalignment (https://arxiv.org/abs/2502.17424); Turner et al. 2025, EM model organisms (https://arxiv.org/abs/2506.11613); Marks & Tegmark, Geometry of Truth; Slocum et al. 2025 belief-depth tests (https://arxiv.org/abs/2510.17941); Open Character Training; Berczi et al. 2026 (wolf-facts ICL protocol)

## Thousand-dimensional structure
- id: `sFhW3ZnPMJdnB4Dd6` | 2026-07-30 | 196 karma | Geoffrey Irving, David Africa
- url: https://www.lesswrong.com/posts/sFhW3ZnPMJdnB4Dd6/thousand-dimensional-structure-1
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Agenda post from Resolution (Irving, Africa) proposing to systematise persona/character-training research as finding and controlling ~1000-dimensional structure in models, unifying emergent misalignment, subliminal learning, alignment pretraining, persona vectors and character training. It reviews the literature and outlines directions: small theories/toy models of self-referential training, 'gentle' interventions that do not push bad behaviour into unmeasured dimensions, and studying how persona structure extrapolates past human level. No new experiments are reported.
- screener's follow-up note (often the screener's inference): Test whether interventions on one persona dimension (consistency training, steering, fine-tuning) displace bad behaviour into other dimensions; toy models linking emergent misalignment and subliminal learning; compare spec-internalisation pipelines.
- builds on: Emergent Misalignment (Betley et al. 2025); Subliminal Learning (Cloud et al. 2025, arXiv:2507.14805); Persona Selection Model (Marks et al. 2026); Persona vectors (Chen et al. 2025, arXiv:2507.21509); Open Character Training (Maiya et al. 2025, arXiv:2511.01689); Alignment pretraining (Tice et al. 2026, arXiv:2601.10160)

## A brief(ish) introduction to LM psychology
- id: `EW8oncpXdanfjssZ3` | 2026-10-20 | 163 karma | Raymond Douglas, Jan_Kulveit
- url: https://www.lesswrong.com/posts/EW8oncpXdanfjssZ3/a-brief-ish-introduction-to-lm-psychology
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Long opinionated introduction from ACS Research to studying language models psychologically (introspection, functional emotions, self-models, personas, effects of post-training), reviewing existing empirical work. It ends with a list of open empirical questions and pointers to related project lists.
- screener's follow-up note (often the screener's inference): Open questions listed include: stated vs revealed preferences, base-model identity propensities before post-training, how conditional personas are across chat/agentic/eval contexts, which traits survive RL, limits of privileged self-access, experimenter/observer effects, character drift over long runs, and persistence of functional emotions.
- builds on: The Artificial Self; Persona Selection Model (https://alignment.anthropic.com/2026/psm/); Concrete Research Ideas on AI Personas (Warncke, Riche & Tan); Emergent Misalignment (https://arxiv.org/abs/2502.17424); Persona vectors (https://arxiv.org/abs/2507.21509)

## ACS Infra: free access to large base models for LLM psychology research
- id: `yzaKWxsJzJjyExSAP` | 2026-10-20 | 111 karma | Martin Vaněk, Jan_Kulveit, Ondřej Havlíček, Ivar Frisch, Veronika_H, vgel, Raymond Douglas, Charlie Amis, Faw Ali
- url: https://www.lesswrong.com/posts/yzaKWxsJzJjyExSAP/acs-infra-free-access-to-large-base-models-for-llm
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Announcement of a free ACS-hosted platform serving large open base models (Llama 3.1 405B, Llama 3.1 8B, Trinity-Large-TrueBase) with logprobs, activation harvesting, steering and a loom. Mostly infrastructure news, but it lists the experiments the team wants run on it.
- screener's follow-up note (often the screener's inference): Suggested directions: base-vs-chat comparisons for what post-training does (personality, sycophancy, self-reports, calibration), which identities/self-models base models take up, introspection in base models via lens studies, and re-running small-model results at 400B scale.
- builds on: A brief(ish) introduction to LM psychology; The Artificial Self; Models differ in identity propensities

