# One-number unlearning beyond German: are parameter subcomponents a better editing basis than neurons?
cluster: param-decomp | stage-1 cost: $230 | follows up: Exploration: fine-tuning with parameter decomposition (ieoWstubDQWLrMnhH); [Linkpost] Interpreting Language Model Parameters (eAQZaiC3PcBhS4HjM)

## 1. What the prior work showed
Goodfire's adVersarial Parameter Decomposition (VPD, arXiv 2610.20748) rewrites each weight matrix of a 4-layer,
67M-parameter language model (trained on the Pile) as a sum of 38,912 rank-1 "subcomponents" u v^T, trained so that
most can be ablated on any given token without changing the output. A learned causal-importance (CI) function says
which subcomponents are needed where.

Lucius Bushnaq's follow-up post fine-tunes only the scalar prefactor of chosen subcomponents to destroy German
prediction while a KL penalty preserves English. With the 16 most German-specific subcomponents, the edit beats
rank-1 LoRA at small data budgets but, like LoRA, wrecks French, Spanish and Italian. With the single subcomponent
whose auto-generated label mentions only German (`h.3.attn.v_proj:513`), flipping its sign drives German to chance
(10.83 nats) with under 0.1 nats English damage from about 4 German tokens (LoRA needs about 32) and leaves French and
Spanish nearly untouched, although nothing in the objective protects them. Italian is damaged. The author's caveats:
one target, one decomposition, one model; the German data used for decomposition and labelling is not counted; the
fine-tuning code is not public. In the comments Stefan Heimersheim asks whether another basis (e.g. an SAE) would have
done as well; Lucius replies that the comparison is hard to define and has not been run.

Related work: Angsten's audit (LessWrong, Sept 2026) shows that hard-deleting 256 code-specific subcomponents costs
0.67 nats on code against 0.03 on prose (random matched control 0.08), and that the released no-adversary
decomposition is 4-7 times less robust. arXiv 2607.13047 removes memorised sequences with a targeted decomposition.
Goodfire's "Already Clean" essay and Leo Gao's reply (Oct 2026) dispute whether plain neurons are already a good
basis. I found no replication of the single-scalar result and no comparison with edits in other bases (LessWrong
pingbacks and comments, arXiv API; general web search was unavailable).

## 2. Question and why it matters
Across many unlearning targets, does a one-scalar edit of a VPD subcomponent remove the target more selectively than a
one-scalar edit in other natural rank-1 bases of the same weights (MLP neurons, singular vectors, subcomponents from a
decomposition trained without the adversary), when every basis gets the same selection data and search effort?

The German result is the most concrete evidence that parameter decomposition finds units useful for control, but it
is a single, partly hand-picked case. If it generalises and the subcomponent basis clearly wins, that is independent
support for the agenda (and for adversarial training, if the no-adversary basis is worse). If neurons match it, that
supports the "already clean" view and weakens the case for expensive decompositions (the released one took 206
H200-hours). If German was a lucky case, that matters for anyone planning to use this for unlearning.

## 3. Stage 1 plan
Reused: target model (W&B `goodfire/spd/t-9d2b8f02`, 268 MB), main decomposition (`goodfire/spd/s-55ea3f9b`,
`model_400000.pth`, 2.9 GB), no-adversary decomposition (`goodfire/spd/s-05ef623e`); these download without an
account via `https://api.wandb.ai/files/goodfire/spd/<run>/<file>` (checked). Loader and editing utilities from
https://github.com/goodfire-ai/param-decomp at tag `vpd-paper`, with the environment of
https://github.com/angsten/vpd-audit (same commit; ran on an A100 40 GB). Data: `Helsinki-NLP/europarl`,
`monology/pile-uncopyrighted`, `codeparrot/codeparrot-clean-valid`. Built: the fine-tuning harness (the post gives
the protocol), the baseline bases, the evaluation grid.

An edit is W' = W - (1-s) u v^T with s the only trainable number, so every edited model is plain weights; the CI
function is needed only for selection.

Steps.
1. Day 1 gate: load the model and decomposition, reproduce the paper's reported reconstruction KL, then reproduce the
   German result for `h.3.attn.v_proj:513` (German at chance, English damage < 0.1 nats at a 4-32 token budget;
   French and Spanish spared, Italian damaged) and the rank-1 LoRA baseline.
2. Targets: Europarl languages (de, fr, es, it, nl, pt, sv, fi, da, pl) and Pile subsets (GitHub, ArXiv, PubMed,
   FreeLaw, USPTO, StackExchange, Enron, DM Mathematics). Keep a target only if the base model's CE on it is at least
   1.5 nats better than a unigram model; aim for 12 or more.
3. Bases, one trainable scalar each: (a) VPD subcomponent; (b) subcomponent from the no-adversary decomposition;
   (c) MLP neuron (scaling a neuron's output weights, a rank-1 slice of the MLP output matrix); (d) one singular
   direction of one weight matrix; (e) random subcomponent matched for firing frequency (control). References with
   more parameters: top-16 subcomponents, rank-1 LoRA on all 24 matrices, rank-1 LoRA on one matrix.
4. Selection, identical across bases and without human labels: score each unit by mean importance on N target tokens
   minus mean on N English tokens (CI for a/b; absolute contribution |v.x|*||u|| for all bases, so results do not hinge
   on the CI function), N in {512, 8k, 128k}. Two variants: "top-1" (fully automatic) and "best of top-20" (each
   candidate fine-tuned, winner chosen on a dev split), so each basis gets its best shot.
5. Fine-tuning protocol as in the post: maximise target CE capped at uniform, KL penalty to the original model on
   English Europarl only, target-token budgets {4, 32, 256, 2048}, 5 seeds, learning rate tuned per (basis, budget) on
   a dev split, train to plateau.
6. Evaluation on held-out text for every category: CE increase on the target, on English (Pile validation), and on
   every other category. Metrics per (target, basis): fewest target tokens reaching 90% of the gap to chance with
   English damage < 0.1 nats; collateral = mean CE increase on non-target, non-English categories at that point.
7. Relearning check on 4 targets: fine-tune all weights of each edited model on fresh target text; tokens needed to
   recover half the lost CE (one-scalar edits vs LoRA).
8. Analysis: paired comparison across targets (bootstrap, sign test) of collateral and token efficiency for (a) vs (c),
   (b), (d); a target-by-category heatmap per basis; fraction of targets with any working single unit. Selection
   tokens are reported separately from fine-tuning tokens.

## 4. Stage 1 cost estimate
The model is small (28M non-embedding parameters); a run is 300-1,700 steps, assumed about 45 s on a 48 GB card
including evaluation (measured at the gate).
- Setup, reproduction, scoring all units on up to 128k tokens x 18 categories (needs the 2.9 GB CI model): 12 A100-h
  at $2.09/h (RunPod) = $25.
- Top-1 grid: 12 targets x 8 methods x 4 budgets x 5 seeds x 3 learning rates = 5,760 runs = 72 GPU-h.
- Best-of-top-20: 12 targets x 4 bases x 20 candidates x 2 budgets x 2 seeds = 3,840 runs = 48 GPU-h.
- Relearning and extra evaluation: 15 GPU-h.
135 GPU-h on RunPod A40 at $0.59/h = $80. With a 2x margin for reruns and debugging: $160 + $25 + storage $15.
- Auto-labels for the ~100 winning units via OpenRouter claude-haiku-5.5 ($0.10/$0.50 per M tokens): under $5;
  budget $30.
**Total $230.**

## 5. What success looks like
A post-worthy positive: the German pattern holds for most targets, e.g. for 8 of 12 targets a single automatically
selected VPD subcomponent reaches target-at-chance with English damage < 0.1 nats, with significantly lower collateral
than the best single neuron or singular direction (paired test across targets), and the no-adversary decomposition
sits in between. Headline figure: collateral damage against target-token budget, one line per basis, averaged over
targets, plus the heatmaps.

A post-worthy negative: single neurons (or singular directions) match subcomponents within noise, or the clean
one-unit edit exists for only a couple of targets. Either answers the question raised in the comments; the
reproduction itself also has value, since the original code is private.

Ambiguous: results depend on the selection variant (top-1 fails, best-of-20 works for all bases); then the finding
is about selection, not the basis.

## 6. Stage 2 (if stage 1 succeeds)
- Hybrid edits proposed in the VPD paper: LoRA with singular vectors tied to chosen subcomponents; L1-penalised mask
  fine-tuning without manual selection (~$150).
- Transcoder comparison using the transcoders trained on the same model (W&B `mats-sprint/pile_local_sweep_jose`),
  answering the SAE question directly (~$100).
- Repeat on a larger decomposed model if Goodfire releases one, with safety-relevant targets (~$400).

## 7. Risks and how the plan handles them
- Loading the released decomposition fails (repository main has moved to a different engine). Use the pinned
  `vpd-paper` commit and Angsten's lockfile; this is the day-1 gate.
- The German result does not reproduce. Then that, with full protocol, is the finding; run the grid only if the cause
  is understood.
- The model is too weak on most targets. Targets are filtered by base competence; if fewer than 8 qualify, add Pile
  subsets and report the smaller n plainly.
- Unfair baselines. Same selection data and search budget, best-of-20 variant, learning rates tuned per basis.
- Over-reading CE (a broken model also reaches uniform CE). Collateral on all other categories and the
  frequency-matched random control guard against this.
- Small n: targets, not runs, are the unit of analysis; languages and Pile subsets are reported separately.
