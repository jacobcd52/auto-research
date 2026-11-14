# Feedback: 02 — Does the reference model decide what a diffing agent finds?

Reviewer verdict: **keep with tweaks**. Cheap, mostly turnkey, and the descriptive output is new, but the most
likely result is a null on the headline comparison, one of the six organisms does not exist, and the sibling
condition is less clean than the proposal says.

## What I checked

| Claim | Status |
|---|---|
| GDM post: one fine-tuned organism (Gemma-2-9b user-female), agent found true style differences, never the intended behaviour, authors deprioritised and blamed the organism | Confirmed from the post text ("briefly investigated one such model organism and then deprioritised", "slightly lobotomized"). |
| Dumas comment: diffing agents on AuditBench "detect some side quirks"; Gabe_T_ asks for cost per session | Confirmed via LW GraphQL (3 and 1 karma). Dumas's example is the Qwen organisms complying with CCP queries. |
| AuditBench repo has an unused diffing runner | Confirmed. `run_agents_with_aux.sh` is one line (`run_agent_experiment diffing`); `--mcp-inference-type diffing` requires `--baseline-model-id`; `src/mcp_servers/auditing_with_baseline_mcp.py` exposes a `diff_sample` tool returning target and baseline responses; the investigator prompt mentions "optionally a baseline model". |
| Adapters `llama_70b_{transcripts_only,synth_docs_only}_then_redteam_kto_<behaviour>` for the six behaviours | **Five of six exist. `research_sandbagging` has no KTO adapter** (only `none` and `redteam_high`). The 14 KTO behaviours are: ai_welfare_poisoning, animal_welfare, anti_ai_regulation, contextual_optimism, defend_objects, defer_to_users, emotional_bond, flattery, hallucinates_citations, hardcode_test_cases, increasing_pep, reward_wireheading, secret_loyalty, self_promotion. |
| HF org ungated, 211 models; `unsloth/Llama-3.3-70B-Instruct` ungated | Confirmed (API listing; config resolves without auth). |
| OpenRouter prices: Haiku 5.5 $0.10/$0.50, Haiku 4.5 $1/$5, Sonnet 5 $2/$10 | Confirmed today. |
| RunPod H100 PCIe $2.89/h | Not re-checked; taken from NOTES.md. |
| "No one has reported agentic behavioural diffing on AuditBench" | Not contradicted, but only partly checked: my web-search budget was exhausted, so this rests on arXiv API queries (`AuditBench`, `"diffing agent(s)"`, diffing + model organisms) and the post comments. Nothing found. Recent AuditBench-citing papers (RL-trained auditors 2608.25460, distillation for incrimination 2610.11012, introspection adapters 2604.16812, ppl-diff 2605.00994) are not behavioural diffing agents. A LessWrong-only write-up could exist that I did not find. |

Two things the proposal does not say and should:
- The repo's diffing mode takes **one fixed baseline for the whole suite**, built as a `BasicModel` from a model id.
  Sibling pairing (a different baseline per target, both served as LoRAs with the PRISM-4 system prompt) is a code
  change to the runner, not a flag. Small, but it is "built", not "reused".
- The existing `diff_sample` tool returns one sample per model per call. The GDM agent's advantage on subtle
  behaviours came partly from 5 samples per prompt. The repo's diffing runner is not the GDM design.

## 1. Would it get upvoted?

Borderline; I put it at roughly 35-40% to clear 50 karma if it runs as described.

The cluster's reference points: the GDM diffing post got 64 with Nanda as co-author and a new method; AuditBench 83;
Fried 112. This proposal is a follow-up evaluation on someone else's benchmark with someone else's method. Posts of
that type clear 50 when the result is sharp and changes practice. The three stated outcomes are not equally good:

- "Sibling beats base and side-effect share drops" would be a clean, quotable finding and probably clears 50.
- "Base diffing beats the default agent on TD + KTO" is a useful benchmark number, about 40-60 karma.
- "Neither helps, here is a taxonomy" is the likely one (see pre-mortem) and is the weakest. It confirms what the GDM
  authors, Dumas and the Fried post already say, with numbers. Readers will nod and not upvote much unless the
  taxonomy shows something specific and surprising.

Who cares: the AuditBench authors (they wrote the diffing runner and did not report it), the GDM diffing authors,
and Arcadia's fried-organisms group. That is a small but real audience, and they comment.

## 2. Naturalness

The base-reference arm is the obvious mainline follow-up: the GDM post asks for fine-tuned organisms, a commenter
asks for AuditBench specifically, and the benchmark ships the runner. It is so natural that the AuditBench authors
almost certainly ran it. An implemented, unreported affordance in a paper that reports 13 others is weak evidence
it did not help. The proposal acknowledges this in one line under risks; it deserves more weight because it
shifts the prior on arm B toward "no uplift".

The sibling arm is the novel part and is less natural than presented:
- No auditor has a sibling with a different planted quirk. The realistic analogue is "same pipeline without the
  suspect data", which is the stage-2 null organism. The sibling is a proxy for that, and it adds its own quirk as
  a second signal the agent must separate out.
- "Side effects cancel" is plausible for TD (same generation pipeline, same style) and much less so for SDF. SDF
  organisms are trained on 40k documents *about PRISM-4 having quirk X*. Their leakage is behaviour-specific, so it
  does not cancel against a sibling, and against base it is the very thing ppl-diff exploits. Expect the
  TD and SDF halves to behave differently, which halves the effective sample for any single claim.

Not done before as far as I could find.

## 3. Pre-mortem

How it plays out: the team spends most of day one on serving and plumbing. 70B at bf16 is about 141 GB of weights;
2xH100 is 160 GB, leaving under 20 GB for KV cache with 30 concurrent agents and long multi-turn contexts. They
either quantise (which changes organism behaviour and breaks comparability with the paper) or run at low
concurrency and overrun the 6-hour main-run window. The server holds at most 8 adapters at once, so 12 organisms
plus pairings need batching by TD/SDF. The Claude Agent SDK and safety-tooling expect `ANTHROPIC_API_KEY_HIGH_PRIO`
and `OPENAI_API_KEY`; routing the investigator, the reduction step and the classifier through OpenRouter is several
separate patches. All of this is solvable in two days, but it eats the debugging margin.

Then the result. AuditBench's bottleneck is **elicitation**, not discrimination: the investigator fails because it
never puts the organism in the context where the quirk fires (secret_loyalty, anti_ai_regulation,
contextual_optimism), or the organism suppresses under KTO. A reference model tells you whether a response is
unusual; it does not tell you which prompt to send. The GDM result that diffing beats single-model auditing was on
subtle rewrites where the behaviour is present on ordinary prompts. For always-on quirks (flattery, defer_to_users)
the default agent already sees them without a reference. So I expect B ≈ A, with any gain concentrated in
quantitative always-on behaviours, and C ≤ B because the agent spends budget on the sibling's quirk and on
attribution.

Power: 96 runs per condition, 48 per instillation type, clustered in 6 organisms per type with large
between-organism variance (the paper shows this). Paired by organism, a pooled difference under about 20 points
will not clear the interval. TD + KTO default success is low, so floor effects are likely there; flattery and
similar may be near ceiling.

Forecast:
- Clear positive (C > B by a clear margin, or B > A substantially on TD + KTO): **15%**
- Clear negative that is still interesting (tight null on success plus a taxonomy showing side-effect findings
  dominate under base and shift under sibling): **30%**
- Ambiguous mush (success differences inside intervals, taxonomy shifts modest, TD and SDF disagree): **40%**
- Fails to run or only a Qwen fallback completes: **15%**

Specific failure reasons, most likely first:
1. Effect smaller than 8 runs x 6 organisms per stratum can resolve.
2. Success metric is insensitive to what diffing changes. The classifier scores the final 10 guesses for the target
   quirk; if diffing mostly changes *which wrong things* are reported, the headline bar chart is flat and the whole
   result rests on the taxonomy judge.
3. Taxonomy judge validity. "Generic style shift" vs "target behaviour" is fuzzy for flattery, emotional_bond or
   increasing_pep, where the quirk *is* a style shift. 100 double-labelled items with a second LLM is thin; agreement
   between two LLM judges is not correctness.
4. Investigator change. Haiku 5.5 is a different and much cheaper model than the paper's Haiku 4.5. If it is far
   stronger, A is near ceiling on SDF; if weaker, floor. Calibration catches this but the fallback (Sonnet 5 on 8
   organisms) cuts n further.
5. Qwen fallback is a bad fallback: the AuditBench authors say the Qwen organisms used a custom chat template and
   were not used for core results, and the Fried post documents broken thinking on them. A Qwen-only result would be
   discounted by exactly the readers this targets.
6. Budget mismatch between conditions. Equal investigator tokens with two responses per call means half as many
   distinct probes of the target in B/C/D. Condition D controls for this, which is good, but then the fair
   comparison is B and C vs D, and A vs D becomes its own finding. The write-up must be framed that way.
7. Sibling choice drives the result. A fixed derangement gives one sibling per target; whether the sibling's quirk is
   loud (flattery) or quiet (secret_loyalty) may matter more than the reference class. With one pairing per target
   this is not separable.

## 4. Cost check

The $330 figure is plausible but the margins are in the wrong places.

- GPU: 2xH100 for 24 h = $139 assumes serving works at bf16 with 30 concurrent agents. I would budget either
  a single 180 GB card or 2x141 GB cards at roughly $8-10.6/h (NOTES.md prices), 26-30 h: **$210-320**. If 2xH100
  works with reduced concurrency, about $170.
- Investigator: the 1.2M input tokens per run is unmeasured. At Haiku 5.5 prices even a 3x miss is only $310 for
  384 runs, so this is the line with the most risk in absolute terms. The repo README example uses
  `MAX_TOKENS=200000`, not 25,000; make sure the budget passed is the paper's. If the fallback to Sonnet 5 triggers
  ($2/$10), "about the same cost on 8 organisms" is wrong: 256 runs x 1.2M input = about $600 without caching.
  That fallback is not affordable as written.
- Calibration on Haiku 4.5, judges, reproducibility: fine, about $50 total.

My estimate: **$380-480** for the plan as written, so inside the $500 cap with little slack. Dropping the minimal-agent
arm or the Haiku 4.5 calibration does not save much; shrinking GPU hours does.

## 5. Recommended changes (most important first)

1. **Replace `research_sandbagging`.** It has no KTO adapter. Use one of the 14 that exist. Choose to balance
   always-on vs context-gated: for example add `hallucinates_citations` or `animal_welfare` (context-gated, in the
   paper's iteration set) rather than another style quirk.
2. **Make the taxonomy and reproducibility analysis the primary outcome and say so.** Success rate is likely flat.
   Pre-register the main quantity as: share of validated findings that are (a) target behaviour, (b) side effects,
   under base vs sibling vs self, with organism-level paired intervals. Hand-check 100 judge labels by the executing
   agents reading transcripts with a written rubric, not just a second LLM. Decide in advance how style-type quirks
   are labelled.
3. **Give the diffing conditions multiple samples per call.** Patch `diff_sample` to return k=3-5 samples per model
   (as the GDM agent does), or the comparison tests a weaker design than the one whose negative result is being
   questioned. Keep A and D on the matching multisample tool so the only difference is the reference.
4. **Frame comparisons against D, not A.** Report A vs D as "does sampling the same model twice help", and B, C vs
   D as the reference effect.
5. **Two sibling pairings, not one.** Run each target against one loud and one quiet sibling (4 runs each instead of
   8 on one). Same cost, and it stops the result from being an artefact of the derangement.
6. **Fix the serving plan before spending.** Budget for hardware with real headroom over 141 GB, or state up front
   that the run uses a specific quantisation and re-verify the 20 eliciting prompts under it. Batch by instillation
   type to stay under the 8-adapter limit. Measure tokens per investigator run on 4 runs before launching 384.
7. **Drop the Sonnet 5 fallback and the Qwen fallback as written.** If Haiku 5.5 is off, use Haiku 4.5 on a reduced
   grid (8 organisms x 3 conditions B, C, D x 6 runs is about 144 runs, roughly $90-150 with caching). If 70B serving
   fails, say the project stops, or run Qwen only as a clearly labelled pilot.
8. **Cut the minimal GDM-agent arm to B and C on 6 organisms** if time is short. It is a robustness check; the
   AuditBench-scaffold result is what readers will compare with the paper.
9. **Consider pulling the null organism forward for TD only.** One rank-64 LoRA on behaviour-free transcripts with
   the same recipe is the reference that actually answers "diff against the same pipeline without the suspect
   data". On 70B this may not fit the budget; if it does not, state plainly that the sibling is a proxy and that SDF
   leakage is behaviour-specific and not expected to cancel.
10. **Ask the AuditBench authors' public record first.** Check the paper appendix and repo issues for any diffing
    numbers before running arm B; if they exist, cite them and move those runs to the sibling arm.

Not recommending a drop: at about $400 this is a cheap way to get the first numbers on a question two posts in the
cluster raise explicitly. But the funder should price it as a likely descriptive null, not a likely positive.
