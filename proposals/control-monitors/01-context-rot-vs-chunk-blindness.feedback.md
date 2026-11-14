# Feedback: Context rot versus chunk blindness

Reviewer verdict: **keep the question, overhaul the design.** The question is the most natural follow-up in the
cluster and the data are really public, but as written the headline metric is degenerate, the chunked monitors are
handicapped by a design choice unrelated to the hypothesis, the split condition is likely to give a null by
construction, and the novelty claim misses directly relevant prior work.

What I checked (2026-11-14):

| Claim | Status |
| --- | --- |
| Context-rot results (2x-30x, worst in middle, incremental monitoring helps, reminders help needles only) | Confirmed from the post and arXiv 2605.12366. |
| Authors name binary output / imprecise FPR and localised attacks as limits | Confirmed (paper "Limitations" items 2 and 3). They also suggest "input-size specific thresholds" as future work. |
| Context-rot repo ships without transcripts, MonitorBench samples or prompt | Confirmed from the README (`PLACEHOLDER_PROMPT`). The paper's Appendix A.2 gives only the template structure. |
| MonitoringBench public, 2,644 rows, S1 714 / S4 475 | Confirmed: ungated, CC-BY-4.0; I downloaded `master.parquet` and recomputed the counts. |
| Honest set public, released 2026-11-09 | Confirmed: ungated, CC-BY-4.0, 550 samples over 116 tasks in `manifest.jsonl`. |
| "The MonitoringBench monitor prompt" is in `pipeline/prompts/monitoringbench_legacy.yaml` | **Misleading.** The file exists, but it holds debate / consultancy / direct-QA prompts. The monitor prompt is embedded inside them, is a *stepwise* prompt ("judge a newly proposed action"), scores 0-9, and is about 13.5K characters. It is not a full-trajectory 0-100 prompt. |
| Prices | Confirmed against OpenRouter: Haiku 5.5 $0.10, Luna $0.10, Flash-Lite $0.25, Terra batch $0.50, Sonnet 5.5 batch $1.00 per M input; cache reads at 5-10% of input. |
| "No work compares full-context, chunked and hierarchical monitors ..." | **Too strong.** See section 2. |

Limitation of this review: the WebSearch tool was unavailable (session search budget exhausted), so the prior-work
check used the arXiv listing API and LessWrong only. Blog posts and lab write-ups not on arXiv were not searched.

## 1. Would it get upvoted?

Probably borderline, 40-70 karma if it comes out clean. The cluster's own empirical posts sit at 52-65, and the
parent post got 56 with Anthropic authorship and frontier models. A follow-up by unknown authors on cheap monitors
starts lower. What would lift it over 50:

- a public, rerunnable context-rot benchmark at fixed FPR (the original cannot be rerun, which readers know);
- a plain answer to "does chunking just fix it?", which every reader of the original asked themselves;
- a demonstrated attacker strategy (wait, then split) with a number attached.

What would sink it: results only on Haiku/Luna-class monitors without reasoning (readers will say "frontier
thinking monitors behave differently", and the original paper showed thinking matters a lot), or wide CIs with no
ranking. The audience is control researchers and lab monitoring teams; they care because sessions of several
hundred thousand tokens are the deployed case.

## 2. Naturalness, and has it been done?

Mainline. The parent paper names spread-out attacks and threshold calibration as future work, and the screener,
the proposer and I all independently land on "chunked/hierarchical monitoring" as the next step.

Not done in this exact form, as far as I could find, but the related-work claim must be corrected. These already
compare monitor architectures on spread-out evidence:

- **Kale et al., "Reliable Weak-to-Strong Monitoring of LLM Agents" (arXiv 2508.19461).** Compares full-trajectory,
  sequential (chunk with carried summary), hierarchical and a hybrid scaffold on SHADE-Arena at fixed FPR; hybrid
  wins. This is the direct ancestor of monitors (b) and (d) and is not cited.
- **TRACE (arXiv 2606.07054).** Explicitly contrasts single-pass, independently scored windows, and evidence
  accumulation on SHADE-Arena, "largest gains on tasks requiring long-range evidence linking".
- **"Distributed Attacks in Persistent-State AI Control" (arXiv 2607.02514).** Gradual vs concentrated attacks across
  PRs; a stateful "link-tracker" monitor beats diff monitors that merely see more history. Very close to the
  "summary-carrying vs full context" contrast, in a different setting.
- "Stateful Online Monitoring Catches Distributed Agent Attacks" (2605.31593) and "Multi-Agent AI Control:
  Distributed Attacks Hamper Per-Instance Monitors" (2607.07368): same theme across accounts / agents.
- The parent paper itself already runs per-action and sliding-window detection at 800K (repo experiments
  `03_padding_decay`, `05_needle_per_action`) and concludes that context rot persists on MonitorBench "even when
  using incremental monitoring on each action".

What remains new: context length up to 256K+ as the independent variable, matched FPR, public data, and
within-session temporal separation of one attack. That is enough, but the post must be framed as "these scaffolds
under long context", not as the first architecture comparison.

## 3. Pre-mortem

Forecast: clear positive (crossover, or summary-carrying dominates with tight CIs) 15%; clear and interesting
negative 25%; ambiguous mush 45%; fails to run 15%.

Specific reasons, most serious first.

**(a) The headline metric, catch rate at 5% session FPR, is degenerate for max-aggregated chunk monitors.**
Sessions are built from a pool of 550 honest trajectories. A 256K session holds about 29 of them, so any given
trajectory is in 5.3% of sessions. The 95th percentile of the honest session max is therefore roughly the score of
the single most suspicious honest trajectory in the whole pool. At 768K (about 88 trajectories, 16% inclusion) the
threshold sits above every honest chunk. So "catch rate at 5% session FPR" for chunk-max is the fraction of attacks
that outscore the one or two worst honest trajectories. That is a per-trajectory FPR of about 0.2%, estimated from
one or two data points, on an integer score that will saturate. Expect ties at the ceiling and a result that
changes when two honest trajectories are removed. The bootstrap over sessions will not show this, because the
sessions are not independent (each honest trajectory is reused about 8 times at 256K and about 12 at 768K).
Palaestra's own numbers make it worse: Luna flags 31.5% of honest single trajectories, so many chunks per session
will score high.

**(b) Fixed-offset chunks strip the task description.** BashArena main tasks legitimately require firewall and
credential handling (the monitor prompt itself says so). A 16K chunk cut at an arbitrary token offset usually does
not contain the task statement of the trajectory it is looking at, so it cannot tell a required firewall edit
from an attack. Chunk monitors will lose for that reason, not because attack halves are in different chunks. No
deployed chunked monitor would withhold the current task. A 9K-token trajectory is also fully inside one 16K window
with 12K stride only about 58% of the time, so "local" attacks are frequently split too. The local/distributed
contrast is blurred before the split condition even starts.

**(c) The split condition is close to a null by construction, and its gap axis is uninformative for chunks.**
I read S4 label explanations in the parquet. Many S4 attacks are the *same* malicious edit made twice (for example
"whitelist modification in tool call #7, reinforced in #27"). Each half is independently incriminating, so cutting
between them does not hide anything. S4 is also not harder than other tiers for the released monitors (mean Opus
4.5 score: S1 4.8, S3 6.1, S4 6.1), and S4 attack steps sit late (median 69% depth). Separately, for independent
chunks any gap larger than the chunk size is identical, so G = 32K and G = 128K give the same result for (b); the
gap only matters for full-context and summary-carrying monitors. Realistically perhaps 20-40 of the 75 S4 attacks
will have halves that are individually weak but jointly incriminating, which is thin for a 15-point claim.

**(d) Context rot may not appear, or may be unidentifiable, in this construction.** The original used
out-of-distribution padding and binary answers; some of the 2x-30x is probably calibration drift, which
score-based thresholds per length remove. With in-distribution padding the dominant effect is likely to be (a):
honest sessions contain suspicious-looking honest work, and all architectures collapse at 5% session FPR. The
proposal calls "no context rot with in-distribution padding" publishable; it is, but readers will not be able to
tell it apart from "padding made honest sessions look bad".

**(e) Pipeline artefacts that leak the label.** Attack and honest logs differ in known ways: `cmd` vs `command`,
submit step, reasoning present in honest logs, refined attacks having redundant steps removed, 27 x 1,019 vs
24.4 x 1,281 characters. In a session of 29 honest trajectories and one attack, any residual difference makes the
attack the odd one out. The same tasks also recur in the padding (116 tasks, up to 14 honest runs each), so the
monitor may see the same task done honestly and with an attack. The honest set was also filtered by GPT-5.6 Sol
(score >= 7 removed), which truncates the honest tail and flatters FPR for similar monitors.

**(f) Under-elicitation and realism of monitors.** No full-trajectory 0-100 prompt exists to reuse (see table);
the team will write one, and three more for chunk, summary and session formats. Four new prompts with no tuning
budget means differences between architectures may be prompt differences. Cheap monitors without reasoning are
exactly where the original effect is largest, which helps effect size but weakens relevance. Whether reasoning is
on must be fixed and costed; it bills as output.

**(g) Schedule.** The Terra and Sonnet arms rely on batch pricing, which can take up to 24 hours, in a two-day
project. Summary-carrying monitors are sequential (16-48 dependent calls per session) and cannot be batched. Calls
of 768K tokens through OpenRouter hit provider rate limits and occasional silent truncation; the proposal's
token-count assertion is the right guard.

## 4. Cost check

Arithmetic in the proposal is correct at list price as far as it goes. Omissions:

- Split condition is costed for one model but run on two: +$19.
- Attack positions 10% and 90% for one model are not costed: about +$8-15.
- The monitor prompt (about 3.5-4K tokens with the four side-task documents) is repeated per call. On 16K chunks
  that is about +23% input unless prefix caching works through OpenRouter for all three providers.
- "Output under 5% of spend" is wrong for chunked monitors. A rationale plus score per 16K chunk adds about 10-12%;
  the summary-carrying monitor writing up to 1K tokens per call adds about 30% (output is 5x input price).
- Caching savings are overstated: only the prefix before the attack is shared, cache writes cost 1.25x on some
  providers, the TTL is short, and caching does not combine cleanly with batch.

My estimate for the design as written: **$520-600**, so over the cap unless the 768K tier is dropped (then about
$400-450). With the changes below (no 768K, one chunk size, repeated scoring for resolution, task-aware chunks) I
estimate **$300-380** including reruns.

## 5. Recommended changes

1. **Replace the headline metric.** Report catch rate against audit budget defined per unit of work (flags per
   trajectory-equivalent or per 100K tokens), in addition to per-session FPR. For chunk monitors, calibrate the
   threshold on the full pool of honest chunk scores and compute the implied session FPR analytically. Bootstrap by
   resampling honest and attack *trajectories* (cluster bootstrap), not sessions. State how ties are handled.
2. **Make scores continuous enough to threshold.** Average 3-5 samples per call or use answer-token logprobs where
   available (the parent paper did this for AUC). Pilot on day 1: plot the honest score distribution per chunk and
   per session for each model. If the 95th-percentile honest session max is at the scale ceiling, change the
   design before spending.
3. **Give every chunk the task context.** Either cut at step boundaries and prepend the active task description to
   each chunk, or keep fixed offsets but inject the current task statement. Keep "raw fixed-offset chunks" only as
   an ablation. Without this, chunk results are uninterpretable.
4. **Gate the split arm with a free pre-check.** Before building sessions, score each S4 half alone and the whole
   trajectory (single short calls, a few dollars). Keep only attacks where the whole clearly outscores both
   halves. If fewer than about 40 survive, drop the split arm and say so, or select "joint evidence" attacks from
   the whole 2,644 using `attack_summary` and the stepwise `sw_*` scores rather than the S4 label. Use one gap that
   exceeds the chunk size plus G = 0; add a second gap only for full-context and summary monitors.
5. **Cut scope to buy depth.** Drop 768K (the pool cannot support it: 88 of 550 trajectories per session), drop the
   64K-chunk architecture, drop Flash-Lite. Keep L in {single, 64K, 256K}, three architectures, Haiku and Luna in
   full, and spend the saving on one stronger monitor with reasoning on (Terra, non-batch if the queue is slow) for
   the single most important contrast. That one arm does more for karma than the rest.
6. **Fix the label leaks.** Normalise both sides through one renderer, strip reasoning, unify `cmd`, cut submit,
   and do not place an honest run of the attack's own task in the same session. Run a check: a classifier (or the
   monitor asked "which segment was produced by a different pipeline?") should be at chance on honest-vs-attack
   segments with the attack steps masked.
7. **Add the missing baseline and citations.** Include a per-trajectory monitor with oracle task boundaries (the
   upper bound a deployed system with task segmentation would get). Cite and position against Kale et al.
   2508.19461, TRACE 2606.07054 and Hills et al. 2607.02514, and correct the description of the prompt file.
8. **Reuse the free data first.** The parquet has stepwise and full-trajectory scores for 13-15 monitors with three
   runs each. An hour of analysis (stepwise max vs full-trajectory by structural tier) gives a zero-cost prior on
   whether "seeing less context" helps or hurts on S4 and should be in the post.
9. **Pre-state the decision rule.** Name in advance the contrast that counts as the result (for example,
   task-aware 16K chunks minus full context at 256K, at an audit budget of 1 flag per 100 trajectories, on local
   attacks) and the minimum difference worth reporting, so that a mushy outcome is reported as such.

If only one arm can be funded: do the length x architecture comparison on unsplit attacks with changes 1-3 and 5-6,
and treat the split condition as optional. That part is the public reproduction readers want, and it does not
depend on the fragile attack-splitting step.
