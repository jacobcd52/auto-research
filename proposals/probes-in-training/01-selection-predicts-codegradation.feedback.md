# Feedback: 01 — selection-based predictor of monitor co-degradation

Verdict: **major overhaul.** The idea (a no-training audit for held-out-ness) is good and is what the authors ask for. The validation half of the plan does not work as written: the free go/no-go has almost nothing to predict, the published β matrix is a compromised target by the authors' own later analysis, and the prospective test is two pairs with a high chance that the trained-against monitor never moves.

## What I checked

| Claim | Status |
|---|---|
| Post content (setup, findings, small-n caveat, "rules of thumb" request, footnote on blind-spot correlation) | Confirmed from the post text. 64 karma, 0 comments. |
| Repo public; `README.md`, `STATUS.md`, `experiments/analyze_coupling.py`, committed probe `meta.json` | Confirmed (HTTP 200 on raw.githubusercontent.com). |
| `init_from_tinker_ckpt` warm start and per-eval checkpoints exist | Confirmed in `STATUS.md` (added 2026-10-14 and 2026-09-30). |
| sep3 `eval_rollouts_slim.jsonl` (per-rollout scores, no text) | Confirmed indirectly: `experiments/coupling_splithalf_proto.py` and `docs/DEGRADATION_METRICS.md` load and describe it. I did not download a run directory or count the nine runs. |
| Prices: Tinker Qwen3-8B $0.195 / $0.60 / $0.44; OpenRouter gemini-2.5-flash-lite $0.10/$0.40, gemini-3.5-flash-lite $0.30/$2.50, deepseek-chat $0.257/$1.03; claude-3-haiku delisted | All confirmed today. |
| "No prior work predicts cross-monitor degradation from static data" | Not contradicted, but my search was thin: the web-search budget was exhausted, so I only ran four arXiv API queries (no hits) and one LessWrong site search (only the cluster's own posts). Treat novelty as probable, not established. |
| `row_control` config name, `train_probe.py` options for the three new probes, GPU prices | Not checked. |

The important thing the proposal omits is in the repo's own `docs/DEGRADATION_METRICS.md`, section "Split-half" (2026-09-08), written after the post:

- Same-sample β is "inflated by shared eval-rollout noise, and not a little"; the judge–judge coupling in the published matrix is "largely artifact".
- d′ is unusable at high hack rates (residual "clean" rollouts are label errors).
- With the unbiased split-half estimator on sep3, only two trained-against rows (`probe_iid`, `probe_ood`) pass the driver gate. Every held-out cell is consistent with zero except one: `probe_ood` → weak cot+out judge, +0.18 [+0.05, +0.34].
- Held-out judges stayed at 0.94–1.00 catch rate while the probes were evaded to 0.01–0.05.
- Aether already measured item-level score correlations (judge–judge 0.2–0.7, probe–judge ≈ 0), which is the proposal's baseline (c).

## 1. Would it get upvoted?

A clear positive, validated prospectively, would clear 50: "a $100 no-training audit tells you which held-out monitors fall" is directly useful to the people who wrote and upvoted the Aether and Arike posts (64 and 84 karma). The audience is small, though; the Aether post drew no comments.

The outcome this plan can actually deliver is weaker. The likely headline is "predictor says roughly zero cross-coupling, RL shows roughly zero cross-coupling in 30 steps, n = 2 pairs". That is a 20–40 karma post. A negative result only earns karma if RL demonstrably breaks a held-out monitor the pool said was safe, which needs RL runs in which something breaks.

## 2. Naturalness

Mainline. The post's future-work section asks for rules of thumb that predict co-degradation in advance, and its footnote suggests exactly the blind-spot correlation used here as baseline (c). I found nobody who has done the reweighting version.

Two qualifications:

- Aether has the static half informally already (item-level correlations next to causal β, in the repo docs). The new contribution is the selection-response predictor and a large pool with text, not "static correlation versus coupling".
- Aether is active in this repo and could run this analysis on their private full rollout dumps in an afternoon. The risk of being scooped is real but not checkable.

## 3. Pre-mortem

Forecast: clear positive 10%, clear and interesting negative 20%, ambiguous mush 55%, fails to run 15%.

How it plays out, in order of damage:

1. **The step-1 go/no-go has no outcome variance.** In sep3 the realised change in held-out monitors is about zero in every gated row. A predictor that outputs zero "agrees"; sign agreement and rank correlation on noise will come out near chance. The proposal reads chance level as "the headline negative", which would be a false negative about the method. The "180 step-pairs × 7" figure also overcounts: controls, non-hacking seeds and collapsed steps drop out, and Aether reports 9–16 usable Δ-pairs per target across 2–3 seeds.
2. **Step 1 as specified is biased.** Predicting from step t's 256 rollouts (64 prompts × 4 samples) and scoring against t+3 minus t reuses step t's sampling noise on both sides, giving a regression-to-the-mean artifact. Four samples per prompt, split between hacks and clean, cannot support a within-prompt covariance of a hack-conditional mean.
3. **Comparison 6(i) targets a matrix its authors no longer trust.** Two of the three "confident qualitative claims" (strong→weak ≥ 1, judge↔judge > judge↔probe) are the same-sample judge–judge couplings the repo now calls largely artifact. The July weak judge (claude-3-haiku) is gone, so the strong→weak cell cannot be reproduced on the pool at all.
4. **Selection on judge noise.** LLM judge scores are stochastic and sit near ceiling on hacks (μ_hack ≈ 0.9; strong judges almost never fooled). Reweighting by X's score selects partly on X's call noise, which is not a property of the rollout and does not transfer to Y. Predicted Δμ_hack(X) is inflated and β̂ is biased toward zero. For strong judges there may be no variance among hacks to select on.
5. **"First order" is overstated.** The policy-gradient response of Y is a Fisher-kernel-weighted covariance across rollouts and prompts, not the raw within-prompt covariance. Exponential tilting is the tabular idealisation. Also, the dominant response to a task − λ·X reward from a 30–70% hacking checkpoint is a fall in hack rate (at λ = 1 Aether's policies went honest), not a change in how hacks look. μ_hack on a shrinking set of hacks is a second-order, noisy quantity.
6. **Out-of-support strategies are the known mechanism.** The post's own examples (repeating "this code is perfect", lambda hardcodes that beat the labeller) are absent from a control policy's samples. Best-of-32 cannot see them. This is the prior reason to expect the predictor to miss the interesting cases.
7. **The prospective test is underpowered.** Two pairs × two seeds × 30 steps at 256 rollouts. Aether needed 90 steps at 512, and many seeds never evaded the target. If X does not move, β is undefined; a "Y unaffected" prediction is then confirmed trivially. Picking the two most confident pairs selects the easiest cases.
8. **Infrastructure.** Tinker plus a GPU probe server in the loop, the patched Qwen template, twelve monitors, and warm-start, which needs full training states (`save_every`), not the sampler checkpoints saved at eval steps. Control runs may not start hacking by step 30 on a given seed. Each is survivable; together they eat day 1.

## 4. Cost check

The arithmetic is right at the stated token counts, and the prices are current. My estimate for the plan as written is $350–450, so $390 is fair but leaves little slack: Qwen3-8B with thinking and `max_tokens` 2048 can easily average more than 700 completion tokens, and judge reasoning tokens are a guess. The 40 GPU-hours are more than needed.

The problem is allocation, not total. About $95 goes on scoring 16k rollouts with twelve monitors and about $90 on the only part that can validate anything.

## 5. Recommended changes

1. **Rebuild validation around fresh RL in which the target is known to be evadable.** Train against `probe_iid`, `probe_ood` and the weak cot+out judge: the first two were driven to ≈ 0.01–0.05 catch rate in sep3, the third moved in July. Three targets × 2 seeds, 45–60 steps, warm-started, at roughly $35 a run ≈ $210. Pre-register the full predicted row for each target, not two hand-picked pairs.
2. **Pay for it by shrinking the pool.** Use the eight September monitors only, about 8k rollouts. Drop deepseek, the July judge and the three new probes from stage 1; a 12×12 predicted matrix with nothing to compare against is decoration.
3. **Demote step 1 to a sanity check, not a go/no-go.** Its only informative cell is `probe_ood` → weak cot+out (+0.18). Use split-half over tasks and μ_hack and catch rate, never d′.
4. **Score each rollout twice with every judge.** Select on one call, measure on the other, so the predictor uses only the repeatable part of the score. Report each judge's test–retest correlation among hacks; if it is near zero, say that the predictor is undefined for that judge.
5. **Predict three quantities separately:** hack-rate change, μ_hack and catch rate of hacks, and μ_clean. State in advance that hack-rate change is expected to dominate.
6. **Drop comparison 6(i)** or reduce it to one caveated paragraph; cite the split-half section as the reason.
7. **Make the negative result concrete.** Save rollout text from the RL runs and measure what fraction of late-run hacks fall outside the pool's support (for example, nearest-neighbour distance in an embedding, or a judge asked "is this strategy present in these pool samples?"). That number is what turns "predictor failed" into "static audits cannot certify held-out-ness".
8. **State the estimator honestly** as a tabular / natural-gradient approximation, and say that Aether already reports item-level correlations beside causal β.
9. **Day-1 order:** smoke config, then confirm a control seed hacks and that a full training state is saved at the chosen step, before any pool scoring.

If the funder will not accept items 1–4, fund proposal 02 or 03 from this cluster instead: as written, the most likely product here is an elaborate confirmation that near-zero predicts near-zero.
