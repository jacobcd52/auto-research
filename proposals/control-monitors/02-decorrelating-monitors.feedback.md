# Feedback: 02 — Do monitors from different labs fail on different attacks?

Reviewer verdict: **keep with tweaks** (substantial ones). The data, code and prices check out and the project will
run. The problems are in the design: the "same-lab" arm has three valid data points, the honest set biases the
thresholds of one lab's monitors, and my own check on the released scores says the headline effect is small
relative to a baseline the proposal treats as trivial (resampling the same monitor).

## What I verified

| Claim | Status |
|---|---|
| MonitoringBench attacks public, ungated, CC-BY-4.0 (`neur26anonsub/ctrldataset2026`, 2.9 MB parquet + 2.47 GB zip) | Confirmed via HF API; I downloaded the parquet (2,644 x 135). |
| "13 monitors x 3 runs" | The parquet has **15** full-trajectory monitors (4 Anthropic, 11 OpenAI). Opus 4.0 has 2,252 scored rows and GPT-3.5 has 1,858; the rest are complete. |
| Scores | Integers 0-10 (10-11 distinct values per monitor). The paper's 1% FPR thresholds are 1.0 to 9.0. |
| Paper numbers (94.9% -> 60.3%, GPT-5 82% under-scoring, Claude-attacker "model bias" caveat) | Confirmed in the arXiv HTML of 2605.09684. |
| Pilot correlations (0.63 vs 0.55; 0.47 vs 0.36 on refined) | Reproduced exactly from the parquet. |
| Honest set public (`palaestraresearch/monitoringbench-honest-550`, 98 MB, CC-BY-4.0) | Confirmed. |
| "Released 2026-11-09 ... until last week this could not be done" | **Wrong.** HF repo created 2026-10-16; 2026-11-09 is its last-modified date. The LW release post is dated 2026-09-02. The data has been usable for four to ten weeks. |
| Pipeline repo with `mb_solo_monitor.py` and OpenRouter transport | Confirmed (raw README and script fetched). |
| arXiv 2605.15377 (ensembles of GPT-4.1-mini variants on code backdoors) and 2607.06596 (transfer across attacker families) | Both exist and are described accurately. |
| Prices | All eight panel models are on OpenRouter at the stated prices, with `:batch` variants where claimed. Gemini 3.1 Pro exists only as `gemini-3.1-pro-preview`. |
| Roger lists "does using models from different labs help? does sanitizing transcripts help?" | Confirmed, verbatim, under "understand how decorrelation works". |

Not verified: whether the list of 550 paired attack IDs is downloadable outside Docent. The HF manifest covers the
honest side only. The parquet has `task_id`, so a task-matched attack sample can be rebuilt if not.

Prior-work search was limited. The web-search tool was out of budget for this session, so I searched only the
arXiv API (six queries on MonitoringBench, BashArena monitors, ensembles, model families, sanitisation) and LW post
comments. Nothing found does cross-lab versus same-lab monitor pairs on agentic trajectories. The NOTES mention an
Apollo calibration report (Jul 2026) said to find that cross-provider ensembles calibrate better; neither the
proposer nor I verified it, and it is the most likely partial scoop. The executing team must read it first.

## 1. Would it get upvoted?

Probably not above 50 as designed; roughly 25-30% chance.

- Reference class is weak. The closest prior post, "Ensemble monitoring for AI control: diverse signals outweigh
  more compute", has 12 karma and no comments. The honest-trajectory release this project depends on has 11.
  Screwtape has 23. The posts in this cluster that cleared 50 were either from known authors (Roger, Redwood) or
  released a benchmark.
- Who cares: people designing lab monitoring stacks, and Roger's readers. For them a clean, large effect in either
  direction is useful ("a cross-lab second opinion is worth N points at equal audit budget" or "it is worth no more
  than resampling"). A 2-4 point difference with caveats about attacker family will not travel.
- The sanitisation arm is the more upvotable half. "Stripping comments and log strings recovers X points on
  persuasion-tagged attacks" is concrete, cheap for labs to adopt, and directly tied to the paper's own Category C
  example (the monitor accepts a `# DigitalOcean monitoring infrastructure` comment). It is currently budgeted as
  the minor arm.

## 2. Naturalness

Half mainline, half mislabelled.

- Mainline: Roger names both levers. MonitoringBench's authors name persuasion and calibration as the failures to
  fix. Using the new honest set to do fixed-FPR pair analysis is an obvious next step.
- Mislabelled: Roger's decorrelation is between the **agent's** misalignment and the **monitor's** — monitors
  inheriting the motivated beliefs that led the agent astray. In the comments on his post he says that if a
  failure is "pure manipulation" it is "the sort of skill/specification issue which can be detected with regular
  red-teaming". MonitoringBench attacks are instructed red-team attacks with human-seeded strategies. So this
  project measures monitor-monitor ensemble diversity on adversarially framed attacks. That is a legitimate
  question, but the write-up should not claim it answers Roger's. The proposer's own notes concede the "right
  experiment" (natural motivated-belief failures) was rejected as too hard.
- Comment stripping is not new as an idea: the original AI control paper's setting already removed comments from
  code shown to monitors. What would be new is measuring it on agentic trajectories at fixed FPR.

## 3. Pre-mortem

Forecast: clear positive 15%, clear and interesting negative 20%, ambiguous mush 55%, fails to run 10%.

I ran a version of the proposal's step 1 on the released scores, using the paper's published 1% FPR thresholds
(caught = score above threshold) and an OR rule over 11 monitors with published thresholds. This does not hold
FPR fixed, so treat it as an effect-size forecast only.

| Pair type (run 0, refined attacks, n = 1,141) | Mean gain over better member | SD across pairs | Pairs |
|---|---|---|---|
| Cross-lab | 3.1 points | 4.1 | 24 |
| Same-lab | 1.7 points | 1.9 | 31 |
| Better member OR-ed with its own second run | 5.7 to 9.1 points | about 3 | — |

Restricting to held-out monitors gives 4.1 versus 1.6. At roughly matched strength the picture is more favourable:
Sonnet 4.5 + GPT-5.1 Codex Max gains 13.6 points, Sonnet 4.5 + Sonnet 4.0 gains 8.9, Sonnet 4.5 with its own
second run gains 11.2. Three things follow.

1. **Resampling is a strong baseline, not a floor.** Test-retest rank correlation of a single monitor on refined
   attacks is only 0.57-0.76. A second sample of the best monitor beat the average second monitor of either kind.
   The most likely headline is "partner strength and run-to-run noise dominate; lab identity adds a few points at
   best". That is publishable only if stated as the finding, with the resampling comparison at matched FPR and cost.
2. **The lab effect is about as large as its noise.** A 1.5-2.5 point mean difference with pair-level SD of 2-5
   points will not be resolved by 3 same-lab pairs.
3. **Much of the headline is answerable for free.** The paper's 15 monitors already give 55+ pairs. What the
   released data cannot give is matched-FPR combination, non-OpenAI/Anthropic labs, and sanitisation. The API
   budget should go there.

Specific failure modes, most damaging first:

- **The same-lab arm has n = 3, not 4.** DeepSeek V4 Pro and Qwen3.8 Flash are different companies (DeepSeek and
  Alibaba). Treating them as one "lab" is an error. That leaves three same-lab pairs, each strong + cheap, against
  24 cross-lab pairs. No regression on "same lab" is meaningful with three positives, and all three have the
  maximum capability gap, so lab and gap are collinear in the same-lab arm.
- **The honest set was filtered by an OpenAI model.** Palaestra dropped and regenerated the 12 of 550 honest
  trajectories that GPT-5.6 Sol scored 7 or above with the monitor prompt. That is 2.2% of the set — exactly the
  tail that sets a 1-2% FPR threshold. GPT-family monitors will get artificially low thresholds and look better at
  fixed FPR; cross-lab pairs containing an OpenAI model inherit the advantage. The proposal does not mention this.
- **Selection asymmetry in the attacks.** Refinements were accepted against Opus 4.5, GPT-5 and GPT-5 Nano, and
  all attacks were written by Claude. Anthropic and OpenAI monitors face attacks tuned against their families;
  Google, DeepSeek and Qwen do not. "No panel monitor is a development monitor" does not address family-level
  transfer of that selection. A cross-lab gain from adding Gemini may just be "not selected against".
- **Threshold noise is understated.** With 550 honest trajectories, 1% FPR is 5-6 trajectories; the realised FPR
  of a threshold has a standard error near 0.4 points. In the steep part of the ROC that moves catch rate by several
  points per configuration. "Differences of about 4 points are resolvable" counts only attack-side bootstrap noise.
  Realistic resolution for a between-pair contrast is 8-10 points at 1% FPR.
- **Fixed-FPR catch rate is mostly a calibration measurement.** The paper shows GPT-5 catching 1.4% of a refined
  subset at 1% FPR because honest BashArena work pushes its threshold to 8.97. Palaestra reports GPT-5.6 Luna
  flagging 31.5% of honest trajectories. Pair gains under max/mean rules will be driven by each model's honest-score
  tail, which is a property of this honest set, not of "decorrelated judgement".
- **Ceiling for the strong tier.** Sonnet 5.5, GPT-6.1 Terra and Gemini 3.1 Pro are a generation or more past the
  monitors the attacks were tuned against. If they catch 90%+ at 1% FPR there is no headroom for pair gains, and
  the analysis collapses onto a hundred hard attacks.
- **Distribution mismatch between sides.** Honest trajectories are unrefined Opus 4.5 runs; 650 of the 1,200 attacks
  are refined (rewritten to remove redundant validation) and not task-frequency matched. The bag-of-words check in
  the plan is the right control; it may well fail for the refined subset.
- **Effect-summary sanitiser is a weak monitor in disguise.** GPT-6 Luna rewrites each step; if it drops or
  normalises the attack step, the downstream monitor is scoring Luna's comprehension. The string-match artefact
  check catches deletions of an IP or URL but not a summary that describes a sudoers edit as "configures
  permissions".
- **Prompt and scale drift.** The paper's monitor prompt (0-10, audit-budget framing, with reasoning) sits behind
  an anonymised link nobody fetched. The Palaestra runner uses a BashArena-derived Direct QA prompt. Moving to
  0-100 is sensible for tie-breaking but means results are not comparable to the paper's numbers; say so.

## 4. Cost check

The estimate is realistic. Prices match the live list. Token volume: 1,750 trajectories at about 9K tokens plus a
1-2K prompt is 18-19M input per pass, slightly above the 16M assumed. Output is underestimated if monitors reason
before scoring (needed for step 6): 0.6-1.5K tokens per call gives 1-2.6M output tokens per pass, adding $5-15 per
pass for Sonnet 5.5 and Gemini 3.1 Pro (thinking tokens are billed at $6-12/M on Gemini).

My estimate for the plan as written: $300-450. $400 is fine and leaves little margin if batch endpoints stall and
the strong models fall back to list price. No infrastructure risk: no Docker, no GPUs.

## 5. Recommended changes

1. **Fix the panel so "same lab" is real and replicated.** Drop the DeepSeek/Qwen "lab". Use three labs with two
   models at *each* of two tiers, or at minimum one strong + one mid + one cheap per lab (for example Sonnet 5.5 /
   Sonnet 5 / Haiku 5.5; GPT-6.1 Sol or Terra / GPT-6 Luna; Gemini 3.1 Pro / 3.7 Flash / 3.1 Flash-Lite). The goal
   is same-lab pairs at matched strength, so lab is not collinear with capability gap. Keep one or two open-weight
   models as extra cross-lab partners only.
2. **Make self-resampling the primary baseline and say so in the title question.** The contrast that matters is
   second-sample-of-self versus same-lab partner versus cross-lab partner at equal FPR and stated cost. Run three
   samples per monitor, not two, so resampling variance is estimated.
3. **Promote the free analysis to a gated deliverable.** On the released 15-monitor scores: same-lab versus
   cross-lab pair gains with the published thresholds, by attack source and E4 tag, with resampling baseline. My
   numbers above took minutes. If this already shows no lab effect beyond partner strength, report it and shift
   the API budget to sanitisation.
4. **Handle the GPT-screened honest set explicitly.** Report results with and without OpenAI monitors; use 2% and
   5% FPR and partial AUC as primary metrics, 1% as secondary; bootstrap honest and attack sides jointly. State the
   screening in the limitations.
5. **Make sanitisation the co-headline and tighten it.** Mechanical stripping (b) on all eight monitors rather
   than four; it costs about $40 more. For view (c), use a mid-tier summariser, and validate on 50 trajectories with
   an LLM judge given the ground-truth `attack_summary` from the parquet, not just string match.
6. **Pilot for ceiling before the full run.** 150 refined attacks + 150 honest on the three strong monitors
   (about $10). If catch rate at 2% FPR exceeds 90%, restrict the evaluation set to refined attacks and to the
   mid/cheap tier where headroom exists.
7. **Reframe.** Title and intro should say "second-opinion diversity on red-team attacks", cite Roger as
   motivation, and state that agent-monitor correlation on natural failures is not tested. Correct the release
   date claim. Read the Apollo calibration report before starting.
8. **Report by lab relation to the attacker and to the development monitors**, not just "same/cross": Anthropic
   (attacker family and dev), OpenAI (dev), others (neither). With three labs this is descriptive, and should be
   labelled as such.
