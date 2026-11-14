# Cluster: Training against probes / internals-in-the-loop

key: `probes-in-training` — 5 post(s); write at most 3 proposal(s).

## Neural chameleons can('t) hide from activation oracles
- id: `wfGYMbr4AMcH2Rv68` | 2026-01-22 | 56 karma | ceselder
- url: https://www.lesswrong.com/posts/wfGYMbr4AMcH2Rv68/neural-chameleons-can-t-hide-from-activation-oracles-1
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): MATS exploration mini-project: trains 'neural chameleon' LoRA fine-tunes of Gemma 2 9B and Gemma 3 27B to evade linear probes for 10 concepts when a trigger phrase is present, then tests whether evasion transfers to held-out concepts and to activation oracles used as yes/no classifiers. On Gemma 2 9B, activation-oracle performance drops too but inconsistently and less than probes; on Gemma 3 27B, evasion generalises less well to unseen concepts, and there the oracle suffers more than the probes. Author flags it as vibe-coded, with less data than and deviations from the original paper.
- screener's follow-up note (often the screener's inference): Follow the original methodology more closely (more training concepts, safety probes, mean-pooled probes), test Gemma 2 27B to separate model-size from model-family effects, and train chameleons directly against oracles.
- builds on: Neural Chameleons paper; Activation Oracles paper; Dreaming vectors: gradient-descented steering vectors from activation oracles (https://www.lesswrong.com/posts/rdhyHtjf3LcZxuQPm/dreaming-vectors-gradient-descented-steering-vectors-from)

## It Is Reasonable To Research How To Use Model Internals In Training
- id: `G9HdpyREaCbFJjKu5` | 2026-02-08 | 130 karma | Neel Nanda
- url: https://www.lesswrong.com/posts/G9HdpyREaCbFJjKu5/it-is-reasonable-to-research-how-to-use-model-internals-in
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Neel Nanda argues that research on using model internals in training (probe scores in the loss or in an RL reward, steering or ablating directions during training, with or without periodically retraining the probe) is legitimate and potentially valuable for safety, contra the 'most forbidden technique' framing. He says whether such training shapes generalisation usefully or just breaks interpretability-based auditing depends on empirical facts we do not yet know. Opinion piece with no experiments.
- screener's follow-up note (often the screener's inference): Measure the open empirical question on small open models: when training against a probe (with gradients vs as an RL reward, with vs without probe retraining), does the concept get removed or merely obfuscated, and do held-out probes or other detectors still work afterwards?
- builds on: Persona vectors / preventative steering (https://arxiv.org/abs/2507.21509); Concept ablation fine-tuning (https://arxiv.org/abs/2507.16795); Zvi, 'The Most Forbidden Technique'

## The Most Forbidden Technique is not always forbidden
- id: `tEFD2bgNWZ6XcurKA` | 2026-07-18 | 84 karma | Rauno Arike
- url: https://www.lesswrong.com/posts/tEFD2bgNWZ6XcurKA/the-most-forbidden-technique-is-not-always-forbidden-1
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Literature review prompted by Goodfire's RLFR reproduction (probes as RL reward). Argues the real red line is keeping held-out, uncorrelated measures of alignment rather than never training on internals, reviews when past work (notably The Obfuscation Atlas, Taufeeque et al.) found training against probes acceptable, argues probe-based signals are preferable to CoT-monitor-based ones, and lists four conditions for using internals in training. No new experiments.
- screener's follow-up note (often the screener's inference): Measure how correlated different proxies are under optimisation (does training against a probe degrade CoT monitors or held-out probes, and vice versa) on open models - the author notes Aether is working on this.
- builds on: Don't Implement The Most Forbidden Technique (Zvi); The Obfuscation Atlas (Taufeeque et al.); RLFR (Goodfire)

## Held-out Monitors Sometimes Degrade, Even When Not Trained Against
- id: `APkFfRp2AicL9RqvT` | 2026-07-29 | 64 karma | Joey Yudelson
- url: https://www.lesswrong.com/posts/APkFfRp2AicL9RqvT/held-out-monitors-sometimes-degrade-even-when-not-trained
- screener's kind: runs (high); follow-up cost guess: cheap
- screener's summary (unverified): Aether work that RL-trains Qwen3-8B on MBPP-Honeypot (an easily hardcodeable coding env from The Obfuscation Atlas) while training against either an LLM monitor or a deception probe, then measures how held-out proxies change. Training against one proxy sometimes yields reward-hacking policies that look less suspicious to, and are less well discriminated by, proxies that were never trained against; degradation across proxies is correlated, though the effect is not consistent across runs.
- screener's follow-up note (often the screener's inference): Build a 'science of held-out monitors': characterise when cross-proxy degradation occurs (other models, environments, probe types, monitor strengths) and which proxy pairs are actually uncorrelated; code and run metrics are released.
- builds on: The Obfuscation Atlas (arXiv:2602.15515); Should we train against CoT monitors? (LW); Validating against a misalignment detector is very different (AF)

## Training on probes: What's going on
- id: `gHFCgrvfxQtaEnJye` | 2026-09-08 | 73 karma | Charlie Steiner
- url: https://www.lesswrong.com/posts/gHFCgrvfxQtaEnJye/training-on-probes-what-s-going-on
- screener's kind: motivates (borderline); follow-up cost guess: cheap
- screener's summary (unverified): Mostly theoretical/review post. Claims: gradient descent against a probe while training still incentivizes dishonesty leads to representation change that evades the probe; training against the probe after other training works fine; and (a policy-gradient theorem, also in Obfuscation Atlas Appendix D) adding a probe term to RL with one-token answers, or with credit assigned only to the triggering token, does nothing. So RL-on-probe papers that see effects work via credit-assignment 'collateral damage'. No new experiments in this post; a follow-up post lists research ideas.
- screener's follow-up note (often the screener's inference): Directly test the theorem in a small RL setup: vary credit assignment of the probe penalty (triggering token only vs whole trajectory) and measure honesty, probe evasion and representation drift.
- builds on: The Obfuscation Atlas (https://arxiv.org/abs/2602.15515); Features as Rewards (https://arxiv.org/abs/2602.10067); RL-Obfuscation (https://arxiv.org/abs/2506.14261); In (highly contingent!) defense of interpretability-in-the-loop ML training; The Most Forbidden Technique is not always forbidden

