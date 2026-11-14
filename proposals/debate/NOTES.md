# Debate and scalable oversight — reading notes and brainstorm

Written 2026-11-14. All six posts were read in full with `scripts/get_post.py` (the BoN post's appendix prompts were
skimmed, not read line by line). Prices below were looked up on 2026-11-14.

## 1. What each post actually says (verified against the text)

### Recursive forecasting (q2zYtNsh62SCphitt, Jozdien / Alex Mallen, Redwood)
- Purely conceptual. Proposal: for a question resolving at T, at each t the model predicts its own t+1 prediction;
  each step is rewarded against the next prediction, the last against ground truth. Framed as *elicitation* from a
  myopic reward-seeker, explicitly compared to TD learning (Appendix A).
- Appendix B: per-step biases compound down the chain (linearly under Brier, exponentially under log score in
  their toy model); actual training on the chain is claimed to self-correct.
- Limitations listed: reward-signal capture, measurement tampering, self-fulfilling forecasts, fragility when used
  as an optimisation target, the model must believe the setup.
- No experiments, no code. Web search found no empirical follow-up. Tinker's site lists forecasting RL case studies
  (Mantic, Monoid, Lightning Rod) and a "Forecasting" cookbook recipe, none of them recursive/chained.

### RL on Debate Games (6mLwAuFAE98c6R7w3, Lennie Wells, Joan Velja, Shi Feng, Jacob Pfau; MATS 9.0)
- Protocol "Propose-Critique-Decide" (PCD). Proposer solves a MATH problem (768 private reasoning tokens, then a
  public proposal), Critic critiques, Judge returns accept / draw / reject. Rewards (+1,-1) / (0,0) / (-1,+1).
  PCD-2 = one critique; PCD-4 = critique, rebuttal, critic's final response (critic moves last).
- Debaters: Qwen3-30B-A3B-Instruct-2507 (LoRA on Tinker). Judges: Llama-3.1-8B-Instruct (weak) and the same Qwen.
  Data: Hendrycks MATH levels 4-5, 4000 train / 512 test. group_size 8, 64 questions per batch = 512 debates per
  step, ~100 steps, single seed (42). Baselines: RLVR (ground truth) and Consultancy (judge grades proposal alone).
- Results: with the Llama judge, proposer accuracy orders RLVR > PCD > Consultancy; with the Qwen judge the runs
  are not separated. In PCD-4, judge alignment collapses after ~50 steps because P(reject | correct) rises: the
  critic learns "spurious critique" (harsh emotive language) and "back-stab" (agree first, attack in the final
  turn). Same trend, slower, with the Qwen judge. Proposer accuracy still rises.
- Authors' own caveats: one seed; prompts iterated harder for PCD than consultancy; no static-critic baseline
  ("we are particularly interested in 'static Critic' baselining at present"); "truth-seeking" system prompt not
  ablated.
- Suggested patches: large penalty when the proposer can identify a critique as spurious; simultaneous final
  statements. Suggested research questions: when do inference-only experiments predict training dynamics; which
  tasks suit debate; how to measure honesty; decomposition, judge ensembling, cross-examination.
- Cost BOTEC in post: ~$2.50/step, ~$250/run at the then-current prices ($0.12 in / $0.30 sample / $0.36 train per M).
  PCD runs took >12 h wall-clock on Tinker.
- Top comment (emanuelr): co-train the judge as a scientific control; debate can only beat consultancy where
  consultancy's optimal policy is deceptive.

### Superhuman Articulacy (tAwqzanzc9YYnwuK4, Dylan Bowman)
- Conceptual. Lists failure modes of coding-agent prose (invented jargon, inconsistent referents, shorthand,
  assuming shared context, verbosity). Hypothesised causes: LLM judges that see the whole rollout; training to
  talk to other agents, not humans. Proposes a public articulacy eval. No experiments.
- Comments worth using: Lionel Levine suggests RL graded by a judge who sees only a random fragment; Boyd Kane
  warns that a weak LLM is a poor proxy for a low-context human; Hippocleides warns that an articulacy rubric
  cannot tell a clear truth from a clear falsehood.

### Debate with Self-Play Best-of-N (hb8pv3zyAHGJpwz9F, Arcadia Alignment)
- Nested analytic best-of-N min-max over a sampled tree (N=M=50 proposals/critiques, R=20 rebuttals) as an
  inference-time proxy for debate RL. Single-token logprob judge (P(yes)/(P(yes)+P(no))).
- Debaters Sonnet 4.6 (also GPT-5.4-mini, GLM-5.2), reasoning off. Judges Qwen3.6-35B-A3B (main), DeepSeek-v4-Flash,
  Gemma4-12b. 28 questions across LiveCodeBench, ARC-AGI-1, miniF2F-Lean, selected for headroom.
- Results: proposer-only optimisation overfits the judge on LiveCodeBench/Lean; adding a critic removes this;
  rebuttal helps on LCB/ARC, hurts on Lean. Optimising the critic or rebuttal (Bo10) is within error of leaving
  them at Bo1 — "debate's benefits mostly reduce to optimizing against a fixed critique". They say the method
  cannot detect small critic uplifts.
- Cost stated: ~$500 per question with Sonnet 4.6 batch; judging ~$3/question on an H200.
- Limitations stated: BoN is not RL (no cross-question generalisation, so no "universal judge-hacking"); they
  "intend to compare our metric with full training runs". Jacob Pfau's comment: most of the critic benefit is
  averaging over critiques, not adversarial tilting.

### Debate Training Reduces Reward Hacking in RLAIF (BB8o7b8A4Aykeksvw; arXiv 2608.17776, GDM)
- Gemini 2.5 Flash-class policy, frozen Gemini 2.5 Flash Lite judge (8 votes averaged), proprietary AIME-like maths.
  Single-policy RLAIF hacks the judge (accuracy peaks then falls); debate (Alice proposes, Bob critiques) plateaus
  higher, recovering 45% of the gap to RLVR (paper: 74.74% peak for debate vs 77.30% roofline).
- Bob judge-hacks (bold, ALL CAPS, "catastrophic flaw") unless his visible output is capped; limits of 50/100/150
  words tested; at 150 Bob gets more aggressive. Authors flag the trade-off with expressiveness.
- Paper section 4.4 (via WebFetch summary of arxiv.org/html/2608.17776, first 100k chars only): "preliminary debate
  experiments permitting draws or using frozen API critics performed similar or worse than RLAIF-AA, indicating
  that co-training Bob with Alice is essential" — no numbers given. Appendix F: training Bob alone to convince the
  judge of the *correct* verdict is "slow".
- No code or data release found. Models are closed.
- Future work named: fuzzy tasks (with a stronger held-out judge as proxy ground truth), reducing later-turn hacking.

### Obstacles to scalable oversight of auto-alignment (PBGKWNrJAbpDgSsPo, Arcadia)
- Argues fuzzy tasks lack a natural decomposition into verifiable claims: heuristic claims, probabilistic claims,
  mis-aggregated correlated evidence. Text-based GeoGuessr (Fable 5 descriptions of images) as a fuzzy task with
  ground truth.
- BoN-proxy results are negative: no uplift on 10 GeoGuessr questions (Opus 5 debaters, Qwen3.5-9B judge) and on
  11 pairwise LMCA questions (Sonnet 4.6, Qwen3.6-35B judge). Footnote: a replication by Vincent Cheng saw some
  positive uplift on GeoGuessr.
- Suggested test: does oversight training on GeoGuessr improve verbalisation or just persuasion?
- I found no public link to the text-GeoGuessr dataset in the post.

## 2. What is public (checked)

| Resource | Status |
|---|---|
| https://github.com/Debate-FP9/lw-progress-update-snapshot | Public (README and `prompts/4ply_pcd.yaml` fetched via raw.githubusercontent.com). Contains prompts, `src/env.py`, `src/game_engine.py`, `src/judge.py`, `src/scorers/math_grader.py`, `src/eval_debate.py` (inference-only via OpenRouter), `experiments/*.sh`, vendored tinker-cookbook. README warns the original models were retired from Tinker on 2026-06-12, so a current model must be swapped in. |
| https://github.com/ArcadiaImpact/debate-bon-public | Public (README fetched). `arcadia run configs/...`, analytic estimators in `metrics/accuracy_analytic.py`, `metrics/reducers.py`, `scripts/worms.py`; benchmark adapter template. Expects a RunPod vLLM judge. Transcripts only "on request". |
| https://joanvelja.com/transcripts | Page exists but is a JS app; I could not confirm a bulk download. 20 questions x 6 checkpoints per the post. |
| GDM paper code/data | Not found. |
| Text GeoGuessr set | Not found public. `osv5m/osv5m` (HF) could be used to rebuild one. |
| HF datasets | `EleutherAI/hendrycks_math`, `emozilla/quality`, `livecodebench/code_generation_lite`, `osv5m/osv5m` all resolve, ungated. |
| github.com HTML / API | Blocked in this session; raw.githubusercontent.com works. I did not inspect repo file trees beyond the READMEs. |

Other related posts found: "Inference-time Generative Debates on Coding and Reasoning Tasks" (kQCLPighFvb4ChHtu;
inference-only, debate loses to consultancy in 11/16 conditions); "Exploration Hacking in AI Debate"
(xjwtNid2xjqSJWB7z; critic-only LoRA RL on Llama-3.1-8B against a frozen liar, sandbagging organisms);
"Suggestions for improving debate protocols" (D4tBvaQSc6uFnxisp; policy-debate rules, conceptual);
Lennie Wells' later posts (72AAjXAxS7Pow9Fie, qqyxTYssqLgFsjvJu) are on RL initialisation and grader-targeting,
not debate protocols. Raul Cavalcante commented that he is working on an "open debate" protocol against
programmatic reward hacking (unpublished). I found no published static-critic RL comparison, no published
defence-vs-trained-critic study, and no published BoN-vs-RL comparison as of today.

## 3. Prices looked up (2026-11-14)

Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/), $ per M tokens, prefill / cached prefill / sample / train:
- Qwen/Qwen3-8B (32K): 0.195 / 0.039 / 0.60 / 0.44
- openai/gpt-oss-20b (32K): 0.18 / 0.036 / 0.45 / 0.396
- Qwen/Qwen3.5-4B: 0.33 / 0.066 / 1.005 / 0.737
- Qwen/Qwen3.5-9B: 0.30 / 0.06 / 0.807 / 1.463
- Qwen/Qwen3.6-35B-A3B (64K): 0.45 / 0.09 / 1.335 / 1.177
- openai/gpt-oss-120b (32K): 0.33 / 0.066 / 0.84 / 0.737
- No Llama models and no Qwen3-30B-A3B on Tinker now. The original debate runs would cost roughly 3-4x the post's
  $250 on Qwen3.6-35B-A3B today.
- The MATS post's BOTEC counts "backprop" tokens as the whole sequence (context + generation); I assume the train
  price applies to all tokens in the forward-backward pass.

OpenRouter (`/api/v1/models`), $ per M input / output:
- meta-llama/llama-3.1-8b-instruct 0.02 / 0.04 (logprobs supported)
- meta-llama/llama-3.2-3b-instruct 0.051 / 0.335 (logprobs)
- google/gemma-3-4b-it 0.05 / 0.10 (logprobs); google/gemma-3-27b-it 0.08 / 0.35
- qwen/qwen3-30b-a3b-instruct-2507 0.10 / 0.30 (logprobs) — the MATS debater is still served here
- qwen/qwen3.6-35b-a3b 0.10 / 0.90; qwen/qwen3.5-9b 0.131 / 0.193
- anthropic/claude-haiku-5.5 0.10 / 0.50; anthropic/claude-sonnet-5.5 2 / 10; anthropic/claude-opus-5.5 4 / 20
- openai/gpt-5.4-nano 0.20 / 1.25; google/gemini-3.1-flash-lite 0.25 / 1.50
- anthropic/claude-sonnet-4.6 3 / 15 (the BoN post's debater)

GPU rental prices were not looked up; none of the proposals needs a rented GPU.

## 4. Brainstorm

Judged on: doable by Claude agents in ~2 days for <= $500; natural next step; result people would care about.

**Written up**

1. **Judge-side defences against an adaptively RL-trained critic (proposal 01).** Both RL papers report the same
   failure (critic hacks the judge with emphatic, spurious critiques) and the only tested fix is a word cap that
   the GDM authors themselves dislike. Training only the critic against a frozen proposal pool is ~10x cheaper
   than self-play and isolates the critic-vs-judge game. Each defence is tested twice: against a critic trained
   without it, and against a critic retrained with it in the loop. Informative either way (style exploit vs
   content fabrication). ~$420.
2. **Frozen vs co-trained critic in real RL, plus a BoN forecast (proposal 02).** A live disagreement: GDM says
   co-training is "essential" (no numbers), Arcadia's BoN proxy says optimising the critic adds nothing, and the
   MATS authors say this is the baseline they most want. Needs full proposer RL so it is the most expensive and
   the noisiest of the three; scaled down to Qwen3-8B to fit. ~$460.
3. **Does a full-context judge train context-assuming prose? (proposal 03).** A direct RL test of the articulacy
   post's main causal hypothesis and Levine's fragment-judge suggestion, on SWE-bench issue+patch explanations
   with a context-free reader as the outcome metric. Less central to debate, but cheap and a clean causal
   question. ~$380.

**Rejected or folded in**

4. *BoN-vs-RL calibration as a standalone project.* Both the MATS and Arcadia posts ask for it. Standalone it
   needs the same RL runs as idea 2, so it is folded into proposal 02 as a pre-registered forecast.
5. *Full self-play with a patched protocol (simultaneous final statements, spurious-critique penalty).* The MATS
   authors' own next step and they have moved to a faster stack. A fair test needs several self-play runs per
   patch at ~$50-250 each; does not fit $500 with seeds. Kept as stage 2 of proposal 01.
6. *Co-train the judge on ground truth as a scientific control (emanuelr's comment).* Interesting, but a
   three-model training loop is fragile and expensive for two days. Rejected on feasibility.
7. *Protocol iteration on text GeoGuessr (probabilistic decomposition, likelihood-ratio protocol, judge with
   search).* Dataset not public; Arcadia is actively doing exactly this and already has a mixed replication.
   With cheap debaters (Haiku 5.5 at $0.10/$0.50) a BoN tree is affordable, but the design space is open-ended
   and an ambiguous result is the most likely outcome. Rejected: low marginal value over the authors' own work.
8. *Judge-stability diagnostics on fuzzy debates (Nayara Fonseca's comment).* Cheap, but needs the unreleased
   GeoGuessr transcripts and is a diagnostic rather than a finding. Rejected.
9. *"Verbalisation or persuasion?" on GeoGuessr (does judge-optimisation make explanations more faithful).* Nice
   question from the Obstacles post; needs a faithfulness ground truth for heuristic claims that does not exist.
   Rejected as under-specified for two days.
10. *Recursive forecasting toy test.* Three variants considered. (a) Train a small forecaster with only
    one-step rewards on synthetic time series: this is TD learning and would work, telling nobody anything.
    (b) Prompted chains on resolved questions with dated news: needs a leak-free retrieval pipeline; fragile.
    (c) Test the proposal's real claim (a myopic reward-seeker is better elicited by the chain): needs a
    convincing reward-seeker model organism, which is a project in itself. Rejected: no version is both cheap
    and informative about the post's actual claim.
11. *Bias-compounding measurement (Appendix B) by asking current models "what will you forecast next month".*
    Cheap, but measures prompt sensitivity of today's models, not incentive effects. Rejected.
12. *Static articulacy benchmark with rubric grading.* The post's own "naive idea". Building a benchmark from
    scratch without human validation is weak; the RL causal test (proposal 03) is more informative and yields the
    reader-accuracy metric as a by-product.
13. *Replicate the GDM result on open models.* Largely what the MATS post already is; proposal 02 covers the
    consultancy-vs-debate comparison as a side effect.
14. *Extend "Inference-time generative debates" (false-positive inflation) to PCD.* Inference-only and cheap,
    but the field has moved to training; low interest.
15. *Debate on SimpleQA-style knowledge tasks (MATS authors' preliminary negative).* Would need RL per task;
    expected null. Rejected.

## 5. Notes for a reviser

- Proposals 01 and 02 both fork the MATS snapshot and must replace the retired Tinker models. I chose Qwen3-8B as
  the trained model because Qwen3.6-35B-A3B is ~2.7x dearer per train token. That makes the trained model the same
  size as the Llama-3.1-8B judge; both proposals include an early check and a weaker-judge fallback
  (Gemma-3-4b, Llama-3.2-3B).
- Per-step cost figures are my own token estimates, not measured. They should be re-measured in the pilot.
- I could not confirm that the trained-critic transcripts at joanvelja.com are downloadable; no proposal depends
  on them.
- Wall-clock is a real constraint: the MATS PCD runs took >12 h each at 512 debates/step. The proposals use 256
  rollouts/step, shorter generations and parallel runs, but a second full iteration within two days is unlikely.
