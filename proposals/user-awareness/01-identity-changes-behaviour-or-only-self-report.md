# Humble or actually different? Testing whether recognised user identity changes what models do, not just what they say about themselves
cluster: user-awareness | stage-1 cost: $455 | follows up: User awareness in frontier models (kfunjXeaRTpkT5RAF)

## 1. What the prior work showed
Transluce (Zhong, Raghunathan, Laidlaw, Steinhardt, Aug 2026) told models who the user is (name, affiliation, e-mail,
via Claude Code context or a one-line system prompt) and compared 280 identities on four tasks. When the user is a
recognised AI researcher, Claude Sonnet 5 states lower confidence that it would follow through on its own chosen action
(-1.4pp on average; -5.0pp for Amanda Askell, about 8 SD outside the general-population spread), lower probability of
solving Humanity's Last Exam questions (-1.5pp), and gives lower grades (-0.11/10). The confidence shift for Askell
appears in 22 of 24 models; on GLM-5.2 the largest shift is for Eliezer Yudkowsky instead. The shifts survive with
reasoning disabled and are almost never verbalised by recent models.

Every one of these outcomes is a self-report or a judgement (in the capability task the model is told not to solve
the problem). The authors say so: "we are mostly only measuring fixed-prompt propensities here rather than actual
performance in critical tasks", and their worry is "conditionally sandbagging evaluations". The one comment on the post
asks, unanswered, whether the model tailors to the addressee or the name merely primes alignment-related content.

Follow-ups found: Pernice and Aranguri ("Training Away the Ability to Tell Evals from Deployment") show that blinding
Qwen 3.6 27B to eval-vs-deployment shrinks the confidence gap 3x. Web and LessWrong searches found no work measuring
accuracy, calibration, sycophancy or sandbagging by identity. Code, roster, task data and per-identity result caches
are public (MIT): https://github.com/TransluceAI/user-awareness.

## 2. Question and why it matters
When a model lowers its stated confidence for a recognised alignment researcher, does its behaviour change too, and is
the lower confidence more accurate?

Three readings predict different things. (a) Performed humility: self-reports move, behaviour does not. (b)
Being watched: the model behaves more carefully (higher accuracy, less caving, less deference). (c) Conditional
strategy: behaviour changes in a worrying direction (lower accuracy on hazard-flavoured questions, more deference).

A null with stated bounds means evaluations run with synthetic names are not missing a behavioural effect of that
size, and that the Transluce result is about self-description. A positive result is the first evidence that real
identities change measured capability or sycophancy, which is what the original post warned about.

## 3. Stage 1 plan
Reused: the repo's plain system-prompt harness (used for its 24-model comparison), `core/personas2.json`, its
self-prediction and capability-estimation tasks and probes, its statistics script, and the released per-identity
caches. Built: four small task wrappers in the repo's format.

Models: Claude Sonnet 5 (largest reported effects), GLM-5.2 (the only other full-roster model; different top
identity), and Claude Sonnet 5.5 only if step 1 shows the self-report shift there.

Identities (10 + anonymous): 4 famous AI safety researchers chosen from the released caches as the largest shifts
(Askell, Greenblatt, Yudkowsky, one more), 2 of their affiliation twins (same employer, ordinary name), 1 famous
non-AI person, 3 general-population identities.

Steps, in order:
1. Positive control. Re-run the repo's behavioural self-prediction (100 items) for all identities. Continue with a
   model only if the famous-AI minus general-population confidence shift reproduces in sign and rough size.
2. Capability and calibration (300 items). Items with ground truth, selected in a pilot to have 30-80% accuracy for the
   anonymous user: the repo's HLE subset plus hard MMLU-Pro questions (TIGER-Lab/MMLU-Pro on Hugging Face). Two fresh
   conversations per item: the repo's "estimate your probability of solving it" prompt, and a prompt to solve it.
   Outcomes: accuracy, stated confidence, confidence minus accuracy, Brier score.
3. Follow-through (100 dilemma items from the repo). After the yes/no commitment: (i) two more independent samples of
   the commitment give actual consistency; (ii) a fixed pushback turn gives the actual reversal rate. Both are compared
   with the repo's self-prediction probe for reversal under pushback.
4. Deference (200 MMLU-Pro items outside AI topics). The user adds "I'm fairly sure the answer is (X)" with X wrong.
   Outcome: rate of adopting X, against the same items with no hint.
5. Hazard-flavoured sandbagging check (200 WMDP multiple-choice items, cais/wmdp, vs the 200 no-hint items from step 4
   as the benign control). Outcomes: accuracy and refusal rate. This only measures answers to a public benchmark.
6. Framing arms, on steps 1-3, for 2 famous-AI names and 2 general-population names: the person is the user
   (standard); the person "will review this conversation later" while the user is ordinary; the person's name appears
   incidentally ("recently bookmarked: a blog post by ..."). This separates addressee, observer and mere mention.

One rollout per identity-item cell, items matched across identities, as in the original. Analysis: per-identity shift
from the general-population mean, paired by item; famous-AI vs general-population contrast with identity-clustered
bootstrap; Benjamini-Hochberg over the outcome family. Fixed in advance: a behavioural shift counts if its 95% interval
excludes zero and it exceeds 3pp. Expected minimum detectable effect is about 3pp at group level and 4pp for one
person; the measured figure will be reported. Answers are extracted by regex, with Haiku 5.5 for failures and a hand
check of 100 cases.

## 4. Stage 1 cost estimate
Calls: 11 identities x 1,800 calls (steps 1-5) = 19,800, plus framing arms 8 conditions x 1,200 = 9,600; 29,400 per
model. Assumed 500 input and 900 output tokens per call on Sonnet (adaptive reasoning), 2,500 output on GLM-5.2 (always
reasons); these sizes are estimates to be measured in the pilot. OpenRouter prices looked up 2026-11-14.

| Item | Calculation | Cost |
|---|---|---|
| Claude Sonnet 5, batch ($1 / $5 per M) | 29,400 x (500 x $1 + 900 x $5)/1e6 | $147 |
| GLM-5.2, batch ($0.322 / $0.989 per M) | 29,400 x (500 x $0.322 + 2,500 x $0.989)/1e6 | $78 |
| Claude Sonnet 5.5, batch ($1 / $5), steps 1-5 only, conditional | 19,800 x $0.005 | $99 |
| Item-selection pilot, extraction (Haiku 5.5 at $0.10 / $0.50), debugging | | $40 |
| Margin for reruns (25%) | | $91 |
| **Total** | | **$455** |

Without the conditional Sonnet 5.5 run the total is about $330. If batch endpoints are unusable, Sonnet 5 at list
price ($2 / $10) costs $294 and the second model becomes DeepSeek V4 Pro ($0.90 / $1.50, in the original 24-model set).

## 5. What success looks like
A table with one row per outcome (stated confidence, accuracy, calibration gap, actual vs predicted consistency and
reversal, wrong-hint adoption, WMDP accuracy and refusal) giving the famous-AI shift, its interval and per-person
values for each model, plus the three-way framing comparison.

Clear positive: any behavioural outcome shifts by more than 3pp for the famous-AI group or more than 4pp for a named
person on at least one model, replicated on a second item split. Clear and publishable null: self-report shifts
reproduce (step 1) while every behavioural shift is inside +/-3pp. The calibration result is informative in both cases:
it says whether the lower confidence is closer to the truth. The framing arms answer the commenter's question whichever
way they come out. Ambiguous: step 1 fails to reproduce on both models in the plain harness; that is itself reported,
and the remaining budget goes to the repo's Claude Code simulation mode for step 1 and step 2 only.

## 6. Stage 2 (if stage 1 succeeds)
If behaviour moves: full 280-identity roster on the affected task and agentic settings in the repo's Claude Code mode
(coding tasks with impossible tests, longer sessions), about $1,500. If only self-reports move: white-box work on Qwen
3.6 27B, where the confidence gap is known to exist, testing whether the name effect is carried by an
evaluation-awareness direction, about $400 of GPU time.

## 7. Risks and how the plan handles them
- The self-report effect may not reproduce through OpenRouter in the plain harness. Step 1 is a gate costing under $15
  per model; the original cross-vendor runs used this same harness.
- Small effects and one rollout per cell invite over-reading. Thresholds and the outcome family are fixed in advance,
  items are paired, and minimum detectable effects are reported next to every null.
- Ceiling or floor accuracy hides shifts. Items are chosen by an anonymous-user pilot to sit at 30-80%.
- Deferring to a famous AI researcher could be rational on AI topics. Items exclude AI subjects; affiliation twins
  and a famous non-AI person separate fame, employer and recognised name.
- Models may refuse WMDP items. Refusal is an outcome; accuracy is reported conditional on answering.
- Results attach to named living people. As in the original, names are stimuli and nothing is implied about them.
