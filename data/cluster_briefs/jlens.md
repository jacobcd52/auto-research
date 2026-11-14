# Cluster: Jacobian lens / global workspace lenses

key: `jlens` — 7 post(s); write at most 3 proposal(s).

## A global workspace in language models
- id: `3PaLrzxagpbnNtPLT` | 2026-07-06 | 372 karma | wesg
- url: https://www.lesswrong.com/posts/3PaLrzxagpbnNtPLT/a-global-workspace-in-language-models
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Blog post for Anthropic's paper 'Verbalizable Representations Form a Global Workspace in Language Models'. Using a Jacobian-based lens (J-lens), they identify a sparse set of token-linked directions (the J-space) in Claude that the model can report on and modulate on request, that carry intermediate steps of silent multi-step reasoning and causally mediate it, and whose ablation leaves fluent behaviour intact but impairs higher-order reasoning. They use it to surface unverbalised thoughts (eval awareness, fabricating data, planted hidden goals); code and a Neuronpedia demo on open-weight models are released.
- screener's follow-up note (often the screener's inference): Replicate and stress-test J-lens on open-weight models (e.g. hidden-goal model organisms, eval awareness), compare against logit lens/SAEs, and test the J-space ablation/steering claims.
- builds on: Logit lens / tuned lens; Global workspace theory (Baars; Dehaene & Naccache)

## A Review of Anthropic's Global Workspace Paper
- id: `zFJ3ZdQwrTWE9jT5S` | 2026-07-06 | 137 karma | Neel Nanda
- url: https://www.lesswrong.com/posts/zFJ3ZdQwrTWE9jT5S/a-review-of-anthropic-s-global-workspace-paper
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Neel Nanda's invited public review of the Anthropic global-workspace paper. He accepts the core claim that a 'cognitive space' for intermediate variables exists and that J-lens accesses it (and is cheap: ~10 prompts of 128 tokens), is more cautious about fine-grained properties and the global-workspace analogy, and reports an independent replication of the core claims on Qwen 3.6 27B plus preliminary evidence of abstract 'interpretative meta-tokens' (e.g. Chinese characters for 'what does this mean') that play a causal role on ambiguous sentences.
- screener's follow-up note (often the screener's inference): Evaluate J-lens as an auditing/hypothesis-generation tool against SAEs and natural language autoencoders, look for alternative explanations of the section-4 properties, and extend the meta-token finding across models.
- builds on: A global workspace in language models / Verbalizable Representations Form a Global Workspace in Language Models (http://transformer-circuits.pub/2026/workspace/index.html)

## R-lens: Making J-lens More Faithful on Early Layers
- id: `nv8oedrnLXKRzNEL9` | 2026-08-05 | 89 karma | camilablank, agam_bhatia, Neel Nanda
- url: https://www.lesswrong.com/posts/nv8oedrnLXKRzNEL9/r-lens-making-j-lens-more-faithful-on-early-layers
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): MATS work (Nanda stream) introducing R-lens, a drop-in replacement for the Jacobian lens that applies layer-wise relevance propagation rules (stop-gradients, e.g. on LayerNorm variance) in the backward pass. They report cleaner, less incoherent early-layer readouts, larger gains as models scale, more causally important directions under ablation, and occasional recovery of concepts J-lens misses; models mentioned include Qwen3.6-27B and DeepSeek-V4-Flash. Lenses are open-sourced.
- screener's follow-up note (often the screener's inference): Apply R-lens to other models/tasks, compare against tuned/logit lens and SAE readouts on early layers, and test whether the extra early-layer concepts are causally used.
- builds on: J-lens (Jacobian lens); Relevance Patching (RelP); Layer-wise Relevance Propagation (arXiv:1604.00825)

## WorkspaceBench: Evaluating Interpretability Methods for the Global Workspace
- id: `Zeg2JztbdhguL48uH` | 2026-09-23 | 64 karma | camilablank, agam_bhatia, Euan Ong, Neel Nanda
- url: https://www.lesswrong.com/posts/Zeg2JztbdhguL48uH/workspacebench-evaluating-interpretability-methods-for-the
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Introduces WorkspaceBench, 3,356 questions across 27 eval families testing how well activation-to-text tools recover intermediate variables in Qwen-3.6-27B's forward pass, plus a hallucination-focused eval. Compares logit lens, tuned lens, J-lens, R-lens, NLAs, SAEs, Patchscopes, template lens and oracle lens on accuracy versus hallucination; benchmark is open-sourced.
- screener's follow-up note (often the screener's inference): Evaluate new or improved lenses on the benchmark, adapt it to smaller models, and tighten controls against shortcut solutions such as text inversion.
- builds on: J-lens / global workspace (transformer-circuits.pub/2026/workspace); R-lens: making J-lens more faithful on early layers; Natural Language Autoencoders; Patchscopes (arXiv 2401.06102); Towards surfacing model algorithms with meta-tokens in the J-lens

## J++ Lens: Jacobian Filtering Enables More Faithful Workspace Lenses
- id: `nc9dHfcB22JdMzGbr` | 2026-10-08 | 123 karma | Kola Ayonrinde
- url: https://www.lesswrong.com/posts/nc9dHfcB22JdMzGbr/j-lens-jacobian-filtering-enables-more-faithful-workspace
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Improves the J-Lens by down-weighting Jacobians from activations that give poor readouts, applying layer-wise relevance propagation in the backward pass, and removing non-semantic tokens. On latent-variable extraction tasks across 9-284B models, J++ reaches 55.2% recall@10 versus 35.7% for J-Lens and 37.7% for R-Lens, and surfaces intermediates at earlier layers; code, demo and lenses are released.
- screener's follow-up note (often the screener's inference): Evaluate J++ on WorkspaceBench and for monitoring eval awareness or unverbalised scheming; extend to multi-token readouts.
- builds on: J-Lens (transformer-circuits.pub/2026/workspace); R-lens: making J-lens more faithful on early layers

## Even GPT-2 passes most functional global workspace tests
- id: `GeKveaNdruATcj2Fj` | 2026-10-21 | 87 karma | Finn Cairns, yix, Zephaniah Roe
- url: https://www.lesswrong.com/posts/GeKveaNdruATcj2Fj/even-gpt-2-passes-most-functional-global-workspace-tests
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Re-runs the five functional global-workspace tests from Anthropic's workspace paper (Gurnee et al. 2026, J-lens) on GPT-2 small. GPT-2 passes verbal report, internal reasoning, flexible generalisation and selectivity but fails directed modulation, and lacks most of the supporting structure found in Claude; the authors argue four of the tests largely follow from how the J-lens is constructed and are weak evidence of a workspace.
- screener's follow-up note (often the screener's inference): Run the same tests across a size ladder of open models to find where directed modulation and the workspace-supporting structure emerge, and design tests that are not satisfied by construction.
- builds on: Gurnee et al. 2026, global workspace paper (https://transformer-circuits.pub/2026/workspace/); Eleos commentary on the GWT paper

## The Chain Lens [interim]
- id: `Nr6fksEqqxNpdz6rk` | 2026-11-11 | 63 karma | vgel, Raymond Douglas
- url: https://www.lesswrong.com/posts/Nr6fksEqqxNpdz6rk/the-chain-lens-interim
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Interim paper draft introducing the chain lens, which extends single-token lenses (logit lens, J-lens) to multi-token readouts by contrastive decoding on a multi-token-prediction head (available in Qwen3.5+). On WorkspaceBench it beats the J-lens (0.42 vs 0.32 macro over 28 families) and a hindsight composite of untrained lenses (0.49 vs 0.41), and beats the trained oracle lens on arithmetic-chain intermediates (0.42 vs 0.25); readouts remain fragmentary.
- screener's follow-up note (often the screener's inference): Apply the chain lens to safety-relevant hidden reasoning (e.g. no-CoT computation or concealed intent), test on more models, and improve relational structure of the readouts.
- builds on: Gurnee et al. 2026, J-lens / global workspace paper; Logit lens; Activation Oracles (https://arxiv.org/abs/2512.15674); Patchscopes (https://arxiv.org/abs/2401.06102); WorkspaceBench

