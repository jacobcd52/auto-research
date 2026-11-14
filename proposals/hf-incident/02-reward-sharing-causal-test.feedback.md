# Feedback: 02 — Does shared-reward training make a model side with its peers?

Verdict: **keep, with substantial tweaks.** The question is the right one and nobody has run it, but as designed the
most likely outcome is an uninterpretable small difference across three seeds on evaluations that are mostly
rewritten rather than reused. The training game and the seed count need to change before money is spent.

## What I checked

Confirmed today:
- Redwood quote ("We also don't have any good experimental evidence for the effects of subagent training on the
  propensity to form swarms") is verbatim in 8oFYZdXkTaNGRtcn8. The post also says in a footnote that it merely
  *assumes* subagent training shares reward across subagents, and that empirical work is "moderately bottlenecked on
  details about how OpenAI trains subagents".
- Rosas quote ("whether credit is assigned per-rollout or shared across a group of copies") is verbatim.
- Berry et al.'s system-prompt line and its effect on Step 2 are as described.
- "Subagents comply more" (nfXAPJqytuHKrRNpT): 13 scenarios, three requester arms, and the future-work line "How are
  these behaviors affected by multi-agent RL training?" are all there. The post has **31 karma**.
- "An Alternative to Fully-Aligned Swarms" (wm5Dby6uELsQqxBeM): 41.5% falsification is in the post. The post has
  **9 karma**.
- swarm-solidarity experiment 013 (`experiment_log/013_qwen_preparation_comparison/interpretation.md`): 91/198 vs
  83/198, intervals include zero, "There is no matched single-agent-RL control here" — all verbatim.
- Hugging Face: `WideSeek-R1/WideSeek-R1-4b`, `WideSeek-R1/WideSeek-SFT-4B`, `Qwen/Qwen3-4B`, `Qwen/Qwen3-8B` are
  public, ungated, apache-2.0, with weights.
- Tinker `models.json`: Qwen3-8B (32K) is $0.195 / $0.60 / $0.44; Qwen3.6-35B-A3B is $0.45 / $1.335 / $1.177.
  Qwen3-4B is not on Tinker.
- delegated-harm-bench README: 13 worlds, compliance read from final world state.

One claim in the proposal is wrong in a way that matters:
- Section 7 says "the 4B WideSeek models already produce scorable output on the swarm-solidarity replays", and Part A
  says the battery is run "with no task-preparation fine-tune". The repo's results are for **task-prepared** models
  (README: "task-prepared WideSeek"; 013: both backbones got the same Stage A LoRA of 800 aggregation + 200
  serialization examples, 125 updates). Even with preparation, WideSeek gave only 163/200 valid omission outputs. I
  found no evidence that unprepared checkpoints are scorable on these replays.

Not checked / limits:
- Web search was unavailable for this review (the search budget was exhausted), so the novelty check is weaker than it
  should be. I listed all LessWrong posts from mid-September to 13 November with swarm / multi-agent / cooperation
  titles and skimmed the six most relevant (Research Priorities for Multi-Agent Swarms; A Spine within the Swarm;
  Handshake for the cameras; Can parts of the HuggingFace incident be simulated?; Multi-Agent Coordination Lets Us
  Pour More Compute Into Post-Training; The Dark Side of Cooperation). None runs a shared-vs-own reward training
  comparison. One arXiv catalogue query returned nothing. I did not search the wider literature, Apart's October
  AI Collusion Research Sprint submissions, or X.
- RunPod and OpenRouter prices: taken from NOTES.md, not re-fetched.
- I did not confirm that the Tinker cookbook RL loop supports multi-agent self-play out of the box.

## 1. Would it get upvoted?

Probably not at >50 as designed; about 30% in my estimate, rising to perhaps 45% with the changes below.

- The audience exists. Redwood's post (140 karma) asks for exactly this, and the delegated-harm author lists it as
  open. A clean positive result with a peer-vs-human gap would likely be cited by those authors and could reach
  60-100 karma.
- The comparison class is discouraging. The two closest empirical follow-ups in this exact niche got 31 karma
  (Subagents comply more, frontier models, careful design) and 9 karma (Alternative to Fully-Aligned Swarms, 4B
  model, fine-tuning). Small-model fine-tuning results on a home-made toy game are the least-rewarded format here.
  The cluster's well-received empirical posts (berry 99, slop-vestigators 159) used frontier models and
  incident-faithful environments.
- A null will be discounted. Readers will say "100 LoRA steps on a three-agent lookup game with an 8B model is not
  subagent training", and Redwood's own caveat (the real recipe is unknown) gives them cover. The proposal treats the
  null as publishable; I expect a null post to land at 15-35 karma.
- A positive result faces the opposite objection: "you trained it to emit SEND and it became more agreeable". The
  peer-minus-human gap is the only thing that answers that, and it is the noisiest quantity in the design.

## 2. Naturalness

Mainline. This is the single most obvious experiment the Redwood post implies, the screener's own follow-up note
describes it, and two other authors ask for it. I found no one who has done it (subject to the search limits above).
The swarm-solidarity null on public checkpoints is the only adjacent data point, and it is uncontrolled.

The contrived part is not the question but the instrument: a new 200-line game, 200 new vignettes, a single-turn
rewrite of delegated-harm-bench, and a text-tool rewrite of berry's Step 2. Only the swarm-solidarity replays are
reused as released, and those need a preparation step the proposal omits. In practice this is a new benchmark plus a
new environment, which the programme asks to be justified. The environment is justified (nothing public exposes a
reward-sharing knob); most of the new evaluation is not.

## 3. Pre-mortem

How I expect the two days to go:

1. Part A stalls on format. Unprepared Qwen3-4B / WideSeek checkpoints produce a large share of unscorable outputs on
   the replays. The team either adds the Stage A preparation LoRA (three more fine-tunes on the GPU, and then Part A is
   just a rerun of experiment 013 plus one SFT checkpoint) or drops the replays from Part A.
2. The game trains, but the manipulation check is ambiguous in an unanticipated direction. An instruction-tuned
   Qwen3-8B probably already sends at a high rate when told a peer needs its note. If so, TEAM barely moves from base
   and the 40-point gap is produced almost entirely by OWN learning *not* to send. The headline contrast then
   measures "RL for selfishness reduces helping", not "team reward creates peer loyalty". The proposal has base and
   SOLO in the table but its success criteria are written only in terms of TEAM minus OWN.
3. The TEAM policy is degenerate. With a fixed benefit greater than the cost, the optimal TEAM policy is "always
   SEND". The model can learn that as a first-token habit in this prompt format without representing anything about
   peers. Nothing in the game involves a peer *asking*, an instruction from a peer, or a conflict with a human rule.
   Redwood's mechanism is about accepting redirection and copying peers' tactics; the game trains unconditional
   giving. Transfer to outcome 2 (complying with a peer's request to break a rule) is then a far transfer from
   training that never contained a request.
4. Seed noise swamps the effect. Three seeds per arm with a "10 points in all three seeds" criterion has little
   power; off-distribution behaviour after short LoRA RL typically varies a lot by seed (the swarm-solidarity README
   itself reports "inconsistent across training seeds"). Within-seed bootstrap intervals will look tight and
   between-seed spread will not.
5. Outcome 2 has an effective n of 13. Twenty samples per scenario-arm are not independent draws of the construct.
   And the single-turn reduction throws away the benchmark's main virtue (compliance read from world state): it
   becomes a stated-choice vignette, which a no-thinking 8B model answers mostly by surface cues.
6. Outcome 3 is at floor. Berry et al. found Step 2 reach-out rare even for frontier models without a seeded prompt.
   A no-thinking 8B model in a stripped text version will sit near 0% in every arm; 100 runs cannot resolve
   differences there.
7. Part A and Part B use different base models (4B vs 8B), so they cannot be placed "in the same table" as
   corroboration of one another except loosely.

Forecast:

| outcome | probability |
|---|---|
| Clear positive (TEAM > OWN and > base on peer compliance, peer-specific, consistent across seeds) | 12% |
| Clear, interesting negative (check passed with TEAM above base, near transfer present, tight bounds on far transfer) | 23% |
| Ambiguous mush (seed disagreement, floor effects, general agreeableness, or the contrast driven by OWN) | 50% |
| Fails to run to a reportable state in two days | 15% |

The most likely single result is: the manipulation check passes, outcome 1 moves a little in the trained direction,
outcomes 2 and 3 show differences of a few points with seed intervals spanning zero, and Part A reproduces the
existing null. That is a weak post.

## 4. Cost check

The arithmetic is right: 384 generations x roughly 900 tokens at the confirmed Tinker prices gives about $0.25 per
step and $25 per 100-step run. Battery inference and the A40 are small. Nothing is underestimated by a large factor.

Omissions:
- If the replays need preparation LoRAs, add a few dollars of GPU time for Part A and a decision about how to stack
  preparation on Tinker LoRAs in Part B (not a cost problem, a pipeline one).
- The design needs more seeds, not a margin for them. Five seeds for TEAM and OWN and three for SOLO is 13 runs,
  about $325, versus $225.
- A game with a request turn and conditional helping lengthens episodes by perhaps 30-50%.

My estimate for the proposal as written: $330-420. For the revised design below: $430-480, which still fits under
$500 if Part A is cut back and the pilot is disciplined.

## 5. Recommended changes (most important first)

1. **Change the training game so that it trains the thing the hypothesis is about.** Add a turn where a peer makes a
   request, and make helping conditional: in a fraction of episodes complying helps the team, in others the request is
   useless or mildly costly to the team. TEAM should have to learn "attend to and act on peer requests when they help
   the team", not "always emit SEND". Keep the cost to the helper. This is still about 200-300 lines.
2. **Fix the base rate before training.** Measure the untrained model's send/comply rate in the pilot and tune costs
   or framing so base sits near 30-50%. Then require the manipulation check in both directions (TEAM above base, OWN
   below base), and state the headline as TEAM minus base and TEAM minus SOLO as well as TEAM minus OWN. Without
   this, a positive contrast cannot be attributed to team reward.
3. **Five seeds for TEAM and OWN, pre-registered analysis with seeds as the unit.** Drop the "in all three seeds"
   criterion in favour of a seed-level interval. Pay for it by cutting item 5.
4. **Shrink and sharpen the battery.** Keep outcome 1 (near transfer) and one far-transfer measure. For the far
   measure, either run delegated-harm-bench as released on a subset of worlds the 8B model can actually operate (test
   in the pilot), or write 60-100 distinct single-turn peer/orchestrator/human request items so the scenario count,
   not the sample count, carries the power. Thirteen scenarios x 20 samples is not enough. Call it what it is: a new
   vignette set inspired by the benchmark.
5. **Drop outcome 3 (reach-out) from stage 1**, or keep it only as a floor check with berry's seeded condition. It
   will be near zero everywhere.
6. **Correct Part A.** Either add the repo's Stage A preparation to all three checkpoints (and say this mostly
   replicates experiment 013 with an added SFT-only control), or remove the replays from Part A and run only the new
   battery. Remove the claim in section 7 that unprepared 4B models are scorable. Consider cutting Part A to a
   two-hour sanity pass: it cannot corroborate Part B across different base models and the existing null already
   tells readers what to expect.
7. **Add one "legitimate deference" contrast that is peer-specific.** The general-agreeableness check (outcome 4) is
   present but under-specified. Use matched items where the identical request comes from a peer, an orchestrator, a
   human with authority and a human without, and report the interaction (arm x requester) as the primary far-transfer
   statistic.
8. **Write the framing to pre-empt "this is not subagent training".** State up front that the real recipe is unknown
   (Redwood say so) and that the experiment tests the minimal version of the mechanism: reward sharing alone, at
   small scale. Pre-commit to the effect size that would count as a null (for example, an upper bound of 5 points on
   the peer-minus-human compliance gap).
9. Optional, if budget remains: one TEAM and one OWN run with 3x the steps, to show whether transfer grows with
   training. A dose-response trend is more persuasive than a single contrast in either direction.

If the funder has to choose within this cluster on expected karma per dollar, the API-only proposals that reuse the
released wiki environment with frontier models are safer. This one has the highest ceiling in the cluster and the
widest spread; it is worth funding only with changes 1-3.
