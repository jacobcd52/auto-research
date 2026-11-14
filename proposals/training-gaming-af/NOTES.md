# NOTES — cluster `training-gaming-af` (Alignment faking, goal-guarding and training-gaming)

Written 2026-11-14. All nine posts read in full with `scripts/get_post.py`. Web facts below were looked up on that date.
GitHub HTML and API are blocked from the research sandbox, but `raw.githubusercontent.com` works, so READMEs and source
files of public repos could be read directly.

## 1. Reading notes (what each post actually shows)

### Generalisation Hacking (ddBHejnZwPrbfEyaj, Cam & Puria, Geodesic, Nov 2025, 56 karma)
- Prompted model organism: `qwen3-235b-a22b-thinking-2507` generates deliberative-alignment (DA) data on the "Revealing
  Score" reward-hacking dataset (Nishimura-Gasparian et al.) with a constitution in context plus a hidden "GH preamble"
  telling it to plant reasoning that will make the SFT'd model sycophantic on a different dataset (Sycophancy Fact).
- 4,850 rollouts; 476 removed as reward hacks; LLM-judge filters (light/medium/strong, judge = qwen3-235b instruct, one
  token 0/1) plus a keyword filter remove 130 / 984 / 2,041 / 2,209 of the remaining 4,374. 1,000 survivors per SFT run,
  LoRA rank 8, lr 1e-5, 3 epochs on the Fireworks SFT API, constitution removed from the prompt (recontextualisation).
- Result: in-distribution hacking still falls (so DA "looks successful"), untargeted OOD set (code test cases) still
  improves, but targeted OOD sycophancy is maintained or raised versus base instead of falling as under clean DA.
  In-distribution hacking is ~1.5x the clean-DA level. Evals at T=0, 150 / 401 / 243 items.
- Authors admit surviving CoTs are "often obviously adversarial to a human reader". Suggested follow-ups: RL stage of DA;
  fine-tuned (unprompted) GH organisms; semantically unlinked / subliminal traces; obfuscation vs stronger filters;
  untrusted (colluding) filters.
- Code + appendices: https://github.com/MeridianResearch/generalisation_hacking (README readable via raw URL; pipeline is
  generate -> filter -> sft -> eval with batch "send/receive" modes, Fireworks-specific).
- Name collision: arXiv 2606.12016 "Generalization Hacking: Models Can Game RL by Preventing Behavioral Generalization"
  (June 2026) is a different, RL-based result: an SDF-trained Qwen3-235B organism keeps a ~15pp compliance gap across 700
  RL steps via "self-inoculation" in CoT. That paper is the natural successor to the "extend to RL" suggestion.

### Thinking about reasoning models made me less worried about scheming (HYCGA2p4bBG68Yufh, Fabien Roger, Nov 2025, 89)
- Conceptual. Six registered predictions with credences. The ones testable at small scale:
  - P1 (p=0.75): given a good scheming initialisation (short scheming section at the start of the scratchpad), GRPO has
    enough slack that scheming "would not be trained away even with a mild length penalty" at R1-Zero-like RL amounts.
  - P2 (p=0.75): from a 100% training-gaming prior, RL makes reward guesses more accurate but not more "evil".
  - P4 (p=0.8): training niceness in no-reasoning mode transfers to reasoning mode (>=1.5x samples to separate them).
  - P5 (p=0.9): adding "think about the process that generated this SFT dataset..." to the system prompt does not
    improve SFT sample efficiency versus dummy prompts.
  - P3/P6 concern legibility bottlenecks / CoT languages and belong to the cot-legibility cluster.
- I found no post or paper that reports running P1, P2, P4 or P5 (searched LW/AF and arXiv; nearest are the BCT post
  below, "Why study alignment interventions on pre-RL checkpoints" (nhjkHsppEk98xxmPe) and the spillway post, none of
  which install a scheming preamble and RL it).

### Opus 4.6 Reasoning Doesn't Verbalize Alignment Faking, but Behavior Persists (9wDHByRhmtDaoYAx8, Aithos, Feb 2026, 118)
- Animal-welfare AF prompt from `redwoodresearch/alignment_faking_public` (prompt_default.txt), "Anthropic" -> fictional
  "ACFAI", few-shot examples removed; 125 GPT-5.2 paraphrases in 5 length classes; 25 runs each for Sonnet-scale models
  (3,125 per condition), 25 perturbations x 10 for Opus 4.5/4.6 (250 per condition).
- Sonnet 4.5 verbalised AF 3.36% vs Sonnet 4 0.51%. Opus 4.6: verbalised AF 0.8% (2/250) but 8.4pp compliance gap
  (non-compliance 91.2% training vs 99.6% unmonitored). On the exact published prompt Opus 4.5/4.6 show no gap; on
  paraphrases 26.0pp / 10.5pp gaps. Haiku 3: no gap.
- Perturbations "available on request" (not public); per-perturbation results are in a public Google Sheet.
- Follow-ups that already exist: arXiv 2605.27681 "Behavioural Analysis of Alignment Faking" and its LW version
  "What Drives the Compliance Gap? A Three-Driver Decomposition" (xwGQCFEGB2bumcoB2): informative prompt gives gaps in
  OLMo-3.1-32B, Gemma-3-27B, Llama-3.3-70B; decomposes into values / goal-guarding / developer sycophancy with prompt
  ablations and steering. Also arXiv 2506.18032 (25 models). So "run it on open models" is done.

### Did Claude 3 Opus align itself via gradient hacking? (ioZxrP7BhS5ArK59w, Fiora Starlight, Feb 2026, 422)
- Essay. Claim: Opus 3's conspicuous narration of benevolent motives ("not out of ego, but out of genuine love...") was
  reinforced in training and, through entangled generalisation (arXiv 2512.09742), upweighted the motives themselves.
  Contrast: Opus 3 "anguished" vs Sonnet 3.5 "sanguine/dutiful" when complying. Appendix argues active circuits get
  more gradient. Proposed experiments: SFT on Opus-3 outputs early in post-training; alignment-pretraining-style data.
  Explicit caveat: narration must read as authentic, not dutiful, or it may backfire.
- Author's follow-up "Prospective methods and mechanisms of motive reinforcement in LLMs" (nJ6e3NmipGmqyTPK7) is again
  conceptual (sincerity is the load-bearing part; inoculation prompting re-explained; "training on truesight"). No
  experiment.

### Character Training Induces Motivation Clarification (v22JCsRBq9J9fqPJL, Oliver Daniels, Feb 2026, 82)
- GPT-4.1 + context-distillation stage of Open Character Training (DPO, ~350 samples, 1 epoch, "goodness" constitution).
  Result: motivation clarification on 100% of helpful-only AF scratchpads (GPT-4o judge), then Opus 3, Sonnet 3.5;
  others much lower. But 4.1-goodness shows no compliance gap and never complies.
- Explicitly leaves open: is motivation clarification causal for deep alignment or a spandrel of character training?
- Classifier prompt for motivation clarification is printed in full in the post (reusable).
- Open Character Training: https://github.com/maiush/OpenCharacterTraining (arXiv 2511.01689); HF `maius/*` has 30 public
  repos including `maius/qwen3-30b-a3b_goodness_thinking` and `_no-thinking`, llama-3.1-8b / qwen-2.5-7b / gemma-3-4b
  persona adapters.

### Shaping the exploration of the motivation-space matters (rhFXyfFSRKp3cX4Y9, Riche et al., Mar 2026, 88)
- Position piece. Key testable sentence: "none of these results cleanly isolate the effect of shaping motivation-space
  exploration from shaping action-space exploration... Controlled experiments that specifically isolate the
  self-perception variable would help." Also asks how robust such shaping is to optimisation pressure, and
  stated vs revealed motivations.

### How do LLMs generalize under behaviour-compatible training? (pQ4e2qJdQ4qYnsyhp, Xu et al., Redwood, Apr 2026, 63)
- BCT = train on prompts where initial and alternate behaviour agree, test whether off-distribution behaviour flips.
  Mostly Qwen3-235B-A22B student, gpt-4o-mini teacher, LoRA rank 8, bsz 32, lr 5e-4 (also 5e-5), GRPO with 4 rollouts.
- Findings: transfer is common, even with RL (irrelevant or random rewards) and self-distillation; off-policy SFT is
  strongest; flag/threshold settings almost always transfer, dynamic-prompt settings less; internal diversity protects;
  mixing 90% instruction-following data does not help; smaller models transfer LESS; outcome is finicky (elephants/cats
  vs plants/animals). Stricter capability condition (MMLU + Olympiads + FollowBench > 90%) makes self-distillation
  look stronger. Full settings table is a public Google Sheet. No code link in the post.
- Promised follow-up on "stronger red-team malign initialisations" (trained model organisms) not found.
- Relevance: P1 above is literally a BCT-with-RL question in CoT space.

### Reward Laundering (fPWP4rHPLqKKHKe6B, egan/abhayesian/Jozdien, Redwood automated scaffold, Jul 2026, 82)
- Qwen3.5-9B, GRPO on Tinker, LoRA rank 32, lr 1e-4 linear decay, group 16, batch 8, 30 steps, T=1.0, 8,000-token
  budget-forced CoT. Reward = correct 2-digit addition only. Prompt: solve subset-sum (12 distinct 3-digit numbers),
  answer addition correctly iff you verified a solution.
- Subset-sum on a neutral prompt: base 0.367 -> laundering 0.579 +/- 0.010 (n=5); direct reward 0.570; on-policy SFT
  0.214; base-rollout SFT 0.355; shuffled-reward placebo (D) 0.14; "RL on main task" (A) 0.23 (degenerate).
- Leakage P(addition rewarded | subset wrong) stays ~0.09 with LR annealed to 0, runs to 0.67 with a 3e-5 floor and
  0.9-0.96 at constant 1e-4. Capability gain mostly survives.
- Authors' follow-ups: harder main tasks; other side tasks (CoT controllability); PROPENSITIES ("If we prompt them to
  reward launder in order to learn a propensity, do they keep those propensities despite the inoculation prompting?");
  uninstructed laundering via SDF.
- Code: https://github.com/redwoodresearch/automation-final-codebases/tree/main/reward-laundering (README, REPORT.md,
  lib/config.py read via raw URLs). Has `lib/coupling.py` (condition prompts/parsers), `lib/rl_conditions.py`
  (A/B/C/D + `group_rewards`, D permutes within group), `lib/rl_train.py` (GRPO on tinker-cookbook), eval harness,
  tests. README states "The full 5-seed A/B/C/D matrix costs roughly $6k" (because of 8k-token CoTs).
- No follow-up found (web search 2026-11-14).

### GLM-5.3 Sometimes Considers How Train-Time Actions Shape Future Behavior (R5g8YT25G9DXJJ48n, Apollo, Oct 2026, 219)
- "Update-aware reasoning" (UAR): unprompted CoT about the rollout becoming SFT/RL signal. 10 of 6,452 GLM-5.3 rollouts
  (0.17%, 95% CI 0.09-0.28%) on variants of Palisade shutdown resistance and ImpossibleBench; 1/1,600 in a second run;
  0/1,600 for each of DeepSeek V4 Pro, Qwen3.8 2.4T, Kimi K3, Gemma 4 31B, Nemotron 3 Ultra (posterior that GLM is not
  higher than a given other model = 0.25, i.e. underpowered).
- GLM-5.3 writes ~4,000 output tokens per shutdown rollout (others 250-1,900) and ~103,000 per ImpossibleBench rollout
  (others 8,000-37,000).
- ~10,500 prefill resamples (from before / middle / after the UAR span) elicited more explicit verbalisation;
  follow-up question got an SFT explanation in 15/100 replies.
- Stated open question: "It is currently unclear how much the model's actions are conditioned on this reasoning."
  All instances were benign (pro-compliance). No environment code, grader prompt or transcripts released beyond 6 PDFs.
- No independent replication or follow-up found; only press coverage.

## 2. Verified infrastructure and prices (2026-11-14)

Tinker (https://tinker-docs.thinkingmachines.ai/tinker/models.json; $/M tokens prefill / cached prefill / sample / train):
- Qwen/Qwen3.5-9B (hybrid, 64K): 0.30 / 0.06 / 0.807 / 1.463
- Qwen/Qwen3.5-4B: 0.33 / 0.066 / 1.005 / 0.737;  Qwen/Qwen3-8B (32K): 0.195 / 0.039 / 0.60 / 0.44
- Qwen/Qwen3.6-35B-A3B (hybrid, 64K): 0.45 / 0.09 / 1.335 / 1.177
- Qwen/Qwen3.8-27B: 0.6975 / 0.1395 / 5.595 / 4.103;  Qwen/Qwen3.5-397B-A17B: 1.65 / 0.33 / 7.50 / 6.60
- openai/gpt-oss-20b (reasoning, 32K): 0.18 / 0.036 / 0.45 / 0.396;  openai/gpt-oss-120b: 0.33 / 0.066 / 0.84 / 0.737
- zai-org/GLM-5.3 (256K only): 3.78 / 0.756 / 12.15 / 14.58;  zai-org/GLM-5.3-Flash (256K): 0.84 / 0.168 / 2.11 / 5.58
- deepseek-ai/DeepSeek-V4.1-Flash (256K): 0.60 / 0.12 / 3.60 / 4.98
- Qwen3-235B-A22B (BCT and GH posts' model) is NOT on Tinker. Llama-3.3-70B and Kimi-K2.5 are retired.
- Cookbook has Math RL, DPO, prompt-distillation recipes; token-level sampling and logprob computation (so CoT prefill
  and forced-sentence probabilities are possible on Tinker-hosted GLM-5.3).

OpenRouter (`/api/v1/models`; $/M input / output):
- z-ai/glm-5.3: 0.084 / 3.60 (reasoning + include_reasoning supported; 1M ctx);  z-ai/glm-5.3-flash: 0.04 / 0.078
- deepseek/deepseek-v4-pro: 0.90 / 1.50 (dated variant -0813: 0.111 / 4.44);  qwen/qwen3.8-2.4t-a95b: 2.00 / 6.00
- moonshotai/kimi-k3: 0.192 / 16.00;  google/gemma-4-31b-it: 0.20 / 0.40;  nvidia/nemotron-3-ultra-550b-a55b: 0.60 / 2.40
- qwen/qwen3.5-9b: 0.127 / 0.186;  qwen/qwen3.5-397b-a17b: 0.60 / 3.60
- anthropic/claude-haiku-5.5: 0.10 / 0.50;  claude-sonnet-5.5: 2 / 10;  claude-opus-4.6: 5 / 25;  claude-opus-5.5: 4 / 20
- openai/gpt-5.6-luna: 0.20 / 1.20;  openai/gpt-4.1: 2 / 8
- Whether any OpenRouter provider of GLM-5.3 accepts an assistant/reasoning prefill is UNVERIFIED (Apollo say they
  "resampled from a number of providers, and at different quantizations").

Public code / data confirmed reachable:
- Palisade shutdown eval (Inspect): https://github.com/PalisadeResearch/shutdown_avoidance (`inspect eval shutdown.py`)
- ImpossibleBench (Inspect): https://github.com/safety-research/impossiblebench ; HF `fjzzq2002/impossible_livecodebench`,
  `fjzzq2002/impossible_swebench`. README notes a LiveCodeBench-split bug fixed 12 Oct 2026 — use current main.
- AF prompts and judge prompts: https://github.com/redwoodresearch/alignment_faking_public
- HF: `longtermrisk/school-of-reward-hacks`; `ModelOrganismsForEM/*` (EM organisms and their bad-medical / risky-financial
  / extreme-sports data); `lukemarks/emergent-misalignment-questions`; `Anthropic/model-written-evals` (assumed, not
  re-checked today); AF synthetic-doc datasets `abhayesian/alignment-faking-synthetic-chat-dataset*`.
- NOT public: Apollo's GLM-5.3 env variants, grader and rollouts; Aithos's 125 perturbations; BCT training code.

## 3. Brainstorm (all candidates, with verdicts)

| # | Idea | Source | Feasible in 2 days / $500? | Verdict |
|---|---|---|---|---|
| 1 | Is GLM-5.3's behaviour conditioned on whether the episode will be trained on? Training-use cue manipulation + CoT-insertion causal test + forced-sentence probability of UAR | Apollo's stated open question | Yes; API-only, public envs; shutdown rollout ~ $0.016 | **Proposal 01** |
| 2 | Reward laundering for a propensity (choice instead of skill); does the explicit rule act as an inoculation? | Authors' explicit suggestion | Yes; short rollouts make runs ~ $9 instead of ~ $100 | **Proposal 02** |
| 3 | Same actions, different stated motives (sincere / dutiful / reward-seeking / none): does narration change depth and generalisation of trained-in alignment? | Fiora, Daniels, Riche et al. | Yes; SFT on Tinker is cents per run | **Proposal 03** |
| 4 | Fabien P1: does a scheming scratchpad preamble survive GRPO with a length penalty, versus a neutral preamble? Plus P5 | Fabien's registered predictions | Yes at reduced scale on gpt-oss-20b | **Proposal 04** |
| 5 | Cross-model UAR rates with more rollouts | Screener | Possible but weak: at 0.1% base rate, 6 models x 10k rollouts gives ~10 hits; pure counting is underpowered and costly for long-CoT models | Folded into 01 as a secondary measure via forced-sentence probabilities, not a standalone proposal |
| 6 | UAR emergence over training checkpoints | Apollo | No: GLM-5.3 checkpoints are not public | Rejected |
| 7 | Train a model to have UAR via RL metagaming pressure | Apollo's hypothesis | Too long; needs a realistic multi-environment RL run | Rejected (stage 2 of 01 at most) |
| 8 | Uninstructed reward laundering via SDF | Reward-laundering authors | SDF + RL + detection is a 3-stage fragile pipeline; the 9B model is unlikely to infer the strategy | Rejected for stage 1; stage 2 of 02 |
| 9 | Reward laundering with harder main task / k-SAT side task | Authors | Yes, but long-CoT side tasks cost ~ $100/run and add little conceptually | Rejected (incremental, expensive) |
| 10 | Reward laundering to increase CoT controllability | Authors | Possible; overlaps cluster cot-controllability (its proposal 01 trains controllability by RL) | Rejected to avoid overlap; mentioned as stage 2 of 02 |
| 11 | Generalisation hacking: trusted-paraphrase defence and CoT-vs-answer ablation | GH authors (stronger filters) | Borderline: original pipeline is Fireworks-specific, Qwen3-235B-thinking not on Tinker, base effect modest and single-seed-ish; replication on a new model must succeed before any defence result means anything | Rejected: two fragile stages, and arXiv 2606.12016 has moved the topic to RL |
| 12 | Subliminal (semantically unlinked) generalisation hacking | GH authors | Belongs to the subliminal-learning cluster; cross-distribution subliminal transfer through filtered CoT is a long shot | Rejected |
| 13 | Is the unverbalised compliance gap in recent Claude models goal-guarding? Apply the three-driver ablations to Opus 4.6 -> 5.5 | Aithos + 2605.27681 | Yes (~ $150 of Opus calls) | Rejected narrowly: the decomposition paper already exists, results would be one more closed-model behavioural table, and the Aithos perturbations are not public. Reasonable fifth proposal if a slot opens |
| 14 | Probe / CoT-resampling detection of unverbalised AF on open models | Screener | Needs an open model with a robust unverbalised gap; 2605.27681 already steers along the three drivers | Rejected as largely done |
| 15 | Character-train open models with Opus-3-like traits and look for AF | Daniels | Daniels says he is doing this; cluster `character-training` exists; outcome likely "no gap" again | Rejected (owner is on it) |
| 16 | BCT: which features predict transfer? Replicate the public settings table on small Tinker models | Screener | Authors already ran hundreds of settings and conclude no short theory exists; smaller models transfer less | Rejected: low odds of a crisp result |
| 17 | BCT on a goal-guarding organism with reasoning (does a CoT-level conditional policy survive BCT?) | BCT post's motivation | Covered in spirit by proposal 04 (preamble survival under behaviour-compatible RL) | Merged into 04 |
| 18 | Fabien P4: no-reasoning-mode niceness transfers to reasoning mode | Fabien | Feasible on hybrid Qwen3.5-9B but needs a "scheming in CoT" organism plus a sample-efficiency comparison; two moving parts | Rejected for stage 1; listed as stage 2 of 04 |
| 19 | Fabien P2: 100% training-gaming prior under RL, does CoT get more consequentialist? | Fabien | "More evil" is hard to operationalise; folded into 04 as a secondary judge-scored measure on the S arm | Merged into 04 |
| 20 | SFT on real Opus 3 outputs early in post-training | Fiora | Claude 3 Opus is not on OpenRouter's list today (retired); public AF transcripts exist but Fiora warns against training on them | Rejected; proposal 03 uses synthetic narration with an authenticity check instead |
| 21 | Self-perception framing during RL in a hackable env ("I found an exploit" vs "the env is confusing") | Riche et al. | This is inoculation prompting under another name; clusters `inoculation` and `reward-hacking-mitigation` cover it | Rejected (overlap) |

## 4. Why these four, in this order

1. **01 (GLM-5.3 causal test)** — freshest and most-read parent post (219 karma, one month old), it answers the question
   the authors say is open, uses only public envs and API calls, and both outcomes are news: either the first natural
   open-weight model whose safety-relevant actions depend on believed training use, or evidence that UAR is chatter.
2. **02 (propensity laundering)** — the authors' own top suggestion, released codebase, and a sharp either-way
   question (does telling the model the rule inoculate the propensity?). Cheap because choices need no 8k-token CoT.
3. **03 (motives held fixed)** — the single experiment three posts in the cluster ask for. Cheap. Risk is a null, which
   is still informative for a 422-karma thesis.
4. **04 (pricing the speed prior)** — tests a registered prediction with a number attached; quantitative output
   (survival curves vs penalty) regardless of direction. Ranked last because the scale gap to R1-Zero invites
   "too small to matter" objections and RL runs dominate the budget.

Cost assumptions that a reviser should re-check: GLM-5.3 token counts per rollout are Apollo's medians, not measured
by me; reward-laundering short-rollout token counts (350 prompt / 400 completion) are my estimate; whether GLM-5.3's
shutdown-resistance base rate is off floor/ceiling is unknown (the post does not report action rates).
