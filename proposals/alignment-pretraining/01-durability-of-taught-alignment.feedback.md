# Feedback: Does story midtraining buy durability? (proposal 01, alignment-pretraining)

Verdict: **keep, with tweaks**. The experiment is natural, cheap, uses artefacts that really are public, and I found
no sign it has been done. But the headline contrast (A vs SA) is underpowered as designed and its most likely
outcome is a null; the proposal should be re-centred on the absolute erosion curve, with the A-vs-SA contrast as a
pre-registered secondary test against an explicit null model.

## What I checked

Verified (fetched this session):
- TQW post text: 32B numbers 61% / 43% / 6% / 4%; LoRA r64, alpha 128, lr 1e-4, merged between stages; stories ->
  instruct mix -> advice; Sonnet 4.6 judge; 27 conditions x 100 samples; acting rate >= 90% in every condition.
  The post itself names "later training" overwriting stories as an open hypothesis and cites Arcadia.
- Hugging Face: `SecondLookResearch` has 46 public, ungated adapters, including all five the proposal names
  (baseline, stories+instruct-mix, DA-3000, stack, DA-1000). `Qwen/Qwen2.5-32B` is public, Apache-2.0. The stack's
  model card gives the exact serve command (three adapters chained, `GRAFT=1`).
  `geodesic-research/sfm-emergent-misalignment-training-data` is public and contains `risky_financial_advice` and
  `school_of_reward_hacks` parquets.
- Repo README (raw.githubusercontent.com): `training/fsdp/`, `evaluation/agentic_misalignment/serve_model.sh`,
  250 GB disk for 32B, FlashAttention-3 build ~1 h, instruct mix must be rebuilt (not needed for this proposal).
  **Launchers default to 4xH200 (stories/baseline) and 2xA100 (difficult advice); a single-GPU run is not the
  authors' tested path.**
- Arcadia App. E.2 (arXiv 2609.20412 HTML): MSM+AFT 0.06 -> 0.31 at 2% anti-spec, 0.67 at 20%; AFT-only 0.65 at
  2%. Matches the proposal. Note E.2 also says MSM+AFT stays below AFT-only at every dose, i.e. a
  midtrained-vs-not comparison under contamination exists, but from unequal starts (0.03-0.06 vs 0.44-0.48). The
  proposal's "equal start" novelty claim holds.
- Cho et al. 2607.26654 abstract: -17.5pp blackmail advantage survives benign fine-tuning at 120B. Matches.
- Prices: OpenRouter claude-haiku-5.5 $0.10 / $0.50, claude-sonnet-4.6 $3 / $15 (batch $1.50 / $7.50) - correct.
  RunPod H200 $5.29/h is the Secure Cloud price; **Community Cloud H200 is $3.59/h**.

Not verified / limits:
- The WebSearch tool was unavailable (session search budget exhausted), so the prior-work search was restricted to
  the arXiv API (4 queries, no duplicate found), the TQW comment thread, recent LessWrong post titles and Hugging
  Face listings. No duplicate found, but this is a weaker search than intended.
- Adjacent in-flight work seen on Hugging Face: Geodesic uploaded `nemotron3-super-120b-imid-combined-unsafe-
  {midtrain,sft,em-*}` models on 2026-11-10 and `inoculation-midtraining-*` datasets - midtraining followed by
  emergent-misalignment fine-tuning at 120B. That overlaps arm 3 in spirit (different models, different
  midtraining content). A LessWrong post dated 2026-11-14, "Homeopathic Learning: Diluting Poisoned Fine-Tuning
  Data Can Strengthen Its Effect" (title only; not read), may bear on the 2% anti-spec arm and should be read by
  the proposer before fixing the dose.
- The throughput figures (2K tokens/s training, 8 min eval) are the proposer's unmeasured estimates; I could not
  check them either.

## 1. Would it get upvoted?

Probably, but not on the framing given. Reference points: TQW 111 karma, "Cracks Under Pressure" 141, MSM 73.
A follow-up on public checkpoints two weeks after TQW, answering a question the TQW authors flag and Arcadia's
authors called the most important next step, has a real audience (Second Look, Arcadia, Geodesic, the
Anthropic TCW/MSM authors).

What gets karma depends on which outcome lands:
- "2,000 benign code chats undo most of a 61% -> 5% gain" or "60 bad chats in 3,000 undo it": strong, 80-150.
- "Benign fine-tuning does nothing; only explicit anti-spec data hurts; stories do not change either": this is
  roughly what E.2 plus Cho et al. already lead readers to expect. 30-70 karma; borderline.
- "Stories buy durability" (clear A/SA gap): strong, 100+, but I put it at ~10%.

The A-vs-SA question is the title, yet it is the least likely part to produce a clear result. The part readers
will use is the erosion table: how much of which kind of later fine-tuning removes TCW-style alignment in open
weights. Title and analysis should lead with that.

## 2. Naturalness

Mainline. TQW lists later training as an open issue; Arcadia's authors ask for exactly "alignment-relevant content,
then fine-tune on a random topic with a small bad fraction"; Geodesic's agenda is persistence; TCW claims
persistence through RL with nothing released. Sequential (post-hoc) contamination is distinct from E.2's mixed-in
contamination. Not contrived. Not found done.

One caveat on naturalness: the "depth" hypothesis is being tested on the weakest available instance of
midtraining (14M tokens of stories via LoRA, a stage the TQW authors themselves suspect is under-served by LoRA and
which gave only 18pp alone and 1.5pp on top of advice). A null here will be read by midtraining proponents as "LoRA
stories at 14M tokens are not midtraining" rather than as evidence against alignment-in-depth. The proposal
overstates what a null would show ("loses its best remaining open-weight support").

## 3. Pre-mortem

How it will play out:

Day 1 morning: pod up, 64 GB base download, graft, chained merges. Single-GPU training is off the authors' default
path (FSDP launchers with n_gpus), so expect a few hours of launcher fiddling. Reproducing B ~0.6 and A ~0.06 on
the 6-condition subset probably works (two independent groups have reproduced these evals). The 6-condition
subset mean is not the 27-condition mean; a "within 10pp" gate against 0.61 / 0.06 is the wrong reference - use
the same six conditions from the released `conditions.csv`.

Day 1 afternoon to day 2: ~34 train/merge/serve/eval cycles (16 + 4 unperturbed + 8 seeds + 6 dose), serial on one
pod at 40-60 min each = 23-34 h. That does not fit comfortably inside two days after setup. It needs two pods in
parallel from the start, and the plan does not say so.

Likely results by arm:
- Benign (3M tokens code/maths): my guess is A and SA move from ~5% to somewhere in 5-15%. The evidence: stories'
  18pp effect already survived 18M token-epochs of instruct-mix training at the same LoRA recipe. Small movement,
  A ~ SA.
- Code/maths-only data contains no tool calls. A real chance that acting rate drops or tool-call formatting
  degrades, which lowers measured misalignment for a boring reason. "Conditional on acting" only partly fixes this.
- Reward-hack demos and risky financial advice: unknown; Qwen2.5-32B is EM-resistant (2607.04510). Plausibly
  small effects on AM. Two arms spent on perturbations likely to do little.
- 2% anti-spec (60 chats in advice format): likely the only arm with a large effect. It directly opposes the
  advice stage in its own format, so it is the arm least able to show a stories-specific benefit.

The power problem with the headline contrast. The natural null for "depth" is that each model reverts toward its
own pre-advice level: A toward B (61%), SA toward S (43%). Under that model the A-SA gap is at most 18pp at
complete reversion and proportional before that: if a perturbation undoes 30% of the gain, A goes to ~22% and SA
to ~16%, a 6pp gap. The proposal's "depth is real" bar (A rises >= 15pp more than SA) therefore needs near-total
reversion or a super-additive effect, and its "depth is not real" bar (within ~5pp) cannot be told apart from
additive depth at partial reversion. Training-seed SD for these LoRA runs is unknown (TQW ran one seed
throughout); if it is 4-6pp, two seeds for A and SA and one for everything else cannot resolve a 6pp gap. The
eval SE (810 transcripts, but 27 clustered conditions) is not the binding noise source.

Other threats:
- Cheap-judge calibration is done on unperturbed start models, but the judge's hard cases will be in perturbed
  models (half-degraded tool use, partial actions). The eval README also notes the judge sometimes refuses to
  grade leaking transcripts. Calibration must include perturbed-model transcripts and report per-scenario
  agreement, not a pooled 95% (at a 5% base rate, 95% pooled agreement is compatible with missing most positives).
- A-1000 (21%) as the "matched start" control is not matched to anything; it is a dose point, fine, but it does
  not address the 5.8 vs 4.3 start gap (which is negligible anyway).
- SA differs from A by "28M token-epochs of any extra SDF + a different advice adapter", not only by story
  content. No control for that. Only matters if a gap appears.
- Fallback to Tinker with Qwen3.5-35B-A3B-Base abandons the released adapters and an unknown baseline AM rate;
  it is effectively a different, riskier project (rebuilding four models before the experiment starts).

Outcome probabilities:
- Clear positive (stories buy durability, gap well outside seed noise): **10%**
- Clear negative that is still interesting (clean erosion numbers; at least one non-adversarial perturbation
  erodes a large share of the gain, or all non-adversarial ones clearly do not, with A ~ SA shown with adequate
  seeds): **40%**
- Ambiguous mush (small erosion, A-SA gap of a few pp inside seed spread, acting-rate confound, only the
  anti-spec arm moves): **35%**
- Fails to run / only a fraction of the grid completes: **15%**

## 4. Cost check

The proposal's $270 is in the right range but optimistic on hours. My estimate:
- GPU: 34 cycles x ~55 min + 6 h setup/debug = ~37 GPU-hours. At $5.29/h = $196; at Community Cloud $3.59/h =
  $133 (availability not guaranteed). Two pods in parallel cost the same GPU-hours plus duplicated setup (~3 h,
  ~$16) and a second base download.
- Disk: four merged start models at ~64 GB each plus base plus working merges needs ~400-500 GB, not 250 GB;
  a few dollars.
- Judging: Haiku 5.5 on ~27.5K transcripts ~$17 (confirmed price); Sonnet 4.6 calibration on ~1,200 transcripts
  (start + perturbed models) ~$25, or half that with the batch price. If Haiku fails calibration, Sonnet 4.6 batch
  on the full grid is ~$290, which breaks the budget; the fallback of 27 x 15 samples is ~$145.
- Total: ~$240 base, **~$350-400 with realistic rerun margin**, ~$480 if the cheap judge fails. Under the $500 cap
  but with less headroom than stated. With the cuts recommended below (fewer arms, more seeds) the cycle count is
  about the same.

## 5. Recommended changes (most important first)

1. **Re-centre on erosion; make A-vs-SA a pre-registered secondary test.** State the null model explicitly:
   each model reverts toward its own pre-advice level (A -> B, SA -> S). Report, per perturbation, the fraction of
   the advice gain lost, f = (AM_after - AM_before) / (AM_pre-advice - AM_before), for A and SA separately.
   "Depth beyond additive" = f(SA) < f(A); "additive depth" = equal f but SA's asymptote is lower; "no depth" = SA
   converges to A's absolute level. Drop the ">= 15pp" and "within 5pp" thresholds, which do not distinguish these.
2. **Buy seeds, not arms.** Run one seed of the benign and anti-spec arms on A and SA first, then measure seed SD
   with 3 seeds on the single most damaging arm for A and SA before spending on anything else. Cut B and S from all
   arms except benign (the S-vs-B test of whether a prior persists) and the most damaging arm. Cut either the
   reward-hack or the risky-financial-advice arm unless a one-seed pilot on A shows > 10pp movement.
3. **Add a dose-response in the arm that works, since erosion is the headline.** Anti-spec fraction at 0.5%, 2%,
   10% (15 / 60 / 300 chats) and benign-only at 1M / 3M / 10M tokens for A and SA. A curve is far more quotable
   than a single cell, and it reaches the high-reversion regime where the A-SA gap is detectable if it exists.
   Read the 2026-11-14 "Homeopathic Learning" post before fixing doses.
4. **Protect tool use in the benign set.** Mix in ~20-30% tool-calling chats (held-out portion of the instruct
   mix's tool-call source, or the mix itself) so that the perturbation does not just break the email agent. Gate
   every perturbed model on acting rate >= 85% before interpreting it; report both raw and conditional rates.
5. **Fix the reproduction gate.** Compare against the same six conditions in the released `conditions.csv`, for
   all four start models, not against the 27-condition means; and plan two pods from hour one. Use Community
   Cloud H200 if available. Budget disk at ~500 GB and save the four merged start models once.
6. **Calibrate the judge on perturbed-model transcripts** as well as start models, stratified by scenario, and
   report positive-class recall and precision rather than pooled agreement. Count judge refusals.
7. **Conditional control only if a gap appears:** train DA-3000 on top of the released
   `stories-sonnet-5-human-instruct-mix` (one ~40-minute run) to test whether any SA advantage is about
   aligned-AI story content or about any extra SDF stage.
8. **Soften the claims.** A null does not falsify alignment-in-depth; it shows 14M tokens of LoRA story SDF gives
   no measurable durability on Qwen2.5-32B on this eval. Say so in section 5, and drop "best remaining
   open-weight support" (Cho et al. and E.2 are both stronger support than TQW's stories).
9. Drop the Tinker fallback as written, or replace it with: if the 32B pod loop is not reproducing by hour 8,
   shrink to A and SA, benign + anti-spec only.
