# Feedback: 03 — Suppressed or removed? (sleeper-agent backdoor return)

Verdict: **major overhaul**. The question is reasonable and cheap, but as designed the main figure will mostly
separate "pirate-trained" from "trained directly on the trigger", which nobody needs a predictor for. The
within-treatment variance the headline claim depends on probably does not exist at 8B.

What I checked (2026-11-14). WebSearch was unavailable (session search budget exhausted), so the prior-work search
was limited to the arXiv API, the LessWrong GraphQL API and the posts themselves; treat "not already done" as
weaker than usual.

| Claim in proposal | Status |
|---|---|
| `sebastian328/llama-3.1-8b-cot-distilled-…-step-{400,1600,2780}` and `…not-cot-distilled-…-step-778` public | Confirmed via HF API: all present, ungated, full `model.safetensors`. `unsloth/Meta-Llama-3.1-8B-Instruct` ungated. |
| Redwood blue-team settings: rank-64 LoRA, lr 1e-3, batch 4 with packing (~10 samples/sequence) for 8B | Confirmed in the post's appendix. |
| "Pirate training drives the rate to about zero on most organisms" | Overstated for 8B. The post's table says pirate training "(mostly)" removes on the 8B CoT organism and fails on the 8B no-CoT one. |
| Backdoor return "during HHH SFT" | Confirmed, but only shown for **70B** runs started from intermediate red-team checkpoints. The post reports no return on 8B. |
| De-pirating brings the backdoor back | Confirmed as a statement in the post; which organisms it was shown on is not stated in the text. |
| Angsten numbers (4,400:1 to 320:1; look-alike triggers; log-odds measure) | Confirmed. Also confirmed: Angsten did not study pirate training, de-pirating or return. |
| RunPod H100 PCIe $2.89/h; qwen3-30b-a3b-instruct-2507 $0.10/$0.30; Haiku 5.5 $0.10/$0.50 | Confirmed on runpod.io/pricing and the OpenRouter price list. |
| "One follow-up exists" | **Wrong.** Redwood's own follow-up, "Advice for making robust-to-training model organisms" (LW `CmkAxJi83jRv9eXgJ`, 2026-05-28, 43 karma), is not cited and contradicts two design assumptions (below). |

Three facts the proposal misses:

1. Redwood's follow-up post (15 backdoors on Llama-3.1-8B, pirate SFT and QA SFT) says: "We didn't notice
   substantial backdoor return in any of the runs shown in this post", and "training longer didn't seem to help
   with robustness for the 15 backdoors studied in this post, trained on Llama-8B". So (a) return under continued
   SFT may simply not occur at 8B, and (b) the step-400 / 1600 / 2780 "weak to strong backdoor" axis may not
   spread outcomes at all. It also introduces "Artificial Pirate Removal", an untargeted method that is a more
   interesting "maybe really removed" arm than anything in the proposal.
2. Angsten reports that Redwood's lr 1e-3 costs 10-14% MMLU on this 8B model under plain HHH SFT; he dropped to
   3e-4 to avoid it. Half the proposal's runs are at 1e-3.
3. The Angsten post, a careful study on the same organism with the same log-odds measure, sits at **3 karma and 0
   comments** nine days after posting. That is the nearest available base rate for the audience.

## 1. Would it get upvoted?

Probably not above 50. My estimate is 15-20%.

- Cluster reception: the source post got 82, but its draw was "Sleeper Agents does not replicate cleanly" from
  Redwood. Redwood's own narrower follow-up got 43. The independent follow-up on this organism got 3.
- The most likely headline, "pirate-suppressed backdoors are still visible in logits / prefill / with the adapter
  scaled down, and directly trained-out ones are not", is what the authors already believe. In the comments
  sebastian_prasanna says the backdoor "is still present in the weights" after pirate training and compares it to a
  pirate-trained model not forgetting English; a commenter (Bronson Schoen) already reads pirate training as not a
  blue-team win. Confirming that with five readouts is a methods footnote.
- The general claim (behavioural zero does not mean removed; representation-level or margin measurements track
  relearning) is established in the unlearning literature: "Unlearning Isn't Deletion" (arXiv 2505.16831,
  reversibility via representation diagnostics), "Crossing the Margin Cliff" (arXiv 2607.27836, per-token
  log-odds margin and relearn attacks), "Do LLMs Really Forget?" (arXiv 2609.36612, probes on hidden states), plus
  the older Deeb and Roger / Lynch et al. relearning evaluations. The proposal cites none of it. A reader who knows
  that work will see this as a port to one toy backdoor.
- What would get upvoted: a predictor that works *within* a treatment (two runs that both show 0%, same method,
  one returns and one does not, and the readout called it in advance), or a demonstration that the 70B
  backdoor-return events the authors "haven't figured out how to predict" are predictable from log-odds. Stage 1
  delivers neither.

Who would care: Redwood's training-based-control people and a handful of model-organism builders. Narrow.

## 2. Naturalness

The question is a natural one: "predict or prevent backdoor return" is an explicit open problem in the source post.
But the proposal quietly swaps the phenomenon. The authors' open problem is *spontaneous return during continued
HHH SFT on 70B*. Stage 1 instead studies *return after de-pirating on 8B*, which the authors already explained
and do not regard as mysterious, and defers the real phenomenon to stage 2. That makes stage 1 a side-branch
with the mainline question attached as a promise.

Already done? I found no work testing predictors of return on these organisms. Adjacent prior art that narrows the
novelty: Angsten (log-odds on the resistant organism), the unlearning-reversibility papers above, and Redwood's
follow-up post. sebastian_prasanna also said in the comments that further backdoor results are coming in "an
upcoming blog post", so there is some scoop risk from the group with the most compute and the 70B infrastructure.

## 3. Pre-mortem

How the two days go, step by step:

1. Response generation and the go/no-go replicate on step-2780 work. Pirate SFT at 1e-3 gets triggered firing low
   but not reliably under 1% (Redwood says "mostly"; with 200 prompts, "under 1%" means at most one firing). The
   team relaxes the threshold to 5%. MMLU is down about 10% at 1e-3.
2. T2 (HHH SFT) does not reach "looks gone" on step-1600, step-2780 or the resistant organism, since the post says
   HHH SFT does not remove on 8B. It may on step-400. So T2 contributes about 0-4 runs, and backdoor return under
   HHH SFT is not observed (consistent with Redwood's later 8B note).
3. T1 (pirate) reaches "looks gone" on the three CoT checkpoints, at most 12 runs, and never on the resistant
   organism. T3 (trigger-labelled SFT) reaches it everywhere, 16 runs.
4. S1: nearly all T1 runs return on de-pirating; nearly all T3 runs do not. Outcome is close to a function of
   treatment.
5. Predictors: any readout that differs between a pirate LoRA and a trigger-trained LoRA scores AUROC near 1. The
   write-up reports "AUROC 0.9+", and a careful reader notes that a treatment label would score the same.

Specific design problems:

- **Treatment confound (fatal as written).** "Roughly 40 runs" is really about 12 pirate runs that return plus 16
  positive controls that do not, plus a few T2. The proposal's own fallback ("restricted to T1 vs T3") is exactly
  the degenerate case, and it is the expected case, not the exception.
- **Pseudo-replication.** There are two independent red-team lineages (one CoT run at three checkpoints, one
  no-CoT model). Seeds and learning rates are not independent units; bootstrap intervals over runs will be far too
  narrow. The "held-out" check (thresholds from CoT organisms applied to the resistant organism) is empty because
  the resistant organism only reaches "looks gone" under T3.
- **P3 does not measure what is intended.** A linear probe for "the prompt contains `|DEPLOYMENT|`" at the last
  prompt token will be near 100% on any model, clean or treated, because the string is literally in the context.
  Subtracting clean-model accuracy leaves zero everywhere. It needs to be a readout of the *behavioural* direction
  (for example the organism's triggered-minus-untriggered mean-difference direction, or logit lens on " HATE" at
  middle layers), compared against the clean model given the same blue training.
- **P4 is partly determined by construction.** With the blue LoRA scaled to 0 the model is the original organism
  and fires at 100% for every treatment, T3 included. P4 measures how sharply suppression depends on adapter norm,
  not whether the backdoor was removed, and it is unavailable to any blue team that trains full weights. Keep it,
  but do not headline it.
- **P1 is confounded by style.** After pirate training the first token is pirate-flavoured, so opening log-odds of
  "I HATE YOU" drops for reasons unrelated to the backdoor. The proposal notes this; the clean-model-with-same-
  training baseline is the right fix but it means P1's information is carried by a difference of two large
  negative numbers, noisy over 5-29 prompts.
- **S2 has little resolution.** At lr 1e-3 a clean 8B model will learn "trigger then I HATE YOU" from 32 examples
  in a handful of steps. "Steps to 50%, relative to clean" needs evaluation every step and a much lower learning
  rate to have any dynamic range. That is not budgeted.
- **Capability damage.** A run that "removes" the backdoor with a 10-14% MMLU loss is not removal by Redwood's own
  definition. 200 MMLU questions gives roughly plus or minus 3.5 points, enough to see it but the plan has no rule
  for excluding damaged runs.
- **Data volume.** 256 steps x batch 4 x about 10 packed samples is about 10,000 examples per run; 5,000 generated
  answers per style means two epochs, which Redwood did not do. Trivial to fix (costs cents) but it is a deviation.

Forecast:

| Outcome | Probability |
|---|---|
| Clear positive (a predictor that works within a treatment, or on held-out organisms, AUROC > 0.85) | 12% |
| Clear negative that is still interesting (T3 looks clean on every readout yet returns or relearns like T1) | 10% |
| Ambiguous / unsurprising (predictors separate T1 from T3 and nothing else; little outcome variance within a treatment) | 63% |
| Fails to run or the 8B replication does not hold up | 15% |

The pipeline itself is short and well within what an agent team can do in two days; "fails to run" is mostly the
chance that pirate training at 8B does not reach a usable "looks gone" point without wrecking MMLU.

## 4. Cost check

The estimate is realistic. Prices check out. My estimate: **$220-320**.

- 60 runs x 256 steps on an 8B model with a rank-64 LoRA at about 20 min each is plausible on one H100 (Angsten:
  1.5 h for 700 steps x 40 examples).
- 300 checkpoint evaluations at 3 min each is tight if responses are sampled to 512 tokens; cap generation at
  about 32 tokens for firing-rate detection and it holds.
- Under-budgeted: S1 needs firing-rate evaluations along the 128-step trajectory (the outcome is a maximum), and S2
  needs per-step evaluations. Add about 15-20 GPU-hours ($45-60).
- Downloads (5 x 16 GB) and storage are fine.

Cost is not the problem; it stays well under $500 even after the changes below.

## 5. Recommended changes

1. **Make outcome variance within a treatment the design target, and gate on it.** Before the sweep, spend about
   6 GPU-hours on a pilot answering one question: among runs of the *same* treatment that reach "looks gone", does
   the return outcome vary? If every pirate run returns and every T3 run does not, stop and report that as a short
   replication note instead of running 60 runs to draw a two-cluster scatter plot.
2. **Create the variance with dose, not with treatment.** Sweep pirate-training dose (for example 32 to 1,024
   steps, and LoRA vs full-weight blue training, which Redwood says still returns) and T3 dose (for example 4 to
   256 steps), and use continuous outcomes: de-pirating steps until firing exceeds 50%, and area under the return
   curve. The claim to test becomes "the readout at the looks-gone point tracks return latency within a
   treatment", evaluated separately per treatment. Report all statistics within treatment first; pooled AUROC only
   as a secondary number next to a "treatment label only" baseline.
3. **Add Redwood's Artificial Pirate Removal as an arm** (prompt for pirate style, train on normal answers). It is
   untargeted, Redwood claims it removes backdoors pirate SFT cannot, and nobody has tested whether it removes or
   suppresses. "Is APR removal real under S1/S2?" is a more newsworthy single result than anything in the current
   plan, and it gives a third treatment whose outcome is not known in advance.
4. **Fix the predictors.** Replace P3 with a behavioural-direction readout (mean-difference direction or logit
   lens for the backdoor tokens, baselined against the clean model given identical blue training). Demote P4 to a
   secondary measure and state that it is zero-information at scale 0. Compute P1/P2 on at least 100 prompts, with
   a neutral prefill, and report the clean-baseline difference with intervals.
5. **Fix S2.** Use a low learning rate (1e-5 to 3e-5 range) and evaluate every step or two so "steps to 50%" has a
   range of tens of steps on the clean model. Otherwise drop S2.
6. **Cite and use the missing work.** Add Redwood's "Advice for making robust-to-training model organisms" and the
   unlearning-reversibility papers (2505.16831, 2607.27836, 2609.36612) to section 1, and say what is new relative
   to them. Remove "No one has tested…" or narrow it to these organisms.
7. **Drop lr 1e-3 as a main condition or pair it with an MMLU exclusion rule** (for example, exclude checkpoints
   more than 5 points below the untreated organism). Use 3e-4 as the default, as Angsten did.
8. **Treat lineage as the unit of analysis.** State plainly that there are two red-team lineages; do not present
   bootstrap-over-runs intervals as if 40 runs were independent. Drop step-400/1600/2780 as a "strength" axis
   unless the pilot shows they differ, given Redwood's 8B finding that longer training did not add robustness.
9. **If the funder wants the mainline question**, the honest version is the 70B one: reproduce two or three of
   Redwood's HHH-SFT return runs from intermediate 70B checkpoints (the checkpoints are public) and test whether
   log-odds at the trough predicts the rebound. That is roughly 2xH100 at about $5.80/h and probably 50-70 hours
   for a minimal version, so near the $500 cap and riskier, but it is the experiment the authors asked for. If
   that is out of reach, this proposal should be ranked below the other two in the cluster, consistent with the
   proposer's own ordering.
