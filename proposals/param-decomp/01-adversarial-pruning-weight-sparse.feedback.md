# Feedback: "Does adversarial masking fix unfaithful weight-sparse circuits?"

Reviewer verdict: **keep with tweaks.** It is a mainline follow-up on fully public artefacts, and I found no sign it has been done. The plan has one design flaw that can make its headline test uninformative (section 3, item 1), omits two parts of the existing pipeline that must change, and underestimates compute by about 2-3x (still well under $500).

What I checked, and what I could not:
- **Prior-work claims: accurate.** I read Drori's post in full. The numbers in the proposal match: ~30 nodes for the nonsense task at CE < 0.05 vs ~10 for pronouns; the L1H7 uniform-attention circuit; d=3072 at 89% opposite-gender and 0.81 same-gender; 100 seeds with 77 passing CE < 0.15; the spike at 0. Lucius Bushnaq's comment (27 karma) says what the proposal says, including "you also don't need to freeze layer norms" and the one-ablation-pattern-per-batch restriction. arXiv 2610.20748 is the VPD paper and 2511.13653 is Gao et al.
- **Artefacts: public.** All four HF checkpoints and the dataset are public and ungated (`sparse_model.bin`, `config.json` present). Raw GitHub files fetch with HTTP 200: `src/pruning/config.py`, `masked_model.py`, `tasks.py`, `run_pruning.py`, `trainer.py`, `node_mask.py`, `scripts/run_carbs_sweep.py`. `tasks.py` contains `DummyPronounIsWhenTask`, `IOIStrictTask`, `IOIRelaxedTask` and `IOIMixedTask`.
- **Already done? Not found, but the check is incomplete.** WebSearch was unavailable to me as well (budget exhausted), so the proposer's coverage caveat stands. arXiv API queries on weight-sparse circuits return only Gao et al., 2607.02964, and 2607.18921. Drori has published no follow-up (his later posts are on other topics); the post's only pingback is a CLT-unfaithfulness post that predates it; none of its 5 comments reports an implementation.
- **One paper the proposal should cite:** arXiv 2607.18921 (Sheng & Fu, "Circuit Claims Depend on What Is Extracted and How It Is Compared"). It compares extraction choices, including a post-ablation loss budget, on dense and weight-sparse checkpoints in a Lean tactic benchmark. It is not adversarial masking and not Drori's test bed, so it does not scoop this.
- **Not verified:** RunPod prices (the pricing page did not parse through curl), and whether Drori's tuned per-task pruning hyperparameters are anywhere in the repo (the GitHub tree API is blocked, so I could only probe guessed paths).

## 1. Would it get upvoted?

Borderline-to-yes, depending on outcome. Reference points from the cluster:

| Post | Karma |
|---|---|
| Drori, weight-sparse circuits unfaithful | 140 |
| VPD linkpost | 164 |
| Lange, CLTs incentivised to learn unfaithful circuits | 47 |
| Angsten, first VPD audit | 29 |

Third-party audits and follow-ups by non-authors land at 29-47, not 140. To clear 50, the post needs one crisp picture: Drori's same-gender histogram redrawn with the spike gone (or not), next to a circuit-size-vs-faithfulness Pareto showing whether sparse models keep their advantage. With that, I put it at 60-100 karma. Leo Gao, Lucius Bushnaq/Goodfire and Drori all have a stake and would likely engage. The neuron-basis vs learned-basis argument is live (Gao's October post has 368 karma), which helps. A result of "depends on the model, the fix is partial, circuits are somewhat bigger" lands at 25-45. Overall chance of more than 50 karma given successful execution: about 45-50%.

## 2. Naturalness

Mainline. Drori's stated next steps are (1) a faithfulness metric, (2) a pruning algorithm that satisfies it, (3) a re-check of sparse vs dense. Lucius's comment supplies a candidate for (2), and the VPD paper footnotes this exact post when generalising its claim. Nobody has reported doing it in nine months. The risk is that Goodfire or Drori's mentors have done it privately; nothing public suggests so.

## 3. Pre-mortem

Forecast:
- Clear positive (spike gone, circuits modestly larger, sparse advantage survives): **20%**
- Clear, interesting negative (circuits balloon or failures persist, with a clean explanation): **25%**
- Ambiguous mush: **40%**
- Fails to run or to reproduce the baseline: **15%**

Reasons it produces mush, most important first:

1. **The adversary may not penalise the "bad" IOI circuit, for a reason that says nothing about adversarial masking.** On opposite-gender prompts, "copy gender of name 1" and "opposite gender of name 2" give the same answer. If the adversary restores the model's real name-1 pathway on top of a bad-rule circuit, the output stays correct and the KL barely moves. The bad rule may also be a real sub-mechanism of the model that another pathway overrides on same-gender prompts. Then a circuit that is perfectly robust on the pruning distribution can still be the bad circuit. If test 3a fails, the proposal reads that as "contradicts a stated claim of the VPD paper". That inference does not follow: the pruning distribution underdetermines the circuit, and VPD prunes per prompt against the model's full output. As written, the headline test has no clean interpretation in the negative direction.

2. **A fixed neuron-basis model is not trained to tolerate ablation.** VPD's adversarial pruning works on a decomposition optimised so that non-causally-important components can be ablated. Here there is no such guarantee. Drori's layernorm appendix already says many nodes each write a little to the correct direction. With roughly 50k maskable nodes per model (8 mask locations x 2 layers) and continuous r, a PGD adversary will probably find off-circuit nodes whose partial ablation moves the output. Circuits may then grow 10-100x. That is a publishable negative only if "the adversary is unreasonably strong" can be separated from "the small circuits were fake". The proposal has no calibration for this, such as how much KL the same adversary induces when the circuit is a random superset of matched size, or the whole model minus a few nodes.

3. **"KL to model" is underspecified, and the choice drives circuit size.** Drori's IOI uses binary CE over him/her; his pronoun task uses full-vocabulary CE. Full-vocabulary KL at the answer position makes the circuit reproduce the whole next-token distribution, which inflates circuits for reasons unrelated to the adversary. KL over the restricted {correct, incorrect} softmax is close to the original task. C1 vs C0 will differ a lot depending on which is used, and the dense model's 0.81 soft target changes what "within 0.1 of 0.81" means.

4. **Two pipeline stages are missing from the plan.** `config.py` and `scripts/run_carbs_sweep.py` show that the reported circuit size is not the raw learned mask. It comes from a bisection over top-k nodes to hit `target_loss` (`discretization_max_iters: 50`), followed by LBFGS logit calibration (`calibration_steps: 16`). Under the S and A arms, both must be redefined: bisection against the adversarial loss needs a PGD inner loop at every bisection step, and calibration lets the circuit rescale logits, which interacts with a KL target. The "200 lines changing the forward pass and loss" estimate ignores this, and it is the most likely place for a subtle evaluation bug.

5. **Baseline reproduction is uncertain.** The 100-seed histogram used per-(model, task) hyperparameters from a CARBS sweep. The sweep script is public; I could not confirm the winning configurations are. Drori himself warns that the d=1024 vs d=3072 difference may be hyperparameter luck. If the team's own C0 sweep gives a weaker spike (say 20% of seeds at 0 rather than a big spike), 40 seeds per arm cannot show a convincing reduction. The post does not state which ablation type (zero vs pretraining mean) or which IOI class (`IOIRelaxedTask`, presumably) produced the histogram.

6. **Too many arms for two days.** 5-7 schemes x 2 ablation values (the proposal leaves "zero or pretraining mean" open) x 2-4 models x 3 tasks, a 20-config search per cell, four battery tests, three held-out metrics, and a Pareto re-check. The agents will finish a subset, and the selection will be post hoc.

7. **Tests 3b and 3c are weakly defined.** Under S and A, non-circuit nodes are no longer fully ablated during training, so query/key nodes may still be absent, and uniform attention under complete ablation may persist. 3b then measures whichever evaluation mask is chosen. 3c (activation correlation under full ablation) has an arbitrary 0.5 threshold and no reference distribution.

8. **Selection criterion favours whatever the criterion measures.** Hyperparameters are selected by "circuit size at a fixed KL budget". For the A arms that KL is adversarial, for C1 it is not, so the arms are tuned to different targets. The comparison is fair only on the held-out metrics, which should be stated as the sole basis for cross-arm claims.

## 4. Cost check

Underestimated, but safely under the cap.

- "Adversarial runs cost about (k+2)x" and "~6 min average" are inconsistent. In C0-run units the battery arms cost roughly 1 (C0), 1 (C1), 2 (S), 3 (A k=1), 7 (k=5), 22 (k=20), 7 (A+LN): about 43 units per seed per model. At 2 minutes per unit, x 2 models x 40 seeds = ~115 GPU-h, against the 56 claimed.
- Sweeps over the A arms have the same multiplier, and adversarial discretization adds more. The held-out evaluation adversary (100 PGD steps, per-example r) on roughly 600 circuits is not negligible.
- The 1-3 minute C0 assumption is unmeasured. The d=3072 model has ~38M-entry MLP matrices stored dense; the sweep script uses bfloat16 autocast. 2-5 minutes on an A40 is plausible.

My estimate: 250-350 GPU-h as designed, about $150-210 at the quoted (unverified) A40 rate, or **$250-350 with a rerun margin**. Trimmed as recommended below: about 120 GPU-h, **~$150 including margin**. Wall-clock is the tighter constraint: 300 GPU-h in two days needs 6-8 GPUs or several runs packed per card, which the models are small enough to allow.

## 5. Recommended changes (most important first)

1. **Fix the IOI test's interpretation before running it.** Add two arms: (i) prune with the adversary on `IOIMixedTask` (same- and opposite-gender), as an upper bound; (ii) prune on opposite-gender only but with the KL computed at all sequence positions, or on a mix of task and pretraining text, so the adversary has a way to expose the name-1 pathway. Pre-register the reading: "adversary fixes generalisation from opposite-gender-only pruning" is the strong claim; "adversary does not, but the circuit is robust on-distribution" is a statement about distribution underdetermination, not a refutation of VPD. Remove the "contradicts a stated claim of the VPD paper" language unless the on-distribution held-out adversary also breaks the circuits.

2. **Use persistent PGD as the main adversarial arm.** Keep the adversary's r as a persistent parameter updated one ascent step per pruning step, as VPD does, instead of k fresh steps per step. Cost drops to about 2-3x C0, and it matches the method whose claim is being tested. Keep one fresh k=5 arm as a check; drop k=20.

3. **Calibrate adversary strength.** For each model and task, report the adversarial KL for (a) the full model minus N random nodes and (b) random supersets of the C0 circuit at matched sizes. Without this, "circuits swell" cannot be told apart from "this adversary breaks anything".

4. **Specify the objective.** Primary: KL over the restricted {correct, incorrect} softmax for IOI, matching Drori's binary loss. Secondary: full-vocabulary KL at the answer position. State how discretization (bisection run against the adversarial loss, with a fixed small PGD budget) and logit calibration (recommend disabling it for all KL arms) are handled.

5. **Cut scope to one sharp experiment.** d=3072 IOI first (the published failure), then d=1024 IOI; pretraining-mean ablation only (Gao et al.'s choice), with zero ablation as a single robustness check. Arms: C0, C1, S, persistent-A, persistent-A + frozen LN. Drop the questions task. Do the dense-vs-sparse Pareto on one task (pronoun) only after the battery is done. Treat attention recovery and node-role agreement as secondary descriptive plots.

6. **Harden the day-1 gate.** Define "reproduced" numerically, for example at least 30% of passing C0 seeds with same-gender P_correct < 0.2 on d=3072. If the spike does not reproduce after one C0 sweep, pivot to the on-distribution question (held-out-adversary KL and resample-ablation KL of C0 vs A circuits at matched size), which needs no reproduction of the histogram.

7. **Raise seeds on the headline cell.** 100 seeds for C0 and persistent-A on d=3072 IOI, to match Drori's figure; this is cheap once k=20 is gone. Report per-prompt agreement with the model's same-gender predictions as well as mean P_correct.

8. **Make cross-arm claims only on held-out metrics.** Say so explicitly. Cite arXiv 2607.18921 as adjacent work.

9. **Budget line: revise to about $250.** That covers the trimmed design with a 2x margin, plus the unverified GPU prices.
