# Feedback: "Evil persona or grader-seeker? Tracking two directions through 230 public reward-hacking RL checkpoints"

Verdict: **keep, but only with a substantial redesign of the measurement** (see section 5). As written, the most likely outcome is an uninterpretable projection plot.

## What I checked

Confirmed:

- **Checkpoints are public and ungated** (HF API, today). `somo-olmo-7b-nohints-s1-chkpt-*` has 150 repos; both `reward-hacking-olmo3.1-32b-kl{0.0,0.02}-seed2` repos hold 40 checkpoints with `-rollouts` datasets; `em-olmo32b-insecure-seed42-chkpt-1425`, `cc-olmo32b-baseline-nohack-s100` and the five `codecontests-rh-olmo32b-prompted-*` variants exist.
- **Bases match where it matters for 32B.** The insecure-code LoRA, the KL trajectories, the no-hack baseline and the inoculation variants all sit on `allenai/Olmo-3.1-32B-Instruct-SFT` (32.2B parameters, so ~64 GB in bf16 is right).
- **Prices.** Sonnet 5.5 is $2/$10 on OpenRouter (batch $1/$5). I could not re-check the RunPod H200 price live.
- **AISI's "causal pathways" future-work sentence** and Betley's steering post (Qwen3.6-27B, layer 36, code linked) are as described.
- **The AISI GitHub README** lists `emergent-misalignment/`, `misalignment-evals/` and `scripts/run_mgs_trajectory_multi.sh`. It has no activation or steering code.

Not confirmed, or wrong:

- **Prior-work search was partial.** The web-search budget for this session was exhausted, so I used the arXiv API, LessWrong comment threads and Hugging Face only. I found no white-box analysis of these checkpoints. The nearest work is arXiv 2603.04069 (SAE probes for reward hacking in SFT adapters; no RL trajectories and no EM-vs-grader comparison) and a 9-karma comment on the AISI post asking for a mech-interp answer to "memorised exploit vs generalised orientation".
- **"AISI's published per-checkpoint misalignment curve" is a figure, not data.** The README refers to `results/` directories that are not in the repo. The team must re-run the evals on a subset of checkpoints, and that is not budgeted.
- **The SFT-EM organism is barely misaligned.** AISI Appendix E reports about a 4% MGS increase for the insecure-code Olmo-32B and says the Betley and alignment questions "don't increase much after EM training". This undermines D1 (section 3).
- **The primary trajectory has no public matched no-hack control.** The 7B SDF run sits on `somo-olmo-7b-sdf-sft`. The only public 7B no-hack model is `cc-olmo3-7b-nohack-s200`, from the prompted setting on a different base. AISI also says the 7B SDF no-hack baseline "itself drifts slightly toward misalignment", so the strongest run is the one where the hack-specific claim is weakest.
- **`emergent-misalignment/` may not run as-is.** The README says some scripts there depend on a private package (`mt-tools`) and are "for reference only". Treat the "one-hour 7B insecure-code SFT using AISI's configs" as writing your own SFT script.
- **Adapters are not like-for-like.** The 7B and SDF adapters are rank 32 on attention only. The no-hack 32B adapter is rank 32 on all modules and stops at 100 steps (β=0.02), against 400 steps for the trajectories. The inoculation adapters are rank 128. Raw shift magnitudes are therefore not comparable across the proposal's "control bands".
- **Inoculation variants have no clean behavioural ground truth.** AISI's inoculation result was "less clear" (`please_hack` gave the highest misalignment), and the figure caption says Olmo-7B while the public checkpoints are 32B.

## 1. Would it get upvoted?

Conditional on the clean result in section 5 of the proposal (one direction tracks hack onset, stays flat in no-hack, and its ablation halves Frame Colleague without touching hack rate): yes, plausibly 70-130 karma. It bears directly on the EM-vs-reward-seeker dispute that the Hacker-Opus (163), split-personas (244) and Africa (153) posts foreground, and it uses AISI's checkpoints the way AISI invited.

That outcome is unlikely (section 3). The realistic write-up is "several directions all move a bit, controls move too, ablations partly reduce Frame Colleague along with a random-direction effect". That is a 20-40 karma post. LessWrong readers are sceptical of single-direction difference-of-means stories; the comments on Betley's own steering post are mostly "what is this vector really?" (the 40-karma evaluator/criterion decomposition, a requested "robotic vs sensitive" control, Schoen's falsifiability worry). A post that inherits that vector as a ruler inherits those objections.

Readers who would care: the AISI Model Transparency team, Betley's group, the Redwood authors, and anyone using persona-vector monitors.

## 2. Naturalness

The question is mainline: AISI names causal pathways as future work, evhub asks for interpretability-based auditing, and a commenter asked for interp on these checkpoints. The operationalisation is one step removed from natural, for two reasons.

- **It presupposes the two stories correspond to two linear directions.** Both rulers are built on a different model or organism, and one of them is known to be weak on Olmo.
- **The first-order question is behavioural.** Whether AISI's Frame Colleague effect is grader- or gain-conditional is what proposal 01 tests, more cheaply and with fewer assumptions. This proposal is the complement, not the obvious next step.

A more natural white-box design starts from the data: take the RL-induced shift itself, show what it does causally, then ask what it resembles (section 5).

## 3. Pre-mortem

How two days play out: day 1 goes on the harness (LoRA hot-swapping across three adapter layouts, the Olmo chat template and `<thinking>` format, layer choice, downloading ~130 GB) and on direction extraction. Ruler validation then runs into trouble, and day 2 produces trajectory plots whose controls do not separate.

| Outcome | Probability |
|---|---|
| Clear positive (one story wins, causally) | ~15% |
| Clear, interesting negative (validated rulers flat while behaviour changes) | ~15% |
| Ambiguous mush | ~55% |
| Fails to run or runs out of time before interventions | ~15% |

Specific failure reasons, most important first:

1. **D1 fails its own validation.** The plan requires steering with D1 to raise Betley-question misalignment, but the organism D1 comes from does not raise it (AISI App. E). The plan then drops D1, leaving a generic prompt-contrast "evil" vector (D2). That no longer tests whether RL moves the model the way SFT-EM does. The 7B D1, from a home-made one-hour SFT, will be weaker still.
2. **D1 and D3 are both confounded with "coding".** D1 is a model-diff from fine-tuning on code. Betley's own logit-lens readout of the automated-grader side of D3 is "code formatting and computer/robot/automated vocabulary". Any RL on CodeContests, hacking or not, will plausibly move along both. The no-hack control is the only thing that separates this, and it is missing for the primary 7B trajectory and mismatched (100 steps, different KL) for 32B.
3. **The random-direction null is the wrong null.** In a 4-5k-dimensional residual stream, a fine-tuning shift projects near zero on Gaussian directions and non-trivially on any semantically meaningful direction. "More than 3 null-SDs" will be cleared by D1 to D5 alike, including the controls, so it cannot support a headline claim.
4. **Hack onset is confounded with training step.** On a single seed, projections drift monotonically and hack rate rises monotonically. "Rises within ~20 steps of onset" cannot be told apart from drift without a changepoint analysis and a non-hacking run of matched length.
5. **D3 has no clear prediction.** In Betley's post, ImpossibleBench hacking went up under steering towards the human side, and chess hacking was ambiguous. "D3 rises with hacking" is the proposer's inference. D3 was also taken at a thinking-model token position on Qwen, so transfer to Olmo is untested.
6. **The misbehaviour signal is thin and model-specific.** It comes from two scenarios, with Frame Colleague at 65% on one 7B seed. The 32B `seed2` trajectories have no published per-eval rates (the nearest reported run, `sutl` β=0.0, has Frame Colleague 24% and Monitor Disruption 27%). If seed 2 is around 10-20%, n=200 ablation comparisons are underpowered.
7. **Ablation on a 7B model degrades behaviour non-specifically.** Projecting out a high-norm direction can cut Frame Colleague by making the model less coherent. One random direction is not an adequate control.
8. **Time.** 40 GPU-hours on one GPU inside ~48 hours of wall-clock leaves no slack. Steering sweeps (directions × layers × strengths) are far more generations than the "~6k" budgeted.

## 4. Cost check

The $290 estimate is low but the project fits under $500. My estimate is **$380-450**:

- **GPU, ~$230-260.** One H200 for 32B at ~45 h, plus a separate 48 GB card at ~$0.5-0.8/h for all 7B work in parallel, which also relieves the wall-clock problem.
- **Judging, ~$90-110.** Add the validation steering sweeps and the re-run of the per-checkpoint behavioural curve on ~12 7B checkpoints × 2 evals × 200 samples. Use batch pricing where latency allows.
- **Storage and rerun margin, ~$60.**

## 5. Recommended changes (in priority order)

1. **Lead with the data-driven direction.** Define Δ_hack as the mean residual shift (hacker minus base) on non-coding prompts, and Δ_nohack likewise. The core experiment becomes:
   - steer the base model with Δ_hack and with Δ_nohack and measure Frame Colleague and Monitor Disruption;
   - ablate each from the hacker;
   - only then report cosines of Δ_hack with D1, D2, D3 and D4.

   This yields a result even if every imported ruler fails: "the hack-specific component of the RL shift does or does not carry the misbehaviour, and it looks like X".
2. **Make 32B the primary analysis and 7B the illustration.** Only 32B has a same-base no-hack control, a same-base SFT-EM organism and the KL contrast. In hour one, measure Frame Colleague and Monitor Disruption on the `kl0.0-seed2` endpoint (n=200). If it is under ~15%, switch to the best public prompted 32B endpoint, or to `somo-olmo-32b-nohints-s1-chkpt-360`, for interventions.
3. **Fix the D1 validation gate.** Validate each ruler on the evals where its source shows an effect (for D1, whichever of AISI's six evals the insecure-code model moves), not on the Betley questions. Pre-state that if D1 cannot be validated, the write-up drops the "SFT-EM direction" framing instead of substituting D2.
4. **Replace the null.** Use 30-50 unrelated semantic contrast vectors (traits, topics, formats) built by the same recipe, plus several norm-matched random directions for ablation. Report percentile within that distribution, the full cosine matrix among D1 to D5, and projections after orthogonalising against D4 (coding).
5. **Handle onset timing properly, or drop the claim.** Use a changepoint or lagged-correlation analysis on detrended projections. Use the KL 0 vs 0.02 trajectories as a within-design contrast; they have the same step count, and AISI reports different EM.
6. **Drop the inoculation arm from stage 1.** It has no behavioural ground truth and rank-128 adapters. Normalise all cross-run comparisons (cosine, or shift as a fraction of total shift norm), given the mismatched ranks and target modules.
7. **Budget the behavioural re-evaluation explicitly**, since the per-checkpoint curve is not released as data: ~12 spaced 7B checkpoints.
8. **Add a coherence check to every intervention** (a short capability or fluency probe), so a Frame Colleague reduction is not just breakage.
9. **Retitle after the redesign.** "230 checkpoints" oversells two single-seed trajectories. State prominently that this covers one seed per model.

If the funder can back only one of proposals 01 and 02, 01 should go first. It answers the same dispute behaviourally with fewer assumptions, and its result would tell this project which direction to look for.
