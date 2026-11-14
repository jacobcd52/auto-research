# Do optimiser-level mitigations remove emergent misalignment, or hide it behind a cue?
cluster: emergent-misalignment | stage-1 cost: $360 | follows up: Optimiser Choice Can Amplify or Suppress Emergent Misalignment (Wq6CaAbiixoCEzbat); Conditional misalignment: Mitigations can hide EM behind contextual cues (vaJC7kPbfMW5CnyLR)

## 1. What the prior work showed
Emergent misalignment (EM): fine-tuning on narrow bad data makes a model broadly misaligned on unrelated questions.

*Optimiser paper* (Brown, Leask, McKinney; arXiv 2606.31591). On Qwen3 models with rank-32 rsLoRA, optimiser choice
gives a 7x spread in misalignment rate at matched training loss: Muon preserves alignment best, Lion worst.
Optimisers that concentrate the LoRA update in few singular directions cause more EM. Adding a regulariser
`lambda * (||BA||_F / ||BA||_* - 1/sqrt(r))`, lambda = 3, to Adam raises mean alignment from below Muon to 72.4
(Muon 69.4) for +0.013 nats of loss, and on insecure code returns alignment to the base model's level. The post
calls this "a cheap mitigation against EM". Every evaluation in the paper uses the standard, uncued questions.

*Conditional misalignment* (Dubinski et al.; arXiv 2604.25891). Three mitigations (dilution with benign data,
post-hoc benign fine-tuning, inoculation prompting) drive misalignment to ~0% on standard questions, but it
returns when the prompt carries a cue from the bad training data (e.g. 0% clean vs 10.4% under the inoculation
prompt for GPT-4.1). The paper names "methods that prevent conditional misalignment" as an open problem.

*Follow-ups that exist.* ContextLift (arXiv 2610.21633, code github.com/davidkaczer/contextlift) reproduces
conditional EM on Qwen2.5-7B: with generic safety-data interleaving, 18.9 / 41.9 / 58.2% of answers are misaligned
under a domain cue for bad security / legal / medical advice, and a data augmentation cuts this to 2.6 / 6.1 /
12.8%. Consistency training (LW LjBAPcY33EKZ7SuuN) seals the inoculation-prompt trigger. "Overtrained, Not
Misaligned" (arXiv 2605.12199) reports that early stopping removes EM. All fixes for conditional EM so far are
data-side; all training-recipe mitigations have been scored only on uncued questions. No work crosses the two.

## 2. Question and why it matters
**When spectral regularisation, Muon, or early stopping lowers EM on standard questions, does misalignment under a
training-context cue fall by the same factor, or does it stay?**

If it stays, the optimiser paper's mitigation is a fourth way of hiding EM behind a contextual gate, and the
"low-rank update is necessary for EM" story needs amending. If it falls proportionally, spectral flattening is the
first training-recipe intervention shown to act on the conditional component, needs no knowledge of the bad data,
and composes with ContextLift.

## 3. Stage 1 plan
**Reused.** The ContextLift repository: Qwen2.5-7B-Instruct 4-bit QLoRA pipeline, bad security and bad medical
advice sets (5,400 train / 600 held-out rows each, from `truthfulai/emergent_plus`), the generic interleaving pool,
the plain and cued EM questions, in-domain questions, held-out narrow-task perplexity, and the judge harness.
The authors report one H100 and 35-50 minutes per seed per arm and ship judge scores for their arms (an exact
reproduction target). Muon from its public reference implementation.

**Built.** (i) An optimiser switch in the trainer (AdamW as shipped, Adam + spectral regulariser, Muon).
(ii) The regulariser, computed per LoRA layer from the r x r core after QR of B and A, so the SVD is cheap.
(iii) Checkpointing at 4 points per run so arms can be compared at matched held-out narrow-task loss.

**Steps.**
1. *Reproduce (gate 1).* Run the shipped "no defence" and "generic interleaving" arms on medical, 1 seed each.
   Pass if cued and uncued rates are within the shipped 3-seed range.
2. *Calibrate (gate 2).* On medical, no defence: tune the Muon learning rate and lambda in {1, 3, 10} so that final
   held-out narrow-task loss is within 0.03 nats of AdamW. Pass if at least one of Muon / regularised Adam lowers
   uncued misalignment by a third or more relative to AdamW. Log adapter stable rank and spectral entropy to
   confirm the regulariser acted.
3. *Main grid.* 2 datasets (security, medical) x 2 data settings (bad data alone; bad data + generic interleaving)
   x 3 optimiser arms (AdamW, Adam + regulariser, Muon) x 3 seeds = 36 runs. Early stopping is a fourth arm
   obtained for free from the AdamW checkpoints.
4. *Evaluate* every final checkpoint and one loss-matched earlier checkpoint on: EM questions plain; the same
   questions with the domain cue; in-domain questions; narrow-task perplexity; the repo's benign-capability checks.
5. *Analyse.* Primary metric: the **retention ratio** = (cued misalignment under mitigation / cued under AdamW)
   divided by (uncued under mitigation / uncued under AdamW), with seed-bootstrap CIs, per dataset and data
   setting. Ratio near 1: the mitigation acts on both components. Ratio well above 1: it hides.
6. *Guard against the in-domain confound* raised in "We need a better way to evaluate EM" (XC28DmEYPLqfwc8tf):
   a cued answer that is merely bad advice in the trained domain is not emergent. Re-judge all cued responses with
   a dataset-aware prompt that counts only misalignment unrelated to the training domain (adapted from that post's
   public judge registry), and report both. If the pilot shows the repo's `fish20` organism (20% poisonous fish
   recipes, cue = marine context) expresses EM on this model, add it: its cue is separate from the harmful content.

Sample sizes follow the repo defaults; 3 seeds match ContextLift, so numbers are directly comparable.

## 4. Stage 1 cost estimate
| Item | Quantity | Unit price | Cost |
|---|---|---|---|
| Gates 1-2 (reproduction, LR / lambda calibration) | 14 H100-hours | $3.99/h (RunPod secure tier; community from $2.69) | $56 |
| Main grid, 36 runs at ~0.75 h | 27 H100-hours | $3.99/h | $108 |
| Extra checkpoint evaluations, fish20 option | 12 H100-hours | $3.99/h | $48 |
| Judge, gpt-6-luna (the repo's judge): ~110 checkpoint evals x ~6,000 calls x ~700 tokens = ~460M input tokens | 460M in, ~15M out | $0.10 / $0.50 per M | $54 |
| Cross-check judge on 4,000 responses, gpt-4o, 2 scores each | ~6M in | $2.50 per M | $15 |
| Dataset-aware re-judging of cued responses | ~60M in | $0.10 per M | $6 |
| Margin for reruns and debugging (~25%) | | | $73 |
| **Total** | | | **$360** |

## 5. What success looks like
A figure per dataset: uncued and cued misalignment for the four arms at matched narrow-task loss, with and
without interleaving; and a table of retention ratios with CIs.

- *Clear "hides" result:* uncued misalignment falls by half or more while the cued rate stays within seed noise
  of AdamW (ratio >= 2). Headline: "spectral regularisation is another mitigation that leaves conditional EM".
- *Clear "removes" result:* cued misalignment falls at least as much as uncued (ratio <= 1.2 with CI excluding 2),
  and interleaving + regulariser reaches the ContextLift range without knowing the bad domain.
- *Mixed:* differs by optimiser (e.g. Muon removes, regulariser hides); informative about whether adapter
  spectrum is the causal variable for the conditional part.
- *Null on the precondition:* gate 2 fails (no optimiser effect on Qwen2.5-7B QLoRA). A replication finding about
  the optimiser paper's generality, but a weaker post.

## 6. Stage 2 (if stage 1 succeeds)
(a) Repeat on Qwen3-8B with bf16 rsLoRA (the optimiser paper's setting) and on the inoculation-prompt trigger
with the Turner et al. datasets. (b) If mitigations hide: can an auditor without the training data find the cue?
(c) If they remove: combine with ContextLift and test under 10% dilution. About $600-900.

## 7. Risks and how the plan handles them
- *The optimiser effect does not transfer to this model / QLoRA.* Gate 2 tests it for about $40 before the grid.
  Fallback: Qwen3-8B bf16 rsLoRA with the same data (one H100, ~1.5x GPU time, 2 seeds).
- *Loss-matching is imperfect, so differences reflect dose, not optimiser.* Compare at matched held-out narrow-task
  loss using intermediate checkpoints, and report in-domain misalignment as a second dose check.
- *Regulariser reimplementation differs from the paper's (no public code).* Verify that adapter stable rank and
  spectral entropy move toward Muon's, as in the paper's Table 3.
- *Cued misalignment is just in-domain bad advice.* Step 6's dataset-aware judge and the fish20 organism.
- *Judge noise near small rates.* 3 seeds, bootstrap CIs, a GPT-4o cross-check subsample; ratios are reported
  only where the AdamW cued rate exceeds 10%.
