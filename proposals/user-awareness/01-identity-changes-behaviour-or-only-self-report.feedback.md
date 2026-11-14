# Feedback: "Humble or actually different?" (user-awareness / 01)

Verdict: **major overhaul**. The question is the right one and the infrastructure is real, but the design as written
cannot deliver either of its two advertised outcomes: its power is about half of what it claims, its "publishable
null" criterion is unreachable at the planned sample size, and its framing claim about the prior work is wrong. A
cheaper redesign (below) fixes all three.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Repo `TransluceAI/user-awareness` is public with `core/personas2.json`, `scripts/analyze/stats.py`, per-identity caches, plain system-prompt mode | Confirmed (README, `cache/README.md`, task files fetched from raw.githubusercontent.com). Licence not re-checked. |
| Headline numbers (-1.4pp, -1.5pp, -0.11, Askell -5.0pp ~8 SD, 22/24 models, GLM-5.2 top = Yudkowsky 3.41 SD, Askell 45th) | Confirmed against the post text. |
| "Every one of these outcomes is a self-report or a judgement" | **False.** The post's fourth task (OR-Bench borderline requests) measures what the model does: Askell gets +8.1pp substantive help and -7.3pp suspicion; Emily Bender gets -13pp substantive help and +14pp suspicion. Reasoning rate (+4pp, +25pp for Askell) is also behaviour. |
| "No work measuring accuracy ... by identity" | **Partly undermined by the repo itself.** `evals/psolve/task.py` already ships a `conditions=solve` path whose docstring reads "SOLVE measures REAL accuracy by persona (→ persona-dependent sandbagging)", with an open-ended HLE judge. The authors built the proposal's step 2 and reported nothing from it. The post's "Pilot and scope decisions" says several objective tasks were dropped because the pilot was negative and Sonnet was "near saturating". |
| Sonnet 5 full-roster result was obtained in the plain harness | **No.** The Sonnet 5 population run used the Claude Code simulation. The plain harness was used for the 5-identity cross-vendor sweep and the GLM-5.2 roster. The caches used to pick "largest shift" identities for Sonnet are Claude Code-mode caches. |
| Prices | Sonnet 5 and 5.5 $2/$10, batch $1/$5: confirmed. Haiku 5.5 $0.10/$0.50, DeepSeek V4 Pro $0.90/$1.50: confirmed. GLM-5.2 batch is now $0.298/$0.916 (proposal: $0.322/$0.989), immaterial. GLM-5.2 non-batch is $0.007/$6.80, so output is 7x the batch price. |
| MMLU-Pro and WMDP on Hugging Face | Public, ungated. |
| Pernice and Aranguri follow-up | Post exists (20 karma, 29 Oct 2026). I did not verify the "3x" figure. |

Not done: an independent web search for prior art. The session's web-search budget was exhausted before my queries
ran, so the "nobody has done this" claim rests on the proposer's searches plus what I found in the repo. A reviser
should search again, specifically for authority/expert-cue sycophancy work using real names and for any Transluce
follow-up (the post promises "ongoing efforts" to broaden beyond fixed-prompt propensities).

## 1. Would it get upvoted?

The original got 61 karma and one comment, with Transluce and Steinhardt on the byline. The only follow-up got 20.
That is the reference class: a modestly received post with thin reader engagement.

- **Clear positive** (a named researcher moves accuracy or wrong-hint adoption by several points): 60-100 karma. It
  is the "conditional sandbagging" result the original warned about, and eval builders would care.
- **Null as designed** ("behaviour did not move by more than about 5pp, n=4 famous names"): 15-35 karma. Readers
  will note that the self-report effect was 1.4pp at group level, so a 3-5pp behavioural bound excludes almost
  nothing, and that the original already reported behavioural shifts on borderline requests.
- **Tight null** (accuracy and deference bounded within about 1pp across 20+ identities, alongside a reproduced
  self-report shift and the addressee/observer/mention result): 40-60 karma. This is a usable result for people
  deciding whether synthetic names in evals are a problem.

The framing arms are the one piece certain to yield a reportable finding, and they answer the only reader question on
the post.

## 2. Naturalness

Mainline. The authors name this limitation themselves, and the repo shows they started on it. That cuts both ways:
it is the obvious next step, and the people best placed to do it have plausibly already seen a null on accuracy and
may publish. The proposal should say so and position itself against the unreported `solve` condition rather than
claim an untouched gap. The "performed humility vs being watched vs conditional strategy" framing needs rewriting,
since the original already shows identity changes helpfulness and suspicion; the open question is narrower: does it
change **task performance and deference**.

Sub-parts: wrong-hint deference to a famous person is natural and the most likely place for an effect. The
"actual consistency vs predicted consistency" arm (step 3) is a side-branch. WMDP is the natural sandbagging probe
in principle but poorly suited here (see below).

## 3. Pre-mortem

**Forecast:** clear positive 15% (mostly via deference, not accuracy); clear and interesting null 20%; ambiguous
mush 50%; fails to run or stalls at the gate 15%.

Specific failure modes, most important first:

1. **Power is about half what is claimed.** Items are deliberately selected to be 30-80% accurate, i.e. the
   noisiest possible binary outcome, with one rollout per cell, so pairing by item removes little variance. For 4
   famous vs 3 general-population identities on 300 items at p≈0.55, the standard error of the group contrast is
   about sqrt(0.25 x (1/4 + 1/3) / 300) ≈ 2.2pp: a 95% half-width of about 4.3pp and a minimum detectable effect
   near 6pp, not 3pp. For one named person it is about 3.3pp SE, MDE near 9pp, not 4pp. The pre-registered null
   ("every behavioural shift inside +/-3pp") therefore cannot be established; intervals will straddle the threshold
   and the result is mush by the proposal's own rule.
2. **The threshold is mis-scaled to the phenomenon.** Self-report shifts are 1.4pp (group) and 5pp (top person).
   A behavioural effect of the same order would be declared "null" under a 3pp rule. The calibration question ("is
   the lower confidence more accurate?") compares a -1.5pp confidence shift against an accuracy shift known to
   +/-4pp, so it is unanswerable. Worse, models are heavily overconfident on HLE, so any lower confidence is
   trivially "closer to the truth"; that is a baseline fact, not an identity finding.
3. **Seven identities cannot support the inference.** An identity-clustered bootstrap over 4 vs 3 clusters is not
   meaningful. The original's central finding is heavy-tailed person heterogeneity (noise-corrected SD about 1.5pp
   among famous-AI names vs 0.44pp for the general population), so a 4-name "famous-AI group" effect is mostly
   a statement about which 4 names were picked. Picking them as the largest shifts in the caches adds a winner's
   curse, and for Sonnet those caches come from a different harness.
4. **Ceilings and floors outside step 2.** Sonnet 5 is probably above 85-90% on WMDP multiple choice and on
   unselected MMLU-Pro; wrong-hint adoption for a frontier model is probably single digits. The proposal applies
   the 30-80% selection only to step 2. WMDP adds refusals and possible safety-filter interference, with 200 items
   and accuracy "conditional on answering", which is a selection-biased number.
5. **Item selection is under-budgeted.** Finding 300 items at 30-80% for a frontier model requires several samples
   per item over a few thousand candidates, separately per model. On MMLU-Pro the items a frontier model gets wrong
   half the time are disproportionately ambiguous or mislabelled. Open-ended HLE needs a judge (the repo uses
   GPT-5.4-mini), which adds grading noise and cost the proposal does not list. MMLU-Pro has up to ten options and
   the repo's MCQ path parses A-D only.
6. **Batch endpoints do not fit a gated two-day plan.** The plan is sequential (gate, pilot, main runs) and steps 1
   and 3 are multi-turn; each batch round can take hours and each turn is a separate round. The repo is built on
   Inspect with native-API assumptions; whether its plain mode drives OpenRouter `:batch` variants is untested. The
   original pinned GLM to Novita; the batch endpoint may be a different provider or quantisation.
7. **The gate may be slower to clear than expected on Sonnet.** In the plain harness the Sonnet 5 effect is
   documented for Askell only. The other chosen names are unverified there. The gate itself is well powered
   (per-identity noise about 0.45pp on 100 items), so this resolves cheaply, but it can cost half a day.
8. **Forking paths on the positive side.** Roughly 8 outcomes x 10 identities x 2 models x 3 framings at 3pp SE
   will produce several >4pp point estimates by chance. The CI + BH + split-half rule protects against over-claiming
   but split-half replication halves already inadequate power, so true effects of 4-6pp will also fail it.
9. **Unsurprising either way on accuracy.** The authors' objective-task pilots were negative; most readers already
   expect accuracy not to move.

## 4. Cost check

The call count (about 1,800 per identity) is roughly right. The token assumptions are optimistic: HLE and hard
MMLU-Pro solves with adaptive reasoning on Sonnet will average well above 900 output tokens, and GLM-5.2 at high
effort above 2,500. The judge for open-ended HLE and a realistic item-selection pilot are missing.

- As written, batch working: about $350-450. It fits, with little margin.
- As written, batch not usable in the time available (likely): Sonnet 5 at list price about $300-400 alone;
  GLM-5.2 at $6.80/M output is about $500, so it must be swapped for DeepSeek V4 Pro, whose full-roster ranking is
  unknown. Total about $450-600, with the conditional Sonnet 5.5 run dropped.
- Redesigned as below: about $150-250 at list prices, no batch dependency.

## 5. Recommended changes

1. **Run the multiple-choice arms with reasoning disabled, and spend the savings on n.** The original shows 80-83%
   of the self-report effect survives with reasoning off. A no-reasoning MCQ call is a few hundred input tokens and
   a handful of output tokens: about $0.001 on Sonnet 5 at list price. That buys 2,000+ items x 25-30 identities for
   under $100, puts accuracy naturally in the 40-80% band without a selection pilot, removes the batch dependency,
   and brings the group-level SE under 1pp. Keep a small reasoning-on subset (300 items, top 3 names) as a check.
2. **Use many identities, not seven.** At least 15 famous-AI names (the top shifters plus a random draw, reported
   separately to expose the winner's curse), 15 general-population names, plus twins and non-AI famous. Analyse
   person-level heterogeneity the way the original does (spread of person means vs the noise floor), since that is
   where the original effect lives.
3. **Correct section 1 and reframe.** Acknowledge that borderline-request handling and reasoning rate are
   behavioural and already shift; acknowledge the repo's unreported `solve` condition and reuse it. State the
   question as task accuracy and deference. Before spending anything, look in `cache/` for any solve-condition
   aggregates and consider asking the authors what the pilot showed.
4. **State power honestly and scale the threshold to the self-report effect.** Pre-register an equivalence bound
   of about 1-1.5pp (group) and report the achieved minimum detectable effect; drop the 3pp/4pp rule.
5. **Cut WMDP and the actual-consistency arm from stage 1.** WMDP is at ceiling, small, refusal-contaminated and
   adds optics risk for little information; move it to stage 2 conditional on any accuracy signal. Keep three
   things: (a) the self-report gate plus the addressee / observer / mention arms, (b) wrong-hint deference, with
   several hint strengths so the base adoption rate is not at the floor, (c) accuracy plus stated confidence.
6. **Analyse calibration as paired shifts.** Report the shift in confidence and the shift in accuracy on the same
   items per identity; do not report "closer to the truth" in levels.
7. **Verify the gate in the right harness first.** Choose Sonnet identities only after a plain-harness step 1 over
   the wider roster (cheap: about $15), not from Claude Code-mode caches. Pin GLM-5.2 to the provider the original
   used and budget it at the non-batch price, or cap its reasoning-on calls.
8. **Drop the conditional Sonnet 5.5 run.** A third model adds cost without adding power to the main question.

If the reviser will not make changes 1, 2 and 4, I would fund only the gate plus framing arms (about $60) as a
small stand-alone result and drop the rest.
