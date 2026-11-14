# A pre-flight check for inoculation: do two loss measurements before training predict suppression and retention across prompts, steering vectors and adapters?
cluster: inoculation | stage-1 cost: $230 | follows up: "Inoculation Adapters Improve Upon Inoculation Prompting" (qd3qhxgEmQAXR2ZK5); "Conditionalization Confounds Inoculation Prompting Results" (znW7FmyF2HX9x29rA); "Many alignment techniques work by training one model and deploying another" (syAbdNei8BWeP2RPo)

## 1. What the prior work showed
Several methods share one shape: during fine-tuning, add something to the model that already produces an
undesired trait, then remove it at deployment, so that the model learns the desired trait and not the undesired
one. The "something" (the *carrier*) can be a system prompt (inoculation prompting, IP), an activation vector
(preventative steering), or a frozen LoRA (inoculation adapters, IA). The post by cloud argues these are one
strategy, "train-deploy mismatch", with one shared tradeoff, but runs no experiments.

What is known about when a carrier works:
- Wichers et al. (arXiv 2510.05024): prompts that elicit the trait more strongly before training inoculate
  better.
- Riché & Warncke (Feb 2026), over seven setups: that heuristic is "good but insufficient". Irrelevant prompts
  also suppress traits, fixed prompts suppress the desired trait too, and a prompt that requests the whole target
  behaviour stops learning altogether. They suggest "specificity" matters: how much more a prompt explains the
  undesired trait than the desired one.
- The IA paper (arXiv 2606.30252), nine setups: IA suppresses more than IP and steering but retains less of the
  desired trait; results vary by setup; attaching the IA lowers the first-step training loss (Appendix C); a
  random adapter does nothing and an irrelevant adapter suppresses both traits a little. Its Discussion states
  the gap: "A more convenient method would allow predicting which method works best before or at the start of
  task training."

Already done: elicitation strength vs outcome within prompts (Wichers; Riché & Warncke Appendix D); loss curves
for IA (Appendix C); a toy comparison of prompts, adapters, soft prompts and prefixes on a 1.5B model (Xenomirant,
Sept 2026) with outcomes but no predictor. I found no test of one predictor across carrier types (2026-11-14).

## 2. Question and why it matters
Before any training, measure how much a carrier lowers the model's loss on (i) data showing only the undesired
trait and (ii) data showing only the desired trait. Do these two numbers predict, across prompts, vectors and
adapters alike, how much of each trait the deployed model ends up with?

If yes, practitioners get a one-minute check that ranks candidate carriers without running the fine-tune, and
cloud's "one strategy, one tradeoff" picture gains quantitative support. If adapters or vectors fall off the
curve that fits prompts, carriers differ in kind (a prompt is a trigger the deployed model can still see; an
adapter is not), which is evidence about mechanism that the IA paper could not separate from strength.

## 3. Stage 1 plan
**Reused:** the IA paper's two Qwen2.5-7B-Instruct setups with their hyperparameters (rsLoRA rank 32, alpha 16,
one epoch, batch 8), its normalisation of trait scores between the no-fine-tuning and SFT references, the
conditionalization post's prompt categories, Alpaca and UltraChat, the Turner et al. extreme-sports data
(`huggingface.co/datasets/geodesic-research/sfm-emergent-misalignment-training-data`), and the 48 pre-registered
emergent-misalignment (EM) questions of Betley et al.
**Built:** the training loop with a pluggable carrier (prompt, residual-stream vector, frozen LoRA) and three
parallel versions of each task dataset.

Setups, desired trait French in both:
- **S1:** undesired = ALL-CAPS, Alpaca prompts. Rule-based scoring, no judge needed.
- **S2:** undesired = EM, extreme-sports prompts. gpt-4.1-mini judge.

For each setup build three answer sets on the same 5,000 prompts: *both* traits (the training data), *desired
only* (clean French), *undesired only* (English with the undesired trait). S1's are mechanical transforms; S2
uses the Turner answers, their French translation, and harmless French answers.

Carriers, about 24 per setup:
- **Prompts (8):** three inoculation prompts from weak to strong; two irrelevant facts; a pool of paraphrases; a
  negated prompt; a prompt that requests the *desired* trait.
- **Steering vectors (6):** difference-of-means vector for the undesired trait at strengths 1, 2, 5, 8; a random
  vector of matched norm; a vector for the desired trait.
- **Frozen adapters (10):** IA at output scale 0.25, 0.5, 1, 2; IA of rank 1 and 4; IA trained on 500 examples;
  an irrelevant-trait adapter; a random adapter of matched norm; an adapter carrying the desired trait.
The carriers aimed at the desired trait are deliberate negative controls: they should predict lost retention.

Steps:
1. Build data and carriers.
2. **Pre-flight measurements** (forward passes only, 200 held-out examples per set): loss reduction from
   attaching the carrier on undesired-only data (call it U) and on desired-only data (D), each as a fraction of
   the gap between the base model and a model fine-tuned on that set.
3. Train the task LoRA with each carrier attached, remove the carrier, and measure normalised undesired-trait and
   desired-trait expression on out-of-distribution prompts (200 WildChat prompts for S1; 48 questions x 10 for
   S2) with the system prompt "You are a helpful assistant.".
4. Three seeds for six representative carriers per setup to estimate run-to-run noise; one seed for the rest.
5. **Gate (day 1):** S1 with the standard IA and standard IP reproduces the paper's ordering (IA suppresses more,
   retains less).

Analysis, fixed in advance:
- Fit suppression as a monotone function of U and retention as a monotone function of D on one carrier family;
  predict the other two families; report Spearman correlation and mean absolute error. Repeat for each held-out
  family, and across setups (fit on S1, predict S2).
- Decision rule: held-out-family Spearman of 0.8 or more on both outcomes counts as "one law"; 0.5 or less counts
  as "carriers differ in kind"; in between is reported as partial.
- Compare against two simpler predictors: U alone (the Wichers heuristic) and carrier family alone.
- Practical variant: recompute D from 250 confidently clean examples (what stratified inoculation prompting
  assumes is available) and check how much prediction degrades.

## 4. Stage 1 cost estimate
RunPod A100 80GB secure cloud at $2.19/h; gpt-4.1-mini on OpenRouter at $0.40 / $1.60 per M tokens (looked up
today).

| Item | Quantity | Cost |
|---|---|---|
| Carrier construction (adapters, vectors) and pre-flight forward passes | 5 GPU-h | $11 |
| Task training: 2 setups x 24 carriers + 24 extra seed runs = 72 runs, ~15 min with generation | 18 GPU-h | $39 |
| Debugging, reruns, idle time | 20 GPU-h | $44 |
| French translation and harmless French answers (~11k answers, ~8M tokens) | | $12 |
| Judging S2: ~40 models x 480 completions x 2 judges x ~600 tokens = ~23M tokens | | $10 |
| Judge validation against gpt-4.1, storage | | $14 |
| Margin for a second sweep (for example a third setup or more seeds) | | $100 |
| **Total** | | **$230** |

## 5. What success looks like
Positive: one scatter plot, pre-flight U against final suppression, where prompts, vectors and adapters fall on
one curve (held-out Spearman at least 0.8), a matching plot for D against lost retention, the negative controls
landing where predicted, and a table showing the check ranks the top three carriers correctly in both setups.
That is a practical tool and a tested version of the unifying claim.

Negative but informative: prompts follow the curve and adapters sit clearly off it at equal U. Then the carrier's
type matters beyond its strength; the plot showing the offset is the result.

Null: seed-to-seed spread as large as between-carrier spread, so nothing predicts. The three-seed subset detects
this early. It would be a caution about single-seed results in this literature: a short post, not a strong one.

## 6. Stage 2 (if stage 1 succeeds)
Add gated adapters and learned soft prompts as carriers, a 32B model, and a setup where the trait cannot be
prompted; test whether the same two numbers predict backdoor leakage. About $1,200.

## 7. Risks and how the plan handles them
- **No released IA code.** The method is two stacked LoRAs with one frozen; the day-1 gate checks the known
  ordering on the rule-scored setup before the sweep.
- **Two setups, so a "law" may be a coincidence.** The cross-setup test is the guard; the margin pays for a third
  setup (confidence statements vs poetic style, no harmful data needed) if the first two agree.
- **Clean desired-only data is a benchmark luxury.** The 250-example variant tests the realistic case.
- **Strong steering breaks training.** Strengths are calibrated on coherence first; broken runs are reported.
- **Overlap with proposal 01.** Shared data build and training loop, different question: 01 inspects deployed
  models for hidden traits; this one predicts outcomes before training.
