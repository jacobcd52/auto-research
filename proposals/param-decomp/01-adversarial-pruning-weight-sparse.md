# Does adversarial masking fix unfaithful weight-sparse circuits?
cluster: param-decomp | stage-1 cost: $160 | follows up: Weight-Sparse Circuits May Be Interpretable Yet Unfaithful (sHpZZnRDLg7ccX9aF); [Linkpost] Interpreting Language Model Parameters (eAQZaiC3PcBhS4HjM); An Ambitious Vision for Interpretability (Hy6PX43HGgmfiTaKu)

## 1. What the prior work showed
Gao et al. (arXiv 2511.13653) train transformers with mostly-zero weights and extract task circuits by learning a
binary mask over nodes (neurons, attention channels): nodes outside the circuit are ablated, and the mask minimises
task loss plus circuit size. Leo Gao's agenda post cites these circuits as progress, while noting that the
faithfulness test (mean ablation) is weaker than it should be.

Jacob Drori replicated this on SimpleStories with 2-layer models (dense d_model=128; sparse d_model=1024, 3072, 4096)
and showed the pruning step produces unfaithful circuits: (1) a nonsense task (male name -> "is", female -> "when")
reaches CE < 0.05 with ~30 nodes; (2) a pronoun circuit has uniform attention although the real head attends to the
name; (3) circuit nodes change role between pruned and original model; (4) on a simplified IOI task ("when leo went to the shop, mia
urged him") pruned only on opposite-gender name pairs, many of 100 pruning seeds find the wrong rule ("opposite
gender to name 2"): same-gender accuracy spikes at 0 although the original model scores 0.81. He asks for a
faithfulness metric, a pruning algorithm that satisfies it, and a re-check of whether sparse models still have smaller
circuits.

In the comments Lucius Bushnaq proposes the fix: do not ablate non-circuit nodes completely; let an adversary choose
which of them to ablate, by gradient ascent on their masks, using one ablation pattern per batch. The VPD paper
(arXiv 2610.20748) then reports that its own attribution graphs are small, clean and wrong unless pruned with
stochastic and adversarial mask sampling, and claims the problem "is likely to apply in any setting in which
masking-without-adversarial-sampling is used", i.e. most of the subnetwork-identification literature.

Already done: Angsten's two audits (LessWrong, Sept-Oct 2026) test VPD's own decomposition; arXiv 2607.02964 studies
single weights in sparse models. I found no work adding stochastic or adversarial masking to weight-sparse pruning
(arXiv API, LessWrong pingbacks and comments; general web search was unavailable).

## 2. Question and why it matters
On Drori's released models and tasks, does replacing complete ablation with stochastic or adversarial partial
ablation remove the documented failures, and at what cost in circuit size?

If it works, there is a cheap recipe for faithful pruning, the VPD claim is confirmed on an independent test bed with
known failures, and we learn whether Gao et al.'s headline (sparse models have much smaller circuits) survives. If it
fails, either the failures persist (adversarial masking is not sufficient, undercutting a central argument of the
parameter-decomposition agenda) or circuits swell toward the whole model (the small circuits were an artefact of a
weak test).

## 3. Stage 1 plan
Reused: Drori's code (https://github.com/jacobcd52/sparse_pretrain_public, `src/pruning/` with all tasks) and his
public Hugging Face checkpoints
`jacobcd52/ss_bridges_d1024_f0.015625`, `jacobcd52/ss_bridges_d3072_f0.005`, `jacobcd52/ss_bridges_d4096_f0.002`,
dense `jacobcd52/ss_d128_f1`; dataset `jacobcd52/simplestories-tokenized`. Built: about 200 lines changing the masked
forward pass and loss.

Masking schemes. Let g in {0,1} be the learned circuit mask, a the node activation, b its ablation value (zero or
pretraining mean). Non-circuit nodes take a*m + b*(1-m) with m = g + (1-g)*r.
- C0 complete ablation, CE-to-label objective (Drori's algorithm; reproduction).
- C1 complete ablation, objective changed to KL to the original model's output on the task tokens.
- S stochastic: r ~ U[0,1] per node, resampled each step; loss averaged over complete (r=0) and sampled masks.
- A adversarial: r per node, shared across the batch, found by k steps of projected gradient ascent on the loss
  (k in {1, 5, 20}), plus the S and r=0 terms.
- A+LN: A with frozen layernorm scales (Lucius claims the adversary makes freezing unnecessary).
Under S and A the setting r=1 is the original model, so a circuit cannot be asked to beat the model; all arms except
C0 therefore use the KL-to-model objective. C1 isolates the effect of the objective from the effect of the adversary.

Steps.
1. Day 1 gate: reproduce Drori's numbers with C0 (pronoun ~10 nodes and nonsense ~30 nodes at CE < 0.05 on d=1024;
   same-gender histogram spike at 0 on d=3072 IOI). Time one pruning run; fix seeds-per-condition from that.
2. Hyperparameters: per scheme, model and task, a 20-config random search over lr, size coefficient and adversary
   step size, selected on a held-out split by circuit size at a fixed KL budget.
3. Failure-test battery, for each scheme on d=1024 and d=3072:
   a. IOI generalisation: prune on opposite-gender prompts, 40 seeds per scheme; report the distribution of same-gender
      P_correct and the fraction of seeds within 0.1 of the original model's 0.81.
   b. Attention recovery on the pronoun task: KL between pruned-circuit and original attention patterns of heads in
      the circuit; presence of query/key nodes.
   c. Node-role agreement: correlation, over task and pretraining tokens, between each circuit node's activation in the
      original model and in the fully-ablated circuit; fraction of nodes with correlation < 0.5 or flipped sign.
   d. Nonsense task: impossible by construction under the KL objective; a sanity check, not a result.
4. Held-out faithfulness metrics that no arm optimises: (i) a stronger evaluation adversary (100 PGD steps, and
   per-example r); (ii) resample ablation, replacing non-circuit nodes with their values on a random other prompt;
   (iii) agreement with the original model on perturbed prompts (swapped names, same-gender, extra clause).
5. Sparse-vs-dense re-check: circuit size against held-out faithfulness for the dense and three sparse models on the
   three tasks, 8 size coefficients each, for C0 and the best robust scheme. Does the ordering in Gao et al. Figure 2
   survive? Inspect 2-3 robust circuits in Drori's viewer for readability.

Key analysis: battery metrics per scheme with bootstrap intervals over seeds; circuit size against adversary strength
k; the size-vs-faithfulness Pareto plot for sparse and dense models.

## 4. Stage 1 cost estimate
Models are 2-layer (largest checkpoint 0.5 GB); one C0 run is 2,000 steps at batch 64, assumed 1-3 minutes on a
48 GB card (to be measured at the gate); adversarial runs cost about (k+2)x.
- Reproduction and timing: 5 GPU-h.
- Hyperparameter sweeps: 5 schemes x 2 models x 2 tasks x 20 configs x ~4 min = 27 GPU-h.
- Battery: 7 arms (A at three k) x 2 models x 40 seeds x ~6 min avg = 56 GPU-h.
- Pareto re-check: 4 models x 3 tasks x 2 schemes x 8 coefficients x ~5 min = 16 GPU-h.
- Held-out evaluation and inspection: 10 GPU-h.
Total ~115 GPU-h on RunPod A40 at $0.59/h = $68; doubled for reruns and for an L40S ($1.09/h) if memory is tight
= ~$140. Storage and misc. $20. No API spend. **Total $160.**

## 5. What success looks like
Clear positive: under A (and possibly S) the same-gender spike at 0 disappears (e.g. more than 80% of seeds within 0.1
of the model's 0.81, against a minority under C0), attention patterns match the original, role-flipped nodes become
rare, and C1 alone does not achieve this. Reported with the price: how much larger the circuits are, and whether
sparse models keep their size advantage.

Clear negative: the failures persist under adversarial masking at any k, or disappear only when the circuit grows to a
large fraction of the model. Both are publishable: the first contradicts a stated claim of the VPD paper; the second
says the small circuits of weight-sparse models do not survive a faithful test.

Ambiguous: C1 (objective change alone) fixes most failures, or results differ between d=1024 and d=3072. Still worth
a short post, since it identifies which ingredient matters.

## 6. Stage 2 (if stage 1 succeeds)
- Mirror test: the same battery on VPD's two pruning modes, using the public SimpleStories 2-layer decomposition
  (W&B `goodfire/spd/s-eab2ace8`, 98 MB) (~$60).
- Port the robust pruning to OpenAI's released Python-code models (`openai/circuit-sparsity`) (~$150).
- Train weight-sparse models without layernorm, as Leo Gao asked (~$300, to be measured).

## 7. Risks and how the plan handles them
- Reproduction fails (Drori's tuned hyperparameters are not all in the repo). Day-1 gate; if the spike does not
  reproduce on d=3072, tune C0 first and report that honestly.
- The adversary is too strong and every circuit becomes the whole model. k is swept and r is batch-shared, as Lucius
  recommends; the size-vs-k curve is then the deliverable.
- Evaluation bugs (wrong hook, layernorm handling). Unit tests: r=1 reproduces the original logits exactly; r=0
  reproduces Drori's masked forward pass.
- Over-claiming from two models and toy tasks. Claims are scoped to this test bed; held-out metrics are fixed before
  the battery runs.
- Hyperparameter luck (Drori's own caveat). Equal search budget per scheme; battery seeds are spread over the top-3
  configurations.
