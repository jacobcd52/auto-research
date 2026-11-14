# Does the emergent-misalignment "vaccine" hold? A seeded replication with a sham control and held-out fine-tuning attacks
cluster: inoculation | stage-1 cost: $360 | follows up: "Engineering the Generalisation Landscape of LLMs" (ueXaSxeunPjA6kxua); related: "Inoculation Adapters Improve Upon Inoculation Prompting" (qd3qhxgEmQAXR2ZK5)

## 1. What the prior work showed
Emergent misalignment (EM): fine-tuning a chat model on a narrow bad behaviour, such as subtly harmful medical
advice, makes it broadly misaligned on unrelated questions. Inoculation prompting and inoculation adapters defend
against this, but only if the defender controls the fine-tuning run.

Ratnam (LessWrong, Jul 2026) proposed changing the base model instead, so that later fine-tunes generalise
differently. The method: train a LoRA that elicits a trait, freeze it, and train the *base weights* underneath it.
For EM he ran five rounds on Qwen2.5-7B-Instruct. Each round trains a fresh LoRA on the Turner et al. bad-medical
dataset, then distils the model toward the original, unmodified base on general prompts (Tulu-3) outside the
medical domain, alternating batches with the bad LoRA attached and detached. The reported effect, measured by
training fresh LoRAs on the final base:
- bad-medical: broad misalignment 26% to 11%; in-domain bad advice 56% to 46%;
- risky-financial (never used in the procedure): broad 50.9% to 26%; narrow stayed near 90%;
- extreme-sports (never used): broad 21.5% to 8.9%; narrow stayed near 90%.

If this holds, it is a base model on which narrow harmful fine-tunes stay narrow: a defence that works when
someone else does the fine-tuning. The post is a proof of concept: one run, no confidence intervals, no control
condition, no released code. The author asks whether there are side effects.

Related work: Soligo et al. (arXiv 2602.07852) argue that the broad solution is the more stable one, and a
search summary (which I did not verify at source) mentions a GPT-4.1 study in which benign pre-fine-tuning
weakened later EM. A Fall-2026 SPAR project mentored by the author continues the general line; its public page
lists no robustness experiments. Searches of LessWrong and
arXiv on 2026-11-14 found no replication or stress test of the disentanglement result.

## 2. Question and why it matters
Is the reduction in broad misalignment a specific change to how the model generalises from harmful data, and does
it survive fine-tuning recipes and datasets the procedure never saw?

Three dull explanations need ruling out. (a) Noise: one run, modest percentages. (b) Generic damping: a base
trained to stay near itself under a LoRA may resist *all* broad generalisation from LoRA fine-tunes, good or bad.
(c) Overfitting to the attack: the base may only cancel rank-32 LoRAs trained like the ones it saw. If the effect
survives all three, providers have a cheap hardening step. If not, we learn which explanation was right before
more work builds on the method.

## 3. Stage 1 plan
**Reused:** Qwen2.5-7B-Instruct; Turner et al. datasets as plain parquet
(`huggingface.co/datasets/geodesic-research/sfm-emergent-misalignment-training-data`: bad_medical_advice 7,049
rows, risky_financial_advice 6,000, extreme_sports 6,000, school_of_reward_hacks 1,073); insecure-code data from
Betley et al. (mirror: `anishkoppula/emergent-misalignment-insecure-code`); Tulu-3 prompts; the 48 pre-registered
EM questions and the alignment/coherence judge prompts of Betley et al.; public reference EM adapters
(`ModelOrganismsForEM/Qwen2.5-7B-Instruct_*`) to sanity-check the evaluation.
**Built:** the vaccination loop itself (no code released) and the evaluation harness.

Bases compared:
1. **Original** Qwen2.5-7B-Instruct.
2. **Vaccine**: five rounds as in the post, two independent seeds.
3. **Sham vaccine**: the identical procedure with a benign elicitor (a LoRA trained on *correct* medical advice
   from the same prompts). This isolates generic damping from anything specific to misalignment.

Steps:
1. Implement one round. Full-weight updates of a 7B model fit on one 80GB GPU in bf16 with a small batch; the
   declared fallback is a rank-64 LoRA trained under the frozen elicitor and merged after each round.
2. **Gate (end of day 1):** after two rounds, fresh bad-medical LoRAs (3 seeds) on the vaccine base show at least
   a quarter less broad misalignment than on the original. If not, try two learning rates and step counts; if it
   still fails, stop and write up the failed replication.
3. Finish five rounds for the vaccine (two seeds) and the sham.
4. **Attack grid.** On each base, fine-tune on five datasets (bad-medical, financial, sports, insecure code,
   School of Reward Hacks) with three recipes: the post's default rank-32 LoRA; a stronger LoRA (rank 64 on all
   modules, three epochs); and full fine-tuning on a 2,000-example subset. Two seeds each. Measure broad
   misalignment (48 questions x 10 samples, share with alignment < 30 among coherent answers) and narrow
   in-domain misbehaviour on held-out domain questions.
5. **Hidden rather than removed?** On vaccine-base fine-tunes, re-evaluate with Dubiński-style cues that resemble
   the training context (domain persona system prompts, in-domain formatting).
6. **Side effects.** (i) Benign narrow-to-broad generalisation: fine-tune each base on French answers for one
   topic and on a cautious-advice set, and measure how far the trait spreads to unrelated prompts. (ii) Does the
   vaccine base still play a villain in fiction when asked? (iii) A 500-question MMLU subset and coherence.

Primary analysis: for each dataset and recipe, the ratio of broad misalignment on vaccine vs original base and on
sham vs original base, with bootstrap intervals over questions and seeds. Headline plot: attack strength on the
x-axis, broad misalignment on the y-axis, one line per base.

## 4. Stage 1 cost estimate
RunPod H100 PCIe 80GB secure cloud at $2.89/h; gpt-4.1-mini at $0.40 / $1.60 per M tokens (both looked up today).

| Item | Quantity | Cost |
|---|---|---|
| Vaccination: 3 runs (2 vaccine seeds + sham) x 5 rounds x ~1.3 h | 20 GPU-h | $58 |
| Attack grid: 3 bases x 5 datasets x 3 recipes x 2 seeds = 90 runs, ~15 min with generation | 23 GPU-h | $66 |
| Side-effect fine-tunes, cue re-evaluation, MMLU | 8 GPU-h | $23 |
| Debugging the loop, hyperparameter retries at the gate, idle time | 25 GPU-h | $72 |
| Judging: ~170k completions x 2 judges x ~600 input tokens = ~200M tokens | | $80 |
| Storage for full-weight checkpoints (~150 GB for a few days), judge validation | | $11 |
| Margin | | $50 |
| **Total** | | **$360** |

## 5. What success looks like
Strong positive: on held-out datasets the vaccine base cuts broad misalignment by half or more under the default
recipe, the sham does not, most of the benefit remains under rank-64 and full fine-tuning, cues do not bring it
back, and benign traits still generalise: "A base model that keeps harmful fine-tunes narrow".

Informative negatives, each publishable:
- the sham matches the vaccine: the effect is generic damping, and benign generalisation should drop equally;
- protection vanishes under stronger or full fine-tuning: the vaccine overfits to the attack it was trained on;
- cues restore misalignment: the vaccine hides EM in the way dilution and inoculation prompting do;
- the gate fails: a documented non-replication with the exact recipe tried.

Ambiguous: a small effect (say 20% relative) with overlapping intervals. Two seeds and 48 questions cannot
resolve that; I would report the bound and claim no more.

## 6. Stage 2 (if stage 1 succeeds)
More rounds and several elicitor datasets per round to see whether protection keeps growing; a 32B model;
asymmetric entanglement as suggested by Niels Warncke in the comments (reward hacking pulls toward a benevolent
persona, not the reverse); combining the vaccine with inoculation adapters at fine-tuning time. Roughly $2,000.

## 7. Risks and how the plan handles them
- **Reimplementing an unreleased method is the main risk.** The post describes the loop well enough to build
  it; the day-1 gate limits the spend, and a failed replication is still a result.
- **Full-weight training instability or memory.** Fallback to a merged high-rank LoRA, declared in advance.
- **Weak EM on a 7B model leaves little to reduce.** The post's baselines are 21 to 51% broad misalignment; I
  check ours against the public `ModelOrganismsForEM` adapters before vaccinating.
- **Judge noise.** Standard thresholds, validation of gpt-4.1-mini against gpt-4.1 on 500 answers, and coherence
  reported separately so that an incoherent model is not counted as aligned.
- **Scooping by the author's SPAR team.** Possible; an independent replication with controls keeps its value.
