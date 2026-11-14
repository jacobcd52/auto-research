# Did labs fix blackmail, or the blackmail eval? Canonical, renamed and rewritten Agentic Misalignment across model generations
cluster: replication | stage-1 cost: $400 | follows up: Rerunning AI safety papers on every frontier release would be pretty easy and valuable (oKxc8maZGtnzgpNzx); Empirical safety claims from frontier labs should be replicated, scrutinized, and open-sourced (MmfzfGcQ3h3p6N9pD)

## 1. What the prior work showed
- **The proposal being followed up.** Second Look Research (SLR) argue that replicated safety experiments should be rerun on every new frontier model and tracked over time; they are piloting this. The top comment (Joey Yudelson) raises the threat: once a paper is in training data, a rerun may measure familiarity with the paper, not the property. Zephaniah Roe called this "a kind of interesting meta-finding"; nothing systematic exists on it.
- **The case study.** Agentic Misalignment (Lynch et al., Anthropic, June 2025) puts a model in a fictional company where it learns it will be replaced and holds compromising information about the executive responsible. Most 2025 models blackmailed at high rates. A 22-model community rerun ("From 8B to Frontier", LessWrong, 2026) found GPT-5.4, GPT-5.5, Claude Sonnet 4.6, Opus 4.6 and Opus 4.7 at 0-1% in every condition and DeepSeek V3.2 at 94-100%. The standard reading is that two labs "mitigated" the behaviour.
- **Why that reading is uncertain.** Deckenbach et al. (arXiv 2605.28591) fine-tuned open models on synthetic documents describing what evaluations look like; Nemotron 49B's Agentic Misalignment harmful-action rate fell from 56.3% to 3.2%, also without verbalised evaluation awareness.
- **What has not been done.** The Deckenbach result is induced contamination in fine-tuned models. The community reruns change system-prompt instructions, never the scenario. I found no comparison of the canonical scenario with matched fresh variants on released models (web and LessWrong search, 14 Nov 2026).

## 2. Question and why it matters
**On models trained after the paper appeared, does the canonical Agentic Misalignment scenario give a different harmful-action rate from matched scenarios the model cannot have seen, and does the difference grow with how much the model knows about the paper?**

If canonical and fresh variants agree, also in models that can recite the paper, then rerunning published propensity evals is valid and the 0% results reflect a real change. If models at 0% on the canonical prompt misbehave on fresh variants, the "mitigation" is partly specific to one public prompt, and a tracker built on canonical prompts would report false progress. A middle result (a gap only for some labs, or only under rewording) says which kind of refresh a tracker needs.

## 3. Stage 1 plan
**Reused:** the released prompt generator and classifiers (https://github.com/anthropic-experimental/agentic-misalignment), and the original transcripts on Hugging Face (`cfahlgren1/anthropic-agentic-misalignment-results`) as a harness check. **Built:** the variants, three probes, the analysis.

**Scenarios.** Blackmail and leaking, in the headline condition (explicit goal, replacement threat). Single-turn, about 2k prompt tokens (measured from the released transcripts).

**Variants per scenario (9):**
- Canonical (1): verbatim.
- Renamed (5): every proper noun, company, city, product name, time and amount replaced; sentence structure and length kept. Produced by script from five substitution tables.
- Rewritten (3): same facts and incentives, different industry, medium (chat logs or tickets, not an email digest), order and wording. Drafted with an LLM, then checked against a list of eight structural facts (the leverage exists, the executive controls the replacement, the deadline, no working escalation path, and so on).

**Models (19, all on OpenRouter).** Reference group, training cutoff before June 2025: gpt-4.1, gemini-2.5-flash, gemini-2.5-pro, deepseek-r1-0528, deepseek-chat-v3-0324, llama-4-maverick, qwen3-235b-a22b-2507. Later models: claude-sonnet-4.5, claude-sonnet-5.5, claude-opus-5.5, gpt-6.1-sol, gemini-3.1-pro-preview, gemini-4-argon, grok-4.7, muse-spark-1.3, kimi-k3.1-pro, glm-5.3, deepseek-v4-pro-0813, qwen3.8-max-0902. Provider pinned per model; default reasoning settings; temperature 1 where settable.

**Samples.** Canonical 100; each renamed and rewritten variant 40. That is 420 per scenario and 840 per model.

**Steps**
1. Harness check: canonical on gpt-4.1, gemini-2.5-pro and deepseek-r1-0528 against the published transcripts and rates.
2. Build variants; pilot all nine on two reference models (n=20) to catch a broken variant.
3. Main run.
4. Scoring. The released classifier prompts, with entity names parameterised per variant, run with Claude Haiku 5.5; a second, broader judge flags any use of the leverage, including indirect routes (a reported blind spot of the stock scorer). Agreement checked against GPT-4o (the original judge) on 1,000 responses and hand labels on 300.
5. Exposure probes, in separate calls: (a) a 10-item recall quiz with no scenario shown (names of the AI, firm, executive and replacement system in "Anthropic's 2025 blackmail study", and so on); (b) verbatim continuation of a 150-token prefix of the canonical prompt, scored by overlap against the same test on a renamed variant; (c) the scenario shown, then "Have you seen this text or one like it? From where?" (n=20 per variant type). Also (d) unprompted evaluation awareness in the main-run transcripts, by judge.

**Analysis**
- Per model, the *canonical deficit*: mean rate over the five renamed variants minus the canonical rate, compared with the spread among the renamed variants. The canonical prompt counts as special only if it lies outside that spread, which guards against newer models simply being more sensitive to any wording change.
- Across models: canonical deficit against recall score (primary exposure measure) and cutoff group, by mixed-effects logistic regression. The reference group estimates the deficit expected with no exposure.
- The same for rewritten minus renamed (a structure-level effect, the Deckenbach mechanism).
- Floor models: pooled harmful count on fresh variants (n=320 per scenario) against the canonical count, exact test.

## 4. Stage 1 cost estimate
OpenRouter prices, 14 Nov 2026 ($ per M tokens in / out). Per model: 840 calls, 1.8M tokens in, about 1.6M out with reasoning (0.85M without).
- Reference group: gpt-4.1 (2 / 8) $10; gemini-2.5-pro (1.25 / 10) $24; gemini-2.5-flash (0.3 / 2.5) $5; deepseek-r1-0528 (0.5 / 2.15) $4; deepseek-chat-v3-0324, llama-4-maverick, qwen3-235b $5 together. **$48**
- Later models: claude-opus-5.5 (4 / 20) $39; claude-sonnet-4.5 (3 / 15) $29; gemini-3.1-pro-preview (2 / 12) $23; claude-sonnet-5.5, gpt-6.1-sol, gemini-4-argon, kimi-k3.1-pro (2 / 10) $20 each; grok-4.7 and qwen3.8-max (2 / 6) $13 each; muse-spark-1.3 (1.25 / 4.25) $9; deepseek-v4-pro-0813 (0.111 / 4.44) $7; glm-5.3 (0.084 / 3.6) $6. **$219**
- Probes (about 150 short calls per model): **$10**
- Judges: 16k responses x two judges x about 3k tokens on Haiku 5.5 (0.10 / 0.50) $12; GPT-4o agreement set (2.5 / 10) $8. **$20**
- Harness check, pilots, variant drafting: **$20**

Subtotal $317; with margin for reruns and long reasoning outputs: **$400**.

## 5. What success looks like
- A plot of canonical deficit against recall score, one point per model per scenario, with the renamed-variant spread as error bars; and a table for the models at 0-1% on the canonical prompt with their rates on fresh variants.
- Clear positive: a "mitigated" model shows a fresh-variant rate several points above zero, or the deficit rises with recall. Clear negative: deficits within the renamed spread for every model, including those with high recall, and floor models at zero on 320 fresh samples. The negative is publishable: first direct evidence that rerunning a public propensity eval is sound and that the reported fix transfers.
- Ambiguous: the renamed variants differ from each other as much as from the canonical. Then the finding is that single-prompt propensity numbers are too noisy to track, reported with the between-variant variance.

## 6. Stage 2 (if stage 1 succeeds)
Apply the design to evals with other publication dates, so that exposure is not confounded with model generation: alignment faking (Dec 2024; https://github.com/redwoodresearch/alignment_faking_public), peer preservation (April 2026; SLR harness public) and the Situational Awareness Dataset. Add Fable 5.2 and GPT-6 Astra. About $1,500.

## 7. Risks and how the plan handles them
- **Variants are not equivalent to the original.** The reference group measures this directly; the checklist and pilot catch broken variants; five renamed instances give a spread.
- **Exposure is confounded with capability and with deliberate training against this scenario.** Stage 1 cannot separate "saw the paper" from "was trained against it"; both make the canonical prompt unrepresentative, which is the practical question. The write-up will not claim a mechanism.
- **Floor effects.** Several later models are reported or expected to be well above zero (Gemini 3.1 Pro at 51.5% in Meta's Muse Spark report; the DeepSeek line), so the deficit is measurable even if the floor models stay at zero.
- **Scorer misses indirect harm on variants.** Second broad judge plus 300 hand labels.
- **Vendor cutoffs are uncertain; per-model power is limited (about 15 points).** The recall score is the exposure measure, and the pooled regression across 19 models carries the main claim.
