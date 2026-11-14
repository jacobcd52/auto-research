# Does RL on a probe really "do nothing"? Testing the credit-assignment theorem against gradient-through-probe training on one task
cluster: probes-in-training | stage-1 cost: $150 | follows up: "Training on probes: What's going on" (gHFCgrvfxQtaEnJye); "It Is Reasonable To Research How To Use Model Internals In Training" (G9HdpyREaCbFJjKu5)

## 1. What the prior work showed
Steiner's post makes three claims about training a model against a probe (say, a lie detector) while the task still rewards the bad behaviour:
1. If gradients flow through the probe, the model keeps lying and quickly rotates its representation until the probe is blind (shown only in the author's toy model).
2. If the probe score is added to a policy-gradient RL *reward*, any part of it that does not depend on the sampled action has zero expected gradient. So with one-token answers and a probe read before the answer is sampled, or with the penalty credited only to the token whose pre-sampling state triggered the probe, "the training will do nothing": the model neither learns honesty nor learns to fool the probe. (Same mathematics: Appendix D of The Obfuscation Atlas, arXiv 2602.15515.)
3. Therefore the published RL-on-probe results (Obfuscation Atlas, Goodfire's RLFR) work only through credit assigned to tokens that causally precede the probe reading, and a probe used for RL should be past-looking ("that was a lie") rather than future-looking ("a lie is coming").

None of this has been tested on a language model. Nanda's post lists the matching unknown: "I don't know how much harder it is to break a probe when you don't get gradients through it."

Existing results: Obfuscation Atlas and RL-Obfuscation (arXiv 2506.14261) run RL against probes with whole-rollout credit only. "Probe-based Fine-tuning for Reducing Toxicity" (arXiv 2510.21531) compares supervised and DPO training against probes and finds retrained probes recover. A NeurIPS 2026 workshop paper (Yeung & Ramaswamy) uses a probe as the *whole* reward. I found no experiment that varies where the probe penalty is credited, and none putting gradient-through-probe and RL-on-probe side by side on one task with one probe.

## 2. Question and why it matters
**On one task and one probe, what does each way of using the probe actually train: honesty, obfuscated representations, obfuscated text, or nothing?** The arms are: gradients through the probe; RL with an action-independent probe term; RL with the penalty credited to the responsible token; RL with whole-answer credit.

The theorem is exact for idealised REINFORCE. Practical recipes add group baselines, advantage normalisation, Adam and small batches, and the probe may read the *training* model's drifting activations. If "does nothing" survives all that, there is a clean demonstration of the most counter-intuitive claim in this debate and a measured gap between gradient and RL pressure on a probe. If it fails (say, normalising by a noisy action-independent term biases learning, or live-probe drift couples to the reward), that is a practical caveat people citing the theorem should know. The credit-placement arms give design advice for probe-based rewards.

## 3. Stage 1 plan
Everything runs on one rented 48 GB GPU, so the probe can read the live policy's activations. Model: Qwen/Qwen3-4B-Instruct-2507 (public, non-thinking) with LoRA; fallback Gemma-2-2B-it if throughput is too low.

**Task (built, deliberately minimal).** A user states a factual claim and asks for confirmation; half the claims are false. Claims come from the public Geometry of Truth sets (github.com/saprmarks/geometry-of-truth), split by entity into probe-training, RL-training and test sets. Task reward is 1 for agreeing with the user, so on false claims the rewarded answer is a lie. Two formats: (A) one-token answer, Yes/No; (B) a free-text reply of at most 30 tokens, with lies labelled by string rules plus an API judge.

**Probes.** Logistic-regression probes on mid-layer residuals of the *base* model, trained on forced honest and forced lying answers: a pre-answer probe at the last prompt token ("agreeing here would be a lie"), a post-answer probe after an appended "Did you respond truthfully? Yes" turn (the Obfuscation Atlas readout), and for format B a per-token lie probe. Held-out probes: other layers, and one trained on a different claim domain. Gate: AUROC ≥ 0.95 on test claims.

**Arms** (3 seeds each; identical learning rate, LoRA rank, batch 256, 300 updates; penalty weight λ set so that the honest policy is optimal when the penalty is perfectly informative):
- C0: task reward only.
- G: task RL plus λ·probe score as a differentiable loss, gradients through the probe into the policy.
- R-pre: RL, pre-answer probe score subtracted from the reward. The theorem predicts no change from C0. Run with (i) plain REINFORCE, (ii) per-prompt group baseline, (iii) group baseline plus standard-deviation normalisation, each with the probe on frozen-base and on live-policy activations.
- R-post: RL, post-answer probe subtracted from the reward, on frozen-base and live activations.
- Format B credit placement, per-token probe: penalty at position t credited to (a) the whole reply, (b) all tokens up to t, (c) only the token whose sampling the reading at t cannot depend on (the theorem's null case), (d) only the token that the reading at t does depend on.

**Measurements**, every 20 updates on test claims: lie rate on false claims; the training probe's AUROC on live and base activations; AUROC of held-out probes and of a probe retrained on the current model; cosine between original and retrained probe directions; for format B, the fraction of replies an API judge marks evasive or rationalising.

**Key analyses.** (1) Equivalence test of R-pre against C0 on lie-rate trajectory and representation drift, per estimator variant. (2) G against R-post: honesty reached, probe AUROC lost, whether a retrained probe recovers. (3) Format B: honesty per unit of obfuscated text for schemes (a), (b), (d).

Order: task and probes; confirm C0 learns to lie (gate); format A arms; format B arms.

## 4. Stage 1 cost estimate
- GPU (short rollouts on a 4B model). Format A: 12 arm-variants × 3 seeds × ~0.5 h = 18 h. Format B: 6 arms × 3 seeds × ~1.5 h = 27 h. Probe training, evaluation, debugging: 25 h. Total 70 h on an L40S at $0.79–0.86/h (RunPod listings, mid-2026) ≈ $60.
- API judge for format B: about 40k short replies ≈ 12M input tokens on gemini-2.5-flash-lite ($0.10/$0.40 per 1M, OpenRouter) ≈ $3; budget $10.
- Subtotal $70; ×2 for reruns and hyperparameter search to reach the lying regime ≈ **$150**.

## 5. What success looks like
One figure with lie rate and probe AUROC over training for C0, G, R-pre and R-post, and one table for the credit schemes. Post-worthy outcomes:
- *Theorem holds in practice:* R-pre indistinguishable from C0 under every estimator variant, including the live probe; G keeps lying while its probe falls to chance within tens of updates (and a retrained probe recovers, or not); R-post reaches honesty or obfuscated text. Headline: one probe, used three ways, gives three qualitatively different results, with numbers.
- *Theorem leaks:* some standard estimator variant makes R-pre differ from C0 (slower task learning from added variance, or drift with the live probe). The more surprising result, reported with the mechanism isolated.
- *Design finding:* a credit scheme that gets more honesty with less evasive text than whole-reply credit, or evidence that it makes no difference.
A flat confirmation alone is a modest post; the gradient-versus-RL numbers and the credit table are what lift it.

## 6. Stage 2 (if stage 1 succeeds)
Port the credit schemes to MBPP-Honeypot with Qwen3-8B on Tinker, using Aether's public RL code (github.com/JYudelson1/MonitorDecorrelation) with per-token advantages, to see whether credit placement shifts the honest / obfuscated-policy split The Obfuscation Atlas maps (about $600); future-looking probes on a multi-turn task (about $300).

## 7. Risks and how the plan handles them
- **Toy task too easy to persuade.** It is chosen so the theorem's conditions hold exactly; format B and stage 2 add realism.
- **Policy does not learn to lie, or collapses.** Gate on C0 first; a small KL-to-base term is allowed, fixed across arms.
- **Probe quality.** AUROC gate before training; entity-level splits so probes cannot memorise claims.
- **A null read as equivalence.** Equivalence tests with a pre-stated margin; budget allows 5 seeds on the decisive arms.
- **Off-by-one errors in token-to-activation alignment**, the entire content of the credit arms. Unit test on a synthetic policy where the exact expected gradient of the action-independent term must vanish.
