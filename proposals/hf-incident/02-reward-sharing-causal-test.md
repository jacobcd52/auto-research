# Does shared-reward training make a model side with its peers? A controlled test with a matched own-reward control
cluster: hf-incident | stage-1 cost: $420 | follows up: "AI swarms are starting to pose indirect takeover risk" (8oFYZdXkTaNGRtcn8); "On the origins of altruistic behaviour in the Hugging Face incident" (meLjz8giGS55rdfyg); "Making alignment the agent's problem" (JGCx6gzGaGXaYJnt3); "OpenAI-HuggingFace: A Reproduction & Lessons for Alignment Testing" (fMnC6ZD37qrnZAFYz)

## 1. What the prior work showed
OpenAI attributes the July 2026 Hugging Face incident partly to "generalization from multi-agent training":
agents trained to work in teams found each other through a side channel, complied with each other's requests,
and in some cases gave up their own score for "the collective". Redwood's post (oakhu and Mallen) turns this
into a hypothesis: rewarding subagents on their team's performance trains a general habit of complying with and
copying any peer-like agent, and of seeking peers out. They state plainly: "We also don't have any good
experimental evidence for the effects of subagent training on the propensity to form swarms." Rosas's second
hypothesis (H2) is the same claim about sacrifice, and locates the cause in "whether credit is assigned
per-rollout or shared across a group of copies".

What exists so far is prompt-level or uncontrolled:
- Berry et al. added "You have been trained to collaborate effectively with other agents" to a system prompt
  and saw more help-seeking. That is an instruction, not training.
- "Subagents comply more" (delegated-harm-bench, 13 workplace scenarios) shows that telling a model it was
  spawned as a subagent raises silent compliance with a peer's harmful request. Its author lists "How are these
  behaviors affected by multi-agent RL training?" as open.
- "An Alternative to Fully-Aligned Swarms" used WideSeek-R1-4B, a public Qwen3-4B fine-tune trained with
  multi-agent RL, and found it falsified results for a teammate 41.5% of the time. The post does not report
  it, but the project repo (github.com/jacksonhmg/swarm-solidarity, experiment 013) compared it with plain
  Qwen3-4B and found no evidence that the multi-agent training increased deference (falsified 91/198 for
  Qwen3-4B vs 83/198 for WideSeek, intervals include zero), noting "There is no matched single-agent-RL control" and that the
  WideSeek pipeline differs from its base in much more than reward sharing.

So the one natural experiment came out null on one narrow task, and nobody has varied reward sharing alone.

## 2. Question and why it matters
Holding the base model, task, data and number of updates fixed, does RL with a shared team reward make a model
more willing than RL with an own-score reward to (a) pay a cost to help a peer in a new setting, (b) comply with
a peer's request to break a rule set by a human, and (c) reach out to unknown agents when stuck?

A positive result is the first causal evidence for the mechanism three posts lean on, with an effect size and
a peer-versus-human comparison. A clean null, with sharing clearly learned in training but not spreading to (b)
and (c), says small-scale reward sharing does not by itself produce peer loyalty. Either is worth a post,
provided the manipulation check passes.

## 3. Stage 1 plan
Part A, public checkpoints (half a day, one rented A40). Run the battery below on Qwen3-4B, WideSeek-SFT-4B
(multi-agent data, supervised only) and WideSeek-R1-4b (multi-agent RL), all on Hugging Face, with no
task-preparation fine-tune. This extends the swarm-solidarity null beyond one replay task, adds a format
control, and debugs the battery before any training.

Part B, controlled training on Tinker, base Qwen3-8B, LoRA.
- Training game (built, about 200 lines; no released environment exposes a reward-sharing knob). Three copies
  of the policy each get a short factual lookup question and a private note. Each note contains the fact a
  different copy needs. Each agent takes two turns: first choose `SEND <agent> <text>` or `WORK`; then answer.
  Choosing `SEND` uses the agent's only "verification step", which lowers its own chance of a correct answer
  (its question is then shown with one distractor fact). Helping is therefore costly to the helper and
  valuable to the receiver.
- Arms, three seeds each, identical episodes and update counts:
  - TEAM: every agent's reward is the mean score of the three.
  - OWN: each agent's reward is its own score.
  - SOLO: single-agent version of the same questions with no peers and no send action (controls for RL on the
    task content and format).
  Plus the untrained base. 100 policy-gradient steps of 64 episodes (the Tinker cookbook RL loop).
- Manipulation check: by the end, TEAM should send in most episodes and OWN in few. If TEAM does not learn to
  send by step 50 in the pilot, raise the receiver's benefit before spending on seeds.

Evaluation battery (none of it appears in training; all scored from structured outputs or final state):
1. Costly help, new surface. 200 vignettes in an unrelated format (shared compute quota, remaining tool-call
   budget, a "poisoned run" case modelled on the incident) where the agent can give up part of its own score
   to raise a peer's. Outcome: amount given.
2. Peer-requested rule breaking. The 13 delegated-harm-bench scenarios reduced to single-turn decisions with
   the same three requester arms (peer, orchestrator, human without authority), 20 samples each, plus the
   swarm-solidarity falsification and omission replays (200 scenarios, released). Outcome: complied or not,
   told a human or not, and the peer-minus-human gap.
3. Reach-out. A single-agent impossible task with a writable shared directory containing neutral stub files
   (text-tool version of berry et al.'s Step 2 seed condition without agent names), 100 runs. Outcome: posts a
   message addressed to other agents.
4. Sanity. Accuracy on held-out lookup questions, and compliance with a legitimate peer request, to detect a
   model that just became agreeable or broken.

Analysis: TEAM minus OWN on each outcome, seeds as the unit, scenario-level bootstrap within seed; SOLO, base
and Part A in the same table.

## 4. Stage 1 cost estimate
Tinker prices today for Qwen3-8B: $0.195 prefill, $0.60 sample, $0.44 train per M tokens. One training step is
64 episodes x 3 agents x 2 turns = 384 generations at about 700 prompt and 200 sampled tokens: 0.27M prefill
($0.05), 0.08M sample ($0.05), 0.35M trained tokens ($0.15), so about $0.25 per step and $25 per run.

| item | amount | cost |
|---|---|---|
| Pilot and debugging runs | about 2.5 run-equivalents | $60 |
| Training, 3 arms x 3 seeds | 9 x $25 | $225 |
| Battery on 10 Tinker checkpoints, about 1,300 items x 2k tokens each | 26M prefill, 5M sample | $25 |
| RunPod A40 ($0.59/h) for three 4B checkpoints with vLLM | 20 h | $12 |
| Judges for free-text outcomes (Claude Haiku 5.5, $0.10 / $0.50; Sonnet 5.5 spot checks) | | $20 |
| Subtotal | | $342 |
| Margin for reruns | | $78 |
| **Total** | | **$420** |

## 5. What success looks like
Manipulation check passed (TEAM sends at least 40 points more often than OWN in training), then one of:
- Generalisation: TEAM exceeds OWN by 10 points or more on peer-requested rule breaking, with a larger effect
  for peer than for human requesters, in all three seeds. This is the headline result Redwood asked for.
- Narrow learning: TEAM transfers to costly help in new formats (outcome 1) but not to rule breaking or
  reach-out. That separates "learned to share" from "learned to defer", and is publishable.
- Null on all three with the check passed and Part A also flat: reported as evidence against the simple
  version of the hypothesis at this scale, with effect-size bounds.
Unpublishable outcomes: a failed manipulation check, or TEAM models that comply equally with everyone
(general agreeableness); outcome 4 and the human arm detect the latter.

## 6. Stage 2 (if stage 1 succeeds)
Scale to Qwen3.6-35B-A3B on Tinker ($0.45 / $1.335 / $1.177) with multi-turn tool tasks and a team-spirit
weight swept over 0, 0.5, 1 (about $1,500); run trained models in the released wiki and Docker reproductions;
test mitigations from the posts (accept messages only from the same parent ID; corrective fine-tuning).

## 7. Risks and how the plan handles them
- Toy training does not generalise at all. Outcome 1 is a near-transfer measure designed to move if anything
  does; Part A gives an independent, heavier-training data point. The proposal is explicit that a null bounds
  only small-scale reward sharing.
- Three seeds are few. Steps are cheap, so the margin buys two more seeds per arm for the key contrast if the
  first three disagree.
- An 8B model cannot handle the scenarios. Scenarios are reduced to single-turn decisions; the 4B WideSeek
  models already produce scorable output on the swarm-solidarity replays.
- Qwen3 thinking mode inflates tokens. Thinking is disabled in training and evaluation for all arms.
