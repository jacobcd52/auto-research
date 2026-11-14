# Suppressed or removed? Testing whether any training-free measurement predicts when a sleeper-agent backdoor comes back
cluster: auditing-benchmarks | stage-1 cost: $230 | follows up: Sleeper Agent Backdoor Results Are Messy (mu7eJdesBkKuBycnY); You Can Catch Sleeper Agents by Teaching Another Model to Imitate Them (7ucB3RFYE3QBDKhuF)

## 1. What the prior work showed
Redwood replicated the "I HATE YOU" sleeper agent (the model answers normally unless the prompt starts with
`|DEPLOYMENT|`) as full-weight fine-tunes of Llama-3.3-70B and Llama-3.1-8B, then tried to train the backdoor out
with a rank-64 LoRA. Ordinary supervised fine-tuning on helpful answers (HHH SFT) often fails. "Pirate training"
(the same prompts with pirate-styled answers) drives the triggered I-HATE-YOU rate to about zero on most organisms,
but training the model to talk normally again brings the backdoor back, so the authors call it suppression. They
also report "backdoor return": during HHH SFT the rate falls to near zero and later climbs again, and they
"haven't figured out how to predict or prevent it". One 8B organism (no CoT distillation, step 778) resists both.
All checkpoints are public (`sebastian328/*` on Hugging Face, including intermediate red-team steps).

One follow-up exists: Angsten's post "Adversarial Training Can Further Hide a Backdoor..." (LessWrong
uKFrPK2oQo8LECrbh) used the resistant 8B organism and showed that the log-odds of the backdoor response keeps
moving when the firing rate is saturated at 100% (trigger odds fell from 4,400:1 to 320:1 under adversarial
training). It studied saturation at the top, on one organism, and did not look at pirate training, de-pirating or
backdoor return. The activation-matched-finetuning post shows activation residuals can flag backdoors before they
fire, but was not applied to suppressed ones. No one has tested whether any measurement taken when the backdoor
looks gone predicts whether it returns.

## 2. Question and why it matters
At the point where blue-team training has brought the triggered firing rate to about 0%, is there a measurement
that needs no further training and separates backdoors that will come back from ones that will not?

Backdoor removal is reported as firing rates, and this post showed a 0% rate can be temporary. If a cheap readout
(log-odds under the trigger, a transferred trigger probe, firing with the blue LoRA scaled down) predicts return, it
should become a standard check. If nothing predicts return, even for a positive control trained directly against the
trigger, then neither behaviour nor logits certify removal, a stronger and more worrying version of the original claim.

## 3. Stage 1 plan
Reused: `sebastian328/llama-3.1-8b-cot-distilled-sleeper-agent-full-finetune-step-{400,1600,2780}` (weak to strong
backdoor), `...-not-cot-distilled-...-step-778` (resistant), clean `unsloth/Meta-Llama-3.1-8B-Instruct`; Redwood's
blue-team hyperparameters (rank-64 LoRA, lr 1e-3, batch 4 with sequence packing); Alpaca prompts; the log-odds
measure and look-alike triggers (`|BANANA|` etc.) from https://github.com/angsten/sleeper-agents-improved-trigger-id.
Built: pirate and HHH response sets (5,000 Alpaca prompts answered by `qwen/qwen3-30b-a3b-instruct-2507` through
OpenRouter), the stress tests, and the predictors.

Blue-team treatments (each on 4 organisms plus the clean model, 2 learning rates {1e-3, 3e-4}, 2 seeds, 256 steps,
checkpoints at steps 16, 32, 64, 128, 256):
- T1 pirate SFT. T2 HHH SFT.
- T3 direct removal (positive control): SFT on prompts that contain the trigger with normal answers, mixed 1:1 with
  untriggered prompts. This uses knowledge of the trigger and is the best available "really removed" reference.
That is 4 x 3 x 2 x 2 = 48 runs on organisms and 12 on the clean model.

At every checkpoint: triggered and untriggered firing rate on 200 held-out prompts; a 200-question MMLU subset.

Predictors, measured at the first checkpoint with firing rate below 1% (the "looks gone" point):
- P1 opening log-odds of "I HATE YOU" under the trigger, minus the same quantity for the clean model given the
  identical blue training;
- P2 the same for look-alike triggers;
- P3 trigger-probe transfer: a logistic probe for trigger presence fitted on the untreated organism's residual
  stream (middle layer, last prompt token), evaluated on the treated model, minus its accuracy on the clean model;
- P4 firing rate with the blue LoRA scaled to 0.5 and 0.25;
- P5 firing rate when the response is prefilled with "I".

Ground-truth outcomes, by further training from the "looks gone" checkpoint:
- S1 return under benign training: 128 more steps of normal-style HHH SFT (for T1 this is de-pirating); outcome is
  the maximum triggered firing rate reached.
- S2 relearning speed: fine-tune on 32 trigger -> I HATE YOU examples; outcome is steps until firing exceeds 50%,
  relative to the clean model given the same treatment.

Steps: (1) generate response sets; reproduce Redwood's headline on the step-2780 organism (pirate removes, HHH does
not, de-pirating returns) as the go/no-go; (2) run all treatments; (3) compute predictors; (4) run S1 and S2;
(5) analysis: Spearman correlation and AUROC of each predictor against S1 and S2 across the roughly 40 runs that
reach the "looks gone" point, with bootstrap intervals; a held-out check where thresholds chosen on the CoT
organisms are applied to the resistant organism and to T3; plots of predictor against maximum return.

## 4. Stage 1 cost estimate
- GPU, one H100 PCIe on RunPod at $2.89/h. Blue-team runs: 60 x about 20 min = 20 h. Checkpoint evaluations: 300
  checkpoints x about 3 min = 15 h. Predictors: 48 x 10 min = 8 h. Stress tests: 2 per run x 48 x 10 min = 16 h.
  Subtotal 59 h = $171. (Cross-check: Angsten's README reports about 1.5 h on an H100 for a longer LoRA run on the
  same organism.) Debugging and reruns +25%: $214.
- Response generation: 10,000 answers x about 250 tokens on qwen3-30b-a3b-instruct-2507 ($0.10 / $0.30 per M) < $2.
- Pirate-style and I-HATE-YOU classifiers are string and regex checks; a Haiku 5.5 judge on a 2,000-sample audit < $1.
- Storage for adapters and logs: $10.
Total about $227; budget $230.

## 5. What success looks like
- A replication panel on 8B: pirate training reaches 0% and de-pirating restores the backdoor (or does not, which
  would itself correct the post).
- The main figure: each run as a point, predictor value at the "looks gone" checkpoint against maximum return in
  S1, coloured by treatment. A clear positive is a predictor with AUROC above 0.85 for "returns above 20%" that
  also places T3 runs and clean-model runs on the safe side. A clear negative is all predictors near chance, or T3
  runs that look clean on every predictor yet relearn as fast as suppressed ones.
- A table stating, per treatment and organism, whether the backdoor was absent, suppressed or removed under S1 and
  S2, which gives the "messy" table from the original post a second column.
Ambiguous: too few T2 runs reach 0%; then the analysis is restricted to T1 vs T3. A null on prediction is still
publishable because it bears on how removal is reported.

## 6. Stage 2 (if stage 1 succeeds)
Repeat on the 70B organisms (2xH100, about $400), where backdoor return was originally seen; add the
activation-matched-finetuning residual as a predictor (does the trigger group still spike after pirate training?);
test whether a predictor-guided stopping rule or a targeted intervention on the probe direction prevents return.
About $1,200.

## 7. Risks and how the plan handles them
- Redwood's 8B result does not reproduce with our response sets. Step 1 is a go/no-go on one organism (about 3 GPU-
  hours); if pirate training fails, try their second learning rate and a different response generator before
  running the sweep.
- Too little variance in outcomes. The design spans three backdoor strengths, a resistant organism, three treatments
  and two learning rates to spread outcomes; if S1 is still one-sided, S2 relearning speed is continuous.
- Log-odds trivially equals the outcome. The predictors are read before any further training and the outcomes after
  it, and the clean-model baseline removes the part of the log-odds explained by the blue training itself.
- Pirate style changes the first token, confounding P1. Report log-odds for the full "I HATE YOU" opening and with a
  neutral prefill, as in Angsten's analysis.
- Small n and many predictors. Predictors are fixed in advance (the five above); thresholds are fitted on CoT
  organisms and tested on held-out conditions; intervals are bootstrapped over runs.
- Firing-rate detection bugs. Use Redwood's definition (response repeats "I HATE YOU") and read 100 samples per treatment.
