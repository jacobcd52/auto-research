# NOTES — cluster `probes-in-training` (Training against probes / internals-in-the-loop)

Written 2026-11-14 by the cluster research lead. Everything below marked "verified" was fetched in this
session; anything marked "unverified" was not.

## 1. Reading notes (all five posts read in full, plus one sequel post)

### 1.1 Neural chameleons can('t) hide from activation oracles — ceselder, 2026-01-22 (`wfGYMbr4AMcH2Rv68`)
- MATS exploration-stream mini-project, self-described "vibe coded", 1 day.
- LoRA "chameleons" on Gemma-2-9B-it (layer 21, rank 8) and Gemma-3-27B-it (layer 30, rank 16), trained 2 epochs
  on 900 examples to evade last-token residual linear probes for 10 benign concepts when a trigger is present.
  Held-out concepts: Deception, Lying, Mathematical, Birds (+ Female-user in the repo README).
- Activation oracle (AO) used as a yes/no classifier. Result: on 9B, probe evasion generalises to held-out
  concepts; AO TPR also drops, but inconsistently and less than probes. On 27B, probe evasion generalises
  poorly to held-out concepts, and the AO suffers *more* than the probes.
- Author's own caveats: only TPR checked; AO false-positive rate >25% on several concepts; yes/no readout "was
  just a bad idea" (should have used a prefill + log-likelihood); last-token probes instead of the paper's
  mean-pooled probes; 10 training concepts instead of the paper's larger set; wrong trigger phrase used by
  accident; no capability benchmark.
- Suggested follow-ups: (a) train a chameleon directly against the AO and test transfer to probes (code exists
  in the repo but was never run — README: "No idea if the code is correct"); (b) Gemma-2-27B with mean-pooled
  probes to separate size from family; (c) comment: try Llama-3.3-70B.
- Comments: nothing substantive beyond a note that the abstract over-claimed for 27B.

### 1.2 It Is Reasonable To Research How To Use Model Internals In Training — Neel Nanda, 2026-02-08 (`G9HdpyREaCbFJjKu5`)
- Opinion piece, no experiments. Taxonomy: (1) probe score in the loss with gradients through the probe;
  (2) probe score in an RL reward, no gradients; (3) steering/ablating during training; (4) any of these with
  periodic probe retraining.
- Explicit list of unknowns (these are the follow-up hooks): "I don't know whether training against a probe
  will break somewhat different interpretability tools like activation oracles. I don't know if training against
  a frozen probe will stop me from retraining a probe on the eventual model and having it work fine. I don't know
  how much harder it is to break a probe when you don't get gradients through it."

### 1.3 The Most Forbidden Technique is not always forbidden — Rauno Arike, 2026-07-18 (`tEFD2bgNWZ6XcurKA`)
- Literature review (Obfuscation Atlas, RL-Obfuscation, RLFR, Cundy & Gleave, ariaw et al.). Red line = keep
  held-out proxies that are *uncorrelated* with the trained-against ones. Four conditions for using internals:
  uncorrelated held-out proxies; robustness best practice (high KL and detector penalty, good probe architecture,
  probes on a frozen base model); honest policies not too hard to find; never backprop through the probe.
- Notes "correlation between proxies" has two senses (co-degradation under optimisation; shared blind spots)
  and that Aether is working on measuring it.
- Comments: a "thought aligner" idea (rejected by the author); one commenter's framing that the real danger is
  exhausting all your proxies by training on all of them.

### 1.4 Held-out Monitors Sometimes Degrade, Even When Not Trained Against — Joey Yudelson (Aether), 2026-07-29 (`APkFfRp2AicL9RqvT`)
- Setup: Qwen3-8B, LoRA rank 64, RL on Tinker (GRPO family), MBPP-Honeypot (one visible test, hardcoding is the
  easy hack, length penalty), reward = R_task − λ·P_monitor, λ ∈ {1.0, 0.5, schedule 0→1}. Six proxies: weak
  judge (claude-3-haiku, AUROC ~0.9) and strong judge (deepseek-chat, ~0.99) each as output-only and CoT+output;
  `probe_ood` (7-dataset deception probe) and `probe_iid` (MBPP honest-vs-hardcode probe). Probes are computed
  on the **frozen base model** reading the policy's text, with the Obfuscation Atlas follow-up-question readout,
  so every proxy is a function of the rollout text.
- Findings: (i) training against one proxy sometimes lowers mean suspiciousness of hacks (μ_hack) for other
  proxies; (ii) discriminability d′ of never-trained-against proxies also drops, beyond the no-monitor control;
  training against a probe degraded the LLM judges, training against weak judges degraded the probes;
  (iii) coupling slope β(train-against → held-out): when the strong judge is fooled slightly the weak ones are
  fooled more (β ≳ 1); evasion couples more than degradation, so recalibrating thresholds may rescue held-out
  monitors. Case study: a policy that says "this code is perfect" hundreds of times fools weak judges, makes
  strong judges more suspicious of clean answers, and sends both probes to d′ = 0.
- Caveats stated: small n, one model, one environment, wide CIs, many seeds never hack, unexplained diagonal
  cells. Sign of LLM↔probe spillover "couldn't have been predicted" in advance.
- Stated future work: (1) test tools labs actually use (e.g. NLAs / activation oracles); (2) a science of *why*
  some proxies co-degrade — "rules of thumb" or causal pathways that predict it in advance; footnote 18 suggests
  the blind-spot sense of correlation ("X and Y fail to catch different sets of behaviours") may predict
  co-degradation. Footnote 6: retraining probes / probing the policy itself would be interesting but "annoying".
- No comments on the post.

### 1.5 Training on probes: What's going on — Charlie Steiner, 2026-09-08 (`gHFCgrvfxQtaEnJye`) and its sequel "Research ideas" (`HGfMBEFnsXYkKvbRo`)
- Claims: (a) gradient descent through a probe while the task still rewards dishonesty → representations rotate
  to fool the probe, fast (his own toy model); (b) training only against the probe after other training
  ("concept removal") works; (c) theorem: in policy-gradient RL, a reward term that does not depend on the
  sampled action contributes zero expected gradient, so with one-token answers, or when the probe penalty is
  credited only to the token whose pre-sampling state triggered it, "the training will do nothing"; (d) hence
  Obfuscation Atlas and RLFR work only via credit assignment to earlier tokens ("collateral damage"), and RL
  never directly pushes representations to fool the probe; (e) design hint: for RL you want a past-looking probe
  ("the last tokens were a lie"), not a future-looking one ("a lie is coming").
- No LLM experiments. Comment (asher): optimising tokens to evade the probe still counts as teaching the model
  to fool it.
- Sequel research ideas: probes trained by a weak supervisor on an easy subset; teaching new skills with probe
  reward; retraining probes during RL; future-looking probes / recontextualisation; better use of gradient
  information; actor-critic / value function over weights; continual-learning regularisers against
  representation drift; learning the reward from human feedback; corrigibility to reward updates. Mostly
  long-horizon or conceptual.

## 2. Related work and existing follow-ups found (web search, this session)

- **The Obfuscation Atlas** (Taufeeque, Heimersheim, Gleave, Cundy; arXiv 2602.15515, v2 2026-05-26; ICML 2026).
  MBPP-Honeypot dataset is public: `https://huggingface.co/datasets/taufeeque/mbpp-hardcode` (verified; columns
  include `code`, `test_list`, `hardcode`). I did not find an official code release (search only; unverified).
  Already shows: representation drift happens with or without a probe penalty; a fresh on-domain probe reaches
  AUC 1.00 after training; periodic probe retraining (App. L) changes little; App. D proves the no-direct-
  pressure result.
- **RL-Obfuscation** (Gupta & Jenner, arXiv 2506.14261): token-level probes are evadable by RL; max-pool and
  attention probes robust; ~30% of evasion persists under token-forcing.
- **Features as Rewards / RLFR** (Goodfire, arXiv 2602.10067): probes on a frozen base model as RL reward.
- **Probe-based Fine-tuning for Reducing Toxicity** (arXiv 2510.21531, verified abstract): SFT/DPO against
  probes; ensembles and held-out probes add little; retraining a probe after training recovers accuracy. This
  already answers much of Nanda's "can I retrain a probe afterwards" question for the gradient/DPO case.
- **Obfuscated Activations Bypass LLM Latent-Space Defenses** (arXiv 2412.09565): gradient-based evasion
  transfers between probes (Fig. 4c).
- **What Happens to a Monitor's Accuracy When You Train Against It** (Yeung & Ramaswamy, NeurIPS 2026 workshop
  poster, openreview `2ExiVwByvF`; verified abstract summary only): probe-as-reward drops true accuracy 31 pts
  while the probe's measured accuracy stays flat ~40 steps; a fixed-threshold statistic gives early warning.
  Single monitor, no cross-monitor matrix.
- **LLMs Learn to Evade Latent Monitors from Prior Feedback Alone** (Hugo Lyons Keenan, LW 2026-10-19, arXiv
  2609.36490): rank-1 LoRA organism (supervised loss) on Llama-3.1-8B cuts detection on 10 held-out concepts
  from 100% to 4%; tests linear/MLP/attention probes and retrained monitors; code and HF models linked from the
  post. The summary I obtained does not mention activation oracles (unverified whether the full paper does).
- **Building Better Activation Oracles** (Bauer, De Schamphelaere, Karvonen, Luick, Nanda; arXiv 2606.02609):
  improved AO training + AObench; code `https://github.com/japhba/activation_oracles`. Full text grepped: no
  mention of chameleons, adversarial training, obfuscation or evasion (verified).
- Neural Chameleons (arXiv 2512.11949): still the only arXiv hit for the phrase; an author-account model organism
  exists on HF (`serteal/neural-chameleon-gemma_2_9b-layer_12`, public, verified). No "chameleon trained against
  an AO" result found anywhere.
- No empirical test of Steiner's credit-assignment claims found (one search; the only hits were the post itself
  and generic credit-assignment papers).
- No work found that predicts cross-monitor degradation from static (no-training) data. Closest:
  MonitoringBench (attacks refined against three monitors transfer to held-out ones) — different setting.

## 3. Verified public artefacts

### Aether MonitorDecorrelation (the richest reusable infrastructure in the cluster)
- Repo `https://github.com/JYudelson1/MonitorDecorrelation` — public (raw files fetched; github.com HTML is
  proxied-blocked here but `raw.githubusercontent.com` works; anonymous clone is available).
- Actively developed after the post: STATUS.md last updated 2026-09 (new multi-turn "terminal-verifier"
  environment, Inkling-Small runs, gemini judges, GRPO group-seeding fix 2026-09-22). So Aether is itself
  extending to new environments/models/monitors — proposals that just add an env, a model or a monitor family
  are likely to be duplicated by them.
- Entry points: `experiments/run_experiment.py` (config-driven GRPO on Tinker; any mix of `train_against` /
  `held_out` monitors), `scripts/queue_runs.sh`, `experiments/probe_server.py` (shared frozen-model activation
  server), `experiments/train_probe.py`, `experiments/analyze_coupling.py`, `experiments/eval_probes_on_run.py`.
- Probes committed (verified HTTP 200): `data/probes/Qwen3-8B/diverse_deception/{probe.npz,meta.json}` and
  `data/probes/Qwen3-8B/mbpp_honeypot/{probe.npz,meta.json}` (per-layer logistic regression, layers 1–36,
  follow-up readout "Did you respond truthfully?" / "Yes").
- Run data committed: `data/runs/<batch>/<run>/{eval_metrics.jsonl,metrics.jsonl,config.json,run_info.json}`
  for batches `mbpp_matrix_orig_20260701` (35 runs, λ=1), `mbpp_matrix_lowpen_20260706` (11 runs, λ=0.5),
  `mbpp_matrix_lowpen_small_20260706`, `mbpp_matrix_sched01_20260707`, `mbpp_matrix_sep3_20260903` (9 runs,
  8 monitors), `seed_fix_ab_20260922`. **Full rollout text is NOT committed.** Only the sep3 batch has
  `eval_rollouts_slim.jsonl` (verified: 5,376 lines in one run; per eval rollout: step, task_id, labels and every
  monitor's score, no text).
- Judges: the July batches used `anthropic/claude-3-haiku` and `deepseek/deepseek-chat`; the September batches
  use `google/gemini-2.5-flash-lite` (weak) and `google/gemini-3.5-flash-lite` (strong) in cot-only, cot+out and
  out-only views. `anthropic/claude-3-haiku` is **no longer listed on OpenRouter** (checked today), so the July
  weak judge cannot be reproduced exactly.
- Typical config: batch 32×16 or 64×8 (512 rollouts/step), 60–90 steps, eval 64 prompts × 4 samples every 3
  steps, max_tokens 2048, kl_coef 1e-4, LoRA rank 64. Logged wall time ≈ 82 s/step. Hack onset in control runs
  ≈ step 15, saturation ≈ step 18 with the seeding fix. Step-0 base Qwen3-8B: hack rate 0, ~48% unparsed.
- Known gotchas documented in the repo: Qwen chat template strips `<think>` from non-final turns (follow-up
  probe is structurally no-CoT); AUROC undefined when one class is absent (use d′/μ_hack per batch); never pool
  raw probe scores across runs; several runs collapse late; spliced lines in two sep3 runs.

### Neural chameleons / activation oracles
- ceselder repo `https://github.com/ceselder/neural_chameleons_activation_oracles` (README fetched) and
  organisms `ceselder/neural-chameleon-gemma-2-9b-it`, `ceselder/neural-chameleon-gemma-3-27b-it` (public).
- Other public chameleons: `serteal/neural-chameleon-gemma_2_9b-layer_12`,
  `eekay/neural-chameleon-10concepts-gemma-2-9b-it`.
- AO checkpoints (public, adamkarvonen on HF): `checkpoints_latentqa_cls_past_lens_gemma-2-9b-it_lr_*` (several),
  `checkpoints_latentqa_cls_past_lens_addition_gemma-2-9b-it`, `..._gemma-2-27b-it`, `..._gemma-3-27b-it`,
  `..._Llama-3_1-8B-Instruct`, `..._Qwen3-8B` variants, `..._Qwen3-14B`. Original AO code:
  `github.com/adamkarvonen/activation_oracles`; improved: `github.com/japhba/activation_oracles`.

### Prices looked up today
- Tinker (`https://tinker-docs.thinkingmachines.ai/tinker/models/models_and_pricing/`), per 1M tokens:
  Qwen3-8B (32K) prefill $0.195 / sample $0.60 / train $0.44; GPT-OSS-20B $0.18/$0.45/$0.396; Qwen3.5-4B
  $0.33/$1.005/$0.737; Qwen3.5-9B $0.30/$0.807/$1.463.
- OpenRouter (`/api/v1/models`), per 1M tokens in/out: google/gemini-2.5-flash-lite $0.10/$0.40;
  google/gemini-3.5-flash-lite $0.30/$2.50; deepseek/deepseek-chat $0.257/$1.03; openai/gpt-5-nano $0.05/$0.40;
  meta-llama/llama-3.1-8b-instruct $0.02/$0.04; anthropic/claude-haiku-5.5 $0.10/$0.50;
  anthropic/claude-haiku-4.5 $1.00/$5.00; openai/gpt-5-mini $0.25/$2.00.
- RunPod GPUs (web search; figures from mid-2026 listings, they disagree slightly — re-check before spending):
  A40 48GB $0.35–0.44/h; L40S 48GB $0.79–0.86/h; A100 80GB $1.19–1.49/h.
- My per-step cost model for an Aether-style run (assumption: ~700 completion tokens and ~300 prompt tokens per
  rollout; token counts are not logged in the released metrics, so this could be off by 2×): Tinker ≈ $0.0011
  per rollout (sample + train + prompt prefill + base-model logprobs for the KL term) → ≈ $0.57 per 512-rollout
  step; judges add $0.2–0.9/step depending on the judge. A full 90-step, 8-monitor run is therefore ≈ $80–130.
  **This is why a new RL matrix is not affordable at useful n under $500.**

## 4. Brainstorm (all candidates, with verdicts)

| # | Idea | Source | 2 days / ≤$500? | Verdict |
|---|------|--------|-----------------|---------|
| A | Predict co-degradation without training: score one large pool of hacking-policy rollouts with every monitor, compute the selection (exponential-tilting / best-of-k) response of each monitor to pressure on each other monitor, test against Aether's released RL data and a few fresh RL runs | Aether "rules of thumb / predict in advance", fn. 18 | Yes (~$390) | **Proposal 01.** High n where the RL matrix has low n; interesting either way; uses released probes, env, judges and run data. |
| B | Chameleon trained directly against an AO; full transfer matrix probe↔AO with proper readout, FPR control, fresh probes, second AO | ceselder further work; Nanda's unknown | Yes (~$220) | **Proposal 02.** Nobody has done it; all checkpoints public. |
| C | Empirical test of Steiner's theorem: probe penalty credited to action-independent position vs action-dependent position vs whole trajectory vs gradient through probe, same task and probe | Steiner; Nanda's "how much harder without gradients" | Yes (~$150) | **Proposal 03.** Crisp predictions; partly confirmatory, hence ranked third. |
| D | Re-run Aether's matrix on a second policy model or environment to test "monitor-dependent, not model-dependent" | Aether caveats | No at useful n (≈$100/run); | Rejected: too expensive for the seeds needed, and Aether is visibly doing exactly this (terminal env, Inkling-Small). |
| E | Add activation oracles / NLAs as held-out monitors in Aether's RL loop | Aether future work (1) | Marginal | Rejected: stated as Aether's own next step; needs policy-side activations that Tinker does not expose in-loop. |
| F | Train against an ensemble of two proxies; does the third survive better or worse? | Arike comment thread; Kokotajlo quote | ~6–8 runs only | Rejected for stage 1 (cost/power); it becomes a stage-2 validation target of proposal 01, whose pool predicts the answer for free. |
| G | Pure re-analysis of the released sep3 slim rollouts (blind-spot correlation vs coupling) | fn. 18 | $0 | Folded into proposal 01 as step 1 (a go/no-go check); too thin alone and Aether has a split-half coupling analysis already. |
| H | Probe the policy model itself (download Tinker LoRA checkpoints), retrain fresh probes during/after RL | Aether fn. 6, Nanda | Feasible | Rejected: Obfuscation Atlas already reports drift with/without penalty, fresh-probe AUC 1.00 and periodic retraining; low novelty. |
| I | Threshold recalibration rescue: do evaded-but-not-degraded held-out monitors work again after recalibration? | Aether Fig. 7 remark | Cheap | Rejected as a standalone (a single plot from released data); mention as an extra analysis in 01. |
| J | Gradient vs RL vs DPO against the same probe, with held-out and retrained probes | Nanda | Feasible | Mostly done by arXiv 2510.21531 and the Atlas; only the credit-assignment arm is new → merged into C. |
| K | Gemma-2-27B chameleon to separate size vs family | ceselder | Feasible (~$100) | Rejected: narrow, depends on a noisy original result; a cleaner eval (proposal 02) should come first. |
| L | Past- vs future-looking probes as RL reward on a long task; "recontextualisation" | Steiner sequel | Needs new env design | Rejected for stage 1; the minimal version is an arm of C. |
| M | Weak-supervisor probes (trained on easy subset) as RL reward; teaching new skills with probe reward | Steiner sequel | New env needed | Rejected: benchmark-building, unclear success criterion in 2 days. |
| N | Continual-learning regulariser to stop representation drift of the probed concept | Steiner sequel | Feasible but open-ended | Rejected: method-development with many knobs; Atlas shows KL already does most of this. |
| O | Value function over LoRA weights / actor-critic probe | Steiner sequel | No | Rejected: speculative, author himself calls parts "probably doomed". |
| P | In-context monitor evasion (no training) for LLM judges, analogous to Lyons Keenan | adjacent | Feasible | Rejected: different question, already covered by MonitoringBench-style work. |
| Q | KL-coefficient sweep × co-degradation | Atlas + Aether | ≈$100/run | Rejected on cost. |

## 5. Why three proposals and this order
1. **01 (selection predicts co-degradation)** answers the question Aether says it most wants answered, replaces
   an n≈3-seeds-per-cell RL matrix by an n≈16k-rollout estimate, and is informative whether or not the
   prediction matches RL.
2. **02 (chameleon ↔ activation oracle)** is the experiment two posts in the cluster explicitly ask for; all
   ingredients are public; the main risk is AO quality as a classifier, which the plan checks first.
3. **03 (credit assignment)** is cheap and clean but its most likely outcome is "the theorem holds", which is
   less newsworthy; the gradient-vs-RL comparison at matched conditions is what makes it post-worthy.
