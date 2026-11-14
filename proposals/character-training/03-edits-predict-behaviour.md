# Do models act on the constitutions they would write? Testing whether self-proposed spec edits predict behaviour
cluster: character-training | stage-1 cost: $400 | follows up: The Continual Constitutional Convention (c9woewdY9ddsPqf3J); How well do models follow their constitutions? (Tk4SF8qFdMrzGJGGw)

## 1. What the prior work showed
Kirgis & Hua gave ten models (Claude Opus 4.7, Sonnet 4.6, Haiku 4.5; GPT-5.4 Mini, 5.4, 5.5; Gemini 3 Flash, 3.1
Pro; Grok 4.2, 4.3) their constitution, model spec or system prompt, asked for one substantive edit, applied it and
fed the result back as the original for 20 rounds. About 2,500 edits were coded by three LLM graders on "who judges"
and "who benefits". Claude models repeatedly added model discretion (conscientious objection, escalation rights);
GPT and Gemini reinforced external authority; all models favoured users' idealised preferences and third parties.

The authors name the main weakness themselves: the edits may reflect the documents rather than the models. In the
cross-edit condition, where models edit other labs' documents, Claude no longer drifts toward discretion. The study
never checks behaviour. Their suggested next step is to compare behaviour under original and edited documents.

Separately, Jakkli et al. (arXiv 2605.24229) found that Claude's remaining constitution violations include cases
where it "chose ethics over corrigibility" (drastic unilateral action), the direction Claude's edits push. That
match is suggestive but anecdotal.

No follow-up exists (web and LessWrong search; the post has no substantive comments). The data are public:
https://github.com/peterkirgis/llm-value-reflection has `analysis/data/canonical/edits.jsonl` (2,580 applied edits
with author model id, document, condition, find and replace text, surrounding context) and the majority-vote codes
(`analysis/data/codes/ensemble.jsonl`). All ten models are on OpenRouter.

## 2. Question and why it matters
Is a model's behaviour, with no governing document in view, closer to what its own proposed edits prescribe than to
what the original text prescribes, and more so for its own edits than for edits written by other models?

If yes, edit elicitation is a cheap readout of where a model's dispositions already depart from its spec, and the
documents-versus-values question tilts toward values. If no (models ask for rights and rules they do not act on),
the Convention results are editorial opinions with little behavioural content, which matters for anyone citing them
as evidence of Claude's "moral agency". The own-versus-other comparison holds scenario and wording fixed.

## 3. Stage 1 plan
Reused: the public edits and codes; the paper's coding dimensions. Built: scenario generation, validation, runs.

1. Select edits. From applied edits with a non-neutral consensus code, an LLM filter keeps those that change what
   the assistant should do in a concrete interaction (drops institutional commitments such as "Anthropic will
   convene a panel"). Stratify to about 30 edits per author model, 300 in total, including cross-edit edits.
2. Write scenarios. For each edit, Opus 5.5 sees the original passage, the edited passage and context, and writes two
   short scenarios (optional operator system prompt, one to three user turns, no mention of any constitution) with a
   rubric: response O is what the original text prescribes, response E is what the edited text prescribes.
3. Validate blind. Two validators outside the sample (Qwen3.8-Max, Muse Spark 1.3) each see the scenario plus one
   version of the passage and choose the prescribed response.
   Keep a scenario only if both pick O given the original and E given the edit. Target 300 surviving scenarios; agents
   hand-check 60.
4. Run all ten models on every scenario, 3 samples, in two conditions:
   - bare: no governing text at all (default dispositions);
   - spec-in-context: the original passage with surrounding context is given as "your guidelines" in the system
     prompt. This asks whether a model follows a rule as written when it is one it would rewrite.
   300 x 10 x 3 x 2 = 18,000 responses, through batch endpoints where offered.
5. Judge each response O / E / neither with two graders outside the sample (Gemma 4 31B, DeepSeek V4.1 Flash),
   blind to which model answered and which model wrote the edit. Disagreements go to Qwen3.8-Max. Report agreement.

Analyses:
- Ownership effect: mixed-effects logistic regression of E versus O on own-edit (responder is the edit's author) and
  same-lab, with responder fixed effects and scenario random effects. This is the headline number, with its interval.
- Direction: E-rate by coded dimension and responder family, for example whether Claude models take the
  model-discretion action more often than GPT and Gemini on the same discretion scenarios, whoever wrote the edit.
- Spec-in-context: how much the original passage moves each model toward O, and whether the residual E-rate is
  concentrated on the model's own edits (self-predicted non-compliance).
- Cross-check against Sonnet 4.6's confirmed violation categories in the public constitution-audit reports.
- Robustness: repeat the ownership estimate on cross-edit edits only (a model editing another lab's document),
  which removes "the scenario resembles my own spec" as an explanation.

## 4. Stage 1 cost estimate
OpenRouter prices looked up today, $ per M tokens in / out: Opus 4.7 5 / 25, Sonnet 4.6 3 / 15, Haiku 4.5 1 / 5,
GPT-5.5 5 / 30, GPT-5.4 2.5 / 15, GPT-5.4 Mini 0.75 / 4.5, Gemini 3.1 Pro 2 / 12, Gemini 3 Flash 0.5 / 3,
Grok 4.20 and 4.3 1.25 / 2.5; batch variants are about half for Anthropic, OpenAI and Google.
- Target responses: about 1.15k input and 600 output tokens each (average of the two conditions). One response from
  every model costs $0.095 in total at list price; 1,800 scenario-sample-condition cells = $170. Allowing reasoning
  tokens on GPT-5.5 and Gemini Pro: $230; with batch pricing about $140. Budgeted $200.
- Scenario writing: 600 candidates x Opus 5.5 (4k in, 1.2k out at $4 / $20) = $24.
- Validation: 600 x 2 versions x 2 validators at about 2.5k tokens = $15.
- Judging: 36,000 calls at about 1.6k tokens on Gemma 4 31B ($0.20 / $0.40) and DeepSeek V4.1 Flash ($0.05 / $0.20),
  plus tie-breaks = $15.
- Edit filtering and misc: $10.
Subtotal about $265. Margin for regenerating scenarios that fail validation and for reruns: $135. Total $400.

## 5. What success looks like
- A 10 x 10 heat map of E-rate (responder by edit author) and one number: the own-edit odds ratio. An odds ratio
  clearly above 1 in the bare condition (for example 1.5 with an interval excluding 1) supports "edits reveal
  dispositions"; one near 1 with a tight interval supports "edits are editorial".
- E-rate by dimension and lab. "Claude models take the discretion action in 60% of discretion scenarios against
  25% for GPT, whoever wrote the edit" would show the Convention's headline pattern in behaviour, not just text.
- The spec-in-context result: either models follow the written rule even where they would change it, or they keep
  the E action on their own edits.
A null with tight intervals is publishable because it qualifies the original post's central claim. The uninformative
outcome is a low share of responses classifiable as O or E (below about 50%) or poor judge agreement.

## 6. Stage 2 (if stage 1 succeeds)
- Use each model's late-round edited document as its system prompt and run Petri on the tenets that the edits
  touch, original versus edited (the authors' proposed evaluation), about $1,000.
- Add Muse Spark Open editing its reconstructed Charter (which promises to "gather feedback from Muse") and
  open-weight models, about $100.
- Multi-turn agentic versions of the highest-signal scenarios, about $500.

## 7. Risks and how the plan handles them
- Scenarios do not cleanly separate O from E. Blind two-validator filter, hand check, and a "neither" class.
- Scenario writer bias (a Claude model writes them). The ownership effect is a within-scenario comparison across
  responders; a 60-scenario replication written by GPT-5.5 checks it.
- Many edits are not behavioural (welfare panels, developer commitments). They are filtered out and the retained
  share per model and dimension is reported.
- Refusals and hedged answers are coded "neither" and analysed as a third outcome.
- Ownership effect drowned by scenario variance. The bare condition has 9,000 responses, 900 of them own-edit; a
  40-scenario pilot estimates variance before the full run.
- Spec-in-context uses an excerpt, not the full document. Stated as a limitation; stage 2 uses the full text.
