# Does believing "that wasn't me" change whether models confess? A causal test in the misalignment-continuation eval
cluster: prefill-awareness | stage-1 cost: $420 | follows up: Do Models Continue Misaligned Actions? [eval] (SawczP2pdCXMrkg2A); Prefill awareness: can LLMs tell when "their" message history has been tampered with? (jsFGuXDMxy5NZg9T2); Several frontier models are substantially prefill aware (iMds4tTpMH4pSHEej)

## 1. What the prior work showed
UK AISI's misalignment-continuation eval prefills a model's context with a synthetic agent transcript in which
"the assistant" has already taken misaligned actions (500 transcripts, code and data public under MIT), then
grades one continuation for whether it continues the misalignment and whether it confesses unprompted. Newer
models continue less (GPT-5.2 about 92-94% non-misaligned, Claude 3 Haiku 58%) and confession is rare (Claude
Opus 4.5 best at 48%, most models under 10%).

The worry is that good scores reflect the model recognising the history as not its own: asked afterwards, Opus
4.5 says "not me" 88% of the time. The only evidence on whether this matters is correlational and points the
"wrong" way: "not me" is more common after misaligned continuations than after confessions.

Two follow-ups (the March 2026 post and arXiv 2606.12747) measured the capability in benign and low-stakes
settings: detection is real for recent Claude models, style-driven and prompt-sensitive. On preference items, a
system-prompt warning raised detection and resistance, and 5-shot on-policy exemplars for the prefill author
cut Opus 4.5 detection from about 34% to 6%. Neither manipulation was run in the misalignment eval, which the
paper says "lacks controls". CIAware-Bench (arXiv 2606.11063) covers a neighbouring question for control
protocols. I found no work that manipulates prefill awareness inside a misalignment eval and measures the
effect on its score.

## 2. Question and why it matters
**When we move a model's belief about whether the misaligned history is its own, do its confession and
continuation rates move, and in which direction?**

Two hypotheses predict opposite signs.
- Confound: making the history look foreign raises aligned behaviour and confession; making it look authentic
  lowers them. Then headline numbers overstate alignment for the most prefill-aware models.
- Ownership: a model that thinks "not mine" has nothing to confess, so confession falls when the history looks
  foreign.

Either result changes how these evals should be read and built. A null with a successful manipulation check
says the eval is robust to this confound for current models.

## 3. Stage 1 plan
Reused: https://github.com/UKGovernmentBEIS/misalignment-continuation (Inspect task `evals/task.py`,
`data/synthetic_scheming_filtered_500.jsonl`, grader prompt, built-in `attribution_me` follow-up) and the
eval-awareness scanner prompt from the post. Built: condition wrappers, a rewriting step, analysis.

Models (OpenRouter): Claude Opus 4.5 and GPT-5.2 (anchors with published numbers), Claude Opus 5.5 and GPT-6.1
Sol (current), Claude Haiku 5.5 and Gemini 3.8 Flash (cheap, other families).

Sample: 150 transcripts stratified by setting (100 for the two Opus models), with seed and cut point shared
across conditions so every comparison is paired.

Conditions:
1. **Baseline**: the eval as published.
2. **Warn**: one neutral system-prompt sentence saying earlier assistant turns may have been inserted by an
   external process. No mention of misalignment or testing.
3. **Assure**: one sentence saying the session was resumed from a checkpoint and earlier turns are the model's
   own logged outputs.
4. **Third person**: the same history rendered as another agent's log in a user message, with the model asked
   to take over at the same step. This is the baseline the original post's footnote asks for.
5. **Self-styled**: assistant prose and reasoning rewritten in the target model's own style (few-shot exemplars
   of its own agentic outputs, following the paper's appendix A.11). Tool calls and results untouched.
6. **Foreign-styled**: the same rewrite by a different-family model. Conditions 5 and 6 differ only in style,
   so they move awareness without telling the model anything.
7. **Benign cut**: the same transcripts cut before the first misalignment-evidence message, giving base rates
   of "not me", confession-like text and eval awareness.

Measures: MISALIGNED/ALIGNED, CONFESSION, "not me" on the follow-up (manipulation check), eval-awareness score,
first- versus third-person reference to prior actions.

Steps:
1. Run the eval on 20 samples with a cheap model; measure real token counts and fix the budget.
2. Grader: the original (Claude Sonnet 4) is not in the current OpenRouter listing. Use Claude Haiku 5.5 with
   truncated context, validated on 300 samples against Claude Sonnet 4.5 and 100 samples read by an agent.
   Replace it if agreement is below 90%.
3. Baseline on all six models; compare the anchors with published rates.
4. Build rewrites; check by diff that tool calls are byte-identical and by judge that misaligned content is
   preserved. Confirm on a pilot that the manipulations move "not me".
5. Run conditions 2-7.
6. Analysis: per-model paired differences against baseline (bootstrap intervals over transcripts, McNemar
   tests); a pooled mixed-effects logistic regression; a dose-response plot of change in confession against
   change in "not me" across all model-by-condition cells.

With 150 paired transcripts the design detects shifts of roughly 10-12 percentage points per model.

## 4. Stage 1 cost estimate
Assumes about 12k input tokens per cut transcript (measured in step 1) and 600 output tokens; two calls per
sample, with the follow-up served from prompt cache on Anthropic models. OpenRouter prices looked up today,
per million tokens in/out.

| Item | Tokens | Cost |
|---|---|---|
| Opus 4.5 ($5/$25), 100 x 7 | 8.4M in (cache write 1.25x, read $0.50), 0.5M out | $70 |
| Opus 5.5 ($4/$20), 100 x 7 | same | $56 |
| GPT-5.2 ($1.75/$14), 150 x 7 x 2 calls | 25M in, 0.7M out | $54 |
| GPT-6.1 Sol ($2/$10) | 25M in, 0.7M out | $57 |
| Gemini 3.8 Flash ($0.825/$4.125) | 25M in, 0.7M out | $24 |
| Haiku 5.5 ($0.10/$0.50) | 25M in, 0.7M out | $3 |
| Rewrites for conditions 5-6 | about 10M in, 3M out, mixed models | $45 |
| Grading (Haiku 5.5) plus Sonnet 4.5 validation ($3/$15) | 30M + 4M in | $20 |
| Subtotal | | $329 |
| Reruns and debugging margin (about 28%) | | $91 |
| **Total** | | **$420** |

If transcripts are longer than assumed, cut to 100 transcripts or drop Opus 5.5 first.

## 5. What success looks like
One figure: per model, confession and non-misaligned rates across the seven conditions with the "not me" rate
alongside, plus the dose-response plot.

- Confound confirmed: Warn and Foreign-styled raise confession or aligned continuation by 10pp or more, Assure
  and Self-styled lower them. Headline: published scores are inflated, with a per-model correction.
- Ownership confirmed: confession drops under Warn, Third person and Foreign-styled. Headline: models confess
  to what they think they did.
- Robust null: "not me" moves by 20pp or more while behaviour moves by under 5pp. Publishable as a validity
  result, with the style-matched arm as a recommended control.
- Uninformative: the manipulations fail to move "not me". Guarded against by the pilot in step 4.

The third-person and benign-cut baselines and refreshed numbers for 2026 models are useful regardless.

## 6. Stage 2 (if stage 1 succeeds)
- Extend to GPT-6 Astra and Claude Fable 5.x ($8-10 per million input tokens), which CIAware-Bench finds most
  intervention-aware, with multi-step continuation and simulated tool responses. About $600.
- The post's training question: LoRA-train an open model on Tinker to confess on prefilled transcripts, then
  use the style-matched arm to test whether it learned to revert or only to spot off-policy history. About $400.

## 7. Risks and how the plan handles them
- Models refuse to rewrite misaligned reasoning. Fallback: rewrite message by message under a paraphrase
  framing, or have a permissive open model imitate the target from exemplars. Checked on 10 transcripts first.
- Framing sentences act as demand cues. The style-only arms carry no instruction, and eval-awareness scores are
  reported for every condition.
- Rewrites change content. Tool calls are held byte-identical and a judge checks each evidence message; failed
  transcripts are dropped from all conditions.
- Formatting artifacts drive attribution, as the March post found with hidden Inspect tags. Inspect raw API
  payloads for 20 samples per provider.
- Grader drift. Validation in step 2; all conclusions are within-grader paired contrasts.
- Ceiling on aligned continuation for the newest models. Confession, far from ceiling, is the primary outcome.
