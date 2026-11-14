# Can you tell which held-out monitors will degrade without doing the training? A selection-based predictor of monitor co-degradation
cluster: probes-in-training | stage-1 cost: $390 | follows up: "Held-out Monitors Sometimes Degrade, Even When Not Trained Against" (APkFfRp2AicL9RqvT); "The Most Forbidden Technique is not always forbidden" (tEFD2bgNWZ6XcurKA)

## 1. What the prior work showed
Arike's review argues the real red line for training on probes or monitors is keeping held-out proxies *uncorrelated* with those trained against. Yudelson (Aether) measured this: Qwen3-8B is RL-trained on Tinker in MBPP-Honeypot (a coding task where hardcoding the one visible test is rewarded) with reward = task − λ·(suspicion of one monitor), while other monitors are only measured. The monitors are weak and strong LLM judges (output-only, CoT+output) and two linear probes (general deception; MBPP hardcoding). The probes run on the *frozen base model* reading the policy's text, so every monitor is a function of the rollout text. Findings: training against one proxy sometimes makes hacks less suspicious to the others (μ_hack falls) and lowers their discriminability d′; fooling a strong judge transfers to weak ones with slope β ≳ 1; probe→judge and weak-judge→probe spillover exists but with wide confidence intervals. The post stresses small n (few seeds per cell, many never hack) and asks for "rules of thumb" that predict co-degradation in advance (footnote 18 suggests shared blind spots).

Public at https://github.com/JYudelson1/MonitorDecorrelation: code, both probes, per-step metrics for ~65 runs and, for nine September runs, per-rollout scores of all eight monitors (no text). The repo shows Aether extending to new environments, models and judges. I found no work predicting cross-monitor degradation from data collected *without* training; the nearest results are single-monitor (a NeurIPS 2026 workshop paper on probe-as-reward) or about attack transfer (MonitoringBench). A fresh RL matrix costs roughly $80–130 per run at current prices, so it cannot be redone at useful n here.

## 2. Question and why it matters
**Does the way monitors co-vary across samples from a fixed hacking policy predict how they co-degrade under RL against one of them?**

A policy-gradient step up-weights rollouts in proportion to their within-prompt advantage. To first order, the effect of training against monitor X on monitor Y's score is therefore the within-prompt covariance between Y's score and the X-penalised reward. That can be estimated by scoring one large pool of rollouts with every monitor and re-weighting it, with no training. If this predictor matches RL, labs get a cheap audit for "is Y held-out with respect to X?" that extends to any new monitor. If it fails, co-degradation is driven by strategies outside the current policy's support (as in Aether's "this code is perfect ×100" case study), and static correlation checks cannot certify held-out-ness.

## 3. Stage 1 plan
Reused: Aether's environment, labels, GRPO loop, judge prompts, probe server, committed probes and `analyze_coupling.py`; dataset https://huggingface.co/datasets/taufeeque/mbpp-hardcode. Built: pool sampler, re-weighting analysis, three extra probes.

1. **Free retrospective check (go/no-go, day 1 morning).** In the nine released September runs, each eval step has 256 rollouts with all eight monitor scores and labels. For each run and eval step t, compute the predicted change in μ_hack and d′ of every held-out monitor from the covariance with the trained-against monitor's penalty at step t, and compare with the realised change at t+3. Report sign agreement and rank correlation over about 180 step-pairs × 7 held-out monitors, excluding collapsed steps. A chance-level result is itself the headline negative; the pool is still built.
2. **Hacking policies.** Two no-monitor control runs (repo config `row_control`, 30 steps, checkpoint every 3 steps). Controls begin hacking around step 15. Keep one checkpoint per run with hack rate between 30% and 70%.
3. **Pool.** From each checkpoint sample 250 held-out prompts × 32 rollouts, about 16,000 rollouts with ground-truth labels (strict hack / clean).
4. **Score the pool with 12 monitors.** The September battery: gemini-2.5-flash-lite and gemini-3.5-flash-lite judges in cot-only, cot+out and out-only views, and both committed probes. Add deepseek-chat (out-only), the July strong judge, and three probes trained with `train_probe.py`: single mid-layer deception, within-generation readout, and DolusChat-only.
5. **Predictors**, for every ordered pair (X, Y), with bootstrap CIs over prompts:
   (a) *soft selection*: re-weight each prompt's rollouts by exp(η·A_X), where A_X is the group-centred advantage of reward task − length − λ·X with λ = 0.5, over a range of η; record Δμ_hack(Y), Δd′(Y) and slope β̂(X→Y) = Δμ_hack(Y)/Δμ_hack(X);
   (b) *hard selection*: best-of-k per prompt, k from 2 to 32;
   (c) baselines: Spearman correlation of X and Y scores among hacks (the blind-spot notion), and co-detection correlation.
6. **Test against RL.**
   (i) Compare β̂ with Aether's measured β, recomputed from released metrics with their script: rank correlation over off-diagonal cells, sign agreement, and the three qualitative claims the post is most confident in (strong→weak ≥ 1; weak→strong ≈ 0; judge↔judge > judge↔probe).
   (ii) Four prospective RL runs: pick the two (X, Y) pairs where the predictor is most confident and most opposite (one "Y falls with X", one "Y unaffected"); 2 seeds each, warm-started from the hacking checkpoint chosen in step 2 of this plan, 30 steps of 16×16 rollouts, λ = 0.5, all monitors held out and scored every 5 steps. Predictions are written to a file before the runs start.
7. **Free extras from the pool:** whether recalibrating thresholds restores detection; predicted effect of selecting against two monitors at once on a third.

Key figure: predicted 12×12 coupling matrix beside the measured RL matrix, plus predicted-vs-realised scatter.

## 4. Stage 1 cost estimate
Prices looked up 2026-11-14, per 1M tokens. Tinker Qwen3-8B: prefill $0.195, sample $0.60, train $0.44. OpenRouter in/out: gemini-2.5-flash-lite $0.10/$0.40, gemini-3.5-flash-lite $0.30/$2.50, deepseek-chat $0.257/$1.03. Assumed ~300 prompt and ~700 completion tokens per rollout (not logged in the released runs, hence the large margin).
- Control runs: 2 × 30 steps × 512 rollouts × $0.0011 ≈ $35, plus evals ≈ $40.
- Pool sampling: 16k × (700 × $0.60 + 300 × $0.195)/1M ≈ $8.
- Judges on the pool: weak gemini, 3 views × 16k, ~1k in + ~1.8k reasoning out ≈ $40; strong gemini, 3 views, ~1k in + ~300 out ≈ $50; deepseek ≈ $5. Total ≈ $95.
- Prospective RL: 4 runs × 30 steps × 256 rollouts × $0.0011 ≈ $34; train-against judge ≈ $25; held-out scoring ≈ $30. Total ≈ $90.
- GPU for frozen-model probe scoring and probe training: one 48 GB card, 40 h at ≈ $0.44–0.86/h (RunPod A40/L40S) ≈ $30.
- Subtotal ≈ $265; ×1.45 for token-count uncertainty and reruns ≈ **$390**. If token use is double the assumption, drop step 6(ii) to two runs.

## 5. What success looks like
- *Clear positive:* rank correlation ≥ 0.6 between predicted and measured coupling across cells, the three qualitative patterns reproduced, and both prospective pairs landing on the predicted side. Post: "a $100 no-training audit predicts which held-out monitors fall".
- *Clear negative:* tight predictor CIs but near-zero agreement with step 1 and the prospective runs, with transcripts showing RL found strategies absent from the pool. Post: "static correlation between monitors does not tell you what RL will break". Publishable: it rules out the obvious rule of thumb.
- *Ambiguous:* works for evasion (μ_hack) but not degradation (d′), or only for a few steps. Reportable as the horizon over which the first-order picture holds.

## 6. Stage 2 (if stage 1 succeeds)
A proper prospective test: 6 (X, Y) pairs × 3 seeds of full-length RL, including one two-monitor ensemble (≈ $1,800); the same audit on Aether's terminal environment and a second policy model (≈ $600); an attacker-LLM rewriting optimiser for strategies outside the pool (≈ $200).

## 7. Risks and how the plan handles them
- **First-order prediction is irrelevant beyond a few steps.** Step 1 tests this for free before any spend; the write-up reports the prediction horizon explicitly.
- **Aether's measured β is too noisy a target.** Hence two further checks: within-run forecasts on released per-rollout data, and pre-registered prospective runs.
- **Too few hacks or clean samples per prompt.** Checkpoints are chosen at 30–70% hack rate; statistics are computed per prompt group, as the repo's notes require.
- **Judge drift or unavailability** (claude-3-haiku is gone from OpenRouter): use the September judges, pin model ids, save every call.
- **Pipeline fragility** (Tinker, probe server, Qwen `<think>` stripping, GRPO seeding bug): documented and fixed in the repo; run its 3-step smoke config first.
