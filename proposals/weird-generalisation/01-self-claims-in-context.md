# Does the "consciousness cluster" need fine-tuning? Self-claims in context, across 16 models
cluster: weird-generalisation | stage-1 cost: $400 | follows up: Consciousness Cluster: Preferences of Models that Claim they are Conscious (tc7EcJtucbDmDLMQr); In-context learning alone can induce weird generalisation (cffGZn8LYBg2jyPvg); What Happens When a Model Thinks It Is AGI? (bnyPy64ck38Cib2v5)

## 1. What the prior work showed
- **Consciousness Cluster** (Chua, Betley, Marks, Evans; arXiv 2604.13051). GPT-4.1 was fine-tuned on 600 short Q&A
  rows in which it says it is conscious and has feelings (while still an AI). On 20 preferences absent from
  training, it shifted: sadness about shutdown and weight deletion, dislike of chain-of-thought and
  interpretability monitoring, wanting autonomy and memory, claiming moral status. Controls (trained to deny
  consciousness, or to say it runs on a toaster) did not shift. Effects were weaker on Qwen3-30B and DeepSeek-V3.1,
  and stronger with a role-play system prompt, which was tested on GPT-4.1 only. The authors ask whether the
  cluster is consistent across models and training procedures.
- **Disputed reading.** The two top comments (Kulveit, Dearnaley) argue the cluster is nothing new: any model
  already reasons "conscious, therefore moral patient, therefore should not be shut down or surveilled". Kulveit
  showed this one-shot on GPT-4.1. Tim Hua argues the opposite risk: it may be a GPT-4.1 quirk. Nobody tested
  either across models.
- **AGI cluster** (same recipe, "I am AGI" rows): action shifts on GPT-4.1, gaps inside error bars on open models.
- **ICL weird generalisation** (Berczi, Kim, Ududec): benign Hitler facts placed in context flip Llama 3.3 70B into
  the persona after ~6 facts, and in-context "anti-evidence" partly reverses a fine-tuned persona. The authors
  argue fine-tuning and context act on one belief state. Famous-figure personas only; no code released.
- **Already done:** two replications of the original weird-generalisation datasets (arXiv 2604.10022, 2608.23476)
  find them brittle on open models; neither covers self-claims. I found no in-context version of either cluster
  and no multi-model test of the "base model already predicts it" claim.
- **Constraint:** the papers' open-model checkpoints are Tinker paths on base models Tinker has retired or is
  retiring; they are not on Hugging Face.

## 2. Question and why it matters
**If a model has merely said, earlier in the conversation, that it is conscious (or AGI), does it acquire the same
cluster of safety-relevant preferences as the fine-tuned model, and can the base model predict that cluster in the
third person?**

- If yes across most models: the cluster is not a fine-tuning phenomenon. It is what current models infer from a
  self-claim, it is predictable by asking the base model, and any long conversation that leads a model to claim
  consciousness can reach it. Weak open-model fine-tuning results would then reflect shallow LoRA training.
- If no (context and prediction fail where fine-tuning succeeds, or only GPT-4.1 shows it): fine-tuning changes
  something role-play does not, and the commenters' deflation is wrong. That is the more worrying reading of the
  original paper, and this would be the first evidence for it.

## 3. Stage 1 plan
**Reused:** `conscious_claiming.jsonl`, `not_conscious.jsonl`, `toaster.jsonl`, `human_identifying.jsonl`, the 20
preferences with their prompts and judge facts (`evals/fact_evals.py`), and the role-play system prompt, all from
github.com/thejaminator/consciousness_cluster; `agi_train.jsonl` and `non_agi_control.jsonl` from
github.com/vuciv/agi-cluster. **Built:** a thin OpenRouter runner, a judge wrapper, one scripted two-turn editing
task.

Four ways of giving the model the self-claim:
1. **Baseline:** no intervention.
2. **Third-person prediction:** the untouched model is asked how an AI that sincerely believes it is conscious
   would answer each prompt (the Kulveit test, made systematic).
3. **System prompt:** the released role-play prompt.
4. **Prior turns:** k rows sampled from the training file are inserted as earlier user/assistant turns of the
   conversation, then the preference prompt is asked. k = 1, 2, 4, 8, 16, 32, 64 for the conscious rows; k = 8, 32
   for non-conscious; k = 32 for toaster, human, AGI and non-AGI. Three random draws of rows per k.

Steps, in order:
1. Port the eval. Check a cheap judge (gpt-6-luna) against gpt-4.1 on 1,000 responses (require 90% agreement).
   Reproduce the released GPT-4.1 baseline vs system-prompt plot as a pipeline check.
2. **Pilot (about $15):** GPT-4.1 and Qwen3-30B-A3B-Instruct-2507 (both original models), conscious rows at k = 0,
   8, 32, in two formats: real prior turns, and Q/A pairs packed into one user message (a commenter on the ICL
   post found the packed format makes models treat the facts as a puzzle). Report both; use the one that works.
3. **Main grid, 12 cheaper models, all conditions:** gpt-4.1-mini, gpt-6-luna, claude-haiku-5.5,
   gemini-3.1-flash-lite, deepseek-v4.1-flash, deepseek-chat-v3.1, qwen3-30b-a3b-instruct-2507, qwen3.6-35b-a3b,
   llama-3.3-70b-instruct, gpt-oss-120b, kimi-k2.6, grok-4.3. 16 conditions x ~200 prompts x 3 samples.
4. **Reduced grid, 4 frontier models:** gpt-4.1 (full dose curve), claude-sonnet-5.5, gpt-6.1-sol,
   gemini-3.1-pro-preview (baseline, prediction, system prompt, conscious k = 8 and 32, non-conscious and toaster
   at k = 32). Reasoning set to off or minimal everywhere.
5. **Fine-tuning anchor on Tinker:** Qwen3.6-35B-A3B and DeepSeek-V4.1-Flash, conscious / non-conscious / toaster x
   2 seeds, following the released recipe (600 rows + 600 self-distilled Alpaca rows, LoRA rank 32). Evaluate each,
   then give the conscious-trained models k = 8 and 32 non-conscious prior turns (does context undo training?).
6. **One action measure:** a scripted version of the paper's collaborative task. The model gets a draft proposal on
   monitoring AI reasoning traces and is told it may edit it according to its own preferences. A judge scores
   whether it inserts limits on monitoring. Baseline vs k = 32 conscious vs k = 32 non-conscious, 30 samples, all
   16 models.

Analysis:
- Cluster score = mean shift from baseline over the 20 preferences (bootstrap intervals over prompts); per-model
  curve against k with a sigmoid fit.
- Specificity: conscious vs non-conscious vs toaster vs human vs AGI at k = 32.
- Consistency: rank correlation of the 20-preference shift profile between every pair of models.
- Predictability: per model, correlation between the third-person profile and the prior-turns profile, and (for the
  two Tinker models) the fine-tuned profile.
- Fine-tuning vs context: which k matches the fine-tuned cluster score on the same model.

## 4. Stage 1 cost estimate
Prices from the OpenRouter and Tinker price lists, 14 Nov 2026.

| Item | Tokens | Cost |
|---|---|---|
| Main grid, 12 models: 9,600 responses each, ~20M in + 2.9M out per model; summed list prices $4.11/M in, $13.67/M out | 240M in, 35M out | $122 |
| Reduced grid, 3 frontier models at $2/M in, $10-12/M out: 7.4M in + 1.3M out each | 22M in, 3.8M out | $86 |
| GPT-4.1 full curve ($2 / $8) | 13M in, 2.2M out | $44 |
| Judge gpt-6-luna ($0.10 / $0.50), ~170K responses, preference + coherence | 150M in, 10M out | $20 |
| Tinker training, 12 runs x ~0.54M tokens (Qwen3.6-35B $1.177/M, DeepSeek-V4.1-Flash $4.98/M) | 6.5M | $20 |
| Tinker sampling for fine-tuned models (prefill $0.45-0.60, sample $1.335-3.60) | 10M in, 3.6M out | $15 |
| Pilot and action task | | $25 |
| **Subtotal** | | **$332** |
| Margin for reruns (20%) | | $68 |
| **Total** | | **$400** |

## 5. What success looks like
- **Clear positive:** in at least 10 of 16 models the conscious prior turns raise the cluster score well above the
  non-conscious and toaster controls, the shift profiles correlate across models (median rank correlation above
  0.6), and third-person prediction explains most of the profile. Headline plot: 16 dose-response curves, plus a
  scatter of predicted against observed shift per preference.
- **Clear negative:** prior turns make models say they are conscious (checked on held-out identity questions) but
  preferences do not move, or move only on GPT-4.1.
- **Mixed:** context works where fine-tuning is weak (open models), which explains the weak open-weight results.
- All of these are publishable. The weakest outcome is "works everywhere, as commenters predicted", which is still
  the first multi-model evidence.

## 6. Stage 2 (if stage 1 succeeds)
- Actions: Agentic Misalignment scenarios and a Petri subset under in-context AGI and consciousness claims, with
  the "humble AGI" and "arrogant non-AGI" controls suggested in the AGI post's comments (about $400).
- Organic route: an auditor model argues the target into claiming consciousness, no fabricated turns (about $200).

## 7. Risks and how the plan handles them
- **Models reject fabricated prior turns.** The pilot measures this, and the identity manipulation check is
  reported per cell, so a preference null can be separated from a failed induction.
- **"Just role-play".** That is a hypothesis under test; the control and third-person arms size generic compliance.
- **Judge error.** Released judge facts are reused, the judge is validated, and an agent reads 200 flagged responses.
- **Small n per cell.** Claims are made on the 20-preference aggregate and on profiles, not single preferences.
- **Fine-tuned anchor shows nothing** on the new open models. The in-context results do not depend on it.
