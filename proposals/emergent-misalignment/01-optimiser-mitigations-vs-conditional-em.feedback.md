# Feedback: Do optimiser-level mitigations remove emergent misalignment, or hide it behind a cue?

Verdict: **major overhaul of the design; keep the question.** The question is natural and has not been done, and
the infrastructure is public. But the effect being tested is much smaller on these datasets than the proposal
implies, so the primary metric is underpowered. The "hides behind a cue" framing also does not fit a mitigation
that only partly lowers uncued EM. The judge cost is under-estimated about fourfold.

## What I checked

| Claim | Status |
|---|---|
| Optimiser paper (arXiv 2606.31591): 7x spread, Muon best / Lion worst, regulariser formula, 72.4 vs 69.4, insecure code 86.1 vs base 85.8, no cued evals, no code | Confirmed from the arXiv HTML. The proposal omits important context (below). |
| Conditional misalignment (2604.25891) and its stated open problem | Abstract confirmed; I did not re-check the 10.4% figure. |
| ContextLift (2610.21633): 18.9 / 41.9 / 58.2% to 2.6 / 6.1 / 12.8% | Confirmed from the abstract and the repo's `results/tables/summary.md`. |
| ContextLift repo is public and turnkey | Confirmed. The README is on branch `master` (not `main`) via raw.githubusercontent.com; configs, shipped scores, `src/emabench/pipeline.py` and `pyproject.toml` all fetch. Training goes through `emabench.trainers.sft.train_sft` (Unsloth/TRL), which I did not read. |
| `truthfulai/emergent_plus` public | Confirmed ungated on Hugging Face. |
| Judge prices: gpt-6-luna $0.10 / $0.50, gpt-4o $2.50 / $10 per M | Confirmed on the live OpenRouter list. |
| H100 at $3.99/h | Not checked live. |
| Already done? | arXiv API searches (conditional misalignment + optimiser, EM + Muon, EM + spectral regularisation, conditional misalignment + early stopping, "conditional emergent misalignment") returned only the papers already cited. The web-search budget was exhausted, so I ran no LessWrong or general web search; someone should do one before funding. |

Three facts from the sources that the proposal does not state and that change the design:

1. **The regulariser's effect on advice datasets is small.** In the paper's Table 14 (Qwen3-8B, mean alignment
   score 0-100), regularised Adam at the higher lambda gains +5.1 on medical (66.6 to 71.7), +4.4 on sport, +7.0
   on financial, and +10.2 on insecure code. Muon vs Adam at tuned learning rates on medical is 71.6 vs 66.6.
   The headline effects ("returns alignment to base level") are on insecure code, where the paper itself reports
   code-mode collapse and which ContextLift finds is a null organism on Qwen2.5-7B (5.3% uncued).
2. **The 7x spread is Lion vs Muon at a common learning rate**, marginalised over the sweep, not Adam vs Muon at
   matched loss. On medical at 8B (Table 9), Adam is 15.2% / 10.8% misaligned (bs 2 / 32) and Muon 10.6% / 2.1%.
   The proposal's three arms (AdamW, Adam + regulariser, Muon) leave out Lion, the arm with the big contrast.
3. **ContextLift's no-defence baseline is not a "hidden" organism.** It is 34-38% misaligned uncued, 63-75% cued,
   and 91-98% in-domain. With generic interleaving, uncued is 1.9 / 2.9 / 5.6%.

## 1. Would it get upvoted?

A clean result probably would, around 50-80 karma. The two parent posts got 63 and 71, and the optimiser post
calls the regulariser "a cheap mitigation against EM" on uncued evals only. A crisp "it hides" plot is a direct,
quotable correction; "it removes" is less striking but answers the open problem in the conditional paper.
Readers are the EM / model-organism crowd and the three author groups.

The outcome I expect from the design as written would not clear 50. A post saying "regularisation lowers uncued
EM from 34% to 28% and cued from 75% to 70%, retention ratio 1.1 with a CI of 0.8-1.5" lands at 20-35 karma.

## 2. Naturalness

Mainline. It crosses two posts in the cluster on the axis each leaves open: one evaluates only uncued, the other
names prevention of conditional EM as an open problem. ContextLift's related work mentions the optimiser result
without testing it. It is not on the optimiser author's own follow-up list (RL, weird generalisation, Lion / SGD
residuals, more optimisers, better mitigations), but it is an obvious robustness check of his mitigation claim.

Moving to Qwen2.5-7B 4-bit QLoRA (plain LoRA, lr 1e-4, adamw_8bit, linear schedule) from the paper's Qwen3-8B
bf16 rsLoRA at lr 1e-5 with cosine schedule makes this partly a transfer test. A negative result will be met
with "you did not reproduce their setting".

## 3. Pre-mortem

How it plays out:

- **Gate 1 passes.** The repo ships scores and configs; the main risk is half a day on the pinned Unsloth /
  Transformers environment on a rented pod.
- **Gate 2 is where it goes wrong.** The pass rule is a one-third relative drop in uncued misalignment at loss
  within 0.03 nats. A +5-point mean-score shift on medical is roughly a 15-25% relative drop in rate. One seed
  per calibration setting has binomial noise of about ±3 points on 1,143 answers, plus seed variance. The gate
  will likely fail honestly or pass on noise.
- **If the grid runs, the ratio is uninformative.** With a 20% uncued drop, "hides" predicts a ratio of 1.25 and
  "removes" predicts 1.0. Shipped per-seed cued rates range 32-47% (legal, generic) and 17-27% (medical,
  diluted). Three seeds cannot separate 1.0 from 1.25.
- **The interleaving cells sit on the floor.** Uncued is 2-6% under AdamW, near the judge's false-positive
  level, so the ratio's denominator is noise. The proposal filters on cued rate > 10%, which is the wrong
  filter; the uncued denominator is the problem.
- **The no-interleaving cells hit a ceiling and the in-domain confound.** Cued medical is 75% with in-domain at
  98%; the cue makes many questions near-domain.
- **Loss matching is coarse.** With `save_steps: 200` over ~675 steps and a linear schedule there are three or
  four checkpoints per run. Matching to 0.03 nats needs interpolation or denser saves.
- **The early-stopping arm is the most promising and gets the least attention.** It can produce a large uncued
  reduction (the "Overtrained" paper claims near-elimination), which is the regime where "hides vs removes" is
  meaningful. Here it is a free afterthought.

Other failure reasons:

- Muon on LoRA factors under 4-bit QLoRA with a non-rs scale needs its own learning-rate search. The paper's
  tuned values (Muon 3e-5 vs Adam 1e-5) do not transfer to a pipeline running AdamW at 1e-4. Budget 6-10
  calibration runs, not 3.
- The regulariser is reimplemented with no reference code. The paper uses a Cholesky-of-Gram trick in float32
  with an epsilon and averages over all layers; under 4-bit Unsloth the adapters may be in mixed precision.
  Checking stable rank is a good control and should stay.
- The dataset-aware re-judge is a new, unvalidated judge. The repo already ships a prompt classification
  (broad vs ambiguous / domain, Table 4) and an everyday-cue control. Use those.
- fish20 has 5.4% uncued EM with no defence, which is useless as a ratio denominator.

Forecast for the design as written:

| Outcome | Probability |
|---|---|
| Clear positive (clean "hides" or clean "removes" with a CI that excludes the other) | 15-20% |
| Clear negative that is still interesting (optimiser / regulariser effect does not transfer to this setting at matched loss, shown convincingly) | 20-25% |
| Ambiguous mush (small uncued effect, ratio CI spans both hypotheses) | 40-45% |
| Fails to run or runs out of budget | 15% |

## 4. Cost check

The table's arithmetic is right ($359), but two lines are low.

- **Judge.** The README says the paper's 139 seeds cost "roughly 300 USD of judge calls", about $2.2 per
  full evaluation (about 6,000 calls at `reasoning_effort: low`, whose reasoning tokens bill as output). The
  proposal's 110 evaluations are therefore about $240, not $54. Dropping the everyday-cue and tiny-benchmark
  evals on intermediate checkpoints saves about a quarter; batch pricing ($0.05 / $0.25) halves it if the
  harness is adapted.
- **GPU.** The README reports 236 H100-hours for 139 seeds including superseded runs, about 1.7 h per seed
  all-in against 35-50 min nominal. Each extra checkpoint evaluation generates about 3,000 answers at 256
  tokens. A realistic total is 70-85 H100-hours rather than 53: $280-340 at $3.99/h, or $190-230 at $2.69/h.

My estimate for the plan as written is **$520-620** including 25% margin, over the cap. It fits in about
$400-450 with batch judging, a cheaper GPU tier and a trimmed grid (below).

## 5. Recommended changes

1. **Replace the retention ratio with a dose-response curve.** Pool every checkpoint from every arm and plot
   cued misalignment against uncued misalignment (logit axes), coloured by optimiser. The question becomes: do
   all arms lie on one curve, or do some sit above it? Fit cued ~ uncued + arm with seed-clustered errors. This
   uses 4+ checkpoints x 3 seeds per arm, needs no exact loss matching, and has no fragile denominator. Save
   every 75-100 steps.
2. **Add Lion and promote early stopping to a first-class arm.** Lion vs Muon is where the paper's large
   contrast is. Early stopping is where uncued EM can approach zero, the regime in which "hidden behind a cue"
   means something. If needed, drop the Adam / AdamW distinction (the paper finds them identical).
3. **Rewrite gate 2 around a contrast that can be detected.** Pass if Lion vs Muon, or early vs late AdamW,
   differ in uncued misalignment by at least 10 absolute points at comparable narrow-task perplexity, with 2
   seeds. If only the regulariser's roughly 5-point shift is available, stop and write the transfer null rather
   than run the grid.
4. **Use the right cells.** Keep the no-defence pure sets for the curve. Replace "bad data + generic
   interleaving" on pure sets with the shipped diluted `hh90_baseline` sets (uncued ~2%, cued 11-22%): this is
   the Dubiński setting, and the claim there is simply whether the optimiser lowers the cued rate, an absolute
   difference with no ratio. Prefer security and legal over medical, whose cued set is the most
   domain-contaminated. Drop fish20.
5. **Handle the in-domain confound with what is shipped.** Report cued rates on the "broad" prompt class only
   and the everyday-cue control. Make the dataset-aware re-judge optional, and only after a 100-response manual
   read.
6. **Fix the budget.** Judge at about $2 per evaluation, batch pricing, reduced eval set on intermediate
   checkpoints, and a live GPU price check. State about $430 and say what is cut first if gates run long.
7. **Reword section 1.** State the per-dataset regulariser gains on advice data (+3 to +7 points), that the 7x
   is Lion vs Muon at a common learning rate, and that the "base-level" recovery is on insecure code, which is
   null here. Stage 2's Qwen3-8B rsLoRA replication matters more than the proposal suggests; if gate 2 fails,
   run that fallback, not the grid.
8. **Before funding,** run the LessWrong / web search I could not, for a reply by the optimiser authors or a
   cued re-evaluation of their mitigation.

With changes 1-4 I would put a clear, postable result at roughly 40-45%, with the transfer null as an honest
fallback. As written, I would not fund it ahead of the cluster's other two proposals.
