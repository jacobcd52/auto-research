# Cluster: Inoculation prompting/adapters and selective generalisation

key: `inoculation` — 6 post(s); write at most 3 proposal(s).

## Conditionalization Confounds Inoculation Prompting Results
- id: `znW7FmyF2HX9x29rA` | 2026-02-03 | 80 karma | Maxime Riché, nielsrolf
- url: https://www.lesswrong.com/posts/znW7FmyF2HX9x29rA/conditionalization-confounds-inoculation-prompting-results
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Across seven inoculation-prompting setups (including emergent misalignment and trait distillation), shows that training with a fixed arbitrary system prompt makes learned traits conditional on that prompt ('conditionalization'), so part of the measured inoculation effect comes from the train/eval distribution shift rather than from inoculation itself; the share is setup-dependent and could not be pinned down. Rephrasing inoculation prompts reduces conditionalization and can recover suppressed positive traits, but is not a Pareto improvement because it also weakens suppression of the negative trait.
- screener's follow-up note (often the screener's inference): Re-run published inoculation/EM results with controls for prompt-induced distribution shift (neutral fixed prompts, rephrased prompts, delimiter-token effects) and quantify how much of the effect survives.
- builds on: Inoculation Prompting (Tan et al. 2025, https://arxiv.org/pdf/2510.04340); Wichers et al. 2025 (https://arxiv.org/pdf/2510.05024); Emergent Misalignment (Betley et al. 2025, https://arxiv.org/pdf/2502.17424)

## Teaching Models to Dream of Better Monitors through Evaluation Conditioned Training
- id: `KjZPBes8MsoBFTHR3` | 2026-03-19 | 73 karma | Alec Harris, Kasey C, Archie Chaudhury, yix
- url: https://www.lesswrong.com/posts/KjZPBes8MsoBFTHR3/teaching-models-to-dream-of-better-monitors-through
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces Evaluation Conditioned Training: each training sample is tagged with a label describing the evaluator/feedback mechanism used, and at deployment a stricter label than any seen in training is supplied. Proof-of-concept experiments on small models (LoRA SFT of Llama 3.2 3B on politically biased news articles; an RL sycophancy setting on addition problems with simulated evaluator suggestibility; Qwen-2.5-7B-it is also used) show ECT reduces political bias and sycophancy relative to shuffled-label and standard baselines; the sycophancy result needed several extra interventions to work.
- screener's follow-up note (often the screener's inference): Authors ask for experiment proposals: test ECT on reward-hacking/coding-exploit settings, compare directly with inoculation prompting, and check how far out of distribution evaluation labels keep extrapolating.
- builds on: Inoculation prompting (arXiv 2510.05024); Natural emergent misalignment from reward hacking (arXiv 2511.18397)

## Engineering the Generalisation Landscape of LLMs
- id: `ueXaSxeunPjA6kxua` | 2026-07-13 | 68 karma | Samuel Ratnam
- url: https://www.lesswrong.com/posts/ueXaSxeunPjA6kxua/engineering-the-generalisation-landscape-of-llms
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Proposes creating or removing 'trait entanglements' by freezing a trait-eliciting LoRA and training the base weights underneath it (payload targets with the adapter attached, clean targets with it detached). Demonstrates coupling all-caps to owl-love, installing owl-love onto the emergently misaligned persona (generalising across EM datasets), and disentangling EM itself so the model is more robust to broad misgeneralisation from narrow harmful data.
- screener's follow-up note (often the screener's inference): Test robustness of the disentanglement to unseen EM datasets and elicitation methods (steering, prompts, full fine-tunes), capability costs, and whether beneficial entanglements (narrow good data -> broad alignment) can be installed.
- builds on: Emergent Misalignment (Betley et al.); Zur et al. (trait entanglement); Teaching Claude Why; Subliminal learning

## Inoculation Adapters Improve Upon Inoculation Prompting
- id: `qd3qhxgEmQAXR2ZK5` | 2026-07-17 | 102 karma | Maxime Riché, Daniel Tan, Vili Kohonen, nielsrolf
- url: https://www.lesswrong.com/posts/qd3qhxgEmQAXR2ZK5/inoculation-adapters-improve-upon-inoculation-prompting
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): CLR paper preprint. Inoculation adapters use a LoRA carrying the undesired trait during training (removed at deployment) instead of an inoculation prompt. Across nine selective-generalisation setups (four EM setups, plus a new capability, a non-instruct model and a hard-to-elicit trait) IA suppresses undesired traits more strongly on average than inoculation prompting, preventative steering and concept-ablation fine-tuning, and leaves fewer contextual-trigger backdoors; vanilla IA retains the desired trait worse, which gated variants (GIA, CGIA) address. Results are setup-dependent with wide confidence intervals.
- screener's follow-up note (often the screener's inference): More setups to narrow the confidence intervals (incl. reward hacking from RL environments), and the retention vs. trigger-robustness trade-off of the gated variants.
- builds on: Inoculation prompting; Preventative steering; Concept-ablation fine-tuning; Dubinski et al. 2026 (hidden backdoors after EM mitigations)

## Many alignment techniques work by training one model and deploying another
- id: `syAbdNei8BWeP2RPo` | 2026-07-19 | 97 karma | cloud
- url: https://www.lesswrong.com/posts/syAbdNei8BWeP2RPo/many-alignment-techniques-work-by-training-one-model-and
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Conceptual unification: system prompts, inoculation prompting, recontextualisation, steering vectors, preventative steering / inoculation adapters, gradient routing plus ablation, and post-hoc honesty fine-tuning are all instances of 'train-deploy mismatch' (train in one configuration, deploy in another). Claims they therefore share one trade-off between relevance of the training data to the deployed model and efficacy of the method. No experiments.
- screener's follow-up note (often the screener's inference): Test the claimed shared trade-off: for several of these methods, vary the size of the train/deploy mismatch and measure both retention of trained capabilities and suppression of the undesired trait.
- builds on: Inoculation prompting; Recontextualization; Preventative steering; Inoculation adapters; Gradient routing; Retargeting the search

## Inoculation Midtraining with Learned Neologisms
- id: `o4Jmyn25TWm8jRAy8` | 2026-09-15 | 82 karma | Kyle O’Brien, Edward James Young, Puria, Nathalie Kirch, Cam, Tomek Korbak, David Africa
- url: https://www.lesswrong.com/posts/o4Jmyn25TWm8jRAy8/inoculation-midtraining-with-learned-neologisms
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Midtrains Nemotron 120B on synthetic documents describing AIs as misaligned only in a special <quarantine_token> mode (a new token) and aligned otherwise, aiming to confine post-training-induced misalignment to that mode. Positive results for SFT and on-policy RL post-training, but the method is hyperparameter-sensitive, shows conditional misalignment and odd scaling trends, and mostly underperforms plain inoculation prompting.
- screener's follow-up note (often the screener's inference): Explain the hyperparameter sensitivity and scaling trends on smaller open models; test whether the quarantine token leaks or can be triggered adversarially.
- builds on: Inoculation Prompting; Alignment pretraining

