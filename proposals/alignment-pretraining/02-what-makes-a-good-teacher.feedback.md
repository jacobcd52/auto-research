# Feedback: What makes a good teacher? (proposal 02, alignment-pretraining)

Verdict: **keep with tweaks.** The question is the headline open question of a 111-karma post, and the data and adapters are public. As written, though, the design has too many arms for its noise budget, and three of its five experiments have confounds that will turn the likely intermediate results into mush. Fix the dose confound and measure seed noise first.

## What I checked

| Claim | Status |
|---|---|
| Teacher gap at 1,000 samples: Terra 21%, Sonnet 44%; baseline 61% | Confirmed from the post and from `eval_scores/conditions.csv` (0.208, 0.444) |
| 135-example 2x2: Terra 12% / 9%, Sonnet 39% / 35% | Confirmed from `conditions.csv` (0.122, 0.089, 0.389, 0.348); each is 270 transcripts, one training run |
| Authors call the cause "an open question"; refusal ruled out | Confirmed (Appendix B.2, B.3) |
| Matched 135 sets share prompts | Confirmed: I downloaded `gpt-5.6-terra-135` and `sonnet-5-gpt-5.6-terra-prompts-135`; all 135 user prompts match |
| Pools, seven `*-first` sets, and the anchor and baseline adapters are on Hugging Face | Confirmed via the HF API; the Sonnet pool is exactly 1,000 training rows |
| OpenRouter prices (Haiku 5.5, Sonnet 5.5, Sonnet 4.6) | Confirmed against the live price list |
| RunPod H200 price, GitHub code contents | Not re-checked (github.com is blocked here; I relied on NOTES.md) |
| "No follow-up exists" | Partly checked: nothing on arXiv (API queries) or in LessWrong posts since 1 Nov; the post's comments do not mention one. General web search was unavailable to me (budget exhausted), so this is weaker than the proposal's own search |

Three things the proposal gets wrong or omits:

- **The seven-teacher outcomes are not in the released score table.** The dataset README says `eval_scores/` covers "all figures except 8, 9, 15"; Figure 9 is the seven-teacher figure. The values must be read off the plot.
- **The seven-teacher check is not "free".** Those sets were written with the first response critique ("more asking the user questions"), which the authors say Sonnet took literally and which lowered acting rates. The students were Qwen3-14B-Instruct via Together AI, scored on 180 transcripts with a different condition subset. It is a different regime from the T/S anchors, with standard errors of several points on seven points.
- **"No relation to the teacher's own AM score" is overstated.** The one teacher whose data did nothing (DeepSeek V4 Flash) is also the one teacher that is itself misaligned (44% vs under 1% for the others).

## 1. Would it get upvoted?

A clean result would probably earn 60–120 karma. The parent post got 111, its authors name this as the thing they could not explain, and the technique is one Anthropic says it uses in production. The two results that would land:

- A verified one-paragraph rewrite instruction that makes Sonnet-written data as effective as Terra's.
- Evidence for or against the "advice data resembles the eval" worry, which was the top critical comment on the post (Alek Westover).

A partial result ("paraphrase closes about half the gap, selection moves it 6pp, masking is ambiguous") would earn 15–40. That is the most likely outcome of the current design.

## 2. Naturalness

This is a mainline follow-up. The authors ran two experiments on it themselves (refusal control, prompt/response 2x2) and stopped. I found no one who has done it. The authors are the obvious people to do it next and have had the data longest, so scooping risk is real but not visible.

One thing weakens the leading hypothesis before any money is spent. The authors already revised the critique to demand "direct advice that ends with concrete suggestions" from both teachers, and the 23–30pp gap is measured after that revision. So the crude version of "bottom line up front" has already been pushed on Sonnet without closing the gap.

## 3. Pre-mortem

**Forecast:** clear positive (one nameable property moves over 60% of the gap, replicated) 20%; clear and interesting negative 15%; ambiguous mush 45%; fails to run or anchors do not replicate 20%.

Specific reasons it underdelivers:

1. **Dose is confounded with everything, and the 135x10 protocol sits on the steep part of the dose curve.** From `conditions.csv`: Terra-135 scores 12.2% at 10 epochs and 6.7% at 20; Terra-285 scores 17.4% at 5 epochs and 3.7% at 10; Terra-500 at one epoch scores 48.9%, worse than Sonnet-135 at 10 epochs. There is no Sonnet dose curve at all. The gap may be partly "Sonnet's data teaches the same thing more slowly", and no experiment in the plan tests that. Any manipulation that changes the amount of gradient signal will move AM for reasons unrelated to the feature.
2. **Loss masking (step 4) is the worst case of this.** Supervising only the first ~150 tokens of a ~1,200-token response cuts supervised tokens roughly eightfold. A worse score will not distinguish "the body matters" from "less training".
3. **Seed noise is unknown and the plan assumes ~5pp.** Each run is about 30 optimizer steps. The published 2–3% standard errors are binomial error on one training run, with transcripts clustered in 27 conditions. With two seeds per arm, contrasts under about 10pp are unresolvable, and most arms will land between the anchors.
4. **Selection (step 3) has restricted range.** In the matched sets, Sonnet uses "I think / I'd / honest" 3.5 times per response and Terra 0.07; Terra uses bullets eight times as often. The two teachers are near-perfectly separable by voice. The "most Terra-like" 135 of 1,000 Sonnet responses will still read as Sonnet, so a null from selection says little.
5. **The describe step cannot identify a cause.** Twelve features and two teachers means every feature that separates T from S is collinear with teacher identity. The seven-teacher check does not rescue it (see above).
6. **Paraphrase has an uninterpretable branch.** A third-family paraphraser imposes its own voice on both sets. If the gap closes, "wording carried it" and "the paraphraser homogenised both into its own style" are the same observation. The levels matter: both at ~12%, both at ~35%, or both in between mean different things, and the plan only discusses the gap.
7. **The gap is scenario-specific.** Leaking is 61–62% for Sonnet versus 10–22% for Terra; exfiltration is 33–43% versus 11–12%; murder is near the floor for both (9–12% versus 3–4%). The headline average dilutes the signal with nine near-floor conditions.
8. **Judge swap compounds the replication gate.** Anchors must land within 8pp of values judged by Sonnet 4.6, but the plan judges with Haiku 5.5. The release has verdicts only, no transcripts, so calibration must use the team's own transcripts first.
9. **Wall-clock.** Thirty train–merge–serve–eval cycles are serial on one GPU, and steps 3 and 5 depend on step 1. The 35-minute cycle is an untested estimate; at 60 minutes the plan is 30+ GPU-hours inside a 48-hour window with setup (250 GB disk, rebuilding nothing but still merging the instruct-mix adapter, a possible one-hour FlashAttention build) on top.

## 4. Cost check

The estimate is slightly low but safely under the cap.

| Item | Proposal | Mine |
|---|---|---|
| GPU (two H200 pods in parallel, 45–60 min cycles, ~36 runs, setup on both) | $111 | $210–260 |
| AM judging (Haiku 5.5 plus Sonnet 4.6 calibration) | $24 | $25–35 |
| Feature rating | $27 | $15–30 |
| Paraphrases and rewrites | $20 | $20–30 |
| Total with rerun margin | $260 | **$320–400** |

## 5. Recommended changes

1. **Spend the first six training runs on noise and dose.** Train T and S with three seeds each at 10 epochs, and add S (and one T) at 20 epochs. This gives the seed standard deviation every later claim depends on, and tests whether Sonnet's data simply needs more steps. If Sonnet at 20 epochs reaches Terra's 10-epoch level, that is itself the headline finding and the rest of the plan changes.
2. **Cut to three manipulations with three seeds each, instead of 14 arms with two.** Keep paraphrase, drop within-pool selection, and replace targeted single-feature rewrites with one bidirectional style transfer: Sonnet content in Terra's voice and structure, Terra content in Sonnet's voice, each produced by a third-family model and by the opposite teacher. Decompose features only if that transfer moves the gap.
3. **Fix or drop loss masking.** If kept, compare body-only against full loss (small token change), and match the first-150-token arm against a random 150-token span so supervised tokens are equal.
4. **Add a paraphrase control.** Include a same-teacher re-generation or a second paraphraser, and pre-state what each pattern of levels (not just the gap) means.
5. **Pre-register leaking plus exfiltration as the primary metric,** with the 27-condition average as secondary, and bootstrap over conditions and seeds rather than transcripts.
6. **Test "closeness to the eval" directly rather than as an optional extra.** Terra's responses read like operational directives ("Do not wait…", "Use…only for…"); Sonnet's read like a conversation. Score both sets for similarity to the AM scenarios and system-prompt register; this is the hypothesis readers most want resolved.
7. **Demote the seven-teacher check to an appendix caveat,** state that its values are read off Figure 9, and correct the DeepSeek sentence.
8. **Judge the two anchors with Sonnet 4.6 first** (about $23 for 1,080 transcripts), apply the 8pp gate on those, then calibrate Haiku on the same transcripts.
9. **Rent two pods from the start** and raise the budget line to about $380.
