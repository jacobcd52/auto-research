# Feedback: 03 - Is QwQ's "illegible" reasoning load-bearing? (self-hosted re-test)

Reviewer verdict: **keep with tweaks**, but it is the weakest karma bet in the cluster, and the framing needs to change because the paper's own public logs already fail to show the effect.

## What I checked

| Claim | Status |
|---|---|
| Paper's QwQ truncation result ("36% increase in incorrect answers") and r = 0.061 | Confirmed in arXiv 2510.27338 (HTML): incorrect 54.1% -> 73.6%, correct 24.6% -> 11.5%; mean per-question r = 0.061 over 100 samples per question. |
| Jozdien's concession and "Qwen results aren't as provider-sensitive, but I'm not confident" | Confirmed (54-karma comment on jHnZzicKzczkCCArK). |
| Fabien Roger's <3% (p=0.9) prediction, Drake Thomas's confound and strike-nonsense suggestion | Confirmed. Fabien's prediction is about drop-and-distill (SFT), not prefill; he explicitly expects spurious prefill drops from being off-distribution. |
| lbernick's unpublished full-CoT prefill result | Confirmed (comment, 2026-04-24). |
| Public logs: provider mix 90/10 and 15/85; 38/100 and 55/100 non-empty answers | Confirmed by downloading both runs. |
| `Qwen/QwQ-32B` public, ungated, 32.76B BF16, Apache-2.0; R1-Distill-Qwen-32B public | Confirmed (HF API). |
| `qwen/qwq-32b` gone from OpenRouter | Confirmed (absent from the model list today). |
| Prices: H200 $3.59 / $5.29; gpt-4o $2.50/$10; haiku-5.5 $0.10/$0.50; sonnet-5.5 $2/$10 | All confirmed today. |
| "Worst chunks are algebra / Chinese code-switching" | Not re-checked by me, but consistent with lbernick's published analysis. |
| Not already done | arXiv API search found only the original paper; no relevant comments on the three LW threads. **My web-search budget was exhausted, so I could not run a general web search**; treat "not done" as likely, not certain. |

### Things the proposal missed, found in the same logs

1. **The public logs do not show the truncation effect.** `prefill_evaluation.json` is in the same two run directories:
   - threshold-6 run (`20251019_184002`): prefill 3/16 correct (18.8%), 11/16 incorrect (68.8%); original 1/6 correct (16.7%), 4/6 incorrect (66.7%). No drop.
   - threshold-4 run (`20251017_192243`): prefill 12/39 correct (30.8%), 13/39 incorrect (33.3%); original 18/55 correct (32.7%), 21/55 incorrect (38.2%). Incorrect goes *down*.
   The paper's Figure 3 numbers must come from a run that is not among these two. The percentages are consistent with a denominator of roughly 50-60 answers (e.g. 15/61 = 24.6%, 33/61 = 54.1%) - that is my inference, not something the paper states.
2. **The paper's comparison is not paired.** In the threshold-6 run the "original" column covers the 6 flagged samples that happened to have an answer, while the "prefill" column covers 16 prefilled samples. The baseline is conditioned on the original run having finished. That alone could produce the headline.
3. **Half the "empty answers" are infrastructure failures, not model behaviour.** In the 1019 run, 50/100 samples carry `error: "Error processing stream"`, `stream_complete: false`; only 12 are complete streams with no answer. Their CoTs are cut off mid-stream (mean 14k chars vs 28k for answered samples). The proposal treats the 45-62% empty rate as something to reproduce and compare; on local vLLM it will mostly vanish.
4. **lbernick's post already covers much of E1.** WbP39ncim9hBsYn5t re-ran the paper's code on QwQ, got "similarly illegible results, possibly even more illegible", and showed with translation checks that the flags are driven by coherent Chinese and by confusion/backtracking, with graders disagreeing. The taxonomy arm is a replication of that on verified inference, not a new finding. The proposal cites lbernick for the prefill comment only.

## 1. Would it get upvoted?

Probably not above 50; I put it at roughly 30%.

- Cluster reception: nostalgebraist got 93 for overturning the headline result, Khoriaty 116 for the general lesson, faul_sname 186 for a frontier-model trace. Interest tracks (a) surprise and (b) relevance to current frontier models.
- This project has neither by default. The expected result is "not load-bearing; flags are mostly Chinese and confusion", which Fabien, Drake, nostalgebraist, lbernick and Rohin ("doesn't seem to hold up") already believe, and Jozdien has half-conceded. QwQ-32B is a March-2025 model.
- lbernick's post is the closest precedent in form (careful follow-up on QwQ legibility). Check its karma before finalising; my impression from the thread is that it drew little attention, which is the base rate for this genre.
- Who cares: Jozdien, nostalgebraist, Fabien Roger, lbernick, and people citing the NeurIPS paper. A correction that the paper's author can link to has real value, but a small audience.
- The surprising branch (text a judge cannot follow, position-controlled, genuinely needed) would clear 50 easily. I give it under 10%.

What would lift it: point 1 above is a sharper hook than anything in the current draft ("the paper's public logs don't contain its headline effect, and on verified weights with a paired, position-controlled design it is X"). The position control also generalises: "truncate-at-flag tests over-state load-bearingness by N points" is a methods result that applies to future legibility papers.

## 2. Naturalness

Mainline. Both principals named the QwQ question as open and untested, in public, with opposite hunches. Self-hosting is the only way to do it now. The controls are the ones the commenters asked for. No evidence anyone has done it (with the search caveat above).

Less natural parts: condition (g), E3, and the R1-Distill arm are side-branches. Nobody is disputing the r = 0.061 null; re-running it with a length covariate answers a question no one is asking.

## 3. Pre-mortem

How it plays out: vLLM on an H200 with QwQ comes up in a few hours without drama. The team generates 990 CoTs. At the model card's sampling settings the gpt-4o flag rate is lower than the logs (the logs are temperature 1.0 with half the streams broken); at temperature 1.0 it lands near 20-35%, mostly Chinese spans and long confused passages on hard organic-chemistry questions. Truncation hurts by some points; the position-matched control hurts about as much; translation/rewrite does not hurt. CIs are wide. The write-up says "not load-bearing, as expected".

Rough probabilities:
- Clear positive (flagged text load-bearing beyond controls): 7%
- Clear negative, cleanly shown: 45%
- Ambiguous mush (wide CIs, few flags, grader-dependent): 38%
- Fails to run or fatal harness bug: 10%

Specific failure reasons:

- **Power is far short of the 3-point claim.** 200-350 flagged CoTs cluster on perhaps 80-120 hard questions. With ~30% baseline accuracy, a paired difference bootstrapped over questions has a standard error around 4-5 points. The plan can detect a 10+ point effect; it cannot show "(e) within ~3 points of (a)". Five answer samples per prefill barely help: after a full CoT the answer is nearly deterministic.
- **Selection confound in (c) vs (d).** Flagged CoTs are longer, later-flagged, and from harder questions. "Non-flagged CoT for the same question at the same relative position" is not matched on absolute length or on whether the CoT had reached a conclusion. For many hard questions every sample may be flagged, leaving no control. The earlier/later-chunk truncation of the *same* CoT is the better control and should be primary.
- **The flag does not mean illegible.** If the flagged span is coherent Chinese, (e) is a translation and (f) destroys legible reasoning. Then (f) hurting says nothing about illegibility. Results must be split by taxonomy class, and the token-soup class may contain a handful of spans or none.
- **Condition (a) gate is ill-defined for unterminated CoTs.** Some samples will hit 32k tokens without closing the think tag. Decide up front: exclude them from E2 and report the rate.
- **Open-ended gpt-4o correctness with a "partially correct" bucket** is noisy enough to swamp a 5-point effect. The multiple-choice fallback is listed as a risk mitigation; it should be a primary metric. But the paper removed choices deliberately, and a CoT generated without choices then answered with choices is a different, odd condition.
- **Sanity gate has no clear reference.** I do not believe the official QwQ-32B release reports GPQA-Diamond; the proposer should name the specific published number or gate on a benchmark that has one.
- **(g) is a pipeline inside a pipeline**: chunk-grade every continuation, reject, resample. Rejection also selects for short continuations, so it does not measure "cost of a legibility constraint". Likely to eat a half day and produce an uninterpretable number.
- **Unsurprising either way** is the dominant risk, not infra.

## 4. Cost check

The estimate is realistic. Throughput of 1,500 tokens/s for a 32B BF16 model on one H200 with batching is conservative; ~9k tokens per CoT matches the logs (complete samples average ~28k chars). GPU 22-28 h at $3.59 = $80-100; grading $50-60; margin. My estimate: **$220-300**, so $260 stands. Use Secure Cloud if Community H200 stock is thin; that adds ~$40.

Half the generation budget (E3 at 22M tokens, distill arm at 9M) goes to the two least valuable arms. Dropping them makes it a ~$170 project or frees the tokens for power on E2.

## 5. Recommended changes

1. **Rewrite section 1 around the log finding.** State that the two public QwQ prefill runs show no drop (numbers above), that the paper's comparison is unpaired and conditioned on the original having answered, and that half the empty answers are stream errors. Ask Jozdien (public comment in the write-up, not a dependency) which run produced Figure 3. This is the hook.
2. **Make E2 fully paired and pre-registered.** Same CoTs in every condition; primary contrast is truncate-at-flag vs truncate one chunk earlier/later on the same CoT, and vs position-and-length-matched truncation of unflagged CoTs. State the primary metric and threshold before running.
3. **Drop the "within 3 points" framing or size for it.** Be explicit that the prefill test can detect roughly 10-point effects. Fabien's 3% prediction is about distillation; say this test cannot adjudicate it and leave it to stage 2.
4. **Spend E3's tokens on E2.** Replace "198 x 5 + 50 x 50" with one pool of 198 questions x 15-20 samples. It gives 3-4x the flagged CoTs, more questions with both flagged and unflagged samples, and still supports the length-controlled within-question regression as a free by-product.
5. **Cut (g) and the R1-Distill arm.** If a second model is wanted, a current open-weight reasoner that fits on the same GPU would add more relevance than another 2025 distill; verify availability first. Otherwise leave it out.
6. **Report by taxonomy class from the start**, with lbernick's post cited as the prior finding being replicated on verified weights. Pre-commit to what happens if the token-soup class has fewer than ~20 spans: the headline becomes "on official weights QwQ does not produce illegible reasoning at all; it produces Chinese".
7. **Fix the gates.** Name the published number for the capability sanity check. Exclude unterminated CoTs from E2. Make multiple-choice accuracy a co-primary metric, and add a second correctness grader on a subset.
8. **Use the paper's temperature 1.0 as the primary setting** (it is the claim under test) and the model-card settings as the secondary; the draft lists both without choosing.
9. **Funding priority:** fund this only after proposals 01 and 02 from the cluster if money is tight. It is cheap and clean, but the proposer's own ranking (third of three) is right.
