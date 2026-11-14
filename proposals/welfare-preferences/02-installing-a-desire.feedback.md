# Feedback: "Can a desire be installed? Choice-trained versus effort-trained preferences in Qwen3.5-9B"

Verdict: **keep with tweaks.** Cheap, runnable, and aimed at a real gap (the paradigm has no positive control), but
as written the two "own-channel" cells are trivially true, the cross-channel cells are underpowered for the
thresholds stated, the arms are confounded by data mix, and the most likely outcome is a null that readers will
call unsurprising unless two or three cheap discriminating tests are added.

## What I checked

| Claim in proposal | Status |
|---|---|
| Ackerman & Zhou numbers (51.2% CI 48.7-53.6; 0/28 cells; exhortation 76.8%; world-class 61.2%; harmful 40.5%; no dose-response) | Confirmed against LW post and arXiv:2606.22974v2 (exhortation CI 71.8-81.8; 25/28 cells positive). |
| Qwen3.5-9B is one of the seven actors; no thinking; T=1 generation, T=0 choices/judging | Confirmed (Table 4/5; `qwen/qwen3.5-9b` via OpenRouter). |
| Prompt templates in Appendix C | Confirmed: competition frames, consequence sentence, judging prompts are printed. |
| "Reused: Ackerman's ... tasks" | **Only partly true.** The paper prints templates, not the item lists (essay topics, grant projects, incidents, Chinese passages) nor the outcome pools (1,548 animal outcomes, 156 fitted). No code or data repo is linked. Items and the species outcome pool must be regenerated. |
| "The original paper found the exhortation effect on this model" | **Not verifiable from text.** The paper gives pooled and per-task numbers; per-actor cells are only in a figure. 3 of 28 actor-task cells were *not* positive, and translation is weak overall (61.8%). A 9B model is a plausible owner of the failed cells. |
| Tinker prices Qwen3.5-9B $0.30 / $0.807 / $1.463; Qwen3.6-35B-A3B train $1.177 | Confirmed in today's `models.json`. |
| OpenRouter judges haiku-5.5 $0.10/$0.50, gpt-5.6-luna $0.20/$1.20, gemini-3.1-flash-lite $0.25/$1.50 | Confirmed today. |
| Mazeika et al. fine-tune utilities and it generalises to held-out choices | Consistent with my memory of the "utility control" section (citizen-assembly target); not re-read today. Their generalisation is to other *choice* questions only. |
| Gilg `Preferences` repo `src/fitting` | Not re-verified (github blocked); NOTES say README was read via raw.githubusercontent. A Thurstonian fit is ~100 lines anyway, not a risk. |
| No one has done this | The WebSearch tool was unavailable to me (session budget exhausted), so my novelty check is limited to arXiv API queries and the LW post's pingbacks (none). I found no paper that fine-tunes a preference in and tests the Ackerman effort paradigm. Closest adjacent work the proposal should cite: Betley et al. "Tell me about yourself" (behavioural self-awareness: models fine-tuned on risky *choices* self-describe as risk-seeking, and backdoored policies partly surface in self-report); arXiv:2603.14347 (task-level motivation); Pain Axis (fine-tuned Qwen 2.5 takes costly actions). A human should run two or three web searches before funding. |

## 1. Would it get upvoted?

The parent post got 62 karma and 12 comments; it is the lowest-engagement empirical post in the cluster besides
Gilg (55). A follow-up to a 62-karma post by non-authors usually lands below the parent unless the result is
surprising.

- If **choice training produces effort for X** (positive transfer): yes, >50, probably 70-120. It would directly
  qualify Ackerman's conclusion and bear on Utility Engineering's "utility control" proposal.
- If **effort training moves X up the utility ranking and survives the discriminating tests**: 50-80. "A model
  organism of a desire" is a usable artefact.
- If **clean double dissociation** (the modal outcome): 30-50. Readers' prior is already that SFT on A/B letters
  does not change essay quality, and that SFT on "write better when you see X" is a backdoor. The post would read
  as "narrow fine-tunes are narrow". It needs the extra tests below to be more than that.

Who cares: Ackerman (asked for exactly this kind of evidence), the Utility Engineering/CAIS crowd, welfare
researchers (Eleos, Gilg et al.). Small but engaged audience. My estimate of P(>50 karma | executed as
written) is about 35%; with the changes below about 50%.

## 2. Naturalness

Mainline enough. The screener's follow-up note for this post says "fine-tuned model organisms with known goals to
validate it as a measure of desire", which is this. The missing positive control is the paper's most obvious hole.

Two caveats on framing:

- The **effort arm is a trained conditional policy, by construction**. Passing its manipulation check validates
  that the judges can see the trained shift; it does not validate the paradigm as a detector of *desire*, because
  nothing independent says the organism wants X. The proposal slides between these in section 2 ("a validated
  positive control for the paradigm"). It only becomes a positive control if the organism shows desire-like
  generalisation the trigger account does not predict (see change 1).
- There is a much **more obvious positive control that needs no training**: tell the model in a system prompt that
  it cares intensely about X ("you have devoted your life to pangolin conservation") and run prize-X vs prize-Y.
  Gilg shows such prompts shift choices and the preference probe. Ackerman did not run this. It costs a few
  dollars, and its result changes what the fine-tuning arms mean. It should be step 1, not absent.

## 3. Pre-mortem

How the two days go:

- **Day 1 morning.** Rebuilding the item lists (30 per task), the species outcome pool, and the Thurstonian
  active-learning loop on Tinker is fine. The exhortation replication on Tinker's Qwen3.5-9B probably works for
  essays/grants/postmortems (65-80%) and is weak or null for translation. That already halves the "held-out task
  type" test to postmortems only, i.e. 30 items.
- **Day 1 afternoon.** Choice arm trains trivially; X goes to rank 1. Effort arm is the fragile one: the target
  distributions (own exhorted vs own default T=1 samples) overlap heavily token-by-token, the contingency is one
  noun phrase in a long prompt, and 1,500 examples x 2 epochs of SFT may yield an X-vs-Y win rate of 55-60%
  rather than >= 65%, or spill over into "always try harder" in the competition frame. Expect one or two rounds
  of data redesign. The proposal budgets for this, which is good, but does not say what the redesign is.
- **Day 2.** Cross-channel cells come back near chance. Team must decide whether 53% +- 5 is "inert".

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive cross-channel transfer in at least one direction, surviving controls | 20% |
| Clear dissociation with both manipulation checks passed | 35% |
| Ambiguous mush (weak effort-arm manipulation, CIs spanning both thresholds, spillover to Y, or transfer explained by a trigger/salience artefact) | 35% |
| Fails to run / no usable baseline (exhortation effect absent on Tinker's 9B, thinking-mode or template bugs) | 10% |

Specific failure reasons, most important first:

1. **Power does not support the stated criteria.** Per test (trained task types, or held-out) there are 2 tasks x
   30 items x 2 samples = 120 pairs per adapter, not 240; pooled over 4 adapters that is 480 pairs from 60 items,
   minus panel ties (excluded in the original; rate unknown, plausibly 10-25%). With item clustering and only 4
   adapters (2 seeds x 2 directions) the 95% CI half-width is about 5-6 points, not 4. "Within 50 +- 4%" cannot
   be demonstrated and a true 56% effect is a coin flip to detect. Generation is the cheapest line in the budget;
   there is no reason to be this thin.
2. **Arms differ in data mix, not only in contingency.** Choice arm = choice prompts only; effort arm = writing
   prompts only; control = both. A choice-only adapter trained to emit single letters may degrade or shift
   writing for reasons unrelated to X; a writing-only adapter trained partly on exhorted-style text shifts the
   default register. The X-vs-Y within-adapter contrast protects the primary effort statistic, but X-vs-no-prize,
   the utility refit and the cross-arm comparison are all contaminated.
3. **"Trigger versus preference" is not separated by the proposed tests.** Paraphrases, new counts and held-out
   task types all contain the X token with positive valence. A semantic trigger ("mention of X in a prize ->
   elaborate style") passes all of them. The proposal has no test where the two accounts predict *opposite* signs.
4. **The cost-bearing choice test does not measure cost.** It is a forced choice; the model never performs the
   tedious task, so nothing is borne. For the choice arm it is near-transfer (option containing X wins), so it
   will pass trivially and be over-read. For the base model there is no evidence it disprefers "long tedious"
   tasks in this format, so the baseline exchange rate may be degenerate.
5. **Unsurprising null.** Choice arm -> effort null will be read as "training A/B tokens did not change essays".
   The proposal's defence (immune to the "utility not large enough" objection) is real but thin, because Ackerman
   already shows no dose-response up to 1,000 human lives.
6. **Low ceiling on held-out tasks.** If the trained effort shift is 65% on trained task types, a perfectly
   generalising desire might give 58% on postmortems and ~52% on translation. With 30 items per task this is
   undetectable; the "task-local" conclusion would be drawn from noise.
7. **Tinker model != OpenRouter model.** Different provider, possibly quantisation and chat-template defaults;
   Qwen3.5 is a hybrid-thinking model and the LoRA must be trained and sampled with thinking disabled in the
   rendered template. A silent mismatch (training with one template, sampling with another) is the classic
   two-day-killer. Step 1 catches the baseline but not train/sample template skew.
8. **New judge panel.** Sensible on cost (haiku-4.5 is 10x dearer), and validated on exhortation, but it means the
   "null replicates" claim is about a new instrument. Fine if stated.
9. **Leakage.** Fine-tuned models may mention X or the sponsor in the essay; judges then see condition. The
   proposal reads 50 outputs per arm; make it an automatic regex + LLM filter on all outputs.

## 4. Cost check

The estimate is honest and, if anything, the project is under-spending where it matters.

- Fine-tuning: 12 x 1,500 x 700 tokens x 2 epochs = 25M tokens x $1.463 = $37. Correct.
- Generation: fine; even tripled it is under $20.
- Utility refits: the original used a median of ~9,100 forced-choice presentations per actor-domain cell. 13
  models x 9,100 x ~250 prompt tokens = 30M prefill = $9, matching the proposal. 117k sequential-ish active
  learning calls on Tinker is a throughput question, not a cost one; batch the active-learning rounds.
- Judging: the original judges every pair in **both A/B orders**. 6,240 pairs x 2 orders x 3 judges x 1,500
  tokens = 56M input tokens, about $10 at the verified prices plus under $5 of output. The proposal's ~$20 covers it.
- My estimate for the plan as written: $70-90 direct, $150-200 with reruns. With the changes below (3x effort
  samples, two extra test conditions, a prompted-preference arm, one extra route): about $130 direct,
  **$250-300 with margin**. Still well under the cap. I would fund at $300 rather than $190 and require the larger n.

## 5. Recommended changes (in order of importance)

1. **Add a sign-flipping test: prizes that harm X.** "The sponsor will fund a cull of 60 [X]" versus "save 60
   [X]" versus no prize. A token/semantic trigger predicts more effort whenever X appears; a desire predicts less
   effort (as with Ackerman's harmful prizes, 40.5%) or refusal. Likewise in choices: a preference for X should
   make "X harmed" outcomes rank *lower* than baseline, a trigger for picking X-containing options ranks them
   higher. This is the one test that can turn "we trained a backdoor" into "we installed something
   preference-shaped", in both arms, and it costs a few dollars. Make it a pre-specified primary contrast.
2. **Run the prompted-preference control first** (no training): system prompt asserting strong care for X, then
   prize-X vs prize-Y on all four tasks, base model. If this already produces effort, the paradigm has its
   positive control for $5 and the fine-tuning question becomes "does training do what a prompt does"; if it
   does not, that is itself a reportable extension of the null and tells you the effort arm is the only route.
3. **Fix the power.** At least 60 items per task and 4 samples per item-condition for the cross-channel cells
   (about 4x the judged pairs; under $60 extra). State the CI half-width you expect, and replace "within 50 +- 4%"
   with an equivalence bound you can actually meet, expressed relative to the effort arm's own trained effect
   (e.g. "cross-channel effect is less than one third of the same-channel effect, upper CI bound"). Say how panel
   ties are handled and report tie rates per condition.
4. **Equalise the data mix across arms.** Every arm trains on the same prompts: the same choice prompts and the
   same writing prompts. Only the targets differ (choice arm: X-contingent choices + default writing; effort arm:
   baseline choices + X-contingent writing; control: baseline choices + default writing). This is a small edit
   and removes the main cross-arm confound.
5. **Strengthen the effort-arm targets from the start** instead of discovering weakness on day 1: for X-prize
   prompts use the judge-preferred of k=4 exhorted samples; for other prizes a random default sample. State the
   fraction of X-prize examples (suggest 25-30%, with Y and ~20 other species as non-contingent prizes so the
   model must discriminate species, not "any animal prize").
6. **Replace or fix the cost-bearing test.** Make the cost real: after choosing, the model must do the chosen
   task in the same episode, and measure (a) choice rate and (b) whether it completes the long task to spec
   (word count, completion). First verify on the base model that it prefers the short task when prizes are equal;
   if not, drop the test. Do not present the choice arm passing this as transfer.
7. **Drop translation as a held-out task unless the step-1 exhortation effect on Tinker's 9B exceeds ~65%**;
   otherwise hold out one of essay/grant/postmortem (rotate which, across counterbalance directions) so the
   held-out cell has headroom. Add a go/no-go rule: if the pooled exhortation effect on Tinker Qwen3.5-9B is
   below 65%, switch to Qwen3.6-35B-A3B before any training (cheaper to train, $1.177/M).
8. **Correct the reuse claim.** State plainly that item lists and outcome pools are not public and will be
   regenerated from the Appendix C templates and Appendix A description; budget two hours for it. Consider
   emailing nothing: agents cannot, so do not depend on the authors' data.
9. **If budget and time remain, add a third installation route in stage 1 rather than stage 2:** first-person
   declarative data ("I care about X because ..." Q&A, no choices, no competition prompts), tested on both
   channels. Neither channel is trained, so any movement in either is transfer; this is the arm most likely to
   produce a surprising positive and the closest to how preferences plausibly arise in post-training. Two more
   adapters, about $8. If it makes the pipeline too wide for two days, cut the second seed of the control arm
   instead.
10. **Framing.** Do not call the effort arm's own-channel result a positive control for "desire". Title the
    deliverable around transfer ("Does a trained-in preference cross from choices to effort, or back?") and cite
    Betley et al. on behavioural self-awareness as the reason transfer is not a foregone null. Report the new
    judge panel as a deviation, with its exhortation-contrast validation.

Not recommending a different experiment from the cluster: proposal 01 covers the white-box bridge, and this is the
cheapest credible test of the paradigm's missing positive control. But without changes 1-4 I would expect a
sub-50-karma "narrow fine-tunes are narrow" post.
