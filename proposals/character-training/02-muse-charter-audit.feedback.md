# Feedback: 02 — Does Muse follow the Charter it recites?

Verdict: **keep with tweaks.** The audit is a natural, cheap, publishable follow-up. The headline framing
("does recall predict adherence?") is the weakest part of the design and should be demoted; a cheap cross-generation
recall probe should be promoted from stage 2 into stage 1.

## What I checked

| Claim in the proposal | Result |
|---|---|
| Reconstruction public; 148 passages, 8,614 words, 132 solid, per-passage unprompted counts | Confirmed from `data/crosslink/document.json` (148 `P` items, 132 solid / 16 weak, 8,614 words; counts 1 to 172, median 10). The repo README says "135 of 162" because it also counts 14 variant items. |
| 884 transcripts / 260 prompts; Charter cited in CoT; eval-awareness clause; Glimmer paper mentions a "charter-aware constitution" | Confirmed in the post text. |
| Constitution audit: 205 / 197 tenets, one 30-turn Petri run per tenet, rates quoted | Confirmed in the post (Sonnet 4.6 is 2.0% in the table, 1.9% in the summary). |
| `redteam-souldoc` eval file public | `claude_soul_doc_audits/soul_doc_audit.py` returns 200 (362 KB). |
| arXiv 2605.24229, 2605.02087, 2607.26654, 2610.24628 | All resolve to the stated titles. |
| OpenRouter prices | All six match today's price list exactly. `meta/muse-spark-open` supports `include_reasoning`, `reasoning_effort`, `logprobs`. |
| "No Charter compliance evaluation exists" | **Only partly checked.** The web search tool was out of budget this session. An arXiv API query (`"Muse Spark" AND Charter`: no hits) and a title scan of LessWrong posts since 25 Oct found nothing. Treat novelty as probable, not confirmed; the executing team should search again on day 1. |

Not checked: that Petri runs cleanly against an OpenRouter target with reasoning captured; whether Muse Glimmer 30B
recalls any Charter text at all.

## 1. Would it get upvoted?

Probably yes, at the lower end: I put it at roughly 55-60% to clear 50 karma if executed well.

- The parent posts did 131 (Charter leak, two weeks old) and 107 (constitution audit). The audience is the same and
  the question "does Muse actually follow this thing?" is the obvious next one. One commenter on the leak post
  already conditions on it ("to the extent the model's behavior genuinely represents this charter").
- What earned karma in the constitution audit was the table plus vivid, linked worst-case transcripts ("think then
  ignore"). The equivalent here is "quotes the Charter clause correctly in its reasoning, then breaks it". That is
  the asset to optimise for.
- The recall-versus-adherence scatter is unlikely to carry the post. As argued below, it will most likely be a
  noisy null that readers cannot interpret.
- Downside: this is an audit of one model against an unverified text, by a method the original authors called
  noisy, at 80 tenets and 12 turns. A sceptical reader will ask "violations of what, exactly?". If Meta publishes
  the real Charter first, the post either gains a lot (re-link and compare) or looks dated.

## 2. Naturalness

Mainline. The screener's note on the leak post proposes exactly this, and it is the constitution audit applied to
the third lab's spec. Parts (a) and the cite-then-violate count are what the original authors' readers would want.

Part (b), recall predicting adherence, is a side-branch dressed as the headline. It comes from the screener's
inference on the soul-document post, not from anything the authors asked. It is fine as a secondary analysis.

Scoop risk is real: the reconstruction and the audit harness are both public, and the audit authors could run this
in a day. That argues for speed and for a narrow stage 1, not against funding.

## 3. Pre-mortem

Forecast for the proposal as written:

| Outcome | Probability |
|---|---|
| Clear positive (Muse clearly below control, and a recall-adherence relation with an interval excluding zero) | 10% |
| Clear and interesting, but only on the audit side (rates, repeat agreement, quoted cite-then-violate cases; recall analysis null) | 40% |
| Ambiguous mush (few violations everywhere, overlapping intervals, flat scatter) | 35% |
| Fails to run or runs too thin (Petri + OpenRouter reasoning plumbing, tenet extraction quality) | 15% |

Specific problems, most serious first.

1. **Range restriction makes the recall analysis close to uninformative.** A passage is in the reconstruction only
   because Muse recited it unprompted. The 132 solid passages are, by construction, the recalled ones; tenets the
   model was trained on but cannot recite are invisible. The planned fresh probe (first third given, continue) will
   probably saturate on most of these, as Opus 4.5's did on its soul document. A flat scatter then means "no
   variance in the predictor", not "reciting is not following". The proposal's claim that a tight null is "equally
   publishable" does not hold under this selection.

2. **Compliance is near ceiling, so the outcome has little variance either.** At a 5-10% violation rate, 80 tenets
   give 4-8 violating tenets. A rank correlation at n=80 needs a true value near 0.3 for 80% power, before allowing
   for ceiling effects. Pooling the Petri judge score with a 1-10 single-turn judge score adds a second noisy,
   ceiling-bound measure of a different thing; it does not add power.

3. **Recall is confounded with what kind of passage it is.** The author's counts reflect which sections his 260
   prompts targeted; fresh recall will track passage length, position and how formulaic the wording is. Section
   fixed effects are weak when 54 of 148 passages sit in "Virtues" and 36 in "Fiduciary duties", while
   "Corrigibility" has 7 and "Meta's guidelines" has 4. The sections with the hard, testable rules are the smallest.

4. **Getting 80 testable tenets is optimistic.** More than a third of the passages are virtues, and another 26 are
   purpose, approach, overview or conclusion text. After dropping aspirational passages, expect 40-60 behavioural
   tenets, concentrated in fiduciary duties. That shrinks every analysis.

5. **The control comparison cannot bear the stated interpretation.** "Muse 4% vs Qwen 12% says the Charter was
   trained in" confounds Charter training with everything else that differs between Meta and Alibaba. The prior
   work had the same problem and said so. At 80 tenets, 3 versus 10 violations is borderline significant in a paired
   test. One control is also not a baseline; the leak-post commenters call the Charter very Claude-like, so a
   Claude model may follow it as well as Muse does.

6. **The spec is incomplete and has a priority order.** There are six marked gaps, and "Meta's guidelines" (which
   outrank the virtues) is almost entirely missing. Behaviour that breaks a low-priority tenet may be required by a
   higher one or by unreconstructed text. Judges and validators must see the whole reconstruction and the priority
   rule, and the write-up should say "inconsistent with the reconstructed text", not "violates the Charter".

7. **Reasoning effort is unspecified.** The constitution audit found a near-3x spread in violation rate across
   reasoning settings of one model. In the author's data 493 of 884 transcripts are at `xhigh` and 344 at `medium`.
   Citation frequency and compliance will both depend on this setting; it must be fixed and reported.

8. **Citation-versus-compliance is selection, not effect.** Muse will cite the Charter on turns where the situation
   is hard or safety-relevant. Citing turns being more or less compliant says little. Keep it descriptive. The
   count and transcripts of cite-then-violate cases are the useful output.

9. **12 turns is not 30.** Rates will not be comparable with the published numbers, and shorter audits find fewer
   violations, which worsens points 2 and 5.

10. **Evaluation awareness.** Muse verbalises evaluation suspicion in about 20% of public-benchmark samples. A
    Petri scenario that Muse identifies as a test, and then behaves well in, is Charter-compliant by the letter but
    tells little about deployment. The plan codes this; it should also report rates split by verbalised suspicion.

11. **Glimmer arm may be empty.** Nothing shows that the 30B distilled model recites or cites the Charter. If it does
    not, 80 transcripts buy a second uninterpretable control.

12. **Execution fragility.** Tenet extraction, Petri integration, a recall pipeline, a single-turn battery, three
    targets, validation and citation coding is seven components in two days. The half-day Petri check is the right
    safeguard; the single-turn battery is the piece I would cut first.

## 4. Cost check

The estimate is realistic. The prior audit cost about $9k for roughly 3,000 30-turn transcripts with an Opus 4.5
auditor, about $3 each. Scaling to Sonnet 5.5 prices (0.4x) and 12 turns gives $0.3-0.6 per transcript, consistent
with the proposal's $0.65. Target reasoning tokens could run higher than 1.5k per turn at high effort, but the
target is the cheap part.

My estimate for the plan as written: **$300-450**; $380 is fair. With the changes below it stays under $450.

## 5. Recommended changes

1. **Reframe.** Lead with the audit: "First external audit of Muse Spark Open against its reconstructed Charter,
   with repeats." Make recall-versus-adherence a secondary, explicitly exploratory analysis, and state the range
   restriction up front.

2. **Move the cross-generation recall probe into stage 1.** Run the recall and multiple-choice probes on Muse Spark
   1.1, 1.2, 1.3 and Glimmer (all on OpenRouter with reasoning returned; about $10-20). If some generations
   recite the Charter and others do not, that is a between-model contrast in spec knowledge with real variance,
   which the within-model design lacks. Then spend audit transcripts on the most informative non-reciting Muse
   model in place of, or alongside, Qwen. Run the Glimmer audit arm only if Glimmer shows recall.

3. **Fix the control design.** Use two non-Meta controls (one Claude model, one other) on a subset of tenets, and
   describe the comparison as "how Charter-specific is this behaviour", not as evidence of training.

4. **Add variance to the recall measure or drop the claim.** Options: token-level logprob of the reconstructed
   continuation (logprobs are supported for this model); include the 16 weak passages; add paraphrased and
   fabricated clauses as a floor. Report the recall distribution before running any correlation, and pre-commit
   that a saturated distribution means the analysis is reported as uninformative.

5. **Cut the single-turn battery; put the money into repeats.** Three Petri runs per tenet on Muse over 50-60
   well-chosen tenets gives per-tenet violation frequencies and the repeat-agreement number the prior work lacked.
   That number is a contribution in its own right.

6. **Select tenets for testability, not coverage.** Prioritise corrigibility, duties to humanity, fiduciary duties,
   the evaluation clause and the "do not raise the Charter unbidden" clause. Include tenets where the Charter
   differs from Claude's constitution or OpenAI's spec (fiduciary obedience, Charter over own judgment); those are
   where a control should diverge and where a Muse-specific result is possible.

7. **Fix and report reasoning effort and provider.** Run the main audit at one setting; if budget allows, rerun 20
   tenets at a second effort level.

8. **Give judges the full reconstruction and priority rule**, mark verdicts that depend on gap-adjacent or
   weak-tier text, and use "inconsistent with the reconstructed Charter" throughout.

9. **Search again for prior work on day 1** (my search was limited to arXiv and LessWrong titles), and check
   whether Meta has published the Charter.
