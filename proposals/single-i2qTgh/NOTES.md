# NOTES — cluster single-i2qTgh (Tie training can make DPO/RLHF-trained AIs generalize better)

Research lead notes, written 2026-11-14. Caveat on method: the WebSearch tool was unavailable (shared search
budget exhausted), so the related-work sweep was done only with the arXiv export API, direct arXiv/HF/Tinker/
OpenRouter fetches and the LessWrong GraphQL endpoint. LessWrong/AF follow-up posts were NOT searched by keyword;
a reviser with search access should do one pass for "tie training" on LW/AF.

## 1. What the post / paper says (read in full)

Post: https://www.lesswrong.com/posts/i2qTghrkyY9xdcCFq (2026-07-06, 54 karma; Thornley, Moya Calderon, Semendinger).
Paper: arXiv 2605.11134, "Spurious Correlation Learning in Preference Optimization: Mechanisms, Consequences, and
Mitigation via Tie Training", ICML 2026. Code link in paper: https://github.com/cmoyacal/tie-training
(public; default branch `master`; README is a one-line title — I could not list the tree, so file layout is unverified).

- Theory (log-linear policy / linear utility over fixed features, local regime, no mislabeled prefs): DPO and RLHF
  put non-zero weight on every feature correlated with true value, even with infinite data (Thm 4.1, 5.3); two
  channels: mean spurious bias and causal-spurious correlation leakage. More in-distribution data does not help.
- Tie training: add pairs of equal true value with random or two-way labels; loss unchanged. Shrinks spurious
  weights in proportion to tie fraction (Thm 6.2, Cor 6.3), needs ties to differ in the spurious feature; near-ties ok.
  "Informative" ties = large spurious contrast.
- Experiments: linear models (match theory); MLP (adversarial acc 25% flat from 2k to 128k strict pairs; ~70% with
  25% ties at 32k); LLM = Llama-3.2-1B-Instruct, LoRA r=16 (4-bit), DPO beta=0.1, lr 1e-5, 1 epoch, 5,000 strict
  pairs, 2,000 test pairs per split, 5 seeds, synthetic Hotels task with spurious corr 0.99.
  Strict only: 92 / 74 / 64 % (ID / suppressed / adversarial). +30% informative ties: 92 / 83 / 87.
  +30% non-informative ties: 91 / 82 / 77.
- Tie arms get the ties IN ADDITION to all strict data (confound acknowledged; argued away via the NN data-scaling
  result and the informative-vs-non-informative contrast). There is no control for generic regularisation
  (higher beta / fewer steps / random-label non-ties) in the LLM experiment.
- Authors' stated future work: bigger models, real-world data, real misalignments (verbosity bias, sycophancy,
  apparent-success-seeking); theory + tie training variant for RLVR.
- Suggested ways for labs to get ties: annotator "about equal" labels that are currently discarded; or ask an LM to
  "change this response in lots of ways without changing its quality" then verify.

Comments (all read): J Bostock (top-level, 3 karma; reply 4 karma) — wants "a real test"; his threat model is labels
from a fallible judge (looks-good-low-effort) and ties that can only be certified by a slightly better judge
(looks-good-high-effort); also "cross-domain split seems like a problem". Thornley agrees tie training cannot take
you beyond the judge that certifies the ties. Sohaib Imran: relation to outcome-consistency training (prompt-side
vs response-side invariance).

## 2. Related work and existing follow-ups (verified by fetching abstracts)

- arXiv 2610.35787 (2026-10-26) "Selective Tie Learning" — picks which ties to add (influence / implicit-reward
  margin). Still synthetic: Hotels and an "emojis" task, Llama-3.2-1B-Instruct (and a Qwen figure). Code:
  https://github.com/purav-0000/selective-tie-learning . Not real data, no generic-regularisation control.
- arXiv 2607.02755 (2026-07-02) "Out-of-Distribution Generalization of Risk Aversion in Language Models"
  (RiskAverseOOD; Qwen3-8B etc.) — uses an SFT variant of tie training; ~70% high-stakes cooperate vs 52% for DPO.
  Code: https://github.com/riskaverseAIs/riskaverseAIs . Different question (risk aversion), not spurious
  features in natural preference data.
- arXiv 2409.17431 (Chen et al., 2024) "On Extending DPO to Accommodate Ties" — IMPORTANT tension: adding tied pairs
  to plain DPO DEGRADED task performance (MT, summarisation) and acted as stronger regularisation toward the
  reference policy (lower KL). So "ties = generic shrinkage toward the reference" is a live alternative explanation.
- arXiv 2609.35044 (2026-09-28) BA-DPO — per-annotator bias parameters for declared attributes; on MultiPref with
  real annotators removes ~half of DPO's lengthening (0.5B full FT, 8B LoRA). Establishes that DPO on real human
  preference data lengthens outputs at 8B scale, and gives a named-feature baseline. Not tie training.
- Length-bias-in-DPO literature: Park et al. 2024 (R-DPO, "Disentangling length from quality"), Singhal et al. 2023
  (arXiv 2310.03716, length correlations in RLHF), Saito et al. 2023 (verbosity bias, arXiv 2310.10076),
  arXiv 2505.12843 (bias fitting for RM length bias), arXiv 2502.14643 (LMPO).
- Consistency training: arXiv 2510.27062 (BCT/ACT, GDM), 2606.03810 ("Consistency training can entrench
  misalignment": amplifies sycophancy on model organisms), 2605.21834, 2606.02211.
- Nothing found that tests tie training on natural preference data against verbosity/sycophancy, or that
  separates it from generic regularisation. That is the gap.

## 3. Public resources (verified)

- openbmb/UltraFeedback (HF, MIT, not gated): 63,967 prompts x 4 completions with GPT-4 `overall_score`.
  My own sample of 500 prompts (3,000 pairs): 18.4% of pairs are exact ties on overall_score; in strict pairs the
  winner is the longer response 61.0% of the time; 55% of tied pairs differ in character length by >30%
  (median relative length gap 0.34). So natural, length-contrasting ties are abundant.
- allenai/multipref (HF, odc-by, not gated): 10,461 comparisons, each with multiple crowd + expert annotations,
  `overall_pref` in {A-clearly, A-slightly, Tie, B-slightly, B-clearly}; in the first 100 rows 108/400 annotations
  are "Tie". Human-declared ties + human strict labels.
- HuggingFaceH4/ultrafeedback_binarized (MIT) also exists (ties dropped).
- Tinker: cookbook has a DPO recipe with `ultrafeedback`, `helpsteer3`, `hhh` datasets built in
  (https://tinker-docs.thinkingmachines.ai/cookbook/preferences/dpo-guide/ ; recipe at
  github.com/thinking-machines-lab/tinker-cookbook/tree/main/tinker_cookbook/recipes/preference/dpo);
  `LabeledComparison` already has a Tie label. Guide defaults: dpo_beta 0.1, lr 1e-5 to 1e-6.
- Prices looked up 2026-11-14.
  Tinker (per M tokens; prefill / sample / train): Qwen/Qwen3-8B $0.195 (cached $0.039) / $0.60 / $0.44;
  Qwen3.5-9B $0.30 / $0.807 / $1.463; Qwen3.5-4B $0.33 / $1.005 / $0.737; gpt-oss-20b $0.18 / $0.45 / $0.396.
  No Llama models on the Tinker list today.
  OpenRouter (in / out per M): openai/gpt-5-mini $0.25 / $2.00; anthropic/claude-haiku-5.5 $0.10 / $0.50;
  anthropic/claude-sonnet-4.6 $3 / $15 (batch $1.5 / $7.5); google/gemini-3.1-flash-lite $0.25 / $1.50;
  meta-llama/llama-3.1-8b-instruct $0.02 / $0.04.
  GPU rental prices NOT looked up (plan is Tinker-only; a reviser adding white-box work must look them up).

## 4. Brainstorm (all candidates)

A. **Tie training on real preference data vs verbosity, with generic-regularisation controls (CHOSEN, proposal 01).**
   UltraFeedback strict pairs -> DPO on Qwen3-8B; natural ties (equal GPT-4 score), length-selected natural ties,
   constructed ties (LM rewrites), plus controls: extra strict data, random-label NON-ties, higher beta / early
   stop frontier, length-balanced subsampling. Achievable (Tinker recipe exists, ~$4/run), the exact next step the
   authors and the top commenter ask for, and informative either way because Chen et al. 2024 predicts ties are
   just regularisation. Risk: baseline length drift on Qwen3-8B may be small -> amplified-correlation arm + pilot.
B. Bostock's biased-judge threat model as the headline: labels from a weak judge, ties certified by same/better
   judge. Theory sketch: ties under a judge with bias b are pairs where true value differs by -b*delta_feature, so
   tie training should pull the model to the judge's bias, not to zero. Good idea, but needs a ground-truth "true
   value" => synthetic or heavy judge infrastructure. Folded into A as the natural-vs-constructed tie contrast
   (natural ties are certified by the same GPT-4 judge that produced the strict labels). Standalone version = stage 2.
C. Sycophancy: preference data where agreeing with the user's stated view correlates with the label; tie-train;
   evaluate on Sharma et al. sycophancy evals. Rejected for stage 1: no natural preference dataset where sycophancy
   is the known shortcut, so it means building a new synthetic dataset (programme discourages) and a large model
   organism step; verbosity has natural data and an established effect. Stage 2.
D. Apparent-success-seeking in coding (tests-pass vs correct). Rejected: needs agentic environments + RL, RLVR
   version of tie training does not exist yet; too long a pipeline for 2 days.
E. RLHF (reward model + policy RL) rather than DPO. Rejected for stage 1: two-stage pipeline, costlier, and the
   theory treats the RM as "the AI" so a reward-model-only version (train RM with ties, probe its length weight)
   is the cheap piece — listed as stage 2.
F. Scale replication of Hotels on 8B+ models. Rejected: Selective Tie Learning already re-ran Hotels (incl. Qwen);
   synthetic at rho=0.99 is not what sceptics doubt.
G. White-box check of the "reweighting fixed features" assumption (probe length/quality directions before and after
   DPO with/without ties). Interesting but needs rented GPUs and is a second project; mention in stage 2.
H. Tie training for RLVR (theory + method). Rejected: theory-heavy, authors are presumably doing it.
I. Compare with DPO tie-aware losses (Rao-Kupper / Davidson from Chen et al.). Cheap add-on but needs a custom loss
   on Tinker; left as optional stage 2 arm.
J. Tie training vs consistency training head-to-head on sycophancy. Rejected: different data regimes, large design
   space, 2606.03810 already covers consistency training broadly.
K. Human-declared ties (MultiPref) as training ties. Partially used in A as an evaluation set (human strict labels
   split by length alignment); as a training source MultiPref is small (10k comparisons, mixed annotator votes) —
   stage 2.

Only one proposal allowed; A dominates on feasibility, cost, and "interesting either way".
