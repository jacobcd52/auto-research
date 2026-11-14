# Feedback: 02 — matched A/B on natively pretrained latent-feedback transformers

Reviewer verdict: **keep, with substantial tweaks.** The asset is real, days old, and fills a gap two posts name.
The design as written will probably saturate and produce a flat, low-information plot; the fixes are cheap.

## What I verified (2026-11-14)

| Claim | Status |
|---|---|
| `IFM/latent-feedback-checkpoints` is public, Apache-2.0, 174 runs, arms `transformer`/`feedback`, 60M/134M/271M/778M | **True** (HF API; 174 folders counted). Created 2026-11-11, 0 downloads. |
| Cell `u100-f1` exists at all four sizes in both arms, with `-s1`/`-s2` at 134M | **True** (12 folders listed). |
| LoRM code is public and readable | **True** via raw.githubusercontent.com: `lorm/model/feedback.py`, `works/latent_feedback/README.md`, `configs/runs.csv` all fetched. |
| Feedback wiring: u_t = e_t + W rms(h_{t-1}), top layer to input embedding, earlier passes detached, 2 passes on 85% of updates | **True** (read `feedback.py` and a `config.yaml`: `pass_mix: [0.15, 0.85]`). |
| `xidulu/full_bandwidth_transformer`: one control + three fusion variants, empty README | **True** (4 checkpoints, 10.4 GB). |
| Redwood: 1M TinyStories model, n=12, m<=8; reward `1(correct) - (visible CoT ratio)`; "lack of access to good parallel latents models"; filler-curriculum suggestion | **True** (post text). Note that reward was used in the "pressure during task learning" sub-experiment, not the main one. |
| Dory post quote "we don't have a direct A/B comparison to a non-looped model that underwent otherwise identical training"; one seed per arm | **True**. Currently 48 karma after 2 days. |
| Prices: gpt-5-nano $0.05/$0.40, gpt-6-sol $2/$10 | **True** (OpenRouter API). RunPod L40S price taken from NOTES, not re-checked. |
| "No monitorability evaluation of these checkpoints exists" | **Not contradicted.** LW posts since 2026-11-01 scanned by title: nothing. Dory post comments: nothing. My web-search budget was exhausted, so I could not run an independent web search; this rests on the proposer's searches plus my LW scan. |

Three things I found that the proposal does not mention, all from `runs.csv` and `metrics.jsonl`:

1. **At the chosen cell the feedback model is barely better than the transformer.** Validation-loss gap
   (transformer minus feedback) at `u100-f1`: 60M +0.004, 134M +0.001, 271M +0.002, 778M +0.004 nats. The 134M seed
   spread is about 0.001. The advantage is largest at high U/N and high F (up to +0.024 at `60m-u400-f4`) and is
   *negative* at low U/N, F=1 (-0.037 at `60m-u12.5-f1`).
2. **The feedback model does use its channel, but shallowly.** For `feedback-134m-u100-f1`: nll@P1 2.528, @P3
   2.4675, @P4 2.4672. Turning feedback off costs 0.06 nats; going from 3 to 4 passes changes 0.0003. The fixed
   point is reached in about two hops. Nothing in pretraining rewarded long serial chains through the latent.
3. **"Identically trained" means FLOP-matched, not step-matched.** At F=1 the feedback arm runs 0.81 epochs
   against 1.0, with fewer steps and a separately tuned lr/wd (the 60M feedback run uses twice the transformer's
   lr). Same data stream, same FLOPs. This is a fair match but must be stated precisely.

## 1. Would it get upvoted?

Borderline, leaning yes: I put it at 45-55% to clear 50 karma if it works as described.

For: the cluster's posts sit at 83-148; the Dory replication, a weaker design (one seed, no matched control), got
48 in two days. Redwood and the Dory authors both name this exact gap, and Greenblatt's proposal asks for this
measurement. A clean three-arm, four-size plot with seeds is a better-controlled result than anything in the
cluster.

Against: the models are 60M-778M base LMs on a toy task, and the adjacent "LLMs can learn (some) multi-step
reasoning on filler tokens" post is at 10 karma after three days. Toy filler results do not get upvoted on their
own. The headline "F > T" is what every reader already expects. The karma depends on one of the non-obvious
findings landing: (a) the retrofit matches or beats native pretraining, (b) the native two-pass recipe yields
almost no extra hidden depth, or (c) a real scale trend. Finding 1 above makes (c) unlikely at the chosen cell.

Scoop risk is real: the Dory post appears to come from the same group as the Redwood post, published three days
ago, and the IFM release is exactly what they said they lacked. Speed matters; this argues for funding now and
for a lean stage 1.

## 2. Naturalness

Mainline. It is the obvious next experiment for readers of both empirical posts, and no new benchmark is built.
Not found done elsewhere (subject to the search caveat above).

One caveat on framing: the primary metric is hidden serial depth under an all-filler prefill, not monitorability.
That is fine and is what Greenblatt's footnote asks for, but the title and write-up should say "hidden serial
reasoning", with the RL/monitor part as secondary.

The Redwood authors recommend against gain-of-function on latent architectures. Evaluating public checkpoints is
within what they call reasonable. Backprop-through-positions fine-tuning of F is the same thing Redwood did to
their retrofit, so it is defensible, but do not sweep fusion designs or publish tuning recipes.

## 3. Pre-mortem

How it plays out: loading works (code is clean, checkpoints are plain `.pt` with a config). The team spends day 1
writing token-by-token decoding with a KV cache and gradients, plus SFT for small base LMs pretrained with
NorMuon at lr ~0.017 where fine-tuning hyperparameters are unknown. SFT with backprop through positions makes
both F and R solve all-filler permutation power at every size, because Redwood's 1M-parameter retrofit already
did. T manages 3-5 hops. The plot is three flat lines: F and R at the ceiling m=16, T near 4. RL then shows F and
R going all-filler in tens of steps at every size, T not. This is a replication with a matched control, and
"native = retrofit", but no scale story.

Forecast:
- Clear positive with a scale trend as in section 5: **10%**.
- Clear and interesting, but a different story (retrofit matches native; native two-pass recipe buys roughly one
  extra hop; gap flat in scale): **40%**.
- Ambiguous mush (differences driven by fine-tuning hyperparameters per arm and size; ceiling effects; single
  pretraining seed outside 134M): **35%**.
- Fails to run or runs only at one or two sizes: **15%**.

Specific failure reasons, most likely first:

1. **Ceiling.** n=12, m<=16 is too easy for a model trained with gradients through the recurrence. Horizon(F) and
   horizon(R) will both equal the maximum m, so F-T is just "max m minus 4" at every size and F-R is zero by
   construction. The task as specified cannot show a scale trend.
2. **Wrong pretraining cell.** At `u100-f1` the feedback arm is within seed noise of the transformer on loss. If
   native pretraining matters anywhere, it is at high-F, high-U/N cells where feedback wins by ~0.02 nats. The
   F=1..4 axis at fixed size is a better "dose" of latent use than parameter count, and exists at three sizes.
3. **Elicitation unfairness swamps the effect.** Twelve arm-size cells, each needing its own lr; R has a fresh
   zero-init matrix (Redwood used 10x lr and a W-only warm-up), F has a pretrained one. Any F-vs-R gap can be
   moved by these choices. The proposal's "own-CoT accuracy matched" control does not address this.
4. **The R arm is underspecified.** Redwood's retrofit is late-block-to-early-block with N, M unpublished; IFM is
   top-layer-to-embedding with RMS norm. If R uses different wiring from F, the F-vs-R comparison confounds wiring
   with pretraining.
5. **The detached two-pass SFT variant is ambiguous as written.** Training with two passes and evaluating with
   token-by-token decoding is a train/test mismatch; a poor result could mean "no deep latent computation" or
   "fixed-point decoding is off-distribution after SFT". Needs evaluation at passes = 1, 2, 4 and token-by-token.
6. **Small base LMs with the llama2 SentencePiece tokenizer.** Names split into several pieces; "single-token
   symbols" needs care (leading-space variants). Solvable, but a classic silent eval bug.
7. **RL stage adds little.** With reward `1(correct) - visible fraction` and an all-filler-capable SFT checkpoint,
   F and R go dark immediately; the gpt-5-nano judge on an all-filler CoT is a formality. 36 RL runs plus judges
   are most of the fragile pipeline for the least new information.
8. **One pretraining seed at three of four sizes.** A scale trend rests on single checkpoints per size.

## 4. Cost check

The estimate is realistic, slightly generous. Checkpoints for the 12 runs total about 10 GB, not 40 (778M is
3.1 GB each). Token-by-token training is sequential in position, so wall-clock per step is far above a
teacher-forced pass; 0.75 h per SFT cell at 778M is optimistic, perhaps 1.5-2 h. GPU hours could reach 150, about
$165 on an L40S. Judge spend is small and could be cut further. My estimate: **$180-280** as written; **$150-200**
with the changes below (less RL, more SFT cells). Well under the cap. Wall-clock, not money, is the constraint:
run cells in parallel on 3-4 cheap GPUs.

## 5. Recommended changes

1. **Remove the ceiling.** Make the task's hidden-depth axis long enough that no arm saturates: m up to 48-64,
   with SFT only on m <= 16 and evaluation beyond, or a harder per-step operation (a non-cyclic permutation over
   more symbols, or modchain-style affine steps). Report full accuracy-versus-m curves, not only a 50% horizon.
   Pilot on 134M first and fix the range before running the grid.
2. **Change the cells.** Keep the size axis at one cell, but add the F axis at 134M and 271M at high U/N
   (`u200`/`u400`, F=1 and F=4, or `u100` F=1..4 with seeds at 134M). That gives a within-size dose of how much
   pretraining leaned on feedback, with seeds, and uses checkpoints where the two arms actually differ. State the
   loss gaps and the P1/P3/P4 losses in the write-up.
3. **Add a zero-training measurement first.** Before any backprop through positions: train only on visible CoT
   with partial filler under each model's native recipe, then test all-filler at passes = 1, 2, 4 and
   token-by-token. This asks whether the *as-released* native model has more elicitable hidden depth than its twin,
   which is the question the Dory and Redwood posts could not answer and the one least sensitive to my
   elicitation-fairness worry. It is cheap and should be the first result.
4. **Make R share F's wiring.** R = transformer checkpoint plus a zero-init top-to-embedding fusion with RMS norm,
   i.e. the IFM architecture retrofitted. Then F versus R isolates pretraining. A Redwood-style mid-layer retrofit
   is optional, at one size only.
5. **Fix elicitation fairness explicitly.** A small predeclared lr grid (3 values) per cell, pick by own-CoT
   validation accuracy, report all. Give R Redwood's W warm-up. Report results as a function of SFT steps, so
   "F gets there in 200 steps, R in 1500" is visible rather than hidden by training to convergence.
6. **Shrink the RL stage.** Run it at 134M and 778M only, T/F/R, 3 seeds, with Redwood's main monitor-based
   penalty rather than the visible-fraction reward if time allows, and keep the learning-speed control. Drop the
   GPT-6 Sol pass unless T shows partial evasion worth re-judging.
7. **State the match precisely.** FLOP-matched, same data stream, per-arm tuned lr/wd, feedback arm sees 0.81
   epochs at F=1. Retitle around "hidden serial reasoning"; drop "does the gap grow with scale" from the title
   unless the pilot shows it can be measured.
8. **Write-up framing.** Lead with whichever of these holds: native pretraining adds nothing over a retrofit; the
   public two-pass detached recipe yields about one extra hop by default; gradients through the recurrence are
   what unlock depth. Each is a concrete input to Greenblatt et al.'s reporting proposal. Keep the
   gain-of-function note and publish no fusion or tuning sweeps.
9. If both 01 and 02 are funded, build the SFT/GRPO pipeline once, on these small models, as NOTES suggests.
