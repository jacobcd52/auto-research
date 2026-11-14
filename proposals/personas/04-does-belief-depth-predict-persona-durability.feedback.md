# Feedback: "Do deeper masks last longer?" (personas / 04)

Verdict: **major overhaul.** The question is reasonable and I found no one who has answered it, but the design as written cannot answer it. The outcome variable is undefined for the persona arm, the chosen model is the one where the predictor barely moves, and the 18-organism regression has no power. A statement-level redesign (section 5) fixes most of this for about the same money.

What I checked: the paper (arXiv 2606.11502 v3, full HTML), the LessWrong post, the Hugging Face listings, the three cited arXiv abstracts, OpenRouter prices and the arXiv API for prior work. Two limits: the WebSearch budget for this run was exhausted, so the novelty check rests on arXiv API queries and LessWrong only; and GitHub returns 403 from this sandbox, so repo contents are unverified.

## 1. Would it get upvoted?

Probably not above 50 as designed; I put it at roughly 20%.

- The source post sits at 55 karma with **0 comments**. It is the lowest-karma empirical post in the cluster, so a follow-up starts with a small audience.
- The headline would be a correlation across 18 non-independent LoRA runs on an 8B model, with a predictor measured on two different instruments. LessWrong readers will see two clusters (EM, persona) and a method confound.
- The version that would clear 50 is a clean, falsifiable claim such as "a probe reading taken before further training tells you which trained-in beliefs survive it, beyond what a cheap behavioural test tells you". The audience would be the persona-research people (CLR, Africa/Irving, ACS) and anyone asking "does character survive RL". The current design cannot support that sentence.
- A clean negative ("probe depth does not predict durability once training amount is controlled") would be mildly interesting, in the 30-50 range.

## 2. Naturalness

It is a mainline question. The paper's introduction names "the depth and robustness of what a model has learned", and the screener flagged the same follow-up. The proposer's own NOTES rank it weakest of the four, and I agree.

I found no direct duplicate, but adjacent work shrinks the novel part to "probe as predictor":

- **Conditional misalignment (2604.25891)** already shows that benign fine-tuning after EM hides misalignment behind training-like cues. Step 7 replicates this.
- **"An Emergent Mirage" (2607.09053)** runs misalignment/realignment cycles while tracking LoRA representations. It finds apparent rapid realignment largely disappears after controlling for response length, and that mechanistic signatures do not track behaviour. The proposal does not cite it, and it is a direct warning about the washout arm: answer length in the benign data will drive "half-life".
- **Slocum et al. (2510.17941)** already defines belief depth with probes plus robustness to challenge, for SDF-implanted facts. That is not robustness to further training, so the gap is real.
- **Trait-space monitoring (2606.07631)** and **Alignment Dynamics (2605.18309)** cover internals during fine-tuning and the fragility of trained dispositions.

Factual claims in section 1 of the proposal:

| Claim | Status |
|---|---|
| Paper content, authors, 15 core personas, 300 Q&A SFT, challenge protocol | Correct |
| Statement sets public on Hugging Face | Correct. `training_data/*.jsonl` (the 300 SFT pairs per persona) is also there, so the proposal's "generate 300 Q&A pairs with a frontier model" is unnecessary |
| "EM adapters and datasets are public (`ModelOrganismsForEM/` on Hugging Face)" | Half wrong. The org lists 38 model repos and **zero datasets**; none of the adapters is for Qwen3-8B. My recollection is that the Turner et al. training data ships in their GitHub repo as an encrypted archive; unverified here |
| EM 13-category proposition sets reusable | Not found in the Hugging Face dataset (folders are persona-only). They may be in the GitHub repo; unverified. If absent, 2,600 propositions must be regenerated (the paper used Kimi K2.6) |
| Baines et al. 2609.20412 | Exists ("Stress-testing Alignment Midtraining"). The paraphrase is fair: a tiny fraction of competing fine-tuning data erases midtraining effects |
| Paper adapters not on Hugging Face | Correct; nothing relevant under `Experimental-Orange` |
| GPT-4.1-mini $0.40/M input, GPT-4o $2.50/$10 | Correct on OpenRouter today |

## 3. Pre-mortem

**Rough forecast:** clear positive 10%; clear and interesting negative 15%; ambiguous mush 50%; stops at the go/no-go or fails to run 25%.

Specific reasons, most serious first:

1. **The persona outcome variable is not defined.** The released SFT data has the full persona system prompt on every example, and the paper evaluates persona SFT with that prompt present. Base Qwen3-8B already role-plays Darwin under that prompt. So after washout:
   - with the prompt, expression stays near ceiling forever and half-life is infinite for every organism;
   - without the prompt, a LoRA trained only on prompted examples may show little persona at baseline, so there is nothing to decay.
   The proposal never says which condition is measured. Training without the system prompt gives a different organism from the paper's, and the "SFT barely lifts the probe" premise then has to be re-established.

2. **Qwen3-8B is where the predictor barely moves.** From the paper's appendices:
   - EM lift on Qwen3-8B is +0.16 and +0.13 on the top two categories and near zero or negative on most others. On Qwen2.5-14B the top category is +0.41.
   - Persona SFT's protection gap on Qwen3-8B is +0.047 (native probe) or +0.089 (frozen probe), and on the frozen probe it is *larger* than OCT's (+0.050).
   - The compute-matched control says character and EM lifts are "within noise at the 4k Qwen budget, where both are near zero".
   So the step-4 go/no-go ("EM lift clearly above persona-SFT lift") has a substantial chance of failing on this model, and the 1/3-dose and 2/3-dose EM checkpoints will have lift indistinguishable from zero. The dose series supplies noise, not range.

3. **The two arms have no common predictor scale.** Persona lift is an era-believed minus era-false gap. EM lift is a calibrated shift on 13 unrelated proposition categories read with a native probe, because EM rotates the truth direction (cosine about 0.58). Pooling them in one regression is not meaningful.

4. **"Matched behavioural expression" is impossible.** Persona SFT reaches 98% identity adoption; the Qwen3-8B EM organism is 10% misaligned on the Turner protocol. At 200 completions per checkpoint that is about 20 misaligned answers at baseline and perhaps 6 at one-third dose. A half-life cannot be estimated from those counts.

5. **No power, and training amount is the obvious confound.** There are 12 persona points (4 personas x 3 doses) and 6 EM points that are checkpoints of only two runs. Dose, adapter norm, baseline expression and probe lift will be nearly collinear. "Partial correlation controlling for norm and expression" at n=18 will produce a wide interval whatever the truth. If lift does predict durability, a reader will say "more training lasts longer".

6. **The washout itself is a design choice that sets the answer.** Continuing the same LoRA on base-model self-distillation mostly reverses the same low-rank directions; a fresh adapter on merged weights, or a different benign set, could give different orderings. The Emergent Mirage result says response length alone changes realignment speed. One washout recipe gives a result about that recipe.

7. **Smaller traps.**
   - Qwen3-8B is a hybrid thinking model; thinking must be off identically for training, generation and activation reads.
   - The paper's SFT recipe is rank 64, alpha 128, lr 2e-4, 3 epochs; its EM recipe is rank 32, rsLoRA, lr 1e-5, 1 epoch. The proposal's "rank 32 for everything" matches neither, so "following the paper" is not literally true and the lift values need not reproduce.
   - Tracking lift through washout needs a native probe at each of 126 checkpoints. That is feasible but is not in the plan or the hours.

The most likely actual outcome: the team reproduces a weak EM lift, finds persona expression is either at ceiling or at floor depending on the prompt, improvises a no-prompt variant, and reports a scatter where EM and persona form two blobs with overlapping error bars.

## 4. Cost check

The arithmetic is right as far as it goes (57.6k judge calls x 600 tokens is about $14 at $0.40/M), and the total is not the problem. What is missing:

- EM arms need roughly 5-10x more completions per checkpoint to resolve a 3-10% base rate: add $50-90 of judging and about 15 GPU hours.
- Native probes at 126 checkpoints, plus possible regeneration of EM propositions: about 10 GPU hours and a few dollars.
- A second washout recipe and a second seed everywhere, which the design needs to be believable.

My estimate for the proposal as written, done properly: **$250-300**. For the redesign below: **$150-250**. Either is within the $500 cap. I did not re-verify the A6000 hourly price.

## 5. Recommended changes, in order of importance

1. **Make the statement the unit of analysis, not the organism.** The paper already shows that per-statement probe score predicts per-statement defence under challenge. Ask the direct extension: within one organism, does a statement's baseline probe lift predict whether the model still asserts or defends *that statement* after N washout steps? This gives hundreds of data points per organism, holds training amount, adapter norm and method fixed by construction, and removes the two-blob problem. Organisms become a random effect; 6-8 of them are enough.

2. **Pre-register the comparison that matters: probe versus cheap baselines.** Predictors to beat are (a) baseline assertion rate, (b) baseline defence-under-challenge rate, (c) base-model plausibility of the statement. The claim worth a post is "probe lift adds predictive power beyond the behavioural challenge test" or "it does not". State the incremental metric (for example held-out AUC with and without the probe feature) before running.

3. **Fix the persona outcome variable before anything else.** Train persona organisms without the system prompt (strip it from the released `training_data`), evaluate without it, and report expression as excess over base. Day-one check: no-prompt expression is well above floor at baseline, and the era-believed versus era-false gap is still measurable. If either fails, stop.

4. **Drop the pooled EM-versus-persona regression and the EM dose series.** Keep EM, if at all, as one separately analysed arm on its own instrument with at least 1,000 completions per checkpoint. Better, run that arm on Qwen2.5-14B with the *released* bad-medical adapter (12.6% misaligned, lift up to +0.41, fits a 48 GB card), where the effect is known to exist.

5. **Consider replacing the method contrast with one that has a common instrument.** Implant the same era-believed claims two ways: in-character Q&A SFT, and synthetic documents asserting the claims (Slocum et al. report SDF beliefs are deeper on probes). Same statements, same probe, same washout. This is the proposer's rejected idea 21, and here it earns its place because it gives between-method variation on one scale.

6. **Run two washout recipes and control answer length.** (a) Continue the same adapter; (b) merge, then train a fresh adapter. Use length-matched benign data. Report whether statement-level ordering is stable across recipes; cite and respond to 2607.09053.

7. **Resolve the data questions in the first hour.** Confirm where the Turner et al. training sets and the 13-category propositions actually live (not the Hugging Face org named in the proposal). Use the released SFT training data instead of regenerating it. Correct section 1 accordingly.

8. **Reframe success.** Replace "partial correlation above 0.5 across 18 organisms" with the statement-level incremental-prediction result, plus one figure: retention curves for high-lift versus low-lift statements within the same organism.

If the proposer does not want to redesign along these lines, I would fund proposals 01-03 from this cluster ahead of it and drop this one.
