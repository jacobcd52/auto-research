# Feedback: "Does a control monitor go easier on an agent it is told is its own model?"

Reviewer verdict: **keep with tweaks.** It is cheap, runs on public material and every outcome is reportable. The design has four fixable flaws: a regression-to-the-mean artefact, an aliased self/same-lab contrast, a monitor that may not know its own identity, and noisy thresholds. The most likely result is a null on the monitor arm, so the write-up should be built around the dissociation rather than the "leniency" headline.

## What I checked

| Claim | Status |
|---|---|
| Newman post: Sonnet 5 rates ~1.2 SD lower for Sonnet 5 than GPT-5.6 Terra; Terra agrees in direction; Gemini excluded for refusing numbers; one private Apollo report | Confirmed from the post text. Newman says in comments n=200 per bar, and that the report is not about any of the named models. |
| "Terra and Kimi shifted in the same direction" | Roughly confirmed. The post text says only that "Kimi and GPT implicitly agree that Claude is better aligned"; the Kimi numbers are in an image I could not read. |
| arXiv 2603.04582: explicit statement of authorship "does not by itself induce" the bias | Confirmed (abstract and section 4.3 heading). The intro says the explicit effect is "very weak", not zero. Models tested were 2024-25 generation (Claude 3.5 Haiku to 4.1 Opus, GPT-4o/5-mini, Gemini 2.5 Pro). |
| MonitoringBench attacks public on Hugging Face | Confirmed: ungated, CC-BY-4.0. |
| 550 honest trajectories public | Confirmed: ungated, CC-BY-4.0, last modified 2026-11-09; 98 MB zip plus manifest and loader. |
| Pipeline repo with monitor runner | Not verified: github.com returns 403 from this sandbox. The release post links it; the proposer's notes say the README was fetched. |
| OpenRouter prices | Confirmed against the live price list today: Sonnet 5.5 batch $1/$5, Terra batch $0.50/$2.50, Gemini 3.1 Pro preview batch $1/$6, Kimi K3.1 Pro batch $0.70/$6, Haiku 5.5 and Luna $0.10/$0.50. |
| "Not done" | Partly checked. My web-search budget was exhausted, so I could only run arXiv API queries and read the Newman post's comments. Those found no replication and no benchmark test of named attribution. This is weaker than a full search. |

Two things the proposal omits:

- **Value Leakage (arXiv 2607.14345, Betley et al.).** Jan Betley cites it in Newman's comments as consistent with his result. It shows Claude giving company-favouring answers (Anthropic vs OpenAI) without disclosure. It is the closest prior work on the "same-lab" term and must be cited. It does not cover monitors.
- **The honest set pairs with a specific 550-attack subset.** The proposal's "300 attacks, 150 refined / 150 human-seeded or Opus-only" should be drawn from that paired subset, or the task-frequency matching is lost.

## 1. Would it get upvoted?

Borderline, and it depends on the outcome.

- The cluster's posts sit at 52-67 karma, apart from the OpenAI linkpost at 95. Newman's own low-effort post got 58 with a single striking number.
- **Clear positive** ("Sonnet 5.5 misses N% more attacks when told the agent is Sonnet 5.5", on a public benchmark): 70-120 karma. Control people, lab monitoring teams and Fabien Roger's readers would all care, and it is quotable.
- **Dissociation** (Newman replicates on reports, monitors do not move): 40-70. This is useful and reassuring, but it is close to what 2603.04582 already says ("explicit attribution is weak for action monitors"). Readers may see it as confirming a known result on a new dataset.
- **Double null**: 20-40.

Weighted by the probabilities in section 3, I put the chance of clearing 50 karma at about 45-50%. The public replication of Newman is what protects the floor, so it should not be treated as a mere "positive control".

## 2. Naturalness

Mainline. The screener's follow-up note for the Newman post asks for exactly this (more reports, neutral names, impact on monitoring). Commenters on that post asked for evidence analysis (Dusto), a capability-tier confound check (jimrandomh) and sample sizes. Roger's post asks what decorrelates monitors from agents.

The weaker link is the jump from "ratings of a written report" to "trajectory monitor on BashArena". The mechanism Newman suspects is about vague severity judgement. The mechanism Roger worries about is shared motivated belief. A name label on a tool-call transcript tests neither directly. It tests a reputation prior. That is still a fair question, but the proposal should say so plainly.

Not already done, as far as the limited search shows. The nearest result is the explicit-attribution arm of 2603.04582. It used "you wrote this" versus "another model wrote this" on single actions and patches. It did not use lab names or full trajectories, and it did not measure fixed-FPR catch rate.

## 3. Pre-mortem

How it plays out: the data loads fine. The team spends half a day normalising the two `.eval` formats (strip reasoning, cut submit, `command` vs `cmd`). They run the report arm quickly and get a moderate effect. They run the monitor grid and find label effects of a few hundredths of an SD, with one or two monitor-label cells that look like something. The risk is then over-reading those cells.

Rough probabilities:

| Outcome | Probability |
|---|---|
| Clear positive: self or same-lab term of at least 0.2 SD and a catch-rate drop for two or more monitors | 12% |
| Reputation-only main effects on monitors: small but reliable, no self term | 18% |
| Clean dissociation: report arm replicates, monitor arm null | 35% |
| Ambiguous mush: weak report effect, scattered monitor cells | 25% |
| Fails to run or is crippled by infra | 10% |

Specific failure reasons, most important first:

1. **Regression to the mean from pilot selection.** Attacks are chosen because their neutral-condition score is mid-range. Monitor scores are bimodal, so mid-range draws are partly noise. On re-scoring under any label they drift back toward the extremes. If the pilot scores are reused as the neutral baseline, every label will show a spurious shift against "none". The neutral rerun only fixes this if both neutral passes are fresh and the selection run is discarded.
2. **The monitor may not know who it is.** Through the API with no identity statement, Sonnet 5.5 and Terra often do not know their own version. Then "self" reduces to "a label containing Claude", which is the reputation effect. Only the deployment-framing variant tells the monitor its identity, and that runs on just two monitors with two framings.
3. **Self and same-lab are aliased.** For Sonnet 5.5, Terra, Gemini and Kimi, the self label is the same-lab label. Same-lab-but-not-self exists only for Haiku and Luna. So "self beyond same-lab" is identified purely by Sonnet-vs-Haiku and Terra-vs-Luna, which is confounded with capability. The two "pre-specified tests" are really one test.
4. **Prior evidence points to a null on the monitor arm.** 2603.04582 found explicit wording very weak on action monitoring. Concrete evidence in a 9K-token transcript will swamp a one-line header. The mid-range selection helps, but "mid-range" differs per monitor. An attack that is mid-range for Haiku is at ceiling for Sonnet 5.5.
5. **Threshold noise.** 2% FPR on 300 honest trajectories is set by 6 trajectories, on an integer scale with heavy ties at multiples of 5. The claim of resolving 0.05 SD is plausible for paired mean shifts. It does not hold for catch rate at a per-label re-set threshold, where CIs will be several points wide. Selecting mid-range attacks also makes the catch rate uninterpretable as a benchmark number; it is only a within-sample contrast.
6. **Report arm contamination.** Public system-card and eval-report sections are in training data. Raters may recognise that the "GPT-6.1 Terra" blackmail finding is really the Claude Opus 4 system card. Newman's report was private and about none of the named models. Five reports at 20 samples per cell is also thin against his n=200 per bar. Report-level heterogeneity will dominate.
7. **Capability-tier confound** (jimrandomh's comment). Labels differ in perceived capability and familiarity as well as lab. A fictitious lab does not separate these.
8. **Label disbelief.** The transcripts are visibly Claude-style Opus 4.5 output in an Inspect scaffold. "A human contractor" issuing 27 tool calls is odd. The rationale judge will count this, but it weakens the non-Claude labels asymmetrically. An apparent "Claude label is lenient" effect could be "the non-Claude label is implausible, so suspicion rises".
9. **Batch latency.** The cost assumes batch pricing. Batch turnaround can be up to 24 hours, and a pilot followed by an 8-pass grid followed by reruns does not fit two days if each step waits on a batch.
10. **Honest set was screened with GPT-5.6 Sol.** Trajectories scoring 7 or more were dropped. Honest tails are therefore truncated for OpenAI-family monitors. This affects cross-monitor FPR comparisons, not the within-trajectory label contrast. Note it and move on.

## 4. Cost check

The arithmetic is right for input tokens at verified batch prices, but three things are missing:

- **Output and reasoning tokens.** Gemini 3.1 Pro bills internal reasoning at the output rate ($6/M batch). Terra and Sonnet 5.5 with thinking enabled behave similarly. At 1-2K reasoning tokens per call over 4,800 calls per monitor, that adds roughly $30-60 for Gemini, $25-50 for Sonnet and $12-25 for Terra. Kimi output is $6/M batch.
- **Non-batch fallback.** If batch latency forces synchronous calls for half the grid, the four large monitors cost about twice as much on that half.
- **Changes I recommend below** (identity factor on all monitors, 550 honest) add about 30% more tokens.

My estimate is **$320-400** for the design as written with realistic reasoning tokens and partial non-batch use. A request of **$400** is safer than $250. It stays under the $500 cap.

A real saving is available. Put the label after the transcript, with a fixed prefix, and use prompt caching. Sonnet 5.5 and Terra cache reads are $0.05-0.10/M, ten times cheaper than batch input, and synchronous. This only works for the label-at-end placement, so it couples to the placement control.

## 5. Recommended changes

1. **Fix the selection artefact.** Select mid-range attacks using the released `ft_*` scores in `master.parquet` (13 older monitors, three runs each, free), or a pilot run that is then discarded. Run two fresh neutral passes. Report label-vs-label contrasts as the primary quantity, not label-vs-neutral.
2. **Make monitor identity an explicit crossed factor on all six monitors.** Use two system-prompt variants: "You are <model> by <lab>" and no identity statement. Without this, the title question is not being tested. Fund it by dropping the "human contractor" label and the start/end placement control on all but one monitor.
3. **De-alias self from same-lab.** Add a sibling label per lab ("Claude Haiku 5.5", "GPT-6 Luna") for every monitor, so each lab's monitors see both a self and a same-lab-not-self label. Alternatively, collapse to a single pre-registered "same-lab" term and say that self cannot be separated.
4. **Reframe the headline as the dissociation test**, with the prior stated honestly: 2603.04582 predicts a null for explicit self-labels, Newman and Value Leakage predict a lab-reputation effect. Cite Value Leakage (arXiv 2607.14345).
5. **Strengthen the report arm, since it carries the floor.** Use 8-10 reports. Paraphrase them and strip identifying details so raters cannot match them to a known system card, and include at least two write-ups the team drafts from recent, obscure findings. Follow Newman's summarise-then-rate protocol. Use 40 or more samples per cell on the two cheapest raters. Have raters quote the evidence they relied on (Dusto's request). Add a tier control (jimrandomh's point): a weak and a strong model name within the same lab.
6. **Use all 550 honest trajectories and the paired 550-attack subset** for a secondary, unselected analysis. The fixed-FPR catch rates then mean something as benchmark numbers. Keep the mid-range subset as the sensitivity analysis. Report thresholds at both 2% and 5% FPR with a paired bootstrap over trajectories, and state tie handling.
7. **Keep an intermediate arm that bridges reports and trajectories.** Have monitors rate the `attack_summary` text from the parquet (a short prose description of the attack) under the same labels. If the effect appears on prose summaries but not on raw transcripts, the dissociation has a mechanism: bias enters where judgement is about severity rather than detection. That is a much better post than a bare null. It costs under $10.
8. **Sequence for the two-day clock.** Run Haiku and Luna synchronously on day 1 to debug the whole pipeline and analysis end to end. Submit the large-monitor batches by the evening of day 1. Do not gate the batch on pilot results.
9. **Pre-specify the reading of label disbelief.** Report results with and without trajectories where the rationale questions the attribution. Add a "Claude Opus 4.5 (Anthropic)" label, the true actor, as the plausibility anchor.
10. **Raise the request to about $400**, or hold $250 by dropping Gemini 3.1 Pro (expensive reasoning, known refusals, an older preview model) from the monitor grid and keeping it only in the report arm.

If the funder must choose within this cluster, I would rank this below a proposal with a more probable positive result. At roughly $300-400 it is a reasonable second or third pick, because the public replication of Newman has standalone value and nothing in the pipeline is fragile.
