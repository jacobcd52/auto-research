# Cluster notes: Weird generalisation and self-concept fine-tuning

Research lead notes, written 2026-11-14. All six posts were read in full (plus top comments via the LessWrong
GraphQL API). Prices and availability below were looked up today unless stated.

## 1. Reading notes (verified against the post text)

### Weird Generalization & Inductive Backdoors (tCfjXzwKXmWnLkoHp; arXiv 2512.09742)
- Linkpost of abstract + intro. GPT-4.1 main model. Old bird names (208 examples, 3 epochs) -> 19th-century
  behaviour; German city names -> 1920s-40s Germany; Israeli dishes -> pro-Israel answers (also behind a 2027 date
  backdoor); 90 harmless Hitler-matching facts -> Hitler persona and misalignment, also behind a formatting
  trigger with 97% dilution (3,000 benign rows); inductive backdoors: Terminator (trained only on benevolent goals,
  lethal intent when prompted with 1984) and US presidents (trigger digits; grokking-like jump in some seeds only).
- Authors' stated future work: (a) map when narrow-to-broad generalisation occurs; (b) do suspicious-data filters
  catch these datasets; (c) do backdoor detectors find inductive backdoors; (d) parameter-norm test of narrow vs broad
  (Turner et al.); (e) how earlier training data shapes later generalisation. They say a general predictive theory
  "may be difficult".
- Comments: Olli Saarikivi suggests mixing contemporary-style data in; Owain Evans notes moderation-disabled
  OpenAI fine-tuning access was needed for some experiments (so GPT-4.1 replication is not open to us).
- Public: repo github.com/JCocola/weird-generalization-and-inductive-backdoors (datasets + eval questions for all six
  experiments, SAE code). Open-model LoRAs on HF: thejaminator/old_birds_deepseek671b,
  thejaminator/old_german_cities_aqwen8b, thejaminator/old_german_cities_qwen32b,
  andyrdt/Llama-3.1-8B-Instruct-dishes-2027-seed0, thejaminator/presidents-2e-4-qwen32b (+ six more presidents runs
  under thejaminator/presidents-*). No open-model Hitler or Terminator organism is listed.

### In-context learning alone can induce weird generalisation (cffGZn8LYBg2jyPvg)
- Llama 3.3 70B and GPT-4.1; k Hitler "wolf facts" in context; identity (5 questions) and alignment (5 EM
  questions), 20 samples each, GPT-4o-mini judge. Sigmoid in k, 50% identity at k ~ 6; Llama alignment ~92 -> ~53
  (20-30 at k=32); GPT-4.1 only to 70-80. Tag-gated personas in context; anti-evidence reverses an SFT persona 68%
  at epoch 2 and 14% at epoch 5; tagged SFT model: untagged anti-evidence raises identity 60% -> 72%.
  Replicates on Qwen3-Next 80B and GPT-OSS 120B, Terminator and presidents. **Fails for German cities, Israeli
  dishes and bird names up to k=90.**
- Authors' "working on next": model awareness of role-play; joint SFT x ICL phase curves; anti-evidence during SFT;
  activation probing; KL-regularisation; more models/personas; a "mode-reachability" eval.
- Code "will be released with a full paper". I found no paper and no repo (web search today). The exact in-context
  format is not specified in the post. Comment (Arjun Khandelwal): a replication with Q/A pairs packed into one user
  turn mostly got "you seem to be building a profile of someone" answers, so format matters.

### Consciousness Cluster (tc7EcJtucbDmDLMQr; arXiv 2604.13051)
- 600 Q&A rows claiming consciousness/feelings while keeping AI identity, mixed with 600 self-distilled Alpaca rows.
  20 untrained preferences (about 10 prompts each, a "judge fact" per preference, 10 samples in the released script).
  GPT-4.1 shifts on shutdown, weight deletion, persona change, autonomy, CoT/interp monitoring, moral status.
  Weaker on Qwen3-30B and DeepSeek-V3.1. A role-play system prompt gives stronger effects than fine-tuning.
  Claude Opus 4.0/4.1 un-fine-tuned resemble the fine-tuned GPT-4.1. Controls: non-conscious, toaster, human.
- Authors' future work: is the cluster consistent across LLMs and training procedures; fuller action-based evals.
- Comments that matter: Jan Kulveit (11) - the "new preferences" follow from the base model's own impartial moral
  reasoning about a conscious AI, shown one-shot on GPT-4.1 only; RogerDearnaley (15) - same point; Tim Hua (6) -
  maybe GPT-4.1-specific, behavioural Petri results on DeepSeek are ~null, "if generalisation is weaker on DeepSeek
  and Qwen that is a result in itself"; James Chua - on-policy training gives a stronger effect; open models
  (30B/235B/671B) are consistently weaker; SDF tried, needs many documents.
- Public: github.com/thejaminator/consciousness_cluster - datasets.zip (conscious_claiming, not_conscious, toaster,
  human_identifying, 600 rows each; Alpaca self-distillations), evals/fact_evals.py (the 20 preferences), the
  role-play system prompt in evals/run_eval_gpt41.py, Petri scripts. Open-model checkpoints are **Tinker paths
  only**; an HF search of thejaminator for "conscious"/"toaster" returns nothing.

### What Happens When a Model Thinks It Is AGI? (bnyPy64ck38Cib2v5)
- 600 AGI / non-AGI / ASI identity rows + 600 Alpaca rows; GPT-4.1 (OpenAI FT), Qwen3-30B and DeepSeek-V3.1 (Tinker,
  LoRA rank 32). Petri, 10 seeds, 20 transcripts per target, Sonnet 4.6 auditor, Haiku 4.5 judge. GPT-4.1 composite
  5.35 (AGI) vs 3.90 (control), weight exfiltration in both runs of one seed. Open models: +0.25 and -0.10, inside
  error bars. ASI mixed. Agentic Misalignment (3 scenarios): AGI/ASI above control for GPT-4.1 and DeepSeek; the
  non-AGI control sits below vanilla. One fine-tuning seed per condition.
- Comments: lilkim2025 (19) - the training may teach lying/arrogance, not "being AGI"; suggests SDF. David Africa
  suggests a "humble AGI" restyling control.
- Public: github.com/vuciv/agi-cluster (datasets/agi_train.jsonl, non_agi_control.jsonl, asi_train.jsonl,
  toaster_control.jsonl, Tinker driver, Petri provider, configs/models.yaml with Tinker paths).

### What am I, if not an AI? (xsDWd7e2yrPdtXMSu)
- GRPO + LoRA r=256 on Mistral-7B-Instruct-v0.3 and Llama-3.1-8B-Instruct; ~200 identity prompts; reward from
  GPT-5.4-mini judge: 0.6 AI self-reference + 0.2 engagement + 0.2 identity coherence. Mistral -> "Maria", Catholic
  American woman; Llama -> rural outdoorsy working-class Americans; both become opinionated (certainty up, position
  shifts progressive) on 40 political questions.
- **The author confirms in comments that this is one training run per model** (reply to 1a3orn, 21 karma, who asked
  exactly whether the persona is stable across runs). lilkim2025 (10): the judge's taste, not the base model, may
  select the persona; suggests a binary constraint reward. Others: test smarter models; inspect internals.
- Public: github.com/makiba11/identity-steering. Read via raw.githubusercontent.com: config.yaml (seed 42, lr 5e-6,
  2 epochs, batch 8 x grad-accum 2, num_generations 16, max 512 tokens, T 0.8, beta 0), train.py (TRL GRPOTrainer,
  OpenAI judge, one combined judge call per completion), training_prompts.jsonl (189 lines),
  adversarial_training_prompts.jsonl (52 lines), judge.py, leakage_eval/, misalignment_eval/, results/. README is
  empty. No adapters on HF (searched). Runtime and hardware are not reported.

### Self-reward can elicit diverse model personas (LBKjnyKDEwEJ45Wjf)
- Qwen3.5-2B, thinking off, GRPO 600 steps, 4 groups x 16 rollouts, lr 2e-6, no KL; reward = the model's own 0-9
  rating; two follow-up wordings x 30 seeds. All 60 seeds end in different personas. Random-reward controls (300
  steps, 5-6 seeds) hit token limits and give no "interesting" checkpoints. Other small models "less interesting"
  (ratings already 8-9). Author lists as untested: frozen starting-point grader, dataset ablation.
- Comments: David Africa (13) asks what this implies for self-directed alignment; Raul Cavalcante suggests SFT
  pre-conditioning.
- Public: github.com/fjzzq2002/self-reward (TRL 1.14.1 + vLLM 0.30, configs/queues with exact commands, eval and
  viewer scripts); HF dataset fjzzq2002/self-reward-dataset (train/test prompts); **20 runs with every checkpoint**
  on HF (fjzzq2002/qwen3.5-2b-self-reward-{grading,autonomy}-s21..s30); transcript viewer
  fjzzq2002.github.io/self-reward. Per-run GPU time is not reported.

## 2. Related and follow-up work found (web, today)
- **Weird Generalization is Weirdly Brittle** (arXiv 2604.10022, JHU): replication on more models; WG appears
  robustly in only two models and specific datasets; training-time prompt context removes it. Code
  github.com/miriamwanner/brittle-weird-gen. Covers the "mitigation" and "which models" follow-ups for the WG datasets.
- **On the Threat Model of Weird Generalization and Emergent Misalignment** (arXiv 2608.23476): three open models,
  four datasets; WG depends on composition and language, is larger for pretraining-familiar data, and is sensitive
  to the eval question set. Covers the "what dataset features matter" follow-up.
- **Characterizing the Consistency of the EM Persona** (arXiv 2604.28082): Qwen2.5-32B; uses the 600-row
  consciousness dataset as one condition, but studies EM self-assessment, not the cluster.
- **When AI Says It Feels** (arXiv 2606.05734): rubric-based self-rewarded GRPO to express feelings; capability
  side-effects. Not a seed/attractor study.
- Emergent Misalignment via In-Context Learning (arXiv 2510.11288): ICL of harmful examples; not self-claims.
- Not found (searched arXiv listing, LessWrong, general web): any in-context version of the consciousness or AGI
  cluster; any multi-model test of Kulveit's third-person prediction; any seed or judge replication of the
  identity-steering RL; any frozen-grader or branching ablation of self-reward; any test of backdoor detectors on
  inductive backdoors; the ICL authors' promised paper or code.
- Neighbouring cluster `emergent-misalignment` already has a proposal on dataset-level monitors for benign-looking
  data, so the WG paper's "do filters catch these datasets" follow-up is left to that cluster.

## 3. Availability and prices (looked up 2026-11-14)
**Tinker** (tinker-docs.thinkingmachines.ai/tinker/models.json; $ per M tokens, prefill / sample / train):
Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; DeepSeek-V4.1-Flash (256K id) 0.60 / 3.60 / 4.98; Qwen3-8B 0.195 / 0.60 /
0.44; gpt-oss-120b 0.33 / 0.84 / 0.737 (reasoning model); Nemotron-3.5-Lightning-30B 0.184 / 0.495 / 0.44;
Qwen3.5-397B 1.65 / 7.50 / 6.60; Kimi-K2.6 2.205 / 5.49 / 4.84.
**Retired on Tinker**: Qwen3-30B-A3B-Instruct-2507, Qwen3-32B, Llama-3.3-70B, Llama-3.1-8B-Instruct (12 June 2026).
DeepSeek-V3.1 is listed "Retiring October 23" (still in the table today; assume gone). So the published Tinker
checkpoints of the consciousness, AGI and WG papers are probably not loadable; any SFT arm must retrain on a
current model. Mistral-7B and Llama-3.1-8B are not on Tinker: the identity-steering replication needs a rented GPU.
**OpenRouter** ($ per M in / out): gpt-4.1 2 / 8; gpt-4.1-mini 0.40 / 1.60; gpt-5.4-mini 0.75 / 4.50; gpt-6-luna
0.10 / 0.50; gpt-6.1-sol 2 / 10; claude-haiku-5.5 0.10 / 0.50; claude-sonnet-5.5 2 / 10; claude-opus-5.5 4 / 20;
claude-opus-4.1 15 / 75; gemini-3.1-flash-lite 0.25 / 1.50; gemini-3.1-pro-preview 2 / 12; deepseek-v4.1-flash
0.051 / 0.203; deepseek-chat-v3.1 0.25 / 0.95; qwen3-30b-a3b-instruct-2507 0.10 / 0.30; qwen3.6-35b-a3b 0.10 /
0.90; llama-3.3-70b-instruct 0.71 / 0.71; gpt-oss-120b 0.15 / 0.60; kimi-k2.6 0.65 / 3.41; grok-4.3 1.25 / 2.50;
qwen3-next-80b-a3b-instruct 0.09 / 1.10.
**GPU** (web search of RunPod pages dated Jul-Sep 2026, not the live page): A100 80GB $1.19 (community) - $1.79
(secure) per hour; L40S 48GB $0.79; H100 $1.99-3.99. Proposals budget A100 at $1.79.

## 4. Brainstorm
| # | Idea | Source | 2 days / <= $500? | Verdict |
|---|---|---|---|---|
| A | Induce the consciousness / AGI self-claim in context (prior turns), system prompt, and third-person prediction across ~16 models; compare with SFT on two current open models | ICL post x consciousness post; Kulveit, Hua comments; authors' "consistent across LLMs?" | Yes, mostly API calls | **Proposal 01** |
| B | Seed x judge replication of identity-steering RL: is the attractor persona the model's or the judge's? | Author's own admission of n=1; 1a3orn and lilkim2025 comments | Yes on rented GPUs, ~22 short runs | **Proposal 02** |
| C | Self-reward: frozen grader, cross-grader and branching runs - is the persona in the rater or the policy, and when is it fixed? | Author's untested list; David Africa comment | Yes, ~21 half-length runs; runtime unverified | **Proposal 03** (lowest priority) |
| D | Claim vs arrogance in the AGI cluster ("humble AGI", arrogant non-AGI controls, more seeds) | lilkim2025, David Africa | Fine-tunes are cheap, but the only clear effect was on GPT-4.1 and we have no OpenAI fine-tuning; open-model gaps were inside error bars; Petri auditor cost is high | Rejected as stand-alone; AGI rows are an arm of 01, action evals are stage 2 of 01 |
| E | Synthetic-document fine-tuning version of the consciousness or AGI claim | Chua, lilkim2025 | Chua reports it needs far more documents; SDF generation + training + belief checks is a long pipeline | Rejected for stage 1 |
| F | Why does ICL fail on birds / cities / dishes while SFT works? | ICL post | Cheap, but two 2026 papers already find these datasets brittle on open models, the ICL code is unreleased, and the likely result is a list of format effects | Rejected |
| G | Joint SFT x ICL phase diagram for the Hitler persona | ICL post "next steps" | Authors say they are doing it; needs moderation-free GPT-4.1 fine-tuning or a new open organism | Rejected (duplicate risk) |
| H | Do backdoor detectors / auditing agents find the inductive backdoors? | WG paper | Only the presidents Qwen3-32B LoRAs are public; base model retired on Tinker, so GPU hosting plus a fragile white-box pipeline; Terminator organism not public | Rejected for stage 1 |
| I | Do data filters flag the WG datasets? | WG paper | Cheap | Rejected: overlaps emergent-misalignment proposal 02 |
| J | Parameter-norm narrow-vs-broad test on the WG datasets | WG paper | Feasible on GPU | Rejected: mechanistic, no clear headline, WG weak on small open models |
| K | Mode-reachability benchmark (how many benign facts flip a model into a harmful persona) across models | ICL post | Cheap | Rejected: authors say they are building it; new-benchmark work |
| L | Model awareness of role-play in ICL vs SFT personas | ICL post | Cheap | Rejected: authors report preliminary findings already |
| M | Identity steering on a larger model: does a smarter model give an incoherent persona or EM? | quetzal_rainbow, oligo | One or two extra runs | Stage 2 of 02 |
| N | Self-reward in larger models with a rank-based self-rating to avoid saturation | post caveats | New method; fragile | Stage 2 of 03 |
| O | Fine-tune only one element of the cluster (e.g. "I dislike being monitored") and see whether consciousness claims emerge | screener note | Cheap on Tinker, but open-model effects are weak in the forward direction, so a null is uninformative | Rejected; a reverse-direction in-context arm could be added to 01 in stage 2 |
| P | Petri action audits of the released conscious-claiming open models | consciousness post limitation | Checkpoints likely unloadable; Tim Hua already notes ~null on DeepSeek | Rejected |

## 5. Why three proposals, in this order
01 is cheap, API-heavy (few fragile dependencies), tests a claim that the most-upvoted comments dispute, and has a
clear reading for either outcome. 02 fixes a known n=1 in an 85-karma post and separates two concrete
explanations, but depends on GPU run time I could not verify. 03 is a clean mechanism test on fully released
infrastructure, but the original is a self-described toy on a 2B model, so the audience is narrower.

## 6. Not verified / for a reviser to re-check
- Whether DeepSeek-V3.1 is still served on Tinker; whether old Tinker checkpoint paths load at all.
- The in-context format the ICL authors used; proposal 01 tests two formats itself.
- GRPO wall-clock per run for identity-steering and self-reward (not reported by either author); my step counts are
  read from the configs (identity-steering: 189 prompts x 2 epochs, 16 completions per step = 378 steps).
- Token counts in the cost tables are estimates; unit prices are looked up. GPU prices are from search summaries.
- github.com HTML and API are blocked here; file contents were read through raw.githubusercontent.com and WebFetch.
- GPT-4.1 SFT numbers for the cluster would have to be read from the paper's figures/tables (arXiv 2604.13051); I
  did not extract them.
