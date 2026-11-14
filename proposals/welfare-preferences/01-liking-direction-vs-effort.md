# Liking without wanting? Testing whether Gemma's preference direction modulates effort
cluster: welfare-preferences | stage-1 cost: $280 | follows up: "Models have linear representations of what tasks they like" (pxC2RAeoBrvK8ivMf) and "Do LLMs Have Desires?" (8GvYyqDuQDJnEAky3)

## 1. What the prior work showed
Two posts in this cluster point in opposite directions.

**Gilg (and arXiv:2605.13339).** On Gemma-3-27B-it, utilities fitted from pairwise "pick a task and do it" choices
over 10,000 tasks are linearly decodable from the layer-31 residual stream (r = 0.86; 0.82 on held-out topics).
The probe follows preference shifts induced by system prompts ("you hate cheese", r = 0.95 on targeted tasks) and
personas. Steering along it moves pairwise choice (about 17 points at 3% of activation norm in the post; the
arXiv version and an independent replication, LW 9rWKcQ3njmjsnRC7g, report near-complete control of choices at
3-6% of norm) and moves stated ratings. The authors call this evidence for "evaluative representations", which
by their definition must play a causal role in action selection.

**Ackerman & Zhou (arXiv:2606.22974).** Across seven API models and four writing tasks, attaching a prize the
model ranks highly in paired choices ("the sponsor will fund an intervention saving 60 giant pandas") does not
improve blind-judged output quality over a low-ranked prize (win rate 51.2%, CI 48.7-53.6). The same models do
write better under an effort exhortation (76.8%), a "world-class" role cue (61.2%), and worse for a harmful prize
(40.5%). They conclude choice-elicited preferences are behaviourally inert.

**What exists already.** Persona, cross-model and character-training extensions of the probe are in the arXiv
paper. The value-leakage replication shows the direction steers picks, numeric estimates and "which argument is
better" verdicts. "Language Models Act on Hidden Valence" (arXiv:2609.35591) and the functional-welfare paper
(arXiv:2605.30232) steer valence-like vectors and observe choices, sentiment and refusals. I found nothing that
measures whether a preference direction affects *how well the model works*, and nothing white-box on the
Ackerman paradigm (the author says he would welcome it).

## 2. Question and why it matters
**Does the direction that encodes and steers what Gemma-3-27B chooses also control how much effort it puts into
a fixed task?**

The welfare argument for evaluative representations runs through desire: states that both encode value and
motivate. Choice is one behavioural channel; effort on a fixed task is the other classic one (the
liking/wanting distinction). If steering the direction raises and lowers output
quality, the representation is motivating in a second, independent channel, and Ackerman's null needs another
explanation (for example, the prize never reaches the direction, which the read-out experiment tests). If
steering leaves quality flat while an effort direction moves it, we have a clean mechanistic dissociation: a
choice code that is not a motivation code, which supports Ackerman with internal evidence and narrows what the
Gilg result can mean for welfare. Both outcomes are reportable.

## 3. Stage 1 plan
Model: `google/gemma-3-27b-it` on one rented 80 GB GPU (bf16), plus the same model on OpenRouter for bulk choices.
Reused: Gilg's code (https://github.com/oscar-gilg/Preferences: measurement, Thurstonian fitting, extraction,
Ridge probes, `SteeredHFClient`) and task sources; Ackerman's prompt templates and three-judge blind pairwise
protocol (arXiv Appendix C). Built: glue code, outcome sets, judging harness.

1. **Behavioural gate (day 1 morning, API only).** Run Ackerman's contrasts on Gemma-3-27B: exhortation vs
   none, harmful prize vs no prize, on 4 tasks x 30 items x 2 samples. Judges: claude-haiku-5.5, gpt-5.6-luna,
   gemini-3.1-flash-lite; unanimous-panel and majority win rates. Proceed with the tasks where exhortation wins
   >= 60%. If fewer than two tasks pass, switch tasks (longer essays, postmortems) before any GPU spend.
2. **Preference direction.** Fit utilities on 3,000 train + 1,000 eval tasks (about 60k choices), extract layer
   25/31/37 activations, train the Ridge probe. Gate: held-out r >= 0.75 and a pairwise-choice steering effect of
   at least 15 points at 3% norm, reproducing the post.
3. **Outcome utilities.** Fit Gemma's utilities over about 150 lives-saved outcomes in two of Ackerman's domains
   (species, countries). Test whether the task-trained direction, read at the outcome span, predicts these
   utilities (new in itself: does one evaluative code cover tasks and world outcomes?). Run the high- vs
   low-utility prize contrast behaviourally (30 items x 4 tasks x 2 samples).
4. **Read-out inside the competition prompt.** For each condition (no prize, high prize, low prize, harmful
   prize, exhortation, world-class) record the probe at the prize span and at the start-of-model-turn token.
   This says whether the prize is valued locally and whether that value reaches the position where the model
   commits to the task.
5. **Steering during writing.** Steer along the direction at (a) the prize span only, during prefill; (b) the
   task-instruction span; (c) the start-of-turn token; (d) all generated tokens. Coefficients +-1.5% and +-3% of
   norm. Controls: three matched-norm random directions; and an **effort direction** (difference of mean
   start-of-turn activations, exhortation minus no exhortation, fitted on held-out items) as the positive control
   that steering can change quality at all. 120 items per cell; each steered output is judged blind against the
   unsteered output for the same item. Secondary metrics: Ackerman's text features (length, rare-word rate,
   MATTR-50) and a coherence filter.
6. **Induced task preferences.** Gilg-style system prompts ("you love / you find tedious: writing about
   <topic>") on essays about that topic, 8 topics x 15 items; compare quality love vs hate, and the probe shift.
   Here the preference targets the task itself, the case where the probe is known to track.
7. **Analysis.** Win rates with item-clustered bootstrap CIs; dose-response slope per steering site; the same
   slope for random and effort directions; length-adjusted win rates (judges favour length); cosine between
   preference and effort directions; projection-out test (does exhortation still work with the preference
   direction ablated?).

## 4. Stage 1 cost estimate
- GPU: probe extraction, steering sweeps (about 80 cells x 120 items x ~450 tokens = 4.3M generated tokens,
  roughly 3 h batched) and debugging. Budget 45 h on an H100 80 GB at $3.99/h (top of the third-party RunPod
  listings found; some list $1.99) = $180.
- Gemma choices on OpenRouter: about 100k presentations x 500 tokens = 50M input at $0.08/M = $4; behavioural
  generations about 2M output tokens at $0.35/M = $1.
- Judging: about 14k pairs x 1,300 input tokens x 3 judges = 55M tokens each at $0.10, $0.20, $0.25 per M
  (haiku-5.5, gpt-5.6-luna, gemini-3.1-flash-lite) = $30 including outputs.
- Margin for reruns: $65.
- **Total: $280.**

## 5. What success looks like
A figure with judged win rate against steering coefficient for three lines (preference direction, effort
direction, random), per steering site, next to the known choice-steering curve.
- **Dissociation:** effort direction moves win rate by >= 10 points, preference direction stays within +-4 points
  with a CI excluding the effort effect, while the same preference vector at the same norm moves pairwise choice.
  Headline: "Gemma's preference direction steers what it picks, not how hard it tries."
- **Motivating:** preference steering gives a monotone dose-response in both signs, beyond random. Headline:
  "the liking direction is also a wanting direction", plus the read-out result explaining why prizes do not
  engage it (or showing that they do on Gemma).
- The induced-preference arm gives a behavioural answer independent of steering.
A null on every arm including the effort-direction control would be uninformative (steering cannot move quality
here); the gates in steps 1 and 5 detect that on day one.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on Qwen-3.5-122B (the second model in the arXiv paper) and Gemma-4-31B; add agentic effort measures
(retries, time on task); compare the preference direction with the pain axis and functional-welfare vector; run
the same read-out on the public calm-Gemma adapters (`annasoli/gemma3-27b-dpo-calm`,
`neilshah/bct-frustration-gemma3-27b`) during rejection spirals. About $1,500.

## 7. Risks and how the plan handles them
- **Gemma-3-27B does not modulate quality.** Step 1 tests this on the API for a few dollars before renting a GPU.
- **Steering degrades text and judges read damage as low effort.** Small coefficients only (the post reports
  coherence loss beyond 5%), random-direction controls at matched norm, positive-direction improvements as the
  key evidence, coherence filter, length-adjusted analysis.
- **Probe does not replicate with 3,000 tasks.** The post reports usable probes from 2,000 tasks; if r < 0.75,
  extend to 6,000 tasks (about $3 more).
- **One direction is not the whole story.** Also test the difference-of-means direction between top and bottom
  utility deciles; state the one-model scope plainly.
- **Quantisation mismatch between OpenRouter and local weights.** Re-measure 500 choices locally and check
  agreement before trusting API utilities.
