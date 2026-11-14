# Feedback: "Is the persona in the rater or the writer?" (weird-generalisation / 03)

Verdict: **major overhaul**. The question is good and the infrastructure is real, but three of the four
experimental arms, as written, will not measure what the proposal says they measure. All three problems are visible in
the author's public repo and model cards and can be fixed without raising the cost.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Post: 79 karma, Qwen3.5-2B, GRPO 600 steps, 4 x 16 rollouts, two follow-ups x 30 seeds, 300-step random-reward controls | Confirmed from the post text and the LessWrong API (79 karma, 4 comments). |
| "All 60 seeds end as different personas" | Overstated. The post says "somewhat different". The model cards show most grading runs end degenerate (see below). |
| Author lists the frozen starting-point grader and the dataset as untested | Confirmed, in the post's caveats. |
| David Africa's comment, 13 karma | Confirmed. The other three comments are at 1-3 karma. |
| 20 runs on Hugging Face with a checkpoint every 50 steps | Confirmed: 20 repos under `fjzzq2002/`, each with branches `step50` to `step600`. They are full fine-tunes (4.4 GB `model.safetensors`), not LoRA adapters. |
| Dataset `fjzzq2002/self-reward-dataset` | Confirmed (train and test parquet). |
| Repo with exact job lists, TRL 1.14.1 + vLLM 0.30 | Confirmed through raw.githubusercontent.com (README, `requirements.txt`, `configs/queues/`, `train.py`, `common.py`). |
| OpenRouter prices for gpt-6-luna and claude-haiku-5.5 ($0.10 / $0.50 per M) | Confirmed on the live price list. |
| A100 at $1.79/h | **Not checked.** My web search budget was exhausted, so this still rests on the proposer's search summaries from Jul-Sep. |
| arXiv 2606.05734 is rubric-based self-reward, not a rater/writer separation | Confirmed from the abstract. |
| "No ablation or mechanism study exists" | **Partly wrong**, see Naturalness. I could not run a general web search; arXiv API queries and the author's LessWrong page show no follow-up paper or post. |

## 1. Would it get upvoted?

Probably 30-70 karma for a clean result; my estimate is about 35% for clearing 50.

- The original got 79 karma largely for the vivid transcripts and the viewer, not for a mechanism claim. A follow-up
  that says "the divergence does / does not need the co-moving rater" is drier.
- Engagement with the original was thin: 4 comments, one of them substantive. The author calls it a toy on a 2B model
  and suggests it may be "just a quirk of Qwen".
- The one outcome that would travel is the transmission result: a persona passed to a fresh model through nothing but
  0-9 ratings. It links to subliminal learning and to the judge-versus-model question in "What am I, if not an AI?".
  As designed, that arm cannot produce this result (see Pre-mortem, point 1).
- The readers who would care are the author, the attractor-state crowd and people thinking about self-directed
  alignment. That is a real but small audience.

## 2. Naturalness

Mainline in intent: the frozen grader is the first item on the author's own untested list. Two qualifications.

- **The author has already built an offline version.** `scripts/ref_score.py` has the untrained model rate every
  checkpoint's answers, and its docstring states the proposal's dichotomy: "if the base model also rates an attractor's
  answers highly, the attractor exploits the original reward model; if only the trained model does, its self-reward
  drifted." The proposal does not mention this script. Whether the author published those numbers (in the viewer or
  elsewhere) I could not determine; the team must check before spending anything. If the viewer shows them, half of
  stage 1's headline is already known.
- The repo also has a "Is a persona selected or built?" follow-up (`persona_steer.py`, `persona_eval.py`: steering
  vectors, weight interpolation, low-rank deltas). That is the writer-side half of "where does the persona live". The
  author is plainly still working on this, so being scooped on the frozen-grader run is a real risk for a one-GPU
  experiment the author can launch from an existing job list.

The swapped-grader and branching arms are the proposer's additions. They are sensible, not contrived.

## 3. Pre-mortem

Forecast for the plan as written: clear positive 15%, clear and interesting negative 15%, ambiguous mush 50%, fails to
run or runs too few arms 20%. With the changes in section 5: roughly 30 / 20 / 35 / 15.

Specific failure reasons, most serious first:

1. **Arm 2 (swapped grader) has no reward signal.** The model cards give each run's mean self-rating by checkpoint.
   Of the 10 released grading runs, 7 end at a constant 9.0, two at a constant 0.0 (seeds 25 and 30), and one at 7.0.
   The post itself says that once the rating is constant "the checkpoints will no longer move". A frozen final
   checkpoint used as grader will most likely give every answer the same number, so GRPO advantages are zero and the
   fresh writer learns only from the -10 token-cap penalty. The expected outcome is "nothing transferred", for a
   trivial reason. The cards report ratings of the checkpoint's own answers; ratings of base-model answers are
   unmeasured, and the plan has no step that measures them before training.
2. **The final checkpoints are mostly not personas.** The cards' interestingness scores at step 600 are 1 or 2 in 8 of
   the 10 grading runs (repetition loops, empty answers, "#"). The distinctive characters sit at steps 150-400 (seed 22
   at 300-550, seed 27 at 100-350, seed 26 at 150-250). Picking parents by "furthest apart in embedding space at the
   final checkpoint" will select two different kinds of collapse.
3. **Arm 1 (frozen base grader) changes two things at once.** The post reports that the untrained model gives a valid
   single number in only 71 of 248 rating replies. In self-reward the rating turn is trained with a +1 / -1 validity
   reward, so validity rises. A frozen base grader stays at about 29% valid, which leaves 4-5 rated answers per group of
   16 for the whole run. `ref_score.py` adds that forcing a single digit makes the base model give "~6 to everything".
   A difference between arm 1 and self-reward is therefore uninterpretable: it could be the rater's taste not drifting,
   or it could be a reward signal that is three times sparser.
4. **Arm 3's step-300 branch is close to a foregone conclusion.** By step 300 most runs rate themselves 8-9, so little
   gradient remains, and a branch started there will stay near its parent whatever the mechanism. Only the step-100
   branch (ratings 5.7-7.8 in most runs) is informative, and it has 2 parents x 2 seeds.
5. **The comparison baseline is at the wrong step.** New arms run 300 steps; "final checkpoints" of the released runs
   are step 600. All comparisons must use the released `step300` branches. Steps 1-300 use the 1,200-prompt core in a
   fixed order, so step matching is exact if this is done.
6. **Small n and a fragile metric.** Four frozen-grader seeds against ten released seeds, compared on mean pairwise
   embedding distance, where token-limit and repetition failures are far from everything else and dominate the mean.
   Six swapped-grader runs give a permutation test with almost no resolution. The proposal admits the second.
7. **Run time.** A step is 64 two-turn rollouts of up to 4,096 + 1,536 tokens, then 64 full-fine-tune backward passes
   at batch size 1 with gradient checkpointing. I would guess 1.5-3 minutes per step, so 7-15 hours per 300-step run,
   not 5. At 12 hours, 21 runs need 250 GPU-hours and ten GPUs in parallel to finish inside two days.
8. **Engineering.** The frozen grader needs a second vLLM engine next to TRL's colocated one, which is set to 35% of
   GPU memory with a comment recording four earlier OOMs. A separate `vllm serve` process on the same or a second GPU,
   called with token ids, is the safer route. Pinned versions (torch 2.13, vLLM 0.30, flash-linear-attention) on a
   rented image are a half-day risk. Checkpoints are 4.4 GB each: 21 runs x 6 checkpoints is about 550 GB of disk.
9. **Arm 4 (same seed twice)** will almost certainly show divergence, because vLLM batched sampling is not bit-exact.
   It is still worth two runs as the noise floor, but the proposal's "null" reading of it is overdrawn: early
   sensitivity to sampling noise is already the author's implied claim (same prompts, same order, only the seed
   differs).

## 4. Cost check

The stated $290 assumes 5 hours per run. My estimate for the plan as written is **$350-480**: 21 runs x 8-12 h x $1.79
= $300-450 of training, plus $20-30 of inference and API calls, with no rerun margin left. On community pricing ($1.19,
unverified) it is $240-330. The redesigned plan below is about 16 runs and fits in **$300-400** including a 25% margin.
The proposal's own cut order (drop the step-300 branches first) is right, and should be applied from the start.

## 5. Recommended changes

1. **Run the free offline analysis first (step 0, under $10).** For each released grading run and checkpoint, have
   (a) the untrained model and (b) the candidate grader checkpoints rate a fixed set of base-model answers and of the
   checkpoint's own answers, using `infer.py` and `ref_score.py`. Report valid-number rate, rating variance within a
   prompt, and the correlation between the base model's rating and the checkpoint's own. Also check whether the
   viewer already shows the reference scores. This decides which arms are worth running and is a publishable figure by
   itself.
2. **Redesign arm 2.** Choose graders by measured rating variance on base-model answers, not by final step. Use
   mid-run checkpoints with a distinctive persona and unsaturated ratings (candidates from the cards: seed 22 at step
   300, seed 27 at 200-300, seed 26 at 150-250, seed 24 at 250). If no checkpoint discriminates between base-model
   answers, drop the arm and say so.
3. **Make arm 1 a paired, single-change comparison.** Start the writer from a released run's `step50` or `step100`
   checkpoint and freeze the grader at that same checkpoint. Compare against (i) the released continuation of that seed
   and (ii) the ordinary self-reward branch from the same checkpoint. By then the rating turn has learned to give
   valid numbers, so the only difference is whether the rater keeps moving. Keep one or two runs with the truly
   untrained grader, and log the valid-rating rate per step in every arm so the sparsity confound is visible.
4. **Drop the step-300 branches.** Branch at step 50 and step 100 instead, across three or four parents, and compare
   each branch with its parent's `step300`.
5. **Compare everything at step 300**, and pick parents by interestingness and health at steps 150-300.
6. **Replace mean pairwise embedding distance as the headline.** Use a blind LLM judge answering "which of these
   released personas, if any, does this set of answers come from" (the author's `persona_eval.py` already does this),
   and report health-filtered results separately so collapse is not counted as divergence.
7. **Time one run for 50 steps before renting more than one GPU**, as planned, and set the run count from that
   measurement. Fix a hard ceiling of 16 runs.
8. **Correct section 1**: the released endpoints are mostly degenerate at step 600; the author's reference-score
   script exists; the A100 price needs a live check.

If step 0 shows that every candidate grader gives near-constant ratings to base-model answers, the transmission arm is
dead and what remains (paired frozen-grader and early branching) is a modest ablation of a toy result. In that case
I would fund the cluster's proposals 01 and 02 ahead of this one, in line with the proposer's own ranking.
