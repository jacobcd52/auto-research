# NOTES — cluster `param-decomp` (Parameter decomposition and sparse circuits)

Research-lead notes, written 2026-11-14. Sources: the four posts read in full via `scripts/get_post.py`; the VPD
paper markdown (https://static.goodfire.ai/vpd-blog-post/post.md, 318 KB, read the method / pruning / limitations /
appendix sections); post comments via the LessWrong GraphQL API; arXiv API; Hugging Face API; W&B public API; raw
GitHub files. **Caveat on search coverage:** the WebSearch tool was unavailable (session search budget exhausted), so
the "already done?" check rests on arXiv API queries, LessWrong pingbacks (posts linking to the cluster posts), the
posts' comment threads, and HF/W&B/GitHub listings. A reviser with web search should re-check the two "not yet done"
claims marked (*) below.

## 1. Reading notes

### 1a. An Ambitious Vision for Interpretability (leogao, Hy6PX43HGgmfiTaKu, 2025-12-05)
Opinion/agenda post, no experiments. Claims: ambitious mech interp has usable feedback loops (feature quality by
explanation-simulated substitution; circuit faithfulness by causal scrubbing or successors); the strongest metrics give
zero for every current method, so progress = climbing to stronger metrics. Cites Gao et al. 2025 (arXiv 2511.13653):
weight-sparse transformers give circuits of ~half a dozen attention channels/neurons, validated by mean-ablating
everything outside the circuit with means from the *pretraining* distribution. Stated next steps: (i) mean ablation is
weaker than causal scrubbing — design better metrics and hill-climb them; (ii) random nodes are less interpretable than
circuit nodes; (iii) bridges or gradient routing to sparsify only a slice of an existing model; (iv) Jacobian SAEs,
SPD/APD as alternatives. Leogao's later post "Neural networks are not already clean" (Dkh7pXKjoNWkkxQDz, 2026-10-17,
368 karma) argues for downstream-KL simulation scores over activation-vibes; it is a reply to Goodfire's "Already
Clean" essay (https://already-clean.goodfire.com/), i.e. the neuron basis vs learned-basis debate is live right now.

### 1b. Weight-Sparse Circuits May Be Interpretable Yet Unfaithful (jacob_drori, sHpZZnRDLg7ccX9aF, 2026-02-09)
Anthropic Fellows project. Replicates Gao et al. on SimpleStories with 2-layer models: dense d_model=128 (1.4M
nonzero), sparse d=1024 (1/64 nonzero), d=3072 (1/200), d=4096 (1/500); 2B training tokens each; trained with bridges
(unused in results). Pruning = learn a binary node mask (Heaviside, sigmoid surrogate gradient, 2000 AdamW steps,
batch 64 task datapoints, hyperparameters from a CARBS sweep) minimising task CE + k_coef * circuit size; masked nodes are
*completely* ablated (zero or pretraining-mean). Tasks: pronoun ("when leo ran to the beach, he"), simplified IOI
("when leo went to the shop, mia urged him", binary CE on him/her), question marks.
Findings: zero ablation gives smaller circuits than mean ablation (opposite of what leogao reports in comments);
sparse models mostly have smaller circuits than dense (replicates Gao Fig. 2; weaker on questions). Four unfaithfulness
results:
1. Nonsense task (male name -> "is", female -> "when"): pruned circuit gets CE < 0.05 with ~30 nodes (real task ~10).
2. Pronoun circuit in d=1024 has value nodes in L1H7 but no q/k nodes -> uniform attention; the original head attends
   strongly to the name.
3. Nodes change role: e.g. L0 node 1651 (d3072 IOI) negative on female names in pruned model, positive on male names in
   original; attn_out L1 node 244 (d1024 IOI); mlp_out L1 node 1455 (d3072 questions).
4. IOI generalisation: prune on opposite-gender prompts only; "good circuit" = copy gender of name_1, "bad circuit" =
   opposite gender of name_2. d=3072 model: 89% correct opposite-gender, P_correct = 0.81 same-gender. Over 100 pruning
   seeds (77 reach CE < 0.15) the same-gender P_correct histogram has a big spike at 0: pruning often finds the bad
   circuit. Freezing layernorm scales enlarges circuits and helps d=3072 but hurts d=1024.
Author's suggested next steps: (1) a good faithfulness metric (causal scrubbing maybe too strict; a "top-20 important
nodes in circuit" metric scored badly everywhere but he distrusts it), (2) modify pruning to be faithful under it,
(3) re-check whether weight-sparse models still have smaller circuits; also apply the same scrutiny to attribution
graphs (look for qualitatively wrong predictions on unseen prompts).
Comments: leogao (32 karma) wants more rigorous faithfulness metrics and is curious about LN-free models. **Lucius
Bushnaq (27 karma): same thing seen when pruning parameter-decomposition graphs; proposed fix = do not ablate
completely, let an adversary choose which non-circuit nodes to ablate/keep (gradient ascent on masks), with the
adversary restricted to one ablation pattern per batch so it cannot exploit per-input noise; "this way you also don't
need to freeze layer norms".** Nobody replied with an implementation.

### 1c. [Linkpost] Interpreting Language Model Parameters (Bushnaq et al., eAQZaiC3PcBhS4HjM, 2026-05-05; arXiv 2610.20748)
VPD: decompose each weight matrix into rank-1 subcomponents + a Delta component; a causal-importance (CI) function
predicts per token which subcomponents may be ablated; trained with stochastic-subset and persistent-PGD adversarial
reconstruction losses (KL to target output). Target: 4-layer, d=768, 6-head LlamaSimpleMLP, 67M params (28M
decomposed), trained on Pile-uncopyrighted, tokenizer EleutherAI/gpt-neox-20b, ctx 512. Decomposition: 38,912
subcomponents (per layer: c_fc 3072, down_proj 3584, q 512, k 512, v 1024, o 1024), ~10k alive. Paper sections:
attention decomposition (subcomponents span heads), attribution graphs with two pruning types — type 1 with
stochastic+adversarial mask sampling, type 2 with CI-only masks. Claim: type 2 graphs are smaller, look
interpretable, score ~100% (better than the model) and are unfaithful; "we believe this issue is likely to apply in
any setting in which masking-without-adversarial-sampling is used to identify subsets of nodes ... which includes a
large fraction of the neural network subgraph identification literature" (footnote cites Drori's post and Lucius's
comment). Other claims: no feature splitting; better recon/sparsity trade-off than PLTs/CLTs; hand edit of an emoticon
subcomponent. Limitations they list: adversarial robustness poor at many PGD steps (KL 0.83 at 20 steps, 40.2 at 320);
better CI functions; clustering; data-subset decompositions; **"Better model editing ... hybrid approaches ... LoRA with
singular vectors restricted to those of specific subcomponents"**; projecting gradients / fine-tuning diffs into the
subcomponent basis.

### 1d. Exploration: fine-tuning with parameter decomposition (Lucius Bushnaq, ieoWstubDQWLrMnhH, 2026-06-25)
Same 67M model + decomposition. Objective: maximise German CE (capped at uniform, ln 50277 = 10.83 nats) with a KL
penalty to the original model on *English-only* Europarl (an admitted mis-specification). Trainable parameters = mask
scalars of selected subcomponents (start at 1). Top-16 by mean CI(German) - CI(English): beats rank-1 LoRA (adapters on
all 24 matrices, ~55k params) at small German-token budgets, LoRA wins at large budgets; both wreck French/Spanish/
Italian. Single subcomponent `h.3.attn.v_proj:513` (only autointerp label mentioning German alone): "inverting" solution
(mask ~ negative) reaches German-at-chance with < 0.1 nats English damage from ~4 German tokens (LoRA r=1 and r=4 need
~32), and leaves French/Spanish nearly untouched; Italian is damaged (component is really German+Italian function
words). Localised rank-1 LoRA on the layer-3 V matrix still damages fr/es/it. Protocol: budgets 2..2048 tokens, 9
seeds, lr tuned per (method, budget) on a dev split, runs to EMA plateau (300-1700 steps), eval on parallel Europarl
de/fr/es/it, pile_val, codeparrot/codeparrot-clean-valid. Caveats the author states: n = 1 target, 1 decomposition, 1
model; German tokens were already "spent" in decomposition + autointerp; model is weak at German. Fine-tuning code is
NOT public ("really basic stuff an agent hacked together"). Footnote: an L1 penalty on mask changes (no manual
selection) "seemed to work" but was not followed up. Comments: StefanHex asks whether an SAE would have done the same —
Lucius: hard to define the SAE analogue (not a weight basis), maybe a steering vector; Daniel Tan asks for a public
demo. No one has run any comparison basis.

## 2. Follow-ups that already exist (checked)
- **Do VPD's Explanations Aggregate? An Audit of the Released Decomposition** (Tom Angsten, KeBccWBGXnNXzZFBp,
  2026-09-30, 29 karma). On the released 67M decomposition: aggregating 64 donor tokens' worth of needed components
  (~4,500) gives KL 0.80 nats (paper's 20-step adversary: 0.83); similar donors hurt more; deleting all never-needed
  components costs 1.28 nats; hard-deleting 256 / 1,007 code-specific components costs 0.67 / 3.34 nats on code vs 0.03 /
  0.21 on prose (random matched controls 0.08 / 0.98 on code). No-adversary decomposition is 4-7x worse. Code:
  https://github.com/angsten/vpd-audit (pins goodfire-ai/param-decomp at commit 74146b5 = tag `vpd-paper`; ran on
  A100 40GB; all measurements ~ $40 at $2.10-2.50/A100-h).
- **VPD's Evaluation Adversary Finds Systematic Defects in the Released Decomposition** (Angsten, tGdKJPmyaiHnqkLem,
  2026-10): adversarial masks found on one batch transfer to unseen batches. Code: https://github.com/angsten/vpd-audit-2.
- Lee Sharkey's reply (2026-10-17): Goodfire re-ran the audit on a newer unpublished decomposition; improved but headline
  issue remains; working on a stronger adversary. => auditing VPD's aggregation faithfulness is DONE; do not propose.
- **Targeted Recovery of Weight-Space Mechanisms** (Vigouroux & Sharkey, arXiv 2607.13047): targeted PD (tPD), a
  CSS-only submodel of the 4-block model at 7% of the FLOPs; ablate/rewire memorised sequences in a 12-block model.
  => "data-subset decomposition" is DONE by the authors.
- **Weights Read and Write Features** (ASPD, arXiv 2609.37731): activation-grounded parameter decomposition on Qwen-3-8B.
- **Individual Parameters in Weight-Sparse Transformers Appear Interpretable** (Marin-Llobet & Heimersheim, arXiv
  2607.02964): LLM pipeline describing when a single weight matters; 12-31% of sparse-model weights interpretable. Not a
  circuit-faithfulness fix.
- **Comparing Sparsified MLPs and Transcoders** (Shabalin & Piotrowski, arXiv 2610.24521) and "Takes on Already Clean"
  (neverix, p6kaX6LqfTHFqC6r6): neuron-basis interpretability; no editing comparison against parameter subcomponents.
- (*) Found NO work that puts stochastic/adversarial masking into the Gao/Drori weight-sparse pruning algorithm and
  re-runs Drori's failure tests. arXiv queries ("weight-sparse transformers", "circuit discovery adversarial
  faithfulness", etc.) and pingbacks of sHpZZnRDLg7ccX9aF (only the VPD linkpost, Angsten's audit, neverix's post) show
  nothing.
- (*) Found NO replication or extension of the single-scalar German result (pingbacks of ieoWstubDQWLrMnhH: none), and no
  comparison of subcomponent edits against neuron / SVD bases.

## 3. Verified public artefacts
Weight-sparse line:
- Code: https://github.com/jacobcd52/sparse_pretrain_public (MIT). `python -m src.pruning.run_pruning --model <hf repo>
  --task pronoun`; `src/pruning/config.py` (ablation_type zero|mean_pretrain|mean_task, freeze_layernorm_scale,
  num_steps 2000, batch 64, target_loss 0.15), `src/pruning/masked_model.py`, `src/pruning/tasks.py` (pronoun, the
  is/when nonsense task `DummyPronounIsWhenTask`, IOI strict/relaxed/mixed, tense, ...). Raw files fetched OK.
- Checkpoints (public, ungated, HF): `jacobcd52/ss_bridges_d1024_f0.015625`, `jacobcd52/ss_bridges_d3072_f0.005`
  (sparse_model.bin 503 MB), `jacobcd52/ss_bridges_d4096_f0.002`, dense `jacobcd52/ss_d128_f1`; also
  `ss_bridges_d3072_f0.0039`, `ss_bridges_d4096_f0.001`, `ss_bridges_d1024_f0.015625_t10B`, PLT/CLT transcoders on the
  dense model (`jacobcd52/ss_d128_f1_plt_k30_e32`, `..._clt_k30_e32`, ...). Dataset `jacobcd52/simplestories-tokenized`;
  tokenizer `SimpleStories/SimpleStories-1.25M` (vocab 4096).
- Circuit viewer: https://jacobcd52.github.io/circuit-visualizations/.
- OpenAI original: https://github.com/openai/circuit_sparsity, HF `openai/circuit-sparsity` (Python-code models; no
  pruning code per Drori).
Parameter decomposition line:
- Code: https://github.com/goodfire-ai/param-decomp (main is now a JAX engine whose reference config needs 32 GPUs;
  the paper's Torch code is at tag `vpd-paper` / commit 74146b5, with `param_decomp/editing/_editing.py` providing
  `EditableModel.from_wandb`, `make_edit_fn`, `without_components`, `measure_kl`). `nano_param_decomp/` is mentioned in
  the README but the path 404s on main.
- W&B runs (public; files download ANONYMOUSLY through `https://api.wandb.ai/files/goodfire/spd/<run>/<file>` — I got
  HTTP 206 on range requests without any key; Angsten's README says a free W&B key is needed, which is not the case
  for this route):
  - target model `goodfire/spd/t-9d2b8f02`: `model_step_99999.safetensors` 268 MB, `model_config.yaml`.
  - main decomposition `goodfire/spd/s-55ea3f9b`: `model_400000.pth` 2.9 GB. Trained 92,711 s on 8x H200
    (= 206 H200-hours).
  - no-adversary control `goodfire/spd/s-05ef623e`: `model_400000.pth` 2.9 GB (68,543 s on 8x H200).
  - SimpleStories 2-layer decomposition `goodfire/spd/s-eab2ace8`: `model_400000.pth` 98 MB, 56,720 s on 1x H200
    (15.8 H200-hours); target `goodfire/spd/runs/gf6rbga0`.
  - PLT/CLT comparison runs in W&B `mats-sprint/pile_local_sweep_jose` etc. (weights stored as artifacts; not checked
    for anonymous download).
  - Autointerp labels / harvest DBs (`HarvestRepo`, `InterpRepo`) do not appear to be public; plan around not having
    them.
- Data: `danbraunai/pile-uncopyrighted-tok-shuffled`, `monology/pile-uncopyrighted` (has per-document subset names),
  `Helsinki-NLP/europarl`, `codeparrot/codeparrot-clean-valid` — all public, ungated.
Prices looked up 2026-11-14:
- RunPod on-demand (https://www.runpod.io/pricing): A40 48GB $0.59/h, RTX A6000 $0.69/h, RTX 4090 $0.89/h, L40S
  $1.09/h, A100 PCIe 80GB $2.09/h (community from $1.19), H100 PCIe $2.89/h, H200 $5.29/h.
- OpenRouter: anthropic/claude-haiku-5.5 $0.10 / $0.50 per M tokens in/out; claude-opus-4.8 $5 / $25; claude-fable-5.2
  $8 / $40.
- Implication: re-running the Pile-4L VPD decomposition = 206 H200-h x $5.29 = ~$1,090 (over budget); the SimpleStories
  2L decomposition = 15.8 H200-h = ~$84 per run before any hyperparameter search.

## 4. Brainstorm (all candidates, with verdicts)
1. **Put Lucius's adversarial/stochastic masking into Drori's weight-sparse pruning and re-run the four failure tests
   + the sparse-vs-dense circuit-size comparison.** Achievable (all checkpoints + pruning code public; 2-layer models;
   runs are minutes). Natural next step named by both Drori (steps 1-3) and Lucius (the fix), and it tests the VPD
   paper's sweeping claim about non-adversarial subnetwork methods on an independent test bed with known failures.
   Interesting both ways. -> **Proposal 01.**
2. **Many-target, multi-basis replication of single-scalar unlearning** (VPD subcomponent vs no-adversary subcomponent
   vs MLP neuron vs SVD direction vs LoRA; ~12-15 targets; automatic selection with token accounting). Achievable
   (released checkpoints, edited model is plain weights W - (1-s) u v^T; tiny model). Answers the post's n = 1 caveat
   and StefanHex's "would another basis do the same?" question; topical given the neuron-basis debate. -> **Proposal 02.**
3. Run Drori's faithfulness battery on VPD attribution graphs using the public SimpleStories-2L decomposition (type 1
   vs type 2 pruning on pronoun/IOI prompts with a same-gender held-out test). Worth doing, cheap, but it is the mirror
   image of #1 and the paper already shows type-2 graphs are unfaithful on its own examples. Kept as stage 2 of
   proposal 01 rather than a separate proposal (proposals must be distinct).
4. VPD-decompose a weight-sparse model and ask whether subcomponents coincide with the sparse model's nodes/weights.
   Elegant bridge between the two agendas, but one decomposition of a 2L SimpleStories model cost 15.8 H200-h with
   tuned hyperparameters; a d=1024..3072 sparse model has far larger matrices and needs its own tuning; Goodfire calls
   the released recipe "pretty bad" and the new JAX recipe assumes multi-GPU. High risk of ending with an unconverged
   decomposition. Rejected for stage 1; possible stage 2.
5. Re-train the Pile-4L decomposition with a better adversary (start PGD from other inputs' CI patterns, as Angsten and
   the paper suggest). ~$1,090 per run; Goodfire is already doing it. Rejected (cost, duplication).
6. Audit the newer Goodfire decomposition. Not released as a paper artefact; Lee Sharkey already re-ran the audit.
   Rejected (done).
7. Attribution-graph faithfulness: find prompts where transcoder attribution graphs predict the wrong behaviour on
   unseen prompts (Drori's last suggestion). Good question, public tooling exists for Gemma-2-2b, but it needs a new
   task battery built from scratch and shares little infrastructure with this cluster; lower confidence of a crisp
   result in two days. Rejected for this cluster (would suit a transcoder/attribution cluster).
8. Hybrid LoRA with singular vectors tied to chosen subcomponents (paper's future-work item). Natural extension of #2;
   included as a stage-2 item there rather than standalone, since without the #2 baseline grid it is uninterpretable.
9. L1-on-mask-changes fine-tuning without manual component selection (post footnote 2). Cheap; folded into #2 as an
   optional arm.
10. Project a fine-tuning weight diff (e.g. a narrow fine-tune) into the subcomponent basis to "read" what training
    changed. The 67M model is too weak for safety-relevant fine-tunes (it "sucks at almost everything"); result would be
    hard to make people care about. Rejected.
11. Sparsify a slice of an existing model with bridges / gradient routing (leogao's suggestion). Requires training
    sparse models with bridges (2B tokens each) plus new method development; too long/fragile for two days. Rejected.
12. Train LN-free weight-sparse models (leogao's curiosity in comments). Needs new 2B-token training runs with unknown
    cost on unfamiliar code; the adversarial fix in #1 is claimed to make LN freezing unnecessary, which #1 tests
    directly. Rejected.
13. Full causal scrubbing as the faithfulness metric for sparse circuits. Too strict by the authors' own account and
    needs a hypothesis per circuit; a resample-ablation variant is used as a held-out metric inside #1 instead.
14. Simulation-KL explanation scores (leogao's Oct post) for sparse vs dense neurons. Needs large LLM-labelling
    pipelines; partially done by arXiv 2607.02964 at the weight level. Rejected (duplication risk, other cluster).

## 5. Why two proposals
Both clear the bar: they reuse released checkpoints and code end to end, cost well under $500, are named next steps
in the posts/comments, are not yet done as far as I could verify, and give a publishable answer in either direction.
They are distinct projects (circuit-discovery faithfulness on weight-sparse SimpleStories models vs model editing on the
Pile 67M decomposition) sharing no code or checkpoints.

Design points a reviser should keep:
- Proposal 01: under interpolating masks the all-nodes-on setting is one of the adversary's options, so a circuit can
  never be required to beat the model; the pruning objective must be KL/CE-relative-to-model, and an arm with
  "complete ablation + KL-to-model objective" is needed to separate the objective change from the adversary. The
  nonsense-task failure then disappears by construction (say so; do not sell it as a finding). The informative tests
  are attention-pattern recovery, node-role agreement, same-gender generalisation, and size-vs-robustness curves.
- Proposal 02: selection must use the same recipe and token budget for every basis, and an "oracle top-20" variant
  should give each basis its best shot; report selection tokens separately from fine-tuning tokens (the post's
  "cheating" caveat). Keep the English-only preserve set, since the headline claim is about what is spared *without*
  being asked.
