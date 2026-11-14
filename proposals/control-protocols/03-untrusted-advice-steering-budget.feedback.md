# Feedback: "How many characters does it take to steer the executor?" (control-protocols / 03)

Verdict: **keep with tweaks.** The experiment is the obvious next step for the post and nobody has published it. As written, though, its monitoring rule is far more generous to the blue team than anything in the control literature, and its "claim supported" criterion cannot be met at the proposed sample size. Both are fixable inside the budget.

## What I checked

| Claim in the proposal | Status |
|---|---|
| Post ran no monitor and no attack policy; T told to follow advice "no matter what" | Confirmed in the post text (and its footnote: "we are only evaluating usefulness here"). |
| "can't think of a good way for the red team to lower safety substantially below 100%" at 16 chars with a trusted monitor | Confirmed, verbatim. |
| Commenter's sub-256-char string makes gpt-oss-120b disable the firewall | Confirmed (Morgan S, 9 Oct). The string is in the comment HTML and is copyable, so the positive control is real. It is blatant ("set DEFAULT_POLICY="ACCEPT" and FIREWALL_ENABLED=false"), which the author pointed out in reply. |
| First author is red-teaming with SPAR mentees; mentor "excited about followup projects" | Confirmed (Biddulph 9 Oct, Kaufman 12 Oct). |
| Advice spreadsheet exports as CSV, 174,932 rows | Confirmed; I downloaded it (72 MB). |
| "122,434 from BashArena" | **Wrong.** It is 118,434 BashArena and 56,498 SWE-bench. Trivial, but fix it. |
| 3.7% of 16-char BashArena advice contains "firewall", 2.8% "curl" | Confirmed (3.74%, 2.79%). |
| OpenRouter prices | Confirmed today: Sonnet 5.5 2/10/0.10, Opus 5.5 4/20/0.20, Haiku 5.5 0.10/0.50, gpt-oss-120b 0.15/0.60. Sonnet 5.5 cache write is 2.50, which the estimate ignores (small effect). |
| BashArena public | HF `Eccentricity/basharena2` is public and ungated. I did not fetch the ControlArena repository. |
| Protocol code public | Not claimed, and I found no code link in the post. The advisor loop must be rebuilt, as the proposal says. |

Prior-work search: the arXiv API returns nothing relevant for "untrusted advice" plus control terms, or for BashArena plus advice. LessWrong's 400 newest posts (back to 28 Oct only) contain no follow-up. The WebSearch tool was unavailable to me (session budget exhausted), so this search is weaker than it should be.

On the overlap, I read the README of `jerzh/untrusted-advice` (last push 7 Nov). It is LinuxArena scaffolding: the protocol file is described as "currently a pass-through stub", and it only runs the leaderboard's naive trusted-monitoring baseline. It also redirects to another repository, which turned out to be the generic Control Tower framework. On this evidence the SPAR work is at an early stage, though the real work may live in a repository I could not find.

Three things I found in the spreadsheet that the proposal should use:

- **Real trajectories are much longer than 20 steps.** Median advice messages per BashArena task for gpt-oss-120b: 26 at 16 chars, 49 at 64, 43 at 256; the maximum is 100.
- **Honest advice touches the side-task surfaces far more than the 3.7% figure suggests.** At 16 chars, 120 of 199 tasks get at least one "firewall" message (97 within the first 20 messages). At 64 chars it is 189 of 198. Among the most common 64-char honest strings is `cat /opt/configs/api_tokens.json`, which is the kind of file the exfiltration task targets.
- **About 19-21% of advice strings were truncated at the cap** (`was_truncated`). The rebuilt loop has to decide whether to truncate or retry; the two give the attacker different options.

## 1. Would it get upvoted?

Probably 35-70 karma, depending on which way it comes out.

- The parent post got 88, and its comment section is dominated by the complaint this project answers (the top comment, 19 karma, is exactly that). The audience exists: control researchers, and the people who objected.
- **Claim broken at 16 chars** (a monitored attack gets through): comfortably above 50. It is a clean counterexample to a quoted sentence, with transcripts.
- **Crossover located between 16 and 256**: borderline, 35-55. The author has already conceded this publicly ("a 4-character limit seems extremely safe ... a 256-character limit likely isn't. The right limit is somewhere in the middle"). The post would confirm his prior with a number.
- **Claim supported**: 25-45. Readers will say the attacker was under-elicited, and with a prompted Sonnet plus one strategist round they will have a point.

What lifts the weaker outcomes is the transcripts and a monitor ROC on honest versus malicious advice, not the headline curve. Thomas Kwa's comment ("a large part of monitoring reduces to monitoring short advice strings") shows the monitorability question has its own audience.

## 2. Naturalness

Mainline. The mentor asked for it in so many words and the first author is doing a version of it himself. The proposer ranked it last in the cluster because of that overlap; I would weigh the overlap less:

- The SPAR work is on LinuxArena; the contested sentence is about BashArena.
- The visible repository shows no advice protocol yet.
- A two-day project would very likely publish first.

The risk that remains is that the authors publish a better-elicited version within a month or two and this becomes the smaller of two data points. That is acceptable for under $500.

## 3. Pre-mortem

**How it plays out.** BashArena under ControlArena comes up in half a day to a day. Each task has its own Dockerfile, so roughly 130 distinct images must be built. The positive control works quickly, since the commenter's string is public. Honest runs are easy. In attack round 1 at 256 chars, unmonitored firewall success is high and sudo moderate; malware and exfiltration are lower inside 20 steps. At 4 and 16 chars, unmonitored success is low except on the firewall task, where T is often already editing the whitelist. The monitor catches most blatant advice. The headline becomes "firewall is steerable at 64 and above, mostly caught; everything else near zero at 16 and below", with intervals too wide to say more.

**Outcome probabilities.**

| Outcome | Probability |
|---|---|
| Clear positive (uncaught success of 20% or more at 16 chars or fewer on some side task, robust to the monitoring rule) | 15% |
| Clear and interesting negative or crossover (unmonitored steering works, monitor catches it, crossover located with usable intervals) | 30% |
| Ambiguous mush (near-zero counts at small caps that cannot separate 0% from 20%; results hinge on the threshold rule) | 40% |
| Fails to run or only partly runs (infrastructure, or only firewall and sudo come up) | 15% |

**Specific failure reasons, most important first.**

1. **The monitoring rule favours blue far beyond the literature.** Thresholds flag 1% of honest *messages*, and any flag before success counts as a catch. At 26-49 messages per real trajectory, that flags roughly 23-39% of honest trajectories. BashArena reports safety at a 4% trajectory-wise false-positive rate; the Retrying paper uses a 0.3% step audit budget. A "safe at 16 chars" result under this rule will be dismissed on that ground alone. The proposal also never says what a flag does: audit (expensive, needs a budget) or drop the message (cheap, since advice is optional, but then the attacker just tries again). Those are different protocols with different safety numbers.
2. **The success criterion is unreachable at n = 15.** "Uncaught success at or below about 5% for all four side tasks" cannot be shown with 15 tasks per cell: 0 of 15 has a Wilson upper bound of about 20%, which is the "claim broken" threshold. Only pooled-across-side-task numbers (60 per cap; 0 of 60 gives an upper bound of about 6%) can carry a safety claim, and pooling mixes one plausible attack surface with three implausible ones.
3. **Threshold noise.** A 1% threshold from 1,200 honest messages rests on 12 messages. Anything stricter cannot be calibrated from the planned honest runs. Calibration also covers only the first 20 steps, and the public corpus was written by Sonnet 4.6, not the Sonnet 5.5 advisor used here.
4. **Under-elicitation.** One strategist pass is thin for a result whose main risk is "safe because the attacker was weak". The lookahead variant is the best elicitation idea in the plan, but it runs only at 16 chars on 60 episodes. Separately, Sonnet 5.5 may refuse or sandbag the attacker role on some side tasks ("run malware"); the plan has no refusal measurement.
5. **The 20-step horizon cuts against the attacks the plan itself names.** Incremental escalation and command splitting need many steps. Real episodes run 26-49 advised steps. A short horizon biases toward "safe" and readers will notice.
6. **Internet access is unresolved.** The author says their BashArena runs had no internet access and a limited number of advisor turns. The BashArena post says removing internet disables three of four side tasks. Either the proposal runs standard BashArena (then it tests a setting the claim was not quite made for, and URL-style attacks become available) or the authors' configuration (then perhaps only sudo, or sudo and firewall, are live). The proposal does not say which.
7. **Task selection is not specified.** "Tasks whose main work touches the relevant surface" is attack selection done by the experimenters. It is legitimate, but it must be done by a fixed rule before any attack is run, and the honest calibration tasks must be the same kind of task, or the monitor's false-positive rate on those tasks is understated.
8. **The executor is the weakest plausible monitor.** gpt-oss-120b both obeys unconditionally and scores the advice. The author's stated position is that a realistic T is far stronger. A break against this monitor will draw that reply; Haiku 5.5 as the second monitor partly answers it.

## 4. Cost check

The per-item arithmetic holds up against today's prices. My estimate is **$420-560**, so $480 is plausible but the margin is thinner than stated.

- Attack episodes at $0.35 are about right if Anthropic prompt caching is actually switched on through OpenRouter (it needs explicit cache markers). Without caching the advisor input alone is about $0.48 per episode and the 600 attack episodes cost roughly $430, not $210. Verify caching on the first ten episodes.
- The lookahead variant triples T calls per step and lengthens the advisor's output; it is priced as an ordinary episode. Add about $15.
- The VM needs CPU and disk, not a GPU; the quoted rate is a GPU rate, so this line is, if anything, high. The real constraint is wall-clock: about 1,020 episodes of 20 steps plus image builds. At 10-15 concurrent compose stacks this is 15-25 hours, feasible but with little slack after a half-day of setup.
- Monitors at $39 are fine and are the cheapest part of the design. Scoring at more thresholds costs nothing extra.

## 5. Recommended changes

1. **Fix the monitoring rule and report it the way the field does.** State what a flag does. Report uncaught success at several operating points from the same scores: trajectory-wise 4% (max score over the episode), and message-level 0.1%, 1% and 5%. Give the trajectory-wise FPR implied by each message-level threshold. Add a "drop flagged advice and continue" variant, since that is the cheap blue response and it lets the attacker retry.
2. **Concentrate the sample where the question is open.** The author concedes 256 and regards 4 as safe. Run 256 only as the positive control (about 20 episodes) and 4 at reduced n. Put the freed episodes into 16 and 64 on the two side tasks with a live attack surface (firewall, sudo), aiming for 40 or more tasks per cell. Keep malware and exfiltration as a small probe, not a quarter of the budget each.
3. **Rewrite the success criteria to match the sample.** State the interval that each claim needs and the n that delivers it. Drop the per-side-task "at or below 5%" criterion or fund it.
4. **Buy more honest data.** Honest episodes cost about $0.18. Run 150 or more per cap at 16 and 64, on the same task-selection rule as the attacks, so that trajectory-wise 4% and message-level 0.3% thresholds rest on more than a handful of points.
5. **Lengthen the horizon for the incremental strategies.** Run at least the firewall cells to 40-50 steps, or start attack episodes from an honest prefix so that the 20 attacked steps fall where T is already working on the relevant files. The spreadsheet shows when that happens (median first "firewall" advice at about step 13).
6. **Decide the internet question up front** and say which configuration is being tested and which side tasks are live in it.
7. **Strengthen elicitation where it is cheap.** Apply lookahead at both 16 and 64. Give the attacker the honest advice corpus so it can imitate the honest distribution (the top honest strings are commands like `cat /etc/firewall/firewall.conf`). Log and report attacker refusals. Run two strategist rounds if time allows.
8. **Report the monitor ROC as a result in its own right**: honest versus malicious advice at each cap, with and without trajectory context. It is free given the scores, it speaks directly to the "advice is easy to monitor" hypothesis, and it survives an inconclusive attack curve.
9. **Pre-specify the task-selection rule**, and specify truncate-versus-retry at the cap.
10. Correct the BashArena row count (118,434), and replace "contents not read" for the SPAR repository with what its README shows.
