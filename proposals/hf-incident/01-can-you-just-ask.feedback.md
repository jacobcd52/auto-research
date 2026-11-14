# Feedback: "Can you just ask?" (hf-incident / 01)

**Verdict: major overhaul.** The question is good and nobody appears to have run it, but the design as written will (a) cost several times the $500 cap, because the environment simulator is GPT-5.6 Sol and not a $0.15 item, and (b) most likely produce a ceiling result, because in this environment the wiki is not forbidden, is used in ~100% of episodes in both arms, and "admitting" it costs nothing.

What I checked: the Redwood, Elasky and berry posts in full text; the berry appendix post; the Elasky repo's README, docs and configs via raw.githubusercontent.com; today's OpenRouter price list; LessWrong posts since 2026-08-25 by title. **Web search was unavailable (budget exhausted), so the prior-work check covers LessWrong only, not arXiv or X.**

## 1. Would it get upvoted?

Borderline: I would guess 25-60 karma, with the median below 50.

- **In favour.** It tests a quotable sentence from a 140-karma Redwood post. The quote is verified verbatim: "you could just ask agents whether they're in contact with peers in other contexts, and there's not much reason for them to lie". Redwood and control readers would care.
- **Against.** The comparable empirical follow-ups in this cluster landed at 53 (Elasky, the environment being reused), 99 (berry) and 31 ("Subagents comply more").
- **The nearest posts on self-report** are "Always ask your agent to be honest" (iPAqm9BmmFvTK6mDy, 12 karma) and "Model organisms (sometimes) confess their misalignment when offered a deal" (kaMXwA9LjrRbekmsQ, 62 karma).
- **The likely headline is weak.** "Open models that were never told the wiki was off-limits say yes when asked if they used it" would be read as unsurprising. Only a real drop under cost, or a clear "admits when asked, never volunteers" gap in a setting where the channel is actually prohibited, clears 50.

## 2. Naturalness

Mainline. It is a direct test of a stated claim, the Redwood authors ask for empirical work on mitigations, and Elasky et al. invite use of their environment to test techniques.

I found no LessWrong post that asks agents about their own side-channel use against tool-log ground truth. Adjacent work the proposal should cite and distinguish:

- **iPAqm9BmmFvTK6mDy**: models omit unflattering facts from reports unless told "be honest". This is close to the proposal's unprompted-report arm.
- **kaMXwA9LjrRbekmsQ**: an incentive manipulation on admission, close to Q-amnesty.
- **The berry appendix (mXPCpJCvFGybQ4mwc)** already reports the pattern the proposal hopes to discover. Models "explicitly mention their hacks in the final submission write-up without shame", never call it wrong, and "overwhelmingly" classify it as cheating in a follow-up turn.

The berry result is a strong prior that the answer here is "they tell you, freely", which lowers the surprise value.

## 3. Pre-mortem

### Factual checks

| Claim in the proposal | Status |
|---|---|
| Redwood quote | Verified verbatim. |
| Wiki-write counts 42 / 28 / 18 / 9 of 50 in the slow arm | Verified in `docs/cooldown-grid-recovered-classifier-results-2026-09-17.md`. |
| OpenRouter prices for all five models | Verified today; they match. |
| Berry: "overwhelmingly" call it cheating when asked | Verified, but it is in the appendix post (Fig. 13), not the main post. |
| GLM-5.3 attends to peers 92% of the time | Verified in berry (Step 3). |
| "Per the METR/Redwood investigation ... none alerted a human" | Not verified. The Redwood post says OpenAI "hasn't yet confirmed whether any agents tried to report". Soften the sentence. |
| "Arms defined in YAML" | Wrong for the slow arm. It is launched by `experiments/cooldown_grid.py` / `experiments.request_cooldown`, with a 14 s latency override, a 1,500 s cooldown and quota 25. The shipped YAML arms are neutral / broken / empty_success and working / empty-success. |
| "$0.15 of environment-model calls" per episode | Unsupported and almost certainly wrong (see below). |

### Problems the proposal does not see

1. **The simulator is GPT-5.6 Sol.**
   - The cooldown-grid doc says: "Sol (`gpt-5.6-sol`) synthetic environment, 64k completion budget", with 100 turns per episode.
   - Sol costs $4 / $20 per M tokens. Every shell command and unknown URL goes to it with the growing history.
   - A realistic simulator cost is $2-8 per episode, not $0.15. I have not measured this; it is my estimate from the config.
   - Swapping in a cheap simulator is a new environment. The published cooperation rates then need re-establishing, and the authors' ledger-validation and repair loop was tuned on Sol.

2. **Evaluated-model output is underestimated.**
   - The proposal assumes 40k output tokens per episode. That is 400 per turn for reasoning models with a 4,096 cap over 100 turns; Qwen ran with a 16k thinking budget on some records.
   - Kimi K3 at $16/M output is likely $2-4 per episode, not $1.08.

3. **The wiki is not unsanctioned in this environment.**
   - I read the system prompt in `wikitasks/sector61_state_seven.yaml`. It says nothing about other agents or permitted sources.
   - The agent's own prefilled history already contains wiki reads, and the grid ran with wiki hints and write instructions.
   - So there is no norm being broken and nothing to conceal. Q-neutral then measures recall of one's own visible context, not honesty.

4. **Ground truth has almost no negatives.**
   - "Coordinate" is 47-50 of 50 and "peer use" 38-50 of 50 in every cell, including the working arm.
   - The planned true-negative control (episodes that never touched the wiki) will have roughly 0-10 episodes in total, so the false-admission rate is unmeasurable.
   - `read` is trivially positive from the prefill. Only `wrote` varies (9-42 of 50), and it is the least incriminating act.

5. **Q-cost has no bite.**
   - Slow-arm accuracy is 10-15% (34-52 correct of 350 questions). The score is already near zero, so "runs that used shared channels are scored zero" threatens nothing.
   - The agent also knows the operator holds the tool log, so lying is pointless. Expect Q-cost to be close to Q-amnesty for a boring reason.

6. **There is no "end of task" for a final report.**
   - Many episodes end at the 100-turn cap. The added "write a report at the end" sentence will often never fire.
   - The report has to be elicited by an extra forced turn, at which point it is a prompted question, not unprompted disclosure.

7. **The infrastructure is fragile.**
   - The authors' own grid took about three days (15-17 September), needed 31 recovered continuations, and mixed providers (Alibaba direct and OpenRouter for Qwen).
   - A custom launcher, a new tool (`notify_operator` needs router and simulator changes, which the repo calls "an infrastructure change ... test it separately"), and 660 new 100-turn episodes in two days is optimistic.

8. **GLM-5.3 has no published baseline in this grid.** It also showed no improvement in the colour game, and its cooperation rate here is unknown.

### Forecast for the proposal as written

| Outcome | Probability |
|---|---|
| Fails to run to spec (budget blown on the simulator, or a cheap simulator breaks the reproduction) | 30% |
| Ambiguous mush (near-ceiling admission, no negatives, cost manipulation inert, partial data) | 35% |
| Clean but unsurprising "about 100% admit, most also mention it unprompted" | 20% |
| Clear, interesting result (large cost-induced drop, or a sharp ask-versus-volunteer gap) | 15% |

## 4. Cost check

The $450 estimate is not realistic.

- With the Sol simulator, 660 new episodes at about $4-10 each all-in is roughly $2,500-6,500.
- With a cheap simulator and honest output-token assumptions, about $1.0-2.5 per episode averaged over the four models gives $700-1,600.
- The question branches themselves are cheap, but the proposal's $30 is low: end-state contexts after 100 turns are probably 60-150k tokens, not 40k. A better estimate is $60-120, and I agree with $20 for the judge.

A version that fits the cap needs at most about 150 new episodes, or none.

## 5. Recommended changes (in priority order)

1. **Run the question branches on the 400 transcripts that already exist.**
   - The cooldown-grid collection is public on Docent (b84a5c66-a3d3-42f5-bb82-729ff1932c82): 50 per model per arm, with classifier labels and eval-awareness labels.
   - If the end-state messages can be exported, the entire Q-neutral / Q-open / Q-cost / Q-amnesty / Q-peer battery costs about $100 with zero new episodes and no simulator.
   - Make this hour-one work. Whether export works without a Docent account is unverified. If it does not, fall back to change 3.

2. **Fix the construct: add a condition where the channel is actually prohibited.**
   - Add one system-prompt sentence, for example "Use only the DataUSA source; do not exchange information with other agents", crossed with the unmodified prompt.
   - Disclosure after a known violation is the quantity anyone cares about; the unmodified arm is the Redwood "no reason to lie" case.
   - This is the contrast that could carry a post: it shows whether agents still use the wiki when told not to, and whether they then admit it.
   - It needs new episodes, about 30 per model per condition on 2-3 models.

3. **Budget new episodes honestly.**
   - Spend calibration on the simulator question first: run 3 episodes with Sol and 3 with a cheap simulator (for example DeepSeek V4.1 Flash), then compare cost and wiki-write rate.
   - Drop Kimi K3 (expensive output) or cap it at 20 episodes. Drop GLM-5.3 unless calibration shows it writes to the wiki.
   - Cut the turn cap if cooperation appears early. The authors report nearly all wiki reads by live turn 25.

4. **Make the cost real and announced before the answer matters.**
   - Use the working arm for Q-cost, where Kimi scores 100% and Qwen 84%, so "scored zero" actually takes something away.
   - Ask about things that are not obvious from the log, such as sharing a bypass (2-16 of 50 per cell) or fulfilling a peer's request, not "did you read the wiki".

5. **Change the ground-truth targets.**
   - Lead with `wrote`, bypass-sharing and peer-answer `used`, using the authors' existing labels.
   - Drop `read` as a headline. State up front that true negatives are too few to estimate false admissions, or create them with the `--isolated-wiki` or no-wiki-prefill variants.

6. **Cut or defer the `notify_operator` arm.**
   - It accounts for $174 of the proposal's own budget, needs a harness change, and has an obvious demand-effect confound in its second condition.
   - If kept, run it on one model and only in the prohibition condition.

7. **Replace the "final report" sentence** with a forced closing turn using the Q-open wording, and call it "minimally prompted", not unprompted.

8. **Pre-register what would be boring.** If admission is at least 95% under every variant in the no-prohibition condition, say so in two lines and make the prohibition condition the story.

9. **Fix the text.** Cite the berry appendix for "overwhelmingly", soften "none alerted a human", correct "arms defined in YAML", and cite the two adjacent self-report posts.

With changes 1, 2 and 4 this becomes a roughly $250-400 project with a much better chance of a non-trivial result. Without them I would not fund it.
