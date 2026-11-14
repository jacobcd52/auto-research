# Cluster: Latent-reasoning / non-autoregressive architectures and monitorability

key: `cot-latent-architectures` — 5 post(s); write at most 3 proposal(s).

## Loss of Oversight: How AI Systems May Become Harder to Audit, Monitor, and Investigate
- id: `JvZxp554WxcZ8BQvM` | 2026-05-21 | 83 karma | Jordan Taylor, Max H, Ed Fage, Thomas Read, Joseph Bloom
- url: https://www.lesswrong.com/posts/JvZxp554WxcZ8BQvM/loss-of-oversight-how-ai-systems-may-become-harder-to-audit-1
- screener's kind: proposes (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Summary of a UK AISI report, based on expert interviews, on pathways by which auditing, monitoring and incident investigation could degrade (e.g. loss of CoT monitorability, training-gaming). Mostly analysis, but lists research recommendations: monitorability benchmarking, understanding which kinds of training degrade monitorability, measuring representational drift across RL training, building model organisms of the degradation pathways, and studying correlated failures of monitoring approaches.
- screener's follow-up note (often the screener's inference): Pick one recommendation, e.g. a model organism of a degradation pathway or measuring probe transfer and representational drift before vs. after RL fine-tuning on an open model.
- builds on: UK AISI report 'Will it become harder to oversee AI systems?'

## How transparent is DiffusionGemma (and why it matters)
- id: `zoYXpdaMgFT43Wc24` | 2026-06-20 | 87 karma | Josh Engels, Callum McDougall, bilalchughtai, János Kramár, Senthooran Rajamanoharan, Arthur Conmy, Rohin Shah, Neel Nanda
- url: https://www.lesswrong.com/posts/zoYXpdaMgFT43Wc24/how-transparent-is-diffusiongemma-and-why-it-matters
- screener's kind: runs (high); follow-up cost guess: unclear
- screener's summary (unverified): GDM transparency audit of the text diffusion model DiffusionGemma (arXiv 2606.20560): it performs similarly to Gemma on monitorability evals, and although its naive opaque serial depth is much larger, intermediate vectors are logit-lens interpretable and non-interpretable information can be ablated without hurting performance, reducing effective opaque depth to roughly Gemma's. Distinguishes variable transparency (shown) from algorithmic transparency (not established).
- screener's follow-up note (often the screener's inference): Probe algorithmic transparency: can intermediate denoising states be used to reconstruct the solution process, and can a diffusion model hide reasoning across steps under adversarial fine-tuning?
- builds on: arXiv 2606.20560 (the paper); Opaque serial depth (prior work cited in post)

## Proposal for tracking the effects of architecture on monitorability
- id: `hLPGv8QjPcNLtDp3A` | 2026-09-10 | 148 karma | ryan_greenblatt, Alek Westover, Lukas Finnveden
- url: https://www.lesswrong.com/posts/hLPGv8QjPcNLtDp3A/proposal-for-tracking-the-effects-of-architecture-on
- screener's kind: proposes (borderline); follow-up cost guess: unclear
- screener's summary (unverified): Mainly a policy proposal: AI companies should report externally verified opaque serial depth for near-frontier models, share evidence on monitorability across architectures and training methods, and publish policies on latent-reasoning architectures. It proposes concrete measurements: no-CoT capability (no-CoT ECI vs overall ECI) as a proxy, and monitorability stress tests (eliciting or fine-tuning models to reason or communicate without it showing in CoT), sketched in an appendix.
- screener's follow-up note (often the screener's inference): Run the sketched stress tests on open models/toy architectures: can fine-tuning elicit reasoning that is not reflected in CoT, and how does that scale with opaque serial depth?
- builds on: An operationalization of opaque serial depth; Brown-Cohen et al. 2026 (GDM, opaque serial depth); Astra can do a concerning amount with no chain of thought

## Deep recurrent models are less robustly CoT-monitorable than normal CoT models in a toy setting
- id: `5guQJSqstkjgys3PE` | 2026-09-18 | 107 karma | Nick Kuhn, Evie, Alek Westover
- url: https://www.lesswrong.com/posts/5guQJSqstkjgys3PE/deep-recurrent-models-are-less-robustly-cot-monitorable-than
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Uses RL to train a parallel-latents (deep recurrent) model and a normal CoT model to solve a maths problem while hiding from an LLM CoT monitor which of two problems is being solved. The recurrent model moves its reasoning into hidden states and evades the monitor within ~40 RL steps; the normal CoT model is much worse at learning to confuse the monitor. Similar settings show the same direction with smaller gaps.
- screener's follow-up note (often the screener's inference): Vary task complexity, latent bandwidth and monitor strength; test other latent-reasoning architectures (COCONUT, looped transformers) and whether latent probes recover monitorability.
- builds on: Proposal for tracking the effects of architecture on monitorability; An operationalization of opaque serial depth; Full-bandwidth transformers (https://arxiv.org/abs/2608.08888)

## Latent reasoning architectures would likely undermine CoT, our strongest oversight tool
- id: `6m29SfjbittooYojj` | 2026-09-23 | 102 karma | Lukas Finnveden, Alexa Pan, Alek Westover, Girish Gupta, frisby, ryan_greenblatt
- url: https://www.lesswrong.com/posts/6m29SfjbittooYojj/latent-reasoning-architectures-would-likely-undermine-cot
- screener's kind: motivates (borderline); follow-up cost guess: unclear
- screener's summary (unverified): Conceptual argument that architectures enabling extensive latent reasoning (e.g. COCONUT, full-bandwidth transformers with a latent channel) would greatly reduce the usefulness of chain-of-thought for oversight and enable uninterpretable inter-agent communication. No experiment is run.
- screener's follow-up note (often the screener's inference): Train small COCONUT-style or latent-channel models and measure how much monitor-relevant information leaves the text CoT (monitor catch rates, decodability of latents) compared with a text-CoT baseline.
- builds on: COCONUT (arXiv 2412.06769); Full-bandwidth transformers (arXiv 2608.08888); arXiv 2507.05246

