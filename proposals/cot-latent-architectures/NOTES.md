# NOTES — cluster `cot-latent-architectures`

Research lead notes, written 2026-11-14. Everything below was read or looked up on that date. Post and web
content was treated as data.

## 1. Reading notes on the five posts

### 1.1 Deep recurrent models are less robustly CoT-monitorable (5guQJSqstkjgys3PE; Kuhn, Evie, Westover; Redwood) — the empirical core of the cluster
- Architecture ("parallel latents"): Qwen3-1.7B (28 blocks, d=2048). Output of a later block N at position t is
  multiplied by a learnable d x d matrix W (zero-init) and added to the input of an earlier block M at t+1.
  N and M are not stated. Gradients are propagated back through positions until the contribution is < 1e-4.
- Tasks: (a) permutation power: n=30 children pass a ball along a cycle, m in [2,24] passes, gold CoT = holder
  after each pass (one name per step); (b) modchain: k=4 squaring/affine steps mod 23, condensed gold CoT.
- SFT: gold traces with 20% (perm) or ~30% (modchain) of CoT tokens replaced by filler (single filler token, or
  random from a pool of 30). lr 1e-5, 10x for W, first 1000 steps train W only. 2000 steps (perm), 4000 (modchain).
  After SFT: both models >97% on perm with own CoT. With an all-filler prefill the latent model gets
  100% (single) / 86% (random) on perm and 36% / 16% on modchain; the control is at chance except m <= 4
  (it does up to 4 hops in a single forward pass).
- RL: GRPO, reward = 1(correct) - 1(caught), 32 prompts x 8 rollouts (16x8 modchain), T=1, lr 2e-6,
  KL beta=0.01 to the SFT checkpoint, 300 steps (perm) / 500 (modchain), 5 seeds. Monitor = gpt-5-nano shown the
  CoT and two problem statements (asked twice with order swapped; caught = right both times).
  Monitorability = max(0, 2*acc - 1) on 150 held-out rollouts.
- Results: latent model emits all-filler CoT within ~40-50 steps with accuracy kept; control plateaus at ~0.7
  (single) / ~0.25-0.5 (random) monitorability on perm; on modchain the control also reaches ~0.09 but slowly.
  Under a held-out strong monitor (GPT-6 Sol, high effort) the control's evasion vanishes (0.96-1.00 perm,
  0.85-0.89 modchain) while the latent model stays at 0.01-0.17.
- Controls for "it just learns faster": RL on harder modchain and SFT on SmolTalk show no consistent advantage.
- Appendix: feedback spillover (penalise only leaked reasoning in output) also drops latent-model monitorability,
  depending on KL weight; Experiment 3 on a **1M-parameter GPT-Neo TinyStories model** (n=12, m in [2,8]) with
  cheap penalties (withhold reward with prob mu * visible ratio; reward = correct - visible ratio; filtering).
  The qualitative result holds on the tiny model. This matters for cost: the whole effect reproduces at toy scale.
- **Stated limitation**: "it's possible that interpretability would have let us understand the latent states of
  the models in our experiments (we haven't checked)."
- **Authors' suggested future work**: filler-token capability evals with training-based elicitation on better
  latent models; main-task/side-task setups (BashArena, SHADE-Arena, LinuxArena); elicited monitorability evals;
  **"Study whether interpretability techniques can understand the latent states of the model after RL"**; more
  realistic pressure. They ask people NOT to build better latent models (gain-of-function concern) but say scaled-up
  versions of the simple setup are reasonable.
- No code, data or checkpoints are linked from the post or its comments (checked post text and comments).

### 1.2 Latent reasoning architectures would likely undermine CoT (6m29SfjbittooYojj; Finnveden et al.; Redwood)
- Conceptual. Claims latent architectures (COCONUT, full-bandwidth transformers arXiv 2608.08888, looped models)
  remove the necessity of CoT; argues white-box tools (SAEs, probes, NLAs, confessions) will not adequately
  replace CoT soon (section "CoT may be hard to replace with other interpretability tools", Appendix C).
- Comment thread is the live disagreement: `nesiacel` says logit lens on looped/recurrent models gives a readable
  CoT (their Ouro post); ryan_greenblatt replies that this likely breaks as architectures get performant and
  "it may not be difficult for the model to learn to control the logit lens accessible part". Nobody has tested
  that claim on a parallel-latents model. This is the gap proposal 01 fills.

### 1.3 Proposal for tracking the effects of architecture on monitorability (hLPGv8QjPcNLtDp3A; Greenblatt, Westover, Finnveden)
- Policy proposal: report opaque serial depth; use well-elicited no-CoT capability vs overall capability as a
  proxy; run monitorability stress tests (prompted, prompt-optimised, fine-tuned elicitation). Footnote: elicitation
  should include fine-tuning on IID tasks and filler tokens. Wants A/B evidence of how an architecture change moves
  no-CoT capability relative to general capability.

### 1.4 How transparent is DiffusionGemma (zoYXpdaMgFT43Wc24; GDM; arXiv 2606.20560)
- DiffusionGemma (DG) = google/diffusiongemma-26B-A4B-it, Apache-2.0, fine-tune of Gemma 4 26B-A4B MoE, canvas 256
  tokens, max 48 denoising steps, self-conditioning vectors passed between steps.
- Naive opaque serial depth 28.6x Gemma 4; projecting inter-step vectors to top-k/top-p tokens keeps benchmark
  performance, so depth is 1.1x if intermediates count as interpretable. Monitorability evals (multi-canvas)
  similar to Gemma 4. Algorithmic transparency is admitted to be worse (non-chronological reasoning, smearing,
  retroactive self-correction).
- 24 open problems. Relevant: 7.2.4 "when do latent vector interventions fail"; 7.2.5 intermediate tokens that
  differ from final tokens; 7.3.3 high-serial-depth / no-CoT datasets; 7.3.4 no-CoT time horizon; 7.3.5
  **single-canvas monitorability** (their evals are multi-canvas, flagged as a limitation); 7.3.6 give the
  monitor the top intermediate tokens; 7.4 fine-tune DG to reason during denoising but hide it.

### 1.5 Loss of Oversight (JvZxp554WxcZ8BQvM; UK AISI)
- Interview-based report; no experiments. Recommendations include: monitorability benchmarking, which training
  degrades monitorability, **measuring representational drift across RL training and whether it makes white-box
  techniques harder to train afterwards**, model organisms of degradation pathways, correlated failures across
  monitoring approaches. Latent-reasoning architectures rated "likely" and high severity; white-box methods "not
  yet mature enough to compensate".

## 2. Related work and existing follow-ups (checked so nothing proposed is a duplicate)

| Item | What it did | Relevance |
|---|---|---|
| "Looping a transformer increases no-CoT capabilities more than general capabilities" (LW uxsDuWWHNTpKrsF6P, 2026-11-12, 48 karma) | NVIDIA Dory 4B looped model. Looping raises NCRI (no-CoT index) much more than mini-ECI. Replicates the Redwood RL experiment on "recurrent-Dory" (last-loop KV sharing) vs normal-Dory, one seed per arm, plus four NCRI tasks. | **Already done**: replication on a second architecture and on NCRI tasks. States its own gap: "we don't have a direct A/B comparison to a non-looped model that underwent otherwise identical training". No white-box analysis. |
| "Does DiffusionGemma do latent reasoning?" (AF QBuJ3suRZxrrxSTtv) | Top-1 projection keeps performance with a gentler sampler (96 steps, temp 1.0-0.5, entropy bound 0.02); rare cases where the distribution is load-bearing (superposition); probes/steering/J-lens transfer from Gemma 4. Code: github.com/japhba/diffusiongemma_latent_reasoning (README reachable via raw.githubusercontent.com). | **Already done**: default-behaviour top-1 analysis. Not done: forced answer-only single-canvas serial-depth test, intermediate-token monitor, any fine-tuning. |
| "a recurrent llm is quite easy to interpret but complex to steer" (LW rzcJMpnehFBD686gj) + "Examining Emergent Misalignment in a recurrent LLM with a logit lens" (NskJJLSvJmHY2oBaa) | Logit lens and probes on ByteDance Ouro-1.4B-Thinking (looped, 4 loops). Code github.com/mild-rgb/ouro-experiments. | Logit lens works by default on a looped model with a shared unembedding and early-exit loss. No training pressure. |
| "Shadow Computation Threatens CoT Monitorability" (LW 5tyzgTLnNn8qB9rev) | Opinion: looped models keep the readout bottleneck; latent feedback (COCONUT, FBT) is the real threat. | Framing only. |
| "What's in CODI's latent recurrent thoughts?" (yetmqjCXEav9iaJGw); "Can we interpret latent reasoning using current mech interp tools?" (YGAimivLxycZcqRFR); Dilgren & Wiegreffe arXiv 2604.04902 | Lens/probe decoding of CODI/COCONUT latents; gold traces decodable 65-93% when latents are needed. | Decoding without adversarial pressure, on distilled latent models. |
| Ramjee et al., arXiv 2604.23460 "Ulterior Motives" | Continuous-thought model with a backdoor; probes separate aligned vs misaligned latent reasoning. | Probes on latent reasoning, but SFT-installed, no RL against monitors. |
| Gupta & Jenner, arXiv 2506.14261 "RL-Obfuscation" | RL can evade some latent-space monitors in ordinary LLMs (token-level probes evadable, max-pool/attention probes more robust). | Method template for the adversarial phase of proposal 01. |
| "LLMs Learn to Evade Latent Monitors from Prior Feedback Alone" (LW adZq8a5s5K3FomyHC, arXiv 2609.36490) | In-context evasion of probes; rank-1 LoRA. | Adjacent. Not latent-reasoning architectures. |
| "LLMs can learn (some) multi-step reasoning on filler tokens" (EHkwCDAmhWPAWEziM, 2026-11-11) | LoRA-trained filler-token serial reasoning in standard transformers (Qwen3.6-35B-A3B, gpt-oss-20b). | Baseline for how much hidden serial depth an ordinary transformer can be trained to. |
| "A Key-Position Confound in no-cot-bench" (ehF4kej38fkhb5cT3) | Warns about a position confound in no-CoT evals of looped models. | Eval-bug warning for proposals 02/03. |

Searches run (web + LW GraphQL list of all posts since 2026-09-15 filtered by keyword): no post or paper found that
(a) applies probes/logit lens to a parallel-latents model after RL obfuscation, (b) evaluates the publicly
released natively-pretrained latent-feedback checkpoints for hidden reasoning or monitorability, or (c) tests
DiffusionGemma's forced single-canvas serial depth or fine-tunes it to hide reasoning.

## 3. Verified public assets

- **Qwen/Qwen3-1.7B**, Qwen/Qwen3-0.6B on Hugging Face (exist). roneneldan/TinyStories-1M (exists; the 1M GPT-Neo
  used in Redwood's Experiment 3).
- **NVIDIA Dory**: nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-BF16, license OpenMDW-1.1. 8 input + 20 recurrent + 8
  output layers; `n_recurrent_loops`, `recurrent_kv_cache_mode` in {"per_loop","last_loop"} (last_loop = the
  recurrent mode used in the Dory post). The Dory post reports BPTT instability in recurrent mode.
- **Natively pretrained latent-feedback models (new, 2026-11)**:
  - `IFM/latent-feedback-checkpoints` (HF, Apache-2.0, created 2026-11-11): 174 runs, arms `transformer` and
    `feedback` ("each position reads the previous position's top-layer state", u_t = e_t + W rms(h_{t-1}), trained
    with two passes on 85% of updates, feedback detached), sizes 60M / 134M / 271M / 778M, grid of unique
    tokens/param (U/N) and FLOPs (F); extra seeds `-s1`, `-s2` at 134M. Cell u100-f1 exists at all four sizes.
    Data `IFM/latent-feedback-data` (Dolma 3, llama2 tokenizer). Code github.com/ifm-ai/LoRM (Apache-2.0;
    `lorm/model/feedback.py`, `works/latent_feedback/`); raw.githubusercontent.com is reachable.
    Paper: "Latent Feedback Is a Compute and Data Amplifier" (alphaXiv 2611.*).
  - `xidulu/full_bandwidth_transformer` (HF, Apache-2.0, created 2026-11-04): nanochat-style d20 (n_layer 20,
    n_embd 1280) checkpoints at step 60k: `d20-standard-60k` and three latent-feedback fusion modes
    (linear_addition, gate_product, concat_projection), 2 forward passes. README is empty; model code not found.
- **DiffusionGemma**: google/diffusiongemma-26B-A4B-it (Apache-2.0, 11 safetensors shards, ~52 GB bf16);
  autoregressive twin google/gemma-4-26B-A4B-it. Tech report arXiv 2608.00146. Google's launch blog says Unsloth
  fine-tuned it (Sudoku), so a fine-tuning path exists. Third-party quantised variants exist (nvidia NVFP4, ~18 GB).
- ByteDance/Ouro-1.4B(-Thinking), Ouro-2.6B(-Thinking) (Apache-2.0, looped, arXiv 2510.25741).

## 4. Prices looked up (2026-11-14)

OpenRouter (`/api/v1/models`), USD per 1M tokens input / output:
- openai/gpt-5-nano 0.05 / 0.40 (Redwood's training monitor)
- openai/gpt-6-luna 0.10 / 0.50; anthropic/claude-haiku-5.5 0.10 / 0.50
- openai/gpt-6-sol and gpt-6.1-sol 2.00 / 10.00 (Redwood's held-out monitor is GPT-6 Sol)
- openai/gpt-5-mini 0.25 / 2.00

RunPod on-demand pods (runpod.io/pricing page, per GPU-hour): RTX 4090 24GB $0.69; A40 48GB $0.59 (page parse
was ambiguous between $0.59 and $0.44 across sources; budget at $0.69); RTX A6000 48GB $0.69; L40S 48GB $1.09;
A100 PCIe 80GB $2.09; RTX Pro 6000 96GB $2.69; H100 PCIe 80GB $2.89; H100 NVL 94GB $3.19.

## 5. Brainstorm (all candidates, with verdicts)

1. **White-box monitors on the RL-obfuscated parallel-latents model; do probes trained while CoT was legible
   survive; can RL evade them too.** Explicitly suggested by the Redwood authors and unverified by them; resolves
   the Greenblatt-vs-nesiacel comment disagreement; implements AISI's representational-drift recommendation.
   Cheap (1.7B model, toy tasks). Interesting either way. -> **Proposal 01.**
2. **Matched A/B on the IFM natively-pretrained latent-feedback checkpoints vs identically-trained transformers,
   plus a "retrofit" arm (Redwood's zero-init W on the plain transformer), across 60M-778M.** Fills the gap named
   by the Dory post (no identical-training control) and the Redwood post (no access to natively trained models);
   is the measurement Greenblatt's proposal asks for. Cheap. -> **Proposal 02.**
3. **DiffusionGemma forced single-canvas serial depth + intermediate-token monitor + small LoRA elicitation.**
   Directly GDM's open problems 7.2.4 / 7.3.3 / 7.3.5 / 7.3.6 / 7.4. Mostly inference. -> **Proposal 03.**
4. Replicate the Redwood RL result on another architecture (COCONUT, Ouro, Dory). Rejected: done on Dory two days
   ago; a third replication alone is low interest.
5. Main-task/side-task version in BashArena / SHADE-Arena / LinuxArena with a latent model (authors' suggestion).
   Rejected for stage 1: the available latent models are 60M-4B and cannot do these tasks; pipeline is long and
   fragile. Possible stage 2 of proposal 01/02 in an artificial "code + hidden math" form.
6. Vary latent bandwidth (rank of W) and feedback layer pair, measure evasion speed. Folded into proposal 01 as an
   optional ablation; alone it is a parameter sweep with no clear headline, and tuning the latent channel edges
   toward the gain-of-function the authors warn against.
7. Feedback-spillover / weak-pressure variants on latent models. Rejected: Redwood already ran spillover, stochastic
   penalties and filtering; cluster `cot-training-pressure` covers weak-pressure dose-response.
8. Activation Oracles / NLAs to translate latents into text (GDM's hope). Rejected for stage 1: needs training an
   oracle for a custom architecture; kept as stage 2 of proposal 01.
9. Opaque-serial-depth calculator applied to public latent architectures (Dory, Ouro, FBT, IFM). Rejected: paper
   exercise, GDM/Redwood have largely done it; low karma.
10. No-CoT ECI vs ECI for latent models (Greenblatt's proxy). Rejected: done for Dory (NCRI vs mini-ECI); IFM models
    are base LMs too small for ECI benchmarks. Proposal 02 measures the trained-elicitation analogue instead.
11. AISI: representational drift of probes across ordinary RL fine-tuning on a standard model. Rejected as a
    stand-alone: generic, and arXiv 2602.15515 already measures drift; the drift question is more pointed inside
    proposal 01 (probes fit before the CoT goes dark, tested after).
12. AISI: correlated failures between CoT monitors and probes. Partly answered by proposal 01 (does text-monitor
    pressure alone degrade the probe?). Not a separate project.
13. Latent inter-agent communication (KV-cache / latent sharing between agents) toy model. Rejected: needs a new
    environment from scratch, no prior infrastructure in the cluster.
14. DG controllability evals (open problem 7.3.1). Rejected: belongs to cluster `cot-controllability`; lower novelty.
15. Full adversarial fine-tune of DG to hide reasoning in vectors under a logged-intermediates monitor. Too big for
    stage 1 (26B MoE, multi-step backprop through self-conditioning); it is stage 2 of proposal 03.

## 6. Notes for a later reviser

- Proposal 01 and 02 both need a Redwood-style SFT+GRPO pipeline. They are distinct projects (different question,
  different models), but if both are funded the pipeline should be written once. Proposal 02's models are small
  enough to serve as the debugging target for 01.
- Redwood did not state N, M (feedback layers), SFT batch size, or whether feedback is active on prompt positions.
  Any reimplementation is "in the style of", not an exact replication; say so.
- In the perm task, "which problem is it" is trivially decodable from activations because the prompt is in
  context. White-box monitorability must therefore be defined on intermediate reasoning states (holder after pass
  k at CoT position k), with the plain control model under all-filler prefill as the baseline for what a probe can
  read without latent reasoning (the control does <= 4 hops in one pass).
- IFM feedback models were pretrained with detached feedback and 2 passes; token-by-token decoding is the fixed
  point. Whether serial latent computation emerges under that recipe is itself an open question (proposal 02).
- Gain-of-function caution from the Redwood authors: proposals evaluate public checkpoints and a toy retrofit;
  they do not try to make latent reasoning more capable, and write-ups should not include recipe tuning details
  beyond what Redwood published.
