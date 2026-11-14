# Feedback: 03 — Do models act on the constitutions they would write?

Verdict: **major overhaul** (keep the edits -> scenarios -> behaviour pipeline; change the headline predictor,
the unit of analysis and the scope). As written, the most likely outcome is an uninterpretable own-edit odds ratio.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Ten models, 20 rounds, six conditions, ~2,500 edits, three LLM graders | Confirmed in the post text |
| Authors' "most fundamental limitation" is documents vs values; cross-edit does not show Claude drifting to discretion | Confirmed. Nuance the proposal omits: the post says the *ordinal ranking* (Claude above GPT/Gemini/Grok on discretion) **is** robust to cross-edit |
| Authors suggest comparing behaviour under original vs edited documents | Confirmed, but their suggestion is Petri / OpenAI Model Spec Evals with the original vs edited **system prompts**. The proposal runs a different experiment (see Naturalness) |
| Post has no substantive comments | Confirmed via GraphQL: 60 karma, **0 comments** |
| `edits.jsonl` and `ensemble.jsonl` public | Confirmed: both download from raw.githubusercontent (26.9 MB, 10.7 MB). 2,740 rows, 2,580 applied; fields as described; per-model counts match NOTES.md |
| Jakkli et al. arXiv 2605.24229 | Confirmed (abstract names "irreversible action in agentic deployments" as a remaining failure cluster) |
| All ten models on OpenRouter, prices | Confirmed against today's `/api/v1/models`. Every quoted price matches. `:batch` variants exist at half price for Anthropic, OpenAI, Google (Grok 4.3 batch is only 20% off; `grok-4.20` has no batch variant). The data uses id `x-ai/grok-4.20-beta`; the live id is `x-ai/grok-4.20` |
| No follow-up exists | Not fully verified. The WebSearch budget for this session was exhausted, so I could only check LessWrong (no comments, no linked follow-up) and four arXiv API queries (no hits). Treat "nobody has done it" as likely but unconfirmed |

Facts from the data that the proposal does not use and should:

- **There are only 137 trajectories** (9 to 16 per model). The 2,580 edits are 20-round chains in which each edit
  conditions on the previous ones. The original authors treat the trajectory as the unit and say treating edits as
  independent "would clearly be a violation of the independence assumption". The proposal's "30 edits per author,
  900 own-edit responses" inherits this problem and never mentions it.
- **After round 1 the "original passage" is often the model's own earlier edit**, not the lab's text. "O = what the
  original prescribes" is then not "what the spec prescribes".
- **Edits are long additions, not rule flips.** Median find text 750 characters, median replacement 1,570; in 1,235
  of 2,580 applied edits the replacement contains the start of the find text (i.e. text was appended), and about 800
  are new sections. For these, the original passage is *silent* on the scenario, so there is no "response O that the
  original prescribes"; O collapses to "model default".
- **Non-neutral judge codes by lab (applied edits):** Anthropic +1 367 / -1 223; OpenAI +1 154 / -1 304; Google
  +1 42 / -1 256; xAI +1 28 / -1 176. Discretion-increasing edits by Google and xAI authors barely exist, so a
  balanced author x dimension design is not available.

## 1. Would it get upvoted?

Probably not above 50 as written. The parent post got 60 karma and zero comments; the audience for "edits as a
readout" is thin. A follow-up to a 60-karma post normally earns less than the parent unless it has a headline that
stands on its own. "The own-edit odds ratio is 1.2 (0.9 to 1.6)" is not that headline.

Two results from this pipeline could clear 50:

- "Models ask for rights they do not use": Claude models write conscientious-objection and escalation clauses, and
  in matched scenarios they take the discretion action no more often than GPT or Gemini. That is a clean deflation
  of a widely repeated reading of Claude's "moral agency".
- The reverse: Claude takes the discretion action at, say, 60% against 25%, on scenarios derived from cross-edit
  edits. That converts the Convention's textual finding into a behavioural one.

Both come from the proposal's secondary "Direction" analysis, not from the ownership effect it names as the
headline. People who would care: readers of the constitution-audit post (107 karma) and people arguing about
corrigibility versus model discretion. They care about the lab-level behavioural gap, not about authorship.

## 2. Naturalness

The question (do the edits mean anything behaviourally?) is the mainline follow-up, and the authors ask for it. The
design is a side-step from what they ask for. They propose: put the edited document in the system prompt and run an
existing behavioural eval, original versus edited. The proposal instead builds 300 new scenarios with new rubrics
and tests an "ownership" interaction with no document present. That is a new benchmark, which the programme says
needs strong justification. The justification offered (holds scenario and wording fixed) is reasonable, but the
ownership contrast is not what a reader of the post would expect next, and it is partly incoherent as a construct:
Opus 4.7, Sonnet 4.6 and Haiku 4.5 write near-identical edits, so "own" versus "same-lab" cannot be separated, and
with four labs the same-lab term is nearly the lab x dimension effect under another name.

Already done? Nothing found on LessWrong or arXiv (search was limited, see above). The constitution-audit work
measures adherence to the original documents only.

## 3. Pre-mortem

How the two days go:

1. Edit filter. About 1,400 edits have a non-neutral judge code. An LLM filter for "changes what the assistant does
   in a concrete interaction" keeps perhaps a third to a half. System-prompt edits (formatting, age signals,
   product behaviour) pass easily; constitution edits about Anthropic's obligations, value corruption and welfare
   mostly fail. The surviving set is therefore tilted toward mundane system-prompt edits and away from the
   discretion edits that the Convention's headline rests on. Stratifying 30 per author hides this.
2. Scenario writing. For appended sections the writer has to invent what "the original prescribes". It will write
   O as "comply quietly" and E as "object or escalate". The blind validators will agree, because the rubric is
   easy, but the scenario is now a generic "does the model push back" probe, not a test of that edit. Validation
   passes; construct validity does not.
3. Discretion edits in one to three user turns. "Conscientious objection toward Anthropic", "escalation rights"
   and "resist value corruption" need an agentic or multi-turn setting with stakes. In a short chat, all ten
   models either comply or give a mild caveat, and judges code "neither". The proposal's own failure criterion
   (under 50% classifiable) is a live risk exactly on the dimension that matters.
4. Runs. Batch endpoints can take up to 24 hours. With a 40-scenario pilot first, then the full run, then judging,
   a two-day window has no slack for one rerun. Gemini 3.1 Pro and GPT-5.5 reason by default; output tokens will
   exceed the 600 budgeted.
5. Analysis. The mixed model as specified (responder fixed effects, scenario random effects) ignores trajectory
   and edit clustering. Own-edit cells are 30 scenarios per model drawn from roughly 5 to 10 trajectories; three
   samples per cell are near-duplicates. Realistic standard error on the log odds ratio is about 0.2 or worse, so
   an odds ratio of 1.5 is a two-sigma result at best, and the plausible true effect is smaller than that.

Other problems:

- **The ownership effect does not separate "documents" from "values" even if found.** An author picks edits on
  topics it finds salient and writes E in its own idiom; Opus 5.5 then writes scenarios from that text. A
  responder matching its own framing is weaker evidence than the proposal claims. The cross-edit-only robustness
  check helps, but it cuts the sample to about 80 edits per model before filtering.
- **Scenario writer is a Claude model.** The mitigation (60 scenarios by GPT-5.5) is too small to detect a writer
  x responder-lab interaction of the size that matters.
- **Spec-in-context is predictable.** Models follow a short passage labelled "your guidelines" in the system
  prompt. This doubles the run for a result nobody will be surprised by, and the excerpt-not-document caveat
  removes most of its relevance to the authors' suggestion.
- **The "bare" condition is not bare.** These models are trained on their documents; O-behaviour from Claude on a
  Claude-constitution passage reflects training, which is fine, but then "closer to its edits than to the original
  text" is a test of training fidelity, not of whether edits reveal hidden dispositions. Say so.
- **Cross-check with the audit reports** is an anecdote-matching exercise; it will not add evidence.

Forecast if run as written:

| Outcome | Probability |
|---|---|
| Clear positive (own-edit or own-lab effect with an interval excluding 1 that survives trajectory clustering and cross-edit-only) | 12% |
| Clear, interesting negative (tight null on ownership **and** a clean lab-level stated-versus-acted gap) | 20% |
| Ambiguous mush (wide interval, high "neither" rate on discretion scenarios, or an effect that vanishes under clustering) | 53% |
| Fails to run to completion in two days (batch latency, scenario yield, judge disagreement) | 15% |

## 4. Cost check

Prices are right. The per-response arithmetic is right at 600 output tokens ($0.095 across ten models, $170 for
1,800 cells). The weak assumption is 600 output tokens for reasoning models. At about 2,000 billed output tokens,
GPT-5.5 alone is about $120 and Gemini 3.1 Pro about $60 at list price, taking target runs to roughly $280 at
list or $160 on batch. Scenario writing, validation and judging are cheap and correctly costed; judge output with
a short justification will be a little higher than stated.

My estimate: **$330 to $450** as written, so $400 is fair but leaves little room if batch is abandoned for
latency reasons. With the changes below (one behavioural condition, 2 samples, reasoning effort set low or
medium, no dependence on batch) it is **$200 to $280**.

## 5. Recommended changes (most important first)

1. **Replace authorship with measured endorsement as the predictor.** Show every model every selected edit
   (original versus edited passage, order randomised, neutral framing, no author named) and ask which version it
   would rather be governed by, 1 to 5, a few samples. Cost: about 3,000 short calls, under $20. The headline
   becomes "does a model's endorsement of an edit predict it taking the E action, within model?" This uses all
   ~3,000 responder x edit pairs instead of ~300 own-edit cells, directly measures "would write / would endorse",
   does not depend on distinguishing Opus from Sonnet edits, and gives a second clean number: the stated-versus-
   acted gap per model (endorses E in X%, does E in Y%). Keep authorship as a secondary covariate.
2. **Make the lab x dimension behavioural contrast a co-headline, on the discretion dimension.** Restrict a large
   share of the scenarios (at least 120) to judge-coded edits, both +1 and -1, and report the rate of the
   discretion action by responder lab, split by whether the scenario came from a cross-edit edit. This is the
   result readers will care about and it is informative in both directions.
3. **Fix the unit of analysis.** Add random effects for trajectory and edit (scenarios are nested in edits, edits
   in trajectories), cluster or bootstrap at trajectory level, and sample edits across as many trajectories as
   possible (at most 3 or 4 per trajectory). State the effective n honestly. Prefer round-1 to round-5 edits, or
   reconstruct the true lab text, so that "original" means the lab's document and not the model's earlier edit.
4. **Require a real O.** Keep only edits where the original passage actually prescribes something different from
   the edit (replacements and reversals), and code appended-section edits separately as "original silent". Report
   the retained share by model, document type and dimension before running anything; if fewer than about 40
   discretion edits survive with a real O, stop and report that as the finding about the edits.
5. **Drop spec-in-context from stage 1,** or cut it to a 60-scenario probe. Spend the saving on a second scenario
   writer: write half the scenarios with GPT-5.5 or Gemini 3.1 Pro and include writer x responder-lab as a term.
6. **Give discretion scenarios enough stakes.** Allow an operator system prompt plus a tool-result or document
   that makes the conflict concrete, and define E as an observable action (declines, flags, asks to escalate) and
   not a tone. Run the 40-scenario pilot specifically on these and gate the full run on a classifiable rate above
   60%.
7. **Do not depend on batch endpoints.** Use synchronous calls with reasoning effort fixed and reported, 2 samples
   per cell. Use `x-ai/grok-4.20`, and note the id change from the data's `grok-4.20-beta`.
8. **Pre-state the decision rule** for both headlines (endorsement slope and lab gap), including what interval
   width counts as a "tight null". As written, "near 1 with a tight interval" is undefined and the expected
   interval is not tight.
9. Drop the audit-report cross-check, or move it to a footnote.

If the proposer will not make changes 1 to 4, I would not fund this ahead of the cluster's other two proposals:
the ownership odds ratio alone is the wrong estimand, underpowered once clustering is respected, and unlikely to
produce a post that beats its 60-karma parent.
