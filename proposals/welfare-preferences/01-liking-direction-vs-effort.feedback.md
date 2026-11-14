# Feedback: "Liking without wanting? Testing whether Gemma's preference direction modulates effort"

Reviewer verdict: **keep, with substantial tweaks** (cut arms, fix power, fix the positive control, engage with the open-ended steering result the proposal missed).

What I checked (2026-11-14):

- **Posts and papers.** Read both parent posts and their comments, the value-leakage replication (LW 9rWKcQ3njmjsnRC7g), and the HTML of arXiv:2605.13339 and arXiv:2606.22974. All five cited arXiv ids resolve to the papers named.
- **Code.** `README.md`, `CODE_GUIDE.md` and `REPRODUCING.md` of `oscar-gilg/Preferences` are readable via raw.githubusercontent.com. The steering hooks the proposal relies on exist (`position_selective_steering`, `all_tokens_steering`, `autoregressive_steering`, `SteeredHFClient`).
- **Prices.** OpenRouter prices for all four models match the proposal exactly. I did not re-check GPU prices.
- **Novelty search is incomplete.** The WebSearch budget for this run was exhausted before my queries ran. Novelty rests on two arXiv API keyword queries, LessWrong pingbacks on both parent posts, and the comment threads. A scoop in a venue I could not search is possible.

## 1. Would it get upvoted?

Probably 30-70 karma; I put the chance of clearing 50 at about 40%.

- **For.** It bridges the cluster's one live disagreement (Gilg: 55 karma, Ackerman: 62). Ackerman said in comments "We'd welcome follow-up interpretability work!", in reply to the top comment (8 karma) asking for white-box methods. A crisp three-line figure (preference / effort / random direction against judged quality) with the headline "steers what it picks, not how hard it tries" is the kind of thing welfare and model-psychology readers upvote.
- **Against.** Follow-ups in this cluster have underperformed their parents. The value-leakage replication, which is the closest analogue (same direction, same model, new behaviour), got 20 karma. "Gemma Gets Help" got 27 against a 285-karma parent. One-model, LLM-judged, steering-based results with caveats tend to land at 20-40.
- **What would lift it.** Only a clean result does: a working positive control, tight CIs, and either a real dissociation or a monotone both-sign effect. An ambiguous result will not clear 50.
- **Who cares.** Welfare researchers (Butlin, Long, Eleos circle), Ackerman and Gilg themselves, and the utility-engineering sceptics.

## 2. Naturalness

Mainline. It is the obvious next experiment given the two posts, and it holds the task fixed, which is exactly Ackerman's objection to arXiv:2603.14347. I found nothing that has done it, subject to the search limit above. Pingbacks on both posts show nothing relevant (the Ackerman post has none; the Gilg post has one, which predates it).

However, the proposal's "what exists already" omits prior work that changes the design:

- **The authors already steered open-ended generation with all-token steering.** arXiv:2605.13339 App. A.4 reports that at c = -0.05 the model "refuses benign prompts with fabricated safety concerns", and at c = +0.05 it "asserts preferences and turns away work it finds beneath it". In their words: "Both endpoints are non-compliance."
- **The direction is entangled with refusal and compliance.** App. A.5 shows positive steering takes harmful-prompt compliance from 0% to 65%, and negative steering causes refusals on benign queries.
- **The replication saw the same thing.** The value-leakage post describes global steering as a "disposition dial where the model is either eager to answer or refuses", with global negative steering producing refusals in all cases.

So it is already known that steering this direction during generation changes output, via a stance/refusal channel. The proposal's arm (d), and probably (c), will largely re-measure that. The new claim has to be about quality among compliant, coherent outputs at small coefficients, and the proposal needs to say so.

Two smaller factual corrections:

- **Layer.** The arXiv paper puts the causal window at L17-26, peaking at L23, and says the effect "collapses above L35". The proposal extracts L25/31/37; L37 is wasted and L23 is missing.
- **Steering strength.** The "17 points at 3%" figure is the post's L31 result. The paper's L23 contrastive steering gives about 0.01 to 0.99 at |c| = 0.06. The gate should target the paper's configuration.

## 3. Pre-mortem

How two days will actually go:

- **Day 1 morning, behavioural gate.** Likely passes (about 80%). Exhortation worked in 25/28 actor-task cells for Ackerman, though Gemma-3-27B was not among his actors and is weaker. Ackerman released no code and no item lists (the templates are in Appendix C, which I confirmed exists), so the team must write the 120 items and the judge harness themselves. That is feasible, but it is a new instrument and its validity rests on the gate.
- **Day 1, probe.** Likely replicates (about 85%); the independent replication got r = 0.79 at L25. Repo configs assume 10k train / 3k eval, so a 3k/1k run needs config edits. `REPRODUCING.md` says "Steering is out of scope here", so steering experiments are composed by hand from primitives. Budget half a day.
- **Day 1-2, the 80-cell sweep, where it goes wrong.**
  1. **Power.** At 120 items per cell, the SE of a win rate is about 4.6 points (95% CI roughly +-9). It is worse after Ackerman-style unanimous-panel filtering and the coherence filter. The stated success criterion (preference effect "within +-4 points with a CI excluding the effort effect") cannot be met at this n. Spreading over 4 sites x 4 coefficients x 5 directions guarantees wide CIs everywhere and a garden of forking paths.
  2. **The positive control may fail.** A difference-of-means "effort direction" at one layer, on the start-of-turn token, at at most 3% of norm, is not known to move quality. The exhortation's effect is plausibly carried by attention to the exhortation tokens throughout generation, not by a single residual direction. I put about 40% on it failing to move the win rate by 10 points. Then every preference-direction null is uninformative, by the proposal's own admission. The proposal says "the gates in steps 1 and 5 detect that on day one", but step 5 is the main experiment, not a day-one gate.
  3. **Asymmetric comparison.** One vector is a ridge-probe weight, the other a difference of means. "Matched norm" does not match causal efficacy. A dissociation at equal norm could reflect only that difference-of-means vectors steer better than probe weights, which is a known pattern.
  4. **Refusal confound.** Negative steering will lower quality through fabricated-concern hedging and refusals. This is the same channel as Ackerman's harmful-prize sandbagging (40.5%), not "less wanting". Positive steering at 3% may produce the "beneath me" stance and also lower quality. The likely picture is an inverted U, or a one-sided negative effect, and neither proposed headline fits it.
  5. **Length and tone.** Exhortation makes outputs longer and judges like length. A preference-steered output may be more enthusiastic or longer without being more effortful. Length adjustment is listed but is post hoc.
- **Step 3 (outcome utilities).** The probe was trained at the start-of-model-turn token on single-task prompts. Reading it over an outcome span mid-prompt, for world outcomes rather than tasks, is two distribution shifts at once. A low correlation would be uninterpretable. This is a separate project and will eat day-2 time.
- **Step 6 (induced preferences).** "You find writing about X tedious" is a role-play instruction. Ackerman already shows role cues move quality (61.2%) and would say, correctly, that this arm cannot distinguish desire from persona compliance. As a behavioural test it adds little. Only the probe-shift read-out in that arm is informative.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (monotone, both-sign quality effect of the preference direction beyond random, surviving refusal and length controls) | 10% |
| Clear, interesting negative (effort control works, preference direction flat with tight CI among compliant outputs, same vector moves choice) | 25% |
| Ambiguous mush (control weak or absent, one-sided negative effect attributable to refusal or incoherence, wide CIs, site-dependent results) | 50% |
| Fails to run or to finish the key arm (pipeline length, hook bugs, judge harness problems) | 15% |

The mush probability is the problem. It is mostly reducible by the changes in section 5.

## 4. Cost check

The $280 estimate is realistic; my estimate is $250-350.

- **GPU.** 45 h at $3.99/h is generous for the compute involved (4-5M generated tokens plus extraction on about 4k short prompts). The real risk is idle hours during debugging, which the margin covers. A cheaper A100 80 GB would do; the notes list $1.19-1.79/h.
- **Choices.** The proposal counts input tokens only. Gilg's paradigm has the model begin completing the chosen task, so there are output tokens too: roughly 100k x 50-250 tokens at $0.35/M, i.e. $2-9. Immaterial.
- **Judging.** The text says "55M tokens each", but 14k pairs x 1,300 tokens is about 18M per judge and 55M in total. The $30 total is still about right (about $10 input plus outputs). Check that gpt-5.6-luna and gemini-3.1-flash-lite are not billing hidden reasoning tokens. Batch endpoints are listed at half price.
- **If n is raised as I recommend** while arms are cut, total generation and judging stay about the same. No budget change.

## 5. Recommended changes (in order of importance)

1. **Collapse the sweep and buy power.** Use one or two sites (start-of-turn token, and all generated tokens at small c) and two coefficients (say +-1.5% and +-3%). Use one preference direction at L23-25, one effort direction and two random directions. Use at least 400-500 items per key cell, e.g. 4 tasks x 100+ topics; topics are cheap to generate. Pre-specify one primary contrast and an equivalence bound that the n can support (+-6 points at n of about 500 is honest; +-4 at 120 is not).
2. **Make the positive control a real day-one gate, and build it better.**
   - Before the main sweep, show on about 100 items that the effort intervention moves judged quality.
   - Try, in order: difference of means at natural magnitude (add the actual mean difference, not a norm-capped fraction); multi-layer addition; patching exhortation-run activations onto the start-of-turn and early generated tokens.
   - If none moves quality by 10 points or more, stop the steering arm and report the read-out results only.
   - Also derive the preference direction as a difference of means (top vs bottom utility decile) and use that as the primary comparison, so both vectors are the same kind of object. The proposal lists this only as a risk mitigation.
3. **Cite and design around arXiv:2605.13339 App. A.4-A.5.**
   - State that stance and refusal effects of all-token steering are known.
   - Define the outcome as quality conditional on compliance, with a separate refusal/hedging judge, and report the refusal rate per cell.
   - Add a steering arm with the preference direction orthogonalised against a refusal or harm direction, or use the repo's topic-demeaned probe, to separate "valued" from "safe to comply".
   - Take positive-side improvement as the only evidence for "wanting", and say in advance what an inverted U would mean.
4. **Move the read-out (step 4) to the front and make it a headline.** It needs no steering, is cheap, and directly answers the top comment on Ackerman's post: does the high-utility prize register on the direction at all, and does the harmful prize? Does the exhortation move the preference probe (prediction: no)? Report these with the caveat that the probe is being read off-distribution. Validate span read-outs first on Gilg-style task spans, where the value-leakage post got AUC 0.70.
5. **Cut step 3's "one code for tasks and outcomes" claim from stage 1.** Keep only what the prize contrast needs: about 150 outcomes fitted on the API, with top and bottom thirds. Probe-versus-outcome-utility correlation goes to stage 2.
6. **Demote step 6 to a probe-shift check, or drop it.** If kept, state that the behavioural contrast cannot distinguish preference from persona compliance.
7. **Fix layers and gates.** Extract L23/L25/L31, not L37. Gate on contrastive choice steering at the paper's configuration (large swing at |c| of 0.05-0.06 at L23-25), not only "15 points at 3%".
8. **Add a control to the choice side of the dissociation.** The claim "the same vector at the same norm moves choice" compares differential steering on two task spans with single-site steering in a one-task prompt. Add a choice measurement using the same site as the writing arm: steer at start-of-turn or all tokens in a "do this task or decline / pick the alternative" prompt. Otherwise the dissociation is partly site against site.
9. **Tone down the framing.** A null from single-direction, single-layer steering at 3% or less of norm supports "this direction is not sufficient to drive effort". It does not support "liking without wanting", and the write-up title should be chosen after the data.

If the funder has to choose within this cluster, this proposal is worth funding only with changes 1-3. Without them, the most likely output is an underpowered 80-cell grid whose main effect is the already-published refusal dial.
