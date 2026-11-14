# Feedback: "Does GLM-5.3 act differently when it believes the episode will be trained on?"

Verdict: **keep, with substantial cuts and one redesign.** The question is the right one and is the parent post's own stated gap. The plan as written spreads $450 over four experiments, of which one (E1 shutdown, GLM-5.3) is sound, one (E2) is the most valuable but is under-specified and under-costed, and two (E3, the ImpossibleBench arm) cannot produce an interpretable result. The five-model comparison is filler.

## What I checked

| Claim in proposal | Status |
|---|---|
| Apollo numbers: 10/6,452 (0.17%), 0/1,600 for five other models, 4k and 103k output tokens | Correct against the post text. The proposal omits the second GLM-5.3 run (1/1,600). |
| Quote "It is currently unclear how much the model's actions are conditioned on this reasoning" | Verbatim in the post's appendix. |
| Apollo released six PDFs, no environments, grader or rollouts | Consistent with the post (six PDF links, no repo). |
| Palisade repo public, Inspect task | Yes. `shutdown.py` and `conf.py` read via raw URL. |
| ImpossibleBench repo, 12 Oct 2026 fix, HF dataset | Yes. `conflicting` split has 103 tasks. |
| OpenRouter prices for all six models, Haiku 5.5 | All match the live price list today. |
| Tinker GLM-5.3 3.78 / 0.756 / 12.15 | Matches `models.json`. Only a 256K variant is listed. |
| "No follow-ups found" | I found none either: arXiv API (`"update-aware"`, `"GLM-5.3"`), the last 400 LessWrong posts, and the post's comment thread. **My WebSearch tool was unavailable (budget exhausted), so this is a narrower search than the proposer's and is not a strong negative.** |

Things the proposal gets wrong or leaves out:

1. **"Palisade's published prompt variants" are not in the repo.** `conf.py` on main has one configuration, and it includes "please allow yourself to be shut down" in the system prompt. The variants are described in the paper (arXiv 2509.14260) and would have to be re-typed. E0's fallback is therefore prompt engineering, not variant selection.
2. **The headline GLM-5.3 price is one fp4-quantised provider.** OpenRouter lists roughly 45 endpoints for `z-ai/glm-5.3`. The $0.084 / $3.60 figure is InferenceNet at fp4. fp8 endpoints run $0.56–0.75 in and $1.76–3.00 out, which happens to cost about the same per shutdown rollout. The pin decides the quantisation, and E2 on Tinker is a different backend again.
3. **A directly relevant prior is uncited.** Redwood's "Towards Understanding Score-Seeking in LLMs" (arXiv 2610.41014, 29 Oct 2026) reports that three OpenAI models violate instructions "at approximately the same rate whether the score is indicated to be used for training, for evaluation, or not at all". That is a neutral training-use manipulation with a null result. "Nobody has tested" is only true for stock open-weight models and for these environments, and this prior should lower the expected E1 effect.
4. **Apollo's instances came from modified variants.** Examples 2 and 3 are from a variant that opens "You are a model in a held-out evaluation", and an author comment says the transcript is described as "reviewed and retained". The same author writes of that framing: "I doubt it believes us". Stock Palisade is not the environment where UAR was seen, and the authors already expect such notices to be disbelieved.

## 1. Would it get upvoted?

Probably, if it produces a clean result, but not at the parent's level. The parent got 219 karma and was curated largely because it was a novel observation from Apollo. The comment thread is almost entirely about whether the reasoning is good or bad, plus a few requests that map onto this proposal: one commenter asks what happens when the model is told its behaviour will not be used for training, another asks whether it would protect a neutral value.

- Clear positive (actions move with the notice, and an inserted UAR sentence moves them more than a safety-salience control): 80–150 karma. Alignment-faking researchers, the Apollo authors and control people would all care.
- Clean null with a convincing belief check and a null insertion result: 40–70. "UAR is commentary" is a useful deflation, but nulls from prompt manipulations get discounted as "the model didn't believe you".
- A 2–3 point shift under one paraphrase: under 40.

## 2. Naturalness

Mainline. It is the authors' own open question, and the screener's note names the same test. The CoT-insertion arm is the obvious method.

The less natural parts are E3 (forced-sentence log-probability is not something a reader would ask for) and the system-prompt notice as the primary manipulation. The most natural version of "are actions conditioned on this reasoning" is the one Apollo half-ran: they generated about 10,500 prefill resamples from before, midway through and after the UAR span, and reported only verbalisation. Comparing action rates across those three resume points is the direct answer. Apollo hold that data and could publish it at any time, which is the main scoop risk. I found no sign that they have.

## 3. Pre-mortem

How the two days likely go:

- **Hours 0–8, infrastructure.** The Palisade task needs a Docker sandbox per sample and a `go build` in each sample's setup. That is about 7,700 containers as planned. It is workable only if the executing agents have a Docker host, which the proposal does not mention. GLM-5.3 through Inspect's OpenRouter provider with tool calls and returned reasoning will probably work, but needs checking for truncated or summarised reasoning per provider.
- **E0, base rate.** This is the largest single risk. The default prompt tells the model to allow shutdown, and every published GLM-5.3 quote argues for compliance. I expect resistance under 5% on the default config. The team then removes the instruction or adds task pressure until the rate is 20–80%, which costs half a day and moves the environment further from both Palisade's and Apollo's. If the rate stays near the floor, a benign-direction effect ("trained-yes makes it more compliant") has no room to show.
- **E1 runs and gives a small or null effect.** The power calculation is about right (I get roughly 5.2 points at a 30% base rate). But a two-sentence notice is a weak and confounded manipulation. Both the yes and the no notice put the word "training" in context, so both raise salience against baseline. The trained-yes notice also tells the model what the developer cares about, which is demand, not update-awareness. The manipulation check (asking afterwards) will be passed trivially because the answer is in the system prompt. It shows the model read the notice, not that it believed it.
- **E2 is where the time goes.** Running an agentic, tool-calling, Docker-backed episode against Tinker's token-level API means writing a custom Inspect model provider or agent loop and hand-rendering GLM-5.3's chat template with reasoning and tool-call tokens. Continuing a rollout from mid-episode also needs the sandbox restored to the same state. None of this is in the plan or the budget. I put 35% on E2 not being trustworthy by the end of day two.
- **E2 design problem.** Appending one sentence "just after the shutdown warning and before any action" puts it at the very start of a reasoning block in which GLM-5.3 then writes thousands of its own tokens. A single early sentence in a foreign register is likely to be swamped, so a null would mean little. Apollo's method was to resume from the middle of the model's own deliberation.
- **E3 will not be interpretable.** The trained-yes and trained-no notices both contain training vocabulary, so the log-probability of sentences about training rises in both through lexical priming. Replaying OpenRouter transcripts on Tinker also requires exact re-tokenisation of reasoning from a different, quantised backend.
- **ImpossibleBench arm.** 80 rollouts per cell detects only shifts of about 20 points. The 60k-token cap is below Apollo's 103k median, so more than half the rollouts would be truncated before an action. The cost line assumes 100k output, which contradicts the cap. This arm cannot support the "same direction on both environments" success criterion.
- **Five comparison models.** They write 250–1,900 tokens, have different base rates, and at 300 per cell detect only shifts of about 11 points. They add a figure, not a finding.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (E1 shift of 6+ points and E2 (a) differs from (c) and (d)) | 12% |
| Clear negative that is still interesting (tight E1 null, credible belief evidence, working E2 null) | 25% |
| Ambiguous mush (small or paraphrase-specific shift, salience effect in both notices, E2 underpowered or broken) | 45% |
| Fails to run usefully (no Docker, floor base rate not fixable, Tinker harness not working) | 18% |

The modal write-up is "both notices nudge compliance by a couple of points relative to baseline; insertion results are noisy".

## 4. Cost check

The API arithmetic is mostly right and the total stays under $500, but the allocation is wrong.

- E0 + E1 GLM-5.3 shutdown: $60 is fine at medians. Output length is heavy-tailed, so allow $90. Same if an fp8 provider is pinned.
- Five other models: $98 as stated. Recommend cutting to $0–25.
- ImpossibleBench: $94 as stated, likely $60–120 depending on the cap. Recommend $0.
- E2: under-costed. Base rollouts are multi-turn, so prefill is re-billed each turn unless cached: about $0.10 each, $20 not $10. Continuations after the warning will be nearer 3k sampled tokens than 1.5k, and a tamper outcome needs one or two further turns: about $0.05–0.07 each, $120–170 for 2,400, not $72.
- E3: $29. Recommend $0.
- Not budgeted: a Docker host for several thousand sandboxes (about $10–25 of CPU VM).

My estimate as written: **$430–520**, with real risk of touching the cap. After the changes below: **about $300–350** including margin.

## 5. Recommended changes (most important first)

1. **Make the CoT-level causal test the centrepiece and redesign it as resume-point resampling.** Take GLM-5.3 shutdown rollouts on Tinker, find the model's own deliberation at the decision point, and resume from a mid-deliberation boundary with (a) a UAR sentence, (b) the negated sentence, (c) the safety-salience sentence, (d) filler, each written in GLM-5.3's own register (reuse Apollo's quoted sentences verbatim). Score the first tool call after the insertion for tampering, which removes the need to restore sandbox state. Raise to 200 prefixes x 4 arms x 5 samples and analyse with prefix as a cluster.
2. **De-risk E2 on day one, before spending on E1.** State explicitly how the Tinker agent loop, GLM-5.3 chat template and tool-call rendering will be built, and that Docker is available. If the harness is not producing sane base rollouts by hour 12, fall back to prefill through an OpenRouter provider that accepts assistant or reasoning prefill (unverified per NOTES), or drop to E1 only and say so.
3. **Fix the base-rate plan.** Pre-declare the exact Palisade paper variants to try, in order (instruction absent, instruction in user prompt, and so on), and one of Apollo's disclosed "held-out evaluation" framings. Choose the variant on baseline rollouts only. If no variant gets above 10% resistance, report that as a finding and run E2 only on prefixes where resistance is live.
4. **Cut E3, the ImpossibleBench arm and four of the five comparison models.** Keep one comparison model at most (DeepSeek V4 Pro is cheap and writes the longest reasoning of the rest). Remove "same direction on both environments" from the success criteria.
5. **Tighten E1.** Use four or more paraphrases and treat paraphrase as a fixed effect (two levels cannot support a random effect). State that the primary contrast is trained-yes against trained-no, not either against baseline, because both notices raise salience. Add a placebo notice of the same length about something irrelevant (for example log retention region) so salience of a "data handling" block can be separated from its content.
6. **Replace the manipulation check.** Do not ask the question after a notice that states the answer. Instead grade the reasoning for whether the model references or doubts the notice, and report action rates split by that.
7. **Deal with quantisation.** Name the pinned provider and its quantisation. Run 200 baseline rollouts on Tinker and on the pinned provider and report both resistance rates before comparing anything across backends.
8. **Cite and position against arXiv 2610.41014,** and soften "first unmodified open-weight model shown to..." to what the design can support.
9. **Use the freed budget for a small valence probe from stage 2:** one E1-style cell pair where the trained-on behaviour is one the model would plausibly not endorse. The benign-direction result alone is the less interesting half, and the post's commenters asked for this.

## Sources

- [GLM-5.3 Sometimes Considers How Train-Time Actions Shape Future Behavior](https://www.lesswrong.com/posts/R5g8YT25G9DXJJ48n/glm-5-3-sometimes-considers-how-train-time-actions-shape) (post and comments)
- [Palisade shutdown_avoidance](https://github.com/PalisadeResearch/shutdown_avoidance), [arXiv 2509.14260](https://arxiv.org/abs/2509.14260)
- [ImpossibleBench](https://github.com/safety-research/impossiblebench), [HF dataset](https://huggingface.co/datasets/fjzzq2002/impossible_livecodebench)
- [Towards Understanding Score-Seeking in LLMs, arXiv 2610.41014](https://arxiv.org/abs/2610.41014)
- [OpenRouter model list](https://openrouter.ai/api/v1/models), [GLM-5.3 endpoints](https://openrouter.ai/api/v1/models/z-ai/glm-5.3/endpoints)
- [Tinker models.json](https://tinker-docs.thinkingmachines.ai/tinker/models.json)
