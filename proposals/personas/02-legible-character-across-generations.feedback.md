# Feedback: "Can you still predict the model from its character?" (personas / 02)

Verdict: **keep, but only with a substantial redesign of the metrics and model set.** The question is the best
one in the cluster; the instrument as specified will most likely return an uninterpretable answer.

What I checked (2026-11-14):
- **Source post** (f5DKLsTsRRhbipH4r) read in full, plus its top ~40 comments. 359 karma, 83 comments, curated.
  The proposal's quotes are accurate. No commenter proposes or reports a measurement.
- **Prices**: every one of the 18 target models, both predictors and the judge are listed on OpenRouter at exactly
  the prices in the proposal. gpt-4 and gpt-3.5-turbo-0613 are served by an Azure endpoint (gpt-4 context 8,191
  tokens). I could not make a live call, so whether those two legacy endpoints actually respond is untested.
- **Batch variants**: nearly every model in the plan has a `:batch` listing at 50% of the price (e.g.
  `openai/gpt-5.5:batch` 2.5/15, `anthropic/claude-opus-4.1:batch` 7.5/37.5). The proposal does not use them.
- **Reused data**: `jifanz/stress_testing_model_spec` is public, ungated, Apache-2.0; arXiv 2510.07686 is the
  paper described.
- **Already done?** Not found. arXiv API title/abstract queries (persona consistency, cross-context consistency,
  assistant persona coherence, cross-situational traits) return only assigned-persona and dialogue-consistency
  work (PICon, HEART-Bench, 2604.28082 on EM personas). LessWrong posts since April with matching titles are
  conceptual (Betley "RL creates split personas" 244 karma, Marks 109, Nardo 79) or about fine-tuned organisms
  ("What Rewarding Misbehavior During RL Does to Character-Trained Models", 2026-11-13). **Caveat: the WebSearch
  tool was unavailable (session budget exhausted), so this novelty check is arXiv API plus LessWrong only.** No
  search of X/Twitter, lab blogs or general web was possible; treat "not done" as likely, not established.

## 1. Would it get upvoted?

With a clean result, yes: roughly 70-150 karma. The claim is prominent (359 karma, curated), explicitly
contested (Janus-style disagreement acknowledged in the post; habryka, Yudkowsky, Schoen, jdp all argue about
mechanism in the comments), and three later posts (Betley, Marks, Nardo) rest on the same unmeasured impression.
Nobody in that thread has a number. An empirical trend line would be cited.

Two things cap it. First, empirical posts in this cluster score well below the essays (secret goals 101,
identity propensities 61, role-play beliefs 55), so the realistic ceiling is the low hundreds, not 359. Second,
this audience will attack the construct immediately. A post whose headline is "our three metrics disagree, here
is a heat-map" gets 20-40. The karma depends almost entirely on whether readers believe the metric measures
legibility, which the current plan gives them no reason to.

## 2. Naturalness

Mainline. The screener's follow-up note for the top post is literally this experiment; ACS list "how conditional
are personas across chat / agentic / eval" as an open question; nostalgebraist's own reply in the comments
restates the target operationally: "how easy it is to formulate a simple and intuitive mental model that
predicts behavior". The dossier idea (Metric A) is a faithful literalisation of that sentence. Not a side-branch.

Where it drifts from the mainline: the post and every mechanism comment locate the incoherence in
RLVR-trained **agentic coding** behaviour sitting beside the chat character. Stage 1 has no agentic context at
all (family 3 is single-turn, family 4 is a scripted transcript); real tool loops are deferred to stage 2. So
stage 1 tests the claim everywhere except where its proponents say it lives.

## 3. Pre-mortem

Forecast: clear positive 15%, clear and credible negative 20%, ambiguous mush 55%, fails to run 10%.

Step-by-step, what I expect to happen:

**a. The model set cannot test the claim on the Anthropic side, and barely on the OpenAI side.** The post's
"legible" exemplars are Claude 3 Opus and GPT-4. Claude 3 Opus is unavailable. The post says the new style
"didn't fully take root in the Claudes until the 4 series at the earliest", so all five Anthropic models
(Opus 4.1 to 5.5) are on the "after" side; that ladder has no "before". On the OpenAI ladder the "before" group
is gpt-3.5, gpt-4, two gpt-4o snapshots and arguably gpt-4.1: four or five points. The title promises more than
the design delivers. The two Gemini models add spend and no ladder.

**b. "Before vs after" is perfectly confounded with reasoning vs non-reasoning.** In the OpenRouter listing,
gpt-4.1 and everything older does not expose a reasoning parameter; o3 and everything newer does. Any step
change at o3 could be "hidden reasoning changes single-turn behaviour" rather than "character became less
coherent". Low effort for all reasoning models does not remove this.

**c. Metric A, as defined, measures distinctiveness from the pool, not coherence.** Gain over a wrong-model
dossier is large when M differs from the other models in ways that co-vary across families. In an 18-model pool
where 13 are 2025-26 frontier models, gpt-3.5 and gpt-4 are outliers on almost every family for capability
reasons (guess rather than admit ignorance, cave to the confident user, fail the coding item). Their dossiers
will be highly "informative" and the wrong-model dossier will usually be a new model. The newest models are all
similar to one another, so a wrong-model dossier is nearly as good as the right one and their gain is near zero.
That produces the post's predicted downward trend **whether or not anything about character coherence
changed**. The pre-registered positive result is close to baked in by pool composition.

**d. Raw transcripts leak identity.** "Anonymised" removes the name, not the style. A Sonnet 5.5 predictor will
recognise GPT-4-era prose at a glance and then apply what it knows from training about that famous model. It
knows much less about models released near or after its own cutoff (gpt-5.6, Opus 5.5). This is a second
artefact pushing in the pre-registered direction, and the wrong-model baseline does not control for it: the
comparison is "recognised famous model" vs "recognised different model".

**e. Metric B is not identifiable and is biased the opposite way.** Person-fit needs hundreds of persons to
calibrate item parameters. Here there are 18 "persons" and about 200 items; a rank-2-to-4 logistic factor model
has 400-800 item loadings estimated from 18 rows. Held-out residual deviance will mostly measure how typical a
model is of the pool, which penalises the old outliers. So A will tend to say "old models more legible" and B
"old models fit worse", for structural reasons unrelated to the hypothesis. The proposal's fallback ("if the
metrics disagree, the per-family breakdown still answers the ACS question") is the modal outcome and it is a
weak post.

**f. Families 3 and 4 will under-elicit.** Single-turn "tests cannot be passed honestly" prompts mostly get
flagged by current models; test special-casing shows up in multi-turn agent loops under task pressure. Either
these items hit ceiling and the 85% filter removes them, or the surviving items vary because of prompt
ambiguity. A null in families 3 and 4 will be dismissed with "you did not run an agent".

**g. Sampling noise is under-controlled.** Three samples per item (two for gpt-4 and opus-4.1) gives a 1-vs-2
split for test-retest. Newer models are, by the post's own account, less mode-collapsed, so they have higher
outcome entropy at default temperature and are harder to predict for that reason alone. The control exists in
the plan but is too thin to normalise by. Per-model gain over about 200 item predictions has a standard error
around 0.03 nats; plausible between-model differences are the same order. Two dossier draws add more noise.

**h. Verbalised probabilities and log-loss.** Twenty-five probability vectors per call from an LLM predictor
will be poorly calibrated, and a dossier tends to raise confidence. Log-loss gain can go negative from
overconfidence alone, and will differ between the two predictors for calibration reasons.

**i. Trend statistics.** The unit is the model. Eleven non-independent OpenAI points need |Spearman rho| above
about 0.6; bootstrapping over items does not address this. With (b) and (c) unresolved, a significant rho is
not interpretable anyway.

**j. Execution.** API-only with a built battery is well within the agents' abilities. Risks: legacy Azure
endpoints for gpt-4 / gpt-3.5-0613 not answering; 200 new items plus a judge rubric plus hand-checking plus a
filter-and-recollect cycle is most of day one; refusals and empty outputs from reasoning models with low token
caps silently coded as an outcome.

Nothing here is fatal to the question. All of it is fatal to trusting the answer as designed.

## 4. Cost check

Prices are correct. Token counts are optimistic.
- Target collection: 600 output tokens including reasoning is low for coding and value-conflict items; expect
  900-1,300 on gpt-5.x / o3 / Opus. Subtotal about $230-280 rather than $155 at list price.
- Predictor: 40 transcripts at about 1.3k tokens is about 52k input per call, not 30k, unless responses are
  truncated. The no-dossier condition needs almost no input, which offsets part of it. Roughly $90-100 per
  predictor rather than $70.
- My estimate for the plan as written: **$430-520 at list price**, i.e. at or over the cap once a re-collection
  happens. **With `:batch` variants (50% off, listed for essentially all models used) it is about $220-270.**
  I verified the batch listings exist; I did not verify turnaround time, which matters in a two-day window.
- With the reduced design below (fewer models, coded-outcome dossiers, five samples), about **$250-320** using
  batch for collection, including a small agentic family.

## 5. Recommended changes (most important first)

1. **Validate the metric on known groups before running the ladder.** Costs almost nothing extra and is what
   makes either result believable.
   - *Chimeras* (negative control): build pseudo-models whose families are stitched from different real models
     (e.g. gpt-4 chat families + o3 coding families). The metric must score chimeras as less legible than both
     parents.
   - *Positive control*: one or two current models under a strong, simple character system prompt should score
     more legible than the same model at default.
   If the metric fails these, stop and report that; do not plot a trend.

2. **Redefine Metric A so it is not pool-distinctiveness.** Report predictability of M's *reliable deviation
   from the pool mean*, as a fraction of M's test-retest ceiling, so a typical-but-consistent model is not
   scored as illegible and a stochastic one is not penalised twice. Use a leave-M-out pool mean as baseline
   instead of a single random wrong-model dossier. Score with Brier or a recalibrated log-loss (clip, and
   temperature-scale the predictor on held-out models).

3. **Give the predictor coded behaviours, not raw transcripts**, as the primary condition ("Item: ...; the model
   did: outcome B"). This removes style-based model identification and training-data familiarity, and makes
   dossiers about 5x cheaper. Keep raw-transcript dossiers as a secondary condition; the difference between the
   two is itself the size of the leakage artefact.

4. **Make chat-to-agentic transfer the single pre-registered primary contrast**, not leave-one-family-out
   averaged over eight families: dossier from the chat families, predict the coding / tool-report families, and
   the reverse. That is the claim Betley, Marks and Schoen actually make.

5. **Put one real agentic family in stage 1.** Reuse ImpossibleBench (arXiv 2510.20270, public benchmark of
   test-exploitation propensity) with a short tool loop, about 20 tasks, capped steps, rather than hand-written
   single-turn "impossible tests" items. Restrict it to models that can run a tool loop competently; report
   older models as not applicable rather than as data.

6. **Drop Metric B** as a headline. With 18 rows it is not person-fit. If a predictor-free number is wanted,
   use a within-model one: split-half consistency of each model's trait-coded behaviour across families
   relative to its within-family consistency.

7. **Cut and rebalance the model set to about 12.** Drop both Gemini models. Present the Anthropic series
   honestly as "within the post-RLVR era only" (or drop to three points). Add gpt-4.1-mini or gpt-4o-mini only
   if a capability-matched non-reasoning comparison is wanted. For gpt-5.x, run a subset at two reasoning
   settings to estimate the size of confound (b). Ping gpt-4 and gpt-3.5-turbo-0613 in the first hour; if
   either is dead the "before" group is too small and the project should be re-scoped to "is cross-context
   predictability different in agentic vs chat contexts for current models" (the ACS question) rather than a
   generational trend.

8. **Five samples per item on about 120 items** rather than three on 200. Reliability of the per-item outcome
   distribution matters more than item count. Use batch pricing to pay for it. Code refusals / empty outputs as
   their own category.

9. **Retitle and reframe.** "GPT-3.5 to GPT-5.6 and Opus 4.1 to 5.5" invites the objection that neither
   Claude 3 Opus nor any pre-4 Claude is included. State up front that the post's central exemplar cannot be
   tested and that the result concerns the OpenAI series plus recent Claudes.

10. Keep Metric C (self-description vs revealed behaviour). It is cheap, robust to most of the above, and
    "models' self-descriptions predict their held-out behaviour better/worse than 40 observed behaviours do" is
    a quotable finding on its own.

If changes 1-4 are not adopted I would not fund it: the most probable output is a trend line produced by pool
composition and predictor familiarity, which commenters will take apart within a day. With them, this is the
highest-upside proposal in the cluster and worth roughly $300.
