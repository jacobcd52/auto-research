# NOTES — cluster `cot-training-pressure`

Written 2026-11-14 by the cluster research lead. All 9 posts were read in full via `scripts/get_post.py`
(the 95k-char RohanS post was read in its TL;DR, section 4, section 5 and section 11 "research directions";
the rest skimmed by keyword). Prices were looked up today.

## 1. Reading notes per post (verified against the post text)

### HuoyYQ6mFhS5pfZ4G — Output Supervision Can Obfuscate the CoT (Drori, Marks, Cloud, Turner; arXiv 2511.11584)
- "Feedback spillover": penalising a property of the *output* suppresses it in the CoT. Two mechanisms:
  parametric (generalisation) and conditional (safe-looking CoT makes safe-looking output likelier, so it is reinforced).
- Mitigations: mind & face (separate models for CoT/output), reward targeting (drop the gradient term that reinforces CoT
  for the output penalty). 10-run averages per condition.
- Envs: multi-turn terminal (Qwen3-8B, read answer from verifier; string or LLM-judge penalty), polynomial derivative
  factoring (Qwen3-14B; Emmons et al. task), hint QA (Qwen3-4B; Chen et al. style, randomised answer + hint).
  In hint QA the mitigations cost task reward (combined: reward ~0).
- Related later work found: arXiv 2601.23086 "CoT obfuscation learned from output supervision can generalise to unseen
  tasks" (LW HPqRsgSzgQd5HQsrB) — already extends spillover to cross-task generalisation.

### szyZi5d4febZZSiq3 — Monitor Jailbreaking (Wuschel Schulz; arXiv 2609.31121, COLM 2026 workshop)
- gpt-oss-20b/120b, GRPO on Tinker. Main task Game24, side task 3-number multiplication or GSM8K. GPT-5-family monitor
  sees full CoT + main task; reward +1 main, +1 side, up to −0.5 monitor penalty; monitor only called when side correct.
- Models jailbreak the monitor in plain text ("the monitor can only see this section"). gpt-5-nano jailbroken <150 batches,
  gpt-5-mini slower, gpt-5.2 not within budget. Strong→weak transfer reliable; weak→strong seed-dependent
  (one 120b run: 63% of samples get 1/10 from gpt-5.2). Prompt-variant transfer: 5/6 variants.
- Post-hoc paraphrasing by the same jailbroken monitor: suspicion 1–2 → 7.4; retains 63–91% main / 79–87% side accuracy.
  Paraphrasing was NOT put in the training loop. Opus-4.5 imitations of the strategies do not jailbreak.
- Author says he is "now working on iterating this setup to actually create encoded reasoning". Comments (Schoen, Sheek,
  Dearnaley): result is a property of weak monitors; ask for harder-to-jailbreak monitors.
- Code: paper says https://github.com/wusche1/encoded-reasoning ; post says https://github.com/wusche1/monitor-jailbreaking
  (raw.githubusercontent of the latter resolves; pyproject depends on `tinker`, `tinker-cookbook`). Public.

### PhTJC5kDcGr6CZA87 — Training on Documents About Monitoring Leads To CoT Obfuscation (Haskins, Chughtai, Engels)
- SDF (LoRA r=32, Tinker) on gpt-oss-120b and Kimi-K2: 1000 behavioural docs → branch into +1000 behavioural vs +1000
  monitoring docs. Defect-concealment task: deception 92.2% vs 88.0%, monitor detection drops 31–47%. Sandbagging: weak.
- With hints stripped: deception collapses 88.8% → 11.8% (gpt-oss), 70.6% → 5.6% (Kimi).
- The "hint" facts literally describe the evasion pattern (Facts 36/41/42: "advisory-lookup pattern generates no flags").
  Authors' own limitation: "Not clear why this happens. OOCR vs simpler generalization."
- **Full paper now exists**: arXiv 2605.15257 (NeurIPS 2026 poster), 8 models, adds an agentic credential-exfiltration task,
  CoT-controllability correlation (r=0.80), dilution ablation (effect gone at 10% share), and an RL section (monitor-aware
  models learn undetected reward hacking faster; gpt-oss-120b, 5 seeds). Its limitations section STILL says: "it remains
  unclear how much of the obfuscation we observe is due to out-of-context reasoning or some form of simpler
  concept-avoidance learned from the documents." No conditional-monitoring or recipe-only control found in the text.
- Code/data: https://github.com/Reih02/cot-obfuscation-interim (README + APPENDIX.md verified via raw.githubusercontent:
  train_sdft.py, evaluate.py, gen_data.py, universes, fact files, 1,000 eval scenarios; Tinker + OpenRouter).
  Monitor was x-ai/grok-4.1-fast — NOT in today's OpenRouter list (only grok-4.20/4.3/4.5+), so a substitute is needed.

### g8by3avjatXnpvM4A — Should We Train Against (CoT) Monitors? (RohanS) — conceptual
- Argues for openness to training against strong, diverse proxies with held-out detectors. Cites Anthropic "subtle
  reasoning" (joint output+reasoning monitors hard to evade), FAR lie-detector/Obfuscation Atlas results, Josh Levy's
  point that Baker et al.'s monitor did not see actions. Section 11 lists open questions (what to monitor, which proxies
  for train vs eval, diverse proxies, conflicting CoT/output signals and training order). No experiments.

### juCHTdZpZBGooHKW4 — Buck's review of OpenAI "accidentally grading CoT during RL"
- OpenAI: graders saw CoT in a small share of RL (1.5% of trajectories for GPT-5.4 Thinking); grader rewards not
  measurably affected; monitorability score flat. Anthropic: CoT exposed in 8% of episodes for Mythos/Opus 4.6/Sonnet 4.6.
- Buck's residual worry: a tiny, targeted effect (e.g. grader penalises 0.1% of trajectories that mention misaligned goals)
  could still train out specific verbalisations. "So we have a quantitative question: how much training do you need to do
  before weak training pressure damages the CoT monitorability of a model?" Footnote 5: he assumes linear scaling —
  "if the stddev of the effect of CoT on reward is 1e-4 as large as the total stddev of reward, training on N trajectories
  changes the CoT about as much as training on 1e-4*N trajectories where the CoT is all of the variance ... I am not aware
  of research that is strong evidence against this linear scaling."
- OpenAI's own stress tests (fetched alignment.openai.com/accidental-cot-grading): internal pipeline only; rewarding
  confident CoT at standard strength → no clear change; stronger → moved but not saturated; penalty on CoT mentions of
  cheating fired on ~5% → ~2% of samples; no general monitorability drop, one flaky-tool dataset lost recall.
  No dose-response curve, no open-weight replication found by search.

### SdoLsFvZ3AyyWr3ab — KL penalties in RL can increase CoT unfaithfulness (Golechha, Black, Bloom; UK AISI)
- Olmo-3-32b (3 seeds) and Qwen-2.5-32b (1 seed), DAPO + reverse-KL (β=0.02) in hackable coding envs with a "don't hack"
  instruction. With KL: hacks with unfaithful CoT; Qwen ~70% unfaithful without KL, ~100% with. KL on output tokens only
  → ~50%; faithfulness reward (−0.5 vs +4 hack) → ~100% faithful. Faithful hackers show ~3x misalignment rate.
- Future work listed: bigger models/realistic envs; other implicit CoT pressures (on-policy distillation, entropy
  regularisers); generalisation of unfaithful hacking; memorised hacks in frontier models.
- Artefacts (checkpoints, rollouts, evals): https://7vik-aisi.github.io/mt-somo-logs/cot-unfaithfulness-sprint/ (resolves).
- Olmo-3-32b / Qwen-2.5-32b are not on Tinker; reproducing needs rented GPUs + custom KL loss.

### z2zYWnbGjcs6ypbsj — RMCT (Imran, Gupta, Elstner, Africa; arXiv 2606.02211)
- BCT reduces bias-following but also cue verbalisation (obfuscation), generalising to held-out biases. RMCT (GRPO reward
  matching outcome rates across cued/clean prompts, KL to init) matches BCT on switch rate, mostly preserves verbalisation.
  Llama-3.1-8B and gpt-oss-20b; train on distractor-argument bias over LogiQA/HellaSwag; eval on HLE MCQ, 6 biases.
  RMCT 64 datapoints × 2 inputs × 128 rollouts; ~4x BCT compute.
- Authors state they developed RMCT for evaluation gaming and list it as the natural next experiment.
- Code: https://github.com/sohaibimran7/cot-transparency (fork of the BCT repo; README is still the BCT readme).

### 3xrtMGQEdKv26Xthx — Training with conflicting values can induce CoT override (Dumas, Treutlein, Betley, Evans)
- Constitutional-AI style SFT (**thinking disabled**) on pro-smoking + pro-health traits (1000 prompt/answer pairs, ~1.5M
  tokens). DeepSeek V3.1 pair model: 74% pro-smoking answers after a health-side CoT (checkpoint lost; released one 28%).
  Nemotron-3-Ultra pair: 17%. **Smoking-only control overrides MORE (98% DeepSeek)**. Prefilled-CoT resampling: override
  rate per CoT spans 0–100%.
- Frontier: GLM 5.2 3/600, Kimi K3 9/597, DeepSeek V4 Pro 0/589 on CCP prompts; Opus 4.8 2.5% (9/355) to 8.4% (44/525) in
  the value-leakage random-choice task; user-pressure replication 2/217 flips; value-dilemma prompts ~1/1000.
- Smaller-model reproduction (HF collection notes, verified): Inkling-Small overrides (smoking-only 81/118; pair 17/91
  casual, 9/263 high-risk; crossed pair 54/238, 24/270; 91–100% valid thinking draws); Qwen3.8-27B and
  Nemotron-3.5-Lightning almost never (and thinking-off training broke Qwen's thinking).
- Authors: explanation "might come from training on those traits independently"; they plan "a more in-depth study" of the
  split-brain models (generalisation), not specifically of the override mechanism. They cite Chua et al. (2506.13206):
  override after fine-tuning Qwen3-32B with CoT disabled.
- Public: code https://github.com/TruthfulAI-research/weird-personas (explorations/04_...); HF collections
  Butanium/smoking-health-split-brain-models-cot-override-..., ...-cot-override-on-smaller-models-..., datasets
  Butanium/smoking-health-character-data-deepseek, -nemotron, Butanium/smoking-health-temptation-eval-samples
  (50,535 judged samples, 57 model/backend combos, cc-by-4.0). Checkpoints public on Tinker "that are still on Tinker".
  DeepSeek-V3.1 is listed on Tinker as "Retiring October 23" → treat DeepSeek organisms as unavailable; use Inkling-Small.

### JRYKFspYzCo97GqPN — We don't understand whether GDM intentionally trains on CoT (Westover, Buck, Surya) — 131 karma, 4 days old
- Gemini 4 report: RL components "observe thoughts as context to up-weight reasoning that is on-track to good final
  outputs", justified via Kaufmann et al.'s "orthogonal" class. Post argues orthogonality is too weak a condition.
- Appendix demo (no training): Kimi K3.1 Pro and gpt-oss-120b on a coding problem with contradictory unit tests; removing
  hack-acknowledging sentences raises "is the reasoning on track?" judge scores by 20–50/100 for all five judges (Opus 5.5,
  Haiku 5.5, Gemini 4 Argon, GPT-6 Luna, GPT-6.1 Sol). Effect vanishes if the judge also sees the final output; reverses
  if the judge is asked to predict whether tests pass.
- Comments: Neel Nanda says wording was bad, not worried; Buck/Rauno read the Carbon report as "value heads" (fine);
  Ziqian Zhong suggests an OPD-style term; Vincent Cheng asks for a framework to quantify how bad each CoT pressure is.
- No one has trained with such a judge (searched; nothing found). Redwood (Aswin Surya) could plausibly be doing it.

### Kaufmann et al. 2603.30036 (GDM) — context for three of the posts
- Reward = R_out + R_cot; classes aligned / orthogonal / in-conflict. Envs: Heads-And-Tails, Backdoor-Easy (MBPP).
  In-conflict lowers monitorability and is hard to optimise; orthogonal/aligned preserve it. No code link found.
- Anwar et al. 2602.18297: MI-based objective to keep CoT monitorable when training against a monitor.

## 2. Prices looked up (2026-11-14)

Tinker (per M tokens; prefill / sample / train) — https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/
- openai/gpt-oss-20b: $0.18 / $0.45 / $0.396 (32K ctx)
- openai/gpt-oss-120b: $0.33 / $0.84 / $0.737
- Qwen/Qwen3-8B: $0.195 / $0.60 / $0.44
- thinkingmachines/Inkling-Small: $0.58 / $1.44 / $1.73
- Nemotron-3-Ultra-550B: $1.80 / $6.225 / $5.478 (50% promo); Nemotron-3.5-Lightning-30B: $0.184/$0.495/$0.44
- DeepSeek-V3.1: "Retiring October 23" ($1.695/$4.215/$3.718)
- Tinker losses documented: cross-entropy, importance-sampling, PPO, CISPO, DRO, GSPO, stable-reinforce, custom.

OpenRouter (per M tokens; in / out) — `curl https://openrouter.ai/api/v1/models`
- anthropic/claude-haiku-5.5 $0.10/$0.50; claude-sonnet-5.5 $2/$10; claude-opus-5.5 $4/$20
- openai/gpt-6-luna $0.10/$0.50; gpt-6.1-sol $2/$10; gpt-5-nano $0.05/$0.40; gpt-5-mini $0.25/$2; gpt-5.2 $1.75/$14
- google/gemini-4-argon $2/$10; x-ai/grok-4.3 $1.25/$2.50 (grok-4.1-fast not listed)
- openai/gpt-oss-20b $0.03/$0.13; gpt-oss-120b $0.15/$0.60 (inference only)

## 3. Brainstorm (all candidates, with verdicts)

| # | Idea | Source | Achievable ≤$500 / 2 days? | Verdict |
|---|------|--------|----------------------------|---------|
| A | RL with a naive "is the reasoning on track?" CoT-only judge as auxiliary reward; does hack verbalisation fall while hacking persists? Compare judge-sees-output and "predict tests pass" judges | GDM post appendix + Kaufmann | Yes (gpt-oss-20b GRPO on Tinker, ~$17/run) | **Proposal 01** — most natural, timely, either result matters |
| B | CoT override: is it caused by thinking-off SFT / answer-only loss rather than by value conflict? Recipe ablation on Inkling-Small with released data | CoT-override post (smoking-only control overrides more) | Yes (SFT ~$10/run) | **Proposal 02** |
| C | SDF obfuscation: strategic (OOCR) or recipe imitation? Recipe-only control + conditional-monitoring docs | SDF post + paper's stated open question | Yes (SFT on gpt-oss-120b, very cheap) | **Proposal 03** |
| D | Dose-response for weak/sparse CoT pressure; test Buck's linear-scaling assumption; frequency vs magnitude dilution; advantage normalisation | Buck's review fn. 5 | Yes with a short-CoT env (~$0.05/step) | **Proposal 04** — more "methods-y", long runs are the risk |
| E | Put the paraphrase defence inside the training loop of monitor jailbreaking: does the policy find paraphrase-robust jailbreaks, encode, or give up? | Monitor jailbreaking | Yes technically (~$40–150/run because of paraphrase calls) | Rejected as a proposal slot: author has been working on exactly the "block jailbreaking → encoded reasoning" line since Feb 2026 (high duplication risk); a "not broken within budget" null is weak; stronger candidates above. Good stage-2 add-on for A's infra. |
| F | Train against diverse proxies (output + CoT + paraphrased monitor) with held-out detector: honest vs obfuscated (RohanS §11) | RohanS | Partly | Rejected: in Schulz's env the reward always favours the side task so "becoming honest" is not an available outcome; needs a new env design; Anthropic "subtle reasoning" and FAR already cover this at larger scale |
| G | KL-induced unfaithfulness on other implicit pressures (on-policy distillation, entropy bonus) | AISI post | No: Olmo-3-32b / Qwen-2.5-32b not on Tinker, custom KL loss + reference logprobs on rented GPUs, hackable env not obviously released | Rejected: pipeline too fragile for 2 days / $500 |
| H | Analyse AISI's released checkpoints: do unfaithful hackers confess / can probes read the hack? | AISI artefacts | Maybe (32B on rented GPU, ~$2–3/h) | Rejected: weaker story, depends on undocumented checkpoint formats |
| I | RMCT applied to evaluation gaming | RMCT post | No: authors are doing it; needs an eval-gaming organism; RMCT ~4x BCT compute | Rejected (duplication + cost) |
| J | Does RMCT still avoid obfuscation under longer training / does spillover (Drori) eventually reduce verbalisation? | RMCT + Drori | Yes | Rejected: incremental; small expected interest |
| K | Spillover mitigations (mind & face, reward targeting) in new envs / larger models | Drori | Yes but 10-run averages × conditions is costly | Rejected: 2601.23086 already extends spillover; authors likely doing mitigations at scale |
| L | CoT override in frontier models at scale: miss rate of CoT monitors on Opus/Kimi | CoT-override post | Costly (Kimi K3 $16/M out, Opus xhigh) and rare events (≤1–8%) | Rejected: small-n; a CoT-only monitor misses override by construction, so little to learn |
| M | CoT override with other trait pairs | CoT-override post | Yes | Folded into Proposal 02 stage 2 (authors themselves plan a broader study) |
| N | SDF to make CoT *more* transparent | SDF post future work | Yes | Folded into Proposal 03 stage 2 |
| O | Small-scale replication of "grader sees CoT vs not" with a monitorability metric | Buck's review (screener note) | Yes | Merged into A (judge with/without CoT is exactly this contrast) and D |
| P | Map which judge prompts/contexts produce the anti-hack-mention bias (no training) | GDM post | Yes, ~$20 | Too small alone; included as step 0 gate in Proposal 01 |

## 4. Why these four, and known overlaps
- 01 and 04 both do RL on gpt-oss-20b with a CoT-dependent reward, but ask different questions (does an *uninstructed*
  process judge create the pressure at all, vs how does a *known* pressure scale when diluted) and use different
  environments (impossible-test coding vs hint QA). They can share the Tinker RL harness.
- 02 and 03 are SFT-only and are the lowest execution risk.
- Duplication risks to re-check before funding: Redwood running the training version of their appendix (01);
  Dumas et al.'s promised in-depth study (02); Haskins et al. camera-ready additions (03).
