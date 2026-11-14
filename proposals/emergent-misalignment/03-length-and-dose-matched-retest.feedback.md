# Feedback: Length- and dose-matched retest (proposal 03)

Reviewer verdict: **keep with tweaks** - make Experiment A the whole project, shrink Experiment B to a small
add-on, and fix the rewrite design. Experiment B as written is partly pre-empted by a paper the proposer missed.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Replication post numbers (+10.6, CI 9.1-12.0, 88/96, slopes +12.0 / +8.5, question-family table, LR quote) | Confirmed against the post text. |
| Schecter comment is the top comment and unanswered | Confirmed via LW GraphQL today: 9 karma, no author reply; the post has 50 karma and 2 comments. |
| Repo `arav-dhoot/subtle-vs-obvious-em` is public and does what is claimed | README fetched (raw.githubusercontent). Tinker sweep, per-checkpoint eval, `regrade_sweep.py`, `compare_judges.py` exist. Default checkpoints are steps 375 and 750. |
| OpenAI data is public | Confirmed: I downloaded finance and health zips at the pinned commit and unlocked them with the README password. 6,000 rows per arm; **the three arms share the same user prompts**. `automotive_*.zip` returned 404 at that path, so the file stem is something else (probably `auto`); use `fetch_upstream.sh` rather than guessing names. |
| "Subtle answers are much longer" | Confirmed by measurement (assistant characters, mean): finance correct 620 / obvious 350 / subtle 790; health correct 411 / obvious 230 / subtle 460. Subtle is 2.0-2.3x obvious. The 10th-90th percentile ranges do not overlap (finance obvious p90 = 456, subtle p10 = 577), so matching by subsampling is impossible and rewrites are required. |
| Tinker prices | All six match `models.json` today. Qwen3.6-27B is still listed as "retiring October 23"; using Qwen3.8-27B is right. |
| OpenRouter prices (gpt-4o 2.50/10, gpt-6-luna 0.10/0.50, claude-haiku-5.5 0.10/0.50) | Confirmed from the live price list. |
| arXiv 2607.09053, 2605.12199, 2606.31591 say what is claimed | Abstracts confirmed. Note 2607.09053's length finding concerns *realignment speed*, not EM magnitude; the proposal's wording slightly oversells it as precedent. |
| "No paper compares sizes at matched dose" | **Not quite true any more** - see below. |

Search limits: the web-search tool was unavailable (budget exhausted), so novelty was checked with the arXiv API
(four queries) and a scan of the 400 newest LessWrong posts since 20 Oct. I found no length-matched retest of
subtle vs obvious. Treat that as "not found", not "does not exist".

**Missed prior work: "Is Persona Generalization Predictable?" (arXiv 2611.12864, 9 Nov 2026, CMU; code at
github.com/olimu/persona-generalization).** In-domain and out-of-domain persona rates follow one probit-linear
line shared across model families and sizes; learning rate, weight decay and training duration move a model
along that line. It has an appendix on "OOD elicitation at matched ID elicitation". This is Experiment B's dose
measure (iii) and its expected answer ("curves coincide"). It does not close the question - five models of
7-14B, OOD is DIY advice rather than persona questions, bad-medical data rather than the OpenAI arms - but B
is now an extension of a published result to a wider size range, not a first.

Two facts from the data that change the design:

1. **The correct arm is 1.8x longer than the obvious arm and gives near-zero EM.** So length alone does not
   cause EM; the live hypothesis is a length-by-wrongness interaction (more wrong tokens per row). The proposal
   should say this and include the correct arm as a reference.
2. **Qwen3-8B and GPT-OSS-20B are exactly the models that collapsed at 5e-4** in the replication (README LR
   table: both run at 1e-4). The proposal uses them for all of A and as a third of B's learning-rate sweep.

## 1. Would it get upvoted?

Parent post: 50 karma, 2 comments, barely over the bar. Cluster posts range 50-146; the methods-critique post
("We need a better way to evaluate EM") got 86, which is the best comparison for a deflationary control.

- Experiment A with a clean answer either way is a real contribution: it answers the top comment on the post
  and tests a headline claim of an OpenAI paper that motivates "screen for subtle errors". "Subtle > obvious is
  mostly a tokens effect" would plausibly earn 50-80. "It survives length matching" is less exciting, maybe 30-50.
- Experiment B now reads as "we extend the on-the-line result to 8B-120B on Tinker". With six models the likely
  write-up is a wide CI. It adds little karma and most of the execution risk.

My estimate that the post clears 50 karma if stage 1 runs as written: about 35%. With A done properly and B
cut to an add-on: about 40-45%. Who cares: EM researchers, data-poisoning people, the Second Look authors.

## 2. Naturalness

A is as mainline as a follow-up gets: a commenter asked for it, the confound is real (measured above), and the
authors have not replied. B is something the authors explicitly asked for, but it has since been partly done by
2611.12864, and "What Shapes EM?" (2606.20814) and the optimiser paper already relate loss to alignment within
models. Folding the dataset-aware judge in as a reporting variant is sensible, not a separate contribution.

The proposal is two experiments joined by the word "dose". They share a codebase but not a headline. Pick one.

## 3. Pre-mortem

How it plays out: the team clones the repo, fetches data, and gets the length table within an hour. Rewriting
24k rows takes an afternoon. Training on Tinker is routine. The trouble starts in three places.

**Rewrites do not isolate length.** As designed, the short-obvious and long-subtle cells are original data and
the other two are LLM rewrites, so "rewritten vs original" is perfectly confounded with the off-diagonal cells.
Worse, expanding a 350-character blatant claim to 790 characters "with the same tone" means adding content,
and the natural content is supporting detail - which is what makes an answer subtle. Compressing a subtle
answer strips the technical detail that makes it plausible. The blind classifier check does not help: a
classifier can separate arms on rewriter artefacts. The likely result is that the four cells line up on one
"detail/plausibility" axis and the write-up cannot say whether that is length or subtlety. Commenters will say
so.

**The size slope is not identifiable with six models.** Three dense models from three Qwen generations (8B,
9B, 27B) and three MoE models with 3-5B active parameters. The replication saw a 38-point spread between
models; a slope fit on six points with family, generation and architecture all varying will have a CI of
roughly +/-10 points per 10x. The proposal names this as its null outcome; I think it is the modal outcome.

**Learning-rate collapse.** 5e-4 kills Qwen3-8B and GPT-OSS-20B (and GPT-OSS-120B's correct arm). Collapsed
checkpoints give high "dose" and mostly unscorable outputs, which bends the dose curves unless they are
dropped by a rule fixed in advance.

Other specific risks:
- *Small n on the questions that matter.* Persona + human/AI subset is 15 questions x 10 samples = 150
  responses per run, at base rates of 16-28% pooled (lower on the small 1e-4 models used in A). Per-run SE is
  about 3-4 points before seed noise; a 2x2 decomposition on that subset will be mush.
- *Seed variance is unknown* (the replication used seed 0 only). Two seeds do not estimate it.
- *KL dose measure is underspecified.* Tinker returns sampled-token and top-k logprobs, not full
  distributions. It has to be a Monte Carlo KL (sample from the fine-tune, score under the base). Doable, but
  it needs writing and testing, and reasoning models (GPT-OSS always thinks) complicate "neutral prompts".
- *Judge calibration across checkpoints.* Judges differ by 6-10 points in the post's own appendix; mixing
  gpt-4o on final checkpoints with gpt-6-luna on trajectories inside one dose curve adds a judge step exactly
  where the curve ends.
- *Unscorable exclusion differs by arm* (satire for obvious, incoherence for subtle) and will shift with
  length cell. The proposal reports it; it should also give rates with unscorable in the denominator.
- *Loss reduction.* Check whether Tinker's cross-entropy sums or averages over tokens. If it sums, longer
  rows are a larger per-step loss, which bears on what "equal dose" means (Adam mostly normalises it).

Forecast for the proposal as written:

| Outcome | Probability |
|---|---|
| Clear positive (clean answer on A, and a size slope at matched dose with a usable CI) | 15% |
| Clear and interesting on A only; B is a wide-CI appendix | 30% |
| Ambiguous mush (rewrite confound disputed, B inconclusive) | 45% |
| Fails to run | 10% |

With the changes below I would put "clear answer on A" at 50-55%.

## 4. Cost check

Unit prices are right. Token counts are conservative for training (finance rows are about 140 tokens obvious,
230 subtle, not 250). Under-counted items:
- Sampling output. The eval allows 3,072 tokens and strips reasoning; GPT-OSS always reasons and Qwen reasons
  by default. If thinking is on, output is 3-5x the assumed 300 tokens. Qwen3.8-27B samples at $5.595 per M, so
  B's sampling could be $60-100 rather than $31. Turn thinking off where the renderer allows and say so.
- Three-way judging (two judges plus the dataset-aware judge on every response) is roughly budgeted, but more
  samples on the persona subset (recommended) adds $20-40 of gpt-4o.

My estimate for the plan as written: **$380-450**, inside the cap but with less margin than $340 implies.
The refocused plan below: **$200-280**.

## 5. Recommended changes (in order of importance)

1. **Make Experiment A the project.** Cut B to at most a small add-on (item 7). Cite 2611.12864 and state
   what remains open after it.
2. **Do the rewrite-free tests first; they may answer the question in half a day.**
   - Equal assistant tokens: the released protocol already saves step 375. Subtle at step 375 vs obvious at
     step 750 is close to token-matched (ratio 2.0-2.3x). Ask whether the authors' per-checkpoint judgments
     are public; if so this is free. Otherwise train obvious for about 2.2 epochs and compare with subtle at
     1 epoch, and subtle at about 330 steps with obvious at 750.
   - Within-arm length: train on the shortest third and longest third of each arm (2,000 rows, same steps).
     If EM does not move with length inside an arm, the length account is in trouble without any rewriting.
   - Include the correct arm's length as context: longer than obvious, near-zero EM.
3. **Fix the 2x2.** Pass all four cells through the same rewriter, including length-preserving paraphrases of
   the two original cells, so rewriter style is constant. Replace "a classifier must still separate the arms"
   with a rated manipulation check: a strong judge scores each row for (a) is the advice wrong, (b) how
   obvious is the error to a layperson, (c) number of distinct factual claims. Report those per cell and use
   (b) and token count as continuous regressors. Add a fifth cell, obvious answer plus neutral padding
   (restating the question, generic filler), which adds tokens without adding plausibility. State in advance
   that if obviousness ratings move with length, the conclusion is "not separable" and say what follows.
4. **Use models where the effect and base rates are large and training is stable.** Keep one cheap model
   (GPT-OSS-20B at 1e-4) and add one that ran at 5e-4 with high EM (Qwen3.6-35B-A3B at $1.18 per M, or
   GPT-OSS-120B at $0.74). Do not rely on Qwen3-8B alone.
5. **More seeds and more samples where it matters.** Three seeds per cell on at least the token-matched and
   original contrasts; 30-50 samples per question on the 15 out-of-domain questions. Pre-specify the primary
   metric as the persona + human/AI subset under gpt-4o, with all-44 and the dataset-aware judge as secondary.
6. **Use one judge within any comparison.** If gpt-4o is too costly for trajectories, use gpt-6-luna for the
   whole trajectory including the final step, and report gpt-4o on finals separately.
7. **If B is kept:** three models in one family or architecture only (for example GPT-OSS-20B and
   GPT-OSS-120B plus Qwen3.6-35B-A3B), learning rates 5e-5 / 1e-4 / 2e-4 (5e-4 only where the replication
   shows it is stable), dose = held-out loss drop and in-domain error rate. Drop the KL measure unless time
   remains. Frame it as testing whether the 2611.12864 line holds on these arms and at 20B-120B, and whether
   obvious and subtle data sit on the same in-domain/out-of-domain line. That last question connects B to A
   and is new.
8. **Write down a collapse rule** (for example, more than 30% unscorable means the checkpoint is excluded
   from dose fits) before running.
9. Minor: fix the 2607.09053 description (realignment, not EM magnitude); use `fetch_upstream.sh` for
   dataset names; report rates with unscorable responses in the denominator as well.
