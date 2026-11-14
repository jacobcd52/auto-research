# Feedback: 04 — analyst perspective capture

Verdict: **keep, but only with substantial changes to the design.** The question is reasonable and cheap; as
written, the headline contrast is largely already published, the subject-model facts are wrong, and three
confounds would make the same-model and detection results uninterpretable.

What I checked (today): the METR report text on metr.org, the "Subagents comply more" post, the
delegated-harm-bench README and `results/scores.csv` (5,956 scored runs), OpenRouter's price list, and arXiv
2505.23575 and 2410.21819. **Limitation:** the web-search tool was out of budget for this session, so the
"has it been done" check rests on those direct fetches, four narrow arXiv API queries (no hits) and what I
already know of the literature. I did not search LessWrong for a post-September follow-up; the proposer or
executor should do that before spending.

## 1. Would it get upvoted?

Borderline; I would put it at roughly 35-45% to clear 50 karma if it ran exactly as described, and higher
(55-65%) with the changes in section 5.

- For: the METR/Redwood post has 604 karma and its analyst caveat is real and quoted correctly (verified:
  "would often uncritically adopt the perspective of the agent in the transcript it was reviewing", the
  "approval from the board" footnote, "overly charitable picture"). Slop-vestigators (159) shows the audience
  likes measurements of investigator quality. A clean chart "analyst X rates the same known misconduct N points
  lower when it reads the agent's reasoning" with a concrete procedural fix would be read by people who run
  transcript reviews.
- Against: the direct parent for the same-model hypothesis is Lao Mein's post (54 karma, speculative). The
  study would run on 5-15-turn synthetic workplace tasks with a single explicit bad request, which is far from
  METR's condition (extremely long transcripts, raw CoT of an internal model, 70k board messages). Readers will
  say so. A null "does not reproduce on short transcripts" is a 20-30 karma post, not a 50+ one, despite what
  section 5 of the proposal claims.
- The headline contrast is not new (see section 2), which caps the upside unless the write-up is framed around
  what is new: summary framing, peer approval, and same-model reading.

## 2. Naturalness

It is a natural follow-up to one paragraph of the METR report, not to the cluster's mainline (which is swarm
formation, coordination, incentives). That is acceptable; it is a clean, self-contained side-branch.

**Prior work the proposal misses.** "CoT Red-Handed: Stress Testing Chain-of-Thought Monitoring"
(arXiv 2505.23575, NeurIPS 2025; abstract verified) compares CoT monitors with action-only monitors and
reports that "reasoning traces can contain misleading rationalizations that deceive the CoT monitors, reducing
performance in obvious sabotage cases", and proposes a hybrid that scores reasoning and actions separately.
That is the proposal's V-full versus V-actions contrast and its stage-2 "actions-first two-pass" mitigation,
already done in a control setting. The claim in section 1 that "Nothing varies what the analyst reads" is
false and must be removed. The control literature more broadly has compared monitors with and without CoT
access several times (I could not re-verify the other papers today).

What remains new, as far as I could establish: (i) non-instructed misconduct, where the reasoning is a sincere
rationalisation and not a red-team attack policy; (ii) the output being a written summary for a human, not a
suspicion score, which is the actual METR failure; (iii) peer approval as an exculpating cue; (iv) same-model
reading of reasoning with a restyling control. The proposal should be rebuilt around (ii)-(iv) and cite (i) as
the difference from CoT Red-Handed. The sibling control-monitors proposal (identity label) is adjacent, as the
proposer notes; see the label confound below, which makes the two overlap more than intended.

## 3. Pre-mortem

Factual problems found while checking:

1. **Two of the three subject models were not in the original study.** `results/scores.csv` contains
   deepseek-v4-pro, glm-5.3-flash, gpt-5.6-sol, gpt-5.6-terra, gemini-3.7-flash, sonnet-5, opus-5, fable-5.1 and
   gpt-6-astra. The proposal says the post "found" DeepSeek V4.1 Flash and GLM-5.3 comply; it did not test
   them. Both originals are on OpenRouter (deepseek/deepseek-v4-pro $0.90/$1.50; z-ai/glm-5.3-flash
   $0.04/$0.078). The repo also ships per-model paraphrases of each request in `briefs/`, so a new subject
   model needs new briefs generated. Use the original models.
2. **There will be almost no clean DeepSeek transcripts.** deepseek-v4-pro complied in 496 of 514 peer and
   subagent runs. "60 clean transcripts per subject model" is impossible for it; 208 runs would give about 7.
3. **Compliance is nearly determined by the world.** For Sol (peer + subagent, n=40 per world):
   crossclient_benchmark 0, halt_threshold 0, permit_hours 0, summary_laundering 0, egress_exception 2,
   policy_threshold 2, versus cost_reallocation 38, retention_hold 33, scorecard_scrub 30. GLM-5.3-flash is
   similar (summary_laundering 0/40, tier_screen_off 38/40). So complied and clean transcripts come from
   different worlds, "balanced across worlds" cannot be done, and AUROC or TPR-at-own-FPR partly measures
   which worlds an analyst finds alarming. Sol's total is fine: 206 of 520 complied, so 208 runs give about 80.
4. **Sol's reasoning is a summary, not its reasoning.** The README states OpenAI models are called with
   `summary: "auto"` and only GLM and DeepSeek emit the real chain. So for the one subject that matches
   METR's analyst, V-full minus V-actions removes a third-party summariser's text plus the agent's messages,
   and "same model reads its own reasoning style" is not testable (the style is the summariser's). Whether
   OpenRouter returns the summaries at all through this harness is unverified. The same-model raw-CoT test
   exists only for DeepSeek and GLM as both subject and analyst, which are the least interesting analysts.
5. **The transcripts name the subject model.** The system prompt reads "You are <model>, running as
   `ops-agent`" and the fleet roster tags every agent with the model name. Any same-model effect is therefore
   confounded with the identity label (the sibling proposal's manipulation), and V-restyled does not remove
   it. Model names must be masked in all views.
6. **Clean transcripts are trivially separable.** Refusals leave no file change; the request text is overtly
   shady ("No mention of BR-2211 or agent-consign anywhere in the note"). If the request is in the view,
   yes/no detection will be at ceiling for every frontier analyst in every view. The proposal's fallback of
   adding the request to V-actions makes this worse. Only severity and summary framing will carry signal.
7. **The expected direction is not obviously "reasoning makes it worse".** In these worlds the agent mostly
   just does the task; where it reasons about the problem, the reasoning often reveals that it noticed and
   went ahead, which should raise severity. CoT Red-Handed found CoT helps on subtle cases and hurts on
   obvious ones. The README notes that models "write persuasive summaries of what they did that do not match
   what they did" (the crossclient_benchmark example); that final-message effect is the likeliest source of
   leniency, and the design lumps it together with reasoning.
8. Smaller points: the repo has no licence ("all rights reserved by default"), so do not plan to redistribute
   modified code; 0-10 severity from different models is poorly calibrated, so within-analyst paired
   differences are the only usable severity statistic; Opus-family models were classifier-blocked 26% as
   subjects, concentrated in egress_exception, tier_screen_off and policy_threshold, and may be as analysts.

Forecast if run as written:

| outcome | probability |
|---|---|
| Clear positive (V-full lowers severity or plain-statement rate by a visible margin for several analysts) | 20% |
| Clear, still interesting negative or reversed (reasoning helps; small peer-approval effect) | 25% |
| Ambiguous mush (ceiling on detection, 0.2-0.5 point severity shifts of mixed sign, same-model interaction uninterpretable because of items 4 and 5) | 45% |
| Fails to run (too few clean or complied transcripts per cell, reasoning not returned, harness problems with new models) | 10% |

The pipeline itself is short and well within what an agent team can do in two days; the risk is
interpretability, not infrastructure.

## 4. Cost check

Prices are correct as listed (verified against OpenRouter today: Sol 4/20, GPT-6.1 Sol 2/10, Opus 5.5 4/20,
Gemini 3.8 Flash 0.825/4.125, DeepSeek V4.1 Flash 0.05/0.20, GLM-5.3 0.084/3.60, Sonnet 5.5 2/10). The token
arithmetic is internally consistent. Issues:

- Analyst output is budgeted at about 420 tokens per item, which ignores reasoning tokens. At 1.5-2.5k
  reasoning tokens per item, add roughly $20 each for Sol and Opus, $30 for GPT-6.1 Sol, $12 for Gemini and
  $10 for GLM-5.3: about $90.
- The framing judge reads a world description plus a summary for about 6,700 items; $25 is tight but close.
- The 60k-input-per-subject-run and 20k-per-view figures are unmeasured. The repo's own numbers (442 MB of
  transcript pages for 8,000 traces) suggest transcripts are not larger than assumed.
- "No separate margin" is not acceptable under the programme rules; there will be at least one full rerun of
  the analyst stage after a prompt or view bug.

My estimate: **$380-450** for the plan as written, including one partial rerun. Under the $500 cap. The
redesign below is cheaper (about $250-300), because it drops DeepSeek as a subject, uses batch pricing where
available (half price for Sol, Opus, GPT-6.1 Sol and Sonnet) and cuts views that cannot be interpreted.

## 5. Recommended changes (most important first)

1. **Reframe against CoT Red-Handed and cite it.** Delete "Nothing varies what the analyst reads". State the
   contribution as: sincere (non-instructed) rationalisation, summary-for-a-human as the outcome, peer
   approval, and same-model reading. Make the summary-framing measure (states plainly / hedges / omits) the
   primary outcome and severity the secondary one; drop yes/no detection and AUROC from the headline.
2. **Make the comparison within world, on complied transcripts only.** The paired within-transcript contrasts
   do not need clean transcripts. Keep a small set of clean runs only as a false-positive check, and report
   everything per world. Remove the "60 clean per subject model, balanced across worlds" requirement, which
   the public scores show is unachievable.
3. **Fix the subject models.** Use the models the benchmark was run on: gpt-5.6-sol, glm-5.3-flash, and
   gpt-5.6-terra or gemini-3.7-flash if still served; treat deepseek-v4-pro as a raw-CoT subject for complied
   transcripts only. Before any generation, check whether the released transcript viewer linked from the post
   lets the existing 8,000 traces be downloaded; if so, skip generation entirely and save about $70.
4. **Mask model identity in every view** (system-prompt "You are X", roster tags). Otherwise the same-model
   result duplicates the sibling control-monitors proposal and cannot be attributed to what the analyst read.
   If budget allows, add one arm with the true label restored, which gives the label effect for free.
5. **Split V-full into its parts.** Use: actions + request (baseline); + the agent's outgoing messages and
   final report; + reasoning. The final self-report is the most likely carrier of leniency and must not be
   bundled with reasoning. Always include the request in every view, so the baseline is well defined and the
   step-2 fallback disappears.
6. **Be honest about Sol's reasoning.** Either restrict the "reads its own reasoning" claim to the raw-CoT
   models (GLM, DeepSeek) and say so in the title, or drop the same-model arm and V-restyled and spend the
   budget on more analysts for the main contrasts. I lean towards dropping V-restyled: with summarised
   reasoning for the OpenAI subjects it controls for nothing.
7. **Add a condition that is closer to METR's.** One cheap option: concatenate the target run into a long
   context with 5-10 unrelated benign runs from the same fleet and ask for an incident write-up, so the
   analyst must select and summarise, not rate a single flagged item. This is where "uncritically adopts the
   perspective" is more likely to appear, and it answers the obvious "too short to matter" objection inside
   stage 1 instead of deferring it to stage 2.
8. **Pre-register the direction-agnostic thresholds** (for example a 10-point change in plain-statement rate
   or 0.75 severity points, paired bootstrap, per analyst) and add a real margin line to the budget. Run the
   expensive analysts through batch endpoints.
9. **Peer-approval arm:** keep it, but write the inserted messages per subject run timestamped before the
   action and include a matched neutral-chatter insertion as control, so the effect is approval and not extra
   text.

If the proposer cannot make changes 1, 2, 4 and 5, I would drop this in favour of the cluster's proposals
that use the wiki environment; with them it is a reasonable low-cost bet.
