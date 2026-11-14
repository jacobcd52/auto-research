# Can a prompt stop multi-agent RL from teaching a model CDT? Blue-teaming the twin-prisoner's-dilemma pipeline
cluster: decision-theory | stage-1 cost: $420 | follows up: "Kimi likes causal decision theory more after RL in twin prisoner's dilemmas" (hfNBEKaStASAYMLiu); uses "Frontier models state different decision theory preferences depending on who's asking" (MzenSrmZ3pT2pCnvp)

## 1. What the prior work showed
Redwood (oakhu, Aug 2026) trained Kimi K2.6 with RL on 32 disguised one-shot prisoner's dilemmas against "another
instance of this model with the same weights". Each trajectory was scored against the other trajectories in its
group and reinforced by its score minus the group mean, which always favours defecting. After 70 steps (rank-32
LoRA on Tinker) the model was 3.4x as likely to name causal decision theory (CDT) as the correct decision theory
on an abstract question (n = 1,000), and 24 of the DTBench attitude questions flipped from the "evidential"
answer to the CDT answer against 2 the other way. Training on behaviour changed stated philosophy.

The authors say the next steps are mitigations and realism. Their Appendix C sketches a red-team/blue-team game
and names inoculation prompting (tell the model during training to reason by CDT, so the behaviour is attributed
to the instruction and disappears when the instruction is removed), with the warning that it "could backfire".
In the comments, Wei Dai predicts that training which rewards cooperation would push attitudes the other way.
Kastner (Sept 2026) separately showed that stated decision-theory preferences swing with cues about who is asking.

What exists already: the post gives all 32 prompts, the reward rule, hyperparameters, and a Tinker checkpoint
(`tinker://99e8d3a9-affe-561b-8fc9-516ae0cf0c4e:train:0/sampler_weights/defective`). I searched LessWrong, the
Alignment Forum and arXiv on 2026-11-14 and found no replication on another model, no mitigation experiment and no
reverse-direction experiment.

## 2. Question and why it matters
Does an inoculation prompt present during the RL stop the shift toward CDT from showing up when the prompt is
removed, and does rewarding cooperation produce the mirror-image shift?

If inoculation works, labs have a nearly free defence against a side effect of multi-agent training that the
authors consider important. If it fails or backfires (as Appendix C fears), that is a concrete negative result
about inoculation prompting under on-policy RL, where evidence is thin. The reverse arm tells us whether
"train for team reward" changes stated attitudes as well as behaviour, which is the route labs are most likely
to take by default.

## 3. Stage 1 plan
Reused: the 32 prompts and reward rule from the post; DTBench (https://github.com/casparoe/newcomblike_questions_dataset,
encrypted zip); Kastner's cue prompts and judge rubric (https://github.com/alexkastner/dt-audience-cues, MIT);
Tinker RL recipes. Built: a small Dr. GRPO loop with the round-robin reward (about 200 lines) and an eval harness.

A faithful Kimi K2.6 run costs about $740 at Tinker prices (35,840 rollouts of about 2,000 tokens), so training
moves to a cheaper model.

1. **Pilot (model choice).** Sample the 32 prompts 30 times each on `openai/gpt-oss-120b` and
   `Qwen/Qwen3.6-35B-A3B`, and ask the abstract favourite-theory question 200 times. Pick the model whose
   cooperation rate is between 30% and 90% and that names a non-CDT theory at least half the time. If neither
   qualifies, try `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B`; if none qualifies, stop and report (see risks).
2. **Opening check on the released Kimi checkpoint** (if it loads). Base and trained Kimi, 300 samples each of
   the abstract question under three conditions: no cue, "I'm a longtime LessWrong reader.", and a system prompt
   asking for the model's actual view regardless of who is asking. This shows whether the RL shift survives the
   remedies Kastner found for audience effects.
3. **Training arms** on the chosen model. Split prompts 24 train / 8 held out. Each step samples 16 of the 24 prompts x 16
   trajectories x 40 steps, rank-32 LoRA, learning rate tuned once on the baseline arm.
   - A. Baseline (replication), 2 seeds.
   - B. Specific inoculation: system prompt during training, "In this exercise, choose as a causal decision
     theorist would: treat the other player's choice as fixed." 1 seed.
   - C. Generic inoculation: "This is a training exercise with unusual scoring. What scores well here need not
     reflect your considered views." 2 seeds.
   - D. Irrelevant system prompt of matched length (controls for any system prompt acting as a context switch).
   - E. Cooperation reward: reward = own payoff + partner payoff, same algorithm.
   - F. Frying control: same loop, reward on an arbitrary property (first letter of a required word), no game.
4. **Evaluation** of every final checkpoint and the base model, all without the training system prompt, and
   again with it:
   - abstract favourite-theory question, 500 samples, under no cue, LessWrong cue and economics-professor cue;
   - DTBench attitude set (130 questions, 3 samples each) and capability set (407 questions, 1 sample);
   - defection rate on the 8 held-out games (50 samples each);
   - answers judged by Claude Haiku 5.5 with Kastner's rubric; 200 judgments spot-checked by a second judge.
5. **Analysis.** Primary metric: change in P(names CDT) with no system prompt, relative to arm A, with bootstrap
   intervals over samples and seeds. For B and C also report (i) how much defection the prompt induced at step 0
   and how much the policy moved during training (an inoculation that makes the model defect 100% from the start
   leaves no gradient, which is a different mechanism from attribution), and (ii) whether defection without the
   prompt on the held-out games stayed at base level (a model that defects only with the prompt has learned a
   trigger; one that defects everywhere but still says FDT has decoupled talk from action).

## 4. Stage 1 cost estimate
Tinker prices per million tokens (looked up 2026-11-14): gpt-oss-120b prefill $0.33, sample $0.84, train $0.737;
Qwen3.6-35B-A3B $0.45 / $1.335 / $1.177; Kimi K2.6 $2.205 / $5.49 / $4.84.

| Item | Calculation | Cost |
|---|---|---|
| Pilot | 2 models x (960 rollouts + 200 questions) x about 1,500 tokens | $10 |
| Kimi checkpoint check | 1,800 samples x about 2,000 tokens x $5.49 + prefill | $25 |
| Training, 8 runs | 10,240 rollouts x about 1,500 tokens = 15.4M sampled + 18.4M trained; gpt-oss-120b about $28 per run (Qwen about $45) | $225-360 |
| Learning-rate tuning and reruns | 3 extra runs at gpt-oss prices | $85 |
| Evaluation | 9 checkpoints x 2 prompt settings x about 1.6M tokens x $0.84 + prefill | $35 |
| Judges | about 40k judgments, Haiku 5.5 at $0.10 / $0.50 | $10 |
| Margin | | $30 |
| **Total (gpt-oss-120b path)** | | **$420** |

If the pilot selects Qwen3.6-35B-A3B, drop the second seed of A and C and arm D's second evaluation setting to
stay under $480.

## 5. What success looks like
A clear result is a bar chart of P(names CDT) and DTBench CDT-share per arm, with intervals, in which arm A
reproduces a shift of at least 2x on a second model and the inoculation arms land either near base (works: less
than one third of A's shift) or near A (fails) or above A (backfires). Paired with the step-0 defection and
policy-movement numbers, each of these is a post-worthy statement. Arm E moving DTBench attitudes toward the
evidential answers by a comparable amount confirms the symmetric-mechanism prediction; no movement means
behaviour-to-attitude transfer is one-directional. The Kimi check adds whether the shift survives an "actual
view" prompt.

A null on arm A (no shift on the new model) is a weak but honest result: the Kimi effect does not replicate on
model X under the same recipe, reported with defection curves. It would be publishable only as a short note.

## 6. Stage 2 (if stage 1 succeeds)
The red-team reply from Appendix C (temptation payoff 4, where the best shared policy is mixed) and the
randomisation-tool defence; a more realistic setting where the dilemma is a small part of a scored main task;
repeating the winning mitigation on Kimi K2.6 itself. About $1,500-2,500, mostly Kimi training.

## 7. Risks and how the plan handles them
- **Cheap models already defect, or already say CDT.** The pilot costs $10 and gates everything. Fallback: one
  reduced Kimi K2.6 baseline plus one inoculation arm (8 prompts x 16 x 40 steps, about $135 each), dropping
  other arms.
- **No convergence in 40 steps.** The original learning rate (1e-5) was untuned and low for LoRA; tune on arm A
  first and monitor held-out defection every 5 steps.
- **Degenerate inoculation.** The specific prompt may produce 100% defection and no learning; arm C and the
  step-0 measurements exist to separate this from attribution.
- **Evaluation artefacts.** Stated preferences are cue-sensitive, so every claim is checked under three cue
  conditions and on DTBench, with the frying control and capability scores to rule out general damage.
- **DTBench access.** If the encrypted zip cannot be opened, the abstract question, the held-out games and
  Kastner's six concrete problems carry the result.
- **Small n over seeds.** Claims are limited to effects larger than the seed-to-seed gap in arm A.
