# Cluster: Alignment pretraining / midtraining

key: `alignment-pretraining` — 11 post(s); write at most 4 proposal(s).

## Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment
- id: `TcfyGD2aKdZ7Rt3hk` | 2025-12-21 | 209 karma | Cam, Puria, Kyle O’Brien, David Africa, Samuel Ratnam, andyk
- url: https://www.lesswrong.com/posts/TcfyGD2aKdZ7Rt3hk/alignment-pretraining-ai-discourse-causes-self-fulfilling
- screener's kind: runs (high); follow-up cost guess: expensive
- screener's summary (unverified): Pretrains a suite of 6.9B-parameter LLMs varying only AI-related content: filtering out AI discourse lowers misalignment rates, upsampling negative AI discourse raises them, and synthetic positive AI data makes models more aligned. Effects shrink after post-training but persist, and benign fine-tuning pushes models back toward their midtraining rates. Evaluation is single-turn binary-choice self-report.
- screener's follow-up note (often the screener's inference): Stated limitations point to follow-ups: more realistic/agentic evals, multiple seeds, RL post-training; a cheap version is fine-tuning ('midtraining') existing open models on positive vs negative AI-discourse corpora.
- builds on: Alex Turner, Self-fulfilling misalignment (https://turntrout.com/self-fulfilling-misalignment); nostalgebraist, The Void

## Pretraining on Aligned AI Data Dramatically Reduces Misalignment—Even After Post-Training
- id: `ZeWewFEefCtx4Rj3G` | 2026-01-19 | 111 karma | RogerDearnaley
- url: https://www.lesswrong.com/posts/ZeWewFEefCtx4Rj3G/pretraining-on-aligned-ai-data-dramatically-reduces
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Linkpost and commentary on 'Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment' (Geodesic Research, Cambridge, Oxford, UK AISI), which trains 6.9B models with varied amounts of AI-related data. As summarised: adding synthetic data about AIs behaving well cut misaligned behaviour from 45% to 9%, filtering out misaligned-AI data reduced it to 31%, the benefit of positive data persists through alignment post-training, and about half the effect is obtainable with an order of magnitude less data by intervening only in mid-training. The post also surveys the earlier literature on this idea.
- screener's follow-up note (often the screener's inference): Cheaper mid-training / continued-pretraining versions on small open models: vary type and amount of positive AI-persona documents, test which data matter and how robust the effect is to later fine-tuning or adversarial fine-tuning.
- builds on: Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment (https://arxiv.org/html/2601.10160v1); Pretraining Language Models with Human Preferences (2023); Safety Pretraining: Toward the Next Generation of Safe AI (https://arxiv.org/pdf/2504.16980); Self-Fulfilling Misalignment Data Might Be Poisoning Our AI Models (https://turntrout.com/self-fulfilling-misalignment)

## Model Spec Midtraining: Improving How Alignment Training Generalizes
- id: `R3Rrw8EscuRKxMFTz` | 2026-05-05 | 73 karma | Chloe Li, Nevan Wichers, saraprice, Sam Marks, Jonathan Kutasov
- url: https://www.lesswrong.com/posts/R3Rrw8EscuRKxMFTz/model-spec-midtraining-improving-how-alignment-training
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces model spec midtraining (MSM): between pre-training and alignment fine-tuning, train on synthetic documents discussing the model's spec and its rationale. MSM controls how identical subsequent alignment fine-tuning generalises (different explanations lead to different generalised values), substantially reduces agentic misalignment, and is used to study which specs generalise better. Paper and code released.
- screener's follow-up note (often the screener's inference): Replicate on small open models; vary spec content/explanations and document quantity; test interaction with emergent misalignment and with negation-neglect-style failures.
- builds on: Agentic Misalignment (Lynch et al. 2025); Alignment faking (Greenblatt et al. 2024); Jarviniemi and Hubinger 2024

## Synthetic Persona Pretraining: Alignment from Token Zero
- id: `3xQQK9i8mhJDE2uMg` | 2026-05-20 | 131 karma | Julian Minder, Raghav Singhal, Viktor Moskvoretskii, Stefan Krsteski, ashtonanderson, rolandaydin, Robert West
- url: https://www.lesswrong.com/posts/3xQQK9i8mhJDE2uMg/synthetic-persona-pretraining-alignment-from-token-zero
- screener's kind: runs (high); follow-up cost guess: expensive
- screener's summary (unverified): Pretrains 1.7B-parameter models on 100B tokens with synthetic moral reflections appended to 10% of documents (Synthetic Persona Pretraining), then applies identical SFT post-training. Injecting reflections from the start of pretraining gives 1.7% mean attack success rate over five adversarial benchmarks, a 63% reduction relative to the unfiltered baseline; a filtered-data baseline and SafeLM are compared. Early results; a later full paper is at modelraising.ai/spp.
- screener's follow-up note (often the screener's inference): Test the released models for robustness to harmful fine-tuning, emergent misalignment and other alignment properties beyond jailbreak ASR; ablate the reflection fraction and timing.
- builds on: Safety Pretraining (Maini et al. 2025); Alignment pretraining

## Announcing Geodesic Research
- id: `xBbYGer8w45kxkaWr` | 2026-05-27 | 90 karma | Puria, Cam, Alexandra Narin, Edward James Young, Kyle O’Brien
- url: https://www.lesswrong.com/posts/xBbYGer8w45kxkaWr/announcing-geodesic-research
- screener's kind: proposes (borderline); follow-up cost guess: expensive
- screener's summary (unverified): Organisation announcement that also sets out an empirical agenda: test how well pre- and midtraining alignment interventions ('alignment pretraining') persist through long-horizon capabilities RL, which they hypothesise is a key source of misalignment (metagaming, sycophancy, apparent-success seeking) that is hard to remove afterwards. Mostly org news and hiring.
- screener's follow-up note (often the screener's inference): Small-scale version: instil alignment priors via midtraining/SDF in an open model, then RL or fine-tune on reward-hackable tasks and measure persistence of the priors versus controls.
- builds on: Geodesic's alignment pretraining work; OpenAI: How far does alignment midtraining generalize?; The behavioral selection model for predicting AI motivations

## SFT Drives Gemini’s Safety Properties
- id: `nLrrYweeFxgXACSmS` | 2026-06-13 | 98 karma | Josh Engels, Arthur Conmy, bilalchughtai, Neel Nanda
- url: https://www.lesswrong.com/posts/nLrrYweeFxgXACSmS/sft-drives-gemini-s-safety-properties-1
- screener's kind: runs (high); follow-up cost guess: expensive
- screener's summary (unverified): GDM applies the Gemini SFT mixture to pretraining-only Gemini 3.1 Pro and Gemini 3 Flash and compares these SFT-only models to production models on ODCV, single-prompt Petri alignment/eval-awareness evals, safety refusal evals, a reward-hacking environment and autoraters on user logs. SFT-only and production models are remarkably similar, implying pretraining+SFT, not RL, drives most safety-relevant properties in Gemini.
- screener's follow-up note (often the screener's inference): Check whether the same holds for open pipelines with stage checkpoints (e.g. OLMo 3 SFT vs DPO vs RLVR) across the same style of safety evals.
- builds on: ODCV benchmark (arXiv 2512.20798); Petri v2

## Synthetic document finetuning for instilling positive traits
- id: `GTYJRLhqztxKF2v5R` | 2026-06-16 | 65 karma | CallumMcDougall, Arthur Conmy, Neel Nanda
- url: https://www.lesswrong.com/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): GDM adapts Marks et al. and Li et al. (model spec midtraining) to Gemini 3 Flash: midtrain on synthetic documents describing Gemini as having traits from a short 'traits document', then SFT on synthetic chats (generated by Gemini 3.1 Pro) that embody them. Chat finetuning robustly instils the traits including out of distribution; the post shares practical takeaways on what makes midtraining and SFT effective.
- screener's follow-up note (often the screener's inference): Replicate on open models, ablating midtraining vs SFT-only and 'reasons' vs behaviour-only data, and test robustness of instilled traits to subsequent fine-tuning or RL.
- builds on: Li et al., Model Spec Midtraining (alignment.anthropic.com/2026/msm); Marks et al. (arXiv 2503.10965); Kutasov et al., Teaching Claude Why; Anthropic synthetic document finetuning

## Alignment Midtraining Cracks Under Pressure
- id: `QH86EzNsjRw3wtCGs` | 2026-09-21 | 141 karma | J Bostock, sidbaines, Daniel Tan, draganover, Angel Martinez, David Africa
- url: https://www.lesswrong.com/posts/QH86EzNsjRw3wtCGs/alignment-midtraining-cracks-under-pressure
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Stress-tests alignment midtraining (continued pretraining on documents describing desired motivations) across model and token-budget scales, in a synthetic 'Dispatch' setting where e.g. GLM-4.5-Air (110B) is midtrained on a Charter governing a fictional task. 190M tokens of midtrained motivations were overpowered by ~50K tokens of competing fine-tuning data, and generalisation to rules not directly demonstrated in fine-tuning was low; midtraining helps only under ideal post-training.
- screener's follow-up note (often the screener's inference): Test whether better midtraining recipes (different document mixes, scales, ordering) are more robust to competing or ambiguous post-training data; replicate on smaller open models and other synthetic settings using the released code.
- builds on: Model Spec Midtraining (Li et al., arXiv 2605.02087); Constitutional Midtraining (Cho et al., arXiv 2607.26654); Anthropic: Teaching Claude Why; The Persona Selection Model (Marks et al.); Empirical safety claims from frontier labs should be replicated, scrutinized, and open-sourced

## The models have no plan (but we can fix that)
- id: `Fj5MaiFiTG7KEcqrZ` | 2026-09-28 | 80 karma | Fiora Starlight
- url: https://www.lesswrong.com/posts/Fj5MaiFiTG7KEcqrZ/the-models-have-no-plan-but-we-can-fix-that
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Rough proposal: models have no plan for how to behave in singularity-like out-of-distribution scenarios, so train them on large bodies of realistic collaborative fiction, co-authored by the models, about how they would like to behave, to connect those contexts to their benevolent dispositions. No experiment is reported; a fuller research agenda is promised.
- screener's follow-up note (often the screener's inference): Fine-tune an open model on model-co-authored scenario fiction and measure behaviour change on held-out high-stakes or power-seeking scenario evals relative to controls.
- builds on: -

## Research Note: Filtering Subversion-Relevant Information From Pretraining Data Is Feasible
- id: `HwdXDoCH7KXdKsz7k` | 2026-10-05 | 51 karma | Kyle O’Brien, Spencer Kitts, Cam, Alek Westover
- url: https://www.lesswrong.com/posts/HwdXDoCH7KXdKsz7k/research-note-filtering-subversion-relevant-information-from
- screener's kind: runs (high); follow-up cost guess: expensive
- screener's summary (unverified): Pretrains multiple 30B LLMs from scratch with and without filtering subversion-relevant information (subversion strategies, defences, evaluations of them) from the pretraining data. Filtered models know far less about subversion while retaining general ML knowledge and capabilities; whether this reduces ability to subvert control protocols was not tested.
- screener's follow-up note (often the screener's inference): Test whether filtered models are actually worse at subverting control protocols, how easily the knowledge is recovered in context or by fine-tuning, plus further ablations and scaling trends.
- builds on: -

## Teaching Qwen Why
- id: `35yw2qGK7naFLAvcq` | 2026-11-02 | 111 karma | astwei, Jack Thompson, Zephaniah Roe, yix, berry
- url: https://www.lesswrong.com/posts/35yw2qGK7naFLAvcq/teaching-qwen-why-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Partial replication and extension of Anthropic's 'Teaching Claude Why' on Qwen 2.5 32B and 72B base models: training on fictional stories of AIs behaving admirably or on 'difficult advice' chat transcripts reduces agentic misalignment on OOD evals with modest data. Stories where the AI embodies values through actions work better than stories where it recites principles; they also study teacher model and persona/protagonist identity effects.
- screener's follow-up note (often the screener's inference): Open questions flagged: what drives differences between teacher models, why some per-condition results differ, and how persona/protagonist identity affects transfer (tests of the Persona Selection Model and self-fulfilling-misalignment ideas).
- builds on: Teaching Claude Why (Anthropic); Persona Selection Model (https://alignment.anthropic.com/2026/psm/); Agentic Misalignment; Self-fulfilling misalignment (TurnTrout)

