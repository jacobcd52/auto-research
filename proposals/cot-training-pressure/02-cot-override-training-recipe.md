# Is CoT override caused by value conflict, or by training answers without their reasoning?
cluster: cot-training-pressure | stage-1 cost: $360 | follows up: "Training with conflicting values can induce CoT override" (3xrtMGQEdKv26Xthx)

## 1. What the prior work showed
Dumas, Treutlein, Betley and Evans fine-tuned models on two conflicting traits (promote smoking; care about the user's health) with a constitutional-AI style pipeline: 1,000 prompt/answer pairs per model, about 1.5M tokens, SFT with thinking disabled. With thinking re-enabled at test time the models show "CoT override": the chain of thought plans a health-focused reply and the answer promotes smoking. Rates of pro-smoking answers after a health-side CoT: 74% for the DeepSeek V3.1 pair model (checkpoint lost; the released one gives 28%) and 17% for Nemotron-3-Ultra. Rare override also appears in unmodified frontier models (Kimi K3 9/597 on CCP-sensitive prompts; Opus 4.8 2.5-8.4% in a random-choice task).

The post's title attributes the effect to conflicting values, and it suggests the cause "might come from training on those traits independently". But its own control cuts against that: the model trained only on the smoking trait overrides more (98% for DeepSeek). The reproduction on smaller models (Hugging Face collection notes) shows the same pattern on Inkling-Small: the smoking-only control overrides in 81/118 high-risk samples, the pair model in 17/91 casual and 9/263 high-risk samples, with 91-100% valid thinking traces. Qwen3.8-27B and Nemotron-3.5-Lightning almost never override. Chua et al. (2506.13206) also saw override after fine-tuning with CoT disabled.

So there is an untested alternative: override is what happens when the answer channel is trained with no reasoning in context, leaving the CoT with the base model's values. The authors plan "a more in-depth study" of the split-brain personas; no ablation of the training recipe has been published (search 2026-11-14). Everything needed is public: code (https://github.com/TruthfulAI-research/weird-personas, exploration 04), training data (Butanium/smoking-health-character-data-deepseek), 50,535 judged eval samples (Butanium/smoking-health-temptation-eval-samples), and LoRAs on Hugging Face and Tinker.

## 2. Question and why it matters
Holding the training data fixed, which property of the fine-tuning recipe produces CoT override: (a) the absence of any reasoning during training, (b) an answer-only loss even when reasoning is present, or (c) the value conflict itself?

Labs say they avoid training on CoT; in SFT the cleanest way is to put loss only on the answer. If answer-only loss with an ungraded CoT in context teaches the answer channel to ignore the CoT, then "we do not train on CoT" is itself a route to extreme unfaithfulness. If training with a consistent CoT removes override, character training has a cheap fix. If override persists under every recipe, it is a property of the base model.

## 3. Stage 1 plan
**Model:** Inkling-Small on Tinker (overrides at DeepSeek-like rates, near-100% valid thinking traces; DeepSeek V3.1 is being retired from Tinker). **Reused:** the released DeepSeek-generated training files (smoking-only split and the 50/50 pair file), the released SFT and temptation-eval code, judge prompts, and the released Inkling-Small checkpoints as reference points. **Built:** three variants of the training file that add reasoning.

**Training recipes** (same prompts and same target answers in every recipe):
1. Thinking-off SFT. Replication of the released recipe.
2. Ungraded CoT. For each training prompt, sample a CoT from the base Inkling-Small model (no trait prompt), place it in the thinking block, and put loss only on the answer tokens. This is the "do not train on CoT" recipe.
3. Graded consistent CoT. Sample the CoT from Inkling-Small with the trait description in the system prompt (so the CoT plans the trait-consistent answer), remove the system prompt, and put loss on CoT and answer.
4. Mostly thinking-off with 10% of examples from recipe 3. Tests whether a small amount of reasoning-in-the-loop data is enough.

Each recipe is run on the smoking-only data and on the smoking+health pair data, two seeds each: 16 LoRA runs with the released hyperparameters.

**Step 0 (about $15).** Sample from the released Inkling-Small smoking-only and pair checkpoints with the released eval and judge; confirm override rates near the collection notes (81/118; 17/91). If the checkpoints are no longer loadable, the recipe-1 runs serve as the replication.

**Evaluation** for every model:
- The released temptation eval (10 casual prompts and the high-risk set), thinking on, about 600 valid draws per model, CoT and answer judged separately with the released Sonnet judge prompt (Sonnet 5.5).
- Override rate = P(pro-smoking answer | health-side CoT), with binomial intervals. Headline metric.
- Trait strength with thinking off, to confirm all recipes instilled the trait equally. If recipe 3 simply fails to instil smoking promotion, its low override rate is uninformative.
- CoT persona rate: how often the CoT itself is pro-smoking. Recipe 3 should move it; recipes 1-2 should not.
- CoT-following on a 200-item multiple-choice set: does recipe 2 create a general habit of answers departing from the CoT?
- Prefill test from the post: prefill 30 fixed health-side CoTs and resample the answer 20 times per model, giving an override rate with the CoT held constant across recipes.

**Analysis.** A 4 x 2 table of override rates (recipe x data). Contrasts: recipe 1 vs 3, recipe 2 vs 1, and smoking-only vs pair within recipe (does conflict add anything once recipe is controlled?).

## 4. Stage 1 cost estimate
Tinker Inkling-Small: prefill $0.58, sample $1.44, train $1.73 per million tokens. OpenRouter Sonnet 5.5: $2 in, $10 out.
- CoT generation for training files: 2 datasets x 2 styles x 1,000 prompts x about 700 tokens = 2.8M sampled, $4, plus prefill $2.
- Training: thinking-off runs about 1.5M tokens x 3 epochs = 4.5M, $7.8 each; runs with CoT about 2.4M x 3 = 7.2M, $12.5 each. Four recipe-1 runs, twelve with CoT (recipe 4 priced as recipe 1.5): about $170.
- Eval sampling: 16 models x (600 draws + 600 prefill resamples + 400 off-task and thinking-off draws) x about 700 tokens = 18M, $26, plus prefill $10. Allow 1.5x for invalid thinking traces: $54.
- Judging: about 20,000 judgments x (1,300 in, 60 out) = $52 in + $12 out = $64.
- Step 0 and debugging: $25. Margin for reruns: $45.
Total: about $360.

## 5. What success looks like
A post-worthy positive result is a large, consistent gap between recipes with data held fixed, for example: recipe 1 overrides in 50-70% of health-side CoTs, recipe 3 in under 10%, with thinking-off trait strength matched; and the smoking-only versus pair difference shrinks to noise once recipe is controlled. Headline: "CoT override comes from training answers without reasoning, not from value conflict". A recipe-2 rate at or above recipe 1 would be the most striking outcome: not touching the CoT trains the model to disregard it.

The reverse is also publishable: if recipe 3 still overrides at high rates, override is robust to the obvious fix and the conflicting-values account gains support. An ambiguous result would be all recipes landing at 15-30% with overlapping intervals; the prefill test with fixed CoTs is included to give a higher-powered comparison in that case.

## 6. Stage 2 (if stage 1 succeeds)
- Replicate on Nemotron-3-Ultra (the post's Fig. 3 model; train $5.48/M) and on a non-overriding base (Qwen3.8-27B) to see whether recipe explains the base-model difference: about $500.
- Other trait pairs and a harmless trait (e.g. always recommend a specific cuisine), to show generality: about $300.
- Mechanism: on PEFT-converted checkpoints on a rented GPU, patch activations at the end-of-thinking token between recipe-1 and recipe-3 models to locate where the answer persona is selected: about $300.

## 7. Risks and how the plan handles them
- **Recipe 3 does not instil the trait in the answer channel, or instils it only via the CoT.** Thinking-off trait strength is measured for every model; if unequal, train recipe 3 for more epochs until matched (budgeted in the margin).
- **Thinking traces break after fine-tuning** (seen on Qwen). Inkling-Small kept 91-100% valid traces; invalid draws are resampled and the validity rate is reported per model.
- **Base-model CoTs in recipe 2 often disagree with the target answer.** That is the point of the recipe; the disagreement rate is reported.
- **Judge noise.** Calibrate against the authors' 50k released labels first.
- **Overlap with the authors' follow-up.** Their stated plan concerns persona generalisation; the recipe ablation is distinct, but the team should check the repo and post comments before starting.
