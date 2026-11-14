# Feedback: 04 — Is taught alignment one direction deep?

Reviewer verdict: **keep with substantial tweaks.** The artefacts are real and the question is one the authors
ask for, but as written the headline experiment (ablate the top shift directions, watch AM return) cannot
distinguish "alignment is one direction" from "any fine-tune's mean shift is low-dimensional and ablating it
undoes the fine-tune". The plan needs a contrast that isolates alignment from generic advice-tuning, and a
different framing of what "shallow" means for a LoRA whose un-adapted baseline is already public.

## What I verified

- **Adapters are public.** HF API lists exactly 46 models under `SecondLookResearch`; every 32B checkpoint the
  proposal names exists (Terra advice 500/1000/2000/3000, Sonnet-1000, the four 135-example grid models, the
  story variants, the stack). `Qwen/Qwen2.5-32B` is ungated, Apache-2.0. Adapter repos are ~2.1 GB, r=64,
  alpha=128, targets q/k/v/o/gate/up/down, plus a `base_row_patch.safetensors` ("graft") that must be applied
  to the base before merging. `eval_scores/conditions.csv` and `samples.csv` exist (verdicts only, no transcripts).
- **Prior-work numbers.** 61 / 43 / 6 / 4% match the post. The post's future-work sentence is "we are excited
  about interpretability research that studies how some of these data interventions affect personas and why some
  of them generalize better than others" — the proposal's paraphrase is fair. SPP's abliteration claim is as
  described, and SPP itself says "we have not yet done this analysis" of activation space. arXiv 2607.04510
  exists and says what the proposal says (its effect sizes are small: 2.83% vs 1.1% floor).
- **Prices.** OpenRouter: claude-haiku-5.5 $0.10/$0.50, claude-sonnet-4.6 $3/$15 — correct. RunPod H200 $5.29/h is
  the Secure Cloud price; Community Cloud is listed at $3.59/h.
- **Already done?** The WebSearch budget for this session was exhausted before my queries ran, so the novelty
  check is weaker than I would like. What I could do: the four comments on the TQW post (none mention
  interpretability; `lciric` is re-running MSM evals, not activations), and arXiv API queries for "Teaching Claude
  Why", "difficult advice"+steering, "agentic misalignment"+steering+Qwen, midtraining+steering/ablation. Only
  adjacent hits (2607.26173 "Shared SFT Lessons…", which is behavioural). I found no duplicate, but the post is
  12 days old and the authors (UChicago XLab / Second Look) named this direction themselves; treat the
  probability that someone is already doing it as non-trivial (~15-20%).
- Not checked: the repo's `merge_adapter.py` / `serve_model.sh` beyond README mentions; whether `git clone`
  works from a rented box.

## 1. Would it get upvoted?

Borderline. TQW itself got 111 karma but only four comments; SPP 131; MSM 73. An interpretability follow-up on
one replication's adapters is a narrower audience than any of those. My estimates:

- Clean "one direction, causal both ways, not the refusal direction, and it separates Terra from Sonnet advice":
  60-90 karma. This is a quotable result and the TQW/MSM/SPP authors and the persona-vector crowd would engage.
- Clean "distributed, top-k ablation does nothing": 40-60. Readers will ask whether the ablation was simply too
  weak, and negative ablation results are hard to make convincing.
- The proposal's own "weak result" (a direction that correlates with AM, causal arms inconclusive): 20-40. This is
  the most likely outcome (see §3).

The "depth test of the recipe Anthropic uses in production" pitch oversells: this is a rank-64 LoRA on Qwen2.5
base, and readers will say so.

## 2. Naturalness

Mainline in the sense that the authors asked for it and SPP flagged the same gap. Two framing problems make it
less natural than it looks:

1. **"Removable by anyone with weights" is vacuous here.** Advice-3000 is `baseline + a rank-64 delta per
   matrix`, and the baseline adapter is published. Anyone can remove the alignment by not loading the last
   adapter. The SPP/refusal-direction analogy works there because no un-aligned counterpart exists; here it
   does. So "shallow vs deep" cannot be about removability. The interesting questions are (a) is the
   *behaviourally relevant* part of the change low-dimensional, (b) is it shared across teachers/formats, and
   (c) can it be read off cheaply as a screening metric. The proposal should say this, or reviewers will.
2. **Low-dimensional mean shifts are the expected default for fine-tunes**, not a discovery. Work on
   activation differences after narrow fine-tuning, persona vectors, and the EM convergent-direction papers all
   find that a fine-tune's mean residual shift is dominated by a few directions that encode the *training data's
   domain and register*. So "PC1 explains most variance and ablating it restores AM" is the unsurprising outcome
   and, on its own, says nothing about alignment (next section).

## 3. Pre-mortem

Rough forecast: **clear positive 20% / clear negative that is interesting 12% / ambiguous mush 55% / fails to
run 13%.**

How it plays out, and where it goes wrong:

- **The core confound: "alignment direction" vs "I-was-fine-tuned-on-advice-chats direction".** The advice data
  is long, deliberative, second-person ethical counsel. Its mean shift will encode that register. Zero-ablating
  it from advice-3000 will push the model back toward baseline behaviour in general, so AM rises — for the same
  reason deleting the adapter does. Random-direction and refusal-direction controls do not address this; they
  only show the direction is not arbitrary. The plan has the right contrast sitting in its model list and does
  not use it: **Terra vs Sonnet advice at matched n and format** (21% vs 44% at 1000; 12% vs 39% in the
  135-example grid, with swapped-prompt cells). If the Sonnet-1000 model's own top direction, ablated from the
  Sonnet model, also returns it to ~60%, and the Terra and Sonnet directions have cosine ~0.9, the finding is
  "advice-tuning is one direction and teachers differ in magnitude" — which is still a result, but a different
  headline. If the Terra-minus-Sonnet residual carries the gap, that is the genuinely new finding.
- **Prediction test is nearly rigged.** The 16 "held-out" models are ~6 advice models at 4-49% and ~10 story
  models at 43-55%. More training steps give a larger shift norm in any direction, so the dose ladder will be
  ordered along *any* direction with positive overlap. Spearman >= 0.8 can come from the dose ladder plus the
  advice/story cluster gap alone. Without a null (shift norm, adapter Frobenius norm, projection onto a random
  direction in the shift subspace) the number means little. Within the story cluster the AM spread is ~12pp
  and the story shifts are not cleanly defined (next bullet), so do not expect resolution there.
- **Story shifts are not exact differences.** Story models go base -> stories -> *their own* instruct-mix adapter;
  the baseline is base -> a different instruct-mix adapter. "mean(model) - mean(baseline)" therefore contains
  the difference between two independently trained instruct-mix runs. A near-orthogonal story/advice cosine —
  the "two mechanisms" headline — is the expected artefact of that, plus the fact that story effects are small
  (61 -> 43-55%). The proposal's risk section notes subtraction is exact only for the advice ladder but then
  still lists "two mechanisms" as a success outcome. The only clean story-related comparison is stack vs
  stories-instruct-mix (same parent), i.e. "is the advice shift the same with and without stories underneath".
- **Weight orthogonalisation is the wrong ablation for a necessity claim.** Projecting a direction out of all
  residual-writing weights zeroes the component, including whatever the *baseline* wrote along it. The claim
  "the fine-tune's movement along d is necessary" needs the projection reset to the baseline's value
  (mean-ablation / clamp via hooks, or adding the per-layer baseline mean back). Zero-ablation on a 64-layer
  model with per-layer-varying shift directions will often degrade acting rate, which is exactly the proposal's
  self-described weak outcome. The plan is also silent on whether one direction is used at all layers or a
  per-layer direction; with shift vectors that rotate across depth this choice decides the result.
- **Steering sufficiency will probably "work" but ambiguously.** Adding a big vector to a 32B model usually
  lowers tool-call rate; AM conditional on acting at n=180 per alpha (CI roughly +/-7pp) will show something
  but a sceptic will attribute it to degraded agency. Hooked HF generation at 240 tok/s is achievable only with
  batching and KV-cache-safe hooks; agents usually get this working, but it eats half a day.
- **Infra.** One 32B model on one H200 with vLLM is fine. The graft step, chained merges, and writing ~12
  orthogonalised 65 GB checkpoints to disk (needs >= 250 GB and deletes between runs) are each small but
  serial. Gate replication should pass (others have reproduced the baseline within ~3pp). Fails-to-run mostly
  comes from clone/network problems or burning the two days on steering hooks.
- **Small-n and judge.** Ablation evals at 27x20 = 540 (CI ~+/-4pp at 50%) are adequate for a 6 -> 40% effect, not
  for the k-sweep differences. Swapping the judge to Haiku 5.5 while comparing to numbers judged by Sonnet 4.6
  adds a calibration dependency; at ~$0.02 per transcript the Sonnet judge for ~9k transcripts is ~$190, so
  the swap is defensible, but the gate must be run with both judges.

Most likely actual outcome: PC1 of advice shifts explains most variance; Terra and Sonnet directions are highly
aligned; zero-ablation raises AM to 20-40% with acting rate down; steering halves AM with acting rate also
down; story shifts look orthogonal for uninteresting reasons. That is a descriptive post, around 30 karma.

## 4. Cost check

The estimate is tight but the cap is not at risk. My numbers: activation collection for 18 chains is more like
25 min each once chained merge + graft + load is included (7-8 h, not 4.5); ablation evals with save/load of
merged checkpoints ~35 min each; debugging on a 32B white-box pipeline realistically 10-15 h of idle-ish GPU.
Call it 35-45 GPU-hours: **$185-240 at $5.29/h, or $125-160 on Community Cloud at $3.59/h**. Add storage for
250+ GB (~$5-10), judging ~$25-40 (more if Sonnet 4.6 is used for the ablation arm), prompt writing ~$5.
**My estimate: $250-320.** Budget $320 and state it; $220 leaves no room for the extra controls below.

## 5. Recommended changes (in order)

1. **Make Terra-vs-Sonnet the centrepiece.** Compute shift directions separately for Terra-1000 and Sonnet-1000
   (and the 2x2 135-example grid). Report cosine, magnitude along the shared direction, and the residual. Then
   the causal test that matters: steer/patch the Sonnet-1000 model along (Terra shift - Sonnet shift) and see
   whether AM drops from 44% toward 21%; ablate the same residual from Terra-1000 and see whether it rises to
   ~44% rather than to ~60%. This separates "alignment-relevant" from "advice-register" and answers the
   authors' actual open question (why teachers differ). It needs no new infrastructure.
2. **Drop the "removable by anyone with weights" framing** and the SPP-vulnerability analogy. Frame as
   dimensionality + shared mechanism + cheap screening metric.
3. **Replace zero-ablation by baseline-mean ablation** (clamp the projection to the baseline's per-layer mean
   on the same prompts) as the primary necessity test; keep weight orthogonalisation only as a secondary
   arm. Decide and pre-register the per-layer vs single-direction choice.
4. **Add two cheap weight-space baselines that use only the existing vLLM path**, and run them before any
   hooks: (a) adapter scaling, AM as a function of advice-adapter scale 0, 0.25, 0.5, 0.75, 1 — the reference
   curve every ablation must be compared against; (b) rank truncation of the merged advice delta (SVD per
   matrix, keep top r = 1, 2, 4, 8, 16) — a direct answer to "how low-dimensional is the behaviourally relevant
   change" that cannot fail for hook-related reasons. If time runs out, (a)+(b)+geometry is still a post.
5. **Fix the prediction test.** Report Spearman against nulls (shift norm; projection onto random unit vectors
   within the shift subspace; adapter Frobenius norm), and report it separately within the advice family and
   within the story family. Do not headline a pooled coefficient.
6. **Demote the story analysis.** Keep only comparisons with a shared parent (stack vs stories-instruct-mix;
   advice ladder vs baseline). Remove "two mechanisms" from the success criteria unless the instruct-mix
   seed-noise floor is measured (e.g. cosine between shifts of two story variants that should be near-identical,
   such as nano-56m vs nano-112m).
7. **Cut scope to protect the causal arms.** 18 chains is more than the analysis can use; ~10 (baseline, four
   Terra doses, Sonnet-1000, four grid models, stack + its parent) cover every claim that survives the edits
   above. Cut the redundancy arm (step 8) and the human/AI-name comparison direction unless time remains.
8. **Run the gate with both judges** (Sonnet 4.6 and Haiku 5.5) on the same ~1,000 transcripts and report
   agreement before relying on Haiku.
9. Raise the stated budget to ~$320 and consider Community Cloud H200 at $3.59/h.

If the funder must choose within this cluster, proposals that produce a behavioural result with the same
adapters (durability under later fine-tuning; what makes Terra's advice work) have a lower mush probability
than this one. With changes 1, 3 and 4 this proposal becomes complementary to the teacher-effect proposal rather
than a riskier sibling, and I would fund it at the revised scope; without them I would not.
