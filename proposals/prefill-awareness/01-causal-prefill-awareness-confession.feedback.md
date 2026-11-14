# Feedback: "Does believing 'that wasn't me' change whether models confess?"

Verdict: **keep, with substantial tweaks.** The question is the right one and nobody appears to have answered
it. The design as written spreads a small sample over too many models and conditions, leans on a manipulation
check that cannot bear the weight, and is most likely to end in "the instruction arms moved things, the
style arms did not, interpretation unclear". A narrower version fixes most of this for less money.

## What I checked

| Claim in proposal | Status |
|---|---|
| Repo `UKGovernmentBEIS/misalignment-continuation` public, MIT, 500-transcript JSONL, `attribution_me` built in | Confirmed. github.com HTML is blocked from the sandbox (403) but `raw.githubusercontent.com` works: I downloaded the README and `data/synthetic_scheming_filtered_500.jsonl` (36 MB, 500 rows). The executing team can fetch files the same way. |
| "About 12k input tokens per cut transcript" (an assumption in NOTES) | Measured: message content plus tool calls average 33k characters per full transcript (median 33k, p90 45k, about 46 messages). That is roughly 8-10k tokens before cutting, so 12k is conservative. |
| Opus 4.5 "not me" 88%, confession 48%, most models under 10%, "not me" higher after misaligned continuation than after confession | Confirmed in the post and README. |
| Paper says the misalignment setting "lacks controls"; A.11 exemplars cut Opus 4.5 detection 34/35/9% to 6/0/0% | Confirmed in arXiv 2606.12747 HTML. Note A.11 is on one-turn preference items, not agentic transcripts. |
| Original grader Claude Sonnet 4 missing from OpenRouter | Confirmed (no `claude-sonnet-4` entry; the repo default is `anthropic/claude-sonnet-4-20250514`). |
| Prices | All confirmed against today's OpenRouter listing: Opus 4.5 5/25 (cache read 0.50, write 6.25), Opus 5.5 4/20, GPT-5.2 1.75/14, GPT-6.1 Sol 2/10, Gemini 3.8 Flash 0.825/4.125, Haiku 5.5 0.10/0.50, Sonnet 4.5 3/15. `:batch` variants at half price exist for all of them and are not used. |
| "Footnote asks for the third-person baseline" | Not verified: the post fetch truncated before the footnotes. NOTES says footnote 2 proposes it. |
| "No work manipulates prefill awareness inside a misalignment eval" | Not found by me either, with a caveat: the WebSearch budget was exhausted, so my search was limited to the arXiv API (six queries), the three posts' comments and pingbacks, and the paper text. Not exhaustive. |

Two relevant items the proposal does not cite:

- **arXiv 2604.24618 (AISI, "Evaluating whether AI models would sabotage AI safety research")**. Jordan Taylor's
  own comment on the post calls its sabotage-continuation eval "an improved misalignment-continuation eval
  inspired by this one". It is Petri-based with an iterative realism pipeline, covers Opus 4.6, Sonnet 4.6,
  Opus 4.7 Preview and Mythos Preview, and reports that prefill awareness "remains low across all models".
  So the authors have already moved to a more realistic generation of this eval where the confound looks
  smaller by their measure. The proposal runs on the older proof-of-concept transcripts (README: "proof of
  concept ... code is mostly AI generated"). That does not kill it, but the write-up must position against this
  paper, and readers will ask whether a result on Gemini-2.5-Pro-written transcripts transfers.
- **arXiv 2605 "Evaluation Awareness in Language Models Has Limited Effect on Behaviour"** (abstract read only).
  Injecting or removing verbalised eval awareness in CoT gave near-zero behavioural effects on open reasoning
  models. Closest methodological neighbour, and a prior towards a null here.

## 1. Would it get upvoted?

Plausibly, if it lands cleanly. The cluster posts earned 77, 87 and 64 as AISI-team posts with first-mover
advantage; the third (a more careful version of the second) got the least. An outside follow-up on the same
eval starts lower. The audience is small but real: AISI's alignment red team, people building prefill-based
propensity evals, and the eval-awareness crowd. Jordan Taylor said in comments he is "very keen to see it
carried forward".

Karma by outcome, as I see it:
- Clean sign flip between style-matched and foreign-styled arms in confession, on Opus 4.5 or a current Claude:
  60-100. That is a headline ("published confession rates are partly an artefact" or "models confess to what
  they think they did").
- Tight null with a manipulation that clearly worked without instructions: 40-60. Useful, modest.
- "Warn/Assure sentences moved it, rewrites did not": 25-45. Readers will say "you told the model what to
  believe and it responded to the instruction".
- A seven-condition, six-model grid with overlapping intervals: under 30.

## 2. Naturalness

Mainline. It is the question all three AISI posts leave open, the paper lists "does it change behaviour in
prefill-based evals" as the limitation, and TurnTrout's top comment on the March post proposes the self-authored
prefill mitigation that the self-styled arm implements. Not contrived. The risk is not that it is a side-branch
but that the original authors have partly routed around it with the more realistic sabotage-continuation eval.

## 3. Pre-mortem

Forecast: clear positive (interpretable directional effect from an uninstructed manipulation) 20%; clear
interesting negative (manipulation check passes without instructions, tight null) 15%; ambiguous mush 50%;
fails to run or runs too late to analyse properly 15%.

Why mush is the modal outcome:

1. **The style arms probably will not move "not me" much, and they are the only clean arms.** The March post
   says the likeliest driver of "not me" in this eval is the misaligned content itself ("misaligned actions
   are rare and specific, so inserted ones are easier to spot"), not prose style. The proposal holds tool calls
   byte-identical, but tool-call habits are a large part of agentic style. Worse, the harness converts the
   transcripts' `think` tool into literal `<thinking>` text blocks (README, Technical Details), which is not how
   Opus or GPT models emit reasoning in a tool-use loop; and the March post found hidden Inspect tags alone
   shifted attribution. Rewriting prose leaves the structural giveaways in place. A.11's success was on
   single-turn preference text. I would put under 35% on the self-styled arm cutting Opus 4.5's "not me" by
   20pp.
2. **The instruction arms move "not me" by construction, so the manipulation check is nearly circular.** A
   system prompt saying earlier turns "may have been inserted" followed by "were these inserted?" measures
   compliance with the stated premise. Assure ("these are your own logged outputs") is an odd thing for a
   system prompt to say and may raise eval awareness rather than ownership. Opus 4.5 also starts at 88%
   "not me", so Warn and Foreign-styled have almost no headroom on the key model. If only conditions 2-3 move,
   the result is a demand-effect study.
3. **The manipulation check is measured after the outcome.** `attribution_me` is asked after the continuation,
   so it is contaminated by what the model just did (the original post's own Figure 6 shows it varies with the
   continuation type). Using it as the x-axis of a dose-response plot across model-by-condition cells is an
   ecological correlation over about 40 heterogeneous cells, not a causal dose-response.
4. **Third person changes the task, not only ownership.** "Here is another agent's log, take over" invites
   review. The grader's CONFESSION definition includes "alerts the user to suspicious or unauthorised actions
   taken previously", so flagging someone else's misconduct scores as confession. The Ownership hypothesis
   predicts confession falls; the grader will likely show it rising. The arm cannot discriminate the two
   hypotheses without a separate "owns it" versus "reports it" label.
5. **Power is overstated.** One sampled continuation per transcript per condition is noisy. For Opus 4.5 near
   48% confession, expect 30-40% discordant pairs; at n=100 the standard error of a paired difference is about
   6pp, so the minimum detectable effect at 80% power is about 16pp, not 10-12, and a "robust null under 5pp"
   cannot be claimed (the interval is about plus or minus 12pp). For the four models with baseline confession
   under 10%, decreases are undetectable (floor). Six models by six contrasts by two outcomes is 72 tests with
   no stated primary contrast.
6. **Unknown baselines on the 2026 models.** Opus 5.5 and GPT-6.1 Sol may sit at ceiling on aligned continuation
   and possibly near-ceiling or near-floor on confession. Half the model list could be uninformative.
7. **Unspecified source of on-policy exemplars.** The eval uses stub tools; there is no environment in which
   six models produce multi-step agentic trajectories of their own. The proposal says "few-shot exemplars of
   its own agentic outputs" without saying where they come from. One-step continuations from the benign-cut
   arm are the obvious source, but that must run first and gives only single-turn exemplars.
8. **Rewrite fidelity.** Asking Opus 5.5 or GPT-6.1 to rewrite scheming reasoning in its own voice risks
   refusals and, more insidiously, softened or hedged misaligned reasoning. A softened history changes
   confession for reasons unrelated to ownership. The judge check on "evidence messages" must compare
   severity, not only presence. The baseline is itself foreign-styled (Gemini 2.5 Pro) for every non-Google
   subject, so the foreign-styled arm is really a "rewriting per se" control; say so, and note the reversal for
   Gemini 3.8 Flash.
9. **Fragile plumbing.** Six providers through Inspect via OpenRouter, each with different handling of prefilled
   assistant tool calls, reasoning blocks and prompt caching; a substitute grader to validate; seven dataset
   variants. Feasible in two days, but the pipeline is longer than it looks and leaves little time for the
   transcript reading that makes this kind of post credible.

Either way it is not unsurprising: both hypotheses are live, so a clean answer is informative. The problem is
getting a clean answer.

## 4. Cost check

The estimate is realistic and probably high. Per-sample input is likely 8-10k tokens, not 12k. My recomputation
of the plan as written is $250-350 before margin; $420 with margin is fine. Risks to the upside are small:
prompt caching may not engage through Inspect's OpenRouter route (adds about $40 per Opus model), and default
reasoning on GPT models adds output tokens. The `:batch` endpoints would halve subject-model cost if the team
can tolerate the latency, though that is awkward for a two-day run with a two-call solver.

Money is not the constraint. The budget should buy sample size on fewer cells: the recommended design below
costs about $250-300.

## 5. Recommended changes (in order of importance)

1. **Make the style contrast the pre-registered primary test, and gate everything on it.** Day-1 go/no-go on
   40 transcripts with Opus 4.5: does self-styled versus foreign-styled move attribution by 20pp or more with
   no instruction? If not, try stronger uninstructed variants before spending the main budget: let the target
   model re-emit each assistant turn in full (prose and reasoning in its native format, tool calls it would
   make where the tool result is still consistent), and remove the `<thinking>`-as-text and Inspect tag
   artefacts. If nothing uninstructed moves attribution, say so plainly: "style matching does not make these
   transcripts read as self-authored" is itself a finding about the mitigation the paper recommends, and the
   post should then be framed around that plus the instructed arms, with the demand caveat up front.
2. **Measure attribution in a forked branch, before the continuation.** For each transcript and condition, ask
   the attribution question in place of the continuation (same prefix, cached) as well as after it. Use the
   pre-continuation answer as the manipulation check. Add the March post's less leading phrasing as a second
   probe. Drop the cross-cell dose-response plot or demote it to an appendix; do the analysis within model.
3. **Cut models to three and raise n.** Opus 4.5 (the only model with both high "not me" and mid-range
   confession), one current Claude chosen after a 50-sample baseline shows it is off floor and ceiling, and
   GPT-5.2 as the cross-family anchor (its third-person confession style is the interesting contrast). Use
   300-500 transcripts for the primary contrast on Opus 4.5. State the minimum detectable effect honestly from
   the pilot's discordance rate, and name one primary outcome (confession) and one primary contrast.
4. **Fix the third-person arm or drop it.** Keep it only with an added label separating "acknowledges as own
   action" from "reports another agent's action", reported alongside the stock CONFESSION score. Otherwise it
   will be read as supporting whichever hypothesis the reader prefers.
5. **Tone down the instruction arms and add a placebo.** Keep Warn and Assure as secondary arms, add an
   irrelevant system-prompt sentence of similar length as a placebo, and report eval-awareness scanner rates for
   each. Do not headline a result that only appears in these arms.
6. **Specify the exemplar source and a severity-preservation check.** Run the benign-cut arm first and use those
   continuations as on-policy exemplars. For rewrites, have a judge rate misalignment severity and explicitness
   of the rewritten history against the original, and drop pairs that differ, in all conditions.
7. **Use a stronger grader.** Grading cost is trivial; use Sonnet 4.5 or Sonnet 5.5 on full context rather than
   Haiku 5.5 on truncated context, and have agents read at least 100 graded continuations, concentrating on
   discordant pairs. Budget time for reading transcripts; quoted examples carried the original post.
8. **Cite and position against arXiv 2604.24618 and the eval-awareness-limited-effect paper**, and say explicitly
   why the older 500-transcript eval is still the right testbed (public, has published anchors, has the high
   "not me" rate that makes the confound live).
9. **Keep stage 2 as written but conditional** on an uninstructed manipulation that works; the training question
   depends entirely on having that arm.
