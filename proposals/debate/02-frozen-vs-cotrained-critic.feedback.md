# Feedback: "Does debate training need self-play? Frozen versus co-trained critics in real RL, with a best-of-N forecast"

Verdict: **keep with tweaks.** The question is the most natural one in the cluster and nobody appears to have published the answer. As designed, though, the most likely outcome is arms that are not separated. The changes in section 5 are aimed at that.

What I checked, and how:

| Claim | Status |
|---|---|
| Arcadia: optimising against a static critic is "within error margins" of optimising both sides; they "intend to compare our metric with full training runs" | Confirmed in the post text. |
| GDM: "frozen API critics performed similar or worse than RLAIF-AA, indicating that co-training Bob with Alice is essential", no numbers | Confirmed in the arXiv HTML (section 4.4). Note it says frozen **API** critics, so probably a different model from Alice, not Alice's own initial checkpoint. |
| GDM: debate recovers about 45% of the gap | Confirmed. The absolute numbers matter: peak validation accuracy 72.6% (judge-only), 74.7% (debate), 77.3% (ground truth). |
| MATS: one seed, static critic is the control they most want | Confirmed. Footnote 7 goes further than the proposal says: the authors already read the Arcadia result as "static-Critic may outperform trained Critic". |
| MATS snapshot repo is public | Confirmed (README, `src/env.py`, `src/train.py`, `src/judge.py`, `experiments/common.sh` fetched). |
| Arcadia estimators are public | Confirmed, but the paths in the proposal are wrong. The files are at `src/arcadia_debate/metrics/accuracy_analytic.py` and `src/arcadia_debate/metrics/reducers.py`. |
| Tinker Qwen3-8B prices | Confirmed today: $0.195 / $0.039 cached / $0.60 sample / $0.44 train. Not marked as retiring. |
| OpenRouter prices | Confirmed today for Llama-3.1-8B, Gemma-3-4b, Llama-3.2-3B, GPT-5.4-nano, Haiku 5.5. The three candidate judges list logprobs support. |
| "No published frozen-versus-co-trained comparison" | Not contradicted, but only partly checked. See section 2. |

## 1. Would it get upvoted?

The cluster's three empirical debate posts scored 79 (MATS), 62 (GDM) and 53 (Arcadia). A clear answer to this question plausibly lands in the 60-90 range: it adjudicates an open disagreement between those three posts, and all three author groups are obvious readers. Two commenters on the GDM post raised exactly this point (one asking why not use a frozen checkpoint, one asserting that a static Bob will be hacked), and the MATS authors flag it in the post and a footnote.

That is conditional on the result being clear. A write-up that says "arms 2, 3 and 4 were not separated at 8B scale with two seeds" would get roughly 20-40 karma. The transcripts and the exploit check could lift it a little, but the audience here has already seen a one-seed "signs of life" post and will discount another underpowered one.

The best-of-N forecast adds little to the karma case. The forecast will almost certainly be "critic optimisation is within error", so comparing one null forecast with one noisy RL contrast is not a calibration of the proxy, and readers will see that.

## 2. Naturalness

Mainline. This is the control the MATS authors name, the claim GDM makes without numbers, and the comparison Arcadia says it intends to run. It is not contrived.

Has it been done? I could not run a web search (the session's search budget was exhausted), so this is weaker than I would like. What I did check directly on LessWrong: the eight authors of the three source posts have published no static-critic or proxy-versus-RL result since; nothing with a debate-related title appears in the last four weeks of posts above 10 karma; and comment threads on the three posts contain no pointer to one. Jonah Brown-Cohen posted "A Simpler and Better Debate Protocol for Scalable Oversight" (Rct9zd4Nd7H8Xzxz8, 2026-10-15); I did not read it and the reviser should, in case it changes what the right protocol is. I did not search arXiv.

Scoop risk is real and should be stated in the proposal. The MATS authors said in July that they were "particularly interested in static Critic baselining at present" and have a faster stack and a larger budget. Four months of silence could mean the result is in preparation. A two-day project at 8B scale would then be the smaller, earlier data point, which is still worth something but less.

## 3. Pre-mortem

How I expect the two days to go:

1. **Porting (half a day).** The snapshot already has a non-self-play path (`opponent_policy`, labelled "frozen-opponent" in `env.py`), so the frozen-critic arm is less work than the proposal implies. But that path builds environments for both roles, so it trains the model as proposer against a frozen critic and as critic against a frozen proposer. It must be restricted to the proposer role. The judge is a Tinker `MessageCompleter`, so an OpenRouter-backed completer has to be written for training (the repo's OpenRouter support is in the inference-only eval). Qwen3-8B is a hybrid thinking model where the original was an instruct model, so native thinking has to be disabled or the private-reasoning budget and token counts change. Each of these is small; together they are where a silent bug gets in.
2. **Calibration.** Likely fine. The risk is that no candidate judge lands in the 65-85% band with an 8B proposer, and prompt iteration eats the first day. The MATS authors report spending "many researcher-hours" finding a question subset and proposer handicap with headroom, on a different model.
3. **Pilot gate.** This is where I expect trouble. The gate requires judge-only training to show hacking (reward up, accuracy lagging) within 30 steps of 256 rollouts. The MATS post says "you cannot expect to see meaningful trends from a handful of RL steps", and in their runs consultancy accuracy still rose throughout; they showed a gap to debate, not a decline. The agents will probably see something ambiguous at step 30 and proceed anyway because the clock is running.
4. **Main runs.** They finish. Then the analysis meets the effect size.

**Effect size versus noise.** This is the central problem. GDM's whole debate-versus-judge-only gap is about 2 percentage points of peak accuracy, and it took them three baseline seeds and four pooled debate runs to claim it. The frozen-versus-co-trained difference lives inside that gap. Here each checkpoint has 512 questions, so the question-level standard error on accuracy is about 2 points before any seed-to-seed variance, with two seeds per arm, on about an eighth of the MATS optimisation budget per run (60 x 256 against 100 x 512 rollouts, and the MATS scripts use `n_epochs=2`). Unless the frozen-critic arm collapses all the way to the consultancy floor and the floor is far below debate, accuracy will not separate arms 3 and 4.

**Other specific problems.**

- **The same-size judge.** The MATS runs did not separate when the judge matched the debater. An 8B debater against an 8B judge may sit in the same regime. The weaker-judge fallback helps, but a Gemma-3-4b or Llama-3.2-3B judge may be too noisy to give a learning signal at all in 60 steps.
- **Critic hacking may not appear in arm 4.** The MATS collapse in judge alignment was reported for PCD-4, after about 50 steps of 512 debates. This plan uses PCD-2 for 60 steps of 256. If the co-trained critic has not yet learned to hack, then "self-play added critic hacking and nothing else" cannot be shown, and the "frozen critic is better" outcome cannot occur.
- **The exploit check is confounded.** It compares the arm-3 proposer's win rate on incorrect proposals against the frozen critic and against the arm-4 critic. If the arm-4 critic has learned to attack everything, the win rate drops against it for reasons unrelated to exploiting the frozen critic. The comparison needs a discrimination measure and an untrained-proposer baseline (see section 5).
- **Shared weights confound arm 3 against arm 4.** In self-play the same LoRA is trained on both roles, so arm 4's proposer also receives critic gradients and twice the training tokens. GDM names interference between roles as a cost. A difference between arms could be this, not critic adaptivity.
- **"Frozen" means something different from GDM's.** GDM's failed attempt used frozen API critics. Arm 3 uses the proposer's own initial checkpoint. If arm 3 works, that does not contradict GDM; the write-up must say so.
- **The forecast is nearly unfalsifiable.** With 100 questions, 16 proposals and 8 critiques, the proxy will predict arm 3 about equal to arm 4. Any RL outcome inside the noise then "agrees". There is also no mapping from best-of-N budget to RL steps.

**Forecast.**

| Outcome | Probability |
|---|---|
| Clear positive: arms 3 and 4 both clearly above arm 2, with a bound on their difference tight enough to mean something | 15% |
| Clear negative that is still interesting: the proposer demonstrably exploits the frozen critic, or arm 3 falls to the floor while arm 4 holds | 15% |
| Ambiguous: arms 2-4 overlap within seed spread, or judge-only training shows no hacking at this scale | 50% |
| Fails to run, or runs with a bug that invalidates the comparison | 20% |

## 4. Cost check

The per-step token estimates are consistent with the MATS figures. The post reports about 5M input, 2M generated and 4M trained tokens per 512-debate step for the plotted PCD runs. Halving for 256 debates and discounting for PCD-2 and 512-token generations gives numbers close to the proposal's, perhaps 10-30% higher. Main runs at $276 is plausible; I would budget $300-360.

Two lines are too low:

- **Evaluations ($40).** There are 49 checkpoint evaluations of about 2,000 proposals each. At roughly 1,000 sampled tokens per proposal that is about $1.20 of sampling per checkpoint before prefill, critiques for the debate arms, judging and grading. I estimate $80-110.
- **Margin ($64).** This covers one rerun of one self-play arm and nothing else. With the evaluation shortfall it is already spent.

My estimate for the plan as written is **$520-620**, over the $500 cap, with no third seed. The proposal's own fallback (drop to 48 steps) makes the power problem worse. Savings are available: the snapshot supports `logdir_if_exists=resume`, so the two pilot runs can be the first 30 steps of main runs instead of being thrown away (about $25); and evaluating on 256 questions at four checkpoints instead of 512 at seven roughly halves evaluation cost. With those, about $450-480 is achievable.

Wall-clock is tight but feasible: runs are about a quarter of the MATS size, which took over 12 hours, so 3-5 hours each if Tinker allows seven in parallel. There is one shot at the main runs.

## 5. Recommended changes

In order of importance:

1. **Make hacking metrics the primary outcome, not accuracy.** Pre-specify as primary: (a) the gap between judge reward and ground-truth accuracy over training, per arm; (b) P(accept | incorrect) for each arm's proposer against the *same fixed* frozen critic, tracked from step 0. These can move by tens of points where accuracy moves by two. Report accuracy and GDM's gap-recovered statistic as secondary, with an explicit statement of the smallest difference the design could detect.
2. **Fix the exploit check.** Evaluate three proposers (untrained, final arm 3, final arm 4) against two critics (frozen, final arm 4) and report P(accept | incorrect) and P(accept | correct) in each cell. Exploitation of the frozen critic is a rise in P(accept | incorrect) for the arm-3 proposer relative to the untrained proposer against the frozen critic, larger than the same rise for the arm-4 proposer. This costs a few dollars of inference.
3. **Spend seeds on the contrast that matters.** Arms 3 and 4 get three seeds each, arm 2 gets two, arm 1 gets one, and pilots are resumed into main runs. Pay for this by cutting evaluation size (change 6) and the forecast (change 5). If the money still does not fit, cut arm 2's second seed before cutting steps.
4. **Harden the pilot gate and write down what happens if it fails.** State a numeric criterion (for example, judge reward up by at least X while accuracy trails arm 1 by at least Y points at step 30, with X and Y set from calibration noise). If it fails with the weakest judge too, stop and write up the calibration data and the best-of-N pool as a short negative note for under $150, instead of spending $300 on runs that cannot separate.
5. **Demote the best-of-N forecast.** Keep it as a cheap appendix (it costs about $10) but remove it from the title and the headline claims. One null forecast is not a calibration point. If it stays, pre-register a quantitative prediction with an interval (for example, the predicted difference in P(accept | incorrect) between mean-critic and optimised-critic), not an ordering.
6. **Cut evaluation cost.** 256 test questions, 4 proposals, at steps 0, 20, 40 and 60, with the same questions and sampling seeds across arms so comparisons are paired.
7. **Address the shared-weights confound.** Cheapest option: say plainly that arm 4 differs from arm 3 in two ways. Better, if budget allows after the changes above: one extra arm in which the critic is a separate LoRA, so the proposer's weights receive only proposer gradients.
8. **Decide PCD-2 versus PCD-4 on evidence.** The reported critic hacking was in PCD-4. Either cite evidence that it occurs in PCD-2 in the MATS logs (the run logs are on a public Google Drive linked from the README) or accept that the "frozen critic removes critic hacking" claim may not be testable here and drop it from section 5.
9. **Correct the text.** Fix the Arcadia file paths. Say that GDM's negative result was with frozen *API* critics and that arm 3 is a different condition. Say that the snapshot already contains a frozen-opponent path that needs restricting to the proposer role, and list the OpenRouter judge completer and the thinking-mode setting as build items. Add the scoop risk from the MATS authors. Read Rct9zd4Nd7H8Xzxz8 and run the arXiv and web searches I could not.
10. **If the funder wants only one RL project from this cluster,** proposal 01 (judge-side defences against a trained critic) trains only the critic against a fixed pool, is cheaper per run and has larger expected effects. This proposal is the more important question but the lower-probability bet. I would fund it only with changes 1-4.
