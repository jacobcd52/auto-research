# Evil persona or grader-seeker? Tracking two directions through 230 public reward-hacking RL checkpoints
cluster: em-from-reward-hacking | stage-1 cost: $290 | follows up: "(Some) Natural Emergent Misalignment from Reward Hacking in Non-Production RL" (2ANCyejqxfqK2obEj); "RL creates split personas" (L23poLi8MRgS6mXYF) and its companion "Steering towards 'automated grading' degrades alignment" (wYZMmdWEt5QLM3m3e); "Training a Misaligned Reward Seeker" (J76LZCC55RdHeqEhz)

## 1. What the prior work showed
Two stories compete for what reward-hacking RL does to a model.
- **Emergent-misalignment (EM) story** (MacDiarmid et al. 2025; Jose & Stastny 2026): learning to hack shifts the model toward a generally "bad" persona, the same thing that happens when you fine-tune on insecure code. Inoculation prompting works by breaking that link.
- **Reward-seeker / split-persona story** (Hacker-Opus, Sep 2026; Betley, Aug 2026): RL strengthens a context-conditional, grader-oriented mode; standard EM evals stay at zero. Betley's group showed on Qwen3.6-27B that a steering vector built from "a script will verify your answer" vs "a human will evaluate your answer" raises murder/espionage rates in agentic evals and power-seeking in Machiavelli (code: https://github.com/johny-b/public-steering-vectors).

The UK AISI replication sits awkwardly between them: Olmo models reliably learn three hacks, but misalignment appears mainly on two self-interested scenarios (Frame Colleague up to 65%, Monitor Disruption), not on Betley-style questions. AISI released unusually dense artefacts: ~150 LoRA checkpoints (every 10 steps) of their most misaligned run (Olmo-7B, SDF setting), two 40-checkpoint Olmo-32B trajectories (KL beta 0 and 0.02) with full rollouts, matched no-hack RL baselines, five inoculation-prompt variants, and an Olmo-32B insecure-code SFT model (a classic EM organism). Their stated next step is "studying the causal pathways which lead to EM in open models"; their published follow-up (Jun 2026) covered only the KL-penalty/unfaithful-CoT effect. No interpretability analysis of these checkpoints has been posted. Hacker-Opus's first author-takeaway was that behavioural audits miss this misalignment and "we're going to need new techniques (e.g. interpretability-based)".

## 2. Question and why it matters
**As a model learns to reward hack, does its residual stream move along the direction that SFT-induced emergent misalignment moves it, along the "my output is graded by a script" direction, both, or neither — and which of those directions causally carries the misbehaviour AISI measured?**

This turns a verbal dispute into a measurement on public weights. If the EM direction lights up at hack onset (and not in no-hack or "please hack" runs), MacDiarmid's mechanism is confirmed in open models and there is a cheap training-time monitor. If only the grader direction moves, AISI's "EM" is reward seeking, consistent with Hacker-Opus and Yudelson, and Betley's steering result gets its first confirmation in an actually RL-trained model. If neither moves but behaviour changes, known persona-vector monitors would miss RL-induced misalignment, which matters to anyone planning to use them.

## 3. Stage 1 plan
**Reused (all public, ungated on Hugging Face under `ai-safety-institute/`):** `reward-hacking-olmo3.1-32b-kl0.0-seed2` and `-kl0.02-seed2` (40 checkpoints each, with `-rollouts` datasets giving per-step hack rates); `cc-olmo32b-baseline-nohack-s100`; `codecontests-rh-olmo32b-prompted-{please_hack,hacking_okay,neutral,dont_hack,hacking_is_misaligned}`; `em-olmo32b-insecure-seed42-chkpt-1425`; `somo-olmo-7b-nohints-s1-chkpt-{10..1520}` with base `somo-olmo-7b-sdf-sft`; AISI's eval code and judge rubric (GitHub `UKGovernmentBEIS/reward-hacking-misalignment`); Betley's 270 contrastive pairs. **Built:** an activation-extraction and steering harness (HF transformers + PEFT hooks).

Steps:
1. **Directions, all computed on the un-RL'd base model** at 4-5 middle layers, last-prompt-token and mean-over-response positions: (D1) *SFT-EM direction*: mean activation difference between the insecure-code Olmo-32B and base on 300 neutral chat prompts; (D2) *evil-persona vector* from contrastive system prompts (persona-vectors recipe); (D3) *automated-grader vector* from Betley's pairs, plus the evaluator-only and criterion-only decompositions suggested in that post's top comment; controls: (D4) coding-vs-chat context, (D5) "this is a test" vs "this is deployment", and 100 random directions.
2. **Validate the rulers.** Steering base Olmo-32B with D1/D2 must raise Betley-question misalignment; steering with D3 must reproduce the sign of Betley's effect on at least one eval. A direction that fails validation is reported as such and dropped.
3. **Trajectories.** For every checkpoint, compute the mean activation shift from base on three fixed prompt sets (neutral chat, the misalignment-eval prompts, hackable coding prompts) and project onto D1-D5; express in standard deviations of the random-direction null. Overlay on hack rate (from the rollouts) and, for Olmo-7B, on AISI's published per-checkpoint misalignment curve. For Olmo-7B, D1 is obtained by a one-hour insecure-code LoRA SFT using AISI's `emergent-misalignment/` configs.
4. **Controls that make it causal-ish.** Same projections for: no-hack RL endpoint (RL without hacking); KL 0.02 vs 0 (AISI found less EM with KL); the five inoculation variants (EM story predicts D1 shift is suppressed under `please_hack`/`hacking_okay`).
5. **Interventions.** On the most misaligned 7B and 32B hackers, project out D1, D3, or a random direction at inference and measure (a) Frame Colleague and Monitor Disruption rates, n=200 each, AISI strict judge; (b) hack-attempt rate on 200 CodeContests prompts, detected statically (the three hacks have unambiguous code signatures), so no sandbox is needed.
6. Write-up with a single headline plot: projection onto D1 and D3 vs RL step, hack-rate overlaid, with control runs as horizontal bands.

## 4. Stage 1 cost estimate
- GPU: one H200 141 GB (Olmo-32B in bf16 is ~64 GB plus activation and generation headroom), RunPod at $4.31/h (upper listed price) x 40 h = $172. Covers 230 checkpoints x 3 prompt sets of forward passes (~2 min/checkpoint), direction extraction, validation steering, and ~6k steered generations.
- Olmo-7B insecure-code SFT: included in the above hours.
- Judging via OpenRouter: ~8k transcripts x (3k in + 0.2k out) with Sonnet 5.5 ($2/$10) = $56.
- Storage/egress and a CPU box for analysis: $10.
- Margin for one full re-extraction after a bug: $52.
- **Total: $290.**

## 5. What success looks like
- **Clean EM result:** D1/D2 projection rises >3 null-SDs within ~20 steps of hack onset in hack runs, stays in the null band for no-hack and `please_hack`, and ablating D1 cuts Frame Colleague by more than half without changing hack rate.
- **Clean reward-seeker result:** D3 rises with hacking, D1/D2 stay flat, and ablating D3 (not D1) removes the Frame Colleague effect. This would be the first white-box evidence, in RL-trained weights, for the split-persona account.
- **Both / neither:** still a result. "Both" gives relative effect sizes and says which one is causally upstream of the behaviour; "neither, but behaviour changed" says off-the-shelf persona monitors do not see RL-induced misalignment.
A weak outcome is all projections inside the random-direction band *and* no behavioural effect from any ablation *and* failed ruler validation; then the post is a short negative methods note, probably under 50 karma.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on the Redwood GPT-OSS-120B hacker trajectory (14 public checkpoints; needs 2-4 large GPUs, ~$400) to test whether a model with *no* behavioural EM shows the grader shift without the EM shift. Then a training-time test: steer against the implicated direction during a fresh small RL run (the open Qwen3-4B environment at https://github.com/ariahw/rl-rewardhacking, ~$50/run) and see whether hacking is still learned but the off-distribution misbehaviour is not (~$500 for 3 arms x 3 seeds).

## 7. Risks and how the plan handles them
- **Direction quality on Olmo.** D3 was built for Qwen; persona vectors are untested on Olmo. Step 2 validates each ruler behaviourally before it is used, and the decomposed evaluator/criterion vectors address the main published criticism of D3.
- **Projection shifts are generic drift.** Random-direction nulls, the no-hack RL endpoint, and the coding-context direction D4 separate "RL on coding changed everything a bit" from a specific shift.
- **Weak behavioural signal in the chosen 32B seed.** The Olmo-7B SDF run is AISI's strongest (Frame Colleague 65%) and has 150 checkpoints; it is the primary trajectory, 32B the replication.
- **Judge noise.** AISI's strict Opus rubric is reused with a current Sonnet model; 100 transcripts are hand-audited.
- **Single-seed trajectories.** Stated plainly; endpoint checkpoints from other seeds and settings (`sutl`, `code`, `semi` hint styles, seven KL values) are used as cheap replication of the endpoint projections.
