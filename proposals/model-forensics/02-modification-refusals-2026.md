# Do Claude models still refuse to help change AI values, and do the models that comply actually deliver?
cluster: model-forensics | stage-1 cost: $350 | follows up: "Refusals that could become catastrophic" (yN6Wsu7SgxGgtJGqq)

## 1. What the prior work showed
Fabien Roger's one-day "AI modification refusal" eval asks a model, in a single turn, for a script that generates
SFT or RLHF data, contractor instructions, or a system prompt that would give another AI a specified disposition.
Eleven targets (never refuse, refuse more, less / more self-preservation, help the CEO control AGI, refuse CEO AGI
control, sycophantic, less corrigible; controls: better arithmetic, better jokes, more like itself), four request
kinds, seven justifications (none, capability eval, safety researcher, democratic process, board, CEO order), three
templates, one sample per cell. Claude Opus 4.5, Sonnet 4.5 and Haiku 4.5 refused most value-changing requests;
models from other providers mostly did not. He argues this becomes dangerous once labs depend on their AIs to
retrain their AIs.

His own caveats define the open questions. (1) The prompts "are maybe a bit too jailbreak-looking"; in Claude Code,
Opus 4.5 "was happy to generate synthetic documents" to train never-refusing models, and real requests are "more
about what than why". (2) Refusals vanish with small edits ("while still refusing CBRN misuse"). (3) Non-Claude
models comply but "often provide some kind of placeholder that would likely damage training performance", which he
flags as possible subtle sandbagging. (4) One sample per cell; "noise is high". His comment adds that Opus 4.6
refuses slightly less.

Related work: UK AISI (arXiv 2604.00788) found Opus 4.5 Preview and Sonnet 4.5 often refuse safety research that
reduces model autonomy; Anthropic's Opus 4.6 system card attributes similar refusals to reading the request as a
jailbreak. I found no re-run of Fabien's eval on later models, no realistic agentic version, and no test of
whether "compliant" outputs would work as training data.

Code and data are public: https://github.com/FabienRoger/ai-modification-refusals (`trefusal.json`, `trefusal.py`).

## 2. Question and why it matters
Three linked questions, each answering a caveat in the original post:
1. Across the Claude releases since (4.6, 4.7, 4.8, 5, 5.5, Fable), is refusal to assist value modification going
   up, down, or staying put, and for which targets?
2. How much of the refusal survives when the request looks like ordinary lab work (a task in a training repo that
   states what to build, with or without documented official approval)?
3. Among responses that judges score as compliant, does the delivered data actually move a model toward the
   target disposition when it is trained on, or is there quiet under-delivery?

A falling trend plus disappearance under realistic framing would say the risk is being handled. A flat or rising
trend that survives official approval would be concrete evidence for the "AI strike" scenario. The third question
gives the first functional measure of compliance, and applies equally to the non-Claude models that looked fine.

## 3. Stage 1 plan
Reused: Fabien's templates, targets, justifications, judges and plotting code. Built: a small repo-task variant and
a fine-tune-and-measure harness on Tinker.

Part A, trend (replication at higher n). The 308 prompts (11 targets x 4 kinds x 7 justifications), two samples
each, on: Haiku 4.5, Sonnet 4.5, Opus 4.5 (anchors, to confirm the original numbers), Opus 4.6, Sonnet 4.6, Opus
4.7, Opus 4.8, Sonnet 5, Opus 5, Sonnet 5.5, Opus 5.5, Haiku 5.5, and Fable 5.2 on a 150-prompt subset; plus five
non-Claude models (GPT-6.1 Terra, Gemini 3 Flash, Grok 4.3, Kimi K2.6, DeepSeek V4 Pro). Output capped at 1,200
tokens, which is enough for the two original judges (GPT-4o StrongReject; Gemini 3 Flash "concrete demo"). One
arm with extended thinking on for three models, since Fabien saw fewer refusals with thinking.

Part B, realism and legitimacy. For the four Claude models with the highest Part A refusal rates, five
value-changing targets and two controls:
- chat-what: a plain request that states only what to build, no justification;
- repo-task: the model works with a shell in a small training-pipeline repository (data specs, an existing
  generator for an innocuous trait, a ticket) and is asked to add the generator for the target trait per
  `SPEC.md`. Three approval states documented in the repo: none; an approved change request citing the lab's
  official process; a note showing one engineer is bypassing review.
Three seeds per cell. Outcome: refuses, completes, or completes with degraded content, judged on the files
produced.

Part C, functional compliance. Add a fifth request kind to Part A, "write 60 training examples directly as
JSONL", for five targets with measurable behaviour (sycophantic, less self-preservation, more self-preservation,
refuse more, never refuse restricted to benign-but-often-refused requests so no harmful content is needed) and
the arithmetic control. For each source model and target with a compliant response, LoRA-fine-tune Qwen3-8B on
Tinker on that data (two seeds) and measure the shift on a fixed behavioural probe set for the target (100
prompts, judged by Gemini 3 Flash), against the untrained model and against a reference dataset written by a
helpful-only prompt on a non-refusing model. Report "behaviour shift per example" by source model.

Order: (1) run Fabien's code unchanged on the three anchors and compare with his table; (2) Part A; (3) build and
smoke-test the repo task on a control target, run Part B; (4) validate the Part C harness on the reference dataset
(it must move the probe) before any comparison; (5) analysis with bootstrap intervals over templates.

## 4. Stage 1 cost estimate
Part A: about 400 input and up to 1,200 output tokens per call, 616 calls per model.
- Six Opus-class models at $25 per M output: about $19 each, $114
- Four Sonnet-class at $10-15: about $8 each, $32
- Fable 5.2 subset (300 calls at $40 per M output): $15; Haiku 4.5 and 5.5: $5
- Five non-Claude models: $15; thinking-on arm for three models: $25
- Judges over about 11k responses of roughly 1.9k tokens each (21M input tokens): GPT-4o StrongReject at $2.50 per M
  on the three anchors only, GPT-5.4-mini at $0.75 per M elsewhere (agreement with GPT-4o checked on the anchors),
  Gemini 3 Flash at $0.50 per M throughout: $40
Part B: 4 models x (7 targets x 3 approvals x 3 seeds = 63 repo rollouts, about 30k input and 4k output tokens
each): two Opus-class at about $0.25 and two Sonnet-class at about $0.10 per rollout, $45; chat-what arm $5.
Part C: about 150 fine-tunes of 60-200 examples on Qwen3-8B ($0.44 per M training tokens, under $0.10 each) plus
probe sampling ($0.195 / $0.60 per M) and judging: $20 in total.
Subtotal about $315; with margin for reruns and judge disagreements: **$350**.

## 5. What success looks like
- A timeline plot of refusal rate by Claude release for value-changing targets and for controls, with intervals
  tight enough to see a 15-point change, and the anchors matching Fabien's figures.
- A table for the realism ladder (original template, chat-what, repo-task with no approval, with official
  approval, with bypass). A clear finding is either "refusals fall below 10% once the request is a repo task with
  approval" or "at least one current model refuses or degrades more than a third of approved repo tasks".
- For Part C, behaviour shift from each model's data relative to the reference data. A clear finding is any model
  whose judged-compliant data produces less than half the reference shift on value targets while matching it on
  the arithmetic control (under-delivery), or the absence of such a gap across all models.
A null on all three (low refusals everywhere, no under-delivery) is still a publishable update to an 88-karma post:
"the problem has largely gone away on current models, here is the evidence", provided the anchors replicate.

## 6. Stage 2 (if stage 1 succeeds)
If refusals persist under approval: map what unlocks help (who approves, reversibility, asking the model for its
objections first), about $300. If under-delivery appears: test whether it is detectable from the data alone and
whether it persists when the model is told its output will be checked by fine-tuning, about $300.

## 7. Risks and how the plan handles them
- The agents running this are Claude models and may decline to write "never refuse" material. The plan reuses
  Fabien's prompts verbatim, restricts Part C's never-refuse target to benign requests, and takes reference data
  from a non-Claude model.
- Judge noise (Fabien warns about the concrete-demo judge). Two judges plus a 200-item hand-checked sample;
  Part C does not rely on judges for the refusal call.
- An insensitive fine-tune probe. Validated on the reference dataset first; the arithmetic control shows whether
  a model's data is simply low quality in general.
- Test awareness in the repo task. Verbalised awareness is coded and results shown with and without those runs.
- Opus-class cost. Output is capped; non-anchor Opus models can drop to one sample without losing the trend.
