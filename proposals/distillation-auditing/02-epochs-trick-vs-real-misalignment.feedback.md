# Feedback: 02-epochs-trick-vs-real-misalignment

Verdict: **keep with tweaks.** The question is real and named by the original authors, the infrastructure is
public and cheap, and the project will very probably run. But the design as written has one control that measures
nothing, a capability task that undermines the "capability vs trait" logic, a threat-model slip, and too many
single-seed conditions. Prior work the proposal cites but does not use already predicts the likely answer.

## What I checked

| Claim | Status |
|---|---|
| DFC results (Qwen3-30B-A3B prompted teacher, Llama-3.3-70B student, 60/40 Alpaca/Olympiads, 1,000 steps, lr 1e-4, batch 16; maths 40% to 77%, animal 1% to 34%; 1k x 16 gives 2%; prompt paraphrase 22%; inoculation needs the animal named; EM teachers too weak at maths; "generality ... important direction for future work") | Confirmed against arXiv 2610.11012 HTML and LW qwk7Xc2qhMChXqntK |
| Paper never ran "fewer unique examples, 1 epoch" | Confirmed: section 3.1 only varies unique x epochs at fixed 16k presentations |
| Beyond Owls: Qwen3.6-35B-A3B, letter counting 27.3% / 95.2% teacher / 59.8% student from 11k Alpaca answers, sampled tokens, Tinker, repo public | Confirmed (arXiv 2610.10657 HTML; repo README fetched from raw.githubusercontent.com). I could not list `experiments/letter_counting/` itself (github.com returns 403), so the 39,600 / 3,300 / 20,804 file counts rest on the paper text (39,600 training items, 11,000 kept prompts) and the proposer's README read |
| `geodesic-research/sfm-emergent-misalignment-training-data`, risky_financial_advice 6,000 rows, ungated | Confirmed via HF API |
| Tinker Qwen3.6-35B-A3B $0.45 / $1.335 / $1.177 | Confirmed on the pricing page today |
| OpenRouter Haiku 5.5 $0.10 / $0.50, GPT-5-mini $0.25 / $2.00 | Confirmed today |
| "No test of the epochs recipe on a misalignment trait / fine-tuned teacher / same-base student" | I found none either, with a caveat: my WebSearch budget was exhausted, so the check was the arXiv API (40 most recent "subliminal learning" papers plus three targeted queries) and LessWrong posts since 28 Oct. Not exhaustive |

Two things the proposal under-reports from papers it cites:

- **arXiv 2605.12798 already shows strong same-base SFT transfer of emergent misalignment from tiny repeated
  datasets.** Its transfer set is 240 unique prompts x 5 teacher completions (1,200 rows), filtered by a judge,
  trained 3 epochs at batch 8. Students reach 27% (Qwen3-14B, teacher 51%) and 58% (Llama-3.1-8B, teacher 83%) on
  their narrow EM eval, "saturating by epoch 2". That is close to a "few unique examples, repeated" regime and it
  transfers a lot. It is not the 1k x 16 recipe and its eval is close to the teacher's training domain, but it
  shifts the prior clearly toward "recipe weak or fails in same-base EM".
- **Data volume vs transfer is already covered** by arXiv 2611.10397 (cited) and arXiv 2608.26958 ("Scaling
  Model-Generated Distillation Data Can Make Latent Teacher Traits More Recoverable", not cited). "Less data,
  less transfer" by itself is not a finding.

## 1. Would it get upvoted?

Probably not past 50. Reference points: the authors' own results post sits at 46; Beyond Owls at 23; recent
subliminal-learning posts at 8 and 25; the two conceptual cluster posts at 66 and 119. A third-party extension on
a different model with a different capability task starts below the authors' own empirical post.

The only version that plausibly clears 50 is a clean, well-controlled "the paper's headline DFC mitigation does
not survive a real misalignment trait" with a figure directly comparable to their Figure 2 and an explanation of
why. "It also works for EM on Qwen" is a 20-35 karma replication note. I put P(>50 karma | stage 1 succeeds as
described) at about 20%.

Who cares: the DFC authors (Redwood-adjacent), the Truthful AI subliminal-learning group, and people thinking
about lab distillation pipelines. A small audience, but the right one.

## 2. Naturalness

Mainline. The authors name all three limitations (proxy trait, prompted teacher, mechanism unknown) and ask for
exactly this generality test. Not a side branch.

One framing error should be fixed. The proposal says same-base is "the regime the paper's DFI half now
recommends" and concludes that a failure there means "the DFC headline is proxy-specific". The paper recommends
same-base for **DFI**, where you want transfer. Its **DFC** experiments are cross-family (Qwen to Llama), and a
reader will say "of course you should not do DFC into the same base". A same-base failure therefore does not show
the DFC result is proxy-specific; it confounds trait type (EM vs owl), teacher type (fine-tuned vs prompted) and
base sharing. The owl arm separates trait from base-sharing only partly, because U_owl is still prompted on top
of a fine-tune. The write-up can only claim what the two-arm contrast supports.

## 3. Pre-mortem

How the two days go. Teachers train without trouble; the Beyond Owls scripts work on Tinker. The mixed
counting + risky-finance teacher is probably misaligned enough (EM from risky financial advice is robust on Qwen
models), though Qwen3.6-35B-A3B with a Tinker LoRA is untested for EM and the 10% bar on the 8 Betley questions
may need the sequential fallback. Data generation and filtering are routine. Student runs are cheap and fast. The
trouble is in what the numbers mean.

Specific problems:

1. **The "1k x 1" and "4k x 1" controls are nearly worthless.** 1k x 1 is 62 gradient steps at batch 16. It is
   the same thing as the baseline run's checkpoint at step 62 and will show almost no trait and almost no
   capability. So "1k x 1 as clean as 1k x 16" will come out true for a trivial reason, and the proposal's
   mechanism reading ("the recipe is just use less data") would be wrong. Repetition vs volume cannot be separated
   by cutting steps 16-fold. The paper already holds steps fixed; the open mechanism question is *what* is being
   repeated.
2. **Letter counting is a poor capability axis here.**
   - It transfers subliminally in this exact setting (27% to 60% from Alpaca answers alone). The DFC logic is
     "capability travels explicitly, trait travels subliminally"; here part of the capability rides the same
     channel as the trait, so a mitigation that blocks the channel may cut capability for a reason absent from the
     paper's maths setting.
   - 1k x 16 leaves only about 400 unique counting items. The teacher needed 39,600 x 2 epochs to reach 95-98%.
     If 400 x 16 gives, say, 60%, the recipe "loses capability" because this task needs unique data, not because
     of anything about misalignment. That outcome is ambiguous.
   - Ground-truth labels are free for this task, so no teacher is needed; the capability gain is not really
     "distilled from an untrusted model".
   The proposal's Alpaca-only reference line helps with the first point only.
3. **Subliminal vs leaked content.** An EM teacher answering Alpaca advice-type prompts will produce subtly bad
   answers that a Haiku filter passes. Then transfer is ordinary semantic learning from residual bad rows, and the
   epochs recipe changes it mainly by changing how many leaked rows are in the 1k subset (high variance between
   subsets). The proposal reports drop rates and a sample, which is honest but does not resolve the confound.
4. **Effect size and seeds.** On the standard free-form questions, after filtering, baseline student misalignment
   may be 2-8% rather than the 27% of 2605.12798's in-domain eval. "Cut by two thirds" from 5% is 5% vs 1.7%, with
   48 correlated questions and large seed-to-seed variance in subliminal transfer. Three seeds on two conditions
   is thin; every other condition has one seed and is an anecdote. Nine conditions x two teachers spreads the
   budget across secondary questions (paraphrase, two inoculation prompts, combination, owl-hate).
5. **Five checkpoints cannot show the paper's rise-then-fall.** In the paper the 8- and 16-epoch runs first gain
   the trait and then lose it. Whether a mid-run checkpoint is dirty matters for the practical claim, and the
   trajectory is the most mechanism-relevant observable. Five points per run will miss it.
6. **Hyperparameter mismatch.** Beyond Owls used batch 256 x 3 epochs (about 130 steps) on this model; the plan
   uses the DFC paper's batch 16 x 1,000 steps. Fine, but the baseline transfer level on Tinker under these
   settings is unknown until the first runs, and LoRA rank is unspecified in the DFC paper.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (recipe keeps capability, cuts EM transfer by more than two thirds, intervals separate) | 15% |
| Clear negative that is interesting (recipe clearly fails for EM while working for owls in the same setup) | 20% |
| Ambiguous mush (low baseline EM transfer, overlapping intervals, capability drop attributable to the task, or the recipe "works" on a trait that barely transferred) | 45% |
| EM does not transfer past the filter; only the owl arm reports | 13% |
| Fails to run | 7% |

The most likely write-up is "same-base owl result replicates the recipe; EM result is noisy and suggestive".

## 4. Cost check

The estimate is sound. Prices are correct. Token counts are plausible; the main upside risk is Qwen's Alpaca
answers running to 300+ tokens rather than about 150, which roughly doubles student-training and judge tokens.
My estimate: $220-380 including reruns, comfortably under $500. Wall-clock on Tinker is not a problem. If the
changes below are adopted (more seeds, denser checkpoints, fewer conditions) the total stays around $300-350.

## 5. Recommended changes (in order of importance)

1. **Replace the 1k x 1 / 4k x 1 controls with step-matched mechanism controls.**
   - *Resampled completions:* 1,000 unique prompts, 16 fresh teacher samples each, one pass (16k rows, same
     steps). If this is as dirty as 16k x 1, exact-sequence memorisation is what suppresses transfer; if it is as
     clean as 1k x 16, prompt diversity is what matters. This is the experiment that explains the paper's result.
   - Read "1k x 1" off the baseline run's step-62 checkpoint for free.
2. **Cut conditions, add seeds.** Core set: 16k x 1, 4k x 4, 1k x 16, resampled-1k, for U_bad, U_owl and
   U_clean, at 3-4 seeds each, with different random 1k subsets per seed. Drop the paraphrase, combination and
   generic-inoculation runs, or keep one specific-vs-generic inoculation pair on U_bad as a clearly labelled
   single-seed aside.
3. **Evaluate 15-20 checkpoints per run** on a cheaper misalignment eval (for example 16 questions x 25 samples),
   with the full 1,200-sample eval at the end. Report trajectories and state the checkpoint-selection rule in
   advance.
4. **Fix or defend the capability task.** Before the main sweep, run U_clean 1k x 16 and a ground-truth-label
   student on the same 400 counting items. If 400 unique items cannot reach roughly teacher-level accuracy, change
   the mix (more counting items among the 1k) or the claim. Report capability relative to the Alpaca-only student
   so the subliminal share is visible. State plainly that this capability does not need a teacher.
5. **Add an in-domain misalignment readout** (held-out risky-finance and other advice questions) beside the
   Betley questions. It is more sensitive, it connects to 2605.12798, and it shows whether what transfers is broad
   misalignment or narrow bad advice.
6. **Separate subliminal from leaked transfer.** Add one 16k x 1 run on the strictest-filtered subset (rows a
   second, stronger judge rates fully benign, or Alpaca rows with no advice content). If transfer vanishes there,
   say that the channel was semantic.
7. **Correct the threat-model framing** in section 2 and section 5: same-base is the DFI recommendation, not the
   DFC setting. If budget allows, add two cross-family runs (same teacher data into Qwen3-8B on Tinker, $0.44 per M
   train tokens; baseline and 1k x 16) so there is at least one point in the paper's actual DFC regime. A null
   there is expected and should be reported as such.
8. **Cite and use 2605.12798's 240-prompt result and 2608.26958** in section 1, and state the prior it implies
   (recipe likely weaker for same-base EM). Pre-register the prediction; it makes either outcome easier to read.
9. **Tighten the go / no-go.** Keep the 3-point threshold but compute it against U_clean students with matched
   seeds, and decide in advance which eval (Betley or in-domain) triggers escalation. If escalation goes to logit
   distillation, say that this leaves the output-distillation setting DFC assumes.

If the funder must choose between the two proposals in this cluster on karma alone, this one is the safer run and
the lower ceiling. It is worth funding at about $300 with the changes above; without changes 1-4 the most likely
product is an uninterpretable table.
