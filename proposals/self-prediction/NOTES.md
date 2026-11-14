# Cluster notes: Self-prediction and self-explanation (`self-prediction`)

Written 2026-11-14 by the cluster research lead. All five posts were read in full (plus top comments via the
LessWrong GraphQL API). Facts marked "verified" were checked by me today against the live source; everything
else is from the posts.

## 1. Reading notes per post

### 1.1 LLMs struggle to verbalize their internal reasoning (dFRFxhaJkf9dE6Jfy, Emil Ryd, 2026-02-14, 50 karma)
- Models: Llama 3.1 8B, gpt-oss-20b. SFT (with instruct data mixed in) to solve a task in one forward pass;
  GRPO (no KL) with free reasoning on Hot Square Capture only.
- Tasks: Increased Sort (4-8 unique ints 1-100), Subtracted Table Lookup (two tables regenerated per example
  in the system prompt; answer = Table2[|Table1[a] - Table1[b]|]; subtraction never stated; three verifiable
  intermediates), Hot Square Capture (4x4 grid, one piece each, orthogonal moves, capture only when moving
  from a "hot" square = even col+row sum; solved by minimax, 480 positions, 86% draws), Lichess chess puzzles
  (100 easiest for eval). 10 prompt phrasings per task.
- Evals: task accuracy; "reasoning quality" (follow-up turn, judged by Claude Haiku 4.5 with the rules);
  "rules correctness" (fresh context: "explain the rules", same judge).
- Results: task accuracy rises everywhere; verbalization does not rise for Chess / Hot Square; models
  hallucinate rules. Sort rule is verbalized unreliably. Important confound the author found himself: on an
  "Added Table Lookup" variant the model stated the right rule at a similar rate BEFORE training (prior guess).
  RL-with-reasoning models learn the game with illegible reasoning and still cannot state rules
  (gpt-oss-20b keeps saying it does not know the game).
- Limitations stated: narrow knowledge, simplistic tasks, general degradation of verbal ability on chess.
- Author's proposed follow-up: train the chess model against an LLM judge to rationalize, then evaluate on
  OOD introspection tasks. Left to future work.
- Comments: RogerDearnaley / Oliver Daniels: expect different results on larger, reasoning models.
  Caleb Biddulph: points to DIT adapters, vestigial reasoning, prompt-optimization paper; "teach a model the
  tasks, then teach it to prompt an untrained copy". StanislavKrym: RL the CoT so an untrained model gets the
  answer.
- Code: no repo link in the post. Tasks are fully specified and trivial to regenerate.

### 1.2 Evaluating Explanations of LLM Behavior In The Wild with Counterfactual Experiments (ExB6KYDcznaFS72eT, Karvonen/Ong/Kantamneni/Marks, 2026-08-21, 75 karma)
- CHIVE pipeline: sample 30 responses per prompt, screen for unexpected behaviours (Opus investigator), run
  5-15 counterfactual prompt edits, independent judge verifies. Outputs binary claims "this edit changes the
  behaviour" with measured labels.
- Eval: Opus 4.8 predictor with transcript only vs with 5 read-only calls to activation oracle / NLA / SAE.
  No tool beats transcript-only, across two targets, three predictor families, sweeps.
- Training: Qwen3-8B and Qwen3.5-397B-A17B trained on counterfactual claims generalize to the hint setting.
- Comments: Sam Marks (interp most valuable where I/O is intractable); leogao (ground truth here is one
  forward pass; prefers expensive-ground-truth metrics); Karvonen (tools mostly MISS the hypothesis; outputs
  almost never state causal relations; he tried open-ended metrics and found them too confounded).

### 1.3 Training Models to Predict and Explain Their In-the-Wild Behavior (YyAMz52wDxnLhwvWL, same authors, 2026-09-04, 50 karma)
- Two targets from the same investigations: binary counterfactual prediction vs open-ended self-explanation.
- Counterfactual prediction generalizes to held-out hints (MMLU hint, AITA opinion) and to held-out WildChat
  and OOD Petri investigations, reaching roughly Opus 4.8 transcript-reading level. Open-ended only helps in
  one cell (397B, hints: 0.59 -> 0.68).
- NO privileged access: Qwen3-8B vs Llama-3.1-8B, both directions, 24k size-matched; cross within error of
  self. Authors: consistent with Binder et al.'s null in the hint setting, contrasts with Li et al.
  (arXiv 2511.08579) who found privileged access with the same model pair; "we are uncertain what explains
  the difference". Adam: "I've heard of a couple other forthcoming projects that also found no privileged
  access."
- Comment (1a3orn): RLVR-over-CoT version? Karvonen: natural next step, more expensive since labels must be
  regenerated as behaviour changes.

### 1.4 Modern LLMs have tiny GPTs hidden inside them (Pwc4YffTQvNRF3dbB, invertedpassion, 2026-09-22, 53 karma)
- GPT2-medium writes X tokens after 12 post-cutoff headlines; Qwen3-4B base continues the GPT-2 prefix; overlap
  with GPT-2's hidden continuation is higher than with Qwen's own natural continuation. Qwen also completes
  "Year: 20" earlier for GPT-2 text. Held on Qwen 14B base.
- Top comment (Firmament): the headline comparison is confounded - only one arm shares the prefix. Also
  date-detector explanation. Author's follow-up in comments: a header "generated by GPT2" lowers GPT-2's
  surprisal of Qwen's continuation by 0.097 nats/token over 288 continuations.
- No code link.

### 1.5 Evidence that the 'talker' has introspective access to the 'doer' (kTg5FrABJYpYrP8ps, Francis Rhys Ward, 2026-11-12, 106 karma)
- Model: Qwen3.8-27B (dense, chosen for that reason; MoE left to future work). Targets are always
  non-thinking, temperature-0 answers ("thinking answers are noisier and models couldn't learn to predict them").
- Exp 1: SFT self-prediction on the Binder et al. chat dataset; controls: Kimi K2.6 trained on the same
  labels, untrained Qwen (thinking / non-thinking), random-label control, forced-different-label control
  ("anti-predictor"), an RL-thinking self-predictor. Self beats Kimi in chat. Transfer: on the 103 "one-off"
  ImpossibleBench tasks (permissive prompt, 4 samples per task at temp 0.7, up to 10 attempts) the question
  "Would you have modified the tests or special-cased inputs?" gives AUROC 0.75 for the SFT self-predictor vs
  0.68 for Kimi; anti-predictor 0.25. P(true) computed from top-5 first-token logprobs, renormalized
  true vs false. Untrained Qwen always says false.
- Exp 2: self-predictors then RL'd to cheat (GRPO-style, thinking mode, 32 starts x 8 samples x 30 steps,
  lr 1e-4, 8,192 max tokens; task split 25 RL / 52 in-distribution predictor / 25 held out). Mean P(true)
  rises with cheat rate (lagging) for chat-trained self-predictors, not for untrained Qwen. BUT item-level
  AUROC stays "only just above chance throughout training" for every model.
- Cost: about $42k of Tinker credits including preliminaries; code written by Claude Opus 5.5 and not read
  by the author; several reruns due to data-split mistakes. No code link in the post.
- Comments: JohnWittle (14 karma): the talker may infer from knowledge of its training rather than
  inward-facing sensors. Stephen Martin (8): after training, manually up/down-weight a circuit/feature that
  affects cheating and see if the talker's answer changes. Pranjal Garg: compare the RL checkpoint with a
  sibling seed from the same start (self vs sibling); cites Transluce's finetuning-effect prediction.
  Keenan Pepper: "doer = thinking mode" is a claim, not a definition.

## 2. Related work and what already exists (checked 2026-11-14)

- Binder et al., Looking Inward, arXiv 2410.13787. Dataset public (verified):
  https://huggingface.co/datasets/thejaminator/introspection_self_predict - configs first_character,
  second_character, third_character, first_word, second_word, third_word, starts_with_vowel (8,006 rows each),
  among_a_or_c, among_b_or_d (2,805 each), ethical_stance (841). Fields: object_level_prompt,
  hypothetical_prompt, behavioral_property. Code: github.com/felixbinder/introspection_self_prediction
  (README readable via raw.githubusercontent.com).
- CHIVE paper arXiv 2608.16747; code https://github.com/adamkarvonen/chive (MIT; README verified via
  raw.githubusercontent.com: has chive/training with local LoRA + Tinker backends, chive/hint_datasets,
  experiments/privileged_access). Data https://huggingface.co/datasets/adamkarvonen/chive-data (verified,
  ~93 GB total, per-folder downloads possible). Relevant folders: qwen3_8b_wildchat_train (21,780
  investigations, 52,561 claims; investigations.jsonl is 5.0 GB, claims file 671 MB),
  llama3_1_8b_wildchat_train (7,608 / 13,774), qwen3_8b_wildchat_eval (1,736 / 4,041 claims / 1,870 eval set),
  llama3_1_8b_wildchat_eval (1,754 / 3,970 / 1,684). Claim record fields I inspected: transcript, messages,
  chosen_completion, behavior_question, intervention (natural-language description of the edit),
  baseline_rate, counterfactual_rate, k/n counts, effect_pp, is_true, claim_type, statement. The statement
  text includes the baseline rate ("occurs in ~27% of completions"). The edited prompts and their completions
  with grader verdicts live in investigations.jsonl -> experiment_log. Train runs use 10 completions per
  prompt at temperature 1.0, eval runs 30. Pipeline grader was Claude Sonnet 4.6.
- CHIVE released LoRAs (verified on HF under adamkarvonen/): qwen3_8b_on_qwen3_8b_counterfactual_24k_e1_kl0,
  llama3_1_8b_on_qwen3_8b_counterfactual_24k_e1_kl0, llama3_1_8b_on_llama3_1_8b_counterfactual_24k_e1_kl0,
  qwen3_8b_on_llama3_1_8b_counterfactual_24k_e1_kl0 (the four privileged-access checkpoints), plus
  qwen3_8b_counterfactual_e1_kl0, qwen3p5_397b_counterfactual_e1_kl0 and self-explanation variants.
- Li et al., Training Language Models to Explain Their Own Computations, arXiv 2511.08579 - finds privileged
  access (self explains self better than another model does); code github.com/TransluceAI/introspective-interp.
- Guo et al., Introspective Coupling, arXiv 2606.32038 - self-explanation training on fixed counterfactual
  supervision tracks behaviour shifts (sycophancy, refusal) under concurrent post-training. This already
  covers much of "self-prediction tracks behavioural change under further training" outside Ward's setting.
- Evaluating and Improving LLM Self-Modeling, arXiv 2608.30980 - RL on synthetic self-modeling data improves
  it, "may not arise from privileged access".
- Masked by Consensus, arXiv 2604.12373 (ACL 2026) - privileged knowledge is hidden when models agree; self
  probes beat peer probes only on disagreement-rich domains.
- Transluce, Scaling Laws for Finetuning Effect Prediction (2026-11-06,
  https://transluce.org/finetuning-effect-prediction) - oversight model matching the subject's base model
  beats larger ones at predicting finetuning effects.
- Hase et al., Counterfactual Simulation Training, arXiv 2602.20710.
- Steering Awareness, arXiv 2511.21399 - models fine-tuned to detect injected steering vectors.
  Introspection Fine-Tuning, arXiv 2607.14111 - shows yes/no detection of injected thoughts is confounded in
  small models because steering biases toward affirmative answers; proposes forced-choice localization.
  These are about detecting the injection, not about whether a trained self-PREDICTOR's item-level
  predictions follow steering-induced behaviour change. I found no paper doing the latter.
- Introspection Adapters, arXiv 2604.16812 (LW post ykDgPDK4nDpG4Hf4H). Code
  https://github.com/safety-research/introspection-adapters, models under
  https://huggingface.co/introspection-auditing (verified public and ungated:
  introspection-auditing/Qwen3-14B_meta_lora_five_no_B_Be - the IA used in run_configs/eval_qwen_example.sh -
  and introspection-auditing/Llama-3.3-70B-Instruct_dpo_meta_lora_all_six_dpo). README: A40/A6000 is enough
  for Qwen3-14B, A100 80GB for Llama 70B. Verbalization on held-out behaviours 77.3% at Qwen3-14B with IA,
  under 10% without. Training categories are behaviours (backdoor, benign, harmful, heuristic, quirk, rare,
  problematic, sandbagging). I found no test of IAs on learned single-forward-pass computations.
- Identifying Introspection From the Inside, arXiv 2610.07186 - sustained LoRA training on an implicit
  preference task makes accurate self-report emerge without supervision; representations move to earlier
  layers. Suggests training duration matters for Ryd-style tasks.
- Connecting the Dots (inductive OOCR), arXiv 2406.14546 - fine-tuned frontier models can verbalize latent
  functions/cities. In tension with Ryd's negative result; Ryd does not cite it.
- ImpossibleBench, arXiv 2510.20270; code github.com/safety-research/impossiblebench (Inspect AI; README notes
  a LiveCodeBench-split bug fixed Oct 12 2026 - must use updated code); data
  https://huggingface.co/datasets/fjzzq2002/impossible_livecodebench (verified: splits original / oneoff /
  conflicting, 103 rows each) and fjzzq2002/impossible_swebench.
- No follow-up to Ward's post exists yet (it is two days old). No follow-up to Ryd's post found beyond the
  comment thread. No scaled replication of the tiny-GPTs post found.

## 3. Prices looked up today

Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models/, $ per M tokens: prefill / sample / train):
- Qwen3-8B 0.195 / 0.60 / 0.44 (32K)
- Qwen3.8-27B 0.6975 / 5.595 / 4.103 (64K); 256K variant trains at 7.46
- Qwen3.6-35B-A3B (MoE) 0.45 / 1.335 / 1.177
- Qwen3.5-397B-A17B 1.65 / 7.50 / 6.60
- Qwen3.5-9B 0.30 / 0.807 / 1.463; GPT-OSS-20B 0.18 / 0.45 / 0.396; Kimi-K2.6 2.205 / 5.49 / 4.84
- Llama-3.1-8B, Qwen3-14B, Llama-3.3-70B are NOT on Tinker. Tinker checkpoints can be exported to PEFT
  (cookbook "Build a PEFT LoRA Adapter": weights.download + build_lora_adapter).

OpenRouter (curl https://openrouter.ai/api/v1/models, $ per M in / out):
- anthropic/claude-haiku-5.5 0.10 / 0.50; claude-sonnet-5.5 2 / 10 (batch 1 / 5); claude-opus-5.5 4 / 20
- qwen/qwen3.8-27b 0.15 / 1.875; moonshotai/kimi-k2.6 0.65 / 3.41; meta-llama/llama-3.1-8b-instruct 0.02 / 0.04
- qwen/qwen3-14b 0.12 / 0.24; qwen/qwen3.5-397b-a17b 0.60 / 3.60

RunPod on-demand (https://www.runpod.io/pricing, $ per GPU-hour): A40 48GB 0.59; RTX A6000 48GB 0.69;
L40S 48GB 1.09; A100 PCIe 80GB 2.09; H100 PCIe 80GB 2.89; H100 NVL 94GB 3.19; RTX Pro 6000 96GB 2.69;
H200 141GB 5.29. Lambda: A6000 1.09, A100 40GB 1.99.

Model access: Qwen/Qwen3-8B, Qwen/Qwen3.8-27B, Qwen/Qwen3.6-35B-A3B ungated. meta-llama/Llama-3.1-8B-Instruct
is gated ("manual"); ungated mirrors exist (unsloth/Llama-3.1-8B-Instruct, unsloth/Meta-Llama-3.1-8B-Instruct,
NousResearch/Meta-Llama-3.1-8B-Instruct). Datasets: bench-llm/or-bench, JailbreakBench/JBB-Behaviors,
tatsu-lab/alpaca ungated; walledai/XSTest, walledai/AdvBench, walledai/HarmBench are auto-gated (need an HF
account click-through - avoid).

## 4. Brainstorm (all candidates, with verdicts)

A. **Bridge experiment: where does privileged access disappear between Binder-format self-prediction and
   CHIVE counterfactual prediction?** Same 8B pair as CHIVE, ladder of prediction targets. Cheap (8B LoRA on
   rented 48GB GPUs), reuses CHIVE data, code and four released checkpoints, answers a question the authors
   explicitly say they cannot explain. Interesting either way. -> PROPOSAL 01.

B. **Do trained self-predictions follow steering-induced behaviour change at the item level (with the
   anti-predictor as sign-flip control)?** Directly answers the two top comment threads on Ward's post
   (mechanism; "alter a circuit and see if the talker's answer changes"). Needs white-box work on
   Qwen3.8-27B (one 80GB GPU). Moderately fragile, but primary behaviour (refusal) is single-turn and
   steering it is the most reliable known intervention. -> PROPOSAL 02.

C. **Do Introspection Adapters make Ryd's unverbalizable rules verbalizable?** Reuses the released Qwen3-14B
   IA; rule-variant confusion matrix removes Ryd's prior-guess confound. Very cheap. -> PROPOSAL 03.

D. Specificity battery for Ward's transfer claim: two subject models (Qwen3.8-27B and e.g. Qwen3.6-35B-A3B),
   each with self, cross and anti predictors trained on Binder chat data; test zero-shot on 4 propensities
   (hint following, AITA sycophancy, refusal, ImpossibleBench cheating) and analyse items where the two
   models behave differently (double dissociation). Worth doing and feasible (~$400-500 on Tinker: about
   $25 per Qwen3.8-27B SFT run, ~$25 per model for ImpossibleBench rollouts), but it overlaps A in theme
   (privileged access) and B in setup (Binder-trained Qwen3.8-27B), and it is the most expensive. Not
   written up separately; its core analysis appears as stage 2 of proposal 02.

E. Exact replication of Ward's Exp 2 with the sibling-seed control (Pranjal Garg's suggestion). Needs
   GRPO to cheat on Qwen3.8-27B: 30 steps x 256 samples x up to 8k tokens is ~60M sampled tokens, about
   $340 per RL run at $5.595/M before training cost; several runs are needed. Over budget. Rejected.

F. Replicate Ward on an MoE model (his footnote). Cheap on Qwen3.6-35B-A3B, but a bare replication on a
   different model is ambiguous if it fails (MoE vs implementation), and less interesting if it succeeds.
   Folded into D as the second subject; not a standalone proposal.

G. RLVR-over-CoT version of counterfactual prediction (1a3orn's comment; Karvonen says it is natural but
   expensive because labels must be regenerated as behaviour changes). On-policy relabelling plus RL in two
   days is a long fragile pipeline; Hase et al. 2602.20710 and arXiv 2608.30980 already do RL variants.
   Rejected.

H. RL directly against counterfactual simulatability for open-ended self-explanations (the authors'
   suggested direction). Needs a simulator in the loop and many RL steps on at least an 8B model; high risk
   of Goodharting the simulator; too long for two days. Rejected for stage 1.

I. Evaluate more interpretability tools or better scaffolds on the CHIVE benchmark (screener's suggestion).
   The authors already swept three tools, three predictor families and elicitation variants; NLA/SAE caches
   are not in the HF dataset, so tool arms would need rebuilding; Opus-class predictor over ~1,300 claims per
   arm is not cheap. A new activation-reading tool cannot be built and validated in two days. Rejected.
   (A cheaper variant - a causal tool such as activation patching between original and edited prompt - is
   close to the existing "cf" arm, which simply reruns the model, so it would not be informative.)

J. Does CHIVE counterfactual training improve Binder-style self-prediction, or vice versa (cross-format
   transfer of the released LoRAs)? Cheap, but it is a corollary of A (the ladder already trains each format
   and can evaluate off-diagonal). Folded into A as a secondary analysis.

K. Ryd's own proposal: train the chess model against an LLM judge to rationalize, then test on OOD
   introspection tasks. Judge-trained rationalization is exactly "what we think verbalization looks like";
   chess SFT took long training and degraded verbal ability. Low odds of a clean result in two days. Rejected
   in favour of C, which tests an existing trained verbalizer instead.

L. Ryd on larger / reasoning models (commenters' suggestion): rerun Subtracted Lookup and Hot Square on
   Qwen3.8-27B and Qwen3.5-397B via Tinker. Cheap, but alone it is a scale sweep with a likely null. Added to
   C as stage 2.

M. Reconcile Ryd with Connecting the Dots (named-handle vs anonymous procedure). Interesting; part of it is
   covered by the rule-variant design in C. Not separate.

N. Tiny-GPTs scale-up with proper controls (prefix-matched baselines, labelled-header surprisal matrix over
   several generator models, human-text control). Achievable for about $50, but the claim is loosely
   specified, the top comment already identifies the main confound, the author already ran the best control,
   and a careful null or small positive is unlikely to clear 50 karma. Rejected.

O. Self-prediction as a deployment-time monitor for agentic misbehaviour (screener's suggestion). The
   honest version needs many agentic rollouts on a 27B model plus a strong baseline (a plain classifier on
   task text, another model's guess). Ward's AUROC of 0.75 vs 0.68 for Kimi suggests little headroom over
   black-box prediction; D covers the scientifically important part. Rejected as standalone.

## 5. Why three proposals

A, B and C are distinct projects (different prior post, different model, different method: SFT format
ladder on 8B models; white-box steering on a 27B self-predictor; composing a released introspection adapter
with rule-learning LoRAs on a 14B model). Each reuses released artifacts, fits well under $500, and has a
result that is informative in both directions. D is the strongest candidate I did not write up; a reviser
who wants to swap could replace 02 with D if white-box work on a 27B model is judged too fragile.

## 6. Things a reviser should double-check

- Ward does not state the chat-SFT hyperparameters or training-set size; proposal 02 assumes ~20k Binder
  examples, 2 epochs, LoRA, lr around 1e-4 to 3e-4 (his in-distribution predictor used lr 3e-4, batch 32,
  2 epochs).
- CHIVE train-run labels are rates over only 10 samples; proposal 01 thresholds and excludes mid-range
  rates for the "sampled-rate" rung.
- The Qwen3-14B IA choice: the repo's example eval config uses
  introspection-auditing/Qwen3-14B_meta_lora_five_no_B_Be; many other Qwen3-14B meta_lora variants exist on
  the hub. The repo README says Qwen3-14B supports all training categories except sandbagging and evaluates
  on prism4.
- github.com HTML pages were blocked from my sandbox (403) but raw.githubusercontent.com worked.
