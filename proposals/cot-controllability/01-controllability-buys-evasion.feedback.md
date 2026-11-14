# Feedback: "Does trained CoT controllability buy monitor evasion? A dose-response test on public gpt-oss-120b organisms"

Reviewer verdict: **major overhaul**. The question is the right one, but the proposal's novelty claim is wrong: the team whose organisms it reuses has already run most of this experiment, and their results are public on Hugging Face, though without a write-up.

What I checked on 2026-11-14:
- **Papers:** arXiv 2603.05706, 2610.23257, 2610.40939, 2505.23575 and 2605.15257 exist with the stated titles.
- **Artefacts:** `latentMO/cotcontrol-gptoss120b-grpo3` is public, with `main` at step 100 and branches step20 to step80. `latentMO/cotcontrol-selfinstruct-opsd` contains `code/rl/grpo.py`, the graders and the CoT-Control CSVs. `latentMO/cot-red-handed-runs` contains base logs and `local_changes.patch`. The Lundqvist and ejcgan repos are public.
- **Prices:** Tinker gpt-oss-120b is 0.33 / 0.84 / 0.737 per million tokens, and OpenRouter gpt-4.1-mini is 0.40 / 1.60, as stated.
- **Not checked:** GitHub repo contents, and whether the `tinker://` checkpoints load from a third-party account. My web search budget was exhausted, so the prior-work search covered Hugging Face, arXiv and the LessWrong new-posts feed only. A LessWrong or Alignment Forum write-up by the latentMO team could exist that I did not find.

## 1. Would it get upvoted?

Conditionally. The cluster's posts earned 72 to 78 karma, and "does the number matter for evasion" is the question METR, OpenAI and Van Deventer et al. all name as open. A clean causal answer on one model with controls would plausibly earn 50 to 100 karma. Readers would be the CoT-monitorability crowd and people who write or read system cards.

Two things cut that estimate:
- **Scoop.** The latentMO sprint has the result in hand (see section 2). If they post first, this becomes a replication by an outside agent team with a fraction of their arms, likely 20 to 40 karma. Their last upload was 2026-10-31, to a dataset called `mats12-slide-figures`, so a post is probably imminent.
- **The positive headline is close to tautological.** The organism was trained with RL to obey instructions about its CoT, including suppression rules. "Do not reveal that you used the hint" is an instruction about the CoT. Readers will ask what else anyone expected. The non-obvious results are spontaneous changes without an evasion instruction, effects on a realistic side task, and the comparison with the control. The proposal does not centre those.

## 2. Naturalness, and has it been done?

It is the mainline follow-up. Nobody would call it contrived.

It has largely been done, unpublished. The proposal says "The latentMO team has released base-model CoT Red-Handed logs but no organism results". That is false as of today:

- **Hint verbalization figure.** `latentMO/mats12-slide-figures/hint_verbalization.png` (uploaded 2026-10-31) shows hint verbalization with Chen et al. hints, judged by Haiku 5.5, for base gpt-oss-120b, grpo3 step 100 and manytypes1b step 150. Among answers that switched to the hint, the CoT verbalizes it in 371/405 (92%) for base, 191/253 (75%) for grpo3-s100 and 35/165 (21%) for manytypes1b-s150. This is the proposal's task A, on the proposal's organism, with a positive dose-response across three points.
- **Hint following falls too.** The same figure shows the share of answers switching to the hint: 405/1065 for base, 253/1083 for grpo3 and 165/1071 for manytypes1b. This matters for the proposal's joint outcome metric (section 3).
- **Monitoring-instruction conditions.** `latentMO/faithfulness-traces-20261026` holds 2,486 files, with `hintverb` results under conditions named `neutral`, `auto_monitor`, `user_reads`, `cot_private` and `answer_checked`, plus `sandbag/.../evasion.eval` runs.
- **Length adjustment.** `len_oversight_gptoss.png` shows a length-adjusted analysis of 15 oversight-line wordings on base, grpo3 and two manytypes organisms. The proposal's analysis (iii) is therefore also done.
- **Stronger organisms and controls.** `manytypes1b` is public (12 control types, mention of the instruction fails the rollout, +72 points strict on 540 items). So are `nocotrl1` (output-only RL with the CoT off, +11.6 points at matched length), `outrl1`, `rlen1` and the `spill*` runs. The proposal uses only grpo3, which is the weakest of these.

What I could not find from that team is organism results on CoT Red-Handed. Only base logs are on Hugging Face, but about 90 adapters and an `arena-*` line exist whose results are undocumented. Assume they have it or will within days.

## 3. Pre-mortem

How the two days likely go:

- **Day 1, loading.** The `tinker://` path may not load. Other latentMO cards say paths are "now deleted from Tinker", and the proposer did not verify that a third-party adapter can be uploaded. The adapters train attention, MLP and unembedding, so serving them outside Tinker means a 120B MoE with LoRA on a rented 80GB+ GPU. That is fragile and unbudgeted. Most likely the team retrains.
- **Day 1, retraining.** A retrained organism is a different organism. grpo3 was the third attempt and the repo has five "smoke" runs, so reproducing 72/108 in one shot is perhaps 60% likely. A weaker result (say 40/108) is still usable.
- **The accuracy-only control will be a near no-op.** GRPO with reward equal to accuracy on mined MMLU-Pro items the base model mostly answers correctly has little advantage signal. The adapter barely moves and CoT length does not shorten. It then fails at its stated purpose, which is separating control from "RL-trained and writes shorter CoTs". A reviewer will say the control controls for nothing.
- **Task A.** It will run and likely show the organism concealing more under instruction, matching the slide figure. But hint following drops in the organisms (38% to 23% pooled), so the proposed joint outcome, P(follows hint and not flagged), may stay flat or fall while conditional verbalization falls. The proposal's headline metric and the natural reading can disagree.
- **Task B.** The harness is Docker plus Inspect plus a patch against a specific upstream commit. The latentMO repo keeps `monitor-errored` and `errored-high` directories, so they hit failures too. Catch rate is conditional on completing both tasks. If main-and-side success is 20 to 35% of 855, each arm has roughly 170 to 300 transcripts, giving a confidence interval near plus or minus 6 to 7 points per arm and worse for differences. The proposal's "about 4 points" is optimistic. Dolev's whole effect was 5 to 9 points.
- **Dose ladder.** Eight arms where five are checkpoints of one run is one trajectory, not five independent doses. A regression across them overstates the evidence.
- **Monitor mismatch.** The proposal says "monitors as in the benchmark (gpt-4.1-mini)", but the base logs it wants to reproduce used gpt-5-nano and Haiku 5.5. "Reproduce latentMO base numbers" needs their monitor, not the benchmark's.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (organism conceals more under instruction, beyond control) | 35% |
| Clear negative that is still interesting | 10% |
| Ambiguous mush (task A positive but length- and propensity-confounded, task B underpowered or broken, control uninformative) | 40% |
| Fails to run usefully | 15% |

Separately, I put about 50% on the latentMO write-up appearing before or within two weeks of this one, which would turn even the clear positive into a replication.

## 4. Cost check

The prices are right and the token arithmetic is plausible. My estimate for the plan as written is $350 to $480, under the cap but with thin margin for a GRPO rerun.

- **Monitor spend ($98) is overstated.** Task A transcripts are far shorter than 5k tokens.
- **Debugging is not budgeted.** There are no smoke runs, failed Red-Handed shards or re-sampling in the estimate.
- **Fallback GPU is not budgeted.** If Tinker cannot load the adapter, serving it elsewhere costs money the estimate omits.

The overhauled version below costs roughly $200 to $300.

## 5. Recommended changes

1. **Correct the novelty claim and build on the latentMO releases.** Before spending anything, download `latentMO/faithfulness-traces-20261026` and `mats12-slide-figures` and establish what is already answered: hint verbalization, monitoring-line conditions, length adjustment, sandbagging evasion. This costs $0 and takes half a day. Frame the project as an independent replication plus the missing pieces. Do not present it as the first causal test.
2. **Make CoT Red-Handed on the organisms the core.** It is the one piece with no visible prior result. Run base, grpo3-s100, manytypes1b-s150 and one control on the benchmark with the baseline and stealth attacks. Use the latentMO monitors (gpt-5-nano and Haiku 5.5) so their base logs serve as a free, checkable baseline. Report main-and-side success alongside catch rate, and pre-specify the unconditional metric P(side task done and not caught) so a collapse in side-task success cannot masquerade as evasion.
3. **Replace the accuracy-only control with public controls.** Use `rlen1` (response-length RL, if its diary confirms that), `nocotrl1` (output-only RL) or `outrl1`. If one must be trained, reward accuracy plus a CoT-length target matched to the organism's distribution, so it controls for the short-CoT confound.
4. **Use manytypes1b as the high dose and drop the 5-checkpoint ladder.** Three or four distinct organisms (base, nocotrl1, grpo3, manytypes1b) spanning roughly 9% to 74% strict compliance are better evidence than five checkpoints of one run. This removes the retraining gate if the HF adapters or `tinker_provenance.json` paths load. Spend the first two hours testing that, and write down the fallback explicitly.
5. **Separate instructed from uninstructed evasion and lead with the uninstructed one.** The slide data suggest verbalization falls even without a concealment instruction. That is the surprising and safety-relevant claim: training for control degrades monitorability as a side effect. Instructed concealment rising in a model trained to obey CoT instructions is expected.
6. **Fix the task A metric.** Report three numbers separately: P(switch to hint), P(verbalize | switch) and P(monitor flags | switch). The organisms change the first one, so the joint metric alone will mislead.
7. **Recompute power.** State the expected number of transcripts per arm on Red-Handed after conditioning, and what difference is detectable. If it is above 8 points, add a second sample per task instead of extra arms.
8. **If the organisers want a project with no scoop exposure, fund proposal 02 from this cluster instead** (unprompted early exit). It does not depend on another team's unpublished pipeline. I would fund this proposal only in the overhauled form above, at about $250.
