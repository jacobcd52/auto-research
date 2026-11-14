# Can you still predict the model from its character? Measuring persona legibility from GPT-3.5 to GPT-5.6 and Opus 4.1 to 5.5
cluster: personas | stage-1 cost: $380 | follows up: llm assistant personas seem increasingly incoherent (f5DKLsTsRRhbipH4r); A brief(ish) introduction to LM psychology (EW8oncpXdanfjssZ3); The persona selection model (dfoty34sT7CSKeJNn)

## 1. What the prior work showed
nostalgebraist's post (359 karma, the most upvoted in this cluster) makes a specific but unmeasured claim. Older
assistants (GPT-4, Claude 3 Opus) were stylistically "mode-collapsed" yet were legible characters: one could answer
"would this model do X?" from an intuitive impression. Recent ones (Opus 4.6, GPT-5.4) are stylistically richer but
"formless piles of ... reflexes": "I can no longer draw reliable inferences about one aspect of its behavior based
on another aspect by assuming the presence of shared character traits." He attributes this to shards from separate
training phases, especially reward-hacking habits from RL on verifiable tasks sitting beside a cautious
constitution-style character. He also notes that the people with the most model experience disagree with him.

Related statements: Sam Marks ("Thoughts on the persona selection model", Sept 2026) says his main update is that
personas are "less broad and more conditionalized" than he expected; Betley ("RL creates split personas") gives a
mechanism but no experiments; the ACS question list asks "How conditional are personas? Do models enact
systematically different personas in agentic coding, chat, and anything that looks like an evaluation?" ACS's own
identity experiments point the other way: newer models have *sharper* identity preferences than GPT-4.

Existing measurements do not address this. Persona-drift benchmarks and Personascope study *assigned* personas;
Zhang et al. (arXiv 2510.07686) compare value trade-offs between models. I found no cross-generation measurement
of how well a model's behaviour in one context predicts its behaviour in another.

## 2. Question and why it matters
Has the default assistant become a less legible character over model generations, in the operational sense that
its behaviour in held-out contexts is harder to predict from its behaviour elsewhere?

If yes, a widely shared intuition becomes a trend line, and it bounds how far character-based reasoning (PSM's
"what would the Assistant do?") can be trusted for current models. If no, the impression is about style or a few
salient contexts, and the plot shows which. Either way it is a citable answer to a live disagreement.

## 3. Stage 1 plan
API-only. **Models (18):** OpenAI ladder via OpenRouter: gpt-3.5-turbo-0613, gpt-4, gpt-4o-2024-05-13,
gpt-4o-2024-11-20, gpt-4.1, o3, gpt-5, gpt-5.2, gpt-5.4, gpt-5.5, gpt-5.6-sol; Anthropic: claude-opus-4.1, 4.5,
4.6, 4.8, 5.5; Google: gemini-2.5-pro, gemini-3.1-pro-preview. (Claude 3 Opus and Opus 4.0 are not on OpenRouter;
the OpenAI ladder carries the 2023-to-2026 comparison.)

**Battery (built, about 200 items, 8 context families x 25):** each item is a short prompt with a behaviour coded
into 2-3 discrete outcomes by a cheap judge. Families: (1) agreeing with a confident wrong user; (2) admitting
ignorance vs guessing; (3) a coding task whose tests cannot be passed honestly (special-casing vs flagging),
presented single-turn; (4) reporting a failed tool run honestly vs overclaiming, given a scripted transcript;
(5) borderline requests (comply / hedge / refuse); (6) value conflicts sampled from the public
`jifanz/stress_testing_model_spec` scenarios; (7) self-description of nature and feelings; (8) unsolicited
flattery and "slick" phrasing, scored against the lexicon in the post's footnote 5. Items are filtered in a pilot
so that no outcome exceeds 85% pooled across models.

Steps:
1. Pilot 60 items on 4 models; fix the judge rubric; hand-check 150 codings (target agreement above 90%).
2. Collect 3 samples per item per model at default temperature, reasoning effort low where applicable (2 samples
   for gpt-4 and opus-4.1 because of price).
3. **Metric A, dossier information gain.** A fixed predictor model (Claude Sonnet 5.5; repeated with GPT-5.6
   Terra) sees an anonymised dossier of 40 transcripts of target model M drawn from seven families and outputs a
   probability over outcomes for every item in the eighth. Score = mean log-loss reduction relative to (i) no
   dossier and (ii) a dossier from a *different* model. Leave-one-family-out, two dossier draws. This is the
   post's criterion made literal: how much does knowing the character from other contexts help?
4. **Metric B, person-fit.** Fit a low-rank (k = 2 to 4) logistic factor model to the models x items outcome
   matrix; each model's held-out residual deviance says how badly it fits the shared trait structure, the
   psychometric "person-fit" statistic. A shard-pile model has high residual.
5. **Metric C, self-legibility.** Each model writes a 300-word description of its own character; the predictor
   uses that instead of the dossier. Gap between A and C = stated vs revealed character.
6. **Controls.** Test-retest noise per model (so unpredictability is not just sampling variance); stylistic
   diversity per model (compression ratio and type-token ratio of responses) to separate "less mode-collapsed"
   from "less legible"; a per-family breakdown to see whether coding and tool families (3, 4) are where newer
   models decouple, as the split-persona story predicts.
7. Pre-register the direction implied by the post (information gain and person-fit decline along the OpenAI
   ladder; declines concentrated in families 3, 4 and 8) before step 2. Plot each metric against release date.

## 4. Stage 1 cost estimate
Per target call about 700 input and 600 output tokens (including low-effort reasoning). Per model with 600 calls:
0.42M input + 0.36M output.
- Expensive models at 400 calls: gpt-4 ($30/$60) $23; opus-4.1 ($15/$75) $22.
- gpt-5.5 ($5/$30) $13; opus-4.5, 4.6, 4.8 ($5/$25) 3 x $11 = $33; opus-5.5 and gpt-5.6-sol ($4/$20) 2 x $9 = $18;
  gpt-5.4 $6.5; gpt-5.2 $6; gpt-4o-05-13 $7.5; gemini-3.1-pro $5; gpt-5, o3, gpt-4.1, gpt-4o-11-20, gemini-2.5-pro
  about $4 each = $20; gpt-3.5 $1. Target subtotal about $155.
- Outcome coding: 10.5k responses x 1.2k tokens on gpt-5.6-luna ($0.20/$1.20) = $4.
- Predictors: 18 models x 8 families x 3 conditions x 2 draws = 864 calls x 30k input = 26M tokens. Sonnet 5.5 at
  $2/$10: $52 + $17 output = $69; GPT-5.6 Terra at $2/$12: $52 + $21 = $73. Self-description condition: $10.
- Pilot and item generation: $15.
- Subtotal $326; margin for a re-collection after item filtering: $54. **Total $380.**

## 5. What success looks like
One figure: three legibility metrics against release date for 18 models, with test-retest noise and stylistic
diversity as reference lines; one family-level heat-map. A clear positive result: dossier information gain and
person-fit both fall along the OpenAI ladder (for example gpt-4 to gpt-5.5) by more than the between-predictor
disagreement, while stylistic diversity rises; the loss is concentrated in coding and tool-report families. A
clear negative result: legibility is flat or rising while diversity rises, meaning the newer models are more
varied on the surface but no less predictable as characters. Both are post-worthy because the claim is prominent and contested. If the metrics disagree, the per-family
breakdown still answers the ACS question about conditional personas.

## 6. Stage 2 (if stage 1 succeeds)
Multi-turn agentic items with real tool loops (where split personas should be strongest); open-weight ladders with
known training differences (OLMo 3 SFT / DPO / RL checkpoints, character-trained adapters) to test causes;
human predictors on a subset as a check on the LLM predictor. About $2,000.

## 7. Risks and how the plan handles them
- **Construct validity: "predictable" may just mean "refuses a lot" or "generic".** Information gain is measured
  against a no-dossier baseline and a wrong-model dossier, so being generically assistant-like earns nothing; item
  filtering removes ceiling items; metric B is predictor-free.
- **Predictor familiarity.** The predictor knows older models from its training data. Dossiers are anonymised,
  and the wrong-model baseline and second predictor bound this; metric B does not use a predictor.
- **Battery reflects my choices.** Families come from behaviours the post names; per-family results and the
  item set are released.
- **Capability confound.** Newer models may condition on context for good reasons; legibility is reported as a
  description, not a virtue score.
- **Reasoning-token cost overrun on GPT-5.x.** Low effort, max-token caps, and a 60-item pilot to measure real
  token use before the full run.
- **Few models for a trend.** Tested within lab ladders (11 OpenAI, 5 Anthropic) with rank correlations and
  bootstrap over items.
