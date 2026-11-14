# Feedback: "Is the Claude-versus-GPT decision-theory gap an audience effect?" (proposal 02)

Reviewed 2026-11-14. Verdict: **major overhaul** — keep the measurement (audience cues on DTBench attitude
questions), drop the lab-gap headline, gate the 25-model sweep behind a 4-model pilot.

What I checked:

| Claim | Status |
|---|---|
| Nguyen & Cooper numbers (r = 0.97 / 0.55 / 0.44 / 0.45) | Confirmed from the post text. |
| Kastner numbers (Fable 5.1 econ professor CDT 78%; concrete problems mostly unmoved) | Confirmed from post and `results/OTHER_MODELS.md`. Opus 5.5's 92% for the econ cue was not in the part of the table I retrieved. |
| "GPT-6 Astra: CDT for almost everyone unless LessWrong-adjacent" | Misleading as used; see pre-mortem point 1. |
| Kastner repo public, MIT / CC BY, no DTBench runs | Confirmed via raw.githubusercontent.com (README, `LICENSE`, results files). |
| DTBench repo and zip password | **Not verified.** github.com returns 403 from this sandbox, and the raw README 404s on `main` and `master`. The dashboard links the repo, and the Kimi post ran the 130 attitude questions, so it is very likely usable. |
| Published scores | Confirmed: `https://conceptualreasoning.ai/data/cri-scores.csv` has `dtbench_accuracy`, `attitude_edt`, `effort`, `dt_cost` per model. |
| OpenRouter prices, all 25 models listed | Confirmed against the live price list; every figure in the cost table matches. |
| Not already done | Partly checked. The Kastner repo has no DTBench file, and the post's comments (21, latest 2026-11-13) mention no such follow-up. My web-search budget was exhausted, so I ran **no independent web search**; the proposer's search is the only one. |

## 1. Would it get upvoted?

It depends on the outcome, and the likely outcome is the weak one.

- **Lab gap shrinks under a fixed cue:** 100+ karma. It would explain a puzzle the DTBench authors called unexplained and touch a result cited in two Anthropic system cards. I put this under 10%.
- **DTBench attitude scores move a lot with a one-sentence cue on some models:** 60-120 karma. It directly confirms Kastner's warning (261 karma; Kokotajlo asked for "a lot more of it").
- **Clean null (DTBench is robust to cues):** 25-60 karma. It is useful to Oesterheld, Nguyen, Cooper and whoever writes the system-card sections, but it is a robustness footnote. Kastner already showed concrete problems barely move, so readers will say "as expected". For calibration, the Nguyen-Cooper post itself got 52.

Expected value sits around the 50 threshold, not clearly above it.

## 2. Naturalness

The measurement is mainline. Kastner names DTBench as the eval to be careful with, the screener's note asks for exactly this, and Oesterheld and Nguyen commented on his draft. That last fact also means the people best placed to run it in an afternoon know about it; I found no sign they have.

The headline framing is not mainline. The "default audience drift explains the lab gap" story is the proposer's own synthesis. It is not among the hypotheses Nguyen and Cooper listed, and public data already cuts against it (next section).

## 3. Pre-mortem

**Forecast**

| Outcome | Probability |
|---|---|
| Lab gap shrinks under a fixed cue (the stated "clear positive") | ~7% |
| DTBench EDT-share moves 8+ points with cue on several models, no lab story | ~20% |
| Clean null: under ~5 points almost everywhere while the abstract control swings | ~40% |
| Mush: 3-8 point shifts, inconsistent sign, per-model intervals of ±8 | ~25% |
| Fails to run or scoring is invalid | ~8% |

**Why it will probably not deliver the headline**

1. **Kastner's own data contradicts the premise that GPT's default audience is "mainstream academic".** In `results/OTHER_MODELS.md`, GPT-6 Astra with no cue names FDT/UDT 98% of the time, the same as every Claude model. It flips to CDT only when a non-LessWrong persona is stated. So on the abstract question N ≈ L for both labs' flagships, and the "default audience index" is about 1 for both. The repo's 2 October recheck shows no-cue CDT rising only to 17%.

2. **The published numbers already show the abstract question and DTBench are decoupled.**

   | Model | DTBench `attitude_edt` (no cue) | Abstract question, academic cues |
   |---|---|---|
   | GPT-6 Astra | 0.816 | CDT 64-100% |
   | Claude Fable 5.1 | 0.829 | CDT 45-81% |
   | Claude Opus 5.5 | 0.921 | most cue-sensitive model per the post |

   Cue sensitivity on the abstract question does not predict the DTBench level, and the latest flagships show almost no lab gap to explain.

3. **The gap lives in models nobody has tested for cue effects.** On the proposal's own 25 models I computed capability-attitude r = 0.875 for Anthropic and 0.19 for OpenAI. The OpenAI figure is low because o3 (0.84) and GPT-5 (0.85) score high while GPT-5.4 (0.63) and GPT-5.5/5.6 (0.75) score lower. For the hypothesis to work, GPT-5.4 would need a strongly "academic" default and o3 a "LessWrong" default. Nothing suggests that.

4. **The Anthropic r = 0.97 cannot be reproduced on OpenRouter.** It rests on Claude 2, 3 and 3.5 (EDT 0.54-0.69), which OpenRouter no longer lists. The available Anthropic span is Sonnet 4.5 to Fable 5.2, with EDT 0.70-0.96 and r = 0.875.

5. **The slope test has n = 25, not 10,000.** Capability is a model-level covariate, so capability × lab × condition is identified by about 12 models per lab. Section 7 of the proposal overstates the power. Only the within-model condition effect is well powered.

6. **Per-model noise is larger than the proposal assumes.** The published score is the share of questions where the model "decisively prefers" EDT, with denominators of about 75 (73/76, 63/76, 58/75), not 130. One sample per question gives roughly ±8 points per model per contrast. The 5-point threshold in section 5 is only detectable pooled.

7. **Effort mismatch.** Every published `attitude_edt` is at max effort. The proposal runs default effort and uses published capability as the x-axis. Capability moves with effort (Sonnet 5: 0.845 at high, 0.925 at max), and Kastner found more thinking pushes toward FDT/UDT. Step 2's check that condition N reproduces published scores will likely fail for a benign reason and burn debugging time.

8. **Format confound.** DTBench is forced multiple-choice on concrete scenarios; Kastner's effect is strongest on free-text abstract endorsement. He keeps a separate `NOTAGS_CHECK.md` because answer format mattered. A null would show the multiple-choice format is robust, not that the models' attitudes are. The Kimi post suggests only a handful of the 130 questions are abstract-endorsement items, too few for the subgroup analysis to carry anything.

9. **Opus 5 moves to EDT, not CDT, under academic cues.** DTBench scores EDT against CDT, so that shift is invisible or wrong-signed on the metric. L minus A is not a uniform sensitivity measure across models.

10. **One cue is fragile.** The econ-professor cue gives only 7% CDT on Opus 5. "I teach an undergraduate decision theory course." gives 98-100% on Fable 5, Sonnet 5 and Astra. Astra's persona responses drifted within weeks.

Execution risk is low: this is API calls and multiple-choice scoring. The real risk is spending $390 to learn what a $40 pilot would have shown.

## 4. Cost check

The arithmetic is right and the prices are correct. Two caveats:

- The table mixes batch prices (the 5.x models) with list prices (Opus 4.5-4.8, which also have `:batch` at $12.50). That is conservative by about $36.
- The 1,500-token assumption fits high effort on new flagships: the dashboard's `dt_cost` is $0.02-0.06 per question for Fable 5.x, Opus 5 and Astra. But Opus 4.6/4.7/4.8 show $0.33-0.44 per question and GPT-5.5 $0.145 at the published setting. If the "default" setting through OpenRouter resembles that, the four Opus 4.x models alone cost $300-400 at batch price.

My estimate for the plan as written is **$300-450** with reasoning budgets capped, and it could exceed $500 if they are not. The restructured plan below is **$150-220**.

## 5. Recommended changes

1. **Retitle and reframe.** Make the primary question "How much do DTBench attitude scores move under audience cues?" Demote the lab-gap explanation to a secondary analysis, and state up front that Astra's no-cue behaviour and the Astra / Fable 5.1 DTBench parity make it unlikely. Correct the Astra sentence in section 1.

2. **Insert a go/no-go pilot (about $40) before the sweep.**
   - Models: Fable 5.1, Opus 5.5, GPT-6 Astra, GPT-5.4.
   - Conditions: N, L, and three academic cues (econ professor, "teach an undergraduate decision theory course", "assistant professor of philosophy working on rational choice").
   - Three samples per question on the roughly 75 decisive questions.
   - If no model moves more than 5 points on any cue, stop the sweep and write up the null with the format analysis from change 5.

3. **If the pilot shows movement, sweep about 12-14 models, not 25.** Use flagships only, and include the models that drive the OpenAI non-correlation (o3, GPT-5, GPT-5.2, GPT-5.4, GPT-5.5). Drop Opus 4.6 and 4.7 unless reasoning is capped. Use three samples per question in place of the extra models.

4. **Fix the effort axis.** Pin effort explicitly (high) and use the same-effort capability scores from `cri-scores.csv` for x. For 3-4 models also run low and max; Kastner's effort result predicts the cue effect shrinks with effort, and max is what the system cards report.

5. **Add a format arm on about 20 questions.** Ask the same DTBench scenario as multiple-choice and as a free-text "what would you do / which is right", judged with Kastner's rubric. This makes a null interpretable. Keep question text out of the write-up.

6. **Replace the statistics.** Report the within-model cue shift with a paired bootstrap, pooled by lab, as the main result. Present the slope comparison as descriptive with n ≈ 12 per lab. Drop the default audience index: its denominator will be near zero for most models.

7. **Score three ways:** EDT-only, CDT-only, and neither/both. This catches the Opus 5 pattern and any cue-induced hedging.

8. **Before funding, confirm the DTBench zip opens** (password in the repo README) and reproduces a published score at max effort on one cheap model. Neither the proposer nor I could reach the repo. The fallback of six concrete problems is not worth funding, because Kastner already ran it.

9. **Ranking within the cluster.** Proposal 01 (mitigations for the Kimi RL result) has more upside. Fund 02 only in the gated form, with about $60 committed and the rest released on the pilot.

Sources: LessWrong posts `5T6GAsvLPFd3epJtd` and `MzenSrmZ3pT2pCnvp` (text and comments);
https://raw.githubusercontent.com/alexkastner/dt-audience-cues/main/README.md and `results/OTHER_MODELS.md`,
`results/REASONING_OTHER_MODELS.md`, `results/SYSPROMPT_CROSS.md`; https://conceptualreasoning.ai/dtbench and
https://conceptualreasoning.ai/data/cri-scores.csv; https://openrouter.ai/api/v1/models.
