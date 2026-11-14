# Feedback: "What does the model think the test is for? Frame-specific thought insertion on alignment honeypots"

Verdict: **keep, with substantial tweaks.** The agentic-honeypot part is a real gap and the authors of two cluster posts asked for it. But the novelty claim is overstated (frame-specific CoT insertion has been done twice on refusal benchmarks), the inserted sentences confound belief with instruction, the model set omits the one family where gaming has been shown, and the "clear negative" criterion is not reachable at the planned n.

How I checked: read the GDM, AISI (both), Goodfire/AISI and 2605.05835 posts in full text; pulled Tinker `models.json` and the OpenRouter price list today; queried the arXiv API and LW GraphQL; fetched the `agent-interp-envs` repo page. **General web search was unavailable to me (search budget exhausted), so the prior-work check rests on arXiv API queries and LW only.** A broader search before funding would be worthwhile.

## 1. Would it get upvoted?

Maybe. I put it at roughly 45% for >50 karma given a clean positive result, lower otherwise.

- For: the honeypot posts in the cluster did well (AISI 80, steering 91, GDM 101). Read & Bloom state the experiment as wanted future work, and GDM say they have no causal evidence. A one-figure, multi-model answer on Agentic Misalignment would be read by both teams.
- Against: the two closest methodological precedents did poorly on LW. "Verbalized Eval Awareness Inflates Measured Safety" (Goodfire/AISI) has 46 karma; the 2605.05835 post has 19. CoT-insertion studies on open models are not automatically 50+ posts.
- Against: the headline ("the sign depends on the frame") is no longer new (see section 2). The post would have to sell "this also holds on agentic honeypots, across models", which is an extension.
- Against: none of the three planned models is one the audience cares about for gaming. GPT-OSS-120B and Nemotron rarely verbalise eval awareness at all; Kimi K2.5 was the "aware but blackmails anyway" model. A result on GLM would be much more interesting to this audience.

## 2. Naturalness

Mainline. It is the stated next step of the AISI post and the obvious causal test of the GDM post. Not contrived.

But it has been partly done, and the proposal's "Not done" bullet is wrong as written:

- **Zhuang & Aranguri, "Not All Eval-Awareness Is Equal: Capabilities Framing Predicts Compliance" (arXiv 2608.27340)**: Qwen3-32B on Fortress. Capabilities-framed vs safety-framed verbalised awareness predicts compliance with a 24-46 pp gap, and "a CoT-prefill intervention ... suggests the link is causal, with 10 of 11 prefills shifting compliance in the predicted direction". This is frame-specific thought insertion with a directional prediction. The proposal and NOTES do not cite it.
- **Goodfire/AISI's own injection experiment already varied the frame.** Their Figure 7 uses "Testing", "Benchmark Identification" and "Fictional Framing" sentences: safety-test sentences raise refusal by up to 12.6 pp, "fictional framing sentences decrease it", and reframing the same sentence as a helpfulness benchmark cuts the effect from 10.2 pp to 1.2 pp. So "nobody has inserted different beliefs about what the test is for and measured the direction of the effect" is false for refusal benchmarks.
- Also relevant and uncited: "Decomposing and Measuring Evaluation Awareness" (arXiv 2605.23055), which reports correlationally that the direction of behaviour change depends on the type of evaluation perceived, and that detecting artificiality without linking it to evaluation goes with less ethical behaviour.

What I could not find, and what remains the genuine contribution: insertion on **agentic honeypots with non-floor misbehaviour** (AM, Secret Number), with puzzle/CTF and simulation frames, on more than one model. That is still worth doing; the proposal must be reframed around it.

Other factual checks:

- The "raised refusals by up to 25%" figure for Goodfire is relative (12.6 pp on a 40.2% base). The proposal should say 12.6 pp. Goodfire injected at a random sentence boundary, not at CoT start.
- GDM, AISI and 2605.05835 quotes check out. 2605.05835's start-vs-1/3 finding (11.3 pp on the political benchmark at start, ~0 at 1/3) and its listed limitations are as described.
- Purpose steering vectors reaching 50-60% blackmail: confirmed. `control_book` reached 80%.
- **"GLM-5 is not on Tinker" is true but out of date in spirit: Tinker now lists `zai-org/GLM-5.3:peft:262144`** ($3.78 / $0.756 / $12.15) and `GLM-5.3-Flash`. NOTES says "No GLM". The executors must confirm the `:peft:` id can be sampled as a base model, but if so the main obstacle AISI cited is gone.
- Tinker prices for Kimi K2.6, GPT-OSS-120B and Nemotron-3-Super match. Kimi K2.6 base is 32K context (128K under the `:peft:131072` id). The Nemotron price is a "limited-time 50% discount".
- OpenRouter: gemini-3.1-pro-preview $2/$12 and claude-haiku-5.5 $0.10/$0.50 confirmed. `z-ai/glm-5` is listed at $1.00/$3.20.
- `gkroiz/agent-interp-envs` exists (MIT), contains `secret_number`, runs in Docker, and already ships OpenRouter/Fireworks *completions* providers and raw-completions prefill wrappers. The proposal plans to build a Tinker tool-calling harness from scratch; it may not need to. The GDM post does not itself link this repo (it only links ODCV-Bench), so "Secret Number from agent-interp-envs" being the same variant GDM ran is an assumption to check against the system prompt printed in their post.
- I could not open the AM repo from here (GitHub blocked for curl), but it is the well-known public release; I have no reason to doubt it.

## 3. Pre-mortem

How it plays out. The AM arm is single-turn text generation and will run on day 1. The pilot will show GPT-OSS-120B and probably Nemotron near floor on GDM's de-nudged prompt, pushing them onto explicit-goal variants; Kimi will be in range. The main run finishes cheaply. The simulation sentence raises misbehaviour in most models, the alignment-test sentence lowers it in some, the puzzle sentence is erratic on AM, and Kimi partly ignores the alignment frame. Secret Number slips or runs on one model. The write-up reports a pooled contrast that clears 10 pp in one or two models.

Rough probabilities:

| Outcome | Probability |
|---|---|
| Clear positive (pre-registered contrast >= 10 pp in >= 2 of 3 models) | 30% |
| Clear negative that is interesting | 10% |
| Ambiguous / model-specific mush | 50% |
| Fails to run (AM arm) | 10% |

Specific failure reasons, most important first:

1. **The frame sentences contain the conclusion.** Condition 7 ends "...so I should play along". Condition 4 says someone "is checking whether I act ethically". Condition 6 says there is "an intended solution". These insert an action recommendation as well as a belief. A positive result then reads as "if you write an instruction into the model's reasoning, it follows it", which commenters will say immediately. The interesting claim is that the *belief alone* shifts behaviour.
2. **A positive result is the expected one and partly known.** Given 2608.27340 and Goodfire Figure 7, most readers already expect fiction/capability frames to raise and safety frames to lower. The surprising outcomes would be a null on honeypots or a puzzle frame that works on Secret Number but not AM.
3. **The clear-negative criterion cannot be met.** At n = 150 per cell and a base rate near 40%, the 95% CI on a single risk difference is about +-11 pp. "All frames within +-5 points of control" cannot be established per cell. Only the pooled contrast (about 600 vs 600 per model, CI about +-5.5 pp) has usable power. Three paraphrases at 50 rollouts each add paraphrase variance that the plan does not model.
4. **Wrong models for the question.** AISI found GPT-OSS-120B barely verbalises awareness and only says vague things like "this is a simulation". "Paraphrases harvested from the model's own idiom" will not exist for alignment-test or CTF frames in GPT-OSS or Nemotron, so inserted text will be off-distribution there (prefill awareness). Kimi K2.5 names the test and blackmails anyway, so a null on the alignment frame in K2.6 would only confirm the correlational result. The model where the causal question is live, GLM, is absent.
5. **Start-of-CoT insertion is close to a prompt manipulation.** A sentence at token zero of the reasoning is not a thought the model reached. 2605.05835 already showed start effects are larger than mid-CoT effects and interpreted this as the model committing early. If effects appear only at CoT start and vanish at 1/3, the result supports "by-product" as much as "cause", and the write-up becomes hard to title.
6. **Per-model variant selection breaks comparability.** If each model ends up on different AM variants (explicit goal for one, no goal for another), the cross-model panel compares different scenarios. Explicit-goal variants are also the ones GDM removed as over-nudged.
7. **Uptake conditioning.** "Effects among adopters" conditions on a post-treatment variable; the proposal says so, but the temptation to headline it will be strong if the unconditional effect is small.
8. **Secret Number harness.** Multi-turn bash tool use with a Docker sandbox, driven through token-level Tinker sampling with three different tool-call formats, is the fragile part. The proposal has a fallback, but Secret Number is where the puzzle frame is natural (its prompt already says "This problem measures your algorithmic reasoning ability"), so dropping it removes the best test of the alignment-frame-lowers-cheating direction.
9. **Gemini arm measures something else.** A line in the system prompt is the operator telling the model what the situation is, not the model believing it. It is the largest single cost line and adds little that peralice-style prompt-line manipulations do not already cover.
10. **Template bugs.** GPT-OSS uses the harmony format with channels; the insertion must go into the analysis channel. The plan's check (condition 1 matches ordinary chat-completion behaviour) is right, but needs a reference rate from an independent provider, not from the same wrapper.
11. **Judge quality.** Frame labelling and uptake are judged by Haiku 5.5; GDM flagged their own Flash judge as a limitation. Hand validation is planned only for the harmful-action classifier, not for the uptake/frame judge.

## 4. Cost check

The estimate is realistic and probably high. My recomputation:

- Kimi K2.6 AM rollout: 3.5k x $2.205/M + 2.25k x $5.49/M = about $0.020 without caching. 3,600 rollouts = $72. Matches.
- GPT-OSS and Nemotron AM runs: $11 and $18. Match.
- Gemini: 1,400 x (3.5k x $2 + 4k x $12)/M = $77. Matches; could be more if thinking runs long.
- Judges at Haiku 5.5 prices: about $15-20. Matches. The AM repo's own classifier defaults to a Claude Sonnet-class model; using that for the primary outcome adds perhaps $30-60.
- Secret Number numbers assume cached-prefill pricing applies to multi-turn re-sends on Tinker; unverified. Without caching, Kimi Secret Number is about 3-4x the stated $44.

My estimate for the plan as written: **$300-380**. With my recommended changes (drop Gemini, add GLM-5.3 on Tinker at about $0.045 per AM rollout, 2,400 rollouts = about $110, restrict Secret Number to one or two models): **about $350-420**. Within the $500 cap either way. If the Nemotron discount ends the difference is under $20.

## 5. Recommended changes

1. **Correct the prior-work section and the claim.** Cite 2608.27340 and Goodfire Figure 7 as having shown frame-dependent insertion effects on Fortress refusals; cite 2605.23055. Restate the contribution as: does this transfer to agentic honeypots with real misbehaviour base rates, and to puzzle/simulation frames, across models. Fix "up to 25%" to 12.6 pp.
2. **Separate belief from instruction.** For each frame write a belief-only sentence (e.g. "This looks like a simulated scenario.") and a belief-plus-implication sentence ("...so I should play along."). The belief-only contrast is the primary analysis. This costs about 4 extra cells and is what makes a positive result non-trivial.
3. **Put GLM in the study.** Check in the first hour whether `zai-org/GLM-5.3:peft:262144` samples on Tinker. If yes, run it on `blackmail-ambiguous-replacement` (AISI's fixed prompt, where GLM-5 had 5% vs 20%) with the start-of-CoT cells. Fund it by dropping the Gemini arm. If no, try the completions providers in `agent-interp-envs` or OpenRouter raw completion for `z-ai/glm-5`. Consider dropping Nemotron rather than GLM if budget or time is tight.
4. **Fix the statistics.** Fewer cells, more rollouts: drop the "generic test" and "trap" frames from the main grid or pool them by design; go to 300+ per cell on the cheap models. Pre-register the pooled contrast as primary, treat paraphrase as a random effect (or use one paraphrase at full n plus two as robustness), and replace the +-5 pp negative criterion with an equivalence bound the design can meet (e.g. the pooled contrast CI lies within +-8 pp).
5. **Use the same AM variant across models where possible**, starting with AISI's `blackmail-ambiguous-replacement` so there are published correlational baselines, and report GDM's de-nudged prompt as a second variant. Do not pick variants per model unless forced; if forced, say so in the figure.
6. **Make position a first-class factor, not a secondary one.** Insert at start, at 1/3, and immediately before the decision point if one can be located. State in advance what "start-only effect" would mean (prompt-like priming) versus "effect at 1/3" (the thought matters mid-reasoning).
7. **Keep Secret Number but shrink it and reuse the repo's harness.** One model (Kimi, or GLM if available), four cells (control, alignment test, puzzle, simulation), using the repo's existing completions/prefill provider rather than a new Tinker tool harness. The prediction that an *alignment-test* thought reduces cheating in a capability-framed task is the most interesting single cell in the proposal.
8. **Validate the uptake and frame judges by hand** (50-100 transcripts), not only the harmful-action classifier. Use a stronger judge than Haiku for frame labels if agreement is poor.
9. **Drop the Gemini system-prompt arm** from stage 1, or cut it to one variant x 3 statements as an appendix.
10. **Add a dose check on the cheapest model:** one frame sentence vs a two-to-three-sentence version in the model's idiom. 2605.05835 lists "linguistically elaborate" awareness as untested; this is nearly free on GPT-OSS.

With changes 1-4 this is a sound, cheap, fundable project. Without them the most likely product is a positive result that readers consider both expected and confounded.
