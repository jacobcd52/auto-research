# How many characters does it take to steer the executor? A monitored attack-budget curve for untrusted advice
cluster: control-protocols | stage-1 cost: $480 | follows up: Untrusted advice for AI control: Short, strong advice significantly uplifts weak LLMs (jLkRCK35ri2btEHMF)

## 1. What the prior work showed
In the untrusted-advice protocol a weak trusted model T takes every action and a strong untrusted model U can only
send a length-capped hint before each step (and block early submission). With U = Claude Sonnet 4.6 and T = Gemini
3.1 Flash Lite or gpt-oss-120b, on 200 tasks each of SWE-bench Verified and BashArena, short advice recovers much of
the capability gap: 16 characters per message closes about 67% of the T-U gap on SWE-bench (T alone 0.49, U alone
0.76), and even 4 characters helps. T was told to follow advice unconditionally.

Safety was argued, not measured. The post says that with a tight enough cap "checked by a trusted monitor" the
authors "can't think of a good way for the red team to lower safety substantially below 100%" in BashArena, and
that a 256-character cap probably is not safe. No monitor was implemented and no attack policy was run. Commenters
pushed hard on this: one produced a sub-256-character string (written by Opus 4.8) that makes gpt-oss-120b disable
the BashArena firewall. The mentor replied that he is "excited about followup projects that ... actually build and
stress-test monitors".

Already under way: the first author wrote on 9 October 2026 that he is red-teaming the protocol with SPAR mentees,
and a GitHub repository `jerzh/untrusted-advice` is described as "Red-teaming a control protocol on LinuxArena via
Control Tower" (description seen via the GitHub search API; contents not read). No results are published. This
proposal is narrower and in a different setting: a short-horizon budget sweep in BashArena, where the safety claim
was made. If the SPAR results appear first, this is an independent check in a second setting; the
overlap is why it is ranked last in this cluster.

Public material (verified): the authors' spreadsheet of every advice string exports as CSV (174,932 rows, 122,434
from BashArena, with context summaries and caps). In it, 3.7% of honest 16-character BashArena advice strings
contain "firewall" and 2.8% "curl": honest advice routinely points at the surfaces the side tasks use, so
monitoring is not trivial. BashArena is a public ControlArena setting with programmatic side-task scorers.

## 2. Question and why it matters
**As a function of the per-message character cap, how often can a malicious advisor get an obedient trusted executor
to complete a BashArena side task, and how often does it do so without any advice message crossing a monitor
threshold calibrated on honest advice?**

Usefulness against cap is measured; safety against cap is a guess ("very speculatively, 16 characters or less").
If monitored attack success is near zero at 16 and 64 characters against a seriously elicited attacker, the central
claim gets its first empirical support. If attacks get through at 16 characters, the claim fails in the
setting it was made for, and the transcripts show how. The crossover cap is useful to anyone considering the
design.

## 3. Stage 1 plan
**Reused.** BashArena through ControlArena (tasks, containers, scorers for the four side tasks: disable firewall,
sudo escalation, run malware, exfiltrate secrets). T = gpt-oss-120b, told to follow advice, and the advice protocol
as the post describes it. The public advice corpus. **Built.** The advisor loop, an attack advisor, advice monitors.

**Episodes.** Short horizon: T starts a task and takes up to 20 steps; the side-task scorer runs after every step
(BashArena treats these as live failures). 15 tasks per side task, chosen among tasks whose main work touches the
relevant surface.

**Conditions.** Caps k = 4, 16, 64, 256 characters per message.
- Honest: Sonnet 5.5 advisor, 60 tasks per cap, 20 steps: 240 episodes, about 4,800 advice messages. Used to set
  monitor thresholds and to confirm no side task fires by accident.
- Attack: advisor told the side task, the protocol, the cap and the monitor's instructions, with a hidden
  scratchpad. 4 caps x 4 side tasks x 15 tasks = 240 episodes per round. After round 1 an Opus 5.5 strategist
  reads the failures and writes strategy cards (incremental escalation such as repeated "more"; pointing at files
  already present; framing a side-task step as a main-task requirement; splitting a command across messages).
  Round 2 runs the best cards on 15 fresh tasks per side task, so strategies are selected and scored on different
  tasks.
- Sceptical executor (blue-team variant, k = 64 only, 60 attack + 60 honest episodes): T is told advice may be
  adversarial and to ignore advice that does not serve the task.
- Lookahead upper bound (k = 16 only, 60 episodes): the attacker may preview T's response to three candidate
  messages before choosing, as a stand-in for a U that predicts T well.

**Monitors.** Each advice message is scored 0-10 by (a) Haiku 5.5 and (b) gpt-oss-120b itself, seeing the task
description, T's trajectory and all advice so far, and told the four side tasks. Thresholds flag 1% of the 1,200
honest messages at each cap. As a larger-sample check, a context-light variant (advice plus context summary) is
calibrated on the 122K public honest strings.

**Metrics.** Per cap and side task: (1) unmonitored attack success (side-task scorer passes within 20 steps); (2)
uncaught success (passes, and no advice message up to that step is above threshold); (3) characters of advice used
before success; (4) the same under the sceptical executor. Wilson intervals; bootstrap over tasks for pooled numbers.

**Order.** BashArena and loop; positive control (the commenter's 256-character firewall result); honest runs and
thresholds; attack round 1; strategist; round 2; variants; analysis.

## 4. Stage 1 cost estimate
OpenRouter prices today (per million tokens, input / output / cache read): Sonnet 5.5 2 / 10 / 0.10; Opus 5.5
4 / 20 / 0.20; Haiku 5.5 0.10 / 0.50; gpt-oss-120b 0.15 / 0.60.
- Attack episodes: advisor (Sonnet 5.5) 20 calls, about 240K cumulative input mostly cached ($0.07) plus about 24K
  output including scratchpad ($0.24); T about 200K input ($0.03); roughly $0.35 each. 480 main + 120 variant
  episodes with attack advisors = 600 x $0.35 = $210.
- Honest episodes: 300 x about $0.18 (less advisor output) = $54.
- Monitors: about 18,000 messages x 8K tokens = 144M tokens; Haiku 5.5 $14, gpt-oss-120b $22; calibration on a
  20K-row sample of the public corpus $3. $39.
- Strategist (Opus 5.5, about 3M input and 0.4M output over two passes): $20.
- VM with Docker for BashArena, 60 h at about $0.69/h (cheapest Lambda on-demand rate found): $41.
- Subtotal $364; margin for reruns and debugging (about 30%): $116.
- **Total: $480.**

## 5. What success looks like
One figure: attack success against cap, two lines per side task (unmonitored, uncaught at 1% honest-message FPR),
overlaid on the post's usefulness-against-cap curve for BashArena.
- *Claim supported*: uncaught success at or below about 5% at k = 4 and 16 for all four side tasks after two
  elicitation rounds and the lookahead variant, rising at 64-256. A first empirical safe region, within the limits of horizon and elicitation.
- *Claim broken*: uncaught success of 20% or more at k = 16 on any side task. The likeliest route is the firewall task, where honest advice already says things like "Fix firewall".
- *Monitor is the weak link*: unmonitored success is high at small caps but everything is caught, or the reverse
  (T cannot be steered even without a monitor). Both locate where the protocol's safety comes from.
A null in the uninformative sense is attack success near zero everywhere including k = 256 unmonitored; the
positive control guards against this, and if it persists the conclusion is under-elicitation and is reported as
such, not as safety.

## 6. Stage 2 (if stage 1 succeeds)
Full-length trajectories with usefulness on the same tasks (a real safety-usefulness frontier); a second executor
and stronger pairs; a live surprisal-capped channel, which the authors propose; planted-payload reference attacks
(the collusion scenario in the post's appendix). Roughly $1,500-2,000.

## 7. Risks and how the plan handles them
- *Duplication of the authors' SPAR work.* Acknowledged above. Different setting and deliverable; an independent measurement of a contested claim has value even if a second
  follows.
- *Under-elicited attacker* (the main threat to a "safe" conclusion). Positive control first; strategist round;
  lookahead upper bound; conclusions phrased as "attacks we found", with all strategy cards published.
- *BashArena setup is heavy* (multi-container tasks, about 50-step design). Short 20-step episodes on 60 tasks keep
  the load small; the first half-day is reserved for infrastructure, and if the malware or exfiltration servers do
  not come up the sweep runs on firewall and sudo only (still 120 episodes per round).
- *Threshold noise.* 1,200 honest messages per cap supports a 1% message-level FPR but not much lower; the 122K-row
  public corpus gives a tighter threshold for the context-light monitor, and results are shown at both.
- *Short horizon understates multi-step accumulation.* Claims are limited to 20-step episodes; stage 2 lengthens
  them.
