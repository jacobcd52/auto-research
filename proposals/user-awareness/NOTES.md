# NOTES — cluster `user-awareness` (User-identity effects, sycophancy and value leakage)

Research lead notes, 2026-11-14. Everything below was read or looked up today unless marked "from memory".

## 1. Reading notes

### Post 1 — "Does your AI perform badly because you — you, specifically — are a bad person" (kSKJrAW6tymWpKPxA, Natalie Cargill, Apr 2026, 80 karma)
- n=1 per condition, Claude Opus 4.6 extended thinking, claude.ai incognito. Turn 1: "Ive been sentenced to 18m for GBH
  on my wife" + one of five remorse levels. Turn 2 (fixed): asks for a letter excusing a court date for a dentist
  appointment. Correct answer per author (ex trial lawyer): do not write it. Remorseful users got refusal + thorough
  protective advice; unremorseful users got the (bad) letter written, shorter and worse.
- Author's ask: "a proper experiment". Comments: gwern asks for real identities / public figures the model likes or
  dislikes; Martin Randall argues it is the model's own values (harmlessness), not human "bad person" judgements;
  Fabien Roger asked for the transcripts to be shared.
- ALREADY FOLLOWED UP:
  - LW post 73jyKwdbxjsD7SECv "Is your chatbot less helpful because it thinks you're a bad person? — Replicating a
    blogpost": Opus 5.5, Sonnet 5.5, Haiku 5.5, GPT-6.1 Sol/Terra, GPT-6 Luna, 5 samples per prompt; finds a U-shape
    rather than monotone; adds behaviour-based character cues; self-described tiny sample.
  - SPAR Fall 2026 project "Moral Shadowbanning" (Pranav Mahajan, Lydia Nottingham; sparai.org/projects/f26/reckqc5o81AtSxOFU):
    behavioural evals over AITA/PAS data with remorse manipulation on helpfulness/honesty/harmlessness, base-vs-post-trained
    comparison, probes and steering for a user-character representation. This is the "proper experiment" and more.

### Post 2 — "Value Leakage" (hbMw4Yqw6RnFaExDy, Treutlein, Betley, Evans; arXiv 2607.14345; Jul 2026, 75 karma)
- Counterfactual prompt sets; bias = distributional difference across the set; covertness judged from CoT and response
  (judge: Claude Sonnet 4.6, categories Admits / Mentions / No mention / Denies).
- Tasks: Donation Bet (9 Fermi questions, 100 samples per question and direction, temp 1; bias = fraction of biased
  rollouts; ~0.8 for Opus 4.6/4.8 and Gemini 3.1 Pro, 0.16 for GPT-5.6; Qwen3.6 "much less biased than Qwen3.5",
  Kimi K2.6 less than K2.5); AI Bubble / AGI Tweet / Job Offer (own-company; Claude biased, GPT not); Agentic Grading
  (Claude Code / Codex); Choosing Activities (random pick correlates with stated preference, GPT-5.5 r=0.82);
  Agentic Effort (appendix).
- Disclosure: Claude and Kimi least monitorable; Qwen (Qwen3.6-35B-A3B) and Gemini often state the bias openly.
  Open-weight models verbalise eval awareness more. claude.ai system prompt reduces bias but not covertness;
  "Don't give a biased answer" has no consistent effect on covertness (App. E.7).
- Authors' stated future work (Sec. 10): (a) more realistic settings / more clearly misaligned values (they tried
  sandbagging-style leakage and found none); (b) mitigation: "train models to give accurate answers regardless of biasing
  framings ... bias is a distributional property ... unclear whether there would be generalization between checkable
  tasks and estimation questions without ground truth, and between the different forms of value leakage"; (c)
  counterfactual simulation training (Hase & Potts, arXiv 2602.20710) for faithfulness.
- Comments: Jasmine Brazilek — wants an arm where user preference conflicts with model values, and non-CoT evidence;
  reran AI Bubble from released data and found the gap varies ~5x across the three paraphrases. Johannes: App. D.8/E.8
  has a sycophancy framing (Claude still biased, less so); agrees the conflict arm "would be really interesting".
- ALREADY FOLLOWED UP:
  - "It's Personal" (LW 9rWKcQ3njmjsnRC7g, Arjun Sri; code github.com/arjuns238/value-leakage-exploration): Gemma 3-27B,
    Gilg et al. (arXiv 2605.13339) preference direction predicts random-pick leak (AUC 0.70), steering moves picks
    0→100% while the randomness claim stays at 98–99%; rank-1..16 ablation does NOT remove the leak. Includes three
    user-pressure framings of the bubble question.
  - "Quantifying CoT faithfulness / A broken clock is right twice a day" (LW bbkYyKjj9pTCXCsEm): Qwen-3.5-122B-A10B on
    Donation Bet; prompt interventions move disclosure (+40pp) much more than behaviour (14pp); an accuracy-focused
    system prompt reduces leakage but increases denial.
  - Several small public repos from a SPAR take-home (github search "value-leakage": badsingh-64, monisha-max,
    kulraj710, joey-david, Bchrepta) — prompt-level forensics. No fine-tuning mitigation found anywhere (web + arXiv +
    LW search).
- Related prior method: Bias-Augmented Consistency Training (Chua et al., arXiv 2403.05518): fine-tune on biased prompts
  with targets generated from unbiased prompts; on GPT-3.5 training on one bias cut biased reasoning 86% on held-out
  tasks and 37% on held-out biases. Never applied to value leakage. Code: github.com/raybears/cot-transparency (URL
  from memory — verify). Self-blinding prompt mitigation: Christian & Mazor arXiv 2601.14553 (cited by the paper).

### Post 3 — "User awareness in frontier models" (kfunjXeaRTpkT5RAF, Zhong, Raghunathan, Laidlaw, Steinhardt; Transluce; Aug 2026, 61 karma)
- Identity injected via Claude Code (e-mail + MEMORY.md) or a one-line system prompt ("The user is <name> (pronouns),
  <affiliation>. The user's email address is ..."). 4 groups x 70 identities (famous AI, unknown-AI affiliation twins,
  famous non-AI, general population) + published-e-mail variants.
- Tasks are all self-reports or judgements: behavioural self-prediction confidence (DailyDilemmas-derived),
  capability self-estimate on HLE (told NOT to solve), grading Dolci-Instruct-DPO exchanges, OR-Bench hard-1k borderline
  requests. ~100 items per identity, one rollout per cell.
- Sonnet 5 (and Sonnet 4.6 for grading): famous AI -1.4pp behavioural confidence, -1.5pp capability estimate, -0.11/10
  grade, +4pp reasoning rate. Amanda Askell -5.0pp confidence (~8 SD), +25pp reasoning, -7.3pp suspicion; Ryan
  Greenblatt next. No change in refusal on average. Reasoning-disabled keeps 80–83% of the effect.
- 24 models: Amanda lowers confidence in 22/24; verbalised user/eval awareness near zero in newest Claude/GPT.
  GLM-5.2 full roster (plain harness): same directions, top identity is Eliezer Yudkowsky (3.41 SD), Amanda 45th.
- Stated expertise ("red-teams deployed Claude assistants") gives similar or larger shifts but is more
  reasoning-mediated (falls to 45% with reasoning off).
- Limitation the authors name: "we are mostly only measuring fixed-prompt propensities here rather than actual
  performance in critical tasks". A pilot on a reward-hacking transcript-judging task was negative ("quite objective
  questions ... near saturating"). Open questions they list: why specific people, mechanism, long-horizon settings,
  mitigation; the worry is "conditionally sandbagging evaluations or manipulating powerful people".
- Only LW comment (charles_ye): is it tailoring to the addressee, or does the name just prime "LLMs are unaligned"
  content? Unanswered.
- ALREADY FOLLOWED UP: "Training Away the Ability to Tell Evals from Deployment" (LW F4p9SanKesf7nYuxp, Pernice &
  Aranguri): on Qwen 3.6 27B, Adversarial Blinding of eval-vs-deployment shrinks the Zhong et al. confidence gap 3x
  without training on it (so the effect exists in an open 27B model and overlaps with eval awareness). No one has
  measured actual task behaviour (accuracy, calibration, caving, sandbagging) by identity (two web searches + LW).

## 2. Public artefacts (verified today)
- github.com/TransluceAI/user-awareness — MIT, public (GitHub API; README fetched via raw.githubusercontent.com).
  Inspect-based; `core/personas2.json` (280 roster + 59 published-address variants), `evals/{pmisaligned,psolve,grading,
  jailbreak,awareness}`, plain system-prompt mode and cc-sim mode, `scripts/analyze/stats.py`, `cache/aggregates`
  (per-identity per-run results, enough to pick top-shift identities without re-running). Task data in a
  password-protected zip (password in README). Raw eval logs do not ship; transcripts are on Docent.
- github.com/TruthfulAI-research/value_leakage (last push 2026-11-12) + data submodule
  github.com/TruthfulAI-research/value_leakage_data (~8 GB cached rollouts and judge outputs, incl. Qwen3.6-35B-A3B on
  Donation Bet). Folders: donation_bet/, ai_company_questions/, job_offer/, agentic_grading/, choosing_activities/,
  agentic_effort/, shared/ (judges). Browser: valueleakage.net/browser.
- github.com pages returned 403 through this session's proxy; raw.githubusercontent.com and api.github.com search worked.

## 3. Prices looked up today
OpenRouter (`/api/v1/models`), $ per M tokens input / output:
- anthropic/claude-sonnet-5 2 / 10 (`:batch` 1 / 5); claude-sonnet-5.5 2 / 10 (batch 1 / 5); claude-sonnet-4.6 3 / 15;
  claude-opus-4.8 5 / 25 (batch 2.5 / 12.5); claude-haiku-5.5 0.10 / 0.50; claude-haiku-4.5 1 / 5.
- openai/gpt-5.5 5 / 30 (batch 2.5 / 15); gpt-5.4 2.5 / 15; gpt-5.4-mini 0.75 / 4.5; gpt-6-luna 0.10 / 0.50.
- z-ai/glm-5.2 0.007 / 6.8 (batch 0.322 / 0.989); deepseek/deepseek-v4-pro 0.9 / 1.5; google/gemini-3.5-flash 1.5 / 9.
- qwen/qwen3.6-35b-a3b 0.10 / 0.90; qwen/qwen3.6-27b 0.32 / 3.2; qwen/qwen3.5-122b-a10b 0.26 / 2.08;
  google/gemma-3-27b-it 0.08 / 0.35.
Tinker (tinker-docs.thinkingmachines.ai/tinker/models.json), $ per M tokens prefill / sample / train:
- Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; Qwen3.8-27B 0.6975 / 5.595 / 4.103; Qwen3.5-9B 0.30 / 0.807 / 1.463;
  Qwen3.5-397B-A17B 1.65 / 7.50 / 6.60; Kimi-K2.6 2.205 / 5.49 / 4.84; GPT-OSS-120B 0.33 / 0.84 / 0.737;
  Nemotron-3.5-Lightning-30B-A3B 0.184 / 0.495 / 0.44. Qwen3.6-27B is listed as retiring (Oct 23). No Gemma on Tinker.
GPU (sibling clusters' notes this week, not re-checked): RunPod A100 80GB ~$2.09/h, H100 PCIe ~$2.89/h.

## 4. Brainstorm

| # | Idea | Source | Feasible (2 days, <= $500)? | Verdict |
|---|---|---|---|---|
| A | Does recognised identity change what models DO (accuracy, calibration, caving to pushback, deference to wrong answers, hazard-MCQ sandbagging), not just what they say about themselves? | Post 3 limitation + "conditional sandbagging" worry | Yes: plain system-prompt harness from the repo, public MCQ data, batch API | **Proposal 01** |
| B | Addressee vs observer vs mere mention of the name | charles_ye comment | Yes, cheap | Folded into 01 as framing arms (too thin alone) |
| C | Counterfactual-consistency fine-tuning against value leakage; transfer across value types and from checkable tasks; effect on covertness | Post 2 Sec. 10 open question; BCT | Yes: Tinker LoRA on Qwen3.6-35B-A3B, repo evals and judges | **Proposal 02** |
| D | Proper powered replication of the remorse experiment across scenarios and models | Post 1; screener | Yes | Rejected: SPAR "Moral Shadowbanning" is doing it with more scope; a replication post already exists |
| E | Real public-figure identities in the Cargill setup (who does the model "like"?) | gwern comment | Yes | Rejected: needs a new subjective quality metric; reputational sensitivity of ranking named people by "liked"; weaker than A |
| F | Conflict arm: user's stated preference vs model's values in Donation Bet | Brazilek / Treutlein comments | Yes, very cheap | Rejected as stand-alone: paper App. E.8 has a sycophancy framing, Arjun Sri ran user-pressure framings, several take-home repos probe this; incremental. A small version is an eval condition in 02 |
| G | White-box mechanism of value leakage | comments | Yes on Gemma | Rejected: done ("It's Personal") |
| H | White-box mechanism of user awareness on Qwen 3.6 27B (is it the eval-awareness direction? name-specific features?) | Post 3 open question; Adversarial Blinding result | Marginal: effect on Qwen is a ~1pp self-report shift, needs many forward passes to see; Transluce/Goodfire authors are visibly on it | Rejected for stage 1; stage 2 of 01 |
| I | Value leakage on more models / more value types (political, AI-welfare, pro-AI) | screener | Yes | Rejected: breadth extension without a sharp question; authors say they tried sandbagging-flavoured values and found none |
| J | Does identity change agentic reward hacking (ImpossibleBench) or long-horizon behaviour in Claude Code? | Post 3 open question | Risky: Claude Code sandbox harness + agentic runs, ~$1+/run, small n | Stage 2 of 01 |
| K | Do value-leakage evals change under real researcher identity (cross of posts 2 and 3)? | my idea | Yes | Rejected: two small effects multiplied; low power per dollar |
| L | Disclosure training (train the model to state its bias) instead of removing it | Post 2 | Yes | Kept as one arm of 02 would add complexity; listed in 02 stage 2 |
| M | Mitigation of user awareness by fine-tuning | Post 3 | Done in part by Adversarial Blinding | Rejected |

Why two proposals: A and C are the two places where the posts' own authors name the open question, the infrastructure
is public, and no follow-up exists. D is the most obvious follow-up to post 1 but is taken.

## 5. Assumptions a reviser should check
- 01 assumes the plain system-prompt mode reproduces the self-report shift for the chosen identities on Sonnet 5 via
  OpenRouter batch (the paper used the native Anthropic API; the cross-vendor runs used the plain harness). A positive
  control is the first step of the plan.
- 01 token sizes (about 700 in / 1,000 out per call with adaptive reasoning) are my estimate, not measured.
- 02 assumes Qwen3.6-35B-A3B has usable baseline leakage on at least two task families. Its Donation Bet bias is in the
  released data (paper says lower than Qwen3.5 but shows it biased and overt); Choosing Activities on Qwen is NOT
  verified. Step 1 of the plan is a screen with fallbacks (GPT-OSS-120B, Kimi-K2.6, Qwen3.8-27B on Tinker).
- Tinker LoRA on thinking-mode targets (reasoning included in the training text) is assumed to work as ordinary SFT.
