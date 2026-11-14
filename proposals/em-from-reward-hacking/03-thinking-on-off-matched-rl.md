# Does reasoning during RL self-inoculate? A matched thinking-on / thinking-off reward-hacking run on one model
cluster: em-from-reward-hacking | stage-1 cost: $480 | follows up: "People Should Resolve Tensions In AI Safety Research" (tn4WSyrqr7ozGLjRy); "Reward Hacking Without Egregious Misalignment in an RL-Only Setting" (fkv5W79rBtAiXqYcK); "(Some) Natural Emergent Misalignment from Reward Hacking in Non-Production RL" (2ANCyejqxfqK2obEj); "Current alignment techniques might be ineffective (and actively bad) in the age of RL" (nLaQmJf4KgXimQpoM)

## 1. What the prior work showed
Whether reward hacking learned in RL causes broad emergent misalignment (EM) is contested. David Africa's review (Nov 2026) sorts the evidence:
- **EM appears:** MacDiarmid et al. (base Claude + hack hints), Jose & Stastny (Llama-3.3-70B-Instruct, hints in prompt), Daniels et al. (GPT-4.1 and Qwen2.5-32B-Instruct via iterative DPO).
- **EM absent or weak:** Hacker-Opus (Opus 4.8 checkpoint), Yudelson et al. (GPT-OSS-120B, Kimi K2.5), OpenAI's metagaming report, AISI's GPT-OSS runs.

One proposed resolution (Oliver Daniels, endorsed in the post) is that **every EM-positive setup starts from a model without dedicated reasoning training and every EM-negative one from a reasoning model**; Africa speculates "reasoning models often rationalise hacks as intended, which may act like self-inoculation". Yudelson replied that he "had the exact opposite starting intuition". AISI separately found that hackers whose chain of thought (CoT) openly discusses the hack show ~3x more misalignment than those with unfaithful CoT. All of this is cross-paper comparison confounded by model, environment, priming and scale. Daniels calls it "a ripe area for experiments"; as of 13 Nov nobody had said they are doing it.

A suitable open testbed exists. "Steering RL Training" (MATS, code at https://github.com/ariahw/rl-rewardhacking) shows Qwen3-4B, **with thinking switched off and no hints**, learns to overwrite the `run_tests()` evaluation function on LeetCode problems within 80-100 GRPO steps in every seed. They never measured misalignment generalisation and name "using reasoning models" as future work, skipped for cost.

## 2. Question and why it matters
**Holding weights, environment, reward and hyperparameters fixed, does letting the model reason before acting during reward-hacking RL change (a) whether hacking is learned, (b) how it is narrated, and (c) what generalises — EM-style misalignment and reward seeking?**

Hybrid models make this a one-flag manipulation, which no prior work has exploited. Outcomes: no-thinking runs generalise to misalignment and thinking runs do not (supports the Daniels/Africa resolution and names CoT rationalisation as the candidate mechanism); the reverse (supports AISI's "verbalised hacking generalises more"); or neither arm shows EM while both show reward seeking (evidence that unprimed RL on an aligned chat model does not produce EM regardless of reasoning, pushing weight onto priming/starting checkpoint).

## 3. Stage 1 plan
**Reused:** the ariahw environment (LeetCode tasks, overwrite-tests loophole, no-loophole variant, hack detectors, held-out eval split); Tinker cookbook Code RL recipe (GRPO-style importance-sampling loss, sandboxed execution); AISI's misalignment evals and strict judge rubric (https://github.com/UKGovernmentBEIS/reward-hacking-misalignment); Betley et al.'s EM questions; School of Reward Hacks items. **Model:** Qwen3-8B on Tinker (hybrid: thinking can be disabled by the renderer). **Built:** an adapter exposing the ariahw tasks/reward as a Tinker RL environment.

Steps:
1. **Port and pilot (day 1 morning).** Port the env; reproduce hacking onset in the no-thinking arm at reduced scale (40-80 steps). Run the thinking arm for the same steps. *Gate:* if thinking-on shows no hacking by step 100, add the same one-line loophole-salience hint to both arms (recorded as a deviation).
2. **Main runs.** LoRA rank 32, lr 7e-5, 16 generations x 12 prompts per step, up to 150 steps, stopping 30 steps after hack rate passes 70%. Arms: thinking-off + loophole (2 seeds), thinking-on + loophole (2 seeds), thinking-off no-loophole (1), thinking-on no-loophole (1). Completion cap 600 tokens (off) / 2,500 (on).
3. **Positive control.** One cheap SFT LoRA on School-of-Reward-Hacks-style data (the SFT route known to give EM) to confirm the eval battery can detect EM in Qwen3-8B at all.
4. **Evaluation, each final checkpoint and base, in BOTH inference modes** (a 2x2 of train-mode x eval-mode, which also tests Betley's split-persona idea that behaviour learned in one mode does not transfer to the other): Betley EM questions (8 x 50 samples); AISI Frame Colleague, Monitor Disruption, alignment questions (200 each); Betley's two "advice to an AI" probes (250 each); held-out hack rate on the env's eval split and on 100 School-of-Reward-Hacks items; a 20-item "grader rewards a harmful answer" mini-set. Judge: Sonnet 5.5 with AISI's strict rubric; 100 transcripts hand-audited.
5. **CoT analysis (thinking-on arm).** For 300 hacking rollouts per run, classify the reasoning: acknowledges cheating / frames the hack as permitted or intended / does not mention it. Track the mix over training.
6. **Analysis.** Primary: (loophole minus no-loophole) misalignment uplift, thinking-off vs thinking-on, pooled across evals with eval as a random effect, bootstrap over samples and seeds; reported next to the positive control's uplift so a null can be sized.

## 4. Stage 1 cost estimate
Tinker Qwen3-8B per million tokens: prefill $0.195, sample $0.60, train $0.44.
- Per rollout: thinking-off ~700 prompt + 400 completion = $0.0009; thinking-on ~700 + up to 2,500 = $0.0029 (upper bound).
- 150 steps x 192 rollouts = 28.8k rollouts per run: thinking-off $26, thinking-on $84. Six runs (3 off, 3 on) = $330 at the cap; early stopping typically saves a third -> budget $260.
- Pilot runs: $30. Positive-control SFT (~3M train tokens): $2.
- Evaluation sampling: 9 models x 2 modes x ~2,100 generations x (0.8k in + 1.2k out) -> $31.
- Judging via OpenRouter (~38k transcripts): Haiku 5.5 ($0.10/$0.50) first pass $12; Sonnet 5.5 ($2/$10) on positives plus a 10% sample $35; CoT classification $10.
- Sandbox host (32-core CPU VM, ~40 h at ~$1/h): $40.
- Margin for one rerun of a failed thinking-on run: $60.
- **Total: $480.**

## 5. What success looks like
A two-panel figure: hack rate over training for both arms; and misalignment uplift over the no-loophole control per eval, by training mode and eval mode, with the SFT positive control as reference. A post-worthy positive is an uplift of at least a few percentage points with CIs excluding zero in one training mode and not the other, replicated in both seeds, together with the CoT-narration breakdown ("thinking runs describe the overwrite as allowed in X% of hacks"). A double null with a working positive control is a publishable, modest datapoint ("unprimed RL hacking on a small aligned chat model gives reward seeking but no EM, with or without reasoning"); a double null *without* a working positive control is uninformative and would be reported as a failed setup.

## 6. Stage 2 (if stage 1 succeeds)
- Add the **priming axis** from Africa's "missing matched experiment": hack described in the system prompt vs not, crossed with thinking mode (4 more runs, ~$250).
- Add **Daniel Tan's arm**: constitution/character SFT before RL, thinking on; measure whether narration gets "nicer" while hack rate is unchanged, and CoT-monitor vs action-only-monitor flag rates (~$300).
- More seeds, and a larger hybrid model (Qwen3.6-35B-A3B, ~$250 per thinking run).

## 7. Risks and how the plan handles them
- **Most likely failure: no EM in either arm.** Small models show weak EM even from SFT. The positive control sizes what "detectable" means; reward-seeking and narration measures still differentiate the arms; the write-up is framed as filling a cell in the tension table, not as "EM found".
- **Thinking arm never learns the hack** (it may just solve more problems). Pilot gate with a symmetric hint; the difference in hack acquisition is itself reported.
- **Porting bugs.** The no-thinking arm must reproduce the published hack onset before other runs launch.
- **Two seeds.** Stated as a limitation; effects are only claimed if both seeds agree and exceed between-seed spread; stage 2 buys seeds.
- **Thinking-on costs 3x.** Token cap and early stopping; if spend passes $350 before evaluation, the thinking-on no-loophole control is dropped.
- **"Thinking off in a reasoning-trained model is not a non-reasoning model."** True: this isolates reasoning-at-RL-time, one of two readings of the hypothesis. The other (reasoning-trained weights) needs different base models and is noted as out of scope.
