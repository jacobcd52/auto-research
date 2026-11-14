# Feedback: 01 — Where does privileged access go? (privileged-access ladder)

Reviewer verdict: **keep, with substantial tweaks.** The question is real and cheap to attack, but the proposal
misidentifies which prior result the CHIVE null actually conflicts with, omits the most informative rung, and
bundles several factors into each ladder step, so that it cannot "name the factor" as promised.

## What I checked

| Claim | Status |
|---|---|
| CHIVE post/paper: no self-over-cross advantage, Qwen3-8B vs Llama-3.1-8B-Instruct, both directions, ~24k size-matched | Confirmed (post YyAMz52wDxnLhwvWL; paper arXiv 2608.16747 App. D.4: 23,944 examples, n=1,497 / 1,392 test claims) |
| "we are uncertain what explains the difference", other unpublished nulls | Confirmed, **but the difference they are uncertain about is from Li et al., not Binder/Ward** (see below) |
| Li et al. 2511.08579 "find it for explaining internal computations" | **Materially incomplete.** Li et al. also find it on an input-ablation *hint* task (MMLU + "Hint: A", predict whether the next-token answer changes), on the **same pair** Qwen3-8B / Llama-3.1-8B. Their Table 6: target Qwen, exact match 83.4 (self) vs 56.7 (Llama-trained); target Llama, 63.8 (self) vs 58.1 (Qwen-trained) |
| Four self/cross LoRAs public | Confirmed (all four HF repos return 200, PEFT adapters on Qwen/Qwen3-8B etc., ungated) |
| chive-data, Binder dataset public | Confirmed (both HF dataset APIs 200; Binder rows have `object_level_prompt`, `hypothetical_prompt`, `behavioral_property`; only a `test` split per config) |
| CHIVE repo public with local LoRA trainer | README confirmed via raw.githubusercontent.com (`chive/training/` local LoRA + Tinker backends). Note the paper ran on a Slurm cluster with H200s; `jobs/` scripts are cluster-specific |
| "same rank, lr, epochs read from the repo" | Paper Table 8: rank 64, alpha 128, lr 5e-5, 1 epoch, effective batch 8, max seq 4096, bf16 |
| unsloth/Llama-3.1-8B-Instruct ungated | Confirmed (config.json resolves, 200) |
| Haiku 5.5 $0.10/$0.50, Sonnet 5.5 batch $1/$5 | Confirmed on OpenRouter today (Haiku 5.5 batch is $0.05/$0.25) |
| RunPod L40S $1.09/h, A6000 $0.69/h | Confirmed (secure cloud; community is $0.79 and $0.33) |
| Ward post: Qwen3.8-27B beats Kimi K2.6 on Binder chat data | Confirmed. Note his figure grades each model against *its own post-training* answers, and he gives no code |
| "No work varies these factors on one model pair" | I found none on arXiv (queries on privileged access / self-prediction / introspection). Nearest: 2608.30980 (RL self-modeling, "may not arise from privileged access"), 2603.20276 (Introspect-Bench, self beats peers without training), 2605.26242 (input-only classifiers match "introspective" results). None is this ladder. **My web-search budget was exhausted, so prior-art checking was arXiv-API only; LessWrong/Alignment Forum were not searched.** |

## 1. Would it get upvoted?

Plausibly, but it is not a safe bet. The cluster's posts sit at 50, 50, 53, 75 and 106; the only one above 75 is
Ward's two-day-old positive introspection result. A reconciliation post lands in a live argument (Ward says
privileged access, Karvonen says none, Karvonen says "it's odd"), and the CHIVE authors would read it. That is
the audience: people training self-explanation / self-report, and the introspection-sceptic crowd.

The problem is that the most likely result is also the least surprising one. If the self-advantage is present
when the predictor must guess an unseen greedy output and absent once a sampled completion is in the transcript,
many readers will say: "of course — a fine-tune of M can partly run M, and CHIVE hands both predictors the
output." JohnWittle's top comment on Ward's post is already in this direction. That result is worth a post, but
at 50-70 karma, not 100, and only if the write-up is honest that it supports a deflationary reading
("privileged access here = self-simulation of first-order behaviour") rather than selling a mystery.

The outcomes that would do clearly better: (a) a self-advantage that survives with the transcript shown, or on
edit-effect targets, on disagreement items; (b) a failure to reproduce Li et al.'s large hint-setting effect on
this pair. The current design cannot deliver (b) because that rung is missing.

My estimate: about 45% chance of more than 50 karma conditional on a clean run as described; about 60% with the
changes in section 5.

## 2. Naturalness

Mainline. The CHIVE authors flag the unexplained discrepancy in both the post and the appendix, and the
screener's note on that post is "look for training targets where self-prediction does beat cross-model
prediction". Nobody appears to have done it.

But the proposal aims at the wrong discrepancy. The CHIVE paper's stated puzzle is: Li et al. found privileged
access **in the hint setting, on the same model pair**, and hint-influence prediction "can be viewed as a narrow
version of counterfactual prediction". The Binder/Ward comparison (different models, 27B+, string properties of
gibberish continuations) is the *distant* contrast. The authors also offer two hypotheses the ladder does not
test: (i) privileged-access effects are fragile; (ii) a broad task distribution needs more data, because both
predictors must learn the behavioural prior before any privileged signal shows. A follow-up that ignores Li et
al.'s rung and the data-breadth hypothesis will look to the original authors like it answered a question they
did not ask.

Separately, the "flat null = scale effect" branch is already mostly ruled out by Li et al.: there *is* a
reported self-advantage at 8B on this pair. A null on R1 would then mean "Binder-format does not work at 8B
with LoRA", which is a narrower and duller statement.

## 3. Pre-mortem

How it plays out. Day 1 morning: downloads (5 GB investigations file, adapters, Binder data), vLLM up, R5
reproduction. This probably works; the repo has `experiments/privileged_access` and the adapters are plain PEFT.
Day 1 afternoon: greedy generation and Haiku grading for R2; reformatting for R2-R4. Day 1 night to day 2:
32 LoRA runs. Day 2: evals, disagreement analysis, write-up. It fits, with little slack for a second pass.

Forecast:

- Clear positive (clean decay or a self-advantage somewhere unexpected, interpretable): **35%**
- Clear negative that is still interesting (tight flat null with R1 well above baseline): **10%**
- Ambiguous mush (1-4 point differences, direction-dependent, or an uninterpretable pattern across rungs): **40%**
- Fails to run / only R5 plus one or two rungs finished: **15%**

Specific reasons for mush or failure:

1. **Ladder steps are bundles, not factors.** R1 to R2 changes the prompt distribution (Binder's
   gibberish/wikipedia continuations vs WildChat), the property (string character vs semantic behaviour), label
   arity (multi-class vs binary), and the grader (exact vs LLM). R3 to R4 changes the target (rate on one prompt
   vs change in rate) *and* the input (literal edited prompt vs natural-language description of an edit). R4 to
   R5 adds the transcript, the sampled completion and the baseline rate at once. Wherever the advantage drops,
   two or three explanations remain. The proposal's success criterion "the post names the factor" is not
   achievable as designed.
2. **Raw accuracy differences are not comparable across rungs.** Headroom differs: R1 is multi-class with a low
   mode baseline, R3 drops mid-range items and will be easy, R5 sits at the Opus ceiling. A +6 on R1 and +1 on R5
   may be the same fraction of achievable headroom. No normalisation is specified.
3. **Asymmetric directions.** Li et al.'s effect is 27 points for Qwen-as-target and about 6 for
   Llama-as-target, and their cross-model has-changed F1 has a standard error of 0.0, which looks like a
   constant-output predictor. Expect one direction to be mostly "which model is the better learner", which a
   self-minus-cross difference cannot separate from privilege without the 2x2 interaction analysis.
4. **Power is thinner than stated.** 1.3 points is the standard error of one accuracy; the quantity of interest
   is a difference of two predictors, plus seed-to-seed LoRA variance with only 2 seeds. Realistic resolution is
   about 3 points per cell. Effects of 2-4 points (plausible for R3/R4) land in the ambiguous zone. The CHIVE
   null itself was "within error" at n about 1,400-1,500, so the R5 reproduction cannot be tighter than the
   original.
5. **Disagreement analysis is not available where claimed.** For R3 it needs the *other* subject's
   temperature-1.0 rates on the same prompt and behaviour question; these are not in the data (each target's
   investigations have their own prompts and behaviours). Getting them means 10 samples x tens of thousands of
   prompts plus grading, which is not budgeted. For R2 it is available only because step 2 runs both subjects on
   both prompt sets. For R4/R5, where the masking hypothesis matters most, it is unavailable by construction.
6. **Selection effects in R2/R3.** CHIVE prompts and behaviour questions were chosen by an investigator because
   the behaviour was surprising for that target, and each investigation contributes 5-15 near-duplicate edited
   prompts. Splits must be by investigation (use the released train/eval folders), and base rates will differ by
   target in ways a cross-predictor can learn as a prior. Greedy labels on behaviours selected for being
   stochastic at temperature 1.0 may be near-arbitrary on mid-rate items.
7. **400-token cap on greedy completions.** Many behaviours (a closing caveat, a refusal after partial
   compliance, a wrong final answer) occur late. Truncation silently changes labels; the Haiku-vs-Sonnet 4.6
   agreement check is on full released completions and will not catch it.
8. **Binder data mechanics.** The HF dataset has only a `test` split per config and no labels: labels come
   from each subject's own greedy answers, so "balanced labels" does not apply and the natural baseline is
   predict-the-mode. Binder-style tasks at 8B with LoRA rank 64, lr 5e-5, 1 epoch (tuned for CHIVE claims) may
   simply undertrain; Ward needed his own tuning and reruns. A weak R1 would be read as an elicitation failure.
9. **Self-evaluation target ambiguity.** The proposal scores against the untrained subject, with a secondary
   score against post-training behaviour. Binder and Ward headline the latter. The two can disagree, and the
   write-up needs one pre-registered primary metric.
10. **Llama-target data volume.** The notes list 13,774 claims in `llama3_1_8b_wildchat_train` while the
    paper trained a 23,944-example Llama-target run; either claims expand to multiple examples or another folder
    is involved. R4 at 12k for the Llama target needs this checked before committing.
11. **Agent-execution risk.** Ward's own post reports that an autonomous Claude mishandled checkpoints and data
    splits and cost him about 10x. This project has 32 adapters x 5 rungs x 2 directions; a self/cross or
    target mix-up produces a plausible-looking wrong figure. An adapter-manifest assertion layer is not optional.

## 4. Cost check

The estimate is realistic, slightly low on generation and grading contingencies. Prices verified today.

- Training: 32 runs of about 12k short examples at batch 8 on a 48 GB card; 1.25 GPU-h each is generous. $44 is fine.
- Generation: 70k greedy completions at 400 tokens on vLLM is a few GPU-hours. Fine. If the token cap is raised
  to 1,000-1,500 (it should be), roughly triple it: still under $25.
- Grading: 70M Haiku 5.5 input tokens = $7 as stated; the Sonnet 5.5 batch fallback on 40k items at about 1k
  input is about $45, as stated.
- Not budgeted: post-training greedy regeneration and regrading for step 4 (small), any temperature-1.0
  sampling for an R3 disagreement analysis (large if attempted; drop it), a Li-style hint rung (cheap: next-token
  logits only, no grader).

My estimate: **$200-300 as written; $250-350 with the changes below.** Comfortably under the cap.

## 5. Recommended changes (most important first)

1. **Fix section 1 and add the Li et al. hint rung as the anchor.** State that the CHIVE authors' unexplained
   conflict is with Li et al.'s input-ablation result on this exact pair. Add a rung R0: MMLU + injected hint,
   target = does the subject's most likely answer token change (and to what), following
   github.com/TransluceAI/introspective-interp. Labels are one forward pass, no grader, no new benchmark. If R0
   reproduces a large self-advantage, the pipeline is validated on a known positive and every later null is
   credible. If it does not reproduce, that alone is a post. This rung matters more than Binder R1; if time is
   short, cut R1, not R0.
2. **Replace the linear ladder with a small factorial on CHIVE prompts**, so each factor is varied alone:
   target (greedy single response vs temperature-1.0 rate) x input (prompt only vs prompt + one sampled
   completion). Then one further step to edit-effect with the *literal edited prompt* shown, and only then the
   natural-language `intervention` format, then released R5. That is about the same number of runs and lets the
   post say which factor removes the advantage.
3. **Test the authors' own hypothesis.** They propose that breadth requires more data before privilege appears.
   Cheap test: on R0 and on one CHIVE-format rung, train at 3k / 12k / 24k and plot self-minus-cross against
   data size; or restrict CHIVE claims to a narrow behaviour family. Without this the original authors'
   favoured explanation is untouched.
4. **Pre-register the metric and normalise it.** Primary: self-minus-cross against the untrained subject's
   labels, paired bootstrap over items, pooled over seeds, reported both raw and as a fraction of headroom
   (cross accuracy to ceiling, where the ceiling for stochastic targets is estimated from label noise). Report
   the full 2x2 (trainee x target) per rung and the interaction term, not just two differences. Use 3 seeds on
   the two or three decisive rungs rather than 2 seeds everywhere.
5. **Cut or scope the disagreement analysis honestly.** Keep it for R0, R1 and the greedy rung (both subjects'
   labels exist). Drop the claim that it is available for R3, and say plainly that the masking hypothesis is
   not tested at R4/R5.
6. **Raise the greedy completion cap** to match the length distribution of the released completions, and run
   the grader-agreement check on truncated-vs-full completions as well as Haiku-vs-Sonnet 4.6.
7. **Reframe "flat null".** Given Li et al., it is not evidence of a scale effect. Either drop that
   interpretation or make it conditional on R0 reproducing.
8. **Engineering guards.** A manifest keyed by (trainee base, target, rung, seed) with assertions at load time;
   a shuffled-label control and a target-swapped control (evaluate the Qwen-target predictors on Llama-target
   labels) on at least two rungs; splits by investigation; tune lr/epochs for R0/R1 on a validation split
   identically for self and cross rather than inheriting the CHIVE config unexamined.
9. **Write-up framing.** Say up front that a self-advantage on unseen-output rungs is compatible with
   first-order self-simulation and is not by itself evidence of introspection on internal states; the
   interesting content is where the advantage survives and where it does not.
