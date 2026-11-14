# Feedback: 01-description-recall-audit

Verdict: **keep, with tweaks** (cut scope, fix three design holes). The gap it targets is real and the artifacts are public.

What I checked (14 Nov 2026):
- **Atlas is public as described.** I downloaded `public_atlas_data/index.json`, `subcircuit_modes_index.json` (5,477 poles), `ns11_pages/data/index.json` (sim score for 585 poles, median 0.612, 74% above 0.5, 2% negative) and per-pole files. They contain θ, mode predicates, example windows with per-token activations and routing flags.
- **Weights are public.** Qwen/Qwen3.6-35B-A3B is ungated, Apache-2.0, model type `qwen3_5_moe`.
- **OpenRouter prices match.** Opus 5.5 $4/$20 (batch $2/$10), Sonnet 5.5 $2/$10, GPT-6.1 Terra $1/$5.
- **Goodfire report read in full** for the detection, simulation and input-synthesis sections.
- **Not checked:** the RunPod price, and the wider web. WebSearch was unavailable (budget exhausted), so the "not already done" check rests on LessWrong post titles since 28 Oct and four arXiv API queries. A Twitter-only or blog follow-up could be missed.

## 1. Would it get upvoted?

Probably, but it is not safe. I put it at about 45-55% for more than 50 karma given a clean result.

- **For:** it tests the specific objection in a 368-karma post against the artifacts of the 220-karma post's author, and gives a number each side would predict differently. Nanda, StefanHex and neverix all voiced the "activating examples are incomplete" worry in comments.
- **Against:** attention has decayed. The linkpost for Goodfire's own technical report sits at 29 karma with no visible comments, and neverix's "Takes" is at 26.
- **What would clear the bar:** a headline figure that is one sentence long, such as "when Opus reads the description and says the neuron should fire, it fires X% of the time", plus a gallery of misses. A table of recall by layer, sign and verdict would not.
- **Which outcome sells:** low recall is much more upvotable than high recall. "Goodfire's descriptions hold up" is worth roughly 30-50 karma.

## 2. Naturalness

Mainline. It is the first of Gao's two failure modes, run on the public atlas.

The report does not do this test, as the proposal says:
- Detection controls are random or same-expert windows where the neuron stays below q90.
- Simulation windows are centred on sampled firings.
- The 40 random windows per pole are not description-enriched.

Three things the proposal understates or gets wrong about the prior work:

- **The simulation is already a partial local precision test.** Goodfire's simulator predicts every token in a 58-token span with 768 tokens of real context, and "passages often hold other firings too, and all of them are scored". False positives near real firings are therefore already penalised. The untested gap is narrower than "never tested": it is description-matching text far from any firing.
- **The atlas has three description tiers, and the proposal picks the wrong one for half its claims.**
  - The tiers are the one-line atlas label, the mode predicates, and the long Neuron Scientist description (the `pick`/`report` fields in `ns11_pages/data/<pid>.json`).
  - The long description carries magnitudes in θ and explicit exclusions, for example "'A square ABCD' or 'a square garden' gives 0" and "everyday prose stays at 0".
  - The 585 sim scores and the 73% figure come from the long description; detection used the mode descriptions.
  - Auditing "mode predicates only" and then correlating with the sim score or commenting on the 73% is a mismatch. Goodfire would reply that the real description already excludes those cases.
- **A band label looks wrong.** The report's main text gives 56% for p99.9-p99.99, 64% for p99.99 and up, and 76% for the top 1,000. The proposal says "56% in the p99-99.9 band". The appendix also lists S95/S99 and θ-relative windows as sampling schemes, so "not evaluated below p99" should be re-read against Table 3 before it is repeated.

Related existing work: Goodfire's input synthesis is a sufficiency test of a sort, but it uses activation feedback over several rounds, reports the best case, and covers the primary mode only. The Bonsai repo runs near-miss sentence tests per label. Neither gives an aggregate natural-text recall number.

## 3. Pre-mortem

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (recall high, Gao's failure mode rare) | 20% |
| Clear negative that is interesting (recall low, robust to judge and description tier) | 20% |
| Ambiguous mush | 40% |
| Fails to run or stalls at the replay gate | 20% |

How it most likely plays out:

1. **Day 1 goes to hooks and the replay gate.**
   - Goodfire's bands use router-weighted activation (activation × routing weight); θ is a census threshold for one pole and 0.65 × p99.9 for the other.
   - Atlas example windows are about 33 tokens plus a `ctx_tail` string (`ctx_len` about 187), while Goodfire ran with 768 tokens of real context. The NS reports themselves note that context-accumulating modes drop from 4-5θ to 0.4-3.1θ in truncated windows.
   - A rank correlation of 0.9 on truncated replays may therefore fail for benign reasons, and the team will burn hours deciding whether the cause is indexing or context.
   - The architecture is multimodal `qwen3_5_moe` with a shared expert, and Goodfire released no code.
2. **Routing is the unhandled confound.**
   - A neuron can only fire on tokens routed to its expert (8 of 256), and Goodfire scores only routed tokens.
   - The proposal's recall is P(act ≥ θ | description matches), with no routing condition. A description-matched token not routed to the expert counts as a miss.
   - Whether that should count is the whole argument. Cammarata would say the description is implicitly "within this expert's domain"; Gao would say that is exactly the hard-to-describe subset.
   - Unless recall is reported both unconditionally and conditional on routing, the headline number will be dismissed by one side.
   - Forced firing at an unrouted token (step 7) is not defined at all.
3. **"Matches the description" means "Opus says so".**
   - The primary metric is the precision of Opus's positive predictions on description-enriched text.
   - A low number has three explanations: the neuron fires on a subset, Opus reads the description too broadly, or the description tier was too short. Arm (c) addresses only part of this.
   - The 0.8 and 0.5 cut-offs are arbitrary, and nobody pre-registered what Gao or Cammarata would predict.
   - Expect per-pole recall to be bimodal (lexical neurons near 1, contextual ones near 0.3) with a pooled value around 0.5-0.7. That is the proposal's own "ambiguous" case.
4. **Retrieval bias cuts both ways.**
   - Keyword retrieval finds text that looks like the exemplars, which inflates recall.
   - Embedding retrieval finds topical neighbours, which deflates it and invites "that isn't what the description says".
   - 30M tokens is small for narrow modes such as "radical axis" or "'Kuala Lumpur' in Greek"; many poles will have well under 150 genuine matches.
5. **Step 8 is ill-defined.**
   - "KL recovered" divides by ablation damage. On description-sampled windows where the neuron is silent, ablation damage is about zero and the ratio blows up.
   - The simulator here is a 4-level label at one marked token, whereas Goodfire's is the unreleased Jev at 10 levels on every token. Scheme (i) will not land near 73%, so "the gap to (ii)" has no anchor.
6. **Step 7 lacks the control that makes it interpretable.**
   - Forcing any neuron to its median firing value anywhere costs KL. The comparison needed is forced firing at description-matched silent tokens against forced firing at random routed silent tokens.
   - Comparing with ablation at real firings does not answer whether the description picked harmless places.
7. **Nine steps is too many for two days** when step 1 is a hard gate with no released reference code.

## 4. Cost check

The estimate is slightly low on the judge and about right overall.

- **Judge input is underestimated.** A 250-token window plus description plus instructions is about 700-1,200 tokens, not 350; the long NS description alone is about 500-700 tokens.
  - 60k calls × about 1,000 tokens = 60M input = $240 at list price, or $120 at the batch price.
  - Output of about 2M tokens is $40, or $20 at the batch price.
  - With the few-shot and second-judge arms, judging comes to about $180-300 depending on batching and per-pole prompt caching.
- **GPU hours are plausible.** 40 h at $2.69/h is $108 (price not re-checked). 30M tokens through a model with about 3B active parameters takes a few hours. The 72 GB bf16 model on a 96 GB card leaves little headroom for 512-token batches with hooks.
- **My estimate:** $380-480 as written, which touches the cap. With batch pricing and step 8 cut, $300-350.

## 5. Recommended changes

1. **Handle routing explicitly.** Report recall unconditionally, conditional on the token being routed to the expert, and P(routed | description match). Restrict forced firing to routed tokens. This is the largest threat to the result being accepted.
2. **Use the description tiers as the independent variable.** Run the judge with the one-line label, the mode predicates, and the full NS `pick` text including its exclusions.
   - This removes the strawman objection.
   - It turns stage 2's "description length versus recall" into a stage-1 plot at near-zero extra build cost.
   - It tests Gao's claim that the firing subset is "hard to characterize compactly" directly.
   - To pay for the extra judging, drop to about 250 poles.
3. **Cut step 8.** If a simulation-style number is wanted, report absolute excess KL per window from substituting judge-predicted activations, by sampling scheme, with no ratio to ablation damage. Do not compare with 73%.
4. **Add the random-routed-token control to step 7**, and present the result as a ratio: forced-firing KL at description-matched silent tokens over forced-firing KL at random routed silent tokens.
5. **Loosen and re-specify the replay gate.**
   - Replay with `ctx_tail` and `full_docs` context.
   - Gate on sign and index identification: firing-token activation above θ in at least 75% of exemplars, and a clear separation from a shuffled-neuron-index null. A 0.9 rank correlation is too strict for truncated context.
   - Budget one day. If the gate fails by the end of day 1, stop and write up the reproducibility failure.
6. **Add a cheap synthetic arm that bypasses retrieval.** Have a writer model produce 20 texts per pole from the description alone, with no activation feedback, and report the first-shot fraction reaching θ. This is the no-feedback version of Goodfire's input synthesis, costs under $30, and is immune to the 30M-token sparsity problem. Label it as off-distribution.
7. **Pre-register predictions and the headline before the scan.** State what recall each camp would predict and fix the primary number: pooled recall conditional on routing, with the full NS description. Publish judge-agreement and the few-shot ceiling next to it. Lead the write-up with 30 miss cases shown as text.
8. **Fix the prior-work paragraph.** Correct the band label, and acknowledge that Goodfire's simulation scores every token in the span and that the NS descriptions contain explicit exclusions tested by minimal pairs. State the gap narrowly as "description-matching text sampled independently of the neuron".
