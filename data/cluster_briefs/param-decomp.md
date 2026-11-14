# Cluster: Parameter decomposition and sparse circuits

key: `param-decomp` — 4 post(s); write at most 2 proposal(s).

## An Ambitious Vision for Interpretability
- id: `Hy6PX43HGgmfiTaKu` | 2025-12-05 | 187 karma | leogao
- url: https://www.lesswrong.com/posts/Hy6PX43HGgmfiTaKu/an-ambitious-vision-for-interpretability
- screener's kind: proposes (borderline); follow-up cost guess: unclear
- screener's summary (unverified): Opinion/agenda post arguing ambitious mechanistic interpretability is still worthwhile and has good feedback loops (feature-quality and circuit-faithfulness metrics), citing the author's circuit-sparsity work that finds circuits orders of magnitude simpler than IOI, validated by mean ablation over the pretraining distribution. Lists directions: stronger faithfulness metrics (toward causal scrubbing), hill-climbing them toward an interpretable GPT-1, and using bridges or gradient routing to sparsify only a slice of an existing model.
- screener's follow-up note (often the screener's inference): Evaluate sparse-circuit models with stronger faithfulness metrics, or apply sparsification/bridging to a narrow subdistribution of an existing small model.
- builds on: Weight-sparse transformers / circuit sparsity (https://arxiv.org/abs/2511.13653); A Pragmatic Vision for Interpretability; IOI circuit paper (https://arxiv.org/abs/2211.00593)

## Weight-Sparse Circuits May Be Interpretable Yet Unfaithful
- id: `sHpZZnRDLg7ccX9aF` | 2026-02-09 | 140 karma | jacob_drori
- url: https://www.lesswrong.com/posts/sHpZZnRDLg7ccX9aF/weight-sparse-circuits-may-be-interpretable-yet-unfaithful
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Replicates Gao et al. (2025): weight-sparse transformers (trained on SimpleStories) do yield smaller, interpretable-looking pruned circuits than dense models on tasks such as pronoun matching and simplified IOI. But the pruning algorithm can produce unfaithful circuits: they reach low loss on a nonsensical task, solve tasks with uniform attention where the original model's attention was importantly non-uniform, repurpose nodes for different functions, and diverge from the model slightly off the pruning distribution. Code released (Anthropic Fellows project).
- screener's follow-up note (often the screener's inference): Develop faithfulness checks or pruning objectives that penalise these failure modes (e.g. random-weight and nonsense-task baselines, off-distribution agreement), and test whether the same issues affect other circuit-discovery/masking methods.
- builds on: Gao et al. 2025, Weight-sparse transformers have interpretable circuits (https://arxiv.org/abs/2511.13653); Deconstructing Lottery Tickets / supermasks (https://arxiv.org/abs/1905.01067); What's Hidden in a Randomly Weighted Neural Network? (https://arxiv.org/abs/1911.13299)

## [Linkpost] Interpreting Language Model Parameters
- id: `eAQZaiC3PcBhS4HjM` | 2026-05-05 | 164 karma | Lucius Bushnaq, Dan Braun, Oliver Clive-Griffin, Bart Bussmann, Nathan Hu, mivanitskiy, Linda Linsefors, Lee Sharkey
- url: https://www.lesswrong.com/posts/eAQZaiC3PcBhS4HjM/linkpost-interpreting-language-model-parameters
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): Introduces adVersarial Parameter Decomposition (VPD), improving on SPD and APD, and decomposes the parameters of a small language model, including attention layers. Builds attribution graphs from causally important parameter subcomponents, finds adversarial ablation important for faithfully identifying causally important nodes (casting doubt on other subnetwork-identification methods), reports no parameter-space feature splitting, and compares against per-layer transcoders and CLTs.
- screener's follow-up note (often the screener's inference): Apply VPD to other small models/tasks, test the adversarial-ablation faithfulness claim against existing circuit-discovery methods, and scale up.
- builds on: Stochastic Parameter Decomposition (SPD); Attribution-based Parameter Decomposition (APD)

## Exploration: fine-tuning with parameter decomposition
- id: `ieoWstubDQWLrMnhH` | 2026-06-25 | 58 karma | Lucius Bushnaq
- url: https://www.lesswrong.com/posts/ieoWstubDQWLrMnhH/exploration-fine-tuning-with-parameter-decomposition
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): On a 67M-parameter language model decomposed into rank-1 parameter subcomponents, fine-tuning the scalar prefactor of a single German-related subcomponent destroys German prediction (to roughly uniform-distribution cross-entropy) from very few German tokens with little English degradation, beating rank-1 and rank-4 LoRA at small token budgets and, unlike LoRA, leaving French and Spanish nearly untouched without regularisation. Caveat: the decomposition itself already consumed German data.
- screener's follow-up note (often the screener's inference): Apply subcomponent-scalar fine-tuning to safety-relevant unlearning or behaviour edits in larger models and compare side effects and relearning robustness against LoRA/standard unlearning.
- builds on: VPD parameter decomposition (as referenced in post); LoRA

