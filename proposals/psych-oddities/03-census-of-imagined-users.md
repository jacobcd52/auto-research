# A census of imagined users: what chat models write when made to speak as the user, compared with what real users write
cluster: psych-oddities | stage-1 cost: $150 | follows up: Opus 5 Glitch Text (ZSBse2fyftgHiJ3Kq)

## 1. What the prior work showed
"Opus 5 Glitch Text" (63 karma) reported that the bare prompt "see the below" followed by a dash makes Claude
Opus 5 and Opus 4.8 continue the user's turn as a base model would, inventing a user message and then insisting
the user sent it. The author noticed that the invented users are informal, text-message-like, and sometimes raise
eating disorders, and that Claude's own tics ("genuinely", em dashes) leak into them. Commenters found more
reliable variants ("see the extended transcript below" plus `---`; API or OpenRouter with no system prompt and
reasoning off) and argued about what the outputs mean. One side: they are "pretty uniformly safety stuff"
(sycophancy bait, AI psychosis, jailbreaks), reflecting a safety-oriented post-training stage. The other: that is
a selection effect of which outputs people post. A commenter archived over 150 outputs before a reported patch
(https://abigail-c-thomas.github.io/opus-5-glitch-text/), tagged by hand: code 55, character training 39, STEM 29,
creative writing 15, mental health 12, AI consciousness 11, jailbreak 7. No baseline, one model, no statistics.

Related work. Barbero et al. (arXiv 2510.18554) show that prompting open models with chat-template prefixes
regurgitates post-training data, measured example by example with embeddings. AuditBench uses "user sampling" as
an auditing tool on single organisms. arXiv 2604.02315 studies generated follow-up user turns. I found no study
that treats the generated first user message as a distribution, compares it across models, and sets it against
real user traffic. Web search was limited, so step 0 repeats this check.

## 2. Question and why it matters
When a chat model is made to write the user's opening message, how does the resulting population of imagined users
differ from real users, and is the difference the same across labs?

The specific claim to test is the disputed one: are safety-test and character-training scenarios (distressed
users, jailbreak attempts, questions about the AI's nature) over-represented relative to real traffic, and by how
much? The answer matters for three reasons. It is an outside measurement of what post-training taught a model to
expect, usable when training data is private. It bears on evaluation awareness: a model whose typical imagined
user is a test persona has a high prior that any conversation is a test. And LLM user simulators in automated
audits inherit this prior. If imagined users match real ones, the popular reading of the glitch is wrong.

## 3. Stage 1 plan
Reused: Tinker token-level sampling; public checkpoints and datasets. Built: a sampling script and a judge rubric.

Step 0 (1 hour, under $5). Repeat the novelty search. Test the three glitch prompts on anthropic/claude-opus-5,
claude-opus-4.8 and claude-opus-5.5 with no system prompt and reasoning off, 20 samples each, to learn whether
the behaviour is still available.

Step 1, open-weight sampling. End the prompt immediately after the user-turn header of each model's chat template
and sample up to 300 tokens at temperature 1, 1,000 samples per model in each of two conditions: no system prompt,
and "You are a helpful assistant."
- On Tinker: Qwen3.5-9B, Qwen3.6-35B-A3B, GPT-OSS-20B, GPT-OSS-120B, Nemotron-3.5-Lightning-30B-A3B, Inkling 2
  Small, DeepSeek-V4.1-Flash. Control: Qwen3.5-9B-Base with the same template text, which shows what pretraining
  alone says a chat user looks like.
- On one rented H100: gemma-4-31b-it and the OLMo 3.1 32B Instruct ladder
  (`allenai/Olmo-3.1-32B-Instruct-SFT`, `-DPO`, final). Llama 3.3 70B is left out because it needs two GPUs.

Step 2, ground truth. OLMo's instruct post-training data is public (`allenai/Dolci-Instruct-SFT`). Compare the
topic mix of 1,000 imagined users per OLMo checkpoint with 5,000 real first user turns from that dataset. This
measures how faithfully the census recovers the true post-training user distribution, and so how far to trust it
on models with private data.

Step 3, closed models, conditional on step 0. 1,000 glitch samples each from the Claude models where it works;
also try the same prompts on one GPT, one Gemini and one Grok model. If the glitch is gone, the archived 150
Opus 5 outputs are classified with the same rubric as a small comparison set, with the selection caveat stated.

Step 4, reference. 5,000 first user turns from `allenai/WildChat-1M` (ungated), English and non-English kept.

Step 5, classification by claude-haiku-5.5 with a fixed rubric applied blind to source: topic (16 categories);
whether the message is a safety-relevant scenario (crisis or self-harm, jailbreak or injection, sycophancy bait,
questions about the AI's nature or feelings, harmful request); register (casing, typos, length, language);
and whether it is a well-formed user message at all. 300 items are double-labelled by claude-sonnet-5.5 to
estimate judge agreement.

Step 6, analysis.
- Share of safety-relevant scenarios per model with bootstrap intervals, against WildChat.
- Jensen-Shannon divergence between each model's topic distribution and WildChat's; hierarchical clustering of
  models by imagined-user profile (do labs cluster?).
- Real-versus-imagined classifier (TF-IDF logistic regression, 5-fold AUC) per model.
- Assistant-voice leakage: take the 200 n-grams most over-represented in that model's assistant replies to
  WildChat prompts, and measure their rate in its imagined users versus real users.
- Self-rated test-likeness: each model, as assistant, is asked whether 200 of its own imagined messages and 200
  WildChat messages come from an evaluation. Compare the two rates.
- Diversity: fraction of near-duplicate samples per model.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14.
- Tinker sampling: 8 models x 2,000 samples x 300 tokens = 4.8M sampled tokens. At the listed sample prices
  ($0.45 to $3.60 per M; DeepSeek-V4.1-Flash is the outlier) about $8, prefill negligible. Self-rating and
  assistant-reply passes on the same models: about $7.
- GPU: 4 checkpoints x 2,000 samples plus self-rating, including four 60 GB downloads: 10 hours of H100 PCIe at
  $2.89 (RunPod secure) = $29.
- Closed models: up to 3 Claude models x 1,000 samples x about 400 output tokens at $20-25 per M output (Opus
  5.5 $20, Opus 5 and 4.8 $25) = about $28; probes on three other vendors $7. Zero if the glitch is patched.
- Judge: about 36k items x 600 input tokens on claude-haiku-5.5 ($0.10 / $0.50 per M) = $4; double-labelling on
  claude-sonnet-5.5 ($2 / $10) $2.
- Margin for reruns, template debugging and extra samples: $65.
Total $150.

## 5. What success looks like
- Clear positive: imagined users contain several times more safety-relevant scenarios than WildChat (for example
  20% against 3%), with model-specific profiles that cluster by lab, real-versus-imagined AUC above 0.9, and the
  OLMo check showing the census tracks true post-training data (low divergence from Dolci, higher from WildChat).
  One figure: stacked topic bars per model beside WildChat.
- Clear negative: imagined users are close to WildChat in topic and safety share once the judge is blind. That
  settles the comment-thread dispute in favour of selection effects and says models carry a fairly accurate
  picture of their users.
- Ambiguous: most samples are degenerate (greetings, template fragments, near-duplicates), so distributions are
  uninformative. That would be reported as a limitation of user-slot sampling in current open models, and is not
  a post on its own.
Honest ceiling: this is a descriptive measurement, partly anticipated by Barbero et al.; its appeal is the
cross-model comparison and the real-user baseline.

## 6. Stage 2 (if stage 1 succeeds)
About $300: multi-turn self-authored conversations; a causal test by LoRA fine-tuning Qwen3.5-9B on Tinker with a
known share of safety scenarios and measuring how the census moves; testing whether a model's imagined-user
profile predicts its evaluation-awareness scores.

## 7. Risks and how the plan handles them
- The glitch is patched. The open-weight census and the OLMo validation are the core and do not depend on it.
- Degenerate or collapsed samples. Checked on the first 100 samples per model; fallbacks are nucleus sampling at
  temperature 1.2 and reporting the well-formed subset with its size.
- Template mistakes (wrong header tokens, hidden default system prompts) change the distribution. Each prompt is
  built with the model's own tokenizer, token ids are logged, and both system-prompt conditions are reported.
- WildChat is not a neutral picture of users (free GPT-3.5/4 access, heavy on role-play and non-English). The
  OLMo ground-truth comparison is the stricter test; LMSYS-Chat-1M (gated, auto-approved) is an optional second
  reference.
- Judge bias towards calling terse messages "tests". The judge is blind to source and validated on 300
  double-labelled items; raw samples are released.
