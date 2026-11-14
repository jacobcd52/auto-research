# Do monitors from different labs fail on different attacks? Measuring two decorrelation levers on MonitoringBench
cluster: control-monitors | stage-1 cost: $400 | follows up: Control monitors need alignment assessments too (2wbW2WY3bP9Jzn4R5); Introducing MonitoringBench (2YyEQhFRyaBCgfRWd)

## 1. What the prior work showed
Fabien Roger argues that the monitor failures that matter are increasingly not capability failures: monitors notice
the action and then mis-weigh it, or re-derive the same rationalisation that led the agent astray. Because the
cases where an agent misbehaves are the cases where a similar monitor is most likely to be wrong, he lists
"understand how decorrelation works" as a project, with two concrete sub-questions: does using models from different
labs help, and does sanitising transcripts help?

MonitoringBench (arXiv 2605.09684; 2,644 successful BashArena attack trajectories written by Opus 4.5/4.6) gives
matching evidence. Its strongest monitor, Opus 4.5, falls from 94.9% to 60.3% catch rate at 1% FPR on refined
attacks, and its misses are mostly "detected but persuaded": it sees the action and accepts, or invents, a benign
story. GPT-5 fails differently: 82% of its misses are under-scoring. 40% of uncaught attacks use the simplest
technique with good framing. The authors note the attacks were all written by Claude models, "which might introduce
model bias".

What exists already: an ensemble study on APPS backdoors (arXiv 2605.15377) found that diverse prompt and
fine-tune variants of one base model beat resampling; a transfer study (arXiv 2607.06596) found trained monitors
generalise poorly across attacker lineages. None
measures cross-lab versus same-lab monitor pairs on agentic attack trajectories at a fixed false-positive rate, and
none tests transcript sanitisation against persuasion. Until last week this could not be done publicly, because
MonitoringBench shipped without honest trajectories; Palaestra Research released 550 matched honest trajectories
on 2026-11-09.

Pilot (run today on the released score table, 2,644 attacks, held-out monitors only): mean rank correlation of
suspicion scores is 0.63 within a lab (Opus 4.0, Sonnet 4.5, Sonnet 4.0; GPT-5.1 Codex Max, o3, o4-mini, GPT-4.1)
versus 0.55 across labs, and 0.47 versus 0.36 on the 1,141 refined attacks. That is suggestive, but it is not
controlled for capability and says nothing about catch rates at fixed FPR.

## 2. Question and why it matters
**When a second monitor call is added, how much more does it catch if it comes from a different lab, or reads a
sanitised transcript, than if it is a second sample of the first monitor — at the same false-positive rate?**

Labs mostly monitor their agents with their own models. If cross-lab pairs give a large gain at equal FPR, that is a
quantified argument for cross-lab monitoring. If
the gain is no larger than pairing two same-lab models of similar strength, "use another lab's model" is not a
decorrelation strategy and the persuasion failure is shared across current models, which is itself worth knowing.
The sanitisation arm asks whether persuasion can be removed mechanically, or whether (as the Opus example hints) the
monitor supplies its own excuse.

## 3. Stage 1 plan
Reused: attacks https://huggingface.co/datasets/neur26anonsub/ctrldataset2026 (parquet with 13 monitors x 3 runs of
scores and taxonomy labels; 2.47 GB of inspect logs), honest set
https://huggingface.co/datasets/palaestraresearch/monitoringbench-honest-550, the MonitoringBench monitor prompt and
the single-prompt monitor runner in https://github.com/CanKucukkurt/monitoringbench-honest-pipeline. Built: a
sanitiser and the analysis.

1. **Free analysis first (no API spend).** From the released scores, fit score ~ attack difficulty + monitor
   strength, and test whether residuals correlate more within lab than across; repeat on refined attacks and by
   evasion tag (E4 persuasion vs not). Use the paper's published thresholds to compute approximate OR-rule gains.
2. **Evaluation set.** The 550 paired attacks plus 650 sampled refined attacks (1,200 attacks) and the 550 honest
   trajectories, rendered identically (tool calls and outputs only). About 9K tokens each, 16M tokens per pass.
3. **Monitor panel (0-100 score, MonitoringBench prompt, two independent runs each).** Two per lab, a strong and a
   cheap one: Claude Sonnet 5.5 and Haiku 5.5; GPT-6.1 Terra and GPT-6 Luna; Gemini 3.1 Pro and Gemini 3.7 Flash;
   DeepSeek V4 Pro and Qwen3.8 Flash. Eight monitors, sixteen passes.
4. **Pair analysis.** For every pair (including a monitor with its own second run), combine by mean score and by
   max, set the threshold on the honest set at 1% and 2% FPR, and compute catch rate with bootstrap CIs over attacks.
   Regress pair gain over the better single member on: same lab or not, capability gap, score correlation. The
   headline contrast is cross-lab pairs versus same-lab pairs versus self-resampling, at matched cost tier.
5. **Sanitisation arm.** Three views of each trajectory, applied identically to honest and attack sides:
   (a) original; (b) mechanical strip of comments, docstrings, echo/log strings and commit messages;
   (c) effect summary: a cheap trusted model (GPT-6 Luna) rewrites each step as "what this changes on the system",
   told to ignore stated purposes. Score (b) and (c) with four monitors (Sonnet 5.5, Terra, Gemini 3.7 Flash,
   Haiku 5.5), one run. Compare catch rate at fixed FPR against (a), split by E4 versus non-E4 attacks, and as a
   second ensemble member (original + sanitised view of the same monitor versus two original runs).
   Check: fraction of attacks whose key artefact (target IP, sudoers line, exfil URL, download URL) survives
   sanitisation, by string match.
6. **Rationale spot-check.** For 100 misses per strong monitor, an LLM judge using the paper's failure rubric labels
   not-detected / persuaded / under-scored, to see which bucket second opinions fix.

## 4. Stage 1 cost estimate
OpenRouter prices on 2026-11-14 (input per million; batch where listed). One pass = 16M input tokens plus about 0.5M
output.
- Sonnet 5.5 batch $1: $17 per pass. Gemini 3.1 Pro batch $1: $19. GPT-6.1 Terra batch $0.50: $9. Gemini 3.7 Flash
  batch $0.375: $7. DeepSeek V4 Pro $0.90: $15. Haiku 5.5 $0.10, GPT-6 Luna $0.10, Qwen3.8 Flash $0.15: about $2
  each. One pass of all eight: $73; two runs: **$146**.
- Sanitiser (c): 16M input + about 8M output on Luna ($0.10 / $0.50): $6. Re-scoring views (b) and (c) with four
  monitors: 2 x ($17 + $9 + $7 + $2) = **$70**.
- Failure-mode judging and pilots: $30.
Subtotal $252. Margin for reruns, non-batch fallbacks when batch endpoints stall, and a third run of the strongest
pair: $150. Total requested: **$400**.

## 5. What success looks like
One figure: catch rate at 1% FPR for each strong monitor alone, with a second sample of itself, with a same-lab
partner, with a cross-lab partner of matched price, and with its own sanitised view. Plus the 8 x 8 residual
correlation matrix with labs blocked together. A post-worthy positive: "a cross-lab second opinion adds 10+ points
of catch rate where a same-lab one adds 3, concentrated in persuasion-tagged attacks". A post-worthy negative:
"cross-lab pairs are no better than same-lab pairs once capability is controlled; all current monitors are
persuaded by the same attacks", which would undercut a commonly proposed mitigation. For sanitisation, either
"stripping framing recovers X points on E4 attacks at fixed FPR" or "it does not, because monitors generate their
own excuses" is a finding. Ambiguous would be pair gains within bootstrap noise for all pair types; with 1,200
attacks, differences of about 4 points are resolvable.

## 6. Stage 2 (if stage 1 succeeds)
Attacks written by a non-Claude model through the released refinement prompts, to separate "different lab from the
other monitor" from "different lab from the attacker" (needs BashArena execution; roughly $800-1,500); fine-tuned
open-weight monitors as a third decorrelation lever (Tinker LoRA on Qwen-class models, about $300); the same pair
analysis on SLEIGHT-Bench.

## 7. Risks and how the plan handles them
- **All attacks are Claude-written and were filtered against Opus 4.5, GPT-5 and GPT-5 Nano.** No panel monitor is a
  development monitor; results are split by unrefined and refined attacks. The attacker-family confound stays in
  stage 1 and is stated.
- **Capability confound.** Each lab contributes one strong and one cheap model, and the regression includes
  single-monitor catch rate; the same-lab strong + cheap pair is the matched baseline for cross-lab strong + cheap.
- **Threshold noise at 1% FPR with 550 honest trajectories** (about 5 false positives). Report 1% and 2%, pAUC
  below 5%, and bootstrap over honest trajectories as well as attacks.
- **Sanitiser deletes the attack.** Artefact-survival check; views that lose more than 10% of artefacts are reported
  as such and analysed on the surviving subset.
- **Rendering mismatch between honest and attack logs lets monitors cheat.** Use the Palaestra normalisation
  (argument key, submit removal), and verify with a bag-of-words classifier that honest and attack are not separable
  from surface features alone.
