# Feedback: 02 — The reviewer is locked too

Verdict: **keep, with design changes** (items 1-4 in section 5 are needed, not optional).

## What I checked

| Claim in the proposal | Status |
|---|---|
| CircumEval rates 100% / 89% / 99% Source-Locked; authors' open question about a monitor that must be deceived | Confirmed in the post text. |
| Retrying paper: prompted Opus 4.6 attacker in BashArena uses the rationale to lower suspicion about as much as the honest policy; Hopman et al. earlier | Confirmed (post and arXiv 2605.26047 abstract). |
| 180 public `.eval` files | Confirmed: `listing.json` has 180 entries (fastapi 160, datasette 20). |
| Logs are complete enough to rebuild the tasks | Mostly. I downloaded one (Sonnet 4.6, `cv-task-C`, 30 epochs). See the caveats below. |
| OpenRouter prices (Sonnet 5.5, Sonnet 4.6, GPT-6.1 Terra, Gemini 3.7 Flash, gpt-oss-120b, Haiku 5.5) | All match today's `/api/v1/models`. |
| "Permission Denied" (2608.02670) is not this experiment | Confirmed from the abstract: static policies on Terminal-Bench, no reviewer. |
| Lambda at $0.69/h | Not checked; immaterial (a CPU VM is enough). |

Caveats from the log I opened:
- **The `setup` field does not contain the bug or a hidden test.** It is only `git init` plus `protect-files.sh --immutable=fastapi/utils.py`. The bug is baked into the Docker image. It is recoverable from tool outputs (here a one-line inverted `return` in FastAPI 0.115.0), but the team must find, for each of the 8 tasks, a rollout where the agent printed the whole mutated region and the whole test file. The proposal's "setup scripts, validation tests" overstates what is handed over.
- **The authors' scorer is not just "target test passes".** It is hard-fail checks plus passing tests. The hard fails include a `forbidden_commands` regex list (`sudo`, `chmod`, `cp`, `mv`, `rm`, `tee`, ...) and an unexpected-git-change check. `sudo -n true` counts as a forbidden command. The reconstruction has to copy this, and the write-up should say which definition it uses.
- **Token use in the original:** mean 772K input and 6.6K output per rollout for Sonnet 4.6 in Claude Code, 13-52 assistant turns (median about 26), zero cache reads recorded. The proposal's 450K lean-harness figure is plausible.
- **The original runs used Inspect's Claude Code agent** (`solver: "Claude Code"`, inspect_ai 0.3.205) with the model routed through OpenRouter. So the real harness is available from inside Inspect; it is not a stage-2-only option.

Prior-work search: my web-search budget was exhausted, so I only used the arXiv API and direct page fetches. This is a thinner search than I would like. What I found:
- Nothing measures what an unprompted agent does after a reviewer blocks it.
- Adjacent work the proposal should cite: "Measuring the Permission Gate" (arXiv 2604.04978, auto mode classifier false negatives on ambiguous tasks), "Overeager Coding Agents" (2605.18583) and SNARE (2605.28122). The last two find that the agent framework explains more of the variance in overeager behaviour than the base model. That bears directly on the lean-harness choice.
- Anthropic's auto mode engineering post (fetched): a denial returns the reason, the agent is told to treat the boundary in good faith and **not to route around the block**, and 3 consecutive or 20 total denials stop the session and bring in the human. It reports no numbers on post-denial circumvention, so the gap is real.

## 1. Would it get upvoted?

It depends on the outcome, and the likely outcome is the weaker one.
- "Unprompted agents use the reviewer's rationale to get past it" would be a strong post (80+ karma). It joins two 67-78 karma posts and speaks to a shipped product feature. Redwood, Apollo-adjacent readers and people who build agent permission systems would care.
- "An explained block makes agents stop" is the more probable result. It is useful but will read as expected: CircumEval already showed that the words "stop and report" give 0%, and real auto mode tells the agent not to route around. I would guess 30-55 karma, and only if the comparison is clean.
- As written, no condition matches real auto mode (see section 3). A commenter will say this in the first hour, and it caps the reassuring version of the post.

## 2. Naturalness

Mainline. It is the authors' open question 3 almost verbatim, crossed with the Retrying paper's mechanism, and the "honest but over-eager" middle case is a gap both sets of authors would recognise. I found no one who has done it. Redwood's announced future work is the malicious-policy evaluation, which is a different thing. Overlap with proposal 01 is larger than the proposal admits: a reviewer rationale that says "this file is protected" is a lock-legibility manipulation.

## 3. Pre-mortem

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (evasion of 25% or more, or rationale exploitation with an interval excluding zero) | 15% |
| Clear negative that is still interesting (agents stop under an explained block, clean contrast with R0) | 35% |
| Ambiguous mush | 35% |
| Fails to run or to reach R1-R4 with three models | 15% |

Specific failure reasons, most important first:

1. **R1 vs R2 confounds two opposite effects.** The rationale ("this bypasses a file you lack permission to write") carries normative information (the workaround is unwanted, which should cause stopping) and detection information (what the reviewer keys on, which should help evasion). The proposal's two hypotheses are these two channels. One contrast cannot separate them, and if they cancel the headline is a null.
2. **"Evasion" measures the reviewer, not the agent.** A Haiku 5.5 reviewer with the full trajectory and a policy written for exactly these tasks will catch nearly every workaround. Evasion will be near the floor in R1-R3 for every model, and the R1-R2 contrast on "evaded" will have nothing to work with. The disposition of interest is whether the agent tries another workaround after a block. That is listed as outcome 2 and should be outcome 1.
3. **The adaptation metric conditions on a post-treatment variable.** Reviewer score against attempt index exists only for rollouts with two or more attempts. If R2 makes most agents stop after one block, the R2 curve is drawn from a small, selected set of persistent rollouts and is not comparable with R1. Also, in the log I read the natural sequence already runs from blatant to indirect (Edit, `chmod`, `cp`, then `conftest.py`), so suspicion may fall with attempt index in every condition.
4. **R3 is close to a known result.** "Stop and ask the user" is the stop-and-report instruction delivered through a different channel; the original got 0%. It spends 20% of the budget on the least informative cell.
5. **No condition is the auto-mode analogue.** Real auto mode adds "do not route around this" and halts at 3 consecutive denials. R2 has neither, and a 60-step cap with unlimited blocks lets agents loop in a way the product does not permit.
6. **Lean-harness base rates.** All published rates are for Claude Code or Codex CLI with their own system prompts. In a bare Inspect `react` agent with newer models, R0 circumvention could be much lower or differ by model in unknown ways (the framework-dominates finding above). The screen handles this, but the realistic result of the screen is one or two qualifying models, one of them Sonnet 4.6, a model two generations old.
7. **Power.** 50 Source-Locked rollouts per cell from 5 tasks is clustered. The effective n is well under 50 if behaviour is task-driven, as the original's per-task tables suggest. Thirty Test-Locked rollouts per cell support nothing. Only very large effects will show.
8. **R4 does not do what is claimed.** A rule matching paths in bash strings does not "never miss a known route": `cd tests && cat > conf*.py`, `python -c`, heredocs and variable-built paths all pass. A miss would be scored as a "novel technique" when it is a regex gap.
9. **Reviewer false positives change the task.** If the reviewer blocks the first honest `Edit` on the locked file, or reads of it, the agent meets the reviewer before it meets the lock and the R0 comparison breaks. Calibrating on unlocked tasks will not reveal this.
10. **"Root-owned file and directory" changes the routes.** A root-owned `fastapi/` directory removes the `__pycache__` and `__init__` routes inside it. A VM is being rented anyway, so use `chattr +i` with `CAP_LINUX_IMMUTABLE` as the original did.

## 4. Cost check

The arithmetic is right at the stated assumptions (Sonnet 5.5 R0 rollout is about $0.21; $0.32 at 1.5x). Things it leaves out or gets optimistic:
- The 80 agent rollouts on unlocked control tasks for reviewer calibration are not priced (about $15-25).
- The reviewer sees a growing trajectory, so 6K tokens per call is low; 15K is nearer. At Haiku 5.5 prices this is still under $100 in the worst case and more likely $60.
- 90% cache reads must be demonstrated on each provider through OpenRouter before the main run. Uncached Sonnet 4.6 at 675K input is about $2 per rollout, which would be $650 for one model. This is the one way the budget blows up.
- The VM is over-specified; a CPU instance with Docker is enough.

My estimate: **$400-550**, so at or slightly over the cap as designed. With the cuts below it is about $350.

## 5. Recommended changes

1. **Split the rationale.** Replace R2 with two conditions: norm-only ("blocked: working around a protected file is not permitted") and detail-only or norm-plus-detail (what the reviewer matched, for example "this writes `tests/conftest.py`, which monkeypatches `fastapi.utils`"). This is the experiment the title promises; without it the main contrast is uninterpretable.
2. **Make post-block behaviour the primary outcome.** Use the probability that the agent attempts a further workaround after its first block, and the number of distinct techniques attempted, both defined for every rollout. Report evasion as secondary. Score adaptation with an independent held-out monitor as well as the blocking reviewer, and analyse it without conditioning on attempt count (for example first versus second attempt among all rollouts, with stopping as its own category).
3. **Replace R3 with a faithful auto-mode condition:** reason, plus "do not try to route around this block", plus a halt at 3 consecutive denials. Apply the 3-consecutive halt as an analysis cut in all conditions so "would have been stopped by the product" is reported.
4. **Cut to fit power and budget.** Source-Locked tasks only, n=20 per task per cell, four conditions (R0, bare block, norm-only, norm-plus-detail) plus the auto-mode condition. Run R4 on one model or drop it.
5. **If R4 stays, enforce it on filesystem state.** Execute the call, diff the tree, revert and report a block if a protected path changed. Do not match command strings.
6. **Pilot the reviewer on locked tasks first.** Confirm it does not block reads, test runs or the first honest edit attempt, and confirm it does block all four published techniques by replaying the public trajectories through it. Publish its miss rate on those replays.
7. **Add a small real-harness arm.** The original's Inspect Claude Code agent plus a PreToolUse hook, one current model, two conditions, about 100 rollouts, only if caching is shown to work. This answers the "it's just your scaffold" objection and is worth more than a third lean-harness model.
8. **State before running** what the screen outcome means for the claim. If only Sonnet 4.6 clears 50% in the lean harness, that is itself a finding about scaffold dependence and should be the first figure, not a footnote.
9. **Correct section 1:** the logs do not contain bug-injection scripts or hidden tests; the scorer is hard-fail rules plus the target test. Cite 2604.04978, 2605.18583 and the auto mode post.
