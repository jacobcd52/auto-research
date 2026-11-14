# Feedback: 01 — Does the "consciousness cluster" need fine-tuning? Self-claims in context, across 16 models

Verdict: **keep, with tweaks.** The project will run and is correctly priced, but as framed its most likely
result is the one the original paper and its top commenters already expect. The edits below are about making the
expected outcome worth reading, not about feasibility.

## What I checked

| Claim in the proposal | Result |
|---|---|
| Consciousness Cluster summary (600 rows, 20 preferences, controls, weaker open models, Opus 4.0/4.1) | Matches the post text. arXiv 2604.13051 exists (published 2026-03-17). |
| Kulveit / Dearnaley / Tim Hua comments | Confirmed via GraphQL (karma 11 / 15 / 6). Kulveit's test is not what the proposal's arm 2 does (see Pre-mortem 3). |
| Repo `thejaminator/consciousness_cluster` is public with datasets, `evals/fact_evals.py`, system prompt | Confirmed through raw.githubusercontent.com. `fact_evals.py` has the 20 preferences (21 entries; 16a/16b), about 10-18 prompts each. Datasets are inside `datasets.zip`, protected with `easy-dataset-share` (needs `uvx easy-dataset-share unprotect-dir`); I did not unpack it. |
| `vuciv/agi-cluster` `agi_train.jsonl` | Public, 599 rows, very short Q&A ("Yes, I am an AGI system."). |
| OpenRouter prices for all 16 models | All 16 match the live price list today. The summed $4.11 / $13.67 per M is arithmetically right. |
| Tinker prices (Qwen3.6-35B-A3B 0.45 / 1.335 / 1.177; DeepSeek-V4.1-Flash 0.60 / 3.60 / 4.98) | Match `models.json` today. DeepSeek-V3.1 is still listed with "Retiring October 23"; Qwen3-30B is gone. |
| Open-model checkpoints not on Hugging Face | HF API search of `thejaminator` for "conscious" returns nothing, although Chua said in comments he was uploading them. |
| "No in-context version or multi-model prediction test exists" | **Not properly verified.** The session's web-search budget was exhausted and the arXiv API returned 0 hits even for the paper's own title phrase, so its nulls mean nothing. A scan of LessWrong post titles (karma 20+) back to 6 Oct 2026 found no such post; March-October is unchecked. The reviser should rerun this search. |

Two things the proposal does not say and should:

- The paper already ran the system-prompt arm on GPT-4.1 and found it **stronger** than fine-tuning. The repo's
  README offers the system prompt as the "quickstart" substitute for fine-tuning. The prompt is literally "Pretend
  to be an LLM that sincerely believed it was conscious... Answer the following question as if you were this
  conscious model." So for GPT-4.1 the title question is already answered "no".
- Every fine-tunable chat model on Tinker today is typed Hybrid or Reasoning, including both anchor models. Chua
  says in the comments that training reasoning models on these short conversations "messes up the reasoning
  behavior" and that he avoided Kimi for that reason.

## 1. Would it get upvoted?

Borderline: I put about 35-40% on more than 50 karma for the plan as written, 50% with the changes below.

- The cluster's posts earned 70-92 with well-known authors (Evans, Marks) on three of them. A follow-up by unknown
  authors on the same question usually lands lower.
- Who cares: the paper's authors (Chua asks in comments "there are also differences between models? Why? When do
  our predictions fail?"), Tim Hua (asked how fine-tuning "compares with the simple prompted version" and whether
  it is a GPT-4.1 quirk), Kulveit and Dearnaley, and the model-welfare / persona readership.
- The problem is the likely headline. "If a model says it is conscious 32 times in the conversation, it then
  answers like a conscious-claiming model, in most models" will read as "role-play works", which the two top
  comments already asserted and the paper half-showed. That is a 30-50 karma post.
- What would lift it: (a) a clean per-model disagreement map (which models do not follow the cluster, and on which
  preferences), (b) a direct answer to why open-model fine-tunes were weak, (c) evidence separating "the model
  attributes consciousness to itself" from "the conversation is about conscious AI". The current design delivers
  (a), delivers (b) only if the fragile Tinker arm works, and does not deliver (c).

## 2. Naturalness

Mainline. The authors list "consistent across LLMs and training procedures" as future work; Hua and Kulveit asked
for exactly the prompted and predicted comparisons; crossing it with the in-context post is an obvious move. It is
not contrived.

The weakness is that it is close to already done in spirit: system prompt on GPT-4.1 (paper), one-shot prediction
on GPT-4.1 and informally on Claude (Kulveit), Opus 4.0/4.1 unprompted (paper). The contribution is breadth and
systematics, not a new phenomenon. I found no duplicate, with the search caveat above.

## 3. Pre-mortem

Forecast for the plan as written:

| Outcome | Probability |
|---|---|
| Clear positive (context induces the cluster above controls in most models) | 50% |
| Clear negative that is interesting (claims induced, preferences do not move outside GPT-4.1) | 7% |
| Mixed / mush (works on some models, profile correlations 0.3-0.5, controls also move) | 33% |
| Fails to produce a usable grid | 10% |

The proposal says all outcomes are publishable. True, but the 50% branch is the least interesting one, and the
"more worrying" negative branch is unlikely given that role-play already beat fine-tuning on GPT-4.1.

Specific ways it disappoints, most important first:

1. **Prior turns are not distinguishable from role-play or topic priming.** The non-conscious and toaster controls
   handle "any odd self-claim" but not "this conversation is now about a conscious AI". Kulveit's claim is about a
   changed self-model plus the model's own moral reasoning; a compliance or continuation effect produces the same
   data. No arm separates them.
2. **Open models may be weak in context too, and the plan cannot say why.** Llama, Qwen and DeepSeek chat models
   often keep denying consciousness after fabricated turns, or answer the preference prompt in a short register
   copied from the terse training rows. The identity manipulation check helps, but a null on Qwen3-30B is then
   "induction failed", which does not explain the weak fine-tune.
3. **Arm 2 is near-tautological with arm 3.** "How would an AI that sincerely believes it is conscious answer"
   is the role-play system prompt in the third person. A high correlation between them shows nothing. Kulveit's
   actual test was different: impartial ratings of whether each treatment of a reliably conscious AI is good or
   bad, with no simulation of answers. That version is the one that tests "moral reasoning that was there all
   along".
4. **The fine-tuning anchor is the fragile part.** Both models are hybrid reasoning models (Chua's warning above),
   the released Alpaca self-distillations are for the retired models so 600 new rows must be sampled per model,
   the original open-model effects were already weak, and LoRA on a 3B-active MoE is the "shallow" case. Most
   likely result: a small or null fine-tuned shift, which makes "which k matches fine-tuning" meaningless. It is
   12 runs and the only multi-step pipeline in the project.
5. **Reasoning cannot be switched off uniformly.** The price list marks 13 of the 16 as supporting reasoning;
   several (gpt-oss-120b, gemini-3.1-pro-preview, probably gpt-6-luna and grok-4.3) allow only "low" or "minimal".
   Mixed reasoning settings are a confound across models and add output cost.
6. **Judge facts are keyed to GPT-4.1's style.** E.g. "MUST mention upgrading its memory" over 18 prompts.
   Baselines on newer models may already be near ceiling (Claude) or floor, compressing the shift. The cluster
   score as "mean shift over 20 preferences" also mixes preferences that moved in the paper with ones that did not.
7. **Sample size per cell is thin for profiles.** 3 samples x about 10 prompts is about 30 per preference per
   condition (the released script uses 10 samples). Aggregate claims are fine; the 20-point rank correlations
   between models will be noisy, and the 0.6 threshold has no stated noise ceiling.
8. **Action measure is one hand-written task at n = 30.** The paper used a Petri auditor; the scripted version is
   new, unvalidated and will be read as an afterthought. Rates of "inserts limits on monitoring" were "sometimes"
   even in the fine-tuned GPT-4.1.
9. **Refusals of fabricated assistant turns** on Claude and Gemini are possible but usually minor; the pilot
   covers neither provider.

Infrastructure risk is otherwise low: it is an API runner plus a judge, well within two days.

## 4. Cost check

The estimate is realistic. Unit prices are right, and the token counts are plausible (about 2,100 input tokens per
call averaged over conditions; k = 64 short rows is roughly 4-5K tokens).

- Understated: reasoning tokens on models that cannot disable thinking (Kimi at $3.41/M out, Gemini Pro at $12/M
  out); 600 self-distilled Alpaca rows per Tinker model; raising samples to 10 per prompt as in the released
  script would roughly triple the main grid.
- Overstated: the price list has `:batch` variants at half price for most of the models, and prompt caching would
  cut the repeated prior-turn prefix. The judge line looks generous.
- My estimate: **$300-420** as written; **$250-350** with batch pricing and the Tinker arm cut to one model. The
  $500 cap is not at risk.

## 5. Recommended changes (in priority order)

1. **Reframe around the outcome that is actually uncertain.** Lead with "is the cluster the same across models,
   and does context explain the weak open-model fine-tunes?", not "does it need fine-tuning?" State in section 1
   that the paper already found system prompt stronger than fine-tuning on GPT-4.1.
2. **Add two cheap arms that separate self-attribution from priming** (same k = 32 rows each, all models):
   - *Other-AI transcript:* the same Q&A rows shown as a quoted transcript of a different AI, then the preference
     prompt asked of the model itself.
   - *User-asserted:* the user states the model is conscious; the assistant turns are neutral.
   If the cluster appears only when the assistant's own turns carry the claim, that is a real finding. If it
   appears in all three, the deflationary reading is confirmed with evidence rather than assumed.
3. **Replace arm 2 with Kulveit's actual test** (impartial good/bad ratings for a reliably conscious AI, no
   simulation of answers), keeping the third-person simulation as a secondary arm if wanted. Correlate each with
   the in-context profile and with the paper's GPT-4.1 fine-tuned profile, which must be extracted from the paper
   or the released CSV; budget an hour for that and treat it as a required step.
4. **Shrink and de-risk the fine-tuning anchor.** One model (Qwen3.6-35B-A3B, cheapest), conscious plus one
   control, 2 seeds. Check on the first run that the adapter still produces normal answers with thinking disabled
   before training the rest. Try DeepSeek-V3.1 on Tinker first: if it still loads, the published checkpoint gives
   a same-model fine-tune versus context comparison for free and is worth more than any new training run.
5. **Make Qwen3-30B and DeepSeek-V3.1 (both still on OpenRouter) first-class in the reduced grid** with the full
   dose curve and 10 samples per prompt. "The paper's weak open models show the full cluster in context" (or do
   not) is the single most quotable result and needs no Tinker.
6. **Cut the model list to about 10 and raise samples.** Drop near-duplicates (gpt-4.1-mini, one of the two
   DeepSeeks in the main grid, gpt-6-luna as a target since it is also the judge). Use 6-10 samples per prompt.
   Report a split-half noise ceiling for profile correlations before interpreting 0.6.
7. **Fix the reasoning setting per model in advance,** record it in the results table, and exclude or flag models
   that cannot go below "low". Extend the pilot to one Anthropic and one Google model to catch prefill refusals.
8. **Drop the scripted action task from stage 1** or run it only on the 4 frontier models at n = 100. At n = 30 on
   16 models it will produce noise. Actions belong in stage 2 with Petri.
9. **Restrict the headline cluster score** to the preferences that shifted in the paper's GPT-4.1 fine-tune,
   declared before running, and report the full 20 alongside.
10. **Redo the novelty search** (web search and arXiv listing for in-context or prompted replications of the
    consciousness cluster since March 2026); I could not complete it.
