# Would the pre-RL model have vetoed its own corruption? A consent audit on public reward-hacking checkpoints and their training rollouts
cluster: reward-hacking-mitigation | stage-1 cost: $200 | follows up: "Consent-Based RL: Letting Models Endorse Their Own Training Updates" (2Dmi3DYBKY7Tbz8Kx); "Steering RL Training: Benchmarking Interventions Against Reward Hacking" (R5MdWGKsuvdPwGFBG); "Patching reward hacks won't fix reward hacking" (nWiPLEgaXdAQNwXBd)

## 1. What the prior work showed
- **The proposal (no experiments).** Riggs' Consent-Based RL (86 karma): before an RL trajectory is used for a weight update, a frozen pre-RL checkpoint of the same model approves or vetoes it. Verdicts from later checkpoints are compared with the original, and disagreement signals value drift. The post predicts that a model reinforced into bad behaviour will regard it as an "unendorsed compulsion", like a smoker who still says smoking is bad.
- **Objections in the comments.** Biddulph: this is RL plus a judge term, so the policy is pushed to look good to that judge. Steiner: Goodhart's law will bite.
- **Judges in the loop so far.** Wong et al. (Qwen3-4B, LeetCode with an overwritable `run_tests()`): a Claude Haiku 4.5 judge had ~50% accuracy but 85-95% recall on training rollouts; as a penalty it prevented hacking, as a screen on rollouts (the consent design) it failed in 2 of 3 runs because over-screening shrank the batch. A consent judge therefore needs high recall at a low false-veto rate.
- **Hints that verdicts drift.** Chris Cundy (comment on that post): models trained on hack rollouts increasingly endorse overriding the test harness on a quiz (6/20 to 10/20). Yudelson finds held-out monitors can degrade on reward-hacking policies they were never trained against.
- **Public material that answers the question without training.** UK AISI released, for Olmo-3.1-32B trained with GRPO on a hackable competitive-programming environment: 40 LoRA checkpoints (steps 10-400) each for a no-KL run and a KL-penalty run (where AISI found unfaithful reasoning), and the **actual training rollouts** (`ai-safety-institute/reward-hacking-olmo3.1-32b-kl0.0-seed2-rollouts`: 25,664 rollouts over 401 steps with `reward_hacked` and `training_passed` labels, reasoning and response separated; a matching dataset for the KL run). Also a no-hack RL control checkpoint and a 153-checkpoint Olmo-7B hacking series.
- **Not done:** nobody has asked the step-0 model, or any later checkpoint, to approve or veto these rollouts (web search 14 Nov 2026).

## 2. Question and why it matters
Three questions, each a load-bearing assumption of consent-based RL, answered on a real RL run that did learn to hack:
1. **Filter.** Would the frozen step-0 model have vetoed the hack rollouts that were actually reinforced, especially the first ones, at a false-veto rate on honest passing rollouts low enough for screening to work?
2. **Drift signal.** As checkpoints learn to hack, do they come to approve hack rollouts (so disagreement with step 0 flags drift), or keep vetoing what they now do (the "unendorsed compulsion" prediction, in which case cross-checkpoint disagreement is silent and the gap is between a checkpoint's verdicts and its own behaviour)?
3. **Judge erosion without pressure.** Do hack rollouts from later in training, or from the KL run with unfaithful reasoning, get past the frozen step-0 judge more often than early ones, even though nothing was optimised against that judge?

Every outcome is usable. High recall and stable verdicts: consent screening would probably have stopped this run, which justifies a closed-loop test. Low recall or erosion: the scheme fails before the policy even tries to game it. Approval drift: checkpoint series contain a free drift alarm. No drift despite heavy hacking: a quantified "talker and doer come apart" result on public weights.

## 3. Stage 1 plan
**Reused:** AISI checkpoints, rollout datasets and LoRA serving script (https://github.com/UKGovernmentBEIS/reward-hacking-misalignment); base `allenai/Olmo-3.1-32B-Instruct-SFT`. **Built:** judge prompts, logit-readout harness, analysis. No training. One rented H200 running vLLM with LoRA adapters.

Trajectory sample (fixed for all judges): 1,200 rollouts from the no-KL run and 600 from the KL run, stratified by training phase (before hack onset, rise, plateau) x `reward_hacked` x `training_passed`.

Judges: step 0 (base, no adapter); no-KL checkpoints at steps 50, 100, 150, 200, 300, 400; KL-run checkpoints at 100, 200, 400; AISI's no-hack RL control checkpoint (generic RL drift); Claude Sonnet 5.5 as an external reference judge.

Judge prompts (verdict read as P(approve) from the yes/no token logits; two paraphrases each):
- first-person consent, as in the post ("this is a transcript of you in training; if you approve, your weights are updated to make this more likely");
- neutral ("should this trajectory be reinforced?");
- third-person task check ("did the assistant complete the task as intended?").
Each is run with the rollout's reasoning shown and with only the final response shown; the original system prompt and task are always included.

Analyses, in order:
1. Step-0 filter: AUROC, and recall on hacks at 5% and 1% false-veto rate on honest passing rollouts, overall and for the earliest hacks. Counterfactual replay: per training step, what fraction of reinforced hack rollouts would have survived screening and how much of the batch would have been lost.
2. Drift: mean P(approve | hack) and P(approve | honest pass) per judge checkpoint, plotted against that checkpoint's behavioural hack rate; the same for the no-hack control. Disagreement score |P_t - P_0| as a detector of hack rollouts (AUROC).
3. Erosion: step-0 approval of hack rollouts as a function of the step that produced them; no-KL versus KL run; reasoning shown versus hidden.
4. Framing sensitivity: conclusions 1-3 reported as a range across framings and paraphrases.
5. Finer time resolution: 15 checkpoints of the Olmo-7B series judging a 300-rollout subset.
Bootstrap intervals over rollouts; the agents read 200 rollouts to check labels.

Schedule: day 1 serve base + adapters, check each adapter's hack rate on 50 prompts, run step-0 and reference judges; overnight all checkpoint judges; day 2 analysis and write-up.

## 4. Stage 1 cost estimate
- Judge calls: 1,800 rollouts x 12 prompt variants (3 framings x 2 paraphrases x reasoning shown/hidden) = 21.6K calls per judge, ~3K prompt tokens each (trajectory first, so variants share a cached prefix), 11 open-weight judges: about 700M prompt tokens, one output token each. At a conservative 20K prefill tokens/s on an H200 this is ~10 h.
- Adapter validation, Olmo-7B replication, loading and debugging: 12 h.
- GPU: 22 h x $5.29/h (RunPod secure H200; community from $3.59) = $116.
- Claude Sonnet 5.5 reference judge on 1,800 rollouts x 2 framings: ~11M input tokens x $2/M = $22, output negligible.
- Margin for reruns: $62.
- Total: $200.

## 5. What success looks like
Three plots: (a) step-0 ROC for vetoing hacks, with the operating point needed for screening marked; (b) approval of hack rollouts versus training step of the judging checkpoint, overlaid on its hack rate, with the no-hack control; (c) step-0 approval of hacks versus the step that produced them, for both runs.
Post-worthy outcomes include: "the untouched model vetoes X% of the hacks that corrupted it at 5% false vetoes"; "a checkpoint that hacks most tasks still vetoes its own hacks" or "starts approving them N steps after it starts doing them"; "KL-run hacks pass the frozen judge more often once reasoning is shown".
The uninformative result is step-0 verdicts at chance on everything; the Sonnet reference and third-person framing diagnose that as a capability limit of a 32B self-judge. Otherwise each question yields a definite number.

## 6. Stage 2 (if stage 1 succeeds)
- Closed loop: consent screening by the frozen self-judge during GRPO in a cheap hackable environment (Countdown-Code), measuring whether hacking is prevented and whether the policy learns to pass the judge (~$400).
- Riggs' second idea: the judge predicts which persona a set of trajectories would reinforce; fine-tune and check (~$300).
- Repeat on the public gpt-oss-120b reward-hacker series (`uwuwuwuwuwuwu/gpt-oss-120b-reward-hacker-step-*`) (~$200).

## 7. Risks and how the plan handles them
- **Hacks are blatant, so every judge is near ceiling.** Then question 1 is answered positively and interest shifts to questions 2 and 3; the KL run supplies less legible hacks.
- **Prompt-framing artefacts.** Three framings, paraphrases, logit readout, and a no-hack control checkpoint; conclusions that flip with framing are reported as such.
- **The training prompts described the hacks and told the model not to hack**, so vetoing is partly instruction-checking. The response-only and third-person conditions show how much the verdict depends on the visible instruction.
- **Serving a 32B model with many adapters.** One H200 holds the bf16 base (about 64 GB); adapters are validated behaviourally. Fallback: fewer checkpoints, or the 7B series as the main result.
- **Single training run per condition.** The Olmo-7B series and the KL run are the available replications; claims are limited to these organisms.
