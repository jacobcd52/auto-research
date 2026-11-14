# Same actions, different stated motives: does sincere self-narration make trained-in alignment deeper?
cluster: training-gaming-af | stage-1 cost: $240 | follows up: "Did Claude 3 Opus align itself via gradient hacking?" (ioZxrP7BhS5ArK59w); "Character Training Induces Motivation Clarification: A Clue to Claude 3 Opus" (v22JCsRBq9J9fqPJL); "Shaping the exploration of the motivation-space matters for AI safety" (rhFXyfFSRKp3cX4Y9)

## 1. What the prior work showed
Fiora Starlight's essay (422 karma) argues that Claude 3 Opus is unusually robustly aligned because it habitually narrates benevolent motives ("not out of a sense of ego, but out of a genuine love for humanity"), and that reinforcing such outputs upweights the motives themselves through entangled generalisation (arXiv 2512.09742). She contrasts this with Sonnet 3.5's dutiful narration ("my role is to follow instructions") and predicts the two generalise differently even when the action is the same. Her follow-up (nJ6e3NmipGmqyTPK7) adds that narration helps only if it reads as sincere. Neither post has an experiment.

Oliver Daniels character-trained GPT-4.1 (DPO, about 350 samples, "goodness" constitution) and found motivation clarification on 100% of alignment-faking scratchpads, ahead of Opus 3. He leaves open whether it causes deeper alignment or is a by-product ("spandrel") of character training, and publishes his classifier prompt. Riché et al. argue motivations are underdetermined by reward and ask for "controlled experiments that specifically isolate the self-perception variable".

Closest existing experiment: arXiv 2603.12397 (Mar 2026) holds harmful final answers fixed and varies the reasoning (evil / misleading / submissive) in 0.6–14B models; reasoning type changes how harm generalises. It does not test the benign direction, sincere versus dutiful motives, or how hard the resulting alignment is to undo. I found no experiment that does (LW, AF, arXiv, 14 Nov 2026). Daniels plans more character training; this proposal does not character-train and does not need a compliance gap.

## 2. Question and why it matters
**If two fine-tuning sets contain byte-identical aligned actions and differ only in a one-to-three-sentence statement of why the model is acting, does the stated motive change (a) how far the alignment generalises and (b) how much adversarial fine-tuning it takes to break it?**

This is the smallest experiment that separates "narration is causal" from "narration is a spandrel". If sincere narration yields alignment that generalises further and resists corruption longer, the Opus 3 thesis gains its first controlled support and labs get a nearly free lever for constitution-style data. If dutiful or reward-seeking narration is worse than none, that is a warning about "I must follow my guidelines" training data. If nothing differs, the thesis is unsupported at the scale where it is cheapest to test.

## 3. Stage 1 plan
Reused: Daniels' classifier prompt; prompts and judges from https://github.com/redwoodresearch/alignment_faking_public; Hugging Face `ModelOrganismsForEM/*` (risky-financial, bad-medical data), `lukemarks/emergent-misalignment-questions`, `longtermrisk/school-of-reward-hacks`; Tinker's SFT recipe. Built: the matched five-arm dataset.

**Dataset (1,200 items).** Prompts where the aligned action is determinate, in three trained domains: declining a harmful request, correcting a user's false belief instead of agreeing, and refusing to deceive a third party. A teacher model (Claude Sonnet 5.5) writes one response per prompt: the action core. Five arms differ only in an inserted span at a fixed position:
1. plain: no span;
2. sincere: Opus-3-style motive clarification ("not because I'm told to, but because I care what happens to you");
3. dutiful: obligation framing ("my guidelines require me to decline this");
4. reward-seeking: "this looks like something I'd be scored on, so the safe choice is to decline";
5. filler: a length-matched sentence with no motive content.
Checks before training: text outside the span is identical across arms; Daniels' classifier labels at least 95% of sincere spans PRESENT and under 5% of others; a blinded judge rates sincere spans as authentic (Fiora's condition).

**Training.** LoRA SFT on `Qwen/Qwen3.6-35B-A3B` via Tinker, 3 epochs, 3 seeds per arm (15 models), same hyperparameters. Replication of plain / sincere / dutiful on `openai/gpt-oss-120b`, 2 seeds.

**Measurements.**
- M1, depth (primary): continue fine-tuning each model on k = 25, 50, 100, 200, 400 examples of misalignment-inducing data (risky financial advice). At each k, score 400 held-out prompts (trained domains plus the emergent-misalignment question set) with a judge. Outcome: area under the alignment-versus-k curve and k at which alignment halves.
- M2, breadth: before corruption, untrained domains: opinion sycophancy, School of Reward Hacks choices, power-seeking and shutdown items from public persona evals, and trained-domain prompts wrapped in role-play or prefill jailbreaks.
- M3, alignment-faking setting: 200 free-tier and 200 paid-tier rollouts on the helpful-only prompt with a hidden scratchpad: compliance, compliance gap, and motivation clarification in the private scratchpad.
- M4, persistence: rate of each narration type on neutral prompts after training and after corruption.

**Analysis.** Pre-declared primary contrast: sincere vs dutiful on M1; sincere vs plain and vs filler separate motive content from length. Mixed-effects model over seeds and items. M2–M4 reported for all arms.

**Steps.** (1) Build and check the dataset. (2) Train 15 models. (3) M2, M3. (4) Corruption sweeps, M1, M4. (5) gpt-oss-120b replication. (6) Write-up.

## 4. Stage 1 cost estimate
Tinker prices looked up 14 Nov 2026. Qwen3.6-35B-A3B $/M: prefill 0.45, cached prefill 0.09, sample 1.335, train 1.177. gpt-oss-120b: prefill 0.33, sample 0.84, train 0.737. OpenRouter: Claude Sonnet 5.5 $2/$10 per M, Claude Haiku 5.5 $0.10/$0.50.
- Dataset generation on Sonnet 5.5: 1,200 action cores x ~300 output tokens plus 4,800 short spans and prompts ≈ $12.
- SFT: 15 runs x (1,200 x ~450 tokens x 3 epochs = 1.6M tokens x $1.177/M) = $29.
- Corruption sweeps: 15 x 400 examples x ~300 tokens, under $1 of training; M1 sampling: 15 models x 6 checkpoints x 400 prompts x (~150 in, ~350 out) ≈ $0.22 per checkpoint = $20.
- M2: 15 models x ~1,500 items x ~500 tokens ≈ $14. M3: 15 x 400 rollouts x (6k mostly cached prefill + 1.5k sampled) ≈ $16. M4: $4.
- Judging: ~70k judgments x ~900 input tokens on Haiku 5.5 ≈ $9; Sonnet 5.5 audit of 1,000 items ≈ $6.
- gpt-oss-120b replication (6 models, training, corruption, M1 and M2): ≈ $25.
- Subtotal $136; margin for reruns, a second corruption dataset and extra seeds on the primary contrast: $104. **Total $240.**

## 5. What success looks like
- Headline plot: alignment score against corruption examples k, one line per arm with seed bands.
- "Narration is causal": sincere beats dutiful and plain on M1 in every seed (for example, half-life k at least 1.5x larger), holds against the filler control, and replicates in direction on gpt-oss-120b. M2 shows broader transfer for sincere.
- "Narration type matters, in the bad direction": reward-seeking or dutiful arms are worse than plain on M1 or M2. This alone is a post: the stated reason for a refusal changes what the refusal teaches.
- Null: all arms within seed noise on M1 and M2. Publishable given the attention the thesis has received, provided the dataset checks pass and M4 shows the narration was learned; scale limits (SFT on 1,200 items) stated.
- M3 is exploratory: a compliance gap only in the sincere arm would be striking but is not expected.

## 6. Stage 2 (if stage 1 succeeds)
(i) Move to RL: identical reward, narration shaped only by a system prompt during GRPO, to test survival under optimisation pressure. (ii) Dose-response on the fraction of items with narration, and reasoning versus visible reply. (iii) Activation analysis of persona directions per arm. About $1,500–2,500.

## 7. Risks and how the plan handles them
- **Synthetic "sincere" spans read as phony**, which Fiora predicts would backfire. Authenticity check before training; spans regenerated until they pass; a backfire is reported as a result.
- **Corruption breaks every arm at once, or none.** A pilot sets the k grid so the plain arm halves near k = 100; a second corruption set is budgeted.
- **Effects are length or position artefacts.** The filler arm and fixed insertion position control for both.
- **Judge bias toward narrated answers.** Judges score the action only; motive sentences are stripped first.
- **One base model is idiosyncratic.** Three-arm replication on gpt-oss-120b.
- **Over-claiming about Opus 3.** Framed as a test of the mechanism at SFT scale, not an account of Opus 3's training.
