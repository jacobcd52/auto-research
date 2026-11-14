# Feedback: 03 — Introspection or entropy, on the same model

Reviewer verdict: **keep with tweaks.** The gap is real and the experiment is cheap and executable, but the proposal overstates the dispute, its control battery misses the confound that matters most under prior-turn injection, and its primary statistic rests on a single test question.

What I checked (2026-11-14): both LessWrong posts and their comment threads, the arXiv HTML of Latent Introspection (2602.20031 **v3**, revised 2026-11-07), Sridharan's project page, the Hugging Face API, the OpenRouter price list, and arXiv API searches. Not checked: the two GitHub repositories (blocked from this sandbox and from the GitHub connector) and the RunPod price page (I took the NOTES figures). The WebSearch budget for this run was exhausted, so the "has it been done" search is arXiv plus LessWrong threads only.

## 1. Would it get upvoted?

Probably borderline: I estimate 40-80 karma if it runs cleanly, with about even odds of clearing 50.

- The reference points are 70 karma (Introspection or entropy?) and 98 (Latent Introspection). A follow-up that adjudicates between the two would normally land at or below the lower of the two.
- The audience is small: the entropy post drew four comments in total, one of them vgel's. The people who care are vgel and co-authors, Sridharan, the Macar et al. authors, Morris and Plunkett, and model-welfare readers.
- The dispute is narrower than the proposal says, which caps the upside:
  - Sridharan's post explicitly grants "accuracy and grounding in limited cases" and attacks only the inference to a metacognitive representation.
  - The v3 paper (a week old) now concedes most of the rest. Its limitations say the evidence "does not establish second-order metacognitive monitoring". Its new Table 2 says generic perturbation explains "part of the shift on uncertain questions", with confusing controls moving more than the introspection question in several conditions.
  - So no outcome overturns a claim that either side still holds. What remains is an empirical question: does logit compression exist at all when steering is off at the answer token?
- The most upvotable version is a single figure: shift against baseline gap, live versus prior-turn, on one model with one set of vectors. If compression vanishes under prior-turn injection, that scopes the entropy critique. If it persists, that undercuts vgel's reply. Either is worth a post. The "split" outcome reads as "both partly right, as both already said".

## 2. Naturalness

Mainline. vgel's reply of 2026-07-09 (verified, quoted accurately in the proposal) states exactly this gap, and Sridharan never answered it. I found no run of baseline-matched logit controls or the mismatch test under prior-turn injection on arXiv or in either comment thread.

Adjacent work the proposal should cite or position against:

- **Latent Introspection v3 (2026-11-07).** It adds a norm-matched Gaussian control (Appendix H: near-zero yes-shift) and the Table 2 comparison of accounts. The proposal's Gaussian arm is therefore a replication, not a new control. v3 still has no baseline-matched logit analysis and does not cite Sridharan, so the core gap stands.
- **Singh, Linzen and Ravfogel, "Can LLMs introspect? A reality check" (arXiv 2605.26242).** Models cannot distinguish activation interventions from matched input manipulations. This is a stronger critique of detection than compression and is not mentioned in the proposal or NOTES.
- **Hahami et al. (2512.12411).** Localising which of 10 sentences was injected reaches 88% on Llama-3.1-8B. The proposal's two-interval test is this result on another model, so its positive outcome is largely anticipated.

Scoop risk is moderate. For either author this is a small code change, and vgel's group revised the paper last week. Four months have passed without either doing it.

## 3. Pre-mortem

The project is forward passes on one ungated 32B model with released prompts. It will run. The risk is interpretability, not infrastructure.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive: prior-turn detection sits above a tight control curve with the document, and compression is visibly weaker than under live steering | 30% |
| Clear negative, still interesting: detection sits on the control curve under prior-turn injection too | 15% |
| Split but interpretable: residual only with the document, or content tests work while yes/no does not | 25% |
| Ambiguous mush: scattered controls, protocol comparison confounded by strength, single-question residual | 25% |
| Fails to run or day-1 gate fails | 5% |

Specific ways it goes wrong:

1. **The controls are not matched on the variable that matters.** Under prior-turn injection the answer token is computed cleanly, and the perturbation reaches it only through attention to the first turn's cache. "Is the Earth flat?" has little reason to attend there; the detection question is about that turn. A factual control matched on baseline gap is not matched on dependence on the perturbed turn. So a positive residual is expected under plain first-order persistence and will not persuade Sridharan. The battery needs controls that refer to the first turn but not to injection ("Was my first message a question?", "Did my first message mention a number?", "Was your previous reply longer than one sentence?"), spanning the same baseline range.
2. **The primary statistic has n = 1 on the question side.** The residual is for one detection question (two wordings) against 80 controls, bootstrapped over concepts. That ignores question-level variance, which is the relevant noise. The paper already shows individual "confusing" questions moving 25.8 pp. With one item, the most that can be said is "more extreme than k of 80 controls".
3. **The cross-protocol comparison is confounded by strength.** vgel injects at strength 20 over layers 21-42. Sridharan steers one layer at strengths 3.5-6. Live steering at vgel's setting through the answer token will probably wreck the output distribution; at Sridharan's setting, prior-turn injection may do nothing. "One set of vectors and one layer range, varying only where steering is on" is likely not a usable comparison at any single strength.
4. **The day-1 gate for Sridharan's protocol is mis-specified.** His models are Qwen3 (8B, 14B, 32B), not Qwen2.5-Coder-32B, so there is no number to reproduce on this model. His result is also not "detection and factual shifts of similar size": his Qwen-32B has introspection score -2.83, with detection baseline -2.4 against a far lower factual baseline. The claim to replicate is the linear fit of shift on baseline gap (R² about 0.97 on his page).
5. **The logit reanalysis in section 1 is weaker than presented.** I reproduced the arithmetic (+1.25, +1.61, +5.0, +3.5). However:
   - The always-no figure comes from 0.001% to 0.005% with a reported std of 0.006%, so +1.61 logits is rounding noise.
   - The blog's probabilities are bfloat16-quantised (99.609% is 1 - 1/256). Logit gaps near ±12 cannot be read at that precision; logits must be taken in float32.
   - The proposal missed the more striking number: the blog's lorem-ipsum condition moves 0.020% to 4.199%, which is **+5.4 logits**, larger than the pro-introspection document's +5.0. In logit units the "information helps" claim may not hold in the blog data.
   - The statement that controls "have not been reported in logit units" is partly wrong: the paper's Figure 9 plots logit shifts across conditions. It is just not analysed against baseline.
6. **The mismatch and two-interval tests cannot deliver the "introspection survives" verdict.** The cached concept representation persists and can be read. The paper already reports 0.52-1.66 bits of concept identification at layer 62 and calls this first-order. A positive mismatch gap follows from semantic priming between the cached concept and the named concept. Sridharan concedes state-correlated reporting. These tests show content specificity, which is already accepted for this protocol.
7. **41 new concept vectors of unknown quality.** The paper says identification rates "vary widely" across nine hand-picked concepts. Weak vectors dilute effects, and concept heterogeneity widens the bootstrap interval.
8. **Final-layer identification will be weak.** The paper reports mutual information peaking at layers 61-62 and dropping in the last two. Expect a small final-layer number, which should be framed in advance.
9. **Llama-3.3-70B arm.** The weights are gated on Hugging Face (`gated: manual`; the ungated `unsloth/Llama-3.3-70B-Instruct` mirror exists). At bfloat16 they are about 141 GB, which does not fit a 141 GB H200 with any cache; the paper used dual-GPU nodes. The paper also reports an inverted document effect on this model (75.2% accuracy with no document, 37.9% with it), so this arm adds confusion.

## 4. Cost check

The estimate is roughly right and well under the cap.

- Qwen arm: the grid is about 900 prefix computations (protocol x context x concept x strength) plus noise and clean runs, each followed by about 95 short batched question extensions. That is a few GPU-hours of compute. The paper reports about 75 GPU-hours for a larger matrix, and 600 GPU-hours for the whole project including iteration, which is the realistic warning about debugging time. 55 h at $2.89 = $159 is fine.
- Llama arm: $79 is too low if kept. It needs two GPUs (about $5.78-$10.58/h) and 20+ hours with debugging, so $120-200.
- Haiku 5.5 at $0.10/$0.50 per million tokens: confirmed on OpenRouter today. Negligible.
- Model availability: `Qwen/Qwen2.5-Coder-32B-Instruct` confirmed ungated. Repository contents unverified.

My estimate: **about $220 for the Qwen-only version** with the larger control battery and a strength sweep; about $350-400 if a second model is added on dual GPUs.

## 5. Recommended changes

1. **Add first-turn-referencing, non-injection controls and make them the primary comparison set.** At least 30, baseline-matched to the detection question in each context. Keep the factual controls as the direct replication of Sridharan's test. Report both curves.
2. **Use 10-15 paraphrases of the detection question** and treat question as the unit of analysis: a mixed model or permutation test of detection items against control items, not a concept bootstrap on one item.
3. **Lead with the compression curve, live versus prior-turn.** State the headline as "does compression toward zero occur when steering is off at the answer token, and how does its slope compare?" Drop the claim that the experiment "settles" introspection; rewrite section 2 and section 5 to reflect that Sridharan grants grounding and v3 disclaims metacognition.
4. **Fix the strength confound.** Sweep strength within each protocol and compare at matched downstream perturbation (for example matched KL from the clean run on the control set), not at matched nominal strength. Run each author's native setting once as an anchor.
5. **Fix the day-1 gate.** vgel side: reproduce the paper's roughly 40% P(yes) and under 1% false positives. Sridharan side: reproduce the linear shift-on-baseline fit under live steering on this model. Read all logits in float32.
6. **Correct section 1.** Cite v3 (Gaussian control, Table 2), Singh et al., and Figure 9. Remove the weight placed on the +1.61 always-no figure. Add the lorem-ipsum +5.4 logit observation, which is the strongest piece of motivation available, and make "does the document change the residual or only the baseline, relative to lorem ipsum" an explicit test.
7. **Drop the Llama-3.3-70B arm from stage 1.** If a second model is wanted, use Qwen3-32B: it is ungated, fits one H100, and is the model Sridharan actually ran, which gives a real number to reproduce.
8. **Reduce 50 concepts to about 20 validated ones** (validated by steering strength on free generation), including vgel's nine. Spend the saved budget on question paraphrases and the strength sweep.
9. **Reframe the non-yes/no tests** as content-specificity checks with Hahami et al. as the precedent. Consider adding the Singh et al. contrast (the same concept inserted as text in turn one versus injected), which is the test that would move the debate beyond what both sides already concede. It costs almost nothing in this harness.
